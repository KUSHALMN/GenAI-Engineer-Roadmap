# PDF RAG Chatbot — Day 08 (Refactored)

Improved version of Day-07 chatbot with modular architecture.

## Architecture

```
app.py          ← main entry point
pdf_loader.py   ← extract text from PDF
chunking.py     ← split text into chunks
embedding.py    ← generate embeddings (lazy loaded model)
vector_store.py ← ChromaDB store & search
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
# Place your PDF as sample.pdf
python app.py
```

## Improvements over Day-07
- Separated embedding logic into `embedding.py`
- Separated vector store logic into `vector_store.py`
- Lazy model loading — model loads only once
- `get_or_create_collection` — safe re-runs
