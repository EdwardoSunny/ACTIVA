from visgen.states.agent_state import AgentState
from visgen.agents.tools import execute_python_code, search_error_solution
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

def create_execute_agent():
    def execute_code_agent(state: AgentState) -> AgentState:
        """Execute the code and capture results."""
        result = execute_python_code({"code": state["code"]})

        if result["success"]:
            state["execution_result"] = result["output"]
            state["error"] = ""
            state["error_search_results"] = ""
            state["messages"].append(AIMessage(content=f"Code executed successfully!\nOutput:\n{result['output']}"))
        else:
            state["error"] = result["error"]
            state["execution_result"] = result["output"]
            state["messages"].append(AIMessage(content=f"Error encountered:\n{result['error']}"))

        state["attempts"] += 1
        return state
    return execute_code_agent
