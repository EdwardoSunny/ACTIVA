from typing import TypedDict, List

# --- Define Agent State ---
class AgentState(TypedDict):
    """
    Represents the state of our agent, holding all necessary information
    for the generation and debugging process.
    
    Fields:
    - task: The original task description
    - code: The current generated code
    - error: The last error encountered (empty string if no error)
    - attempts: Number of attempts made so far
    - execution_output: Output from the last execution attempt
    - error_solutions: List of potential solutions found for errors
    - implementation_guide: Initial implementation examples found
    """
    task: str
    code: str
    error: str
    attempts: int
    execution_output: str
    error_solutions: List[str]
    implementation_guide: str
