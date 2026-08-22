"""
Interactive CLI and Benchmark Runner for Autonomous AI Research Agent.
"""

import sys
import os
import argparse
import json
from typing import Optional

# Ensure standard output supports UTF-8 on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass

# Ensure parent directory is on sys.path for direct script execution
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

try:
    from schemas import AgentFinalReport
    from agent import ResearchAgent
except ImportError:
    from .schemas import AgentFinalReport
    from .agent import ResearchAgent



def print_banner():
    banner = """
======================================================================
  🧠  AUTONOMOUS AI RESEARCH AGENT (ReAct Reasoning Engine)  🔬
======================================================================
  * Multi-Step Autonomous Planning & Tool Calling Loop
  * Document Search over Seminal AI Research Papers
  * Safe AST Mathematical Evaluation & Scaling Laws Analysis
  * Provider Support: Groq (Llama-3.3-70B) / OpenAI (GPT-4o) / Simulation
======================================================================
"""
    print(banner)


def render_report(report: AgentFinalReport):
    print("\n" + "=" * 70)
    print("                    📑 FINAL RESEARCH REPORT                    ")
    print("=" * 70)
    print(f"🎯 Research Query: {report.query}")
    print(f"📊 Confidence Score: {report.confidence_score * 100:.1f}% | Total Steps: {report.total_steps_executed}\n")

    print("📌 Executive Summary:")
    print(f"   {report.executive_summary}\n")

    print("🔍 Key Verified Findings:")
    for idx, finding in enumerate(report.key_findings, 1):
        print(f"   {idx}. {finding}")
    print()

    if report.quantitative_analysis:
        print("📐 Quantitative Calculations & Scaling:")
        for expr, res in report.quantitative_analysis.items():
            print(f"   * Expression: `{expr}` => {res}")
        print()

    if report.citations:
        print("📚 Verified Citations:")
        for idx, cite in enumerate(report.citations, 1):
            print(f"   [{idx}] {cite.source_title}")
            print(f"       Citation/URL: {cite.citation}")
            print(f"       Excerpt: \"{cite.excerpt}\"")
        print()
    print("=" * 70 + "\n")


def export_report_to_markdown(report: AgentFinalReport, filepath: str):
    md_content = [
        f"# Research Report: {report.query}\n",
        f"**Confidence Score:** {report.confidence_score * 100:.1f}%  ",
        f"**Total ReAct Steps:** {report.total_steps_executed}\n",
        "## Executive Summary",
        f"{report.executive_summary}\n",
        "## Key Findings",
    ]
    for idx, f in enumerate(report.key_findings, 1):
        md_content.append(f"{idx}. {f}")

    if report.quantitative_analysis:
        md_content.append("\n## Quantitative Calculations")
        for expr, val in report.quantitative_analysis.items():
            md_content.append(f"- **`{expr}`**: {val}")

    if report.citations:
        md_content.append("\n## Citations & References")
        for idx, c in enumerate(report.citations, 1):
            md_content.append(f"{idx}. **{c.source_title}**  \n   URL: {c.citation}  \n   > *\"{c.excerpt}\"*")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(md_content))
    print(f"💾 Successfully exported report to: {filepath}")


def run_benchmark_demo():
    print("\n🚀 Running Autonomous Research Agent Benchmark Suite...\n")
    agent = ResearchAgent(verbose=True)

    benchmark_queries = [
        "Compare LoRA parameter reduction and memory savings against full fine-tuning for a 70B model.",
        "Analyze DeepSeek-V3 MoE architecture, token activation ratio, and training FLOP compute budget.",
        "Calculate VRAM requirements for serving a 70B parameter LLM in FP16 vs INT4 quantization."
    ]

    for idx, q in enumerate(benchmark_queries, 1):
        print(f"\n[{idx}/{len(benchmark_queries)}] Executing Benchmark Task: \"{q}\"")
        report = agent.run(q)
        render_report(report)


def interactive_mode():
    agent = ResearchAgent(verbose=True)
    print("\n💡 Type your research inquiry below (or 'exit' / 'demo' / 'help'):\n")

    while True:
        try:
            user_input = input("Research-Agent > ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit", "q"]:
                print("Exiting Research Agent. Happy learning!")
                break
            elif user_input.lower() == "demo":
                run_benchmark_demo()
                continue
            elif user_input.lower() == "help":
                print("Commands:\n  'demo' - Run benchmark queries\n  'exit' - Quit\n  Or enter any technical AI question!")
                continue

            report = agent.run(user_input)
            render_report(report)

        except (KeyboardInterrupt, EOFError):
            print("\nSession ended.")
            break


def main():
    parser = argparse.ArgumentParser(description="Autonomous AI Research Agent CLI")
    parser.add_argument("--demo", action="store_true", help="Run automated multi-query research benchmark")
    parser.add_argument("--query", type=str, default=None, help="Direct research query to execute")
    parser.add_argument("--provider", type=str, default=None, choices=["groq", "openai", "simulation"], help="LLM Provider")
    parser.add_argument("--export", type=str, default=None, help="Path to export report markdown file")

    args = parser.parse_args()
    print_banner()

    if args.demo:
        run_benchmark_demo()
    elif args.query:
        agent = ResearchAgent(provider=args.provider, verbose=True)
        report = agent.run(args.query)
        render_report(report)
        if args.export:
            export_report_to_markdown(report, args.export)
    else:
        interactive_mode()


if __name__ == "__main__":
    main()
