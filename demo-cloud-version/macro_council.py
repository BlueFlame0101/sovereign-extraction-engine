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
import time
import config


def retry_with_backoff(func, max_retries=3, base_delay=1.0):
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise Exception(f"Failed after {max_retries} attempts: {str(e)}")
            delay = base_delay * (2 ** attempt)
            print(f" [RETRY {attempt + 1}/{max_retries} after {delay}s]", end="", flush=True)
            time.sleep(delay)

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
        def execute():
            with dspy.context(lm=self.lm):
                return self.opener(role=self.role, query=query, micro_reports=report).argument
        return retry_with_backoff(execute)

    def give_rebuttal(self, my_arg, context):
        def execute():
            with dspy.context(lm=self.lm):
                return self.reply(role=self.role, my_argument=my_arg, opponent_arguments=context).rebuttal
        return retry_with_backoff(execute)

class Sovereign(dspy.Module):
    def __init__(self):
        super().__init__()
        self.lm = config.get_sovereign_model()
        self.brain = dspy.Predict(SovereignSignature)

    def forward(self, query, persona, args, rebuttals):
        def execute():
            with dspy.context(lm=self.lm):
                return self.brain(
                    query=query,
                    persona=persona,
                    cfo_pos=f"Argument: {args['fin']} | Rebuttal: {rebuttals['fin']}",
                    cmo_pos=f"Argument: {args['gro']} | Rebuttal: {rebuttals['gro']}",
                    cto_pos=f"Argument: {args['tec']} | Rebuttal: {rebuttals['tec']}"
                )
        return retry_with_backoff(execute)