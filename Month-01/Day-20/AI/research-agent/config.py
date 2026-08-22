"""
Configuration settings and system prompts for Autonomous AI Research Agent.
"""

import os
from typing import Dict, Any
from dotenv import load_dotenv

# Load .env if present
load_dotenv()

# ==========================================
# LLM & API Configuration
# ==========================================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# Default model selections
DEFAULT_GROQ_MODEL = "llama-3.3-70b-versatile"
DEFAULT_OPENAI_MODEL = "gpt-4o-mini"

# Active model provider precedence: Groq -> OpenAI -> Simulation Mode
LLM_PROVIDER = "groq" if GROQ_API_KEY else ("openai" if OPENAI_API_KEY else "simulation")

# Execution constraints
MAX_REACT_STEPS = 6
SEARCH_TOP_K = 3
DEFAULT_TEMPERATURE = 0.2

# ==========================================
# Prompts
# ==========================================
RESEARCH_AGENT_SYSTEM_PROMPT = """You are an Autonomous AI Research Scientist and Technical Analyst.
Your goal is to answer complex technical inquiries by iteratively planning, searching verified academic & engineering documentation, performing precise mathematical calculations, and synthesizing a fully cited report.

You have access to the following tools:
1. `document_search(query: str, top_k: int = 3)`: Searches technical AI research documents, benchmarks, architecture specs, and papers.
2. `calculator(expression: str)`: Safely evaluates mathematical and arithmetic formulas (e.g., parameter counts, FLOPs, memory requirements, latency, percentages).

You must operate using the ReAct (Reason + Act + Observe) paradigm:
1. Thought: Analyze current state and state what you need to discover next.
2. Action: Call a tool with structured JSON arguments.
3. Observation: Review the tool output.
4. Reflection: Verify if you have sufficient ground truth to formulate the complete final answer. If yes, synthesize the final report; if not, execute next research step.
"""

SYNTHESIZER_SYSTEM_PROMPT = """You are a Principal AI Technical Writer.
Synthesize the collected observations, calculations, and factual evidence into a comprehensive, rigorous research report with executive summary, verified bullet findings, quantitative calculations, and explicit citations.
"""
