from micro_council import consult_finance, consult_growth, consult_tech
import time

def generate_official_reports():
    query = "Should we pause the AWS migration to save cash?"
    
    print(f"🚀 GENERATING DEPARTMENT REPORTS FOR QUERY: '{query}'")
    print("(Processen kører i baggrunden... vent venligst mens de 9 arbejdere tænker)\n")

    # Vi kører afdelingerne, men vi er ligeglade med live-loggen lige nu
    # Vi vil bare have slut-resultatet (return værdien)
    
    start = time.time()

    # 1. Hent Finans-rapporten
    print("   💰 Consultng Finance Dept...")
    report_finance = consult_finance(query)
    
    # 2. Hent Vækst-rapporten
    print("   📈 Consulting Growth Dept...")
    report_growth = consult_growth(query)
    
    # 3. Hent Tech-rapporten
    print("   💻 Consulting Tech Dept...")
    report_tech = consult_tech(query)
    
    duration = time.time() - start

    # --- HER ER DET DU SKAL SE ---
    # Dette er præcis den tekst, som Macro-rådet vil modtage
    
    print("\n" + "="*80)
    print(f"📂 OFFICIELLE AFDELINGSRAPPORTER (Genereret på {duration:.1f}s)")
    print("="*80)

    print(f"\n🏛️  AFDELING A: FINANS (Chef: Llama-3.3)")
    print("-" * 40)
    print(report_finance)
    print("-" * 40)

    print(f"\n🚀 AFDELING B: VÆKST (Chef: Llama-3.3)")
    print("-" * 40)
    print(report_growth)
    print("-" * 40)

    print(f"\n💾 AFDELING C: TECH (Chef: Llama-3.3)")
    print("-" * 40)
    print(report_tech)
    print("-" * 40)
    print("\n✅ Disse 3 tekster sendes videre til Macro-diskussionen.")

if __name__ == "__main__":
    generate_official_reports()
