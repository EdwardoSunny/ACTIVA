from visgen.states.agent_state import AgentState
from visgen.agents.tools import execute_python_code, search_error_solution
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

def create_error_searcher():
    def search_for_error(state: AgentState) -> AgentState:
        """Search the web for solutions to the encountered error."""
        if state["error"] and state["attempts"] < 5:
            state["messages"].append(AIMessage(content="Searching the web for error solutions..."))
            search_results = search_error_solution(state["error"])
            state["error_search_results"] = search_results
            state["messages"].append(AIMessage(content=f"Found potential solutions from web search"))
        return state

    return search_for_error
