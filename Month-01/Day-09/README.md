# Month 1 - Day 9

## Topics Learned
- Full Modular RAG Pipeline (8 dedicated modules)
- Retriever with distance scores
- Prompt builder with labeled chunks
- RAG pipeline orchestrator
- Two Pointers DSA pattern

## DSA (Java)
- Valid Palindrome — LeetCode #125
- Merge Sorted Array — LeetCode #88

## AI Project
- PDF RAG Chatbot (Full Pipeline)
  - `pdf_loader.py` — PDF extraction
  - `chunking.py` — word & sentence chunking
  - `embedding.py` — lazy model loading
  - `vector_store.py` — ChromaDB store & search
  - `retriever.py` — retrieve with distance scores
  - `prompt_builder.py` — labeled context prompt
  - `rag_pipeline.py` — ingest + query orchestrator
  - `app.py` — thin entry point

## Interview Prep
- technical_questions.md — RAG architecture, Two Pointers
- coding_questions.md — Java & Python problems
- hr_questions.md — HR answers and questions to ask

## What I Learned
Today I built the most complete version of the RAG pipeline — fully modular with 8 focused files. Each module has a single responsibility, making the system production-ready.

---

## Folder Structure

```
Day-09/
├── AI/
│   └── pdf-rag-chatbot/
│       ├── app.py
│       ├── pdf_loader.py
│       ├── chunking.py
│       ├── embedding.py
│       ├── vector_store.py
│       ├── retriever.py
│       ├── prompt_builder.py
│       ├── rag_pipeline.py
│       ├── requirements.txt
│       └── README.md
├── DSA/
│   ├── valid_palindrome.java
│   └── merge_sorted_array.java
├── Interview/
│   ├── technical_questions.md
│   ├── coding_questions.md
│   └── hr_questions.md
├── Notes/
│   └── day9_notes.md
├── Resources.md
└── README.md
```

## How to Run

**DSA (Java):**
```bash
javac DSA/valid_palindrome.java && java -cp DSA valid_palindrome
javac DSA/merge_sorted_array.java && java -cp DSA merge_sorted_array
```

**PDF RAG Chatbot:**
```bash
cd AI/pdf-rag-chatbot
pip install -r requirements.txt
# Add .env with GROQ_API_KEY and place sample.pdf
python app.py
```
