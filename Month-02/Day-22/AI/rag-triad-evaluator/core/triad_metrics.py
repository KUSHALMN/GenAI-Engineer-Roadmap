"""
core/triad_metrics.py — Mathematical Formulations for RAG Triad Metrics
1. Context Relevance: How relevant is the retrieved context to the query?
2. Faithfulness: Is the generated answer grounded in the retrieved context?
3. Answer Relevance: Does the generated answer address the question?
"""
import re
from typing import Dict, Any, Set


def tokenize(text: str) -> Set[str]:
    """Tokenize text into lowercase words."""
    return set(re.findall(r"\b\w+\b", text.lower()))


def context_relevance(question: str, context: str) -> float:
    """Measures the proportion of question information covered by retrieved context."""
    q_tokens = tokenize(question)
    c_tokens = tokenize(context)
    if not q_tokens:
        return 0.0
    return round(len(q_tokens & c_tokens) / len(q_tokens), 4)


def faithfulness(answer: str, context: str) -> float:
    """Measures what fraction of the answer tokens are directly grounded in the context."""
    a_tokens = tokenize(answer)
    c_tokens = tokenize(context)
    if not a_tokens:
        return 0.0
    return round(len(a_tokens & c_tokens) / len(a_tokens), 4)


def answer_relevance(answer: str, question: str) -> float:
    """Measures what fraction of the question tokens are addressed in the answer."""
    a_tokens = tokenize(answer)
    q_tokens = tokenize(question)
    if not q_tokens:
        return 0.0
    return round(len(a_tokens & q_tokens) / len(q_tokens), 4)


def compute_rag_triad(question: str, context: str, answer: str) -> Dict[str, Any]:
    """Calculates all three RAG Triad scores plus composite overall score."""
    cr = context_relevance(question, context)
    fa = faithfulness(answer, context)
    ar = answer_relevance(answer, question)
    composite = round((cr + fa + ar) / 3.0, 4)

    return {
        "context_relevance": cr,
        "faithfulness": fa,
        "answer_relevance": ar,
        "composite_score": composite,
        "is_acceptable": (cr >= 0.35 and fa >= 0.50 and ar >= 0.40),
    }
