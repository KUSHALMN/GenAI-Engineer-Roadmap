# AI/GenAI Concepts Cheatsheet — Month 01

## Core Concepts

| Term | Definition |
|------|-----------|
| LLM | Large Language Model trained on massive text data |
| Token | Smallest unit of text an LLM processes |
| Embedding | Dense vector representation of text |
| RAG | Retrieval Augmented Generation — fetch docs + generate |
| Prompt | Input instruction given to an LLM |
| Context Window | Max tokens an LLM can process at once |
| Temperature | Controls randomness of LLM output (0=deterministic) |

## Prompting Techniques

| Technique | When to Use |
|-----------|------------|
| Zero-shot | Simple tasks, no examples needed |
| Few-shot | Complex tasks, provide 2-3 examples |
| Chain-of-Thought | Math/reasoning — ask to think step by step |
| System Role | Set AI persona/behavior for entire conversation |

## RAG Pipeline

```
Document → Chunk → Embed → Store in VectorDB
Query → Embed → Search VectorDB → Retrieve → LLM → Answer
```

## FastAPI Quick Reference

```python
@app.get("/")          # GET endpoint
@app.post("/")         # POST endpoint
@app.put("/{id}")      # PUT endpoint
@app.delete("/{id}")   # DELETE endpoint
```

## SQL Quick Reference

```sql
CREATE TABLE users (id SERIAL PRIMARY KEY, name VARCHAR(100));
INSERT INTO users (name) VALUES ('Kushal');
SELECT * FROM users WHERE id = 1;
UPDATE users SET name = 'MN' WHERE id = 1;
DELETE FROM users WHERE id = 1;
```

## Tools Used So Far

| Tool | Purpose |
|------|---------|
| Groq API | LLM inference (LLaMA 3.3 70B) |
| ChromaDB | Local vector database |
| Sentence Transformers | Generate text embeddings |
| FastAPI | Build REST APIs |
| psycopg2 | Connect Python to PostgreSQL |
| pypdf | Extract text from PDFs |
