from .base import BaseAgent

class CreativeAgent(BaseAgent):
    def generate(self, insight, failing_ads):
        """
        Generates new ad copy suggestions based on the insight.
        """
        payload = {
            "insight": insight,
            "failing_ads_context": failing_ads
        }
        # Uses 'prompts/creative.md'
        return self.invoke("creative", payload)