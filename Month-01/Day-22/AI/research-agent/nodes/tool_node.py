"""
Tool Node Module
Executes scheduled tool invocations (document_search, calculator),
catches execution errors safely, extracts citations, and appends structured
observations back to the State Graph.
"""

from typing import Dict, Any, List
from state import ResearchState
from schemas import ToolResult, Citation
from tools.document_search import search_documents
from tools.calculator import evaluate_expression


def tool_node(state: ResearchState) -> Dict[str, Any]:
    """
    Node Function: Tool Execution
    Processes all pending tool calls in the state and collects observations.
    """
    pending = state.get("pending_tool_calls", [])
    observations = list(state.get("observations", []))
    citations = list(state.get("citations", []))
    calc_cache = dict(state.get("calculation_cache", {}))
    tool_history = list(state.get("tool_history", []))
    logs = list(state.get("logs", []))

    for call in pending:
        tool_name = call.tool_name
        args = call.tool_input

        logs.append(f"[TOOL NODE] Executing '{tool_name}' with args {args}")

        try:
            if tool_name == "document_search":
                query_str = args.get("query", "")
                top_k = args.get("top_k", 2)
                res = search_documents(query=query_str, top_k=top_k)

                obs_text = f"Document Search for '{query_str}':\n{res.get('content', '')}"
                observations.append(obs_text)

                for c_dict in res.get("citations", []):
                    citation_obj = Citation(**c_dict)
                    if not any(existing.source_id == citation_obj.source_id for existing in citations):
                        citations.append(citation_obj)

                tool_history.append(ToolResult(
                    tool_name=tool_name,
                    tool_input=args,
                    output=res,
                    success=True
                ))

            elif tool_name == "calculator":
                expr_str = args.get("expression", "")
                res = evaluate_expression(expr_str)

                if res.get("success"):
                    obs_text = f"Calculator evaluated '{expr_str}' => {res.get('result')} (Scientific: {res.get('scientific_notation')})"
                    calc_cache[expr_str] = res.get("result")
                    success_flag = True
                else:
                    obs_text = f"Calculator error on '{expr_str}': {res.get('error')}"
                    success_flag = False

                observations.append(obs_text)
                tool_history.append(ToolResult(
                    tool_name=tool_name,
                    tool_input=args,
                    output=res,
                    success=success_flag,
                    error=res.get("error")
                ))

            else:
                err_msg = f"Unknown tool: '{tool_name}'"
                observations.append(err_msg)
                tool_history.append(ToolResult(
                    tool_name=tool_name,
                    tool_input=args,
                    output=None,
                    success=False,
                    error=err_msg
                ))

        except Exception as e:
            err_msg = f"Exception executing tool '{tool_name}': {str(e)}"
            observations.append(err_msg)
            tool_history.append(ToolResult(
                tool_name=tool_name,
                tool_input=args,
                output=None,
                success=False,
                error=err_msg
            ))

    return {
        "pending_tool_calls": [],
        "observations": observations,
        "citations": citations,
        "calculation_cache": calc_cache,
        "tool_history": tool_history,
        "logs": logs
    }
