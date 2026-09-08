from typing import List, Optional, Literal
from pydantic import BaseModel, Field, EmailStr, field_validator

class LineItem(BaseModel):
    description: str = Field(..., min_length=1)
    quantity: int = Field(..., ge=1)
    unit_price: float = Field(..., ge=0.0)
    total_price: float = Field(..., ge=0.0)

    @field_validator("total_price")
    @classmethod
    def validate_total(cls, v, info):
        qty = info.data.get("quantity")
        price = info.data.get("unit_price")
        if qty is not None and price is not None:
            expected = round(qty * price, 2)
            if abs(v - expected) > 0.05:
                raise ValueError(f"Total price {v} does not match expected {expected}")
        return round(v, 2)

class InvoiceExtraction(BaseModel):
    invoice_number: str
    vendor_name: str
    billing_date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
    line_items: List[LineItem]
    subtotal: float
    tax_amount: float
    total_amount: float

class SupportTicketExtraction(BaseModel):
    ticket_id: str
    customer_email: EmailStr
    urgency: Literal["low", "medium", "high", "critical"]
    category: Literal["billing", "technical", "account", "feature_request"]
    summary: str
    action_items: List[str] = Field(default_factory=list)
