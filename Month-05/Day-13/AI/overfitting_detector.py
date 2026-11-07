"""
Day 13: Overfitting and Generalization
Detects memorization and catastrophic forgetting by tracking
training loss vs validation loss divergence and early stopping triggers.
"""

from typing import List, Dict, Any

class OverfittingDetector:
    def __init__(self, patience: int = 3, delta_threshold: float = 0.05):
        self.patience = patience
        self.delta_threshold = delta_threshold

    def monitor_losses(self, train_losses: List[float], val_losses: List[float]) -> Dict[str, Any]:
        best_val = float("inf")
        patience_counter = 0
        early_stop_epoch = -1

        for epoch, (t_loss, v_loss) in enumerate(zip(train_losses, val_losses), start=1):
            if v_loss < best_val - self.delta_threshold:
                best_val = v_loss
                patience_counter = 0
            else:
                patience_counter += 1

            if patience_counter >= self.patience:
                early_stop_epoch = epoch
                break

        divergence = [round(v - t, 3) for t, v in zip(train_losses, val_losses)]
        is_overfitting = any(d > 0.5 for d in divergence)

        return {
            "early_stopped": early_stop_epoch != -1,
            "stop_epoch": early_stop_epoch,
            "best_val_loss": round(best_val, 4),
            "is_overfitting": is_overfitting,
            "loss_divergence": divergence
        }

if __name__ == "__main__":
    detector = OverfittingDetector(patience=2)
    # Simulated overfitting: train loss drops rapidly while val loss rises
    train_history = [2.0, 1.4, 0.8, 0.4, 0.2]
    val_history   = [2.1, 1.5, 1.6, 1.8, 2.3]

    res = detector.monitor_losses(train_history, val_history)
    assert res["early_stopped"] is True
    assert res["is_overfitting"] is True
    print("Overfitting Detection Report:")
    print(res)
    print("Day 13 AI Overfitting Detector passed all tests.")
