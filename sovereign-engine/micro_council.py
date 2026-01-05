"""
Micro Council Module - Departmental Worker Deliberation Engine.

This module implements the first phase of the hierarchical decision pipeline:
micro-level deliberation within each department. Each department consists of
3 worker agents that draft responses, cross-review each other's work, and
a department head that synthesizes the final departmental report.

Architecture:
    - 3 Departments: Finance, Growth, Tech
    - 3 Workers per Department: Mistral, Gemma, Llama
    - 1 Department Head: Llama-70B (synthesis role)
    - Peer Review Protocol: Cross-validation scoring

DSPy Signatures:
    - DraftSignature: Worker generates answer using RAG context
    - PeerReviewSignature: Worker scores colleague's draft
    - BossSignature: Department head synthesizes final report
"""

import dspy
from config import TEAM_FINANCE, TEAM_GROWTH, TEAM_TECH, BOSS_MODEL
from retriever import search_graph_rag


# --- DSPy Signatures ---

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


# --- Department Engine ---

class Department(dspy.Module):
    """
    Departmental deliberation engine with worker agents and synthesis.
    
    Orchestrates the micro-council workflow: RAG retrieval, parallel
    drafting by 3 workers, cross-peer review, and boss synthesis.
    
    Attributes:
        name: Department identifier (FINANCE, GROWTH, TECH)
        goal: Department's optimization objective
        workers: List of 3 DSPy language model instances
        boss_lm: Department head's language model
    """
    
    def __init__(self, name, goal, team_models):
        """
        Initialize department with name, goal, and worker models.
        
        Args:
            name: Department name for logging and identification
            goal: Strategic objective (e.g., 'Maximize ROI')
            team_models: List of 3 DSPy language model instances
        """
        super().__init__()
        self.name = name
        self.goal = goal
        self.workers = team_models
        self.boss_lm = BOSS_MODEL

        self.drafter = dspy.Predict(DraftSignature)
        self.reviewer = dspy.Predict(PeerReviewSignature)
        self.boss = dspy.Predict(BossSignature)

    def forward(self, query):
        """
        Execute full departmental deliberation pipeline.
        
        Workflow:
            1. RAG retrieval for department-specific context
            2. Parallel drafting by 3 worker agents
            3. Cross-peer review with scoring
            4. Boss synthesis of final departmental report
        
        Args:
            query: Strategic question requiring departmental analysis
            
        Returns:
            str: Synthesized departmental report for macro-council
        """
        print(f"\n[{self.name}] ACTIVATING TEAM (3 WORKERS + BOSS)")

        # Phase 1: RAG Context Retrieval
        context = search_graph_rag(query, self.name)

        # Phase 2: Parallel Drafting
        drafts = []
        worker_names = ["Worker 1 (Mistral)", "Worker 2 (Gemma)", "Worker 3 (Llama)"]

        for i in range(3):
            model = self.workers[i]
            print(f"   |- {worker_names[i]} drafting...", end="", flush=True)

            with dspy.context(lm=model):
                res = self.drafter(department_goal=self.goal, rag_context=context, query=query)
                drafts.append(res.draft_answer)
            print(" [DONE]")

        # Phase 3: Cross-Peer Review Protocol
        print("   |- Internal Peer Review Protocol...")
        reviews = []
        peer_map = [[1, 2], [0, 2], [0, 1]]

        for i in range(3):
            scores = []
            for judge_idx in peer_map[i]:
                judge_model = self.workers[judge_idx]
                print(f"   |  {worker_names[judge_idx]} reviewing Draft {i+1}...", end="", flush=True)

                with dspy.context(lm=judge_model):
                    res = self.reviewer(department_goal=self.goal, proposal_text=drafts[i])
                    try:
                        s = float(str(res.score).split('/')[0].strip())
                    except:
                        s = 5.0
                    scores.append(s)
                print(f" Score: {s}")
            reviews.append(scores)

        # Phase 4: Boss Synthesis
        print(f"   |- {self.name} HEAD synthesizing...", end="", flush=True)
        report = ""
        for i in range(3):
            avg = sum(reviews[i])/len(reviews[i])
            report += f"\n[DRAFT {i+1}]: {drafts[i][:150]}... (Avg: {avg})"

        with dspy.context(lm=self.boss_lm):
            final = self.boss(department_goal=self.goal, query=query, report_data=report)
        print(" [DECISION MADE]")

        return final.final_answer


# --- Public API ---

def consult_finance(query):
    """
    Invoke Finance department deliberation.
    
    Args:
        query: Strategic question for financial analysis
        
    Returns:
        str: Finance department's synthesized report
    """
    return Department("FINANCE DEPT", "Maximize ROI", TEAM_FINANCE)(query)


def consult_growth(query):
    """
    Invoke Growth department deliberation.
    
    Args:
        query: Strategic question for growth analysis
        
    Returns:
        str: Growth department's synthesized report
    """
    return Department("GROWTH DEPT", "Maximize User Base", TEAM_GROWTH)(query)


def consult_tech(query):
    """
    Invoke Tech department deliberation.
    
    Args:
        query: Strategic question for technical analysis
        
    Returns:
        str: Tech department's synthesized report
    """
    return Department("TECH DEPT", "System Stability", TEAM_TECH)(query)
