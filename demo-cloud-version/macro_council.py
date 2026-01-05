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
import config

class OpeningSignature(dspy.Signature):
    role = dspy.InputField()
    query = dspy.InputField()
    micro_reports = dspy.InputField()
    argument = dspy.OutputField()

class RebuttalSignature(dspy.Signature):
    role = dspy.InputField()
    my_argument = dspy.InputField()
    opponent_arguments = dspy.InputField()
    rebuttal = dspy.OutputField()

class SovereignSignature(dspy.Signature):
    query = dspy.InputField()
    persona = dspy.InputField()
    cfo_pos = dspy.InputField()
    cmo_pos = dspy.InputField()
    cto_pos = dspy.InputField()
    internal_thought_process = dspy.OutputField()
    final_decision = dspy.OutputField()

class DepartmentHead(dspy.Module):
    def __init__(self, role, model):
        super().__init__()
        self.role = role
        self.lm = model
        self.opener = dspy.Predict(OpeningSignature)
        self.reply = dspy.Predict(RebuttalSignature)

    def give_opening(self, report, query):
        with dspy.context(lm=self.lm):
            return self.opener(role=self.role, query=query, micro_reports=report).argument

    def give_rebuttal(self, my_arg, context):
        with dspy.context(lm=self.lm):
            return self.reply(role=self.role, my_argument=my_arg, opponent_arguments=context).rebuttal

class Sovereign(dspy.Module):
    def __init__(self):
        super().__init__()
        self.lm = config.get_sovereign_model()
        self.brain = dspy.Predict(SovereignSignature)

    def forward(self, query, persona, args, rebuttals):
        with dspy.context(lm=self.lm):
            return self.brain(
                query=query,
                persona=persona,
                cfo_pos=f"Argument: {args['fin']} | Rebuttal: {rebuttals['fin']}",
                cmo_pos=f"Argument: {args['gro']} | Rebuttal: {rebuttals['gro']}",
                cto_pos=f"Argument: {args['tec']} | Rebuttal: {rebuttals['tec']}"
            )