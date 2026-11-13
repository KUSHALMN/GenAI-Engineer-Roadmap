"""
Precision Formats & Numerical Stability in LLM Pretraining:
FP32, FP16, BF16, FP8 (E4M3 vs E5M2) Bit Layouts, Dynamic Loss Scaling,
Underflow / Overflow Detection, and Gradient Norm Clipping.
"""

from dataclasses import dataclass
import math
from typing import List, Tuple


@dataclass
class FloatingPointFormat:
    name: str
    sign_bits: int
    exponent_bits: int
    mantissa_bits: int

    @property
    def max_exponent(self) -> int:
        return (1 << (self.exponent_bits - 1)) - 1

    @property
    def dynamic_range_max(self) -> float:
        # Approximate largest finite representable value
        return (2.0 - 2.0 ** (-self.mantissa_bits)) * (2.0 ** self.max_exponent)

    @property
    def smallest_positive_normal(self) -> float:
        return 2.0 ** (-(self.max_exponent - 1))


class DynamicLossScaler:
    """
    Simulates FP16 / FP8 Dynamic Loss Scaling to prevent underflow of small gradients.
    Automatically doubles scale factor on consecutive successful steps,
    and halves scale factor upon encountering NaN / Inf gradients.
    """
    def __init__(self, initial_scale: float = 65536.0, scale_factor: float = 2.0, scale_window: int = 100):
        self.loss_scale = initial_scale
        self.scale_factor = scale_factor
        self.scale_window = scale_window
        self.consecutive_successful_steps = 0

    def step(self, raw_gradients: List[float]) -> Tuple[List[float], bool]:
        # Check for NaN or Inf in scaled gradients
        has_nan_inf = any(math.isnan(g) or math.isinf(g) for g in raw_gradients)

        if has_nan_inf:
            self.loss_scale = max(1.0, self.loss_scale / self.scale_factor)
            self.consecutive_successful_steps = 0
            return [0.0] * len(raw_gradients), False # Skip optimizer step

        # Unscale gradients: g_unscaled = g / loss_scale
        unscaled = [g / self.loss_scale for g in raw_gradients]
        self.consecutive_successful_steps += 1

        if self.consecutive_successful_steps >= self.scale_window:
            self.loss_scale *= self.scale_factor
            self.consecutive_successful_steps = 0

        return unscaled, True


if __name__ == "__main__":
    formats = [
        FloatingPointFormat("FP32", 1, 8, 23),
        FloatingPointFormat("FP16", 1, 5, 10),
        FloatingPointFormat("BF16", 1, 8, 7),
        FloatingPointFormat("FP8-E4M3", 1, 4, 3),
        FloatingPointFormat("FP8-E5M2", 1, 5, 2)
    ]

    print("Floating Point Format Numerical Envelopes:")
    for fmt in formats:
        print(f" -> {fmt.name}: Exp={fmt.exponent_bits}b, Mantissa={fmt.mantissa_bits}b | Max: ~{fmt.dynamic_range_max:.2e} | Min Normal: ~{fmt.smallest_positive_normal:.2e}")

    scaler = DynamicLossScaler(initial_scale=1024.0, scale_factor=2.0, scale_window=2)
    # Step 1: Valid gradients
    unscaled1, ok1 = scaler.step([512.0, 1024.0])
    assert ok1 is True
    assert unscaled1 == [0.5, 1.0]

    # Step 2: Valid gradients (triggers scale increase)
    unscaled2, ok2 = scaler.step([1024.0, 2048.0])
    assert ok2 is True
    assert scaler.loss_scale == 2048.0

    # Step 3: Gradient overflow (contains Inf)
    _, ok3 = scaler.step([100.0, float("inf")])
    assert ok3 is False
    assert scaler.loss_scale == 1024.0
    print("Day 14 Mixed Precision Numerical Stability verification passed.")
