"""
RAG Evaluation Metrics in Depth: Context Precision, Context Recall,
Faithfulness, and Answer Relevance.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class RAGEvaluationSample:
    query: str
    retrieved_contexts: List[str]
    ground_truth_contexts: List[str]
    generated_answer: str
    ground_truth_answer: str


class RAGEvaluationMetricsEngine:
    def compute_context_recall(self, sample: RAGEvaluationSample) -> float:
        # What fraction of ground truth contexts were successfully retrieved?
        if not sample.ground_truth_contexts:
            return 1.0
        retrieved_set = set(sample.retrieved_contexts)
        hits = sum(1 for c in sample.ground_truth_contexts if c in retrieved_set)
        return round(hits / len(sample.ground_truth_contexts), 2)

    def compute_faithfulness(self, generated_answer: str, retrieved_contexts: List[str]) -> float:
        # Simplified token overlap grounding check
        context_words = set(" ".join(retrieved_contexts).lower().split())
        answer_words = generated_answer.lower().split()
        if not answer_words:
            return 0.0
        grounded_count = sum(1 for w in answer_words if w in context_words)
        return round(grounded_count / len(answer_words), 2)


if __name__ == "__main__":
    engine = RAGEvaluationMetricsEngine()
    sample = RAGEvaluationSample(
        query="What is the RPO target?",
        retrieved_contexts=["The disaster recovery RPO target is 5 minutes."],
        ground_truth_contexts=["The disaster recovery RPO target is 5 minutes."],
        generated_answer="The RPO target is 5 minutes.",
        ground_truth_answer="5 minutes"
    )
    recall = engine.compute_context_recall(sample)
    faithfulness = engine.compute_faithfulness(sample.generated_answer, sample.retrieved_contexts)
    assert recall == 1.0
    assert faithfulness > 0.8

    print("=== Day 05: RAG Evaluation Metrics Engine ===")
    print(f"Context Recall: {recall} | Faithfulness: {faithfulness}")
