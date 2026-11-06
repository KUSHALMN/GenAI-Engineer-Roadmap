"""
Day 07: Workflow Graphs and Conditional Edges
Builds a graph-based agent orchestration engine with nodes,
conditional routing edges, loop cycles, and terminal state checks.
"""

from typing import Callable, Dict, Any, List
import json

class WorkflowGraph:
    def __init__(self):
        self.nodes: Dict[str, Callable[[Dict[str, Any]], Dict[str, Any]]] = {}
        self.conditional_edges: Dict[str, Callable[[Dict[str, Any]], str]] = {}
        self.entry_point: str = ""

    def add_node(self, name: str, func: Callable[[Dict[str, Any]], Dict[str, Any]]):
        self.nodes[name] = func

    def set_entry_point(self, name: str):
        self.entry_point = name

    def add_conditional_edge(self, source_node: str, condition_router: Callable[[Dict[str, Any]], str]):
        self.conditional_edges[source_node] = condition_router

    def run(self, initial_state: Dict[str, Any], max_cycles: int = 10) -> Dict[str, Any]:
        current_node = self.entry_point
        state = dict(initial_state)
        cycles = 0

        while current_node and current_node != "__END__":
            cycles += 1
            if cycles > max_cycles:
                state["error"] = "Max graph cycles exceeded."
                break

            print(f"[Graph] Executing node: {current_node}")
            node_func = self.nodes[current_node]
            state = node_func(state)

            if current_node in self.conditional_edges:
                current_node = self.conditional_edges[current_node](state)
            else:
                current_node = "__END__"

        return state

if __name__ == "__main__":
    graph = WorkflowGraph()

    def generate_draft(state):
        state["draft"] = "AI generated summary of company earnings."
        state["score"] = 0.6
        return state

    def critique_draft(state):
        # Improve score each iteration
        state["score"] += 0.25
        print(f"[Critique] Evaluated draft score: {state['score']:.2f}")
        return state

    def router_condition(state):
        if state["score"] >= 0.8:
            return "__END__"
        return "critique_node"

    graph.add_node("draft_node", generate_draft)
    graph.add_node("critique_node", critique_draft)
    graph.set_entry_point("draft_node")
    graph.add_conditional_edge("draft_node", router_condition)
    graph.add_conditional_edge("critique_node", router_condition)

    result = graph.run({})
    assert result["score"] >= 0.8
    print(f"Graph completed with final state: {result}")
    print("Day 07 AI Workflow Graph passed all tests.")
