import dspy
from config import TEAM_FINANCE, TEAM_GROWTH, TEAM_TECH, BOSS_MODEL
from retriever import search_graph_rag

# --- SIGNATURER ---
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

# --- DEPARTMENT ENGINE ---
class Department(dspy.Module):
    def __init__(self, name, goal, team_models):
        super().__init__()
        self.name = name
        self.goal = goal
        self.workers = team_models # Her modtager vi listen med de 3 modeller
        self.boss_lm = BOSS_MODEL

        self.drafter = dspy.Predict(DraftSignature)
        self.reviewer = dspy.Predict(PeerReviewSignature)
        self.boss = dspy.Predict(BossSignature)

    def forward(self, query):
        print(f"\n🏢 [{self.name}] ACTIVATING TEAM (3 WORKERS + BOSS)")

        # 1. RAG LOOKUP
        context = search_graph_rag(query, self.name)

        # 2. DRAFTING (3 Modeller arbejder parallelt)
        drafts = []
        worker_names = ["Worker 1 (Mistral)", "Worker 2 (Gemma)", "Worker 3 (Llama)"]

        for i in range(3):
            model = self.workers[i]
            print(f"   ├─ 🧠 {worker_names[i]} is drafting...", end="", flush=True)

            with dspy.context(lm=model):
                res = self.drafter(department_goal=self.goal, rag_context=context, query=query)
                drafts.append(res.draft_answer)
            print(" ✅ Done.")

        # 3. PEER REVIEW (Kryds-tjek internt i afdelingen)
        print("   ├─ ⚔️  Internal Peer Review Protocol...")
        reviews = []
        peer_map = [[1, 2], [0, 2], [0, 1]]

        for i in range(3):
            scores = []
            for judge_idx in peer_map[i]:
                judge_model = self.workers[judge_idx]
                print(f"   │  👀 {worker_names[judge_idx]} reviewing Draft {i+1}...", end="", flush=True)

                with dspy.context(lm=judge_model):
                    res = self.reviewer(department_goal=self.goal, proposal_text=drafts[i])
                    try:
                        s = float(str(res.score).split('/')[0].strip())
                    except:
                        s = 5.0
                    scores.append(s)
                print(f" Score: {s}")
            reviews.append(scores)

        # 4. BOSS SYNTHESIS
        print(f"   └─ 👔 {self.name} HEAD (Llama-70B) Synthesizing...", end="", flush=True)
        report = ""
        for i in range(3):
            avg = sum(reviews[i])/len(reviews[i])
            report += f"\n[DRAFT {i+1}]: {drafts[i][:150]}... (Avg: {avg})"

        with dspy.context(lm=self.boss_lm):
            final = self.boss(department_goal=self.goal, query=query, report_data=report)
        print(" ✅ Decision Made.")

        return final.final_answer

# --- EXPORT FUNCTIONS (Her kobler vi teams til afdelinger) ---
def consult_finance(query): 
    return Department("FINANCE DEPT", "Maximize ROI", TEAM_FINANCE)(query)

def consult_growth(query): 
    return Department("GROWTH DEPT", "Maximize User Base", TEAM_GROWTH)(query)

def consult_tech(query): 
    return Department("TECH DEPT", "System Stability", TEAM_TECH)(query)
