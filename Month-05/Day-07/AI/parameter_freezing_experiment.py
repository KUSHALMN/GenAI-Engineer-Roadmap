"""
Day 07: Transformer Adaptation Concepts
Analyzes parameter counts across transformer blocks, simulating full fine-tuning
vs selective layer freezing vs parameter-efficient adapter injection.
"""

from typing import Dict, Any, List

class TransformerParamAuditor:
    def __init__(self, hidden_dim: int = 4096, num_layers: int = 32, vocab_size: int = 32000):
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        self.vocab_size = vocab_size

    def calculate_parameter_counts(self, lora_rank: int = 16) -> Dict[str, Any]:
        # Embeddings: vocab_size * hidden_dim
        embed_params = self.vocab_size * self.hidden_dim

        # Per layer: Q, K, V, O projections (4 * d^2) + MLP (gate, up, down: ~3 * 8/3 * d^2)
        attn_weights = 4 * (self.hidden_dim ** 2)
        mlp_weights = int(3 * (8 / 3) * (self.hidden_dim ** 2))
        layer_params = attn_weights + mlp_weights

        total_base_params = embed_params + (layer_params * self.num_layers)

        # LoRA on Q and V projections: 2 * (d * r + r * d) per layer
        lora_params_per_layer = 2 * (2 * self.hidden_dim * lora_rank)
        total_lora_trainable = lora_params_per_layer * self.num_layers

        return {
            "total_base_parameters": total_base_params,
            "total_base_params_billions": round(total_base_params / 1e9, 2),
            "lora_trainable_parameters": total_lora_trainable,
            "trainable_percentage": round((total_lora_trainable / total_base_params) * 100, 3)
        }

if __name__ == "__main__":
    auditor = TransformerParamAuditor(hidden_dim=4096, num_layers=32)
    stats = auditor.calculate_parameter_counts(lora_rank=16)

    assert stats["trainable_percentage"] < 1.0 # Less than 1% of weights trained!
    print("Transformer Adaptation Parameter Audit:")
    for k, v in stats.items():
        print(f"  {k}: {v}")
    print("Day 07 AI Parameter Freezing Experiment passed all tests.")
