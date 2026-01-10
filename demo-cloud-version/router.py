"""
Query Router Module - Intelligent Pipeline Selection.

This module implements complexity-based routing to determine whether queries
should be processed via the fast lane (direct response) or deep lane (full
council deliberation). Uses LLM-based complexity scoring with manual override
capability.

Routing Logic:
    - FAST_LANE (score <= 4): Simple queries bypassing council assembly.
    - DEEP_LANE (score > 4): Complex queries requiring full deliberation.
"""

import dspy
import time
from config import BOSS_MODEL


def retry_with_backoff(func, max_retries=3, base_delay=1.0):
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise Exception(f"Failed after {max_retries} attempts: {str(e)}")
            delay = base_delay * (2 ** attempt)
            time.sleep(delay)


class AssessComplexity(dspy.Signature):
    """
    Signature for query complexity assessment and routing decision.
    
    Evaluates incoming query to determine appropriate processing pipeline
    based on strategic complexity scoring.
    """
    query = dspy.InputField(desc="The user's question or command")
    complexity_score = dspy.OutputField(desc="A score between 1.0 (Trivial) and 10.0 (Highly Strategic)")
    reasoning = dspy.OutputField(desc="Brief justification for the score")
    route = dspy.OutputField(desc="Must be exactly 'FAST_LANE' or 'DEEP_LANE'")


class RouterModule(dspy.Module):
    """
    Query complexity router with chain-of-thought reasoning.
    
    Analyzes query complexity and produces routing decision with
    score normalization and fallback handling.
    """
    
    def __init__(self):
        super().__init__()
        self.lm = BOSS_MODEL
        self.assess = dspy.ChainOfThought(AssessComplexity)

    def forward(self, query):
        """
        Evaluate query and produce routing prediction.

        Args:
            query: User input string for complexity assessment.

        Returns:
            dspy.Prediction: Contains route, score, and reasoning fields.
        """
        def execute():
            with dspy.context(lm=self.lm):
                result = self.assess(query=query)

                try:
                    score = float(result.complexity_score)
                except:
                    score = 5.0

                final_route = "DEEP_LANE" if score > 4 else "FAST_LANE"

                return dspy.Prediction(
                    route=final_route,
                    score=score,
                    reasoning=result.reasoning
                )

        return retry_with_backoff(execute)


def route_query(query_text, force_deep=False):
    """
    Primary routing interface with manual override support.
    
    Args:
        query_text: User query string for routing evaluation.
        force_deep: If True, bypasses AI assessment and routes directly
                    to DEEP_LANE for full council assembly.
                    
    Returns:
        dspy.Prediction: Routing decision with score and reasoning.
    """
    if force_deep:
        return dspy.Prediction(
            route="DEEP_LANE",
            score=10.0,
            reasoning="MANUAL OVERRIDE: User requested Council assembly explicitly."
        )

    router = RouterModule()
    return router(query=query_text)
