import json
from langgraph.graph import StateGraph, END
from src.state import AgentState
from src.agents.data_agent import DataAgent
from src.agents.insight_agent import InsightAgent
from src.agents.evaluator import EvaluatorAgent
from src.agents.creative_agent import CreativeAgent
from src.utils.logger import setup_logger

# 1. Setup Logger
logger = setup_logger("Graph")

# 2. Initialize the Agents
# These are the Python classes you created in src/agents/
data_agent = DataAgent()
insight_agent = InsightAgent("Insight")
evaluator_agent = EvaluatorAgent("Evaluator")
creative_agent = CreativeAgent("Creative")

# --- 3. Define Graph Nodes (The Steps) ---

def data_node(state: AgentState):
    logger.info("Data Agent is analyzing the dataset...")
    # Execute the pandas logic
    summary = data_agent.execute(state["query"])
    # Return update to state
    return {"data_summary": summary, "retry_count": 0}

def insight_node(state: AgentState):
    attempt = state.get("retry_count", 0) + 1
    logger.info(f"Insight Agent is thinking (Attempt {attempt})...")
    
    # Generate hypothesis, passing previous critique if it exists
    hypo = insight_agent.generate(
        state["query"], 
        state["data_summary"], 
        state.get("critique")
    )
    return {"hypothesis": hypo}

def evaluator_node(state: AgentState):
    logger.info("Evaluator is validating the hypothesis...")
    val = evaluator_agent.validate(state["hypothesis"], state["data_summary"])
    return {"validation": val}

def creative_node(state: AgentState):
    logger.info("Creative Agent is drafting new ads...")
    creatives = creative_agent.generate(state["hypothesis"], ["Old Failing Ad Context"])
    return {"creatives": creatives}

def reporting_node(state: AgentState):
    logger.info("Saving Final Report...")
    # Save the full state to a JSON file
    with open("reports/final_report.json", "w") as f:
        json.dump(state, f, indent=2, default=str)
    return {"final_report": "Saved"}

# --- 4. Define Logic Edges (The Rules) ---

def check_validation(state: AgentState):
    """
    The Router: Decides where to go after Evaluation.
    """
    validation = state.get("validation", {})
    is_valid = validation.get("is_valid", False)
    
    # Path A: Success
    if is_valid:
        # Check if we need creatives (keyword search in hypothesis)
        hypo_text = str(state["hypothesis"]).lower()
        if "fatigue" in hypo_text or "creative" in hypo_text:
            return "creative"
        return "report"
    
    # Path B: Failure (Retry Logic)
    current_retries = state.get("retry_count", 0)
    if current_retries < 3:
        critique = validation.get("critique", "Invalid Logic")
        logger.warning(f" Hypothesis Rejected: {critique}")
        
        # Increment retry count and loop back
        return "retry"
    
    # Path C: Max Retries Reached (Give up)
    logger.error("Max retries reached. Exiting.")
    return "report"

def route_critique(state: AgentState):
    """Helper to update state before looping back"""
    return {
        "critique": state["validation"].get("critique"),
        "retry_count": state["retry_count"] + 1
    }

# --- 5. Build the Graph ---

workflow = StateGraph(AgentState)

# Add the Nodes
workflow.add_node("data", data_node)
workflow.add_node("insight", insight_node)
workflow.add_node("evaluator", evaluator_node)
workflow.add_node("creative", creative_node)
workflow.add_node("report", reporting_node)

# Add the Edges (Linear flow)
workflow.set_entry_point("data")
workflow.add_edge("data", "insight")
workflow.add_edge("insight", "evaluator")

# Add the Conditional Edge (The Loop)
workflow.add_conditional_edges(
    "evaluator",
    check_validation,
    {
        "creative": "creative", # If valid + creative issue
        "report": "report",     # If valid + no creative issue OR failed too many times
        "retry": "insight"      # If invalid -> Try Again (Loop)
    }
)

workflow.add_edge("creative", "report")
workflow.add_edge("report", END)

# Compile the graph
app = workflow.compile()