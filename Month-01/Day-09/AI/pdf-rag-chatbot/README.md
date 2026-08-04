# PDF RAG Chatbot — Day 09 (Full Pipeline)

Most complete version — fully modular RAG pipeline with dedicated modules for every step.

## Architecture

```
app.py            ← entry point (thin layer)
rag_pipeline.py   ← orchestrates ingest + query
retriever.py      ← retrieves relevant chunks
prompt_builder.py ← builds LLM prompt from context
vector_store.py   ← ChromaDB store & search
embedding.py      ← lazy model loading + encoding
chunking.py       ← word & sentence chunking
pdf_loader.py     ← PDF text extraction
```

## RAG Flow

```
PDF → load_pdf → chunk_by_words → add_chunks → ChromaDB
Query → retrieve → build_prompt → Groq LLM → Answer
```

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

## Improvements over Day-08
- Added `retriever.py` — dedicated retrieval with distance scores
- Added `prompt_builder.py` — clean prompt construction with chunk labels
- Added `rag_pipeline.py` — single orchestrator for ingest + query
- `app.py` is now just 10 lines — clean entry point
