from langchain_core.tools import tool
from openai import OpenAI
import subprocess
import tempfile
import sys
import os

client = OpenAI()

# Create a tool for web searching errors
@tool
def search_error_solution(error_message: str) -> str:
    """Search the web for solutions to Python errors."""
    try:
        # Create a focused search query for the error
        search_query = f"Python error fix: {error_message[:200]}"  # Limit query length
        
        response = client.chat.completions.create(
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

