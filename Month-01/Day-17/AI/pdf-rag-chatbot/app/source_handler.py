from __future__ import annotations

from typing import Any, Dict, List


def format_sources(retrieved_docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Format and deduplicate source metadata citations."""
    sources: List[Dict[str, Any]] = []
    seen = set()

    for idx, doc in enumerate(retrieved_docs):
        src_name = doc.get("source", "unknown")
        page = doc.get("page", 1)
        key = (src_name, page)

        if key not in seen:
            seen.add(key)
            sources.append(
                {
                    "citation_id": len(sources) + 1,
                    "source": src_name,
                    "page": page,
                    "snippet": doc.get("text", "")[:150] + "...",
                    "score": round(float(doc.get("score", 0.0)), 4),
                }
            )

    return sources
