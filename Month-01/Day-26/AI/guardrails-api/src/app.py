from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any

try:
    from .guardrails import GuardrailsEngine
    from .resilience import ResilienceOrchestrator, ModelRateLimitError
except ImportError:
    from guardrails import GuardrailsEngine
    from resilience import ResilienceOrchestrator, ModelRateLimitError

app = FastAPI(
    title="Production GenAI Guardrails & Fallback Gateway",
    description="Multi-tier safety validation, exponential backoff retries, and model fallback cascades.",
    version="1.0.0"
)

orchestrator = ResilienceOrchestrator(max_retries=2, base_delay=0.01)

class PromptPayload(BaseModel):
    prompt: str = Field(..., min_length=1)
    simulate_primary_failure: bool = False

# Simulated inference backends
async def primary_model_backend(prompt: str) -> str:
    return f"Frontier-Model: Processed request '{prompt}' with deep multi-step reasoning."

async def failing_primary_backend(prompt: str) -> str:
    raise ModelRateLimitError("429 Too Many Requests: Rate limit exceeded on Primary Frontier API")

async def fallback_model_backend(prompt: str) -> str:
    return f"Fallback-Model: Quickly synthesized response for '{prompt}'."

@app.get("/")
def root():
    return {"status": "online", "topic": "Day 26: Error Handling + Guardrails"}

@app.post("/api/v1/chat")
async def secure_chat(payload: PromptPayload):
    # Tier 1: Input Guardrails
    is_valid, violation_msg = GuardrailsEngine.validate_input(payload.prompt)
    if not is_valid:
        raise HTTPException(status_code=400, detail={"error": "Input Guardrail Blocked", "reason": violation_msg})

    # Tier 2: Sanitize PII
    sanitized_prompt = GuardrailsEngine.redact_pii(payload.prompt)

    # Tier 3: Model Execution with Retry & Fallback
    primary_fn = failing_primary_backend if payload.simulate_primary_failure else primary_model_backend
    
    execution_result = await orchestrator.execute_with_fallback(
        sanitized_prompt, primary_fn, fallback_model_backend
    )

    if execution_result["status"] == "error":
        raise HTTPException(status_code=503, detail=execution_result)

    # Tier 4: Output Guardrails
    validated_output = GuardrailsEngine.validate_output(execution_result["output"])
    execution_result["output"] = validated_output

    return execution_result
