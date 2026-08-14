# PDF RAG Chatbot — Day 15 (Hybrid Search)

RAG chatbot with semantic, keyword, and hybrid retrieval strategies.

## Architecture

```
PDF → loader → splitter → embedding → vector_store (ChromaDB)

Query
  ├── semantic_retriever  → ChromaDB vector search
  ├── keyword_retriever   → keyword overlap scoring
  └── hybrid_retriever    → merge + deduplicate → top-k
        ↓
  prompt_builder → Groq LLM → Answer
```

## Structure

```
pdf-rag-chatbot/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── loader.py
│   ├── splitter.py
│   ├── embedding.py
│   ├── vector_store.py
│   ├── retriever.py
│   ├── prompt_builder.py
│   ├── rag_pipeline.py
│   └── source_handler.py
├── retrieval/
│   ├── semantic_retriever.py
│   ├── keyword_retriever.py
│   └── hybrid_retriever.py
├── tests/
│   └── test_health.py
├── Dockerfile
├── requirements.txt
├── .env.example
└── README.md
```

## Retrieval Strategies

| Strategy | How | Best For |
|----------|-----|----------|
| Semantic | ChromaDB vector similarity | Meaning-based queries |
| Keyword | Word overlap scoring | Exact term matching |
| Hybrid | Merge both, deduplicate | Best overall coverage |

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env  # add GROQ_API_KEY
```

## Run

```bash
python -m app.main
```

## Docker

```bash
docker build -t pdf-rag-chatbot .
docker run --env-file .env pdf-rag-chatbot
```

## Tests

```bash
pytest tests/
```
