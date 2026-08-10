# Technical Questions — Day 12

## Stack DSA

**Q: What is a monotonic stack?**
A stack where elements are maintained in increasing or decreasing order. Used for "next greater/smaller element" problems.

**Q: Time complexity of Daily Temperatures solution?**
O(n) — each element is pushed and popped at most once.

**Q: How does Evaluate RPN work?**
Push numbers onto stack. On operator, pop two operands, apply operator, push result. Final stack top is the answer.

**Q: Why use stack for Valid Parentheses?**
LIFO matches the nesting structure — the most recently opened bracket must be closed first.

## RAG Pipeline

**Q: What does source_handler.py do?**
Loads PDF, extracts text, and splits into overlapping chunks for better context preservation.

**Q: Why overlap chunks?**
Prevents losing context at chunk boundaries — a sentence split across chunks is still retrievable.

**Q: What is the role of prompt_builder.py?**
Formats retrieved chunks + user query into a structured prompt that guides the LLM to answer from context only.
