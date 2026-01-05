"""
Micro Council Module - Departmental Worker Agent Orchestration.

This module implements the micro-intelligence layer of the council architecture.
Each department consists of 3 worker agents that draft responses, perform
cross-validation via peer review, and synthesize a final report through
a department head.

Workflow:
    1. RAG Context Retrieval: Query knowledge graph for relevant context.
    2. Parallel Drafting: 3 workers generate independent draft responses.
    3. Peer Review: Cross-validation scoring between workers.
    4. Boss Synthesis: Department head aggregates drafts weighted by peer scores.
"""
import dspy
import config

def run_worker(role, query, model):
    with dspy.context(lm=model):
        pred = dspy.Predict("role, query -> report")
        return pred(role=role, query=query).report

def consult_finance(query):
    model = config.get_finance_worker_1()
    return run_worker("Senior Financial Analyst", query, model)

def consult_growth(query):
    model = config.get_growth_worker_1()
    return run_worker("Market Research Specialist", query, model)

def consult_tech(query):
    model = config.get_tech_worker_1()
    return run_worker("Senior Tech Architect", query, model)