"""
RAG Triad Evaluator:
1. Context Relevance: Retrieved context quality wrt user question
2. Faithfulness (Groundedness): Answer hallucination check wrt retrieved context
3. Answer Relevance: Completeness of answer wrt user query
"""

import json
from typing import Any, Dict, List


class RAGEvaluator:
    """
    Computes heuristic and sentence-level alignment scores across the RAG triad.
    """

    @staticmethod
    def _extract_ngrams(text: str, n: int = 1) -> Set[str]:
        words = [w.strip(".,!?;:()[]\"'").lower() for w in text.split() if len(w) > 2]
        if n == 1:
            return set(words)
        return {" ".join(words[i:i+n]) for i in range(len(words) - n + 1)}

    @classmethod
    def _stem_match(cls, word1: str, word2: str) -> bool:
        """Simple stem/prefix matching for inflection handling (e.g. weight/weights)."""
        w1, w2 = word1.lower(), word2.lower()
        if w1 == w2:
            return True
        if len(w1) >= 4 and len(w2) >= 4:
            return w1.startswith(w2[:4]) or w2.startswith(w1[:4])
        return False

    @classmethod
    def context_relevance(cls, query: str, context: str) -> float:
        """
        Fraction of significant query terms and key concepts represented in retrieved context.
        """
        query_terms = cls._extract_ngrams(query, 1)
        if not query_terms:
            return 1.0
        context_terms = cls._extract_ngrams(context, 1)
        matched = 0
        for qt in query_terms:
            if any(cls._stem_match(qt, ct) for ct in context_terms):
                matched += 1
        return round(matched / len(query_terms), 4)

    @classmethod
    def faithfulness(cls, answer: str, context: str) -> float:
        """
        Estimates groundedness: checks if answer claims/ngrams exist in the context.
        A score of 1.0 indicates high groundedness (no unbacked vocabulary/hallucinations).
        """
        answer_sentences = [s.strip() for s in answer.split(".") if len(s.strip()) > 5]
        if not answer_sentences:
            return 1.0

        grounded_count = 0
        context_words = cls._extract_ngrams(context, 1)

        for sent in answer_sentences:
            sent_words = cls._extract_ngrams(sent, 1)
            if not sent_words:
                continue
            matched = sum(1 for sw in sent_words if any(cls._stem_match(sw, cw) for cw in context_words))
            supported = matched / len(sent_words)
            if supported >= 0.40:
                grounded_count += 1

        return round(grounded_count / len(answer_sentences), 4)

    @classmethod
    def answer_relevance(cls, query: str, answer: str) -> float:
        """
        Calculates answer relevance: semantic intent and question word coverage.
        """
        q_unigrams = cls._extract_ngrams(query, 1)
        a_unigrams = cls._extract_ngrams(answer, 1)
        if not q_unigrams:
            return 1.0

        matched = sum(1 for qu in q_unigrams if any(cls._stem_match(qu, au) for au in a_unigrams))
        unigram_cov = matched / len(q_unigrams)
        return round(min(1.0, unigram_cov * 1.2), 4)

    @classmethod
    def evaluate_rag_triad(cls, query: str, context: str, answer: str) -> Dict[str, Any]:
        """Runs complete RAG triad benchmark."""
        c_rel = cls.context_relevance(query, context)
        faith = cls.faithfulness(answer, context)
        a_rel = cls.answer_relevance(query, answer)

        triad_avg = round((c_rel + faith + a_rel) / 3.0, 4)

        return {
            "context_relevance": c_rel,
            "faithfulness": faith,
            "answer_relevance": a_rel,
            "rag_triad_score": triad_avg,
            "is_grounded": faith >= 0.75,
            "is_relevant": a_rel >= 0.60,
        }


if __name__ == "__main__":
    from typing import Set

    q = "What is the primary role of an attention mechanism in Transformers?"
    ctx = "The attention mechanism in Transformers allows the model to dynamically weight tokens in a sequence."
    ans_good = "It dynamically weights tokens in a sequence to capture long range dependencies."
    ans_hallucinated = "The attention mechanism uses quantum neural networks to run at speed of light."

    eval_good = RAGEvaluator.evaluate_rag_triad(q, ctx, ans_good)
    eval_bad = RAGEvaluator.evaluate_rag_triad(q, ctx, ans_hallucinated)

    print("Good RAG Triad:", eval_good)
    print("Hallucinated Triad:", eval_bad)
    assert eval_good["is_grounded"] is True
    assert eval_bad["is_grounded"] is False
    print("RAGEvaluator tests passed successfully!")
