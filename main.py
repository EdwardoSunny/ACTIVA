import os
from activa.agent.graph import get_manim_agent
from activa.utils.manim_tools import execute_manim_code

def main():
    """
    Main function to run the Manim code generation agent.
    
    This script prompts the user for a task, generates Manim code,
    and saves the successful result to a file.
    """
    # --- Example Task ---
    task = """
Please create an animation visualization to explain what amount Lind report as salaries should expense in its income statement for the month ended June 30, based on the question and explanation below: 
Question: Lind Co.'s salaries expense of $10,000 is paid every other Friday for the 10 workdays then ending. Lind's employees do not work on Saturdays and Sundays. The last payroll was paid on June 18. On Wednesday, June 30, the month-end balance in the salaries expense account before accruals was $14,000. 
"""

    print(f"🎬 Generating Manim code for the task...")
    print("-" * 60)

    # Get the compiled agent workflow
    app = get_manim_agent()

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
    
    # Set a high recursion limit for complex tasks
    config = {"recursion_limit": 50}

    try:
        # Invoke the agent to get the final state
        final_state = app.invoke(initial_state, config=config)

        # --- Process the final result ---
        final_code = final_state.get("code", "")
        error_message = final_state.get("error", "")

        if not error_message and final_code:
            print(f"\n✨ Success after {final_state['attempts']} attempt(s)!")
            print("=" * 50)
            print("FINAL MANIM CODE:")
            print(final_code)
            print("=" * 50)

            # Save the successful code to a file
            filename = "final_manim_animation.py"
            with open(filename, 'w') as f:
                f.write(final_code)
            print(f"\n💾 Code saved to {filename}")
            
            # Optional: Automatically run the final script
            # print("\n🚀 Executing final script...")
            # execute_manim_code(final_code)

        else:
            print(f"\n⚠️ Generation failed after {final_state['attempts']} attempts.")
            if final_code:
                print("\n" + "="*50)
                print("LAST ATTEMPTED CODE:")
                print(final_code)
                print("="*50)
            if error_message:
                print(f"Last error: {error_message}")

    except Exception as e:
        print(f"\n❌ An unexpected error occurred during generation: {e}")


if __name__ == "__main__":
    main()
