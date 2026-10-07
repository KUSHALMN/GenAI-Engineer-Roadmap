"""Token usage and pricing calculator for LLM invocations."""
from typing import Dict, Any


# Standard token pricing per 1M tokens ($ USD)
MODEL_PRICING_PER_1M = {
    "llama-3.3-70b-versatile": {"input": 0.59, "output": 0.79},
    "llama-3.1-8b-instant": {"input": 0.05, "output": 0.08},
    "gpt-4o": {"input": 2.50, "output": 10.00},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "claude-3-5-sonnet": {"input": 3.00, "output": 15.00},
    "default": {"input": 0.50, "output": 1.00},
}


class CostTracker:
    """Tracks token consumption and calculates USD monetary costs."""

    def __init__(self):
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0
        self.total_cost_usd = 0.0
        self.invocation_records = []

    def record_usage(
        self,
        model: str,
        prompt_tokens: int,
        completion_tokens: int,
        request_id: str = ""
    ) -> Dict[str, Any]:
        """Record token usage for a single model call and calculate cost."""
        pricing = MODEL_PRICING_PER_1M.get(model, MODEL_PRICING_PER_1M["default"])
        input_cost = (prompt_tokens / 1_000_000) * pricing["input"]
        output_cost = (completion_tokens / 1_000_000) * pricing["output"]
        call_cost = round(input_cost + output_cost, 6)

        self.total_prompt_tokens += prompt_tokens
        self.total_completion_tokens += completion_tokens
        self.total_cost_usd += call_cost

        record = {
            "request_id": request_id,
            "model": model,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": prompt_tokens + completion_tokens,
            "cost_usd": call_cost,
        }
        self.invocation_records.append(record)
        return record

    def get_summary(self) -> Dict[str, Any]:
        """Get aggregate metrics."""
        return {
            "total_invocations": len(self.invocation_records),
            "total_prompt_tokens": self.total_prompt_tokens,
            "total_completion_tokens": self.total_completion_tokens,
            "total_tokens": self.total_prompt_tokens + self.total_completion_tokens,
            "total_cost_usd": round(self.total_cost_usd, 6),
        }
