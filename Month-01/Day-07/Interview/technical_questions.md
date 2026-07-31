# Technical Interview Questions — Day 7

## GenAI / AI

**Q: What is RAG and why is it used?**
> RAG (Retrieval Augmented Generation) combines a retrieval system with an LLM. Instead of relying on training data alone, it fetches relevant documents from an external knowledge base and uses them as context. This makes answers more accurate and up-to-date.

**Q: What is the difference between an embedding and a token?**
> A token is the smallest unit of text an LLM processes (word or subword). An embedding is a dense numerical vector that represents the semantic meaning of text. Tokens are inputs; embeddings are representations.

**Q: What is cosine similarity?**
> A metric to measure similarity between two vectors. It computes the cosine of the angle between them. Range: -1 to 1. In NLP, values closer to 1 mean the texts are semantically similar.

**Q: What is ChromaDB?**
> An open-source vector database used to store and query text embeddings. It enables semantic search — finding documents by meaning rather than exact keyword match.

**Q: What is the difference between zero-shot and few-shot prompting?**
> Zero-shot: ask the model directly without examples. Few-shot: provide 2-3 examples before the actual question to guide the model's output format and reasoning.

---

## Python

**Q: What is a decorator in Python?**
> A function that wraps another function to add behavior without modifying it. Used for logging, timing, authentication, retry logic, etc.

**Q: What is the difference between `@staticmethod` and `@classmethod`?**
> `@staticmethod` — no access to class or instance. `@classmethod` — receives the class (`cls`) as first argument, can access/modify class state.

**Q: What is a context manager?**
> An object that manages resources using `with` statement. Ensures proper setup and teardown (e.g., file closing, DB connection closing).

---

## FastAPI

**Q: What is Pydantic used for in FastAPI?**
> Data validation and serialization. Pydantic models define the shape of request/response data and automatically validate types.

**Q: What is the difference between `@app.get` and `@app.post`?**
> GET retrieves data (no body). POST sends data in the request body to create/process something.

---

## SQL

**Q: What is the difference between DELETE and DROP?**
> DELETE removes rows from a table (table still exists). DROP removes the entire table structure and data permanently.

**Q: What is a PRIMARY KEY?**
> A column (or combination) that uniquely identifies each row. It must be UNIQUE and NOT NULL.
