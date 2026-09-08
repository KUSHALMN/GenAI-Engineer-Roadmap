# 🎯 Day 24 Technical Interview Questions: Prompt Engineering & Evals

### Q1: How do you prevent regression when modifying production prompts?
**Answer**:
1. **Golden Evaluation Dataset**: Maintain a curated dataset of at least 100-500 historical queries covering standard inputs, edge cases, multilingual samples, and known failure modes.
2. **Automated CI/CD Prompt Testing**: Run automated evals on every pull request that touches prompt templates (measuring Exact Match, BLEU/ROUGE, and LLM-as-a-judge score).
3. **Shadow Deployments / Canary Prompts**: Route 5% of production traffic to the candidate prompt, monitoring downstream task completion and user acceptance before a 100% rollout.

---

### Q2: What are the primary biases of LLM-as-a-Judge and how do you mitigate them?
**Answer**:
1. **Position Bias**: The judge often prefers the first response it reads. *Mitigation*: Run two passes with swapped order and average the scores.
2. **Verbosity Bias**: Models favor longer, fluffier responses over concise, accurate ones. *Mitigation*: Penalize excessive token length in rubric instructions.
3. **Self-Enhancement Bias**: A model (e.g. GPT-4) may favor its own generated outputs over Claude or LLaMA. *Mitigation*: Blind model identity or use multi-model ensemble judges.
