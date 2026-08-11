# Month 1 - Day 13

## Topics Learned
- Dockerized modular RAG chatbot with app/ package structure
- pytest unit testing for RAG modules
- Hard Stack DSA — Largest Rectangle in Histogram

## DSA (Java)
- Valid Parentheses — LeetCode #20
- Daily Temperatures — LeetCode #739
- Largest Rectangle in Histogram — LeetCode #84

## AI Project
- PDF RAG Chatbot (Dockerized + Tested)
  - `app/config.py` — centralized settings
  - `app/loader.py` — PDF extraction
  - `app/splitter.py` — chunking with overlap
  - `app/embedding.py` — lazy-loaded model
  - `app/vector_store.py` — ChromaDB operations
  - `app/retriever.py` — store and retrieve
  - `app/prompt_builder.py` — prompt formatting
  - `app/rag_pipeline.py` — orchestrator
  - `app/source_handler.py` — load + chunk
  - `app/main.py` — entry point
  - `tests/test_health.py` — unit tests
  - `Dockerfile` — containerized deployment

## Interview Prep
- `technical_questions.md` — Docker, Stack DSA, RAG
- `coding_questions.md` — Java & Python patterns
- `recruiter_questions.md` — project walkthrough

## What I Learned
Refactored RAG chatbot into a proper Python package with app/ structure. Added Docker for portability and pytest for reliability. Solved Largest Rectangle — hardest stack problem.

---

## Folder Structure

```
Day-13/
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
│       │   ├── prompt_builder.py
│       │   ├── rag_pipeline.py
│       │   └── source_handler.py
│       ├── tests/
│       │   └── test_health.py
│       ├── Dockerfile
│       ├── requirements.txt
│       ├── .env.example
│       └── README.md
├── DSA/
│   ├── valid_parentheses.java
│   ├── daily_temperatures.java
│   └── largest_rectangle.java
├── Interview/
│   ├── technical_questions.md
│   ├── coding_questions.md
│   └── recruiter_questions.md
├── Notes/
│   └── day13_notes.md
├── Resources.md
└── README.md
```

## How to Run

**DSA (Java):**
```bash
javac DSA/largest_rectangle.java && java -cp DSA largest_rectangle
```

**RAG Chatbot:**
```bash
cd AI/pdf-rag-chatbot
pip install -r requirements.txt
cp .env.example .env  # add GROQ_API_KEY
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
