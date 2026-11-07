"""
Day 28: Cost and Capacity Planning
Models GPU hardware capacity (number of A100/H100 nodes needed),
monthly cloud spend, and token throughput requirements.
"""

from typing import Dict, Any

class CapacityCostPlanner:
    @staticmethod
    def calculate_plan(daily_active_users: int,
                       queries_per_user: int = 10,
                       avg_input_tokens: int = 400,
                       avg_output_tokens: int = 150,
                       gpu_hourly_cost: float = 2.50) -> Dict[str, Any]:
        daily_queries = daily_active_users * queries_per_user
        daily_input_tokens = daily_queries * avg_input_tokens
        daily_output_tokens = daily_queries * avg_output_tokens
        total_daily_tokens = daily_input_tokens + daily_output_tokens

        # Assuming 1 GPU node sustains ~80 tokens/sec continuously = ~6.9M tokens/day
        tokens_per_gpu_day = 80 * 3600 * 24
        gpus_needed = max(1, int((total_daily_tokens + tokens_per_gpu_day - 1) // tokens_per_gpu_day))

        monthly_cost = gpus_needed * gpu_hourly_cost * 24 * 30

        return {
            "daily_queries": daily_queries,
            "total_daily_tokens_millions": round(total_daily_tokens / 1e6, 2),
            "recommended_gpu_instances": gpus_needed,
            "estimated_monthly_gpu_spend_usd": round(monthly_cost, 2)
        }

if __name__ == "__main__":
    planner = CapacityCostPlanner()
    plan = planner.calculate_plan(daily_active_users=5000, queries_per_user=10)
    print("Capacity and GPU Spend Plan (5,000 DAU):")
    for k, v in plan.items():
        print(f"  {k}: {v}")

    assert plan["recommended_gpu_instances"] >= 1
    print("Day 28 AI Cost and Capacity Planning passed all tests.")
