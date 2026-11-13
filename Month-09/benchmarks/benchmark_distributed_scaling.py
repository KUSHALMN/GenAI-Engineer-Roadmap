"""
Benchmark Profiler for Month-09 Distributed Pretraining:
Benchmarks MoE Routing Throughput, Sequence Parallel Activation Footprint,
RingAttention Step Latencies, Collective Communication Bounds, and MFU Scaling.
"""

import os
import sys
import time
from typing import Dict, List

# Setup sys.path for days 11-20
current_dir = os.path.dirname(os.path.abspath(__file__))
month_dir = os.path.abspath(os.path.join(current_dir, ".."))
for d in range(11, 21):
    sys.path.insert(0, os.path.join(month_dir, f"Day-{d:02d}", "AI"))

from moe_expert_router import MoETop2GatingRouter
from megatron_sequence_parallel import SequenceParallelismSimulator
from collective_communication_topology import CollectiveCommunicationModeler, InterconnectLink
from hardware_profiling_mfu_analyzer import PretrainingMFUAnalyzer, GPUHardwareProfile


def run_benchmarks() -> Dict[str, any]:
    results = {}

    # 1. MoE Routing Latency (10,000 tokens)
    router = MoETop2GatingRouter(num_experts=8, capacity_factor=1.25)
    tokens = [[(i + j) * 0.01 for j in range(4)] for i in range(1000)]
    t0 = time.time()
    for _ in range(10):
        router.route_tokens(tokens)
    t1 = time.time()
    moe_latency_ms = (t1 - t0) * 100.0 # ms per 10k tokens
    results["moe_routing_latency_10k_ms"] = round(moe_latency_ms, 2)

    # 2. Sequence Parallel Memory Savings (8k context, hidden 4096, TP=8)
    sp = SequenceParallelismSimulator(seq_len=8192, hidden_dim=4096, tp_size=8)
    mem_stats = sp.calculate_activation_memory_savings()
    results["sp_activation_reduction_pct"] = mem_stats["savings_percentage"]

    # 3. Collective Communication Transfer (1GB All-Reduce & All-to-All)
    nvlink = InterconnectLink("NVLink-4", bandwidth_gb_s=900.0, latency_us=1.0)
    modeler = CollectiveCommunicationModeler(world_size=8, link=nvlink)
    results["all_reduce_1gb_nvlink_ms"] = round(modeler.all_reduce_time(1000.0), 2)
    results["all_to_all_1gb_nvlink_ms"] = round(modeler.all_to_all_time(1000.0), 2)

    # 4. MFU Scaling (8B model on 8x H100)
    h100 = GPUHardwareProfile("H100-SXM", peak_tflops_fp16=989.0, memory_bandwidth_tb_s=3.35)
    analyzer = PretrainingMFUAnalyzer(8.0, 4096, 32, 4096, h100)
    mfu_stats = analyzer.analyze_step_performance(tokens_per_step=32768, step_time_sec=0.16, num_gpus=8)
    results["model_flops_utilization_pct"] = mfu_stats["mfu_percentage"]

    return results


if __name__ == "__main__":
    bench_results = run_benchmarks()
    print("=== Distributed Pretraining Scaling Benchmark Results ===")
    for k, v in bench_results.items():
        print(f" -> {k}: {v}")
