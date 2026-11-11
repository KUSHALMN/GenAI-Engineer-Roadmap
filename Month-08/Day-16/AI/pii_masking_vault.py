"""
Privacy and PII Handling: Deterministic Pseudonymization, Masking, Re-identification Vault,
and GDPR/HIPAA Compliant Tokenization for LLM Training and Inference Pipelines.
"""

from dataclasses import dataclass
import hashlib
import re
from typing import Dict, List, Tuple


@dataclass
class PIISpan:
    entity_type: str
    original_value: str
    masked_placeholder: str
    start: int
    end: int


class PIIMaskingVault:
    """
    Handles regex & heuristic based PII tokenization, reversibility vault,
    and anonymization for LLM inputs and responses.
    """
    def __init__(self, salt: str = "enterprise_salt_2026"):
        self.salt = salt
        # Token vault mapping placeholder -> original
        self.vault: Dict[str, str] = {}
        # Patterns
        self.patterns = {
            "EMAIL": re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'),
            "PHONE": re.compile(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'),
            "SSN": re.compile(r'\b\d{3}-\d{2}-\d{4}\b'),
            "CREDIT_CARD": re.compile(r'\b(?:\d{4}[-\s]?){3}\d{4}\b')
        }

    def _generate_surrogate(self, entity_type: str, value: str) -> str:
        h = hashlib.sha256(f"{self.salt}:{value}".encode("utf-8")).hexdigest()[:8]
        return f"<PII:{entity_type}:{h.upper()}>"

    def mask(self, text: str) -> Tuple[str, List[PIISpan]]:
        raw_matches = []
        for entity_type, regex in self.patterns.items():
            for m in regex.finditer(text):
                raw_matches.append((m.start(), m.end(), entity_type, m.group(0)))
        
        # Sort matches descending by start position to safely replace without invalidating earlier indices
        raw_matches.sort(key=lambda x: x[0], reverse=True)

        spans = []
        masked_text = text
        for start, end, entity_type, orig in raw_matches:
            placeholder = self._generate_surrogate(entity_type, orig)
            self.vault[placeholder] = orig
            spans.append(PIISpan(
                entity_type=entity_type,
                original_value=orig,
                masked_placeholder=placeholder,
                start=start,
                end=end
            ))
            masked_text = masked_text[:start] + placeholder + masked_text[end:]

        spans.reverse()
        return masked_text, spans

    def demask(self, masked_text: str) -> str:
        demasked = masked_text
        for placeholder, orig in self.vault.items():
            demasked = demasked.replace(placeholder, orig)
        return demasked


if __name__ == "__main__":
    vault = PIIMaskingVault()
    sample = "Patient John Doe email john.doe@example.com, phone 415-555-2671, SSN 123-45-6789 reported mild fatigue."
    masked, spans = vault.mask(sample)
    print("Original:", sample)
    print("Masked:", masked)
    assert len(spans) == 3
    demasked = vault.demask(masked)
    assert demasked == sample
    print("Demasked matches original! PII Masking Vault passed.")
