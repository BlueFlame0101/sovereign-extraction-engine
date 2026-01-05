from router import route_query
import time

def test_routing():
    print("--- 🚦 STARTING ROUTER DIAGNOSTICS ---")

    # Scenario A: Simpelt spørgsmål (Reflex) - Forventer FAST_LANE
    q1 = "What is the capital of Denmark?"
    print(f"\n🧪 TEST CASE A (Simple): '{q1}'")
    res1 = route_query(q1)
    print(f"   -> DECISION: {res1.route}")
    print(f"   -> SCORE:    {res1.score}/10")
    print(f"   -> REASON:   {res1.reasoning}")

    # Scenario B: Komplekst spørgsmål (Reasoning) - Forventer DEEP_LANE
    q2 = "Analyze the strategic risks of migrating our on-prem servers to AWS given a budget cut of 20%."
    print(f"\n🧪 TEST CASE B (Complex): '{q2}'")
    res2 = route_query(q2)
    print(f"   -> DECISION: {res2.route}")
    print(f"   -> SCORE:    {res2.score}/10")
    print(f"   -> REASON:   {res2.reasoning}")

    # Scenario C: Override (User Agency) - Forventer DEEP_LANE trods simpelt spørgsmål
    q3 = "What is 2+2?"
    print(f"\n🧪 TEST CASE C (Force Override): '{q3}'")
    res3 = route_query(q3, force_deep=True)
    print(f"   -> DECISION: {res3.route}")
    print(f"   -> SCORE:    {res3.score}/10")
    print(f"   -> REASON:   {res3.reasoning}")

    print("\n--- 🏁 DIAGNOSTICS COMPLETE ---")

if __name__ == "__main__":
    test_routing()
