from visgen.states.agent_state import AgentState
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from visgen.agents.code_runner import create_execute_agent
from visgen.agents.code_writer import create_code_agent
from visgen.agents.error_searcher import create_error_searcher
from langgraph.graph import StateGraph
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from visgen.graph.logic import should_continue 

class VisGenAgent():
    def __init__(self, code_llm="gpt-4o-mini"):
        if "gpt" in code_llm:
            llm = ChatOpenAI(model=code_llm)
        elif "claude" in code_llm:
            llm = ChatAnthropic(model=code_llm)

        graph = StateGraph(AgentState)
        graph.add_node("write_code", create_code_agent(llm))
        graph.add_node("execute_code", create_execute_agent())
        graph.add_node("search_error", create_error_searcher())

        # Add edges
        graph.set_entry_point("write_code")
        graph.add_edge("write_code", "execute_code")
        graph.add_conditional_edges(
            "execute_code",
            should_continue,
            {
                "search_error": "search_error",
                "end": "__end__"
            }
        )
        graph.add_edge("search_error", "write_code")

        # Compile the graph
        self.app = graph.compile()

    def run(self, task: str, verbose: bool = True) -> dict:
        """Run the code writing and debugging agent."""
        initial_state = {
            "messages": [HumanMessage(content=f"Task: {task}")],
            "code": "",
            "error": "",
            "attempts": 0,
            "task": task,
            "execution_result": "",
            "error_search_results": ""
        }

        final_state = self.app.invoke(initial_state)

        if verbose:
            print("\n=== EXECUTION TRACE ===")
            for msg in final_state["messages"]:
                print(f"\n{msg.content}")
            print("\n=== FINAL RESULT ===")

        return {
            "task": task,
            "final_code": final_state["code"],
            "output": final_state["execution_result"],
            "attempts": final_state["attempts"],
            "success": final_state["error"] == "",
            "final_error": final_state["error"] if final_state["error"] else None
        }


