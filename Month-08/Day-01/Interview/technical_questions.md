# 🎯 Technical Interview Questions — Day 01: Evaluation Strategy & Arrays

### 1. How do you construct a comprehensive evaluation matrix for enterprise GenAI applications?
**Answer:**
A robust evaluation matrix measures five orthogonal axes:
1. **Faithfulness / Groundedness:** Verifies answers rely strictly on retrieved context without hallucinations.
2. **Context Relevance / Precision:** Measures noise ratio in retrieved chunks.
3. **Task Completion / Helpfulness:** Assesses fulfillment of user intent and formatting adherence.
4. **Safety & Policy Guardrails:** Evaluates resistance to jailbreaks, toxic outputs, and PII leakage.
5. **Operational SLAs:** Latency (TTFT, Total Response) and Token Cost per transaction.

### 2. What is the time and space complexity of HashMap lookups in Java under high collision?
**Answer:**
Under uniform hash distribution, lookups take $O(1)$ amortized time. Under severe collisions (Java 8+), bucket linked lists exceeding 8 nodes transform into Red-Black Trees (`TreeNode`), guaranteeing $O(\log N)$ worst-case lookup time instead of legacy $O(N)$.
