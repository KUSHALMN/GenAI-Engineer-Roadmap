# Month 1 - Day 8

## Topics Learned
- Refactored PDF RAG Chatbot into modular architecture
- Lazy loading pattern for ML models
- Single Responsibility Principle
- Binary Search patterns (Java)
- Interview preparation

## DSA (Java)
- Binary Search — LeetCode #704
- Search Insert Position — LeetCode #35

## AI Project
- PDF RAG Chatbot (Refactored)
  - `embedding.py` — lazy model loading
  - `vector_store.py` — ChromaDB abstraction
  - `chunking.py` — word & sentence chunking
  - `pdf_loader.py` — PDF extraction

## Interview Prep
- technical_questions.md — RAG, Python, Binary Search
- coding_questions.md — Java & Python coding problems
- hr_questions.md — HR answers and questions to ask

## What I Learned
Today I refactored the Day-07 RAG chatbot into a clean modular architecture. Each file has a single responsibility — making the codebase easier to maintain, test, and extend.

---

## Folder Structure

```
Day-08/
├── AI/
│   └── pdf-rag-chatbot/
│       ├── app.py
│       ├── pdf_loader.py
│       ├── chunking.py
│       ├── embedding.py
│       ├── vector_store.py
│       ├── requirements.txt
│       └── README.md
├── DSA/
│   ├── binary_search.java
│   └── search_insert_position.java
├── Interview/
│   ├── technical_questions.md
│   ├── coding_questions.md
│   └── hr_questions.md
├── Notes/
│   └── day8_notes.md
├── Resources.md
└── README.md
```

## How to Run

**DSA (Java):**
```bash
javac DSA/binary_search.java && java -cp DSA binary_search
javac DSA/search_insert_position.java && java -cp DSA search_insert_position
```

**PDF RAG Chatbot:**
```bash
cd AI/pdf-rag-chatbot
pip install -r requirements.txt
# Add .env with GROQ_API_KEY and place sample.pdf
python app.py
```
