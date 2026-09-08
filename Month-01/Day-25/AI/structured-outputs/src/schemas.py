from typing import List, Optional, Literal
from pydantic import BaseModel, Field, EmailStr, field_validator

class LineItem(BaseModel):
    description: str = Field(..., min_length=1, description="Item description")
    quantity: int = Field(..., ge=1, description="Number of units")
    unit_price: float = Field(..., ge=0.0, description="Price per unit")
    total_price: float = Field(..., ge=0.0, description="Quantity * unit price")

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
    invoice_number: str = Field(..., description="Invoice identifier e.g. INV-1024")
    vendor_name: str = Field(..., min_length=1)
    billing_date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$", description="YYYY-MM-DD")
    line_items: List[LineItem] = Field(..., min_items=1)
    subtotal: float = Field(..., ge=0.0)
    tax_amount: float = Field(..., ge=0.0)
    total_amount: float = Field(..., ge=0.0)

class SupportTicketExtraction(BaseModel):
    ticket_id: str
    customer_email: EmailStr
    urgency: Literal["low", "medium", "high", "critical"]
    category: Literal["billing", "technical", "account", "feature_request"]
    summary: str = Field(..., max_length=200)
    action_items: List[str] = Field(default_factory=list)
