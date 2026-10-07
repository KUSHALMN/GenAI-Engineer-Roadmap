"""Fallback handler routing failed requests to alternative models or cache."""
import logging
from typing import List, Callable, Any, Dict, Optional

logger = logging.getLogger("reliability.fallback")


class FallbackHandler:
    """Orchestrates sequential degradation across primary and fallback LLMs."""

    def __init__(self, primary_provider: Callable, fallback_providers: List[Callable]):
        self.primary_provider = primary_provider
        self.fallback_providers = fallback_providers

    def execute(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Try primary provider first, cascading through fallbacks upon error."""
        errors = []
        try:
            res = self.primary_provider(prompt, **kwargs)
            return {"source": "primary", "response": res, "errors": []}
        except Exception as e:
            errors.append(f"Primary failed: {str(e)}")

        for idx, fallback_fn in enumerate(self.fallback_providers, start=1):
            try:
                res = fallback_fn(prompt, **kwargs)
                return {
                    "source": f"fallback_{idx}",
                    "response": res,
                    "errors": errors
                }
            except Exception as e:
                errors.append(f"Fallback {idx} failed: {str(e)}")

        return {
            "source": "static_safe_response",
            "response": "Service is currently operating under degraded availability. Please retry shortly.",
            "errors": errors
        }
