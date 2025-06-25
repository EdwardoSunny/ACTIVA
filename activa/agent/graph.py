from typing import TypedDict, List, Literal
from langgraph.graph import StateGraph
from activa.agent.state import AgentState
from .nodes import plan_and_search, write_manim_code, execute_code, search_error

# --- Conditional Edge Logic ---
def should_continue(state: AgentState) -> Literal["search", "done"]:
    """
    Determines the next step based on the current state.
    
    - If there's no error, the process is done.
    - If the max attempts are reached, it's done.
    - Otherwise, it continues to search for an error fix.
    """
    if not state["error"]:
        return "done"
    
    if state["attempts"] >= 20:
        print("⚠️ Max attempts reached. Ending process.")
        return "done"
    
    return "search"

# --- Build and Compile Graph ---
def get_manim_agent():
    """
    Builds and compiles the LangGraph agent.
    """
    workflow = StateGraph(AgentState)

    # Add nodes to the graph
    workflow.add_node("plan", plan_and_search)
    workflow.add_node("write", write_manim_code)
    workflow.add_node("execute", execute_code)
    workflow.add_node("search", search_error)

    # Define the flow of the graph
    workflow.set_entry_point("plan")
    workflow.add_edge("plan", "write")
    workflow.add_edge("write", "execute")
    workflow.add_conditional_edges(
        "execute",
        should_continue,
        {
            "search": "search",
            "done": "__end__"
        }
    )
    workflow.add_edge("search", "write")

    # Compile the graph into a runnable app
    return workflow.compile()
