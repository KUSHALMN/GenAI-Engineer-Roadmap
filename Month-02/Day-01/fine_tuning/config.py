from dataclasses import dataclass

@dataclass
class FineTuneConfig:
    model_name: str = "llama3-8b-8192"
    dataset_path: str = "fine_tuning/dataset.jsonl"
    output_dir: str = "fine_tuning/output"
    num_epochs: int = 3
    batch_size: int = 4
    learning_rate: float = 2e-4
    max_seq_length: int = 512
    lora_r: int = 16
    lora_alpha: int = 32
    lora_dropout: float = 0.05
    warmup_steps: int = 10
    save_steps: int = 50
    logging_steps: int = 10
    fp16: bool = True
    gradient_checkpointing: bool = True
