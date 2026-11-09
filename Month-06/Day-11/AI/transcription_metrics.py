"""
Speech-to-Text Transcription Evaluation Engine.
Computes Word Error Rate (WER), Character Error Rate (CER),
Word Information Lost (WIL), and Term-Specific Accuracy (TSA) across accents & acoustic noise.
"""

from dataclasses import dataclass, field
import difflib
import re
from typing import Any, Dict, List, Optional, Set, Tuple


@dataclass
class TranscriptionEvaluationResult:
    reference: str
    hypothesis: str
    wer: float
    cer: float
    wil: float
    domain_term_accuracy: float
    substitutions: int
    deletions: int
    insertions: int
    matched_terms: List[str]
    missed_terms: List[str]


class TranscriptionEvaluator:
    def __init__(self, domain_terms: Optional[Set[str]] = None):
        self.domain_terms = {t.lower() for t in domain_terms} if domain_terms else set()

    @staticmethod
    def _normalize(text: str) -> List[str]:
        cleaned = re.sub(r"[^a-zA-Z0-9\s]", "", text.lower())
        return [w for w in cleaned.split() if w]

    def evaluate(self, reference: str, hypothesis: str) -> TranscriptionEvaluationResult:
        ref_words = self._normalize(reference)
        hyp_words = self._normalize(hypothesis)

        matcher = difflib.SequenceMatcher(None, ref_words, hyp_words)
        substitutions = sum(max(i2 - i1, j2 - j1) for tag, i1, i2, j1, j2 in matcher.get_opcodes() if tag == 'replace')
        deletions = sum((i2 - i1) for tag, i1, i2, j1, j2 in matcher.get_opcodes() if tag == 'delete')
        insertions = sum((j2 - j1) for tag, i1, i2, j1, j2 in matcher.get_opcodes() if tag == 'insert')

        total_ref = max(1, len(ref_words))
        wer = (substitutions + deletions + insertions) / total_ref

        ref_chars = list(re.sub(r"\s+", "", reference.lower()))
        hyp_chars = list(re.sub(r"\s+", "", hypothesis.lower()))
        char_matcher = difflib.SequenceMatcher(None, ref_chars, hyp_chars)
        char_dist = sum(
            max(i2 - i1, j2 - j1) if tag == 'replace' else (i2 - i1 if tag == 'delete' else (j2 - j1 if tag == 'insert' else 0))
            for tag, i1, i2, j1, j2 in char_matcher.get_opcodes()
        )
        cer = char_dist / max(1, len(ref_chars))

        hits = total_ref - substitutions - deletions
        total_hyp = max(1, len(hyp_words))
        wil = 1.0 - ((hits / total_ref) * (hits / total_hyp)) if (total_ref > 0 and total_hyp > 0) else 1.0

        matched_terms = [t for t in self.domain_terms if t in set(hyp_words) and t in ref_words]
        missed_terms = [t for t in self.domain_terms if t not in set(hyp_words) and t in ref_words]
        total_domain = len(matched_terms) + len(missed_terms)
        term_acc = (len(matched_terms) / total_domain) if total_domain > 0 else 1.0

        return TranscriptionEvaluationResult(
            reference, hypothesis, round(wer, 4), round(cer, 4), round(wil, 4),
            round(term_acc, 4), substitutions, deletions, insertions, matched_terms, missed_terms
        )


if __name__ == "__main__":
    evaluator = TranscriptionEvaluator(domain_terms={"pagedattention", "continuous", "vllm", "kvcache"})
    ref = "The model utilizes vLLM with PagedAttention and continuous batching for fast KVCache access."
    hyp = "The model utilizes VM with page attention and continuous matching for fast KV cache access."
    res = evaluator.evaluate(ref, hyp)
    print("=== Transcription Evaluation Benchmark ===")
    print(f"WER: {res.wer * 100:.2f}% | CER: {res.cer * 100:.2f}% | Term Acc: {res.domain_term_accuracy * 100:.2f}%")
