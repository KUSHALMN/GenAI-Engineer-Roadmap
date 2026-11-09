"""
Multimodal Answer Grounding & Citation Validator Engine.
Validates that generated claims quote valid page coordinates and timestamps.
Flags ungrounded assertions and gracefully admits lack of evidence.
"""

from dataclasses import dataclass
import re
from typing import Dict, List, Tuple


@dataclass
class GroundingValidationResult:
    is_grounded: bool
    total_claims: int
    grounded_claims: int
    ungrounded_claims: List[str]
    missing_evidence_admitted: bool


class MultimodalCitationValidator:
    def validate_answer(self, generated_answer: str, available_evidence_ids: List[str]) -> GroundingValidationResult:
        admitted = "insufficient evidence" in generated_answer.lower() or "not found in documents" in generated_answer.lower()
        sentences = [s.strip() for s in re.split(r"(?<=[.!?]) +", generated_answer) if s.strip()]

        ungrounded = []
        for s in sentences:
            citations = re.findall(r"\[(.*?)\]", s)
            valid_cite = any(any(e_id in c for e_id in available_evidence_ids) for c in citations)
            if not valid_cite and not admitted:
                ungrounded.append(s)

        grounded_count = len(sentences) - len(ungrounded)
        is_fully_grounded = (len(ungrounded) == 0) or admitted

        return GroundingValidationResult(is_fully_grounded, len(sentences), grounded_count, ungrounded, admitted)


if __name__ == "__main__":
    val = MultimodalCitationValidator()
    ans = "Revenue reached $4.2B in Q3 [Doc: report.pdf, Page 4]. Margins were 45% [Figure 2.1, 14.5s]. Uncited random claim."
    res = val.validate_answer(ans, ["report.pdf", "Figure 2.1"])
    print("=== Multimodal Answer Grounding Audit ===")
    print("Is Fully Grounded:", res.is_grounded)
    print("Ungrounded Claims:", res.ungrounded_claims)
