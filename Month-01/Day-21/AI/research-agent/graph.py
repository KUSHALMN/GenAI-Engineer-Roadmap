"""
State Graph Definition & Orchestration Engine
Builds the cyclic DAG (Directed Acyclic / Cyclic Graph) workflow:
  [START] -> agent_node ──(should_continue)──> tool_node ──> agent_node
                               │
                               └──(finish)──> answer_node ──> [END]

Provides both native zero-dependency state engine and LangGraph-compatible interface.
"""

from typing import Dict, Any, Callable, List, Optional
from state import ResearchState, create_initial_state
from nodes.agent_node import agent_node
from nodes.tool_node import tool_node
from nodes.answer_node import answer_node


def should_continue(state: ResearchState) -> str:
    """
    Conditional Routing Function.
    Inspects agent reasoning thought to determine the next graph branch.
    """
    thought = state.get("current_thought")
    step_count = state.get("step_count", 0)
    max_steps = state.get("max_steps", 8)

    if step_count >= max_steps:
        return "answer"

    if thought and thought.action_type == "call_tool":
        return "tools"

    return "answer"


class NativeStateGraph:
    """
    Production-grade, zero-dependency StateGraph implementation.
    Mimics LangGraph StateGraph API with typed state, functional node reducers,
    conditional edge branching, cycle prevention, and execution tracing.
    """

    def __init__(self, state_schema=ResearchState):
        self.state_schema = state_schema
        self.nodes: Dict[str, Callable[[ResearchState], Dict[str, Any]]] = {}
        self.edges: Dict[str, str] = {}
        self.conditional_edges: Dict[str, Tuple[Callable[[ResearchState], str], Dict[str, str]]] = {}
        self.entry_point: Optional[str] = None

    def add_node(self, name: str, func: Callable[[ResearchState], Dict[str, Any]]):
        self.nodes[name] = func

    def set_entry_point(self, name: str):
        self.entry_point = name

    def add_edge(self, source: str, target: str):
        self.edges[source] = target

    def add_conditional_edges(self, source: str, routing_fn: Callable[[ResearchState], str], mapping: Dict[str, str]):
        self.conditional_edges[source] = (routing_fn, mapping)

    def compile(self):
        """Validates graph structure and returns executable runner."""
        if not self.entry_point or self.entry_point not in self.nodes:
            raise ValueError(f"Invalid entry point: '{self.entry_point}'")
        return self

    def invoke(self, initial_state: ResearchState) -> ResearchState:
        """Executes the full graph synchronously until termination."""
        state = dict(initial_state)
        curr_node_name = self.entry_point

        while curr_node_name and curr_node_name != "END":
            node_fn = self.nodes.get(curr_node_name)
            if not node_fn:
                raise ValueError(f"Node '{curr_node_name}' not found in graph.")

            # Execute node reducer
            updates = node_fn(state)
            state.update(updates)

            # Determine next node via conditional edges or standard edges
            if curr_node_name in self.conditional_edges:
                routing_fn, mapping = self.conditional_edges[curr_node_name]
                branch_key = routing_fn(state)
                curr_node_name = mapping.get(branch_key, "END")
            elif curr_node_name in self.edges:
                curr_node_name = self.edges[curr_node_name]
            else:
                curr_node_name = "END"

        return state

    def stream(self, initial_state: ResearchState):
        """Yields step-by-step state snapshots for real-time visualization."""
        state = dict(initial_state)
        curr_node_name = self.entry_point

        while curr_node_name and curr_node_name != "END":
            node_fn = self.nodes.get(curr_node_name)
            if not node_fn:
                break

            updates = node_fn(state)
            state.update(updates)

            yield curr_node_name, state

            if curr_node_name in self.conditional_edges:
                routing_fn, mapping = self.conditional_edges[curr_node_name]
                branch_key = routing_fn(state)
                curr_node_name = mapping.get(branch_key, "END")
            elif curr_node_name in self.edges:
                curr_node_name = self.edges[curr_node_name]
            else:
                curr_node_name = "END"


def build_research_graph() -> NativeStateGraph:
    """
    Constructs and compiles the Research Agent State Graph.
    
    Graph Topology:
        (ENTRY: agent)
             │
             ▼
        [agent_node] ──(call_tool)──> [tool_node]
             │                             │
             │ (finish)                    │
             ▼                             ▼
        [answer_node] <────────────────────┘ (loops back to agent)
             │
             ▼
          [END]
    """
    workflow = NativeStateGraph(ResearchState)

    # 1. Register Nodes
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", tool_node)
    workflow.add_node("answer", answer_node)

    # 2. Set Entry Point
    workflow.set_entry_point("agent")

    # 3. Add Conditional Routing Edges from Agent
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            "answer": "answer"
        }
    )

    # 4. Add Cycle Edge: Tool execution always loops back to Agent for re-evaluation
    workflow.add_edge("tools", "agent")

    # 5. Add Terminal Edge
    workflow.add_edge("answer", "END")

    return workflow.compile()
