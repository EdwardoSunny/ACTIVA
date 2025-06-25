from typing import TypedDict, List

# --- Define Agent State ---
class AgentState(TypedDict):
    """
    Represents the state of our agent, holding all necessary information
    for the generation and debugging process.
    """
    task: str
    code: str
    error: str
    attempts: int
    execution_output: str
    error_solutions: List[str]
    implementation_guide: str
