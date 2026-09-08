import math
import re
from typing import List, Dict, Any, Set
from collections import Counter

class PromptEvaluator:
    """
    Automated evaluation framework for production LLM prompts.
    Provides deterministic lexical metrics (Exact Match, BLEU, ROUGE-L)
    and semantic scoring (cosine similarity and rubric evaluation).
    """

    @staticmethod
    def tokenize(text: str) -> List[str]:
        return re.findall(r"\b\w+\b", text.lower())

    @classmethod
    def exact_match(cls, prediction: str, ground_truth: str) -> float:
        return 1.0 if prediction.strip().lower() == ground_truth.strip().lower() else 0.0

    @classmethod
    def calculate_bleu(cls, prediction: str, reference: str, n: int = 1) -> float:
        pred_tokens = cls.tokenize(prediction)
        ref_tokens = cls.tokenize(reference)
        
        if not pred_tokens or not ref_tokens:
            return 0.0

        pred_ngrams = [tuple(pred_tokens[i:i+n]) for i in range(len(pred_tokens)-n+1)]
        ref_ngrams = [tuple(ref_tokens[i:i+n]) for i in range(len(ref_tokens)-n+1)]

        if not pred_ngrams or not ref_ngrams:
            return 0.0

        pred_counts = Counter(pred_ngrams)
        ref_counts = Counter(ref_ngrams)

        clipped_matches = sum(min(count, ref_counts[ng]) for ng, count in pred_counts.items())
        precision = clipped_matches / len(pred_ngrams)

        # Brevity penalty
        bp = 1.0
        if len(pred_tokens) < len(ref_tokens):
            bp = math.exp(1 - (len(ref_tokens) / len(pred_tokens)))

        return round(bp * precision, 4)

    @classmethod
    def calculate_rouge_l(cls, prediction: str, reference: str) -> float:
        pred_tokens = cls.tokenize(prediction)
        ref_tokens = cls.tokenize(reference)
        m, n = len(pred_tokens), len(ref_tokens)
        
        if m == 0 or n == 0:
            return 0.0

        # Longest Common Subsequence (LCS) matrix
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if pred_tokens[i-1] == ref_tokens[j-1]:
                    dp[i][j] = dp[i-1][j-1] + 1
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])

        lcs_len = dp[m][n]
        prec = lcs_len / m
        rec = lcs_len / n
        if prec + rec == 0:
            return 0.0
        f1 = (2 * prec * rec) / (prec + rec)
        return round(f1, 4)

    @classmethod
    def cosine_similarity(cls, text_a: str, text_b: str) -> float:
        tokens_a = cls.tokenize(text_a)
        tokens_b = cls.tokenize(text_b)
        if not tokens_a or not tokens_b:
            return 0.0

        counts_a = Counter(tokens_a)
        counts_b = Counter(tokens_b)
        all_words = set(counts_a.keys()).union(set(counts_b.keys()))

        dot_product = sum(counts_a[w] * counts_b[w] for w in all_words)
        norm_a = math.sqrt(sum(c * c for c in counts_a.values()))
        norm_b = math.sqrt(sum(c * c for c in counts_b.values()))

        if norm_a == 0 or norm_b == 0:
            return 0.0
        return round(dot_product / (norm_a * norm_b), 4)

    @classmethod
    def evaluate_response(cls, prediction: str, ground_truth: str) -> Dict[str, float]:
        return {
            "exact_match": cls.exact_match(prediction, ground_truth),
            "bleu_1": cls.calculate_bleu(prediction, ground_truth, n=1),
            "rouge_l": cls.calculate_rouge_l(prediction, ground_truth),
            "cosine_similarity": cls.cosine_similarity(prediction, ground_truth)
        }
