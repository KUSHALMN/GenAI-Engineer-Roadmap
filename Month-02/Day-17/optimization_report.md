# ⚡ Advanced LLM Inference Optimization Report

## 1. Precision Formats & Quantization Comparison

| Precision | Bits / Weight | Memory per 7B Params | Perplexity Impact | Hardware Support |
|---|---|---|---|---|
| **FP32** | 32 bits | $\approx 28\text{ GB}$ | Baseline | All CPUs / GPUs |
| **FP16** | 16 bits | $\approx 14\text{ GB}$ | Zero degradation | NVIDIA V100, T4, A100 |
| **BF16** | 16 bits | $\approx 14\text{ GB}$ | Preserves dynamic range | NVIDIA A100, H100, TPU |
| **INT8 (SmoothQuant / GPTQ)** | 8 bits | $\approx 7\text{ GB}$ | Negligible ($< 0.1\%$) | Ampere+, Ada Lovelace |
| **INT4 (AWQ / EXL2)** | 4 bits | $\approx 3.8\text{ GB}$ | Minimal ($< 0.5\%$) | Turing+, Ampere, Hopper |

---

## 2. Key Inference Bottlenecks

### A. Compute-Bound vs Memory-Bandwidth Bound
- **Prefill Phase (TTFT)**: Compute-bound. Matrix multiplications over the full prompt token sequence can saturate GPU Tensor Cores.
- **Decoding Phase (Autoregressive Token Generation)**: Memory-bandwidth bound. Each step reads entire model weights and KV Cache from High-Bandwidth Memory (HBM) to compute just 1 token per stream.

---

## 3. KV Cache Memory Sizing Formula

$$\text{KV Cache Size (Bytes)} = 2 \times n_{\text{layers}} \times n_{\text{kv\_heads}} \times d_{\text{head}} \times L_{\text{seq}} \times B \times \text{bytes\_per\_element}$$

For LLaMA-3-8B with $B=16$ concurrent streams and sequence length $L=4096$:
$$2 \times 32 \times 8 \times 128 \times 4096 \times 16 \times 2 \approx 8.58\text{ GB VRAM allocated strictly to KV cache}$$

### Mitigations:
1. **PagedAttention (vLLM)**: Eliminates internal fragmentation by allocating KV cache in non-contiguous virtual pages.
2. **Multi-Query Attention (MQA) & Grouped-Query Attention (GQA)**: Shares key/value heads across query heads, reducing KV cache size by $4\times$ to $8\times$.

---

## 4. Speculative Decoding
- A smaller, fast "draft model" (e.g. LLaMA-3-1B) generates $K$ candidate tokens sequentially.
- The larger "target model" (e.g. LLaMA-3-70B) verifies all $K$ tokens in a single parallel forward pass.
- Yields $2\times$ to $2.5\times$ wall-clock speedup with mathematically identical output distribution.
