"""OpenAI/Groq compatible Tool and Function calling schemas."""
from typing import Dict, Any, List

TOOL_SCHEMAS: List[Dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "calculate_mortgage",
            "description": "Calculates monthly mortgage payments based on principal, annual interest rate, and term years.",
            "parameters": {
                "type": "object",
                "properties": {
                    "principal": {"type": "number", "description": "Total loan amount"},
                    "annual_rate": {"type": "number", "description": "Annual interest rate (e.g. 0.065 for 6.5%)"},
                    "years": {"type": "integer", "description": "Loan term in years"}
                },
                "required": ["principal", "annual_rate", "years"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "lookup_stock_ticker",
            "description": "Looks up real-time stock valuation and price-to-earnings ratio.",
            "parameters": {
                "type": "object",
                "properties": {
                    "symbol": {"type": "string", "description": "Stock ticker symbol (e.g. AAPL, GOOGL)"}
                },
                "required": ["symbol"]
            }
        }
    }
]
