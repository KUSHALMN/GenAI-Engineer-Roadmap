# PDF RAG Chatbot — Day 12

A modular Retrieval-Augmented Generation chatbot that answers questions from PDF documents.

## Architecture

```
PDF → source_handler → chunks → retriever (ChromaDB)
Query → retriever → top-k chunks → prompt_builder → Groq LLM → Answer
```

## Files

| File | Purpose |
|------|---------|
| `config.py` | All settings in one place |
| `source_handler.py` | Load PDF and chunk text |
| `retriever.py` | Store and retrieve chunks via ChromaDB |
| `prompt_builder.py` | Build context-aware prompts |
| `rag_pipeline.py` | Orchestrate ingest and query |
| `app.py` | Entry point |

## Setup

```bash
pip install -r requirements.txt
```

Create `.env`:
```
GROQ_API_KEY=your_key_here
```

## Run

```bash
python app.py
```
