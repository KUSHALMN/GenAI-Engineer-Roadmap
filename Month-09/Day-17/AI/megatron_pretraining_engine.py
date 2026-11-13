"""
Megatron-LM Pretraining Loop from First Principles:
Forward Compute, Backward Propagation, Global Gradient Norm Clipping,
Cosine Annealing Learning Rate Scheduler with Warmup, and Weight Decay.
"""

import math
from typing import List, Tuple


class CosineWarmupLRScheduler:
    """
    Standard LLM Cosine Annealing learning rate schedule with linear warmup and minimum floor.
    """
    def __init__(self, max_lr: float, min_lr: float, warmup_steps: int, total_steps: int):
        self.max_lr = max_lr
        self.min_lr = min_lr
        self.warmup_steps = warmup_steps
        self.total_steps = total_steps

    def get_lr(self, current_step: int) -> float:
        if current_step < self.warmup_steps:
            return self.max_lr * (current_step / max(1, self.warmup_steps))
        if current_step > self.total_steps:
            return self.min_lr
        decay_ratio = (current_step - self.warmup_steps) / (self.total_steps - self.warmup_steps)
        coeff = 0.5 * (1.0 + math.cos(math.pi * decay_ratio))
        return self.min_lr + coeff * (self.max_lr - self.min_lr)


class DistributedPretrainingEngine:
    """
    Simulates a step in the distributed pretraining loop including
    norm clipping, learning rate updates, and AdamW weight decay.
    """
    def __init__(self, max_grad_norm: float = 1.0, weight_decay: float = 0.1):
        self.max_grad_norm = max_grad_norm
        self.weight_decay = weight_decay

    def clip_grad_norm(self, gradients: List[float]) -> Tuple[List[float], float]:
        norm = math.sqrt(sum(g * g for g in gradients))
        clip_coef = self.max_grad_norm / (norm + 1e-6)
        if clip_coef < 1.0:
            clipped = [g * clip_coef for g in gradients]
            return clipped, norm
        return gradients, norm

    def optimizer_step(self, weights: List[float], gradients: List[float], lr: float) -> List[float]:
        clipped_grads, norm = self.clip_grad_norm(gradients)
        updated = []
        for w, g in zip(weights, clipped_grads):
            # Decoupled AdamW weight decay: w = w - lr * wd * w - lr * g
            w_next = w - (lr * self.weight_decay * w) - (lr * g)
            updated.append(w_next)
        return updated


if __name__ == "__main__":
    scheduler = CosineWarmupLRScheduler(max_lr=3e-4, min_lr=3e-5, warmup_steps=100, total_steps=1000)
    engine = DistributedPretrainingEngine(max_grad_norm=1.0, weight_decay=0.1)

    # Step 0: Warmup start
    lr_0 = scheduler.get_lr(0)
    assert lr_0 == 0.0

    # Step 100: Peak warmup
    lr_100 = scheduler.get_lr(100)
    assert abs(lr_100 - 3e-4) < 1e-8

    # Step 1000: Min LR floor
    lr_1000 = scheduler.get_lr(1000)
    assert abs(lr_1000 - 3e-5) < 1e-8

    # Test Gradient Clipping
    weights = [1.0, 2.0]
    grads = [3.0, 4.0] # Norm = 5.0 > max_grad_norm 1.0
    clipped, raw_norm = engine.clip_grad_norm(grads)
    assert raw_norm == 5.0
    assert abs(math.sqrt(sum(c * c for c in clipped)) - 1.0) < 1e-5

    print(f"Pretraining Loop verified: LR schedule [{lr_0:.1e} -> {lr_100:.1e} -> {lr_1000:.1e}], Grad Norm clipped from 5.0 to 1.0.")
    print("Day 17 Megatron Pretraining Engine verification passed.")
