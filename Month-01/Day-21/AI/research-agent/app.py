"""
State Graph Research Agent Application CLI
Interactive CLI, benchmark test suite, and markdown report generator.
"""

import sys
import argparse
import time
from typing import Optional

# Ensure UTF-8 output encoding across Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

from state import create_initial_state
from graph import build_research_graph
from schemas import ResearchReport


# Rich formatting support with graceful ASCII fallback
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.markdown import Markdown
    console = Console()
    HAS_RICH = True
except ImportError:
    HAS_RICH = False
    console = None


def print_banner():
    banner = """
========================================================================
  🚀 DAY 21: STATE GRAPH AUTONOMOUS RESEARCH AGENT (LangGraph Paradigm)
  Multi-Node Cyclic Reasoning Engine with Dynamic AST & BM25 Tool Nodes
========================================================================
"""
    if HAS_RICH:
        console.print(f"[bold cyan]{banner}[/bold cyan]")
    else:
        print(banner)


def run_research(query: str, max_steps: int = 8, export_path: Optional[str] = None) -> ResearchReport:
    """Executes the State Graph for a research query with live transition streaming."""
    if HAS_RICH:
        console.print(f"\n[bold yellow]🔍 Initiating Research Query:[/bold yellow] [white]{query}[/white]\n")
    else:
        print(f"\n🔍 Initiating Research Query: '{query}'\n")

    graph = build_research_graph()
    initial_state = create_initial_state(query=query, max_steps=max_steps)

    start_time = time.time()
    final_state = None

    for node_name, state_snapshot in graph.stream(initial_state):
        final_state = state_snapshot
        step = state_snapshot.get("step_count", 0)

        if node_name == "agent":
            thought = state_snapshot.get("current_thought")
            if thought:
                msg = f"Step {step} | Agent Thought: {thought.thought}\nAction: {thought.action_type}"
                if thought.tool_call:
                    msg += f" -> {thought.tool_call.tool_name}({thought.tool_call.tool_input})"
                if HAS_RICH:
                    console.print(Panel(msg, title=f"[bold blue]Node: {node_name.upper()}[/bold blue]", border_style="blue"))
                else:
                    print(f"[{node_name.upper()}] {msg}")

        elif node_name == "tools":
            pending = state_snapshot.get("tool_history", [])
            last_tool = pending[-1] if pending else None
            if last_tool:
                msg = f"Executed: {last_tool.tool_name}\nStatus: {'SUCCESS' if last_tool.success else 'FAILED'}"
                if HAS_RICH:
                    console.print(Panel(msg, title=f"[bold magenta]Node: {node_name.upper()}[/bold magenta]", border_style="magenta"))
                else:
                    print(f"[{node_name.upper()}] {msg}")

        elif node_name == "answer":
            if HAS_RICH:
                console.print(Panel("Final synthesis & citation verification complete.", title=f"[bold green]Node: {node_name.upper()}[/bold green]", border_style="green"))
            else:
                print(f"[{node_name.upper()}] Final synthesis complete.")

    elapsed = round(time.time() - start_time, 2)
    report: ResearchReport = final_state.get("final_report")

    # Render Final Report
    print("\n" + "=" * 70)
    print("                      RESEARCH REPORT")
    print("=" * 70 + "\n")

    if HAS_RICH:
        console.print(f"[bold green]Executive Summary:[/bold green]\n{report.executive_summary}\n")
        console.print(f"[bold cyan]Detailed Analysis:[/bold cyan]\n{report.detailed_analysis}\n")

        # Metrics Table
        if report.key_metrics:
            table = Table(title="Quantitative Metrics & Evaluation", show_header=True, header_style="bold magenta")
            table.add_column("Metric / Expression", style="dim")
            table.add_column("Value", justify="right")
            for k, v in report.key_metrics.items():
                table.add_row(str(k), str(v))
            console.print(table)

        # Citations Table
        if report.citations:
            c_table = Table(title="Verified Academic Citations", show_header=True, header_style="bold yellow")
            c_table.add_column("Source ID", style="dim")
            c_table.add_column("Paper Title")
            c_table.add_column("Score", justify="right")
            for c in report.citations:
                c_table.add_row(c.source_id, c.title, str(c.score))
            console.print(c_table)
    else:
        print(f"Executive Summary:\n{report.executive_summary}\n")
        print(f"Detailed Analysis:\n{report.detailed_analysis}\n")
        print("Key Metrics:")
        for k, v in report.key_metrics.items():
            print(f"  - {k}: {v}")
        print("\nCitations:")
        for c in report.citations:
            print(f"  [{c.source_id}] {c.title} (Score: {c.score})")

    print(f"\n⏱️ Graph Execution Completed in {elapsed}s | Total Steps: {final_state.get('step_count')}\n")

    # Optional Markdown Export
    if export_path:
        export_markdown(report, export_path)
        print(f"📁 Report saved to: {export_path}")

    return report


def export_markdown(report: ResearchReport, filepath: str):
    """Exports structured report into clean GitHub-flavored markdown."""
    lines = [
        f"# Research Report: {report.query}\n",
        "## Executive Summary\n",
        f"{report.executive_summary}\n",
        "## Detailed Analysis\n",
        f"{report.detailed_analysis}\n",
        "## Key Quantitative Metrics\n",
        "| Metric / Formulation | Evaluated Value |",
        "| :--- | :--- |"
    ]
    for k, v in report.key_metrics.items():
        lines.append(f"| `{k}` | **{v}** |")

    lines.append("\n## Verified Grounded Citations\n")
    for idx, c in enumerate(report.citations, 1):
        lines.append(f"{idx}. **{c.title}** (`{c.source_id}`)")
        lines.append(f"   > *\"{c.snippet}\"*\n")

    lines.append("## Graph Execution Trajectory\n```")
    for log in report.graph_trajectory:
        lines.append(log)
    lines.append("```\n")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def run_benchmark_suite():
    """Runs a series of automated benchmark queries testing graph cyclic routing and tool calls."""
    benchmarks = [
        "Analyze DeepSeek-V3 MoE architecture and calculate activated parameter percentage ratio",
        "Explain Chinchilla scaling laws and calculate compute-optimal FLOPs for 70B parameter model",
        "How does GraphRAG use community detection for global query-focused summarization?"
    ]

    print_banner()
    if HAS_RICH:
        console.print("[bold green]Starting Automated StateGraph Benchmark Suite (3 Test Cases)...[/bold green]\n")
    else:
        print("Starting Automated StateGraph Benchmark Suite (3 Test Cases)...\n")

    for i, q in enumerate(benchmarks, 1):
        print(f"\n>>> Running Benchmark Case {i}/{len(benchmarks)}...")
        run_research(query=q, max_steps=8)
        print("-" * 70)


def main():
    parser = argparse.ArgumentParser(description="StateGraph Research Agent CLI")
    parser.add_argument("--query", "-q", type=str, help="Research question to investigate")
    parser.add_argument("--demo", action="store_true", help="Run automated benchmark suite")
    parser.add_argument("--export", "-e", type=str, help="Filepath to export markdown report")
    parser.add_argument("--max-steps", type=int, default=8, help="Maximum allowed graph transitions")

    args = parser.parse_args()

    if args.demo:
        run_benchmark_suite()
    elif args.query:
        print_banner()
        run_research(query=args.query, max_steps=args.max_steps, export_path=args.export)
    else:
        print_banner()
        print("Interactive Mode. Enter research query (or 'exit' to quit):")
        while True:
            try:
                user_q = input("\nResearch Query > ").strip()
                if not user_q or user_q.lower() in ("exit", "quit", "q"):
                    print("Exiting StateGraph Research Agent.")
                    break
                run_research(query=user_q, max_steps=args.max_steps)
            except (KeyboardInterrupt, EOFError):
                print("\nExiting.")
                break


if __name__ == "__main__":
    main()
