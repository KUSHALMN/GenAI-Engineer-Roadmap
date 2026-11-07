# Day 06 Notes: Supervised Fine-Tuning Fundamentals

## 1. Key Hyperparameters
- **Effective Batch Size:** `batch_per_device * grad_accum_steps * gpus`.
- **Learning Rate:** Typically $10^{-4}$ to $2 \times 10^{-4}$ for LoRA; $10^{-5}$ to $2 \times 10^{-5}$ for full fine-tuning.
- **Prompt Masking:** Always mask prompt tokens from loss computation.
