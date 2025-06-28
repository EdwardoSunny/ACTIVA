import re
from langchain_core.messages import SystemMessage, HumanMessage
from activa.agent.state import AgentState
from activa.utils.manim_tools import search_manim_implementation, search_error_fix, execute_manim_code
from config.config import config, get_llm_client

# Initialize LLM client based on config
try:
    llm = get_llm_client(config)
    print(f"✅ Using {config['provider']} with model {config['model']}")
except Exception as e:
    print(f"❌ Error initializing LLM client: {e}")
    print("Falling back to OpenAI...")
    # Fallback to OpenAI
    from langchain_openai import ChatOpenAI
    llm = ChatOpenAI(model="gpt-4o")

def plan_and_search(state: AgentState) -> AgentState:
    """
    Plans the implementation by searching for examples if it's the first attempt.
    """
    if state["attempts"] == 0:
        print("🔍 Searching for implementation examples...")
        state["implementation_guide"] = search_manim_implementation(state["task"])
    return state

def write_manim_code(state: AgentState) -> AgentState:
    """
    Writes or revises the Manim code based on the current state.
    """
    print(f"\n📝 Attempt {state['attempts'] + 1}: Writing/Revising code...")

    # Base system prompt for the LLM
    system_prompt = """You are a Manim expert. Your task is to write clean, executable Python code for Manim animations.

Follow these rules strictly:
1.  **Imports:** Always start with `from manim import *`.
2.  **Class Definition:** Define a single class that inherits from `Scene`.
3.  **Construct Method:** All animation logic must be within the `construct(self)` method.
4.  **Simplicity:** Keep animations straightforward and focused on the core task.
5.  **Output:** Return ONLY the Python code, without any explanations, comments, or markdown formatting like ```python.
"""

    if state["attempts"] == 0:
        # First attempt: Use the initial task and implementation guide
        user_prompt = f"""Create Manim code for the following task:
{state['task']}

Here are some implementation examples to guide you:
{state['implementation_guide'][:1000]}

Write the complete, working Python script."""
    else:
        # Subsequent attempts: Fix code based on the error
        error_info = state.get('error', 'Unknown error')
        solutions = "\n".join(state.get('error_solutions', []))
        
        user_prompt = f"""The previous code failed. Your task is to fix it.

**Original Task:**
{state['task']}

**Previous Code:**
```python
{state['code']}
```

**Error Encountered:**
{error_info[:1000]}

**Potential Solutions Found:**
{solutions}

**Instructions:**
Rewrite the ENTIRE script to fix the error. Pay close attention to class names, object instantiation, and animation logic. Ensure the new code is complete and executable."""

    # Invoke the language model
    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ])
    
    # Clean the response to get raw code
    # Handle different response types from different providers
    if hasattr(response, 'content'):
        code = response.content.strip()
    elif isinstance(response, str):
        code = response.strip()
    else:
        # Fallback: try to get content from response
        code = str(response).strip()
    
    code = re.sub(r'^```python\n|```$', '', code, flags=re.MULTILINE)
    
    state["code"] = code
    state["attempts"] += 1
    
    return state

def execute_code(state: AgentState) -> AgentState:
    """
    Executes the generated Manim code and captures the outcome.
    """
    print("🚀 Executing Manim code...")
    result = execute_manim_code(state["code"])
    
    if result["success"]:
        state["error"] = ""
        state["execution_output"] = result["output"]
        print("✅ Code executed successfully!")
    else:
        state["error"] = result["error"]
        state["execution_output"] = result["output"]
        print(f"❌ Error encountered during execution.")
    
    return state

def search_error(state: AgentState) -> AgentState:
    """
    Searches for a solution to the encountered error.
    """
    if state["error"]:
        print("🔍 Searching for an error solution...")
        solution = search_error_fix(state["error"], state["code"])
        
        if "error_solutions" not in state or not state["error_solutions"]:
            state["error_solutions"] = []
        
        state["error_solutions"].append(solution)
        print("💡 Found a potential solution.")
        
    return state
