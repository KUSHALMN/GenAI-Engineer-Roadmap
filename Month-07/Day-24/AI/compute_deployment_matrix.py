"""
GPU vs CPU Service Deployment Matrix: Total Cost of Ownership (TCO) Calculator,
Cold-Start Latency vs Reserved Instances, and Serverless vs Self-Hosted Math.
"""

from dataclasses import dataclass
from typing import Dict


@dataclass
class DeploymentOption:
    name: str
    setup_type: str # "serverless" vs "dedicated"
    monthly_fixed_cost_usd: float
    cost_per_million_tokens_usd: float
    p95_cold_start_seconds: float


class ComputeDeploymentMatrix:
    def compare_costs(self, monthly_tokens: int) -> Dict[str, float]:
        tokens_in_millions = monthly_tokens / 1_000_000
        # 1. Managed API (e.g. OpenAI/Anthropic)
        api_cost = tokens_in_millions * 0.40
        # 2. Serverless GPU (e.g. RunPod / Modal Serverless)
        serverless_cost = 50.0 + (tokens_in_millions * 0.25)
        # 3. Dedicated Reserved GPU (1x A10G on AWS)
        dedicated_cost = 730 * 1.212 # $884.76 fixed regardless of volume
        return {
            "managed_api_usd": round(api_cost, 2),
            "serverless_gpu_usd": round(serverless_cost, 2),
            "dedicated_gpu_usd": round(dedicated_cost, 2)
        }


if __name__ == "__main__":
    matrix = ComputeDeploymentMatrix()
    low_vol = matrix.compare_costs(monthly_tokens=2_000_000) # 2M tokens
    assert low_vol["managed_api_usd"] < low_vol["dedicated_gpu_usd"]

    high_vol = matrix.compare_costs(monthly_tokens=50_000_000) # 50M tokens
    print("=== Day 24: Compute Deployment Matrix ===")
    print(f"50M Tokens TCO Comparison: API=${high_vol['managed_api_usd']} | Dedicated=${high_vol['dedicated_gpu_usd']}")
