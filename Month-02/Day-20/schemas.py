"""
Pydantic Request & Response Schemas for Capstone GenAI Service.
"""

from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class AgentTaskType(str, Enum):
    RESEARCH = "research"
    CALCULATION = "calculation"
    DOCUMENT_QA = "document_qa"
    GENERAL = "general"


class CapstoneQueryRequest(BaseModel):
    query: str = Field(min_length=3, max_length=4000, description="User query or instruction")
    task_type: AgentTaskType = Field(default=AgentTaskType.GENERAL, description="Task classification")
    session_id: Optional[str] = Field(default="sess_default", description="Conversation session ID")
    temperature: float = Field(default=0.0, ge=0.0, le=1.0, description="Sampling temperature")
    bypass_cache: bool = Field(default=False, description="Whether to bypass the response cache")


class CitationItem(BaseModel):
    source_id: str
    snippet: str


class CapstoneQueryResponse(BaseModel):
    query: str
    answer: str
    task_type: str
    cached: bool
    latency_ms: float
    estimated_cost_usd: float
    citations: List[CitationItem] = Field(default_factory=list)
    tools_executed: List[str] = Field(default_factory=list)
    session_id: str
    status: str = "success"


class HealthCheckResponse(BaseModel):
    status: str
    version: str
    cache_entries: int
    uptime_seconds: float
