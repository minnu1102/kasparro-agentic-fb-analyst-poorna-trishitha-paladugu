from typing import TypedDict, List, Optional, Dict, Any

class AgentState(TypedDict):
    """
    Defines the 'Shared Memory' of the agent workflow.
    Every node in the graph receives this state and returns updates to it.
    """
    query: str                          # The user's original question
    data_summary: str                   # JSON string from the Data Agent
    hypothesis: Optional[Dict[str, Any]]# The Insight Agent's theory
    validation: Optional[Dict[str, Any]]# The Evaluator's judgment
    critique: Optional[str]             # Feedback if validation failed
    creatives: Optional[List[str]]      # Generated headlines (if needed)
    retry_count: int                    # How many times we've tried to fix the insight
    final_report: Optional[str]         # Final status message