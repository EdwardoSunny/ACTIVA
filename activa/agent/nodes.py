import re
from langchain_core.messages import SystemMessage, HumanMessage
from activa.agent.state import AgentState
from activa.utils.manim_tools import search_manim_implementation, search_error_fix, execute_manim_code
from config.config import config, get_llm_client

# Initialize LLM client based on config
try:
    llm = get_llm_client(config)
    max_tokens = config.get("max_tokens", 4000)
    print(f"✅ Using {config['provider']} with model {config['model']} (max_tokens: {max_tokens})")
except Exception as e:
    print(f"❌ Error initializing LLM client: {e}")
    print("Falling back to OpenAI...")
    # Fallback to OpenAI with increased token limit
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
        # Subsequent attempts: Fix code based on the error with much more specific guidance
        error_info = state.get('error', 'Unknown error')
        solutions = "\n".join(state.get('error_solutions', []))
        previous_code = state.get('code', '')
        
        # Extract key error information for better guidance
        error_lines = error_info.split('\n')
        key_error_line = next((line for line in error_lines if 'Error:' in line or 'error:' in line or 'Exception:' in line), error_info[:200])
        
        # Create a more specific retry prompt
        user_prompt = f"""CRITICAL: The previous code failed with a specific error. You MUST fix this exact issue.

**Original Task:**
{state['task']}

**Previous Code (that failed):**
```python
{previous_code}
```

**EXACT ERROR MESSAGE:**
{key_error_line}

**FULL ERROR CONTEXT:**
{error_info[:1500]}

**Potential Solutions Found:**
{solutions}

**CRITICAL INSTRUCTIONS:**
1. Analyze the EXACT error message above
2. Identify the specific line or concept that caused the failure
3. Make targeted changes to fix ONLY that specific issue
4. Keep the working parts of the code unchanged
5. Ensure the new code addresses the root cause of the error
6. Pay special attention to:
   - Import statements
   - Class names and inheritance
   - Method names (especially 'construct')
   - Object instantiation syntax
   - Animation method calls

Rewrite the ENTIRE script with the specific fix for the error above."""

    # Invoke the language model
    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ])
    
    # Clean the response to get raw code
    # Handle different response types from different providers
    if hasattr(response, 'content'):
        content = response.content
        # Handle case where content might be a list
        if isinstance(content, list):
            # Join list elements if it's a list of strings
            code = " ".join([str(item) for item in content])
        else:
            code = str(content)
    elif isinstance(response, str):
        code = response
    else:
        # Fallback: try to get content from response
        code = str(response)
    
    # Clean up the code
    code = code.strip()
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
        # Clear error state on success
        state["error"] = ""
        state["execution_output"] = result["output"]
        print("✅ Code executed successfully!")
    else:
        # Store error for retry logic
        state["error"] = result["error"]
        state["execution_output"] = result["output"]
        print(f"❌ Error encountered during execution: {result['error']}")
    
    return state

def search_error(state: AgentState) -> AgentState:
    """
    Searches for a solution to the encountered error.
    """
    if state["error"]:
        print("🔍 Searching for an error solution...")
        
        # Extract more specific error information for better search
        error_info = state["error"]
        error_lines = error_info.split('\n')
        
        # Find the most relevant error line
        key_error = next((line for line in error_lines 
                         if any(keyword in line.lower() for keyword in 
                               ['error:', 'exception:', 'traceback:', 'attributeerror', 'nameerror', 'syntaxerror'])), 
                        error_info[:300])
        
        # Get the code context for better search
        code_context = state.get('code', '')
        
        # Search for specific solutions
        solution = search_error_fix(key_error, code_context)
        
        if "error_solutions" not in state or not state["error_solutions"]:
            state["error_solutions"] = []
        
        # Add the solution with some context about what it addresses
        solution_with_context = f"Error: {key_error[:100]}...\nSolution: {solution}"
        state["error_solutions"].append(solution_with_context)
        
        print(f"💡 Found solution for: {key_error[:50]}...")
        
    return state
