from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

try:
    from .schemas import InvoiceExtraction, SupportTicketExtraction
    from .validator import StructuredOutputValidator
except ImportError:
    from schemas import InvoiceExtraction, SupportTicketExtraction
    from validator import StructuredOutputValidator

app = FastAPI(title="Structured Outputs API - Day 25")

class RawLLMPayload(BaseModel):
    raw_completion: str

@app.get("/")
def root():
    return {"status": "online", "topic": "Day 25: Structured Outputs + Pydantic"}

@app.post("/api/v1/extract/invoice", response_model=InvoiceExtraction)
def extract_invoice(payload: RawLLMPayload):
    instance, error = StructuredOutputValidator.parse_and_validate(
        payload.raw_completion, InvoiceExtraction
    )
    if error:
        raise HTTPException(status_code=422, detail={"error": error})
    return instance

@app.post("/api/v1/extract/ticket", response_model=SupportTicketExtraction)
def extract_ticket(payload: RawLLMPayload):
    instance, error = StructuredOutputValidator.parse_and_validate(
        payload.raw_completion, SupportTicketExtraction
    )
    if error:
        raise HTTPException(status_code=422, detail={"error": error})
    return instance
