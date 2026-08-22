"""
Pydantic Schemas and Data Models for Autonomous AI Research Agent.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class SearchResult(BaseModel):
    """Result returned from document/corpus search."""
    id: str = Field(description="Document ID or section anchor")
    title: str = Field(description="Document title")
    snippet: str = Field(description="Relevant excerpt from document")
    relevance_score: float = Field(description="Normalized similarity score [0.0 - 1.0]")
    source: str = Field(description="Source URL or paper citation")
    category: str = Field(default="AI/ML", description="Category tag")


class CalculationResult(BaseModel):
    """Result returned from safe AST math calculator."""
    expression: str = Field(description="Evaluated mathematical expression")
    result: float = Field(description="Calculated numerical result")
    formatted: str = Field(description="Human-readable formatted result")
    success: bool = Field(default=True, description="Whether calculation succeeded")
    error: Optional[str] = Field(default=None, description="Error message if failed")


class ToolCall(BaseModel):
    """Model representing an LLM-invoked tool call."""
    tool_name: str = Field(description="Name of the tool to execute")
    arguments: Dict[str, Any] = Field(default_factory=dict, description="Dictionary of arguments")
    call_id: Optional[str] = Field(default=None, description="Unique tool call ID")


class ResearchStep(BaseModel):
    """A discrete research step in the ReAct execution plan."""
    step_number: int = Field(description="Step sequence number")
    thought: str = Field(description="Reasoning behind executing this step")
    tool: str = Field(description="Tool to invoke ('document_search', 'calculate', or 'final_answer')")
    arguments: Dict[str, Any] = Field(default_factory=dict, description="Arguments for tool")
    observation: Optional[str] = Field(default=None, description="Output from tool execution")
    completed: bool = Field(default=False, description="Whether step is finished")


class ResearchPlan(BaseModel):
    """Decomposed research execution plan."""
    query: str = Field(description="User research query")
    objective: str = Field(description="Primary research objective")
    sub_tasks: List[str] = Field(default_factory=list, description="Sub-questions to investigate")
    planned_steps: List[ResearchStep] = Field(default_factory=list, description="Sequence of planned steps")


class ReflectionCritique(BaseModel):
    """Agent self-reflection on intermediate research progress."""
    findings_sufficient: bool = Field(description="Whether enough evidence is gathered")
    identified_gaps: List[str] = Field(default_factory=list, description="Missing pieces of information")
    critique_notes: str = Field(description="Observations on current answer quality")
    next_recommended_action: str = Field(description="Next tool call or synthesize final answer")


class Citation(BaseModel):
    """Source citation for synthesized final report."""
    source_title: str = Field(description="Title of cited paper or technical document")
    citation: str = Field(description="Formal reference or author/year citation")
    excerpt: str = Field(description="Supporting text snippet")


class AgentFinalReport(BaseModel):
    """Comprehensive synthesized research report."""
    query: str = Field(description="Original user query")
    executive_summary: str = Field(description="Executive level overview answering the prompt")
    key_findings: List[str] = Field(default_factory=list, description="Bullet points of verified factual findings")
    quantitative_analysis: Optional[Dict[str, Any]] = Field(default=None, description="Numerical calculations & metrics")
    citations: List[Citation] = Field(default_factory=list, description="List of source citations used")
    confidence_score: float = Field(default=0.95, description="Confidence score [0.0 - 1.0]")
    total_steps_executed: int = Field(default=0, description="Total ReAct iterations taken")
