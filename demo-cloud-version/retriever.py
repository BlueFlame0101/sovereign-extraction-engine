import chromadb
from chromadb.config import Settings


client = chromadb.Client(Settings(anonymized_telemetry=False))

try:
    collection = client.get_collection("company_knowledge")
except:
    collection = client.create_collection("company_knowledge")

    documents = [
        "Current burn rate is $50k per month with 18 months of runway remaining. Q4 expenses exceeded budget by 12%.",
        "AWS migration project is approved but paused due to cost concerns. Estimated cost: $15k/month vs current $8k/month.",
        "Engineering headcount budget is frozen except for critical backend roles. Sales hiring is completely frozen.",
        "User base grew 15% last quarter, reaching 12,000 active users. However, enterprise churn rate is 5% monthly.",
        "Product-led growth is the 2025 strategic priority per CEO directive. Focus on self-service onboarding.",
        "Competitor analysis shows we're 30% cheaper but lack enterprise features like SSO and audit logs.",
        "Legacy on-premise servers are experiencing daily crashes. Uptime SLA is currently at 94% (target: 99.5%).",
        "Technical debt backlog estimated at 400 engineering hours. Priority items: database migration, API refactor.",
        "Security audit identified 3 critical vulnerabilities. Remediation required before enterprise sales can proceed.",
        "Kubernetes migration is 60% complete. Remaining work: database stateful sets and monitoring integration.",
    ]

    metadatas = [
        {"department": "FINANCE", "source": "CFO Q4 Report"},
        {"department": "FINANCE", "source": "Infrastructure Budget"},
        {"department": "FINANCE", "source": "HR Policy Doc"},
        {"department": "GROWTH", "source": "Growth Metrics Dashboard"},
        {"department": "GROWTH", "source": "Strategy Memo 2025"},
        {"department": "GROWTH", "source": "Competitive Intelligence"},
        {"department": "TECH", "source": "Incident Reports"},
        {"department": "TECH", "source": "Engineering Roadmap"},
        {"department": "TECH", "source": "Security Audit"},
        {"department": "TECH", "source": "Infrastructure Status"},
    ]

    ids = [f"doc_{i}" for i in range(len(documents))]

    collection.add(documents=documents, metadatas=metadatas, ids=ids)


def search_graph_rag(query, department_focus):
    print(f"   [GraphRAG] Querying vector store for: {department_focus}...")

    dept_key = department_focus.split()[0] if department_focus else None

    if dept_key and dept_key in ["FINANCE", "GROWTH", "TECH"]:
        results = collection.query(
            query_texts=[query],
            n_results=3,
            where={"department": dept_key}
        )
    else:
        results = collection.query(
            query_texts=[query],
            n_results=3
        )

    if results['documents'] and len(results['documents'][0]) > 0:
        context_blocks = []
        for i, doc in enumerate(results['documents'][0]):
            source = results['metadatas'][0][i].get('source', 'Unknown')
            context_blocks.append(f"[{source}]: {doc}")
        return "\n\n".join(context_blocks)
    else:
        return "[No relevant context found in knowledge base]"
