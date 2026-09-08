# 💼 Day 24 Recruiter & System Architecture Interview Questions

### 1. "How do you evaluate prompt effectiveness in an enterprise engineering setting?"
**Talking Points**:
- "We replaced intuition with empirical evaluation pipelines. Every prompt template in our service is paired with a test suite and a golden benchmark dataset.
- We measure deterministic metrics (Exact Match and schema conformity for structured outputs) and semantic metrics (BLEU, ROUGE-L, and cosine similarity with sentence embeddings).
- For qualitative quality, we leverage an asynchronous LLM-as-a-judge worker using structured rubrics, with position-swapping to eliminate order bias."

### 2. "When would you use Few-Shot prompting instead of Fine-Tuning?"
**Talking Points**:
- Few-shot prompting has zero training cost, zero GPU cold starts, and can be iterated in seconds by updating the prompt template.
- We choose Few-Shot when adapting a generalist model to a new formatting standard, tone, or few-class classification task.
- We only escalate to Fine-Tuning (LoRA / QLoRA) when we need to teach new specialized vocabulary, reduce token prompt overhead significantly across billions of calls, or achieve deterministic style on an open-weight model.
