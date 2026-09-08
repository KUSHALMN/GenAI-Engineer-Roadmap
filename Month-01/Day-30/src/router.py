import re
from typing import Dict, Any

class DynamicModelRouter:
    COMPLEX_PATTERNS = [
        r"\b(code|algorithm|refactor|debug|derive|proof)\b",
        r"\b(architecture|system design|scalability)\b"
    ]
    LIGHTWEIGHT_MODEL = "gpt-4o-mini"
    FRONTIER_MODEL = "gpt-4o"

    @classmethod
    def route_request(cls, prompt: str) -> Dict[str, Any]:
        p_lower = prompt.lower()
        is_complex = any(re.search(pat, p_lower) for pat in cls.COMPLEX_PATTERNS)
        if is_complex or len(prompt.split()) > 150:
            return {"selected_model": cls.FRONTIER_MODEL, "tier": "frontier"}
        return {"selected_model": cls.LIGHTWEIGHT_MODEL, "tier": "lightweight"}
