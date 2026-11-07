# 📅 Month 05 — Fine-Tuning, Model Adaptation & Inference

> Topics: Fine-Tuning Decision Framework, Instruction Dataset Design (ChatML, Alpaca, ShareGPT), Dataset Cleaning & Near-Deduplication, Data Leakage Prevention, Synthetic Data Generation (Self-Instruct), Supervised Fine-Tuning (SFT) Fundamentals & Masked Next-Token Loss, Parameter Freezing, Low-Rank Adaptation (LoRA Mechanics, Rank, Alpha), QLoRA & 4-bit NormalFloat (NF4), Training Loops & Checkpointing, Experiment Tracking (MLflow/WandB), Fine-Tuning Evaluation & Golden Prompts, Catastrophic Forgetting & Early Stopping, Direct Preference Optimization (DPO), Knowledge Distillation & Soft Targets, Model Artifact Packaging & Manifests, Inference vs Training (Prefill vs Decode, TTFT & TPOT), Quantization Methods (AWQ, GPTQ, GGUF), KV Cache Memory Math & Grouped-Query Attention (GQA), Batching Strategies & Continuous Batching, vLLM & PagedAttention Virtual Paging, Streaming Inference API (SSE), Model Server Concurrency & Preemption, Model Gateway & Provider Abstraction, Model Routing Evaluation, Prompt & Model Version Control, Inference Failure Handling, Cost & Capacity Planning, and Capstone Benchmarking.

---

## 🎯 Day-by-Day Implementation Plan (Day 01 – Day 31)

| Day | GenAI / Fine-Tuning & Serving Topic | Key Deliverables (Python in `AI/`) | DSA & Concurrency (Java in `DSA/`) | Status |
|:---:|:------------------------------------|:-----------------------------------|:-----------------------------------|:------:|
| [Day 01](Day-01/) | Fine-Tuning Decision Framework | `fine_tuning_decision_framework.py` (Prompting vs RAG vs SFT) | Collections — ArrayList vs LinkedList (`ListComparison.java`) | ✅ Done |
| [Day 02](Day-02/) | Instruction Dataset Design | `instruction_dataset_schema.py` (ChatML schema, role validation) | HashMap Internals & Resizing (`CustomHashMap.java`) | ✅ Done |
| [Day 03](Day-03/) | Dataset Cleaning & Validation | `dataset_cleaner_validator.py` (Deduplication, token bounds) | Sets & Ordered Maps — TreeSet/TreeMap (`OrderedMapsSets.java`) | ✅ Done |
| [Day 04](Day-04/) | Data Splitting & Leakage Prevention | `dataset_splitter.py` (Stratified splits, contamination audit) | PriorityQueue & Custom Comparators (`PriorityQueueScheduler.java`) | ✅ Done |
| [Day 05](Day-05/) | Synthetic Data Generation | `synthetic_data_generator.py` (Combinatorial domain synthesis) | Generics & Type Safety PECS (`GenericsTypeSafety.java`) | ✅ Done |
| [Day 06](Day-06/) | Supervised Fine-Tuning Fundamentals | `sft_trainer_config.py` (Cosine schedule, effective batch size) | Java Streams & Collection Pipelines (`StreamPipelines.java`) | ✅ Done |
| [Day 07](Day-07/) | Transformer Adaptation Concepts | `parameter_freezing_experiment.py` (Trainable parameter audit) | Immutability & Defensive Copies (`ImmutableClassPattern.java`) | ✅ Done |
| [Day 08](Day-08/) | LoRA Mechanics | `lora_linear_simulator.py` (Low-rank forward pass, weight merge) | Amortized Complexity — Dynamic Array (`DynamicArrayAmortized.java`) | ✅ Done |
| [Day 09](Day-09/) | QLoRA & Quantized Fine-Tuning | `qlora_memory_calculator.py` (4-bit NF4, double quant VRAM math) | Advanced Design — LRU Cache (`LRUCache.java`) | ✅ Done |
| [Day 10](Day-10/) | Training Loop and Checkpoints | `training_loop_simulator.py` (Gradient accumulation, checkpoints) | Advanced Design — LFU Cache (`LFUCache.java`) | ✅ Done |
| [Day 11](Day-11/) | Fine-Tuning Experiment Tracking | `experiment_tracker.py` (Hyperparameters, loss curves, metrics) | Data Structures — MinMaxStack O(1) (`MinMaxStack.java`) | ✅ Done |
| [Day 12](Day-12/) | Fine-Tuning Evaluation | `model_eval_comparison.py` (Base vs adapted accuracy benchmarks) | Streaming Median — Two Heaps (`MedianFinder.java`) | ✅ Done |
| [Day 13](Day-13/) | Overfitting and Generalization | `overfitting_detector.py` (Train/val divergence, early stopping) | O(1) Insert/Delete/GetRandom (`RandomizedSet.java`) | ✅ Done |
| [Day 14](Day-14/) | Preference Optimization (DPO) | `dpo_loss_simulator.py` (Closed-form preference loss, beta margin) | Time-Based Key-Value Store (`TimeMap.java`) | ✅ Done |
| [Day 15](Day-15/) | Model Knowledge Distillation | `knowledge_distillation_loss.py` (Soft targets, temperature scaling) | System Design — Design Hit Counter (`HitCounter.java`) | ✅ Done |
| [Day 16](Day-16/) | Model Artifact Packaging | `model_packaging_manifest.py` (Manifests, zero weight pollution) | Rate Limiter — Token Bucket (`RateLimiterAlgorithms.java`) | ✅ Done |
| [Day 17](Day-17/) | Inference vs Training Deep Dive | `prefill_decode_benchmark.py` (Compute-bound prefill vs memory decode) | Concurrency — ConcurrentHashMap (`ConcurrentStateMap.java`) | ✅ Done |
| [Day 18](Day-18/) | Quantization Methods | `quantization_compare.py` (FP16 vs INT8 vs AWQ/GPTQ 4-Bit) | Concurrency — Bounded Blocking Queue (`BoundedBlockingQueue.java`) | ✅ Done |
| [Day 19](Day-19/) | KV Cache & Memory Math | `kv_cache_calculator.py` (GQA memory sizing, sequence bounds) | Concurrency — Producer-Consumer Queue (`ProducerConsumerQueue.java`) | ✅ Done |
| [Day 20](Day-20/) | Batching & Continuous Batching | `continuous_batching_sim.py` (Iteration-level batching) | Concurrency — ExecutorService & Futures (`ThreadPoolBatchExecutor.java`) | ✅ Done |
| [Day 21](Day-21/) | Inference Serving with vLLM | `paged_attention_sim.py` (Virtual page memory tables) | Concurrency — CompletableFuture (`AsyncCompletableWorkflows.java`) | ✅ Done |
| [Day 22](Day-22/) | Streaming Inference API | `streaming_inference_api.py` (SSE token stream, disconnect hooks) | Concurrency — ReentrantReadWriteLock (`ReadWriteLockState.java`) | ✅ Done |
| [Day 23](Day-23/) | Model Server Concurrency | `model_server_concurrency.py` (GPU queue saturation dynamics) | Concurrency — Deadlock Avoidance (`DeadlockAvoidance.java`) | ✅ Done |
| [Day 24](Day-24/) | Model Gateway & Abstraction | `model_gateway.py` (Unified provider dispatch & fallback) | Concurrency — Atomic CAS Operations (`AtomicCounterCAS.java`) | ✅ Done |
| [Day 25](Day-25/) | Model Routing Evaluation | `model_router_eval.py` (3B vs 8B vs 70B cost-quality routing) | Advanced Design — Thread-Safe TTL Cache (`ThreadSafeTTLCache.java`) | ✅ Done |
| [Day 26](Day-26/) | Prompt & Model Version Control | `version_control_manifest.py` (Semantic versioning & hashes) | Concurrency — ThreadPool Rejection (`CustomThreadPoolRejection.java`) | ✅ Done |
| [Day 27](Day-27/) | Inference Failure Handling | `inference_failure_handler.py` (Context overflow truncation) | Concurrency — Semaphore Rate Limiting (`SemaphoreRateLimiter.java`) | ✅ Done |
| [Day 28](Day-28/) | Cost and Capacity Planning | `cost_capacity_model.py` (GPU sizing & cloud budget models) | Concurrency — Java Memory Model / DCL (`SafePublicationJMM.java`) | ✅ Done |
| [Day 29](Day-29/) | Reproducible Model Comparison | `model_comparison_benchmark.py` (Quality vs TTFT vs cost matrix) | Performance — Microbenchmarking Profiler (`MicrobenchmarkProfile.java`) | ✅ Done |
| [Day 30](Day-30/) | Project 5 Release: Adaptation Lab | `project5_adaptation_lab_release.py` (Full package release) | 90-Min Capstone Collections Mock (`CapstoneCollectionsMock.java`) | ✅ Done |
| [Day 31](Day-31/) | Enterprise Serving Capstone | `enterprise_serving_benchmark.py` (Throughput, P99, VRAM benchmarks) | Concurrency — Lock-Free Ring Buffer (`ConcurrentRingBuffer.java`) | ✅ Done |

---

## 🏗️ Directory Architecture

Every day module strictly adheres to the established repository standard:
- `AI/` — **Python GenAI engines, fine-tuning scripts, memory calculators, and inference servers.**
- `DSA/` — **Runnable Java solutions with comprehensive `main` verification test drivers.**
- `Interview/` — **Technical Q&A deep-dives covering systems design and algorithm invariants.**
- `Notes/` — **Explanatory engineering notes detailing theory, architecture, and production trade-offs.**
- `README.md` — **Individual day guide with problem breakdown, folder layout, and run instructions.**
