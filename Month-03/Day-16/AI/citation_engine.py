"""
Citation & Provenance Attribution Engine
Tracks document ID, page number, section, and chunk ID through retrieval.
Validates generated citations against ground-truth evidence spans to detect
unsupported citations or citation hallucinations.
"""

import re
from typing import List, Dict, Any, Tuple


class CitationEngine:
    def __init__(self):
        self.citation_pattern = re.compile(r'\[(?:Doc|Ref|Source)\s*(\d+)\]', re.IGNORECASE)

    def extract_citations(self, response_text: str) -> List[int]:
        """Extracts numerical citation markers e.g. [Doc 1], [Ref 2]"""
        matches = self.citation_pattern.findall(response_text)
        return [int(m) for m in matches]

    def validate_grounding(
        self,
        response_text: str,
        retrieved_evidence: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Validates that:
        1. All citations in the response correspond to retrieved documents.
        2. Cited statements contain lexical/semantic overlap with the cited source chunks.
        3. Identifies hallucinated citations (referring to non-existent sources).
        """
        cited_indices = self.extract_citations(response_text)
        evidence_by_id = {idx + 1: doc for idx, doc in enumerate(retrieved_evidence)}

        valid_citations = []
        hallucinated_citations = []
        ungrounded_claims = []

        # Split response into statements
        sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', response_text) if s.strip()]

        for sentence in sentences:
            sentence_cites = [int(m) for m in self.citation_pattern.findall(sentence)]
            for cite_id in sentence_cites:
                if cite_id not in evidence_by_id:
                    hallucinated_citations.append({"citation_id": cite_id, "sentence": sentence})
                else:
                    # Check token overlap between sentence and cited chunk
                    cited_doc = evidence_by_id[cite_id]
                    s_words = set(re.findall(r'\w+', sentence.lower()))
                    doc_words = set(re.findall(r'\w+', cited_doc["text"].lower()))
                    overlap = len(s_words.intersection(doc_words)) / max(1, len(s_words))

                    if overlap >= 0.2:
                        valid_citations.append({
                            "citation_id": cite_id,
                            "source_id": cited_doc["id"],
                            "page": cited_doc.get("page", 1),
                            "overlap_ratio": round(overlap, 3),
                            "sentence": sentence
                        })
                    else:
                        ungrounded_claims.append({
                            "citation_id": cite_id,
                            "sentence": sentence,
                            "overlap_ratio": round(overlap, 3),
                            "reason": "Citation referenced, but content has low factual alignment with source."
                        })

        grounded = len(hallucinated_citations) == 0 and len(ungrounded_claims) == 0

        return {
            "grounded": grounded,
            "total_citations_found": len(cited_indices),
            "valid_citations": valid_citations,
            "hallucinated_citations": hallucinated_citations,
            "ungrounded_claims": ungrounded_claims
        }


if __name__ == "__main__":
    evidence = [
        {"id": "ch_01", "page": 4, "text": "PostgreSQL provides Write-Ahead Logging (WAL) ensuring durability across server crashes."},
        {"id": "ch_02", "page": 9, "text": "HNSW graphs use probabilistic skip-lists with M connections per vector node."}
    ]

    engine = CitationEngine()

    test_response = (
        "PostgreSQL uses Write-Ahead Logging (WAL) to guarantee transaction durability [Doc 1]. "
        "HNSW graphs maintain probabilistic multi-layer skip connections [Doc 2]. "
        "Quantum entanglement enables instant cross-database synchronization [Doc 99]."
    )

    result = engine.validate_grounding(test_response, evidence)

    print("=== Citation & Provenance Audit ===")
    print(f"Overall Grounded: {result['grounded']}")
    print(f"Total Citations: {result['total_citations_found']}")

    print("\nValid Grounded Citations:")
    for v in result["valid_citations"]:
        print(f" - [Doc {v['citation_id']}] -> Source: {v['source_id']} (Page {v['page']}) | Overlap: {v['overlap_ratio']}")

    print("\nHallucinated Non-Existent Citations:")
    for h in result["hallucinated_citations"]:
        print(f" - [Doc {h['citation_id']}] in: \"{h['sentence']}\"")
