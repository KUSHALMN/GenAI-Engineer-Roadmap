# 📄 PDF RAG Chatbot

An advanced, production-grade **Retrieval-Augmented Generation (RAG)** chatbot engineered with **Hybrid Search (Dense Semantic Embeddings + Sparse BM25)**, **Reciprocal Rank Fusion (RRF)**, **Cross-Encoder Reranking**, and an automated evaluation suite.

---

## 🏗️ Architecture & Flow

```
PDF / Document
      │
      ▼
[1. Document Loader (app/loader.py)]
      │
      ▼
[2. Recursive Text Splitter (app/splitter.py)]
      │
      ├───► [Semantic Index] (app/embedding.py & retrieval/semantic_retriever.py)
      └───► [BM25 Keyword Index] (retrieval/keyword_retriever.py)
                  │
                  ▼
          [User Query]
                  │
                  ├───► Semantic Cosine Search (Top 2k)
                  └───► BM25 Keyword Search (Top 2k)
                              │
                              ▼
            [3. Hybrid RRF Fusion (retrieval/hybrid_retriever.py)]
                              │
                              ▼
            [4. Cross-Encoder Reranker (retrieval/reranker.py)]
                              │
                              ▼
            [5. Grounded Prompt Builder (app/prompt_builder.py)]
                              │
                              ▼
            [6. Groq LLaMA 3.3 Generation (app/rag_pipeline.py)]
                              │
                              ▼
                        [Answer + Citations]
```

---

## 📁 Project Structure

```
pdf-rag-chatbot/
│
├── app/
│   ├── __init__.py
│   ├── config.py              # Environment configuration & paths
│   ├── loader.py              # PDF and document parser
│   ├── splitter.py            # Recursive character chunker
│   ├── embedding.py           # Dense embeddings & cosine similarity
│   ├── vector_store.py        # In-memory vector database
│   ├── prompt_builder.py      # Grounded prompt template constructor
│   ├── source_handler.py      # Citation management & snippets
│   ├── rag_pipeline.py        # End-to-end RAG orchestrator
│   └── main.py                # FastAPI REST API & CLI runner
│
├── retrieval/
│   ├── __init__.py
│   ├── semantic_retriever.py  # Vector cosine similarity retriever
│   ├── keyword_retriever.py   # BM25 keyword frequency retriever
│   ├── hybrid_retriever.py    # Reciprocal Rank Fusion (RRF)
│   └── reranker.py            # Cross-scoring precision reranker
│
├── evaluation/
│   ├── questions.json         # Benchmark evaluation test cases
│   ├── evaluate.py            # Automated evaluation runner (MRR, Recall, Latency)
│   └── results.json           # Output evaluation benchmark results
│
├── tests/
│   ├── __init__.py
│   └── test_rag.py            # Unit test suite
│
├── requirements.txt           # Project dependencies
├── Dockerfile                 # Container setup
├── .env.example               # Environment variables template
├── .gitignore
└── README.md
```

---

## 🚀 Quick Start

### 1. Installation & Environment

```bash
cd pdf-rag-chatbot
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

### 2. Run CLI Test

```bash
python -m app.main
```

### 3. Start FastAPI Server

```bash
uvicorn app.main:app --reload --port 8000
```
Interactive Swagger API docs available at: `http://localhost:8000/docs`

---

## 📡 API Endpoints

- `GET /health` : System health check and model status
- `POST /upload-pdf` : Upload and ingest PDF document into hybrid vector store
- `POST /index-text` : Index raw text snippets
- `POST /query` : Query the RAG engine (`retriever_type`: `hybrid` | `semantic` | `keyword`, `use_reranker`: `true`)
- `POST /ask` : Simplified context Q&A endpoint
- `POST /clear` : Reset indexed documents

Example Query Request:
```json
{
  "question": "What is hybrid search and how does RRF combine ranks?",
  "retriever_type": "hybrid",
  "top_k": 4,
  "use_reranker": true
}
```

---

## 📊 Evaluation Benchmark

Run the automated evaluation benchmark:
```bash
python evaluation/evaluate.py
```
Outputs precision, recall, MRR, and latency metrics to `evaluation/results.json`.

---

## 🧪 Running Tests

```bash
python -m unittest tests/test_rag.py
```
