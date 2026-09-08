import sys
import os
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from app import app
from validator import StructuredOutputValidator
from schemas import InvoiceExtraction, SupportTicketExtraction

client = TestClient(app)

def test_json_repair_markdown_fences():
    raw = """
    ```json
    {
      "ticket_id": "TICK-901",
      "customer_email": "alex@enterprise.com",
      "urgency": "high",
      "category": "technical",
      "summary": "Database connectivity loss in us-east region",
      "action_items": ["Restart RDS pool", "Check security group",]
    }
    ```
    """
    instance, err = StructuredOutputValidator.parse_and_validate(raw, SupportTicketExtraction)
    assert err is None
    assert instance is not None
    assert instance.ticket_id == "TICK-901"
    assert len(instance.action_items) == 2

def test_invoice_extraction_validation():
    valid_raw = """{
      "invoice_number": "INV-2024-001",
      "vendor_name": "Cloud Infra Inc",
      "billing_date": "2024-05-15",
      "line_items": [
        {"description": "GPU Server Instance", "quantity": 2, "unit_price": 50.0, "total_price": 100.0}
      ],
      "subtotal": 100.0,
      "tax_amount": 10.0,
      "total_amount": 110.0
    }"""
    response = client.post("/api/v1/extract/invoice", json={"raw_completion": valid_raw})
    assert response.status_code == 200
    assert response.json()["invoice_number"] == "INV-2024-001"

def test_validation_error_feedback():
    # Invalid email and missing required field
    invalid_raw = """{
      "ticket_id": "TICK-902",
      "customer_email": "not-an-email",
      "urgency": "low",
      "category": "billing"
    }"""
    response = client.post("/api/v1/extract/ticket", json={"raw_completion": invalid_raw})
    assert response.status_code == 422
    data = response.json()
    assert "llm_retry_prompt" in data["detail"]
    assert "customer_email" in data["detail"]["llm_retry_prompt"]
