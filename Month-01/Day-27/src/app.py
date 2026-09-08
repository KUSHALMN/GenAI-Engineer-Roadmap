import asyncio
from fastapi import FastAPI
from pydantic import BaseModel, Field

try:
    from .tracer import ObservabilityTracer
except ImportError:
    from tracer import ObservabilityTracer

app = FastAPI(title="LLM Observability Gateway - Day 27")
tracer = ObservabilityTracer()

class PromptRequest(BaseModel):
    prompt: str = Field(..., min_length=1)
    model: str = Field(default="gpt-4o-mini")

@app.get("/")
def root():
    return {"status": "online", "topic": "Day 27: LLM Observability"}

@app.post("/api/v1/generate")
async def generate_with_telemetry(req: PromptRequest):
    with tracer.start_span(name="llm_inference", model=req.model) as span:
        await asyncio.sleep(0.01)
        span.prompt_tokens = max(1, len(req.prompt) // 4)
        completion_text = f"Observability-traced response for: '{req.prompt}'"
        span.completion_tokens = max(1, len(completion_text) // 4)
        return {
            "output": completion_text,
            "telemetry": {
                "trace_id": span.trace_id,
                "span_id": span.span_id,
                "tokens": span.total_tokens,
                "cost_usd": span.estimated_cost_usd,
                "duration_ms": span.duration_ms
            }
        }

@app.get("/api/v1/metrics")
def get_metrics():
    return tracer.get_summary_metrics()
