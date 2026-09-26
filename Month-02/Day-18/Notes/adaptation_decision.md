# 🧭 GenAI Model Adaptation Decision Framework

## 1. Adaptation Decision Matrix

| Dimension | Prompt Engineering / Few-Shot | RAG (Retrieval-Augmented) | Fine-Tuning (LoRA / SFT) | Continued Pre-training |
|---|---|---|---|---|
| **Primary Goal** | Task steering & formatting | Dynamic factual knowledge injection | Style, tone, syntax, domain vocabulary | Core world knowledge in new languages/domains |
| **Knowledge Dynamic** | Static / Short-term | Real-time / Dynamic | Static snapshot at training | Highly static snapshot |
| **Setup Cost** | Near \$0 | Low to Moderate (Vector DB) | Moderate (\$100–\$5,000 GPU) | Extremely High (\$50k–\$1M+) |
| **Inference Cost** | Higher (long context tokens) | Higher (context chunks added) | Lower (shorter prompts needed) | Standard |
| **Hallucination Control**| Moderate | Superior (strict context citations) | Poor (hallucinates ungrounded facts) | Poor without RAG |
| **Maintenance** | Trivial (prompt updates) | Moderate (ETL pipeline & indexing) | High (retraining on drift) | Very High |

---

## 2. Decision Tree Rule of Thumb

1. **Start with Prompt Engineering**: Always establish a few-shot prompt baseline with structured outputs.
2. **If the model lacks private / rapidly changing facts**: Add **RAG**. Fine-tuning is NOT a substitute for knowledge retrieval.
3. **If the model fails to adhere to rigid output styles or syntax**: Use **Fine-Tuning (LoRA)** to bake behavioral conventions into weights, reducing prompt token overhead.
4. **The Ideal Production Pattern**: Combine **Fine-Tuned Small Model (for style/efficiency) + RAG (for live factual grounding)**.
