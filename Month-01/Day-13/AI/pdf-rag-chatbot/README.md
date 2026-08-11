# PDF RAG Chatbot — Day 13

Fully modular, Dockerized RAG chatbot with tests.

## Architecture

```
PDF → loader → splitter → embedding → vector_store (ChromaDB)
Query → retriever → prompt_builder → Groq LLM → Answer
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
├── tests/
│   └── test_health.py
├── Dockerfile
├── requirements.txt
├── .env.example
└── README.md
```

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env  # add your GROQ_API_KEY
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
