"""
Macro Council Module - Executive Debate and Sovereign Synthesis.

This module implements the second phase of the hierarchical decision
pipeline: the macro-level council where C-Level executives (CFO, CMO, COO)
engage in structured debate using departmental reports.

Architecture:
    - DepartmentHead: Generates opening arguments and rebuttals per role
    - Sovereign: Final arbiter that synthesizes executive debate into verdict
"""

import dspy

# --- DSPy Signatures ---

class OpeningStatement(dspy.Signature):
    """You are a C-Level Executive. Read your team's report.
    Argue FIERCELY for your department's KPI using the data provided.
    """
    role = dspy.InputField()
    query = dspy.InputField()
    argument = dspy.OutputField(desc="Primary argument (Max 3 sentences)")


class Rebuttal(dspy.Signature):
    """You are a C-Level Executive. Read the arguments from the other two chiefs.
    Destroy their logic if it threatens your department.
    """
    role = dspy.InputField()
    my_position = dspy.InputField()
    opponent_arguments = dspy.InputField()
    rebuttal = dspy.OutputField(desc="Counter-argument")


class SovereignThinking(dspy.Signature):
    """You are THE SOVEREIGN.
    1. Analyze the triangular conflict (Finance vs Growth vs Ops).
    2. Evaluate the rebuttals based on your Persona Strategy.
    3. Synthesize a final verdict.
    """
    query = dspy.InputField()
    
    finance_arg = dspy.InputField()
    growth_arg = dspy.InputField()
    ops_arg = dspy.InputField()
    
    finance_rebuttal = dspy.InputField()
    growth_rebuttal = dspy.InputField()
    ops_rebuttal = dspy.InputField()
    
    internal_thought_process = dspy.OutputField(desc="Deep analysis showing your reasoning")
    final_decision = dspy.OutputField(desc="Final directive")


# --- DSPy Modules ---

class DepartmentHead(dspy.Module):
    def __init__(self, role, model):
        super().__init__()
        self.role = role
        self.lm = model
        self.opener = dspy.Predict(OpeningStatement)
        self.reply = dspy.Predict(Rebuttal)

    def give_opening(self, query):
        with dspy.context(lm=self.lm):
            return self.opener(role=self.role, query=query).argument

    def give_rebuttal(self, my_arg, other_args):
        with dspy.context(lm=self.lm):
            return self.reply(role=self.role, my_position=my_arg, opponent_arguments=other_args).rebuttal


class Sovereign(dspy.Module):
    def __init__(self, model):
        super().__init__()
        self.lm = model
        self.brain = dspy.Predict(SovereignThinking)

    def forward(self, query, args, rebuttals):
        with dspy.context(lm=self.lm):
            return self.brain(
                query=query,
                finance_arg=args['fin'], growth_arg=args['gro'], ops_arg=args['ops'],
                finance_rebuttal=rebuttals['fin'], growth_rebuttal=rebuttals['gro'], ops_rebuttal=rebuttals['ops']
            )

# --- Orchestration Logic ---

def run_council_meeting(query, cfo_model, cmo_model, coo_model):
    """
    Orchestrates the council meeting using injected models.
    """
    
    # 1. Initialize Agents (Using the models passed from dashboard)
    cfo = DepartmentHead("CFO", cfo_model)
    cmo = DepartmentHead("CMO", cmo_model)
    coo = DepartmentHead("COO", coo_model)
    sov = Sovereign(coo_model) 

    # 2. Opening Arguments
    args = {
        'fin': cfo.give_opening(query),
        'gro': cmo.give_opening(query),
        'ops': coo.give_opening(query)
    }

    # 3. Rebuttals
    rebuttals = {
        'fin': cfo.give_rebuttal(args['fin'], f"CMO: {args['gro']} | COO: {args['ops']}"),
        'gro': cmo.give_rebuttal(args['gro'], f"CFO: {args['fin']} | COO: {args['ops']}"),
        'ops': coo.give_rebuttal(args['ops'], f"CFO: {args['fin']} | CMO: {args['gro']}")
    }

    # 4. Sovereign Decision
    verdict = sov.forward(query, args, rebuttals)

    # 5. Format Professional Report
    return f"""
    ### Executive Arguments
    **CFO:** {args['fin']}
    **CMO:** {args['gro']}
    **COO:** {args['ops']}
    
    ### Rebuttals
    **CFO Rebuttal:** {rebuttals['fin']}
    **CMO Rebuttal:** {rebuttals['gro']}
    **COO Rebuttal:** {rebuttals['ops']}

    ---
    ### 🏛️ Sovereign Decree
    **Reasoning:** {verdict.internal_thought_process}
    
    **Directive:** {verdict.final_decision}
    """