"""
Pydantic Response and Tool Schemas.
Defines strongly-typed data contracts for LLM outputs and tool execution.
"""

from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, field_validator


class SeverityLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class IssueFinding(BaseModel):
    title: str = Field(description="Short title of the finding")
    severity: SeverityLevel = Field(description="Severity classification")
    file_path: Optional[str] = Field(default=None, description="Affected file path")
    line_number: Optional[int] = Field(default=None, description="Line number if known")
    recommendation: str = Field(description="Actionable fix recommendation")


class CodeReviewReport(BaseModel):
    repository: str = Field(description="Name or URL of the repository")
    overall_score: float = Field(ge=0.0, le=10.0, description="Overall code quality score from 0 to 10")
    summary: str = Field(description="Executive summary of the review")
    findings: List[IssueFinding] = Field(default_factory=list, description="List of findings")
    approved: bool = Field(description="Whether the code is approved for merge")

    @field_validator("overall_score")
    @classmethod
    def round_score(cls, v: float) -> float:
        return round(v, 2)


class ToolCallSpec(BaseModel):
    name: str = Field(description="Name of the tool to invoke")
    arguments: Dict[str, Any] = Field(default_factory=dict, description="Key-value arguments for tool")


class ToolExecutionResponse(BaseModel):
    tool_name: str
    success: bool
    result: Optional[Any] = None
    error: Optional[str] = None
    execution_time_ms: float = 0.0


if __name__ == "__main__":
    report = CodeReviewReport(
        repository="GenAI-Engineer-Roadmap",
        overall_score=9.5,
        summary="Architecture is well-tested and robust.",
        findings=[
            IssueFinding(
                title="Add type hints",
                severity=SeverityLevel.LOW,
                recommendation="Ensure all function signatures include type hints",
            )
        ],
        approved=True,
    )
    print("Schema serialization test passed:", report.model_dump_json())
