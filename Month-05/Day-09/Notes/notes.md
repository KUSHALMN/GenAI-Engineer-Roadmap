# Day 09 Notes: QLoRA and Quantized Fine-Tuning

## 1. VRAM Scaling
- A 70B parameter model in FP16 requires >140 GB just for weights.
- With 4-bit QLoRA, the 70B base model occupies ~35 GB, allowing fine-tuning on two 24GB GPUs.
