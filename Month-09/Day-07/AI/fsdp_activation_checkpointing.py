"""
PyTorch FSDP (Fully Sharded Data Parallel) & Activation Checkpointing:
Layer-by-Layer Forward All-Gather, Immediate Weight Release,
Backward Re-unshard, and Activation Recomputation Trade-off Simulation.
"""

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class TransformerLayerProfile:
    layer_id: int
    param_size_mb: float
    activation_size_mb: float


class FSDPCheckpointingSimulator:
    """
    Models memory dynamics of FSDP with and without Activation Checkpointing (Gradient Checkpointing).
    Trades 33% extra forward compute for a dramatic 70%+ reduction in peak activation memory.
    """
    def __init__(self, layers: List[TransformerLayerProfile], num_gpus: int):
        self.layers = layers
        self.num_gpus = num_gpus

    def simulate_standard_fsdp(self) -> Dict[str, float]:
        # In standard FSDP:
        # Sharded param storage = total_params / num_gpus
        # Peak active memory during layer compute = (total_params / num_gpus) + layer_param_size (unsharded)
        # All layer activations are stored in memory for backward pass
        total_param_mb = sum(l.param_size_mb for l in self.layers)
        sharded_param_mb = total_param_mb / self.num_gpus
        max_layer_param_mb = max(l.param_size_mb for l in self.layers)
        total_activation_mb = sum(l.activation_size_mb for l in self.layers)

        peak_vram_mb = sharded_param_mb + max_layer_param_mb + total_activation_mb
        return {
            "sharded_params_mb": sharded_param_mb,
            "peak_vram_mb": peak_vram_mb,
            "total_activations_stored_mb": total_activation_mb,
            "compute_recomputation_overhead": 0.0
        }

    def simulate_fsdp_with_activation_checkpointing(self) -> Dict[str, float]:
        # With Activation Checkpointing:
        # Only layer input activations are retained; intermediate activations are dropped and recomputed
        total_param_mb = sum(l.param_size_mb for l in self.layers)
        sharded_param_mb = total_param_mb / self.num_gpus
        max_layer_param_mb = max(l.param_size_mb for l in self.layers)

        # Retain only input boundary activations (~10% of full activation state)
        boundary_activations_mb = sum(l.activation_size_mb * 0.10 for l in self.layers)
        max_single_layer_activation_mb = max(l.activation_size_mb for l in self.layers)

        peak_vram_mb = sharded_param_mb + max_layer_param_mb + boundary_activations_mb + max_single_layer_activation_mb
        return {
            "sharded_params_mb": sharded_param_mb,
            "peak_vram_mb": peak_vram_mb,
            "total_activations_stored_mb": boundary_activations_mb + max_single_layer_activation_mb,
            "compute_recomputation_overhead": 0.33 # Exactly 1 extra forward pass per layer during backward
        }


if __name__ == "__main__":
    # Simulate a 32-layer LLM where each layer has 500MB params and 400MB activations
    layers = [TransformerLayerProfile(i, 500.0, 400.0) for i in range(32)]
    sim = FSDPCheckpointingSimulator(layers, num_gpus=8)

    standard = sim.simulate_standard_fsdp()
    checkpointed = sim.simulate_fsdp_with_activation_checkpointing()

    print("Standard FSDP Peak Memory:", standard["peak_vram_mb"], "MB")
    print("FSDP + Checkpointing Peak Memory:", checkpointed["peak_vram_mb"], "MB")
    print(f"Memory Reduction: {(1 - checkpointed['peak_vram_mb'] / standard['peak_vram_mb']):.1%}")

    assert checkpointed["peak_vram_mb"] < standard["peak_vram_mb"] * 0.40 # > 60% memory reduction!
    print("Day 07 FSDP & Activation Checkpointing verification passed.")
