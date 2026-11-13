"""
Automated Integration Test Suite for Month-09 Days 11-20:
Validates MoE Routing, Sequence Parallelism, RingAttention, Mixed Precision,
Async Distributed Checkpointing, Collective Communication, Pretraining Loops,
Elastic Fault Tolerance, Hardware MFU Profiling, and Pretraining Evaluation.
"""

import os
import sys
import unittest

current_dir = os.path.dirname(os.path.abspath(__file__))
month_dir = os.path.abspath(os.path.join(current_dir, ".."))

# Add all Day-XX/AI directories to sys.path
for day in range(11, 21):
    day_ai_path = os.path.abspath(os.path.join(month_dir, f"Day-{day:02d}", "AI"))
    sys.path.insert(0, day_ai_path)

from moe_expert_router import MoETop2GatingRouter
from megatron_sequence_parallel import SequenceParallelismSimulator
from ring_attention_simulator import RingAttentionSimulator
from mixed_precision_numerical_stability import DynamicLossScaler
from distributed_async_checkpointing import DistributedCheckpointManager
from collective_communication_topology import CollectiveCommunicationModeler, InterconnectLink
from megatron_pretraining_engine import CosineWarmupLRScheduler, DistributedPretrainingEngine
from elastic_fault_tolerance_engine import ElasticTrainingFaultManager
from hardware_profiling_mfu_analyzer import PretrainingMFUAnalyzer, GPUHardwareProfile
from pretraining_eval_suite import PretrainingValidationEvaluator


class TestDistributedPretrainingDays11to20(unittest.TestCase):

    def test_day11_moe_gating(self):
        router = MoETop2GatingRouter(num_experts=4, capacity_factor=1.5)
        tokens = [[1.0, 0.5, -0.2, 0.4], [-0.5, 1.0, 0.3, -0.8]]
        decisions, aux_loss = router.route_tokens(tokens)
        self.assertEqual(len(decisions), 2)
        self.assertGreater(aux_loss, 0.0)

    def test_day12_sequence_parallel(self):
        sim = SequenceParallelismSimulator(seq_len=4096, hidden_dim=2048, tp_size=4)
        stats = sim.calculate_activation_memory_savings()
        self.assertEqual(stats["savings_percentage"], 75.0)

    def test_day13_ring_attention(self):
        sim = RingAttentionSimulator(num_ranks=2)
        q = [[[1.0, 0.0]], [[0.0, 1.0]]]
        k = [[[1.0, 0.0]], [[0.0, 1.0]]]
        v = [[[2.0, 1.0]], [[1.0, 2.0]]]
        out = sim.compute_ring_attention(q, k, v)
        self.assertEqual(len(out), 2)
        self.assertGreater(out[0][0][0], 0.0)

    def test_day14_mixed_precision_stability(self):
        scaler = DynamicLossScaler(initial_scale=1024.0, scale_factor=2.0, scale_window=2)
        unscaled, ok = scaler.step([512.0, 1024.0])
        self.assertTrue(ok)
        self.assertEqual(unscaled, [0.5, 1.0])

    def test_day15_distributed_async_checkpointing(self):
        import tempfile
        tmp = tempfile.mkdtemp()
        mgr = DistributedCheckpointManager(tmp, rank=0, world_size=1)
        meta = mgr.save_sharded_state(1, {"w": [1.0, 2.0]})
        self.assertTrue(os.path.exists(meta))

    def test_day16_collective_communication(self):
        link = InterconnectLink("TestNVLink", bandwidth_gb_s=900.0, latency_us=1.0)
        modeler = CollectiveCommunicationModeler(world_size=8, link=link)
        t_ar = modeler.all_reduce_time(500.0)
        self.assertGreater(t_ar, 0.0)

    def test_day17_megatron_pretraining_engine(self):
        scheduler = CosineWarmupLRScheduler(max_lr=1e-3, min_lr=1e-4, warmup_steps=10, total_steps=100)
        engine = DistributedPretrainingEngine(max_grad_norm=1.0, weight_decay=0.01)
        lr = scheduler.get_lr(10)
        self.assertAlmostEqual(lr, 1e-3)
        clipped, norm = engine.clip_grad_norm([3.0, 4.0])
        self.assertAlmostEqual(norm, 5.0)

    def test_day18_elastic_fault_tolerance(self):
        mgr = ElasticTrainingFaultManager(heartbeat_timeout_sec=1.0)
        mgr.register_heartbeat(0, 100.0)
        status = mgr.evaluate_cluster_health()
        self.assertTrue(status["cluster_healthy"])

    def test_day19_hardware_mfu(self):
        gpu = GPUHardwareProfile("H100", peak_tflops_fp16=989.0, memory_bandwidth_tb_s=3.35)
        analyzer = PretrainingMFUAnalyzer(8.0, 4096, 32, 4096, gpu)
        metrics = analyzer.analyze_step_performance(tokens_per_step=32768, step_time_sec=0.16, num_gpus=8)
        self.assertGreater(metrics["mfu_percentage"], 30.0)

    def test_day20_pretraining_evaluation(self):
        evaluator = PretrainingValidationEvaluator()
        metrics = evaluator.evaluate_checkpoint([1.5, 1.7], total_utf8_bytes=10, num_tokens=2)
        self.assertGreater(metrics.perplexity, 1.0)


if __name__ == "__main__":
    unittest.main()
