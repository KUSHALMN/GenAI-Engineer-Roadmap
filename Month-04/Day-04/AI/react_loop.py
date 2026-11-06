"""
Day 04: ReAct Agent Loop
Demonstrates an Observe-Think-Act bounded control loop with scratchpad logging,
tool invocation, step bounds, and terminal answer extraction.
"""

from typing import Dict, Any, List, Optional
import json

class MockLLMEngine:
    def __init__(self):
        self.step = 0

    def generate_next_step(self, user_query: str, scratchpad: List[Dict[str, str]]) -> Dict[str, Any]:
        """Simulates LLM reasoning and action proposal."""
        self.step += 1
        if self.step == 1:
            return {
                "thought": "I need to check the current stock price of AAPL to answer the user.",
                "action": "get_stock_price",
                "action_input": {"ticker": "AAPL"},
                "is_final": False
            }
        elif self.step == 2:
            return {
                "thought": "I now have the stock price of AAPL ($180.50). I can formulate the final answer.",
                "action": None,
                "action_input": None,
                "final_answer": "Apple Inc. (AAPL) is currently trading at $180.50.",
                "is_final": True
            }
        return {"thought": "No further actions.", "is_final": True, "final_answer": "Done"}

class ReActAgent:
    def __init__(self, tools: Dict[str, Any], max_steps: int = 5):
        self.tools = tools
        self.max_steps = max_steps
        self.scratchpad: List[Dict[str, str]] = []

    def run(self, query: str) -> Dict[str, Any]:
        llm = MockLLMEngine()
        self.scratchpad = []

        for step_idx in range(1, self.max_steps + 1):
            decision = llm.generate_next_step(query, self.scratchpad)
            thought = decision.get("thought", "")
            print(f"[Step {step_idx}] Thought: {thought}")

            if decision.get("is_final"):
                return {
                    "status": "COMPLETED",
                    "steps_taken": step_idx,
                    "answer": decision.get("final_answer"),
                    "scratchpad": self.scratchpad
                }

            action = decision.get("action")
            action_input = decision.get("action_input", {})
            print(f"[Step {step_idx}] Action: {action} with input {action_input}")

            # Execute tool
            if action in self.tools:
                obs = self.tools[action](**action_input)
            else:
                obs = f"Error: Tool '{action}' not found."

            print(f"[Step {step_idx}] Observation: {obs}")
            self.scratchpad.append({
                "step": step_idx,
                "thought": thought,
                "action": action,
                "observation": str(obs)
            })

        return {
            "status": "MAX_STEPS_EXCEEDED",
            "steps_taken": self.max_steps,
            "answer": "Failed to complete within max steps limit.",
            "scratchpad": self.scratchpad
        }

if __name__ == "__main__":
    tools = {
        "get_stock_price": lambda ticker: 180.50 if ticker == "AAPL" else 0.0
    }
    agent = ReActAgent(tools=tools, max_steps=4)
    result = agent.run("What is AAPL stock price?")
    
    assert result["status"] == "COMPLETED"
    assert "180.50" in result["answer"]
    assert len(result["scratchpad"]) == 1
    print("\nReAct Loop execution finished successfully:")
    print(json.dumps(result, indent=2))
