import sys
import os
import time

# Ensure Day-29 root is on sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.state import AgentState, AgentStatus
from agents.tool_selection import ToolSelector
from agents.router import IntentRouter


class AutonomousAgent:
    """Implements an autonomous ReAct reasoning and execution loop."""

    def __init__(self, max_steps: int = 4):
        self.max_steps = max_steps
        self.tool_selector = ToolSelector()
        self.router = IntentRouter()

    def run(self, user_goal: str) -> AgentState:
        state = AgentState(
            session_id=f"sess_{int(time.time())}",
            user_goal=user_goal,
            max_steps=self.max_steps
        )

        # 1. Routing phase
        route_info = self.router.route(user_goal)
        state.add_thought(f"Route selected: {route_info['route']} with confidence {route_info['confidence']}")

        # 2. ReAct iteration loop
        while state.current_step < state.max_steps:
            state.current_step += 1

            if "calculate" in user_goal.lower() or "mortgage" in user_goal.lower():
                state.add_thought("Need mathematical tool to compute loan interest.")
                # Mock tool call execution
                res = {"monthly_payment": 1898.30, "total_interest": 183388.0}
                state.add_tool_step("calculator", {"principal": 300000, "rate": 0.065}, res)
                state.final_answer = f"The estimated monthly mortgage payment is $1,898.30 with total interest of $183,388."
                state.status = AgentStatus.COMPLETED
                break
            else:
                state.add_thought("Need search retrieval tool to answer factual inquiry.")
                res = "ChromaDB and Pinecone support HNSW indexing for approximate nearest neighbors."
                state.add_tool_step("web_search", {"query": user_goal}, res)
                state.final_answer = f"Summary: {res}"
                state.status = AgentStatus.COMPLETED
                break

        if not state.final_answer:
            state.status = AgentStatus.FAILED
            state.error_message = "Max step limit reached before conclusion."

        return state


if __name__ == "__main__":
    agent = AutonomousAgent()
    final_state = agent.run("Calculate mortgage for a 300000 loan at 6.5% interest")
    print("--- AGENT EXECUTION TRACE ---")
    print("Session ID   :", final_state.session_id)
    print("Status       :", final_state.status.value)
    print("Final Answer :", final_state.final_answer)
    print("Scratchpad   :", final_state.scratchpad)
