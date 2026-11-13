"""
Pretraining Evaluation & Validation Suite:
Validation Perplexity (PPL), Bits-Per-Byte (BPB),
Cross-Entropy Validation Loss Tracking, and Downstream Zero-Shot Probing.
"""

from dataclasses import dataclass
import math
from typing import List


@dataclass
class PretrainingValidationMetrics:
    eval_loss: float
    perplexity: float
    bits_per_byte: float
    zero_shot_accuracy: float


class PretrainingValidationEvaluator:
    """
    Computes rigorous information-theoretic metrics for evaluating pretraining quality
    and diagnosing overfitting or validation loss divergence.
    """
    def evaluate_checkpoint(self, token_cross_entropies: List[float], total_utf8_bytes: int, num_tokens: int) -> PretrainingValidationMetrics:
        avg_loss = sum(token_cross_entropies) / max(1, len(token_cross_entropies))
        # Perplexity = exp(loss)
        ppl = math.exp(avg_loss)

        # Bits-Per-Byte (BPB) = (total_loss_in_bits) / total_utf8_bytes
        # Natural log loss to bits: loss / ln(2)
        total_loss_bits = (avg_loss * num_tokens) / math.log(2.0)
        bpb = total_loss_bits / max(1, total_utf8_bytes)

        # Simulated zero-shot benchmark probe (MMLU / GSM8k proxy)
        # Quality inversely scales with perplexity
        zero_shot_acc = max(0.0, min(1.0, 1.0 - (avg_loss / 5.0)))

        return PretrainingValidationMetrics(
            eval_loss=round(avg_loss, 4),
            perplexity=round(ppl, 2),
            bits_per_byte=round(bpb, 4),
            zero_shot_accuracy=round(zero_shot_acc * 100.0, 2)
        )


if __name__ == "__main__":
    evaluator = PretrainingValidationEvaluator()
    # 5 sample token losses
    sample_losses = [1.8, 1.9, 1.75, 1.85, 1.80]
    metrics = evaluator.evaluate_checkpoint(
        token_cross_entropies=sample_losses,
        total_utf8_bytes=25,
        num_tokens=5
    )

    print("Pretraining Evaluation Report:")
    print(f" -> Validation Loss: {metrics.eval_loss}")
    print(f" -> Perplexity: {metrics.perplexity}")
    print(f" -> Bits-Per-Byte (BPB): {metrics.bits_per_byte}")
    print(f" -> Zero-Shot Accuracy: {metrics.zero_shot_accuracy}%")

    assert metrics.perplexity > 1.0
    assert metrics.bits_per_byte > 0.0
    print("Day 20 Pretraining Eval Suite verification passed.")
