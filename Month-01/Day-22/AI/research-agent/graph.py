"""
State Graph Definition & Checkpoint Orchestration Engine
Builds the cyclic workflow with persistent state checkpoints:
  [START] -> agent_node ──(should_continue)──> tool_node ──> agent_node
                               │
                               └──(finish)──> answer_node ──> [END]
"""

from typing import Dict, Any, Callable, List, Optional, Tuple
from state import ResearchState, create_initial_state
from nodes.agent_node import agent_node
from nodes.tool_node import tool_node
from nodes.answer_node import answer_node
from memory.memory_store import MemoryStore, global_memory_store


def should_continue(state: ResearchState) -> str:
    """
    Conditional Routing Function.
    Evaluates current agent thought to determine next graph transition.
    """
    thought = state.get("current_thought")
    step_count = state.get("step_count", 0)
    max_steps = state.get("max_steps", 8)

    if step_count >= max_steps:
        return "answer"

    if thought and thought.action_type == "call_tool":
        return "tools"

    return "answer"


class PersistentStateGraph:
    """
    StateGraph engine with integrated checkpoint persistence.
    Saves immutable state snapshots at each node transition.
    """

    def __init__(self, memory_store: Optional[MemoryStore] = None):
        self.nodes: Dict[str, Callable[[ResearchState], Dict[str, Any]]] = {}
        self.edges: Dict[str, str] = {}
        self.conditional_edges: Dict[str, Tuple[Callable[[ResearchState], str], Dict[str, str]]] = {}
        self.entry_point: Optional[str] = None
        self.memory_store = memory_store or global_memory_store

    def add_node(self, name: str, func: Callable[[ResearchState], Dict[str, Any]]):
        self.nodes[name] = func

    def set_entry_point(self, name: str):
        self.entry_point = name

    def add_edge(self, source: str, target: str):
        self.edges[source] = target

    def add_conditional_edges(self, source: str, routing_fn: Callable[[ResearchState], str], mapping: Dict[str, str]):
        self.conditional_edges[source] = (routing_fn, mapping)

    def compile(self):
        if not self.entry_point or self.entry_point not in self.nodes:
            raise ValueError(f"Invalid entry point: '{self.entry_point}'")
        return self

    def stream(self, initial_state: ResearchState):
        """Yields step-by-step state transitions while recording checkpoints."""
        state = dict(initial_state)
        curr_node_name = self.entry_point
        thread_id = state.get("thread_id", "default_thread")
        step_idx = 0

        while curr_node_name and curr_node_name != "END":
            node_fn = self.nodes.get(curr_node_name)
            if not node_fn:
                break

            updates = node_fn(state)
            state.update(updates)
            step_idx += 1

            # Persist checkpoint snapshot
            chk_id = self.memory_store.save_checkpoint(
                thread_id=thread_id,
                step_index=step_idx,
                node_name=curr_node_name,
                state=state
            )
            state["checkpoint_id"] = chk_id

            yield curr_node_name, state

            if curr_node_name in self.conditional_edges:
                routing_fn, mapping = self.conditional_edges[curr_node_name]
                branch_key = routing_fn(state)
                curr_node_name = mapping.get(branch_key, "END")
            elif curr_node_name in self.edges:
                curr_node_name = self.edges[curr_node_name]
            else:
                curr_node_name = "END"

    def invoke(self, initial_state: ResearchState) -> ResearchState:
        """Executes the full graph synchronously to completion."""
        final_state = initial_state
        for _, state in self.stream(initial_state):
            final_state = state
        return final_state


def build_research_graph(memory_store: Optional[MemoryStore] = None) -> PersistentStateGraph:
    """Constructs and compiles the Persistent State Graph."""
    workflow = PersistentStateGraph(memory_store=memory_store)

    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", tool_node)
    workflow.add_node("answer", answer_node)

    workflow.set_entry_point("agent")

    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            "answer": "answer"
        }
    )

    workflow.add_edge("tools", "agent")
    workflow.add_edge("answer", "END")

    return workflow.compile()
