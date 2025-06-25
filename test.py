import subprocess
import tempfile
import sys
from typing import TypedDict, Literal
from langgraph.graph import StateGraph
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import os
from openai import OpenAI

# Define the state structure
class AgentState(TypedDict):
    messages: list
    code: str
    error: str
    attempts: int
    task: str
    execution_result: str
    error_search_results: str

# Initialize OpenAI client for web search
openai_client = OpenAI()

# Create a tool for web searching errors
@tool
def search_error_solution(error_message: str) -> str:
    """Search the web for solutions to Python errors."""
    try:
        # Create a focused search query for the error
        search_query = f"Python error fix: {error_message[:200]}"  # Limit query length
        
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are searching for solutions to Python errors. Provide concise, actionable solutions."},
                {"role": "user", "content": search_query}
            ],
            tools=[{"type": "web_search"}],
            tool_choice="required"
        )
        
        # Extract the search results from the response
        if response.choices[0].message.content:
            return response.choices[0].message.content
        else:
            return "No specific solution found for this error."
            
    except Exception as e:
        return f"Error during web search: {str(e)}"

# Create a tool for executing Python code
@tool
def execute_python_code(code: str) -> dict:
    """Execute Python code and return the result or error."""
    try:
        # Write code to a temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_file = f.name
        
        # Execute the code
        result = subprocess.run(
            [sys.executable, temp_file],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # Clean up
        os.unlink(temp_file)
        
        if result.returncode == 0:
            return {
                "success": True,
                "output": result.stdout,
                "error": None
            }
        else:
            return {
                "success": False,
                "output": result.stdout,
                "error": result.stderr
            }
    except subprocess.TimeoutExpired:
        os.unlink(temp_file)
        return {
            "success": False,
            "output": "",
            "error": "Code execution timed out after 30 seconds"
        }
    except Exception as e:
        return {
            "success": False,
            "output": "",
            "error": str(e)
        }

# Initialize the LLM
llm = ChatOpenAI(model="gpt-4", temperature=0)

# Define node functions
def write_code(state: AgentState) -> AgentState:
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
    state["code"] = response.content.strip()
    state["messages"].append(AIMessage(content=f"Attempt {state['attempts'] + 1}: Writing code..."))
    
    return state

def execute_code(state: AgentState) -> AgentState:
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

def search_for_error(state: AgentState) -> AgentState:
    """Search the web for solutions to the encountered error."""
    if state["error"] and state["attempts"] < 5:
        state["messages"].append(AIMessage(content="Searching the web for error solutions..."))
        search_results = search_error_solution(state["error"])
        state["error_search_results"] = search_results
        state["messages"].append(AIMessage(content=f"Found potential solutions from web search"))
    return state

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

# Build the graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("write_code", write_code)
workflow.add_node("execute_code", execute_code)
workflow.add_node("search_error", search_for_error)

# Add edges
workflow.set_entry_point("write_code")
workflow.add_edge("write_code", "execute_code")
workflow.add_conditional_edges(
    "execute_code",
    should_continue,
    {
        "search_error": "search_error",
        "end": "__end__"
    }
)
workflow.add_edge("search_error", "write_code")

# Compile the graph
app = workflow.compile()

# Example usage
def run_code_agent(task: str, verbose: bool = True) -> dict:
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
    
    final_state = app.invoke(initial_state)
    
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

# Example usage
if __name__ == "__main__":
    # Example 1: Simple task
    print("Example 1: Simple Task")
    result = run_code_agent("Create a function that calculates the factorial of a number and test it with factorial(5)")
    print(f"Success: {result['success']}")
    print(f"Attempts: {result['attempts']}")
    print(f"Final Code:\n{result['final_code']}")
    print(f"Output: {result['output']}")
    
    print("\n" + "="*70 + "\n")
    
    # Example 2: Task that might need web search (using a library)
    print("Example 2: Task requiring library knowledge")
    result = run_code_agent("Use pandas to create a DataFrame with columns 'name' and 'age', add 3 sample rows, and display it")
    print(f"Success: {result['success']}")
    print(f"Attempts: {result['attempts']}")
    print(f"Final Code:\n{result['final_code']}")
    print(f"Output: {result['output']}")
    
    print("\n" + "="*70 + "\n")
    
    # Example 3: Complex task that might have multiple errors
    print("Example 3: Complex task")
    result = run_code_agent("Create a class that implements a binary search tree with insert and search methods, then test it")
    print(f"Success: {result['success']}")
    print(f"Attempts: {result['attempts']}")
    print(f"Final Code:\n{result['final_code']}")
    print(f"Output: {result['output']}")
