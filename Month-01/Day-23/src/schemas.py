from pydantic import BaseModel, Field
from typing import Optional

class StreamRequest(BaseModel):
    prompt: str = Field(..., description="User prompt to stream completion for", min_length=1)
    model: str = Field(default="gpt-4o-mini", description="Target model name")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=256, ge=1, le=4096)
    chunk_delay_ms: int = Field(default=25, ge=0, le=500)
    stream_type: str = Field(default="sse")

class StreamTokenPayload(BaseModel):
    id: str
    token: str
    index: int
    is_finished: bool = False
    finish_reason: Optional[str] = None

class StreamMetrics(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    time_to_first_token_ms: float
    total_duration_ms: float
    tokens_per_second: float
