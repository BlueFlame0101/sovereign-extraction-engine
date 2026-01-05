import time

def search_graph_rag(query, department_focus):
    """
    Henter data fra firmaets videns-graf.
    Alle 3 medarbejdere får præcis denne samme data-pakke.
    """
    print(f"   🔍 [GraphRAG] Querying secure vault for context related to: {department_focus}...")

    # Simuleret firma-data (Dette ville komme fra din Vector DB i fremtiden)
    common_knowledge = """
    [CONFIDENTIAL COMPANY DATA]
    1. Financials: Current burn rate is $50k/month. Cash runway: 18 months.
    2. Growth: User base grew 15% last Q, but churn is high (5%) in Enterprise sector.
    3. Tech: The legacy servers are crashing daily. Migration to AWS is approved but paused due to cost.
    4. Strategy: CEO wants to focus on "Product-Led Growth" in 2025.
    5. Personnel: Hiring freeze is active for all non-engineering roles.
    """

    return common_knowledge
