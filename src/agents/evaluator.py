from .base import BaseAgent

class EvaluatorAgent(BaseAgent):
    def validate(self, hypothesis, evidence):
        """
        Validates if the hypothesis is supported by the numerical evidence.
        """
        payload = {
            "hypothesis": hypothesis,
            "evidence": evidence
        }
        # Uses 'prompts/evaluator.md'
        return self.invoke("evaluator", payload)