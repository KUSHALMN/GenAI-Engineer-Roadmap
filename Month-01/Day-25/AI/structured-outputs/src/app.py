from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any

try:
    from .schemas import InvoiceExtraction, SupportTicketExtraction
    from .validator import StructuredOutputValidator
except ImportError:
    from schemas import InvoiceExtraction, SupportTicketExtraction
    from validator import StructuredOutputValidator

app = FastAPI(
    title="Structured Outputs & Pydantic Validation API",
    description="LLM raw output parsing, auto-repair, and strict Pydantic V2 validation.",
    version="1.0.0"
)

class RawLLMPayload(BaseModel):
    raw_completion: str = Field(..., description="Raw text or markdown output from LLM")

@app.get("/")
def root():
    return {"status": "online", "topic": "Day 25: Structured Outputs + Pydantic"}

@app.post("/api/v1/extract/invoice", response_model=InvoiceExtraction)
def extract_invoice(payload: RawLLMPayload):
    instance, error = StructuredOutputValidator.parse_and_validate(
        payload.raw_completion, InvoiceExtraction
    )
    if error:
        raise HTTPException(
            status_code=422,
            detail={"error": "Schema validation failed", "llm_retry_prompt": error}
        )
    return instance

@app.post("/api/v1/extract/ticket", response_model=SupportTicketExtraction)
def extract_ticket(payload: RawLLMPayload):
    instance, error = StructuredOutputValidator.parse_and_validate(
        payload.raw_completion, SupportTicketExtraction
    )
    if error:
        raise HTTPException(
            status_code=422,
            detail={"error": "Schema validation failed", "llm_retry_prompt": error}
        )
    return instance
