# Day 29: Technical Interview Preparation — Model Comparison & JIT Profiling

### Q1: What trade-offs dictate whether to deploy a QLoRA 4-bit model vs an FP16 SFT model?
**Answer:**
- **Deploy QLoRA 4-bit:** When hardware is constrained (consumer GPUs, edge devices), throughput must be maximized, or VRAM costs must be reduced by 70%.
- **Deploy FP16 SFT:** When zero perplexity degradation is permissible (e.g. medical diagnosis, legal contracts), or when the base model is already small (e.g. 1B-3B) where 4-bit quantization can degrade syntax.

### Q2: Why is a "Warmup Phase" mandatory when benchmarking Java algorithms?
**Answer:**
The JVM begins execution in interpreted mode. As methods are called frequently ("hot code"), the Tier 1 (C1) and Tier 2 (C2) JIT compilers compile bytecode into optimized machine code and inline methods. Benchmarking without a warmup phase measures interpreter overhead rather than peak runtime efficiency.
