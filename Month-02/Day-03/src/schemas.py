from pydantic import BaseModel, Field
from typing import Optional


class SearchInput(BaseModel):
    query: str = Field(..., description="Search query to look up")
    max_results: int = Field(default=3, ge=1, le=10)


class CalculatorInput(BaseModel):
    expression: str = Field(..., description="Math expression to evaluate, e.g. '2 + 3 * 4'")


class WeatherInput(BaseModel):
    city: str = Field(..., description="City name to get weather for")
    units: str = Field(default="celsius", pattern="^(celsius|fahrenheit)$")


class AgentResponse(BaseModel):
    answer: str
    tool_used: Optional[str] = None
    tool_input: Optional[str] = None
    tool_output: Optional[str] = None
    steps: int = 0
