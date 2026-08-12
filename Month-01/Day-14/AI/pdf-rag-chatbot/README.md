# PDF RAG Chatbot — Day 14

Multi-document RAG chatbot. Ingests all PDFs from `sample_documents/` and answers questions using Groq LLM.

## Structure

```
pdf-rag-chatbot/
├── app/
│   ├── main.py           ← entry point, ingests all PDFs
│   ├── config.py         ← all settings
│   ├── loader.py         ← PDF text extraction
│   ├── splitter.py       ← chunk with overlap
│   ├── embedding.py      ← lazy-loaded SentenceTransformer
│   ├── vector_store.py   ← ChromaDB upsert + query
│   ├── retriever.py      ← store and retrieve chunks
│   ├── rag_pipeline.py   ← ingest + query orchestrator
│   └── source_handler.py ← load + chunk in one call
├── tests/
│   └── test_health.py
├── sample_documents/     ← place your PDFs here
├── Dockerfile
├── requirements.txt
├── .env.example
└── README.md
```

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env  # add GROQ_API_KEY
# place PDFs in sample_documents/
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
