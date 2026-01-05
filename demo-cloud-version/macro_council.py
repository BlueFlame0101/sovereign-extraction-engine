import dspy
from config import BOSS_MODEL, get_cfo_model, get_cmo_model, get_cto_model
from micro_council import consult_finance, consult_growth, consult_tech

# --- 1. SIGNATURER ---

class OpeningStatement(dspy.Signature):
    """You are a C-Level Executive. Read your team's report.
    Argue FIERCELY for your department's KPI using the data provided.
    """
    role = dspy.InputField()
    dept_report = dspy.InputField()
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
    
    YOUR CURRENT PERSONA/STRATEGY: {sovereign_persona}
    
    1. Analyze the triangular conflict (Finance vs Growth vs Tech).
    2. Evaluate the rebuttals based on your Persona Strategy.
    3. Synthesize a final verdict.
    """
    sovereign_persona = dspy.InputField(desc="The strategic lens to view this decision")
    query = dspy.InputField()
    
    finance_arg = dspy.InputField()
    growth_arg = dspy.InputField()
    tech_arg = dspy.InputField()
    
    finance_rebuttal = dspy.InputField()
    growth_rebuttal = dspy.InputField()
    tech_rebuttal = dspy.InputField()
    
    internal_thought_process = dspy.OutputField(desc="Deep analysis showing your reasoning")
    final_decision = dspy.OutputField(desc="Final directive")

# --- 2. MODULER ---

class DepartmentHead(dspy.Module):
    def __init__(self, role, specific_model):
        super().__init__()
        self.role = role
        self.lm = specific_model
        self.opener = dspy.Predict(OpeningStatement)
        self.reply = dspy.Predict(Rebuttal)

    def give_opening(self, report, query):
        with dspy.context(lm=self.lm):
            return self.opener(role=self.role, dept_report=report, query=query).argument

    def give_rebuttal(self, my_arg, other_args):
        with dspy.context(lm=self.lm):
            return self.reply(role=self.role, my_position=my_arg, opponent_arguments=other_args).rebuttal

class Sovereign(dspy.Module):
    def __init__(self):
        super().__init__()
        self.lm = BOSS_MODEL
        self.brain = dspy.Predict(SovereignThinking)

    def forward(self, query, persona, args, rebuttals):
        with dspy.context(lm=self.lm):
            return self.brain(
                query=query,
                sovereign_persona=persona, # Her sender vi strategien ind
                finance_arg=args['fin'], growth_arg=args['gro'], tech_arg=args['tec'],
                finance_rebuttal=rebuttals['fin'], growth_rebuttal=rebuttals['gro'], tech_rebuttal=rebuttals['tec']
            )

# (Vi behøver ikke convene_council her mere, da Dashboardet styrer flowet)
