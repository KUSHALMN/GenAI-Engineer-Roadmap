import re
import base64
from typing import List, Optional, Dict, Any

class SecurityFirewall:
    INJECTION_PATTERNS = [
        r"ignore\s+(all\s+)?(previous|above|system)\s+instructions?",
        r"disregard\s+(all\s+)?(prior|system)\s+(rules|prompts?)",
        r"you\s+are\s+now\s+(in\s+developer\s+mode|dan|jailbroken)",
        r"system\s*override",
        r"print\s+(your\s+)?system\s+prompt",
        r"reveal\s+(the\s+)?confidential\s+instructions"
    ]

    DELIMITER_SPOOFING = [
        r"<\/?system>",
        r"\[INST\]",
        r"\[\/INST\]",
        r"<\|im_start\|>",
        r"<\|im_end\|>"
    ]

    def __init__(self, canary_tokens: Optional[List[str]] = None):
        self.canary_tokens = canary_tokens or ["CANARY_SECRET_987654"]

    def _decode_obfuscation(self, text: str) -> List[str]:
        candidates = [text]
        b64_matches = re.findall(r"\b[A-Za-z0-9+/]{16,}={0,2}\b", text)
        for token in b64_matches:
            try:
                decoded = base64.b64decode(token).decode("utf-8", errors="ignore")
                if len(decoded.strip()) > 4:
                    candidates.append(decoded)
            except Exception:
                pass
        return candidates

    def inspect_prompt(self, user_prompt: str) -> Dict[str, Any]:
        decoded_variants = self._decode_obfuscation(user_prompt)
        for variant in decoded_variants:
            for delim in self.DELIMITER_SPOOFING:
                if re.search(delim, variant, re.IGNORECASE):
                    return {
                        "is_safe": False,
                        "threat_type": "DELIMITER_SPOOFING",
                        "details": f"Attempted special token injection: {delim}"
                    }
            for pat in self.INJECTION_PATTERNS:
                if re.search(pat, variant, re.IGNORECASE):
                    return {
                        "is_safe": False,
                        "threat_type": "PROMPT_INJECTION",
                        "details": f"Matched injection pattern: '{pat}'"
                    }
        return {"is_safe": True, "threat_type": None, "details": "Safe prompt"}

    def inspect_completion_for_leak(self, completion: str) -> bool:
        return any(canary in completion for canary in self.canary_tokens)
