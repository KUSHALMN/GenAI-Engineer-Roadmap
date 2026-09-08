from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

try:
    from .guardrails import GuardrailsEngine
    from .resilience import ResilienceOrchestrator, ModelRateLimitError
except ImportError:
    from guardrails import GuardrailsEngine
    from resilience import ResilienceOrchestrator, ModelRateLimitError

app = FastAPI(title="GenAI Guardrails Gateway - Day 26")
orchestrator = ResilienceOrchestrator(max_retries=2, base_delay=0.01)

class PromptPayload(BaseModel):
    prompt: str = Field(..., min_length=1)
    simulate_primary_failure: bool = False

async def primary_backend(prompt: str) -> str:
    return f"Frontier-Model: Analyzed '{prompt}'"

async def failing_backend(prompt: str) -> str:
    raise ModelRateLimitError("429 Too Many Requests")

async def fallback_backend(prompt: str) -> str:
    return f"Fallback-Model: Responded to '{prompt}'"

@app.get("/")
def root():
    return {"status": "online", "topic": "Day 26: Error Handling + Guardrails"}

@app.post("/api/v1/chat")
async def secure_chat(payload: PromptPayload):
    is_valid, violation = GuardrailsEngine.validate_input(payload.prompt)
    if not is_valid:
        raise HTTPException(status_code=400, detail={"error": violation})

    sanitized = GuardrailsEngine.redact_pii(payload.prompt)
    primary_fn = failing_backend if payload.simulate_primary_failure else primary_backend

    res = await orchestrator.execute_with_fallback(sanitized, primary_fn, fallback_backend)
    if res["status"] == "error":
        raise HTTPException(status_code=503, detail=res)

    res["output"] = GuardrailsEngine.validate_output(res["output"])
    return res
