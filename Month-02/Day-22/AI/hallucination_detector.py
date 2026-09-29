"""
Day 22 AI — Hallucination & Factuality Detection
Evaluates generated LLM responses against retrieved context to flag unsupported claims and entity drift.
"""
import os
import re
import json
from typing import List, Dict, Any


def tokenize_words(text: str) -> List[str]:
    """Tokenize text into lowercase alpha-numeric words."""
    return re.findall(r"\b\w+\b", text.lower())


def extract_entities(text: str) -> List[str]:
    """Extract named entities, acronyms, and numeric claims."""
    patterns = [
        r"\b[A-Z]{2,}\b",            # Acronyms (e.g., RAG, LoRA, HNSW)
        r"\b\d+(?:\.\d+)?%?\b",       # Numbers, percentages
        r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b"  # Proper nouns
    ]
    entities = set()
    for pat in patterns:
        for match in re.finditer(pat, text):
            entities.add(match.group(0))
    return list(entities)


def split_sentences(text: str) -> List[str]:
    """Split text into sentences cleanly."""
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    return [s.strip() for s in sentences if s.strip()]


class HallucinationDetector:
    """
    Analyzes generated responses against source contexts to calculate:
    - Sentence grounding ratio
    - Unsupported entity claims
    - Overall hallucination risk score
    """

    def __init__(self, token_overlap_threshold: float = 0.5):
        self.threshold = token_overlap_threshold

    def evaluate_sentence(self, sentence: str, context: str) -> Dict[str, Any]:
        s_words = set(tokenize_words(sentence))
        c_words = set(tokenize_words(context))

        if not s_words:
            return {"sentence": sentence, "grounded": True, "overlap": 1.0, "unsupported_entities": []}

        overlap = len(s_words & c_words) / len(s_words)
        
        # Check entities
        sent_entities = extract_entities(sentence)
        unsupported = [e for e in sent_entities if e.lower() not in context.lower()]

        is_grounded = (overlap >= self.threshold) and (len(unsupported) == 0)

        return {
            "sentence": sentence,
            "grounded": is_grounded,
            "token_overlap": round(overlap, 4),
            "unsupported_entities": unsupported,
        }

    def evaluate(self, response: str, context: str) -> Dict[str, Any]:
        sentences = split_sentences(response)
        if not sentences:
            return {"hallucination_score": 0.0, "is_safe": True, "sentence_breakdown": []}

        breakdown = [self.evaluate_sentence(s, context) for s in sentences]
        ungrounded_count = sum(1 for b in breakdown if not b["grounded"])
        hallucination_score = round(ungrounded_count / len(sentences), 4)

        return {
            "total_sentences": len(sentences),
            "ungrounded_sentences": ungrounded_count,
            "hallucination_score": hallucination_score,
            "is_safe": hallucination_score <= 0.25,
            "breakdown": breakdown,
        }


# ── Interactive / Demo Test Cases ───────────────────────────────────────────────

TEST_SUITE = [
    {
        "context": (
            "FlashAttention is an exact attention algorithm that reduces memory reads/writes between GPU HBM and SRAM. "
            "It speeds up transformer training and inference by up to 3x without approximating softmax."
        ),
        "response": (
            "FlashAttention is an exact attention method optimizing GPU SRAM usage. "
            "It delivers up to 3x speedups for training and inference."
        ),
        "expected_risk": "Low",
    },
    {
        "context": (
            "Vector databases utilize Approximate Nearest Neighbor (ANN) indexing like HNSW to search millions of vectors in sub-5ms."
        ),
        "response": (
            "Vector databases use HNSW for fast search. "
            "It was invented by Google DeepMind in 2024 and achieves 99.9% quantum accuracy."
        ),
        "expected_risk": "High (invented claims & quantum accuracy)",
    },
]

def run_hallucination_benchmark():
    detector = HallucinationDetector(token_overlap_threshold=0.45)
    print("=" * 60)
    print("[RUN] RAG Hallucination & Factuality Detection Benchmark")
    print("=" * 60)

    for i, test in enumerate(TEST_SUITE, 1):
        print(f"\nTest Case {i}: Expected Risk: {test['expected_risk']}")
        res = detector.evaluate(test["response"], test["context"])
        print(f"  Total Sentences:      {res['total_sentences']}")
        print(f"  Ungrounded Sentences: {res['ungrounded_sentences']}")
        print(f"  Hallucination Score:  {res['hallucination_score']} ({'PASS' if res['is_safe'] else 'FAIL'})")
        for b in res["breakdown"]:
            status = "[GROUNDED]" if b["grounded"] else "[HALLUCINATED]"
            print(f"    - {status} \"{b['sentence']}\"")
            if b["unsupported_entities"]:
                print(f"      Unsupported Entities: {b['unsupported_entities']}")


if __name__ == "__main__":
    run_hallucination_benchmark()
