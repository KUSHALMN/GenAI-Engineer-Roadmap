"""
Agent Node Module with Session Memory Awareness
Reasoning engine of the State Graph. Evaluates user query alongside cross-turn
session memories, deciding whether to invoke tools or proceed to report synthesis.
"""

import json
from typing import Dict, Any, List
from state import ResearchState
from schemas import AgentThought, ToolCall, MemoryEntry
from config import config


AGENT_SYSTEM_PROMPT = """You are an Autonomous AI Research Agent operating inside a Persistent State Graph.
You have access to historical session memories from previous turns and specialized research tools.

Available Tools:
1. `document_search(query: str, top_k: int)`: Lexical BM25 search over AI research corpus.
2. `calculator(expression: str)`: Safe AST arithmetic and scientific evaluation.

Instructions:
- Examine both the current user query and any relevant past conversational memories.
- Decide whether additional literature retrieval or mathematical calculation is required.
- Return ONLY valid JSON in one of the following schemas:

Schema 1 (To call a tool):
{
  "thought": "Rationale explaining what information is missing and why this tool is needed.",
  "action_type": "call_tool",
  "tool_call": {
    "tool_name": "document_search" | "calculator",
    "tool_input": { "query": "..." } | { "expression": "..." },
    "reasoning": "Brief explanation of this invocation"
  }
}

Schema 2 (When research is sufficient):
{
  "thought": "All necessary documents and calculations have been collected.",
  "action_type": "finish",
  "draft_answer": "Summary of findings."
}
"""


def _simulate_reasoning(state: ResearchState) -> AgentThought:
    """Deterministic simulation fallback when no external LLM API key is present."""
    query = state["query"].lower()
    history = state.get("tool_history", [])
    step = state.get("step_count", 0)
    session_mem: List[MemoryEntry] = state.get("session_memory", [])

    # Check if cross-turn memory provides immediate context
    memory_context_found = False
    if session_mem and ("earlier" in query or "previous" in query or "recall" in query or "compare" in query):
        memory_context_found = True

    # Step 0: Initial literature retrieval
    if step == 0 or len(history) == 0:
        if "deepseek" in query or "moe" in query or "ratio" in query:
            return AgentThought(
                thought="To analyze DeepSeek-V3 MoE architecture and parameter activation, I will search the paper database.",
                action_type="call_tool",
                tool_call=ToolCall(
                    tool_name="document_search",
                    tool_input={"query": "DeepSeek-V3 MoE activated parameters total parameters MLA"},
                    reasoning="Retrieve DeepSeek-V3 official architecture specifications."
                )
            )
        elif "chinchilla" in query or "scaling" in query or "flops" in query:
            return AgentThought(
                thought="I will retrieve Chinchilla compute-optimal scaling constants and formulas.",
                action_type="call_tool",
                tool_call=ToolCall(
                    tool_name="document_search",
                    tool_input={"query": "Chinchilla scaling laws compute optimal FLOPs tokens per parameter"},
                    reasoning="Retrieve Chinchilla empirical scaling constants."
                )
            )
        elif "graphrag" in query or "rag" in query:
            return AgentThought(
                thought="I will retrieve GraphRAG community detection and summarization principles.",
                action_type="call_tool",
                tool_call=ToolCall(
                    tool_name="document_search",
                    tool_input={"query": "GraphRAG community detection Leiden query focused summarization"},
                    reasoning="Retrieve GraphRAG community detection methodology."
                )
            )
        else:
            return AgentThought(
                thought="I will search the AI research corpus for the requested topic.",
                action_type="call_tool",
                tool_call=ToolCall(
                    tool_name="document_search",
                    tool_input={"query": state["query"]},
                    reasoning="Broad keyword search across research corpus."
                )
            )

    # Step 1: Mathematical evaluation if quantitative analysis is requested
    if step == 1 or len(history) == 1:
        if "ratio" in query or "percentage" in query or "deepseek" in query:
            return AgentThought(
                thought="Calculating parameter activation ratio (37B / 671B * 100) using safe AST calculator.",
                action_type="call_tool",
                tool_call=ToolCall(
                    tool_name="calculator",
                    tool_input={"expression": "37 / 671 * 100"},
                    reasoning="Calculate activated parameter percentage."
                )
            )
        elif "flops" in query or "chinchilla" in query:
            return AgentThought(
                thought="Calculating compute-optimal FLOPs for 70B parameter model on 1.4T tokens.",
                action_type="call_tool",
                tool_call=ToolCall(
                    tool_name="calculator",
                    tool_input={"expression": "6 * 70000000000 * 1400000000000"},
                    reasoning="Compute training FLOPs (6 * N * D)."
                )
            )

    # Step 2: Finalize research
    return AgentThought(
        thought="Sufficient evidence and quantitative metrics have been verified. Transitioning to answer synthesis.",
        action_type="finish",
        draft_answer="Completed data collection and calculations for the research query."
    )


def _call_llm_reasoning(state: ResearchState) -> AgentThought:
    """Executes live LLM completion (Groq or OpenAI) for dynamic reasoning."""
    messages = [{"role": "system", "content": AGENT_SYSTEM_PROMPT}]

    # Build prompt context with session memory and gathered observations
    context_text = f"User Research Query: {state['query']}\n\n"
    
    # Inject session memory
    if state.get("session_memory"):
        context_text += "Past Session Memories:\n"
        for mem in state["session_memory"]:
            context_text += f"- [Turn {mem.turn_id}] Query: '{mem.query}' | Summary: {mem.summary}\n"
        context_text += "\n"

    context_text += "Gathered Observations in Current Graph Execution:\n"
    if state.get("observations"):
        for idx, obs in enumerate(state["observations"], 1):
            context_text += f"[{idx}] {obs}\n"
    else:
        context_text += "No observations gathered yet in this turn.\n"

    context_text += f"\nCurrent Iteration: {state.get('step_count', 0)} / {state.get('max_steps', 8)}"
    messages.append({"role": "user", "content": context_text})

    try:
        if config.groq_api_key:
            from groq import Groq
            client = Groq(api_key=config.groq_api_key)
            completion = client.chat.completions.create(
                model=config.default_groq_model,
                messages=messages,
                temperature=config.temperature,
                max_tokens=config.max_tokens,
                response_format={"type": "json_object"}
            )
            raw_response = completion.choices[0].message.content
        elif config.openai_api_key:
            from openai import OpenAI
            client = OpenAI(api_key=config.openai_api_key)
            completion = client.chat.completions.create(
                model=config.default_openai_model,
                messages=messages,
                temperature=config.temperature,
                max_tokens=config.max_tokens,
                response_format={"type": "json_object"}
            )
            raw_response = completion.choices[0].message.content
        else:
            return _simulate_reasoning(state)

        parsed = json.loads(raw_response)
        return AgentThought.model_validate(parsed)
    except Exception:
        return _simulate_reasoning(state)


def agent_node(state: ResearchState) -> Dict[str, Any]:
    """
    Node Function: Agent Reasoning with Memory Awareness
    Analyzes graph state and decides next action (call_tool or finalize).
    """
    step_count = state.get("step_count", 0) + 1
    max_steps = state.get("max_steps", 8)

    if step_count >= max_steps:
        thought = AgentThought(
            thought=f"Reached maximum allowed graph steps ({max_steps}). Finalizing research.",
            action_type="finish",
            draft_answer="Maximum iteration threshold reached. Synthesizing available evidence."
        )
    elif config.simulation_mode:
        thought = _simulate_reasoning(state)
    else:
        thought = _call_llm_reasoning(state)

    pending_tools = []
    if thought.action_type == "call_tool" and thought.tool_call:
        pending_tools.append(thought.tool_call)

    log_entry = f"[AGENT NODE] Step {step_count}: Action={thought.action_type}"
    if thought.tool_call:
        log_entry += f" | Tool={thought.tool_call.tool_name}({thought.tool_call.tool_input})"

    return {
        "step_count": step_count,
        "current_thought": thought,
        "pending_tool_calls": pending_tools,
        "draft_answer": thought.draft_answer,
        "logs": state.get("logs", []) + [log_entry]
    }
