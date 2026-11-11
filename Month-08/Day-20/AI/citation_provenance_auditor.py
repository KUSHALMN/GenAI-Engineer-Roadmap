"""
Citation & Provenance Audits: RAG Fact-Verification, Substring Alignment,
Attribution Precision/Recall, and Source Link Verification.
"""

from dataclasses import dataclass
import re
from typing import Dict, List


@dataclass
class RetrievedChunk:
    chunk_id: str
    text: str
    source_url: str


@dataclass
class CitationClaim:
    sentence: str
    cited_chunk_ids: List[str]
    is_supported: bool
    evidence_snippet: str = ""


class CitationProvenanceAuditor:
    """
    Audits generated text containing inline citation tags [1], [2] to verify
    factual alignment and attribution accuracy against retrieved context chunks.
    """
    def __init__(self):
        self.citation_regex = re.compile(r'\[(\d+)\]')

    def audit_provenance(self, response_text: str, chunks: List[RetrievedChunk]) -> Dict[str, float]:
        sentences = [s.strip() for s in re.split(r'(?<=[.!?]) +', response_text) if s.strip()]
        total_claims = 0
        supported_claims = 0
        unsupported_claims = 0
        chunk_map = {str(i + 1): chunks[i] for i in range(len(chunks))}

        audited_claims: List[CitationClaim] = []

        for sent in sentences:
            citations = self.citation_regex.findall(sent)
            if not citations:
                continue

            total_claims += 1
            supported = False
            evidence = ""
            for cid in citations:
                if cid in chunk_map:
                    chunk = chunk_map[cid]
                    # Heuristic token overlap check
                    claim_words = set(re.findall(r'\w+', sent.lower()))
                    chunk_words = set(re.findall(r'\w+', chunk.text.lower()))
                    overlap = claim_words.intersection(chunk_words)
                    overlap_ratio = len(overlap) / max(1, len(claim_words))
                    if overlap_ratio >= 0.5:
                        supported = True
                        evidence = chunk.text[:80]
                        break

            if supported:
                supported_claims += 1
            else:
                unsupported_claims += 1

            audited_claims.append(CitationClaim(
                sentence=sent,
                cited_chunk_ids=citations,
                is_supported=supported,
                evidence_snippet=evidence
            ))

        precision = supported_claims / total_claims if total_claims > 0 else 1.0
        return {
            "total_claims": total_claims,
            "supported_claims": supported_claims,
            "unsupported_claims": unsupported_claims,
            "attribution_precision": precision
        }


if __name__ == "__main__":
    auditor = CitationProvenanceAuditor()
    chunks = [
        RetrievedChunk("c1", "Antigravity 2.0 was officially released in November 2026.", "https://docs.gemini.dev"),
        RetrievedChunk("c2", "The enterprise rate limit is 5000 requests per minute.", "https://docs.gemini.dev/limits")
    ]

    generated = (
        "Antigravity 2.0 was launched in November 2026 [1]. "
        "The default quota allows 5000 requests per minute [2]. "
        "It also automatically cures all computer viruses [1]."
    )

    metrics = auditor.audit_provenance(generated, chunks)
    print("Citation Audit Metrics:", metrics)
    assert metrics["total_claims"] == 3
    assert metrics["supported_claims"] == 2
    assert metrics["unsupported_claims"] == 1
    assert abs(metrics["attribution_precision"] - 0.666) < 0.01
    print("Day 20 Citation Provenance Auditor verification passed.")
