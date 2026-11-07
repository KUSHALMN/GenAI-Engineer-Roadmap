# Day 10 Notes: Training Loop and Checkpoints

## 1. Checkpoint Hygiene
- Save optimizer state alongside model weights for seamless restart.
- Maintain a rolling window of best validation checkpoints to save disk.
