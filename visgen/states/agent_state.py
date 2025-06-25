from typing import TypedDict, Literal

class AgentState(TypedDict):
    messages: list
    code: str
    error: str
    attempts: int
    task: str
    execution_result: str
    error_search_results: str
