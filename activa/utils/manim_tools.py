import os
import re
import subprocess
import tempfile
from openai import OpenAI

# Initialize the OpenAI client for tool use
client = OpenAI()

def search_manim_implementation(task: str) -> str:
    """Search for how to implement specific Manim features."""
    try:
        search_query = f"Manim tutorial how to {task} code example"
        
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Find specific Manim code examples and implementation details. Focus on working code patterns."},
                {"role": "user", "content": search_query}
            ],
            tools=[{"type": "web_search"}],
            tool_choice="required"
        )
        
        return response.choices[0].message.content or "No examples found."
    except Exception as e:
        return ""

def search_error_fix(error: str, code_context: str) -> str:
    """Search for specific fixes for Manim errors."""
    try:
        # Extract the most relevant part of the error
        error_lines = error.split('\n')
        key_error = next((line for line in error_lines if 'Error' in line or 'error' in line), error[:200])
        
        search_query = f"Manim fix error: {key_error}"
        
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a Manim debugging expert. Provide specific code fixes for Manim errors."},
                {"role": "user", "content": f"Error: {key_error}\n\nContext: Working with Manim animations. Find the fix."}
            ],
            tools=[{"type": "web_search"}],
            tool_choice="required"
        )
        
        return response.choices[0].message.content or "Check imports and class structure."
    except Exception as e:
        return "Ensure proper Manim imports and Scene inheritance."

def execute_manim_code(code: str) -> dict:
    """Execute Manim code with better error handling."""
    try:
        # Extract scene name - handle multiple scene classes
        scene_matches = re.findall(r'class\s+(\w+)\s*\(.*Scene.*\)', code)
        if not scene_matches:
            return {
                "success": False,
                "output": "",
                "error": "No Scene class found. Make sure to define a class that inherits from Scene."
            }
        
        # Use the last scene class found
        scene_name = scene_matches[-1]
        
        # Write to temporary file with better naming
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, dir='.') as f:
            f.write(code)
            temp_file = f.name
        
        # Execute with minimal quality for speed
        cmd = f"manim -pql --disable_caching {temp_file} {scene_name}"
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=45
        )
        
        # Clean up
        try:
            os.unlink(temp_file)
        except:
            pass
        
        if result.returncode == 0:
            return {
                "success": True,
                "output": result.stdout,
                "error": None
            }
        else:
            # Combine stderr and stdout for better error context
            error_msg = result.stderr or result.stdout
            return {
                "success": False,
                "output": result.stdout,
                "error": error_msg
            }
    
    except subprocess.TimeoutExpired:
        try:
            os.unlink(temp_file)
        except:
            pass
        return {"success": False, "output": "", "error": "Execution timeout - animation might be too complex"}
    except Exception as e:
        return {"success": False, "output": "", "error": f"Execution error: {str(e)}"}
