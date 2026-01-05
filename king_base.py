"""
Council Debate Engine - Multi-Agent Deliberation System.

This module implements a round-table debate pattern where multiple LLM agents
with distinct personas engage in structured argumentation. A sovereign arbiter
synthesizes the final decision using a higher-capacity model.

Architecture:
    - Worker Agents: Low-latency models for rapid inference during debate rounds.
    - Sovereign Agent: High-capacity model for final verdict synthesis.
    - Shared Context: Cumulative transcript enabling cross-agent awareness.
"""

import dspy
import os

# Model Configuration
expert_lm = dspy.LM(model='openrouter/google/gemini-3-flash-preview', api_key=os.getenv("OPENROUTER_API_KEY"), api_base="https://openrouter.ai/api/v1")
leader_lm = dspy.LM(model='openrouter/meta-llama/llama-3.3-70b-instruct', api_key=os.getenv("OPENROUTER_API_KEY"), api_base="https://openrouter.ai/api/v1")

dspy.settings.configure(lm=expert_lm)


class DebateTurn(dspy.Signature):
    """
    Signature for a single debate turn within the council deliberation.
    
    Enables context-aware response generation by providing full discussion
    history, allowing agents to reference and rebut prior arguments.
    """
    
    role = dspy.InputField(desc="Agent persona identifier")
    objective = dspy.InputField(desc="Strategic objective guiding argumentation")
    discussion_log = dspy.InputField(desc="Cumulative transcript of prior exchanges")
    
    current_stance = dspy.OutputField(desc="Condensed position statement")
    response = dspy.OutputField(desc="Contextual response addressing prior arguments")


class CouncilMember:
    """
    Individual debate agent with persistent persona and objective.
    
    Attributes:
        name: Agent identifier for transcript attribution.
        role: Persona defining argumentation style and domain focus.
        objective: Strategic goal influencing response generation.
        brain: DSPy predictor with chain-of-thought reasoning.
    """
    
    def __init__(self, name, role, objective):
        self.name = name
        self.role = role
        self.objective = objective
        self.brain = dspy.ChainOfThought(DebateTurn)
    
    def speak(self, history):
        """
        Generate contextual response based on debate transcript.
        
        Args:
            history: Full transcript of preceding debate exchanges.
            
        Returns:
            str: Agent's response to current debate state.
        """
        pred = self.brain(
            role=self.role, 
            objective=self.objective, 
            discussion_log=history
        )
        return pred.response


class FinalVerdict(dspy.Signature):
    """
    Signature for sovereign arbiter's final decision synthesis.
    
    Processes complete debate transcript to produce executive verdict
    incorporating all perspectives and trade-offs.
    """
    debate_transcript = dspy.InputField()
    decision = dspy.OutputField(desc="Executive decision with resource allocation")


def run_round_table(topic, rounds=2):
    """
    Execute multi-round council deliberation on specified topic.
    
    Orchestrates debate flow across configured rounds, maintaining
    shared context for cross-agent argumentation. Concludes with
    sovereign synthesis using elevated model tier.
    
    Args:
        topic: Strategic question for council deliberation.
        rounds: Number of complete debate cycles. Default: 2.
        
    Side Effects:
        - Writes debate transcript and verdict to council_debate_log.txt
        - Prints real-time debate progress to stdout.
    """
    print(f"\n--- COUNCIL CONVENED: '{topic}' ---")
    
    council = [
        CouncilMember("Alpha", "Hardware Extremist", "Maksimer performance, ignorér pris."),
        CouncilMember("Beta", "Software Purist", "Alt skal løses med kode. Hardware er spild."),
        CouncilMember("Delta", "CFO (Finans)", "Spar penge. Stop unødvendige indkøb.")
    ]
    
    transcript = f"EMNE: {topic}\n"
    
    for r in range(1, rounds + 1):
        print(f"\n--- ROUND {r} ---")
        
        for member in council:
            response = member.speak(transcript)
            entry = f"\n[{member.name} ({member.role})]:\n{response}\n"
            transcript += entry
            print(f"[{member.name}]: {response[:100]}...")

    print("\n[SOVEREIGN] Synthesizing final verdict...")
    
    with dspy.context(lm=leader_lm):
        sov_brain = dspy.ChainOfThought(FinalVerdict)
        verdict = sov_brain(debate_transcript=transcript).decision
    
    print(f"\n{'='*40}\nDEBATE TRANSCRIPT:\n{transcript}\n{'='*40}")
    print(f"\nVERDICT:\n{verdict}")
    
    with open("council_debate_log.txt", "w", encoding="utf-8") as f:
        f.write(transcript + "\n\nVERDICT:\n" + verdict)


if __name__ == "__main__":
    spørgsmål = "Skal vi migrere vores database til Cloud eller bygge vores eget datacenter i kælderen?"
    run_round_table(spørgsmål, rounds=2)