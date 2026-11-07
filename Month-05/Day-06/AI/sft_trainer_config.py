"""
Day 06: Supervised Fine-Tuning (SFT) Fundamentals
Configures next-token prediction loss, learning rate schedules (Cosine/Linear),
gradient accumulation, batch sizes, and validation evaluation intervals.
"""

from dataclasses import dataclass
from typing import Dict, Any
import json

@dataclass
class SFTTrainingConfig:
    model_name_or_path: str
    output_dir: str
    num_train_epochs: int = 3
    per_device_train_batch_size: int = 4
    gradient_accumulation_steps: int = 4 # Effective batch size = 16
    learning_rate: float = 2e-4
    warmup_ratio: float = 0.03
    lr_scheduler_type: str = "cosine"
    fp16: bool = False
    bf16: bool = True
    logging_steps: int = 10
    save_strategy: str = "epoch"

    def calculate_effective_batch_size(self, num_gpus: int = 1) -> int:
        return self.per_device_train_batch_size * self.gradient_accumulation_steps * num_gpus

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__

if __name__ == "__main__":
    cfg = SFTTrainingConfig(
        model_name_or_path="meta-llama/Llama-3.2-3B",
        output_dir="./checkpoints_sft"
    )
    eff_batch = cfg.calculate_effective_batch_size(num_gpus=2)
    assert eff_batch == 32 # 4 * 4 * 2
    print("SFT Training Configuration:")
    print(json.dumps(cfg.to_dict(), indent=2))
    print(f"Effective Global Batch Size (2 GPUs): {eff_batch}")
    print("Day 06 AI SFT Configuration passed all tests.")
