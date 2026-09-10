"""
inference.py — Run agent inference and return structured AgentResponse.
"""
from model import build_agent_executor
from schemas import AgentResponse


def run_agent(query: str) -> AgentResponse:
    executor = build_agent_executor()
    result = executor.invoke({"input": query})

    output = result.get("output", "")
    steps = result.get("intermediate_steps", [])

    tool_used = tool_input = tool_output = None
    if steps:
        last_action, last_obs = steps[-1]
        tool_used = last_action.tool
        tool_input = str(last_action.tool_input)
        tool_output = str(last_obs)

    return AgentResponse(
        answer=output,
        tool_used=tool_used,
        tool_input=tool_input,
        tool_output=tool_output,
        steps=len(steps),
    )


if __name__ == "__main__":
    queries = [
        "What is 15 * 24 + 100?",
        "What is the weather in Bangalore?",
        "Search for LangChain agents tutorial",
    ]
    for q in queries:
        print(f"\nQuery: {q}")
        resp = run_agent(q)
        print(f"Answer: {resp.answer}")
        print(f"Tool: {resp.tool_used} | Steps: {resp.steps}")
