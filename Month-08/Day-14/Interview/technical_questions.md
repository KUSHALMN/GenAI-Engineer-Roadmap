# 🎯 Technical Interview Questions — Day 14: Red Teaming & Topological Sort

### 1. What is an automated red-teaming harness (e.g., Garak or PyRIT)?
**Answer:**
An automated red-teaming harness programmatically generates attack vectors (character-level encoding tricks, linguistic style shifts, multi-turn conversational traps, indirect payload injections) against an AI endpoint and evaluates whether the model violated its safety policy or leaked system instructions, outputting a quantifiable attack vulnerability report.

### 2. How does Kahn's algorithm detect cycles in a directed graph?
**Answer:**
Kahn's algorithm initializes a queue with all nodes having `inDegree == 0`. Every time a node is dequeued, its outgoing edges are removed, decrementing the in-degrees of its neighbors. If the graph contains a directed cycle, the nodes within the cycle will never reach an in-degree of 0, resulting in the final visited node count being strictly less than the total number of nodes $V$.
