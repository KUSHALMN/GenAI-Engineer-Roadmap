# 📝 Day 24 Study Notes: Production Prompt Engineering & Quantitative Evaluation

## 1. Moving Beyond Ad-Hoc Prompting
Production Prompt Engineering is the discipline of treating prompts as version-controlled, tested software components.
- **Zero-shot**: Relying purely on pre-trained weights. Vulnerable to hallucination, formatting violations, and style drift.
- **Few-shot In-Context Learning (ICL)**: Supplying 2-5 explicit demonstration pairs ($x_i \to y_i$). Sets stylistic bounds, reduces output entropy, and establishes strict token formatting.
- **Chain-of-Thought (CoT)**: Forcing the model to generate intermediate reasoning tokens prior to producing the final answer. Elicits multi-step logic from attention heads.

## 2. Quantitative Prompt Evaluation Metrics
1. **Exact Match (EM)**: Binary string equality. Useful for classification, code tokens, and fixed vocabulary outputs.
2. **BLEU (Bilingual Evaluation Understudy)**: Measures n-gram precision with a brevity penalty. Useful for translation and constrained summaries.
3. **ROUGE-L (Recall-Oriented Understudy for Gisting Evaluation)**: Evaluates the Longest Common Subsequence (LCS) between prediction and reference, rewarding structural sentence alignment.
4. **Semantic Cosine Similarity**: Embedding or TF-IDF vector dot products, capturing semantic meaning even when exact words differ.
5. **LLM-as-a-Judge**: Using a larger, frontier model (e.g. Claude 3.5 Sonnet / GPT-4o) with a detailed rubric (1-5 scale) for subjective qualities (factuality, tone, coherence).

## 3. Production Prompt Anti-Patterns
- **The "Everything Prompt"**: Packing 15 unrelated tasks into a single 4,000-token system prompt. (Solution: modular task routing).
- **Hardcoded Prompts in Source Code**: (Solution: extract templates into YAML/JSON with automated version tags).
- **Negation Traps**: "Do NOT include explanations" is far less reliable than "Output ONLY the raw JSON object".
