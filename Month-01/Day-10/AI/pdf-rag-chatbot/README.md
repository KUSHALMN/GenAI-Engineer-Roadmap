# PDF RAG Chatbot — Day 10 (Chain Architecture)

Most advanced version — introduces `chain.py` as the LLM execution layer.

## Architecture

```
app.py            ← thin entry point
rag_pipeline.py   ← ingest + query orchestrator
chain.py          ← LLM execution layer (NEW)
retriever.py      ← retrieve chunks with scores
prompt_builder.py ← build labeled context prompt
vector_store.py   ← ChromaDB store & search
embedding.py      ← lazy model loading + encoding
splitter.py       ← word, sentence, paragraph splitting
loader.py         ← PDF text extraction
```

## RAG Flow

```
PDF → loader → splitter → embedding → vector_store
Query → retriever → prompt_builder → chain → LLM → Answer
```

## New in Day-10
- `chain.py` — dedicated LLM execution, returns question + context + answer
- `splitter.py` — added paragraph splitting strategy
- `query_with_context()` — returns full result dict for debugging

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
