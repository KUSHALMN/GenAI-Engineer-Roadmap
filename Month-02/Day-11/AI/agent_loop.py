"""
ReAct-Style Autonomous Agent Loop.
Executes Reason + Act iterative loop:
1. LLM formulates Thought + selects Tool Action
2. Tool is invoked and returns Observation
3. Observation appended to scratchpad
4. Repeats until Final Answer reached or max iterations exceeded
"""

import json
import re
from typing import Any, Callable, Dict, Optional
from agent_state import AgentState


class ReActAgent:
    """ReAct autonomous tool-calling agent."""

    def __init__(
        self,
        tools: Dict[str, Callable[..., Any]],
        llm_caller: Optional[Callable[[str], str]] = None,
        max_iterations: int = 5,
    ):
        self.tools = tools
        self.llm_caller = llm_caller or self._mock_llm_react
        self.max_iterations = max_iterations

    def _mock_llm_react(self, prompt: str) -> str:
        """Simulates ReAct steps for demo/offline test."""
        if "Observation: 50" in prompt:
            return "Thought: I now have the calculation result.\nFinal Answer: The result is 50."
        elif "Action: calculator" not in prompt:
            return 'Thought: I need to calculate 25 * 2.\nAction: calculator\nAction Input: {"a": 25, "b": 2, "op": "mul"}'
        return "Thought: Task complete.\nFinal Answer: Done."

    def run(self, query: str, session_id: str = "sess_react") -> AgentState:
        """Run ReAct loop."""
        state = AgentState(query=query, session_id=session_id, status="running")

        for iteration in range(1, self.max_iterations + 1):
            scratchpad = state.get_scratchpad()
            prompt = (
                f"Question: {query}\n"
                f"Available Tools: {list(self.tools.keys())}\n"
                f"Scratchpad:\n{scratchpad}\n"
                f"What is your next Thought and Action?"
            )

            # 1. Call LLM
            llm_output = self.llm_caller(prompt)

            # Check for Final Answer
            if "Final Answer:" in llm_output:
                thought = llm_output.split("Final Answer:")[0].replace("Thought:", "").strip()
                final_answer = llm_output.split("Final Answer:")[1].strip()
                state.add_step(thought=thought, observation="Reached Final Answer")
                state.final_answer = final_answer
                state.status = "completed"
                return state

            # Parse Thought and Action
            thought_match = re.search(r"Thought:\s*(.*?)(?=\nAction:|$)", llm_output, re.DOTALL)
            action_match = re.search(r"Action:\s*(\w+)", llm_output)
            input_match = re.search(r"Action Input:\s*(\{.*\}|[^\n]+)", llm_output)

            thought = thought_match.group(1).strip() if thought_match else "Analyzing next step"
            action = action_match.group(1).strip() if action_match else None

            action_input = {}
            if input_match:
                raw_input = input_match.group(1).strip()
                try:
                    action_input = json.loads(raw_input)
                except Exception:
                    action_input = {"raw": raw_input}

            # 2. Execute Action
            if action and action in self.tools:
                try:
                    observation = str(self.tools[action](**action_input))
                except Exception as e:
                    observation = f"Error executing tool '{action}': {e}"
            elif action:
                observation = f"Tool '{action}' not recognized. Available tools: {list(self.tools.keys())}"
            else:
                observation = "No explicit action requested. Please select an action or provide Final Answer."

            # 3. Record step
            state.add_step(thought=thought, action=action, action_input=action_input, observation=observation)

        state.status = "max_iterations"
        state.error = f"Agent stopped: exceeded maximum iteration budget ({self.max_iterations})"
        return state


if __name__ == "__main__":
    def calc_tool(a: float = 0, b: float = 0, op: str = "add") -> float:
        return a * b if op == "mul" else a + b

    agent = ReActAgent(tools={"calculator": calc_tool}, max_iterations=4)
    res_state = agent.run("What is 25 times 2?")

    print("ReAct Agent Status:", res_state.status)
    print("Final Answer:", res_state.final_answer)
    print("Steps:", len(res_state.steps))
    assert res_state.status == "completed"
    assert "50" in res_state.final_answer
    print("ReAct agent tests passed successfully!")
