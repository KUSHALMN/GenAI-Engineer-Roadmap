"""
Day 11: Fine-Tuning Experiment Tracking
Simulates MLflow / WandB run tracking: logs parameters, epochs,
training loss, eval perplexity, and generates run comparison tables.
"""

from typing import Dict, Any, List

class ExperimentTracker:
    def __init__(self):
        self.runs: Dict[str, Dict[str, Any]] = {}

    def log_run(self, run_id: str, params: Dict[str, Any], metrics: Dict[str, float]):
        self.runs[run_id] = {
            "run_id": run_id,
            "params": params,
            "metrics": metrics
        }

    def get_best_run(self, metric_key: str = "eval_loss", lower_is_better: bool = True) -> Dict[str, Any]:
        sorted_runs = sorted(
            self.runs.values(),
            key=lambda r: r["metrics"].get(metric_key, float("inf")),
            reverse=not lower_is_better
        )
        return sorted_runs[0]

if __name__ == "__main__":
    tracker = ExperimentTracker()

    tracker.log_run("run_lora_r8", {"rank": 8, "lr": 2e-4}, {"eval_loss": 0.85, "eval_accuracy": 0.82})
    tracker.log_run("run_lora_r16", {"rank": 16, "lr": 1e-4}, {"eval_loss": 0.72, "eval_accuracy": 0.89})
    tracker.log_run("run_lora_r32", {"rank": 32, "lr": 5e-5}, {"eval_loss": 0.76, "eval_accuracy": 0.87})

    best = tracker.get_best_run("eval_loss")
    assert best["run_id"] == "run_lora_r16"
    print(f"Best Experiment Run: {best['run_id']} with eval_loss {best['metrics']['eval_loss']}")
    print("Day 11 AI Experiment Tracker passed all tests.")
