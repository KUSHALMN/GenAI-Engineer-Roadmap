"""
Day 08: LoRA Mechanics (Low-Rank Adaptation)
Implements forward pass and weight merging for Low-Rank Adaptation:
h = W_0 * x + (alpha / r) * (B * A) * x
"""

import numpy as np

class LoRALinear:
    def __init__(self, in_features: int, out_features: int, rank: int = 4, alpha: float = 8.0):
        self.in_features = in_features
        self.out_features = out_features
        self.rank = rank
        self.scaling = alpha / rank

        # Frozen base weights W_0
        self.W0 = np.random.randn(out_features, in_features) * 0.01

        # LoRA Low-rank matrices: A ~ N(0, sigma), B = 0 (so Delta W starts at 0)
        self.A = np.random.randn(rank, in_features) * (1.0 / np.sqrt(in_features))
        self.B = np.zeros((out_features, rank))

    def forward(self, x: np.ndarray) -> np.ndarray:
        # Standard base pass
        base_out = np.dot(x, self.W0.T)
        # Low rank adaptation pass
        lora_out = np.dot(np.dot(x, self.A.T), self.B.T) * self.scaling
        return base_out + lora_out

    def merge_weights(self) -> np.ndarray:
        """Merges LoRA delta into base matrix for zero-overhead inference."""
        delta_w = np.dot(self.B, self.A) * self.scaling
        return self.W0 + delta_w

if __name__ == "__main__":
    np.random.seed(42)
    layer = LoRALinear(in_features=64, out_features=128, rank=4, alpha=8.0)
    x = np.random.randn(2, 64)

    # Initial forward pass (since B=0, lora delta is 0)
    out1 = layer.forward(x)
    assert np.allclose(out1, np.dot(x, layer.W0.T))

    # Simulate gradient update on B
    layer.B += np.random.randn(128, 4) * 0.05
    out2 = layer.forward(x)
    assert not np.allclose(out1, out2)

    # Merged weight inference parity check
    W_merged = layer.merge_weights()
    merged_out = np.dot(x, W_merged.T)
    assert np.allclose(out2, merged_out, atol=1e-6)

    print("LoRA forward pass and weight merging parity validated successfully.")
    print("Day 08 AI LoRA Simulator passed all tests.")
