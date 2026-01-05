import dspy
import os

# --- 1. SETUP ---
# Vi bruger en hurtig model til debatten, så det flyder let
expert_lm = dspy.LM(model='openrouter/google/gemini-3-flash-preview', api_key=os.getenv("OPENROUTER_API_KEY"), api_base="https://openrouter.ai/api/v1")
leader_lm = dspy.LM(model='openrouter/meta-llama/llama-3.3-70b-instruct', api_key=os.getenv("OPENROUTER_API_KEY"), api_base="https://openrouter.ai/api/v1")

dspy.settings.configure(lm=expert_lm)

# --- 2. DEBATTØRENS HJERNE ---
class DebateTurn(dspy.Signature):
    """Du deltager i en intens rundbordsdiskussion. Læs hvad de andre har sagt, og giv dit besyv med."""
    
    role = dspy.InputField(desc="Din rolle")
    objective = dspy.InputField(desc="Dit mål")
    
    # Her er nøglen: De får adgang til hele samtalens historik
    discussion_log = dspy.InputField(desc="Hvad de andre har sagt indtil nu")
    
    current_stance = dspy.OutputField(desc="Din nuværende holdning (kort)")
    response = dspy.OutputField(desc="Dit svar til rådet (reager på de andre)")

class CouncilMember:
    def __init__(self, name, role, objective):
        self.name = name
        self.role = role
        self.objective = objective
        self.brain = dspy.ChainOfThought(DebateTurn)
    
    def speak(self, history):
        # Agenten læser historikken og formulerer et svar
        pred = self.brain(
            role=self.role, 
            objective=self.objective, 
            discussion_log=history
        )
        return pred.response

# --- 3. ORDSTYREREN (THE SOVEREIGN) ---
class FinalVerdict(dspy.Signature):
    """Læs debatten og træf en endelig eksekutiv beslutning."""
    debate_transcript = dspy.InputField()
    decision = dspy.OutputField(desc="Endelig konklusion og budgetfordeling")

# --- 4. RUNDBORDS-MOTOREN ---
def run_round_table(topic, rounds=2):
    print(f"\n--- 🛡️ RÅDET MØDES OM: '{topic}' ---")
    
    # Vores deltagere
    council = [
        CouncilMember("Alpha", "Hardware Extremist", "Maksimer performance, ignorér pris."),
        CouncilMember("Beta", "Software Purist", "Alt skal løses med kode. Hardware er spild."),
        CouncilMember("Delta", "CFO (Finans)", "Spar penge. Stop unødvendige indkøb.")
    ]
    
    # Den fælles hukommelse (Transcript)
    transcript = f"EMNE: {topic}\n"
    
    # Vi kører et antal runder, så de kan nå at svare hinanden
    for r in range(1, rounds + 1):
        print(f"\n--- 🔄 RUNDE {r} ---")
        
        for member in council:
            # Hvert medlem får 'transcript' som input -> De ser hvad de andre lige har sagt
            response = member.speak(transcript)
            
            # Vi formaterer indlægget
            entry = f"\n[{member.name} ({member.role})]:\n{response}\n"
            
            # Opdaterer den fælles hukommelse
            transcript += entry
            
            # Live output
            print(f"🗣️ {member.name}: {response[:100]}...") # Viser preview

    # --- KONKLUSION ---
    print("\n👑 The Sovereign rejser sig for at tale...")
    
    # Lederen bruger den tunge model til at analysere hele debatten
    with dspy.context(lm=leader_lm):
        sov_brain = dspy.ChainOfThought(FinalVerdict)
        verdict = sov_brain(debate_transcript=transcript).decision
    
    print(f"\n{'='*40}\nREFERAT AF DEBATTEN:\n{transcript}\n{'='*40}")
    print(f"\nDOMMEN:\n{verdict}")
    
    # Gem til log
    with open("council_debate_log.txt", "w", encoding="utf-8") as f:
        f.write(transcript + "\n\nDOM:\n" + verdict)

# --- 5. EKSEKVERING ---
if __name__ == "__main__":
    spørgsmål = "Skal vi migrere vores database til Cloud eller bygge vores eget datacenter i kælderen?"
    run_round_table(spørgsmål, rounds=2)