# 🎯 Day 23 Technical Interview Questions: Corrective RAG (CRAG) & Self-RAG

---

### Q1: What is Corrective RAG (CRAG) and how does it improve standard RAG?
**Answer:**  
Standard RAG naively passes retrieved documents to the LLM regardless of their quality or relevance. If the retriever fetches noisy or irrelevant chunks, the model hallucinates or outputs irrelevant answers.  
**CRAG (Corrective RAG)** introduces a **Retrieval Evaluator** that scores the confidence of retrieved documents:
1. **Correct:** High confidence — performs knowledge refinement (strips irrelevant sentences from chunks).
2. **Ambiguous:** Medium confidence — combines refined local strips with external web search.
3. **Incorrect:** Low confidence — discards local documents entirely, reformulates the query, and triggers external web retrieval.

---

### Q2: What are Self-RAG reflection tokens?
**Answer:**  
Self-RAG trains or prompts language models to output explicit critique tokens during generation:
- `[Retrieve]`: Predicts whether external knowledge retrieval is needed (`Yes` vs `No`).
- `[IsRel]`: Evaluates if retrieved context is actually relevant to the query (`Relevant` vs `Irrelevant`).
- `[IsSup]`: Checks if the generated answer is supported by the context (`Fully Supported`, `Partially Supported`, `No`).
- `[IsUse]`: Rates the helpfulness and utility of the response on a 1-5 scale.

---

### Q3: How do you implement O(1) LRU Cache in Java?
**Answer:**  
Combine a **HashMap** (keys to node references) with a **Doubly Linked List** (tracks access recency):
- `get(key)`: Lookup node in HashMap in $O(1)$. Move node to head of list in $O(1)$. Return value.
- `put(key, value)`: If key exists, update value and move to head. If new, insert at head. If capacity is exceeded, remove node from tail (least recently used) and delete from HashMap. Both operations execute in $O(1)$ time and $O(N)$ space.
