# 📝 Notes — Day 15: Distributed Checkpointing & Maximal Rectangle

- **Resharding on Resume:** DCP metadata tracks global tensor slices and offsets, allowing checkpoints saved on 128 GPUs to be seamlessly loaded and resharded onto a different cluster topology (e.g. 64 or 256 GPUs).
- **Matrix Array Cache Locality:** Maintain a single reusable 1D `heights` array rather than reallocating per row to minimize JVM garbage collection pressure.
