# Day 01: Technical Interview Preparation — Fine-Tuning Decision Matrix & Java Lists

### Q1: When is Supervised Fine-Tuning (SFT) the WRONG choice for an LLM application?
**Answer:**
SFT is unsuitable when:
1. **Dynamic/Factual Knowledge Updates:** LLMs are poor fact databases; updating factual memory via fine-tuning causes hallucinations and knowledge cutoff issues. RAG is the appropriate solution.
2. **Lack of High-Quality Labeled Data:** Fine-tuning on fewer than 500 noisy or malformed samples destroys base model generalization.
3. **Budget/Maintenance Constraints:** Fine-tuned weights must be hosted, scaled, and re-trained as base model versions advance.

### Q2: Why is `ArrayList` almost universally preferred over `LinkedList` in modern Java, even for frequent middle insertions?
**Answer:**
`ArrayList` stores elements in contiguous memory arrays, maximizing CPU L1/L2 cache line hits (spatial locality). `LinkedList` allocates discrete node objects scattered across heap memory, incurring significant pointer-chasing latency and 24-32 bytes of reference overhead per element.
