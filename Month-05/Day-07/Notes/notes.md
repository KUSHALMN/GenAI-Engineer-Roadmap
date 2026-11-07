# Day 07 Notes: Transformer Adaptation Concepts

## 1. Trainable vs Frozen Weights
- **Full Fine-Tuning:** 100% weights updated (high GPU VRAM, high storage, risk of forgetting).
- **LoRA / PEFT:** < 1% weights updated (low VRAM, modular adapter swapping).
