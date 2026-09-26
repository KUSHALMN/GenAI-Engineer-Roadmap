"""
Metadata Filtering Engine for Vector & Document Retrieval.
Supports pre-filtering (filtering candidate universe before vector search)
and post-filtering (pruning results based on dynamic user security attributes).
"""

from typing import Any, Dict, List, Optional
from hybrid_retriever import Document


class MetadataFilter:
    """Executes boolean, comparison, and containment filters on document metadata."""

    @staticmethod
    def match_criteria(doc_meta: Dict[str, Any], criteria: Dict[str, Any]) -> bool:
        """
        Evaluates criteria dict against document metadata:
        e.g.: {"category": "security", "access_level": {"$lte": 2}, "tags": {"$in": ["api"]}}
        """
        for key, condition in criteria.items():
            if key not in doc_meta:
                return False

            val = doc_meta[key]

            # If condition is an operator dictionary
            if isinstance(condition, dict):
                for op, target in condition.items():
                    if op == "$eq" and val != target:
                        return False
                    elif op == "$ne" and val == target:
                        return False
                    elif op == "$gt" and not (val > target):
                        return False
                    elif op == "$gte" and not (val >= target):
                        return False
                    elif op == "$lt" and not (val < target):
                        return False
                    elif op == "$lte" and not (val <= target):
                        return False
                    elif op == "$in" and val not in target:
                        return False
            else:
                # Direct equality check
                if val != condition:
                    return False

        return True

    @classmethod
    def filter_documents(cls, docs: List[Document], criteria: Dict[str, Any]) -> List[Document]:
        """Filters list of documents matching criteria."""
        return [d for d in docs if cls.match_criteria(d.metadata, criteria)]


if __name__ == "__main__":
    docs = [
        Document("d1", "Public guidelines", {"category": "policy", "access_level": 1, "department": "HR"}),
        Document("d2", "Internal security architecture", {"category": "tech", "access_level": 3, "department": "Sec"}),
        Document("d3", "Standard engineering onboarding", {"category": "tech", "access_level": 2, "department": "Eng"}),
    ]

    # Pre-filter: department == tech and access_level <= 2
    filtered = MetadataFilter.filter_documents(docs, {"category": "tech", "access_level": {"$lte": 2}})
    assert len(filtered) == 1
    assert filtered[0].doc_id == "d3"

    print("Metadata filter tests passed successfully!")
