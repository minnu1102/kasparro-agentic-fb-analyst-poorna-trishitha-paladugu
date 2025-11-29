from .base import BaseAgent

class InsightAgent(BaseAgent):
    def generate(self, query, data, critique=None):
        """
        Generates a hypothesis based on data. 
        If 'critique' is present, it means the previous attempt failed.
        """
        payload = {
            "query": query,
            "data_summary": data,
            "previous_critique": critique or "None"
        }
        # Uses 'prompts/insight.md'
        return self.invoke("insight", payload)