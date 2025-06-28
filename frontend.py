import chainlit as cl
from activa.agent.graph import get_manim_agent
from activa.utils.manim_tools import execute_manim_code
import os
import glob
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor

# Initialize the agent once
manim_agent = get_manim_agent()

# Global variable to store the last prompt and generated code
last_prompt = None
last_generated_code = None
last_filename = None

# Thread pool for running blocking operations
executor = ThreadPoolExecutor(max_workers=1)

# Ensure generated_code directory exists
def ensure_generated_code_dir():
    """Ensure the generated_code directory exists"""
    generated_dir = "generated_code"
    if not os.path.exists(generated_dir):
        os.makedirs(generated_dir)
    return generated_dir

@cl.on_chat_start
async def start():
    """Initialize the chat session"""
    # Ensure the generated_code directory exists
    ensure_generated_code_dir()
    
    await cl.Message(
        content="🎬 Welcome to the ACTIVA Code Generation Agent!\n\n"
                "I can help you create Manim animations. Just describe what you want to visualize, "
                "and I'll generate the code for you.\n\n"
                "Example: 'Create an animation showing a bouncing ball'"
    ).send()

def run_agent_sync(initial_state):
    """Run the agent synchronously in a thread pool"""
    return manim_agent.invoke(initial_state)

@cl.on_message
async def main(message: cl.Message):
    """Handle incoming messages and generate Manim code"""
    global last_prompt, last_generated_code, last_filename
    
    # Get the user's task
    task = message.content
    
    # Update last prompt
    last_prompt = task
    
    # Show initial progress
    progress_msg = await cl.Message(content="🤔 Analyzing your request...").send()
    
    # Define the initial state for the agent
    initial_state = {
        "task": task,
        "code": "",
        "error": "",
        "attempts": 0,
        "execution_output": "",
        "error_solutions": [],
        "implementation_guide": ""
    }
    
    try:
        # Send progress update
        await cl.Message(content="🔄 Generating Manim code... This may take a few minutes.").send()
        
        # Run the agent in a thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        final_state = await loop.run_in_executor(executor, run_agent_sync, initial_state)
        
        # Get the results
        final_code = final_state.get("code", "")
        error_message = final_state.get("error", "")
        attempts = final_state.get("attempts", 0)
        
        # Send completion status
        await cl.Message(content=f"✅ Generation completed after {attempts} attempt(s)!").send()
        
        if not error_message and final_code:
            # Store the generated code and filename globally
            last_generated_code = final_code
            timestamp = int(time.time())
            
            # Save to generated_code directory
            generated_dir = ensure_generated_code_dir()
            last_filename = os.path.join(generated_dir, f"manim_animation_{timestamp}.py")
            
            # Save the code to a file
            with open(last_filename, 'w') as f:
                f.write(final_code)
            
            # Success! Show the code
            await cl.Message(
                content=f"✨ Success! Generated Manim code in {attempts} attempt(s)."
            ).send()
            
            # Display the code in a nice format
            await cl.Message(
                content=f"```python\n{final_code}\n```",
                author="ACTIVA Agent"
            ).send()
            
            # Find where Manim saves the output files
            output_info = get_manim_output_info()
            
            await cl.Message(
                content=f"💾 **Code saved to:** `{os.path.abspath(last_filename)}`\n\n"
                        f"📁 **Animation output will be saved to:** `{output_info}`"
            ).send()
            
            # Show persistent action buttons
            await show_action_buttons()
            
        else:
            # Show error
            error_content = f"⚠️ Generation failed after {attempts} attempts."
            if final_code:
                error_content += f"\n\nLast attempted code:\n```python\n{final_code}\n```"
            if error_message:
                error_content += f"\n\nError: {error_message}"
            
            await cl.Message(content=error_content).send()
            
            # Show retry buttons
            await show_retry_buttons()
            
    except Exception as e:
        await cl.Message(content=f"❌ An unexpected error occurred: {str(e)}").send()

async def show_action_buttons():
    """Show the persistent action buttons"""
    actions = [
        cl.Action(name="run_animation", label="🚀 Run Animation", payload={"filename": last_filename}),
        cl.Action(name="rerun_same", label="🔄 Rerun Same Prompt", payload={"action": "rerun"}),
        cl.Action(name="new_prompt", label="📝 New Prompt", payload={"action": "new"})
    ]
    
    await cl.Message(
        content="What would you like to do next?",
        actions=actions
    ).send()

async def show_retry_buttons():
    """Show retry buttons for failed generations"""
    actions = [
        cl.Action(name="rerun_same", label="🔄 Retry Same Prompt", payload={"action": "rerun"}),
        cl.Action(name="new_prompt", label="📝 Try New Prompt", payload={"action": "new"})
    ]
    
    await cl.Message(
        content="Would you like to try again?",
        actions=actions
    ).send()

def get_manim_output_info():
    """Get information about where Manim saves output files"""
    # Check for common Manim output directories
    possible_dirs = [
        "media",  # Default Manim output
        "output",  # Alternative
        ".",  # Current directory
    ]
    
    for dir_name in possible_dirs:
        if os.path.exists(dir_name):
            return os.path.abspath(dir_name)
    
    return "media/ (default Manim output directory)"

def execute_manim_sync(code):
    """Execute Manim code synchronously in a thread pool"""
    return execute_manim_code(code)

@cl.action_callback("run_animation")
async def run_animation(action):
    """Run the generated Manim animation"""
    filename = action.payload.get("filename")
    
    # Show progress updates during execution
    await cl.Message(content="🎬 Starting animation execution... This may take a while.").send()
    
    try:
        # Read the code from the file to pass to execute_manim_code
        with open(filename, 'r') as f:
            code = f.read()
        
        # Execute the Manim code in a thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(executor, execute_manim_sync, code)
        
        if result.get("success", False):
            # Find the generated media files
            media_files = find_manim_output_files()
            
            success_content = f"✅ Animation completed successfully!\n\n"
            if media_files:
                success_content += f"📁 **Generated files:**\n"
                for file_path in media_files:
                    success_content += f"   - `{file_path}`\n"
            else:
                success_content += f"📁 **Output saved to:** `{get_manim_output_info()}`\n"
            
            if result.get("output"):
                success_content += f"\n📋 **Execution output:**\n```\n{result['output'][:500]}...\n```"
            
            await cl.Message(content=success_content).send()
            
        else:
            error_content = f"❌ Animation execution failed.\n\n"
            if result.get("error"):
                error_content += f"**Error:** {result['error']}\n\n"
            if result.get("output"):
                error_content += f"**Output:** {result['output']}"
            
            await cl.Message(content=error_content).send()
        
        # Show action buttons again after execution
        await show_action_buttons()
        
    except Exception as e:
        await cl.Message(
            content=f"❌ Error running animation: {str(e)}"
        ).send()
        # Show action buttons even after error
        await show_action_buttons()

def find_manim_output_files():
    """Find recently created Manim output files"""
    media_files = []
    
    # Look for common Manim output patterns
    patterns = [
        "media/**/*.mp4",
        "media/**/*.png", 
        "media/**/*.gif",
        "output/**/*.mp4",
        "output/**/*.png",
        "output/**/*.gif",
        "*.mp4",
        "*.png",
        "*.gif"
    ]
    
    for pattern in patterns:
        files = glob.glob(pattern, recursive=True)
        # Get files modified in the last 5 minutes
        recent_files = [
            f for f in files 
            if os.path.exists(f) and (time.time() - os.path.getmtime(f)) < 300
        ]
        media_files.extend(recent_files)
    
    return list(set(media_files))  # Remove duplicates

@cl.action_callback("new_prompt")
async def new_prompt(action):
    """Handle new prompt request"""
    await cl.Message(
        content="Great! Just send me your new prompt and I'll generate a new animation for you."
    ).send()

@cl.action_callback("rerun_same")
async def rerun_same(action):
    """Handle rerun request - automatically rerun the same prompt"""
    global last_prompt
    
    if last_prompt:
        # Show that we're rerunning
        await cl.Message(content=f"🔄 Rerunning: '{last_prompt}'").send()
        
        # Create a fake message to trigger the main function
        class FakeMessage:
            def __init__(self, content):
                self.content = content
        
        fake_message = FakeMessage(last_prompt)
        await main(fake_message)
    else:
        await cl.Message(
            content="❌ No previous prompt to rerun. Please send a new prompt."
        ).send()

if __name__ == "__main__":
    # This will be handled by chainlit
    pass 