# PDF RAG Chatbot — Day 11 (Config-Driven)

All settings centralized in `config.py` — no hardcoded values anywhere.

## Architecture

```
config.py         ← ALL settings (NEW)
app.py            ← thin entry point
rag_pipeline.py   ← ingest + query orchestrator
chain.py          ← LLM execution layer
retriever.py      ← retrieve chunks with scores
prompt_builder.py ← build labeled context prompt
vector_store.py   ← ChromaDB store & search
embedding.py      ← lazy model loading + encoding
splitter.py       ← word, sentence, paragraph splitting
loader.py         ← PDF text extraction
```

## New in Day-11
- `config.py` — single source of truth for all settings
- All modules import from config — no hardcoded strings
- Easy to change model, chunk size, collection name in one place

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
