import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any

try:
    from .tracer import ObservabilityTracer, LLMSpan
except ImportError:
    from tracer import ObservabilityTracer, LLMSpan

app = FastAPI(
    title="Production LLM Observability & Telemetry Service",
    description="Distributed trace instrumentation, latency percentiles, and token accounting.",
    version="1.0.0"
)

tracer = ObservabilityTracer()

class PromptRequest(BaseModel):
    prompt: str = Field(..., min_length=1)
    model: str = Field(default="gpt-4o-mini")

@app.get("/")
def root():
    return {"status": "online", "topic": "Day 27: LLM Observability"}

@app.post("/api/v1/generate")
async def generate_with_telemetry(req: PromptRequest):
    # Instrument call with an OpenTelemetry-compatible span
    with tracer.start_span(name="llm_inference", model=req.model) as span:
        # Simulate inference time proportional to prompt length
        await asyncio.sleep(0.02)
        
        # Track token telemetry
        span.prompt_tokens = max(1, len(req.prompt) // 4)
        completion_text = f"Observability-traced completion for prompt: '{req.prompt}'"
        span.completion_tokens = max(1, len(completion_text) // 4)
        
        return {
            "output": completion_text,
            "telemetry": {
                "trace_id": span.trace_id,
                "span_id": span.span_id,
                "prompt_tokens": span.prompt_tokens,
                "completion_tokens": span.completion_tokens,
                "estimated_cost_usd": span.estimated_cost_usd,
                "duration_ms": span.duration_ms
            }
        }

@app.get("/api/v1/metrics")
def get_metrics():
    return tracer.get_summary_metrics()

@app.get("/api/v1/traces")
def get_traces():
    return {"traces": [s.model_dump() for s in tracer.spans]}
