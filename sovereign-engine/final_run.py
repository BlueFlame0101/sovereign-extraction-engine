from macro_council import convene_council
import time

if __name__ == "__main__":
    # Et komplekst dilemma, der kræver balance (Persona C)
    user_query = "Should we authorize the $20k server upgrade now, even though Q4 budget is tight?"
    
    start_time = time.time()
    result = convene_council(user_query)
    end_time = time.time()
    
    # HER ER OUTPUTTET TIL BRUGEREN
    print("\n" + "="*80)
    print("🧠 THE SOVEREIGN'S INTERNAL MONOLOGUE (Tanker & Analyse)")
    print("="*80)
    print(result.internal_thought_process)
    
    print("\n" + "="*80)
    print("📜 FINAL DIRECTIVE (Den Endelige Beslutning)")
    print("="*80)
    print(result.final_decision)
    
    print("\n" + "-"*80)
    print(f"⚡ Execution Complete in {end_time - start_time:.1f} seconds.")
