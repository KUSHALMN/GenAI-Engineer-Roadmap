"""
Day 14: Preference Optimization & DPO Foundations
Implements Direct Preference Optimization (DPO) loss calculation
given chosen vs rejected response log-probabilities and reference model log-probabilities:
L_DPO = -E[log(sigmoid(beta * (log(pi(y_w)/pi_ref(y_w)) - log(pi(y_l)/pi_ref(y_l)))))]
"""

import math
from typing import Dict, Any

class DPOSimulator:
    def __init__(self, beta: float = 0.1):
        self.beta = beta

    def sigmoid(self, x: float) -> float:
        return 1.0 / (1.0 + math.exp(-x))

    def compute_dpo_loss(self,
                         pi_chosen_logp: float,
                         ref_chosen_logp: float,
                         pi_rejected_logp: float,
                         ref_rejected_logp: float) -> Dict[str, float]:
        # Log ratios
        chosen_ratio = pi_chosen_logp - ref_chosen_logp
        rejected_ratio = pi_rejected_logp - ref_rejected_logp

        # Implicit reward margin
        reward_margin = self.beta * (chosen_ratio - rejected_ratio)
        prob = self.sigmoid(reward_margin)
        loss = -math.log(max(1e-12, prob))

        return {
            "dpo_loss": round(loss, 4),
            "chosen_reward_delta": round(chosen_ratio, 4),
            "rejected_reward_delta": round(rejected_ratio, 4),
            "implicit_reward_margin": round(reward_margin, 4)
        }

if __name__ == "__main__":
    dpo = DPOSimulator(beta=0.1)

    # Well-aligned model: policy assigns higher prob to chosen than ref, lower to rejected
    res = dpo.compute_dpo_loss(
        pi_chosen_logp=-1.2,
        ref_chosen_logp=-2.5,
        pi_rejected_logp=-4.0,
        ref_rejected_logp=-2.0
    )
    assert res["implicit_reward_margin"] > 0
    assert res["dpo_loss"] < 0.5
    print("DPO Loss Metrics:")
    for k, v in res.items():
        print(f"  {k}: {v}")
    print("Day 14 AI DPO Simulator passed all tests.")
