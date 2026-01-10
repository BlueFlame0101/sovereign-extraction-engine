import dspy
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from config import TEAM_FINANCE, TEAM_GROWTH, TEAM_TECH, BOSS_MODEL
from retriever import search_graph_rag


def retry_with_backoff(func, max_retries=3, base_delay=1.0):
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise Exception(f"Failed after {max_retries} attempts: {str(e)}")
            delay = base_delay * (2 ** attempt)
            print(f" [RETRY {attempt + 1}/{max_retries} after {delay}s]", end="", flush=True)
            time.sleep(delay)


class DraftSignature(dspy.Signature):
    """You are a specialized employee. Use the RAG Context to answer based on your Department Goal."""
    department_goal = dspy.InputField()
    rag_context = dspy.InputField()
    query = dspy.InputField()
    draft_answer = dspy.OutputField(desc="Detailed answer based on context")


class PeerReviewSignature(dspy.Signature):
    """Review a colleague's draft strictly. Rate 1-10."""
    department_goal = dspy.InputField()
    proposal_text = dspy.InputField()
    score = dspy.OutputField(desc="Score 1-10 (float)")
    critique = dspy.OutputField(desc="Short critique")


class BossSignature(dspy.Signature):
    """Synthesize the department's final answer based on the 3 drafts and their ratings."""
    department_goal = dspy.InputField()
    query = dspy.InputField()
    report_data = dspy.InputField()
    final_answer = dspy.OutputField()


class DataAnalystSignature(dspy.Signature):
    """Extract quantitative insights and key metrics from RAG context. Focus on numbers, trends, and measurable data points."""
    query = dspy.InputField()
    rag_context = dspy.InputField()
    quantitative_summary = dspy.OutputField(desc="Key metrics and data points")


class StrategicAdvisorSignature(dspy.Signature):
    """Provide meta-analysis of all department reports. Identify consensus, conflicts, and strategic blind spots."""
    query = dspy.InputField()
    finance_report = dspy.InputField()
    growth_report = dspy.InputField()
    tech_report = dspy.InputField()
    meta_analysis = dspy.OutputField(desc="Cross-departmental strategic assessment")


class Department(dspy.Module):
    def __init__(self, name, goal, team_models):
        super().__init__()
        self.name = name
        self.goal = goal
        self.workers = team_models
        self.boss_lm = BOSS_MODEL
        self.boss = dspy.Predict(BossSignature)

    def _draft_worker(self, worker_id, model, context, query):
        def execute():
            drafter = dspy.Predict(DraftSignature)
            with dspy.context(lm=model):
                res = drafter(department_goal=self.goal, rag_context=context, query=query)
                return res.draft_answer
        return retry_with_backoff(execute)

    def _review_draft(self, judge_model, draft_text):
        def execute():
            reviewer = dspy.Predict(PeerReviewSignature)
            with dspy.context(lm=judge_model):
                res = reviewer(department_goal=self.goal, proposal_text=draft_text)
                try:
                    score = float(str(res.score).split('/')[0].strip())
                except:
                    score = 5.0
                return score
        return retry_with_backoff(execute)

    def forward(self, query):
        print(f"\n[{self.name}] ACTIVATING TEAM (3 WORKERS + BOSS)")

        context = search_graph_rag(query, self.name)

        worker_names = ["Worker 1 (Mistral)", "Worker 2 (Gemma)", "Worker 3 (Llama)"]

        print(f"   |- All 3 workers drafting in parallel...")
        with ThreadPoolExecutor(max_workers=3) as executor:
            draft_futures = {
                executor.submit(self._draft_worker, i, self.workers[i], context, query): i
                for i in range(3)
            }
            drafts = [None] * 3
            for future in as_completed(draft_futures):
                worker_id = draft_futures[future]
                drafts[worker_id] = future.result()
        print(" [DONE]")

        print("   |- Peer review protocol (6 reviews in parallel)...")
        peer_map = [[1, 2], [0, 2], [0, 1]]
        with ThreadPoolExecutor(max_workers=6) as executor:
            review_futures = []
            for i in range(3):
                for judge_idx in peer_map[i]:
                    future = executor.submit(self._review_draft, self.workers[judge_idx], drafts[i])
                    review_futures.append((i, future))

            all_scores = []
            for i in range(3):
                scores_for_draft = []
                for draft_id, future in review_futures:
                    if draft_id == i:
                        scores_for_draft.append(future.result())
                all_scores.extend(scores_for_draft)

        reviews = []
        score_idx = 0
        for i in range(3):
            scores = [all_scores[score_idx], all_scores[score_idx + 1]]
            reviews.append(scores)
            score_idx += 2
        print(" [DONE]")

        print(f"   |- {self.name} HEAD synthesizing...", end="", flush=True)
        report = ""
        for i in range(3):
            avg = sum(reviews[i])/len(reviews[i])
            report += f"\n[DRAFT {i+1}]: {drafts[i][:150]}... (Avg: {avg})"

        def execute_boss():
            with dspy.context(lm=self.boss_lm):
                final = self.boss(department_goal=self.goal, query=query, report_data=report)
                return final.final_answer

        result = retry_with_backoff(execute_boss)
        print(" [DECISION MADE]")
        return result


def consult_finance(query):
    return Department("FINANCE DEPT", "Maximize ROI", TEAM_FINANCE)(query)


def consult_growth(query):
    return Department("GROWTH DEPT", "Maximize User Base", TEAM_GROWTH)(query)


def consult_tech(query):
    return Department("TECH DEPT", "System Stability", TEAM_TECH)(query)


def consult_data_analyst(query):
    print("\n[DATA ANALYST] ACTIVATING (Specialist Agent)")

    context_finance = search_graph_rag(query, "FINANCE DEPT")
    context_growth = search_graph_rag(query, "GROWTH DEPT")
    context_tech = search_graph_rag(query, "TECH DEPT")

    combined_context = f"FINANCE:\n{context_finance}\n\nGROWTH:\n{context_growth}\n\nTECH:\n{context_tech}"

    print("   |- Analyzing quantitative data across all departments...", end="", flush=True)
    analyst = dspy.Predict(DataAnalystSignature)

    def execute():
        with dspy.context(lm=BOSS_MODEL):
            result = analyst(query=query, rag_context=combined_context)
            return result.quantitative_summary

    result = retry_with_backoff(execute)
    print(" [ANALYSIS COMPLETE]")
    return result


def consult_strategic_advisor(query, finance_report, growth_report, tech_report):
    print("\n[STRATEGIC ADVISOR] ACTIVATING (Specialist Agent)")
    print("   |- Performing meta-analysis of all departmental reports...", end="", flush=True)

    advisor = dspy.Predict(StrategicAdvisorSignature)

    def execute():
        with dspy.context(lm=BOSS_MODEL):
            result = advisor(
                query=query,
                finance_report=finance_report,
                growth_report=growth_report,
                tech_report=tech_report
            )
            return result.meta_analysis

    result = retry_with_backoff(execute)
    print(" [META-ANALYSIS COMPLETE]")
    return result