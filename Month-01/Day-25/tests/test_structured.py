import sys
import os
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from app import app
from validator import StructuredOutputValidator
from schemas import InvoiceExtraction, SupportTicketExtraction

client = TestClient(app)

def test_json_repair():
    raw = """
    ```json
    {
      "ticket_id": "TICK-100",
      "customer_email": "dev@ops.io",
      "urgency": "medium",
      "category": "technical",
      "summary": "Disk space warning on node 4",
      "action_items": ["Rotate logs", "Scale EBS volume",]
    }
    ```
    """
    instance, err = StructuredOutputValidator.parse_and_validate(raw, SupportTicketExtraction)
    assert err is None
    assert instance is not None
    assert instance.ticket_id == "TICK-100"

def test_invoice_api_valid():
    raw = """{
      "invoice_number": "INV-5501",
      "vendor_name": "Acme SaaS",
      "billing_date": "2024-07-01",
      "line_items": [
        {"description": "Core Seats", "quantity": 5, "unit_price": 20.0, "total_price": 100.0}
      ],
      "subtotal": 100.0,
      "tax_amount": 5.0,
      "total_amount": 105.0
    }"""
    response = client.post("/api/v1/extract/invoice", json={"raw_completion": raw})
    assert response.status_code == 200
    assert response.json()["total_amount"] == 105.0
