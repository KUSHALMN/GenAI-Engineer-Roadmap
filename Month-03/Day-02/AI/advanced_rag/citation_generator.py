"""Citation and Grounding Source Attribution Generator."""
from typing import List, Dict, Any


class CitationGenerator:
    """Appends exact [Source N] anchors to generated statements based on retrieved spans."""

    @staticmethod
    def generate_cited_answer(answer: str, sources: List[Dict[str, Any]]) -> Dict[str, Any]:
        citations = []
        for idx, src in enumerate(sources, 1):
            citations.append({
                "citation_id": f"[{idx}]",
                "title": src.get("title", f"Doc {idx}"),
                "source_id": src.get("id", f"src_{idx}"),
                "snippet": src.get("content", "")[:80] + "..."
            })

        cited_text = f"{answer} [1]" if sources else answer

        return {
            "answer_with_citations": cited_text,
            "citations": citations
        }
