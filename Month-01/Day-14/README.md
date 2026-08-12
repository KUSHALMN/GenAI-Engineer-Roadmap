# Month 1 - Day 14

## Topics Learned
- Multi-document RAG — ingest all PDFs from a folder
- Sliding Window DSA pattern (fixed + variable)
- Cleaner RAG architecture — prompt built inline

## DSA (Java)
- Maximum Average Subarray I — LeetCode #643 (fixed sliding window)

## AI Project
- PDF RAG Chatbot (Multi-Document)
  - `app/main.py` — ingests all PDFs in sample_documents/
  - `app/config.py` — centralized settings
  - `app/loader.py` — PDF extraction
  - `app/splitter.py` — chunking with overlap
  - `app/embedding.py` — lazy-loaded SentenceTransformer
  - `app/vector_store.py` — ChromaDB upsert + query
  - `app/retriever.py` — store and retrieve
  - `app/rag_pipeline.py` — ingest + query with inline prompt
  - `app/source_handler.py` — load + chunk
  - `tests/test_health.py` — unit tests
  - `sample_documents/` — place PDFs here

## Interview Prep
- `technical_questions.md` — multi-doc RAG, sliding window
- `coding_questions.md` — Java & Python patterns
- `recruiter_questions.md` — project walkthrough

## What I Learned
Extended RAG to handle multiple documents — all chunks go into one ChromaDB collection, retrieval is cross-document. Sliding window reduces O(n²) subarray problems to O(n).

---

## Folder Structure

```
Day-14/
├── AI/
│   └── pdf-rag-chatbot/
│       ├── app/
│       │   ├── main.py
│       │   ├── config.py
│       │   ├── loader.py
│       │   ├── splitter.py
│       │   ├── embedding.py
│       │   ├── vector_store.py
│       │   ├── retriever.py
│       │   ├── rag_pipeline.py
│       │   └── source_handler.py
│       ├── tests/
│       │   └── test_health.py
│       ├── sample_documents/
│       ├── Dockerfile
│       ├── requirements.txt
│       ├── .env.example
│       ├── .gitignore
│       └── README.md
├── DSA/
│   └── max_average_subarray.java
├── Interview/
│   ├── technical_questions.md
│   ├── coding_questions.md
│   └── recruiter_questions.md
├── Notes/
│   └── day14_notes.md
├── Resources.md
└── README.md
```

## How to Run

**DSA (Java):**
```bash
javac DSA/max_average_subarray.java && java -cp DSA max_average_subarray
```

**RAG Chatbot:**
```bash
cd AI/pdf-rag-chatbot
pip install -r requirements.txt
cp .env.example .env  # add GROQ_API_KEY
# place PDFs in sample_documents/
python -m app.main
```

**Docker:**
```bash
docker build -t pdf-rag-chatbot .
docker run --env-file .env pdf-rag-chatbot
```

**Tests:**
```bash
pytest tests/
```
