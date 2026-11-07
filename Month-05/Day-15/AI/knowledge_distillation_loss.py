"""
Day 15: Model Knowledge Distillation
Computes soft-target distillation loss combining:
- Cross-entropy with ground-truth hard labels
- KL Divergence with temperature-scaled soft teacher logits
L = (1 - alpha) * CE(student, hard) + alpha * (T^2) * KL(soft_student, soft_teacher)
"""

import numpy as np

class DistillationLossCalculator:
    def __init__(self, temperature: float = 2.0, alpha: float = 0.5):
        self.temperature = temperature
        self.alpha = alpha

    def softmax(self, logits: np.ndarray, temp: float = 1.0) -> np.ndarray:
        scaled = logits / temp
        exp_logits = np.exp(scaled - np.max(scaled))
        return exp_logits / np.sum(exp_logits)

    def compute_loss(self, student_logits: np.ndarray, teacher_logits: np.ndarray, label_idx: int) -> float:
        # 1. Hard Cross Entropy
        student_hard_probs = self.softmax(student_logits, temp=1.0)
        hard_loss = -np.log(max(1e-12, student_hard_probs[label_idx]))

        # 2. Soft KL Divergence
        soft_student = self.softmax(student_logits, temp=self.temperature)
        soft_teacher = self.softmax(teacher_logits, temp=self.temperature)
        kl_div = np.sum(soft_teacher * np.log(soft_teacher / (soft_student + 1e-12)))

        total_loss = (1 - self.alpha) * hard_loss + (self.alpha * (self.temperature ** 2) * kl_div)
        return round(float(total_loss), 4)

if __name__ == "__main__":
    calc = DistillationLossCalculator(temperature=2.0, alpha=0.6)
    student_l = np.array([2.0, 1.0, 0.1])
    teacher_l = np.array([3.0, 1.5, 0.0])
    loss = calc.compute_loss(student_l, teacher_l, label_idx=0)

    assert loss > 0.0
    print(f"Calculated Knowledge Distillation Loss: {loss}")
    print("Day 15 AI Knowledge Distillation passed all tests.")
