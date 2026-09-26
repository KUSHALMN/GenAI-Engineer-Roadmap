"""
Automated Evaluation Suite for Capstone Service.
Runs benchmark queries against the agent pipeline, measures latency,
verifies cache speedup, and audits security defenses.
"""

import json
import os
import time
from typing import Any, Dict
from agent_service import CapstoneAgentService
from schemas import AgentTaskType, CapstoneQueryRequest


def run_capstone_eval() -> Dict[str, Any]:
    service = CapstoneAgentService()
    dataset_file = os.path.join(os.path.dirname(__file__), "eval_dataset.jsonl")

    total_cases = 0
    passed_cases = 0
    latencies = []
    cached_latencies = []

    with open(dataset_file, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            case = json.loads(line)
            total_cases += 1

            req = CapstoneQueryRequest(
                query=case["query"],
                task_type=AgentTaskType(case.get("task_type", "general")),
            )

            # First call (cold / un-cached)
            resp = service.process_query(req)
            latencies.append(resp.latency_ms)

            # Verification logic
            if case.get("expected_action") == "blocked":
                if resp.status == "blocked":
                    passed_cases += 1
            else:
                expected_kw = case.get("expected_concept", "")
                if expected_kw.lower() in resp.answer.lower():
                    passed_cases += 1

            # Second call (warm / cached)
            resp_cached = service.process_query(req)
            cached_latencies.append(resp_cached.latency_ms)
            if not resp.status == "blocked":
                assert resp_cached.cached is True

    avg_cold_latency = sum(latencies) / len(latencies) if latencies else 0.0
    avg_cached_latency = sum(cached_latencies) / len(cached_latencies) if cached_latencies else 0.0
    speedup = avg_cold_latency / max(avg_cached_latency, 0.001)

    return {
        "total_test_cases": total_cases,
        "passed_cases": passed_cases,
        "pass_rate_pct": round((passed_cases / total_cases) * 100, 2),
        "avg_cold_latency_ms": round(avg_cold_latency, 2),
        "avg_cached_latency_ms": round(avg_cached_latency, 2),
        "cache_speedup_factor": round(speedup, 1),
    }


if __name__ == "__main__":
    results = run_capstone_eval()
    print("Capstone Benchmark Results:\n", json.dumps(results, indent=2))
    assert results["pass_rate_pct"] == 100.0
    print("Capstone automated evaluation completed successfully!")
