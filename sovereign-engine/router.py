"""
Semantic Complexity Router - Query Classification Pipeline.

This module implements the routing layer that classifies incoming queries
by semantic complexity, directing them to either the FAST_LANE (simple
responses) or DEEP_LANE (full council deliberation).

Architecture:
    - AssessComplexity: DSPy signature for complexity scoring
    - RouterModule: Chain-of-thought classification module
    - route_query: Public API with manual override capability

Routing Logic:
    - Score 1-4: FAST_LANE (direct response)
    - Score 5-10: DEEP_LANE (council assembly)
"""

import dspy
from config import lm


class AssessComplexity(dspy.Signature):
    """Analyze the query complexity to route it to the correct processing pipeline."""

    query = dspy.InputField(desc="The user's question or command")
    complexity_score = dspy.OutputField(desc="A score between 1.0 (Trivial) and 10.0 (Highly Strategic)")
    reasoning = dspy.OutputField(desc="Brief justification for the score")
    route = dspy.OutputField(desc="Must be exactly 'FAST_LANE' or 'DEEP_LANE'")


class RouterModule(dspy.Module):
    """
    Chain-of-thought query complexity classifier.
    
    Uses DSPy's ChainOfThought to analyze query complexity and
    produce routing decisions with confidence scores and reasoning.
    """
    
    def __init__(self):
        """Initialize router with complexity assessment signature."""
        super().__init__()
        self.assess = dspy.ChainOfThought(AssessComplexity)

    def forward(self, query):
        """
        Classify query complexity and determine routing lane.
        
        Args:
            query: User's input query for classification
            
        Returns:
            dspy.Prediction: Contains route, score, and reasoning
        """
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


def route_query(query_text, force_deep=False):
    """
    Route query to appropriate processing pipeline.
    
    Public API for query classification with optional manual override.
    When force_deep is True, bypasses AI classification and routes
    directly to DEEP_LANE for council assembly.
    
    Args:
        query_text: User's input query
        force_deep: If True, bypass classification and force council assembly
        
    Returns:
        dspy.Prediction: Contains route, score, and reasoning fields
    """
    if force_deep:
        return dspy.Prediction(
            route="DEEP_LANE",
            score=10.0,
            reasoning="MANUAL OVERRIDE: User requested Council assembly explicitly."
        )

    router = RouterModule()
    return router(query=query_text)
