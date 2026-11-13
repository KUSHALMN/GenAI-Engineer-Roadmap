"""
Mixture-of-Experts (MoE) Architecture & Expert Parallelism:
Top-K Gating, Softmax Routing, Expert Capacity Factor, Dropped Token Handling,
and Load Balancing Auxiliary Loss.
"""

from dataclasses import dataclass
import math
from typing import List, Tuple


@dataclass
class RoutingDecision:
    token_idx: int
    selected_experts: List[int]
    expert_weights: List[float]
    is_dropped: bool = False


class MoETop2GatingRouter:
    """
    Simulates Top-2 Softmax Gating for Mixture-of-Experts with capacity limits
    and auxiliary load-balancing loss calculation.
    """
    def __init__(self, num_experts: int = 8, capacity_factor: float = 1.25):
        self.num_experts = num_experts
        self.capacity_factor = capacity_factor
        # Simulated gate linear projection weights (dim -> num_experts)
        # Using deterministic pseudo-weights for reproducible routing
        self.gate_weights = [
            [(i * 0.3 + j * 0.7) % 1.5 - 0.75 for j in range(num_experts)]
            for i in range(4)
        ]

    def _softmax(self, logits: List[float]) -> List[float]:
        max_l = max(logits)
        exps = [math.exp(x - max_l) for x in logits]
        sum_exp = sum(exps)
        return [e / sum_exp for e in exps]

    def route_tokens(self, token_embeddings: List[List[float]]) -> Tuple[List[RoutingDecision], float]:
        num_tokens = len(token_embeddings)
        # Capacity = ceil((num_tokens * K / num_experts) * capacity_factor)
        capacity = math.ceil((num_tokens * 2 / self.num_experts) * self.capacity_factor)
        expert_counts = [0] * self.num_experts
        expert_prob_sums = [0.0] * self.num_experts

        decisions = []

        for idx, emb in enumerate(token_embeddings):
            # Compute gate logits: emb @ gate_weights
            logits = [0.0] * self.num_experts
            for e_idx in range(self.num_experts):
                s = sum(emb[d] * self.gate_weights[d][e_idx] for d in range(len(emb)))
                logits[e_idx] = s

            probs = self._softmax(logits)
            for e_idx, p in enumerate(probs):
                expert_prob_sums[e_idx] += p

            # Select Top-2 experts
            indexed_probs = list(enumerate(probs))
            indexed_probs.sort(key=lambda x: x[1], reverse=True)
            top2 = indexed_probs[:2]

            selected_e = []
            selected_w = []
            top2_sum = top2[0][1] + top2[1][1]

            dropped = False
            for e, w in top2:
                if expert_counts[e] < capacity:
                    expert_counts[e] += 1
                    selected_e.append(e)
                    # Renormalize Top-2 weights
                    selected_w.append(w / top2_sum)
                else:
                    dropped = True

            decisions.append(RoutingDecision(
                token_idx=idx,
                selected_experts=selected_e,
                expert_weights=selected_w,
                is_dropped=dropped and len(selected_e) == 0
            ))

        # Switch Transformer Auxiliary Load Balancing Loss:
        # L_aux = num_experts * sum(f_i * P_i) where f_i is fraction of tokens dispatched to expert i,
        # and P_i is the mean routing probability allocated to expert i.
        total_dispatched = sum(expert_counts)
        aux_loss = 0.0
        if total_dispatched > 0:
            for e in range(self.num_experts):
                f_e = expert_counts[e] / total_dispatched
                P_e = expert_prob_sums[e] / num_tokens
                aux_loss += f_e * P_e
            aux_loss *= self.num_experts

        return decisions, aux_loss


if __name__ == "__main__":
    router = MoETop2GatingRouter(num_experts=4, capacity_factor=1.5)
    # 6 mock token embeddings of dimension 4
    tokens = [
        [1.0, 0.2, -0.5, 0.8],
        [-0.4, 1.2, 0.1, -0.9],
        [0.8, -0.1, 1.5, 0.3],
        [-1.0, -0.8, 0.4, 1.1],
        [0.2, 0.9, -1.1, 0.4],
        [0.7, 0.5, 0.2, -0.3]
    ]

    decisions, aux_loss = router.route_tokens(tokens)
    print(f"MoE Routed {len(tokens)} tokens across 4 experts:")
    for d in decisions:
        print(f" -> Token {d.token_idx}: Experts={d.selected_experts}, Weights={[round(w, 3) for w in d.expert_weights]}, Dropped={d.is_dropped}")

    print(f"Auxiliary Load-Balancing Loss: {aux_loss:.4f}")
    assert len(decisions) == 6
    assert aux_loss > 0.0
    assert not decisions[0].is_dropped
    print("Day 11 MoE Expert Router verification passed.")
