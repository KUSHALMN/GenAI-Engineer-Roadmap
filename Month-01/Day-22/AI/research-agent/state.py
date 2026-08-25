"""
State Module for StateGraph Research Agent with Session Memory
Defines the state structure passed between nodes in the cyclic graph,
including thread identifiers, memory buffers, and checkpoint references.
"""

from typing import TypedDict, List, Dict, Any, Optional
from schemas import ToolCall, ToolResult, Citation, AgentThought, ResearchReport, MemoryEntry
import uuid


class ResearchState(TypedDict, total=False):
    """
    Central State passed between nodes in the State Graph.
    
    Fields:
        thread_id (str): Unique identifier for the persistent conversation thread.
        session_id (str): High-level session namespace.
        checkpoint_id (str): Unique ID of the current graph step snapshot.
        query (str): The current user query being investigated.
        messages (List[Dict[str, str]]): Conversational history of queries and responses.
        step_count (int): Current iteration index in the graph loop.
        max_steps (int): Safety threshold to prevent infinite cyclic transitions.
        plan (List[str]): Decomposed sub-goals or research milestones.
        current_thought (Optional[AgentThought]): Reasoning step from Agent Node.
        pending_tool_calls (List[ToolCall]): Tools scheduled for execution by Tool Node.
        tool_history (List[ToolResult]): Full log of executed tools and observations.
        observations (List[str]): Accumulated context and evidence.
        citations (List[Citation]): Unique verified source references.
        calculation_cache (Dict[str, Any]): Evaluated mathematical expressions.
        session_memory (List[MemoryEntry]): Cross-turn recalled facts and previous research summaries.
        draft_answer (Optional[str]): Preliminary draft synthesized by Agent Node.
        final_report (Optional[ResearchReport]): Structured report from Answer Node.
        next_node (str): Routing target for next graph transition.
        is_complete (bool): Terminal completion flag.
        logs (List[str]): Execution trace for logging, debugging, and visualization.
    """
    thread_id: str
    session_id: str
    checkpoint_id: str
    query: str
    messages: List[Dict[str, str]]
    step_count: int
    max_steps: int
    plan: List[str]
    current_thought: Optional[AgentThought]
    pending_tool_calls: List[ToolCall]
    tool_history: List[ToolResult]
    observations: List[str]
    citations: List[Citation]
    calculation_cache: Dict[str, Any]
    session_memory: List[MemoryEntry]
    draft_answer: Optional[str]
    final_report: Optional[ResearchReport]
    next_node: str
    is_complete: bool
    logs: List[str]


def create_initial_state(
    query: str,
    thread_id: Optional[str] = None,
    session_id: str = "default_session",
    session_memory: Optional[List[MemoryEntry]] = None,
    max_steps: int = 8
) -> ResearchState:
    """Instantiates a clean, initialized ResearchState for graph execution."""
    tid = thread_id or f"thread_{uuid.uuid4().hex[:8]}"
    cid = f"chk_{uuid.uuid4().hex[:8]}"
    mem = session_memory or []

    return {
        "thread_id": tid,
        "session_id": session_id,
        "checkpoint_id": cid,
        "query": query,
        "messages": [{"role": "user", "content": query}],
        "step_count": 0,
        "max_steps": max_steps,
        "plan": [],
        "current_thought": None,
        "pending_tool_calls": [],
        "tool_history": [],
        "observations": [],
        "citations": [],
        "calculation_cache": {},
        "session_memory": mem,
        "draft_answer": None,
        "final_report": None,
        "next_node": "agent",
        "is_complete": False,
        "logs": [f"[INIT] StateGraph initialized for thread: '{tid}' | Query: '{query}'"],
    }
