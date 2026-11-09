# Technical Interview Preparation — Answer Grounding & Knapsack DP
1. Citation Verification in RAG: Every generated factual claim must map to a retrieved evidence chunk ID. Sentences lacking bracketed citations fail grounding audits.
2. 0/1 Knapsack Reverse Traversal: Inner loop traverses backwards (`j = target; j >= num; j--`) to ensure each item is used at most once.
