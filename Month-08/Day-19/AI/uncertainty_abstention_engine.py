"""
Uncertainty Estimation and Selective Abstention: Output Entropy, Token Probability Dispersion,
Self-Consistency Consensus, and Confident Refusal Logic.
"""

from dataclasses import dataclass
import math
from typing import List, Tuple


@dataclass
class TokenLogprob:
    token: str
    logprob: float


@dataclass
class GenerationSample:
    text: str
    token_logprobs: List[TokenLogprob]


class UncertaintyAbstentionEngine:
    """
    Computes semantic entropy and token perplexity to selectively abstain or request
    clarification on high-uncertainty outputs.
    """
    def __init__(self, entropy_threshold: float = 1.25, avg_logprob_threshold: float = -0.65):
        self.entropy_threshold = entropy_threshold
        self.avg_logprob_threshold = avg_logprob_threshold

    def calculate_sequence_metrics(self, token_logprobs: List[TokenLogprob]) -> Tuple[float, float]:
        if not token_logprobs:
            return 0.0, 0.0
        
        total_logprob = sum(t.logprob for t in token_logprobs)
        avg_logprob = total_logprob / len(token_logprobs)
        perplexity = math.exp(-avg_logprob)
        return avg_logprob, perplexity

    def calculate_self_consistency_entropy(self, candidate_responses: List[str]) -> float:
        """
        Computes Shannon entropy across clustered candidate responses.
        """
        if not candidate_responses:
            return 0.0
        total = len(candidate_responses)
        counts: dict = {}
        for r in candidate_responses:
            counts[r] = counts.get(r, 0) + 1
        
        entropy = 0.0
        for count in counts.values():
            p = count / total
            entropy -= p * math.log(p)
        return entropy

    def should_abstain(self, candidate_responses: List[str], token_logprobs: List[TokenLogprob]) -> Tuple[bool, str]:
        entropy = self.calculate_self_consistency_entropy(candidate_responses)
        avg_logprob, perplexity = self.calculate_sequence_metrics(token_logprobs)

        if entropy > self.entropy_threshold:
            return True, f"Abstain: High response disagreement (Entropy {entropy:.2f} > {self.entropy_threshold})"
        
        if avg_logprob < self.avg_logprob_threshold:
            return True, f"Abstain: Low token confidence (Avg Logprob {avg_logprob:.2f} < {self.avg_logprob_threshold})"

        return False, f"Proceed: Confident generation (Entropy: {entropy:.2f}, Avg Logprob: {avg_logprob:.2f})"


if __name__ == "__main__":
    engine = UncertaintyAbstentionEngine(entropy_threshold=1.0, avg_logprob_threshold=-0.5)

    # Confident scenario: All 5 sampled responses agree
    confident_samples = ["The capital of France is Paris."] * 5
    confident_logprobs = [TokenLogprob("Paris", -0.05), TokenLogprob(".", -0.02)]
    abstain_1, reason_1 = engine.should_abstain(confident_samples, confident_logprobs)
    assert not abstain_1
    print("Test 1 Result:", reason_1)

    # Uncertain scenario: Divergent responses
    uncertain_samples = ["1992", "1994", "1991", "1995", "1993"]
    abstain_2, reason_2 = engine.should_abstain(uncertain_samples, confident_logprobs)
    assert abstain_2
    print("Test 2 Result:", reason_2)

    print("Day 19 Uncertainty & Abstention Engine verification passed.")
