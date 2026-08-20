"""
Pydantic schemas and data models for Tool Calling Assistant.
Defines OpenAI-compatible function and tool specifications, messages, and execution results.
"""

from typing import Any, Dict, List, Literal, Optional, Union
from pydantic import BaseModel, Field


class FunctionDefinition(BaseModel):
    name: str = Field(..., description="The name of the function to be called")
    description: str = Field(..., description="A description of what the function does")
    parameters: Dict[str, Any] = Field(
        default_factory=dict,
        description="JSON Schema representation of parameters the function accepts",
    )


class Tool(BaseModel):
    type: Literal["function"] = "function"
    function: FunctionDefinition


class FunctionCall(BaseModel):
    name: str = Field(..., description="Function name to invoke")
    arguments: str = Field(..., description="JSON-serialized string of arguments")


class ToolCall(BaseModel):
    id: str = Field(..., description="Unique identifier for the tool call")
    type: Literal["function"] = "function"
    function: FunctionCall


class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant", "tool"]
    content: Optional[str] = None
    name: Optional[str] = None
    tool_call_id: Optional[str] = None
    tool_calls: Optional[List[ToolCall]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert ChatMessage into an API-compatible dictionary omitting None values."""
        data: Dict[str, Any] = {"role": self.role}
        if self.content is not None:
            data["content"] = self.content
        if self.name is not None:
            data["name"] = self.name
        if self.tool_call_id is not None:
            data["tool_call_id"] = self.tool_call_id
        if self.tool_calls is not None:
            data["tool_calls"] = [
                {
                    "id": tc.id,
                    "type": tc.type,
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments,
                    },
                }
                for tc in self.tool_calls
            ]
        return data


class ToolExecutionResult(BaseModel):
    tool_call_id: str
    name: str
    success: bool
    result: Any
    error: Optional[str] = None

    def to_tool_message(self) -> ChatMessage:
        content_str = str(self.result) if self.success else f"Error: {self.error}"
        return ChatMessage(
            role="tool",
            name=self.name,
            tool_call_id=self.tool_call_id,
            content=content_str,
        )
