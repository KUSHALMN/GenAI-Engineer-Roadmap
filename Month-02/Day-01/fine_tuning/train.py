"""
train.py — Simulated LoRA fine-tuning loop (Groq/local-compatible).

In production replace the stub forward/backward with:
  - HuggingFace Trainer + peft LoraConfig
  - or Unsloth for 2x faster training
"""
import json
import time
from pathlib import Path
from config import FineTuneConfig


def load_dataset(path: str) -> list[dict]:
    with open(path) as f:
        return [json.loads(line) for line in f if line.strip()]


def simulate_train_step(batch: list[dict], step: int, cfg: FineTuneConfig) -> float:
    """Stub: replace with real forward + backward pass."""
    time.sleep(0.01)
    loss = max(0.1, 2.5 - step * 0.04 + (hash(str(batch)) % 10) * 0.01)
    return round(loss, 4)


def train(cfg: FineTuneConfig = FineTuneConfig()):
    samples = load_dataset(cfg.dataset_path)
    if not samples:
        raise ValueError(f"No samples found at {cfg.dataset_path}. Run prepare_dataset.py first.")

    Path(cfg.output_dir).mkdir(parents=True, exist_ok=True)
    total_steps = (len(samples) // cfg.batch_size) * cfg.num_epochs
    step = 0

    print(f"Starting fine-tune: {cfg.model_name} | {len(samples)} samples | {cfg.num_epochs} epochs")
    print(f"LoRA r={cfg.lora_r}, alpha={cfg.lora_alpha}, lr={cfg.learning_rate}\n")

    for epoch in range(1, cfg.num_epochs + 1):
        for i in range(0, len(samples), cfg.batch_size):
            batch = samples[i : i + cfg.batch_size]
            loss = simulate_train_step(batch, step, cfg)
            step += 1

            if step % cfg.logging_steps == 0:
                print(f"Epoch {epoch} | Step {step}/{total_steps} | Loss: {loss}")

            if step % cfg.save_steps == 0:
                ckpt = Path(cfg.output_dir) / f"checkpoint-{step}"
                ckpt.mkdir(exist_ok=True)
                print(f"  Saved checkpoint -> {ckpt}")

    print(f"\nTraining complete. Final loss: {loss}")
    print(f"Model saved to: {cfg.output_dir}")


if __name__ == "__main__":
    train()
