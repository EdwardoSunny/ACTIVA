from visgen.graph.graph import VisGenAgent

agent = VisGenAgent(code_llm="gpt-4o")
result = agent.run("Write code to calculate the factorial of a number. Your code should produce a result if I run it", verbose=True) 
print(f"Success: {result['success']}")
print(f"Attempts: {result['attempts']}")
print(f"Final Code:\n{result['final_code']}")
print(f"Output: {result['output']}")
