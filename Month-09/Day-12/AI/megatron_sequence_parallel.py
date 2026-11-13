"""
Sequence Parallelism (Megatron-SP & DeepSpeed-SP):
Sharding Activations along the Sequence Dimension (s / tp),
All-Gather Forward / Reduce-Scatter Backward across Dropout & LayerNorm.
"""

from typing import Dict, List


class SequenceParallelismSimulator:
    """
    Simulates Megatron-LM Sequence Parallelism.
    In standard TP, LayerNorm and Dropout are replicated across all TP ranks.
    Sequence Parallelism shards activations along the sequence length (s / tp)
    across LayerNorm and Dropout, eliminating activation redundancy.
    """
    def __init__(self, seq_len: int, hidden_dim: int, tp_size: int):
        self.seq_len = seq_len
        self.hidden_dim = hidden_dim
        self.tp_size = tp_size
        assert seq_len % tp_size == 0, "Sequence length must be divisible by TP size"
        self.sub_seq_len = seq_len // tp_size

    def calculate_activation_memory_savings(self) -> Dict[str, float]:
        """
        Calculates memory consumption for LayerNorm, Dropout, and Attention activations.
        """
        # Memory in bytes (FP16 = 2 bytes)
        bytes_per_elem = 2
        
        # Standard TP: Sequence length is replicated for LayerNorm and Dropout
        replicated_ln_dropout = 2 * (self.seq_len * self.hidden_dim) * bytes_per_elem
        
        # Sequence Parallel: Sharded along sequence dimension across TP ranks
        sharded_ln_dropout = 2 * (self.sub_seq_len * self.hidden_dim) * bytes_per_elem
        
        savings_bytes = replicated_ln_dropout - sharded_ln_dropout
        return {
            "standard_tp_ln_bytes_per_gpu": replicated_ln_dropout,
            "sequence_parallel_ln_bytes_per_gpu": sharded_ln_dropout,
            "savings_percentage": round((1.0 - sharded_ln_dropout / replicated_ln_dropout) * 100.0, 2)
        }

    def simulate_forward_backward_flow(self) -> List[str]:
        # Sequence parallel execution sequence per Transformer layer
        return [
            f"1. Input activation enters LayerNorm sharded: shape [s/{self.tp_size}, b, h]",
            "2. Sharded LayerNorm computed locally with zero communication",
            "3. All-Gather transforms sharded activations [s/tp, b, h] -> full [s, b, h]",
            "4. ColumnParallelLinear projects Q, K, V",
            "5. Local Attention computed on full sequence",
            "6. RowParallelLinear projects output",
            "7. Reduce-Scatter transforms full output [s, b, h] -> sharded [s/tp, b, h]",
            "8. Sharded Dropout and Residual Addition executed with zero communication"
        ]


if __name__ == "__main__":
    # Test SP for sequence length 8192, hidden dimension 4096, TP=8
    sp_sim = SequenceParallelismSimulator(seq_len=8192, hidden_dim=4096, tp_size=8)
    mem_stats = sp_sim.calculate_activation_memory_savings()
    flow = sp_sim.simulate_forward_backward_flow()

    print("Sequence Parallelism Memory Metrics (TP=8):")
    for k, v in mem_stats.items():
        print(f" -> {k}: {v}")

    print("Execution Flow:")
    for step in flow:
        print(" ", step)

    assert mem_stats["savings_percentage"] == 87.5 # (1 - 1/8) = 87.5% reduction in LayerNorm memory!
    print("Day 12 Megatron Sequence Parallel verification passed.")
