# 📝 Notes — Day 19: Hardware Profiling & N-Queens

- **6P Rule of Thumb:** In Transformer pretraining, computing the forward pass takes $2P$ FLOPs per token, and the backward pass takes $4P$ FLOPs per token (total $6P$).
- **Bitmask Diagonal Shifting:** Shifting diagonal bitmasks by 1 simulates the geometric projection onto the adjacent chessboard row.
