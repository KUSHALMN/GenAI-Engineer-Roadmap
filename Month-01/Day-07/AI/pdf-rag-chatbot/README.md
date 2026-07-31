# PDF RAG Chatbot

A chatbot that answers questions from a PDF using RAG (Retrieval Augmented Generation).

## How It Works

```
PDF → Extract Text → Chunk → Embed → Store in ChromaDB
Question → Embed → Search ChromaDB → Retrieve Context → LLM → Answer
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

Place a `sample.pdf` in this directory before running.

## Files

| File | Purpose |
|------|---------|
| app.py | Main chatbot app |
| pdf_loader.py | Extract text from PDF |
| chunking.py | Split text into chunks |
| requirements.txt | Dependencies |
