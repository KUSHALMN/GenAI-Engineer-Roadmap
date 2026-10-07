"""Intent Router directing queries to specialized sub-agents or deterministic paths."""
import re
from typing import Dict, Any


class IntentRouter:
    """Classifies user intent into specialized execution routes."""

    ROUTES = {
        "FINANCIAL_MATH": [r"mortgage", r"interest", r"amortization", r"calculate", r"dividend"],
        "RESEARCH_FACT": [r"who is", r"what happened", r"latest news", r"history of", r"compare"],
        "DATABASE_LOOKUP": [r"select", r"customers", r"orders", r"revenue", r"table"],
    }

    def route(self, query: str) -> Dict[str, Any]:
        q_lower = query.lower()
        for route_name, patterns in self.ROUTES.items():
            for pat in patterns:
                if re.search(pat, q_lower):
                    return {
                        "route": route_name,
                        "confidence": 0.95,
                        "agent_type": "specialized_agent"
                    }

        return {
            "route": "GENERAL_REASONING",
            "confidence": 0.70,
            "agent_type": "general_react_agent"
        }
