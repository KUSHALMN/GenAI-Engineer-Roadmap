"""
Agent Node Module
The primary reasoning engine of the State Graph. Analyzes research state,
decomposes complex queries, decides whether to invoke tools or finalize research.
"""

import json
import re
from typing import Dict, Any, Optional
from state import ResearchState
from schemas import AgentThought, ToolCall
from config import config


AGENT_SYSTEM_PROMPT = """You are an Autonomous AI Research Agent operating inside a State Graph.
Your objective is to thoroughly investigate the user's research query by querying the scientific literature database and performing precise mathematical computations.

Available Tools:
1. `document_search(query: str, top_k: int)`: BM25 search over AI papers (DeepSeek-V3, Attention, Chinchilla Scaling, FlashAttention, LLaMA 3, GraphRAG, Switch MoE).
2. `calculator(expression: str)`: Safe AST arithmetic and scientific evaluator (e.g., '37 / 671 * 100', '6 * 70e9 * 15e12').

Instructions:
- Deconstruct the user query into factual retrieval and quantitative verification steps.
- Search for authoritative architectural specs before calculating derived metrics.
- Return ONLY valid JSON in one of the following two schemas:

Schema 1 (To call a tool):
{
  "thought": "Rationale explaining what information is missing and why this tool call is needed.",
  "action_type": "call_tool",
  "tool_call": {
    "tool_name": "document_search" | "calculator",
    "tool_input": { "query": "..." } | { "expression": "..." },
    "reasoning": "Brief explanation of this invocation"
  }
}

Schema 2 (When sufficient evidence has been collected):
{
  "thought": "All necessary documents and calculations have been collected.",
  "action_type": "finish",
  "draft_answer": "Summary of technical findings and metrics."
}
"""


def _simulate_reasoning(state: ResearchState) -> AgentThought:
    """Deterministic simulation fallback when no external LLM API key is present."""
    query = state["query"].lower()
    history = state.get("tool_history", [])
    step = state.get("step_count", 0)

    # Step 0: Initial literature retrieval based on keywords
    if step == 0 or len(history) == 0:
        if "deepseek" in query or "moe" in query or "ratio" in query:
            return AgentThought(
                thought="To analyze DeepSeek-V3 architecture and calculate its parameter activation ratio, I need to fetch its technical specifications.",
                action_type="call_tool",
                tool_call=ToolCall(
                    tool_name="document_search",
                    tool_input={"query": "DeepSeek-V3 MoE activated parameters total parameters MLA"},
                    reasoning="Retrieve official parameter count and architecture specs from DeepSeek-V3 report."
                )
            )
        elif "chinchilla" in query or "scaling" in query or "compute" in query or "flops" in query:
            return AgentThought(
                thought="I need to retrieve Chinchilla compute-optimal scaling law parameters and formulas.",
                action_type="call_tool",
                tool_call=ToolCall(
                    tool_name="document_search",
                    tool_input={"query": "Chinchilla scaling laws compute optimal FLOPs tokens per parameter"},
                    reasoning="Retrieve Chinchilla empirical scaling constants."
                )
            )
        elif "attention" in query or "flash" in query:
            return AgentThought(
                thought="I need to look up FlashAttention memory complexity and IO speedup metrics.",
                action_type="call_tool",
                tool_call=ToolCall(
                    tool_name="document_search",
                    tool_input={"query": "FlashAttention IO awareness exact attention speedup memory"},
                    reasoning="Retrieve FlashAttention speedup and memory complexity data."
                )
            )
        elif "graphrag" in query or "rag" in query:
            return AgentThought(
                thought="I need to retrieve GraphRAG vs Vector RAG architectural differences.",
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
                    reasoning="Broad keyword search across corpus."
                )
            )

    # Step 1: Check if quantitative computation is needed
    if step == 1 or len(history) == 1:
        if "ratio" in query or "percentage" in query or "deepseek" in query:
            return AgentThought(
                thought="The DeepSeek-V3 report reveals 671B total parameters and 37B activated parameters per token. I will calculate the exact activation percentage.",
                action_type="call_tool",
                tool_call=ToolCall(
                    tool_name="calculator",
                    tool_input={"expression": "37 / 671 * 100"},
                    reasoning="Calculate activated parameter percentage (37B / 671B * 100)."
                )
            )
        elif "flops" in query or "chinchilla" in query:
            return AgentThought(
                thought="Calculating compute-optimal FLOPs for 70B parameter model trained on 1.4T tokens using FLOPs = 6 * N * D.",
                action_type="call_tool",
                tool_call=ToolCall(
                    tool_name="calculator",
                    tool_input={"expression": "6 * 70000000000 * 1400000000000"},
                    reasoning="Compute training FLOPs (6 * 70B * 1.4T tokens)."
                )
            )

    # Step 2: Conclude research
    return AgentThought(
        thought="Sufficient empirical literature and quantitative metrics have been verified. Transitioning to answer synthesis.",
        action_type="finish",
        draft_answer="Completed data collection and calculations for the research query."
    )


def _call_llm_reasoning(state: ResearchState) -> AgentThought:
    """Executes live LLM completion (Groq or OpenAI) for dynamic reasoning."""
    messages = [{"role": "system", "content": AGENT_SYSTEM_PROMPT}]
    
    # Build prompt context with gathered observations
    context_text = "User Research Query: " + state["query"] + "\n\nGathered Observations:\n"
    if state.get("observations"):
        for idx, obs in enumerate(state["observations"], 1):
            context_text += f"[{idx}] {obs}\n"
    else:
        context_text += "No observations gathered yet.\n"
        
    context_text += f"\nCurrent Iteration: {state.get('step_count', 0)} / {state.get('max_steps', 8)}"
    messages.append({"role": "user", "content": context_text})

    raw_response = ""
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

        # Parse JSON output
        parsed = json.loads(raw_response)
        return AgentThought.model_validate(parsed)
    except Exception as e:
        # Fallback to deterministic simulation on API failure
        return _simulate_reasoning(state)


def agent_node(state: ResearchState) -> Dict[str, Any]:
    """
    Node Function: Agent Reasoning
    Analyzes graph state and decides the next action (call_tool or finalize).
    """
    step_count = state.get("step_count", 0) + 1
    max_steps = state.get("max_steps", 8)

    # Prevent infinite cycles: force completion if max_steps reached
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
