import dspy
from config import lm

# 1. Definer Signaturen (Input/Output kontrakten)
class AssessComplexity(dspy.Signature):
    """Analyze the query complexity to route it to the correct processing pipeline."""

    query = dspy.InputField(desc="The user's question or command")
    complexity_score = dspy.OutputField(desc="A score between 1.0 (Trivial) and 10.0 (Highly Strategic)")
    reasoning = dspy.OutputField(desc="Brief justification for the score")
    route = dspy.OutputField(desc="Must be exactly 'FAST_LANE' or 'DEEP_LANE'")

# 2. Byg Modulet
class RouterModule(dspy.Module):
    def __init__(self):
        super().__init__()
        self.assess = dspy.ChainOfThought(AssessComplexity)

    def forward(self, query):
        result = self.assess(query=query)

        # Sikrer at vi får en brugbar score
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

# 3. Den opdaterede funktion med 'Override' mulighed
def route_query(query_text, force_deep=False):
    # Tjek for manuel override FØR vi spørger AI
    if force_deep:
        return dspy.Prediction(
            route="DEEP_LANE",
            score=10.0,
            reasoning="MANUAL OVERRIDE: User requested Council assembly explicitly."
        )

    # Ellers kør normal AI vurdering
    router = RouterModule()
    return router(query=query_text)
