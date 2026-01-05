from micro_council import consult_finance, consult_growth, consult_tech
import time

def run_full_council():
    query = "Should we pause the AWS migration to save cash?"
    print(f"🚨 QUERY: {query}\n")

    # 1. Finans Teamet (3 Modeller)
    print("--- CALLING FINANCE TEAM ---")
    res_fin = consult_finance(query)
    print(f"💰 RESULT: {res_fin[:100]}...\n")

    # 2. Vækst Teamet (3 Modeller)
    print("--- CALLING GROWTH TEAM ---")
    res_growth = consult_growth(query)
    print(f"📈 RESULT: {res_growth[:100]}...\n")

    # 3. Tech Teamet (3 Modeller)
    print("--- CALLING TECH TEAM ---")
    res_tech = consult_tech(query)
    print(f"💻 RESULT: {res_tech[:100]}...\n")

if __name__ == "__main__":
    run_full_council()
