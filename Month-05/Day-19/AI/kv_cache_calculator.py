"""
Day 19: KV Cache and Memory Math
Calculates Key-Value cache memory requirements across context length,
batch size, layers, and KV heads (Multi-Head vs Grouped-Query Attention).
KV_bytes_per_token = 2 (K & V) * 2 (bytes in FP16) * num_layers * num_kv_heads * head_dim
"""

from typing import Dict, Any

class KVCacheCalculator:
    @staticmethod
    def calculate_kv_memory(num_layers: int,
                            num_kv_heads: int,
                            head_dim: int,
                            batch_size: int,
                            seq_len: int,
                            precision_bytes: int = 2) -> Dict[str, Any]:
        # Bytes per single token across all layers
        bytes_per_token = 2 * precision_bytes * num_layers * num_kv_heads * head_dim

        total_bytes = bytes_per_token * batch_size * seq_len
        total_mb = total_bytes / (1024 * 1024)
        total_gb = total_bytes / (1024 * 1024 * 1024)

        return {
            "bytes_per_token": bytes_per_token,
            "total_kv_cache_mb": round(total_mb, 2),
            "total_kv_cache_gb": round(total_gb, 2),
            "batch_size": batch_size,
            "seq_len": seq_len
        }

if __name__ == "__main__":
    calc = KVCacheCalculator()
    # Llama-3-8B configuration: 32 layers, 8 KV heads (GQA), head_dim 128
    res = calc.calculate_kv_memory(num_layers=32, num_kv_heads=8, head_dim=128, batch_size=16, seq_len=4096)
    print("KV Cache Calculation (Llama-3-8B GQA, Batch 16, 4k Context):")
    for k, v in res.items():
        print(f"  {k}: {v}")

    assert res["total_kv_cache_gb"] > 0
    print("Day 19 AI KV Cache Calculator passed all tests.")
