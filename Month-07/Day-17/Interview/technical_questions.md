# 🎯 Technical Interview Questions — Day 17: Autoscaling & Rate Limiting LLD

### 1. Why is CPU utilization an inadequate autoscaling metric for LLM inference clusters?
**Answer:**
LLM inference running on GPU workers (e.g., vLLM, TensorRT-LLM) offloads computations to Tensor Cores, leaving host CPU utilization low (<20%) even when the GPU VRAM is completely saturated. Key metrics for GPU autoscaling must be:
- **GPU KV Cache Usage / Memory Allocation %**
- **Inference Request Queue Depth**
- **Time to First Token (TTFT) SLA Degradation**

### 2. How do you scale a Sliding Window Log Rate Limiter across multiple servers?
**Answer:**
In a distributed setting, storing timestamps in local Java queues causes split-brain limits. Use **Redis Sorted Sets (ZSET)**:
1. Add timestamp: `ZADD ratelimit:tenant_id <now> <now>`.
2. Remove expired entries: `ZREMRANGEBYSCORE ratelimit:tenant_id -inf <now - window>`.
3. Count remaining: `ZCARD ratelimit:tenant_id`.
Execute these 3 commands inside an atomic Redis transaction or Lua script.
