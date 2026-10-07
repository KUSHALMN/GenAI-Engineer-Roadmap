"""Metadata Filter applying boolean predicates and pre/post-retrieval filters."""
from typing import List, Dict, Any


class MetadataFilter:
    """Filters document collections by tenant, access role, or date range."""

    @staticmethod
    def apply_filters(documents: List[Dict[str, Any]], filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        filtered = []
        for doc in documents:
            metadata = doc.get("metadata", {})
            match = True
            for key, expected_val in filters.items():
                if metadata.get(key) != expected_val:
                    match = False
                    break
            if match:
                filtered.append(doc)
        return filtered
