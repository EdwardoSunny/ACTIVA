from visgen.states.agent_state import AgentState
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from typing import TypedDict, Literal

def should_continue(state: AgentState) -> Literal["search_error", "end"]:
    """Decide whether to continue debugging or end."""
    # If no error and we have a result, we're done
    if not state["error"] and state["attempts"] > 0:
        return "end"
    
    # If we've tried too many times, give up
    if state["attempts"] >= 5:
        state["messages"].append(AIMessage(content="Maximum attempts reached. Unable to fix all errors."))
        return "end"
    
    # Otherwise, search for error and try again
    return "search_error"
