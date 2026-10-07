"""Concrete tool implementations and execution handlers."""
import math
from typing import Dict, Any


class ToolExecutor:
    """Executes validated function calls."""

    @staticmethod
    def calculate_mortgage(principal: float, annual_rate: float, years: int) -> Dict[str, Any]:
        """Calculates monthly payment: M = P [ i(1 + i)^n ] / [ (1 + i)^n – 1]"""
        monthly_rate = annual_rate / 12.0
        n_months = years * 12
        if monthly_rate == 0:
            monthly_payment = principal / n_months
        else:
            factor = math.pow(1 + monthly_rate, n_months)
            monthly_payment = principal * (monthly_rate * factor) / (factor - 1)

        total_payment = monthly_payment * n_months
        return {
            "principal": principal,
            "monthly_payment": round(monthly_payment, 2),
            "total_payment": round(total_payment, 2),
            "total_interest": round(total_payment - principal, 2)
        }

    @staticmethod
    def lookup_stock_ticker(symbol: str) -> Dict[str, Any]:
        """Simulates stock valuation lookup."""
        mock_data = {
            "AAPL": {"price": 232.50, "currency": "USD", "pe_ratio": 33.2},
            "GOOGL": {"price": 181.20, "currency": "USD", "pe_ratio": 24.1},
            "MSFT": {"price": 420.80, "currency": "USD", "pe_ratio": 35.7},
        }
        sym = symbol.upper()
        if sym in mock_data:
            return {"symbol": sym, **mock_data[sym]}
        return {"symbol": sym, "price": 100.0, "currency": "USD", "pe_ratio": 20.0, "note": "Default market rate"}
