from visgen.states.agent_state import AgentState
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

def create_code_agent(llm):
    def code_agent(state: AgentState) -> AgentState:
        """Write or improve code based on the task and any previous errors."""
        messages = [
            SystemMessage(content="""You are an expert Python programmer. Write clean, efficient code to solve the given task. 
            If there was a previous error, analyze it and fix the code accordingly.
            If web search results are provided, use them to guide your solution.
            Return ONLY the Python code, no explanations or markdown formatting.""")
        ]

        if state["attempts"] == 0:
            messages.append(HumanMessage(content=f"Write Python code to: {state['task']}"))
        else:
            error_context = f"""
            Task: {state['task']}

            Previous code:
            {state['code']}

            Error encountered:
            {state['error']}
            """

            if state.get("error_search_results"):
                error_context += f"\n\nWeb search results for the error:\n{state['error_search_results']}"

            error_context += "\n\nPlease fix the code to resolve this error."

            messages.append(HumanMessage(content=error_context))

        response = llm.invoke(messages)
        print(response.content)
        state["code"] = response.content.strip()
        state["messages"].append(AIMessage(content=f"Attempt {state['attempts'] + 1}: Writing code..."))

        return state
    return code_agent
