# Month 1 - Day 10

## Topics Learned
- Chain Architecture in RAG pipeline
- Paragraph splitting strategy
- Stack DSA pattern (Valid Parentheses, Min Stack)
- Interview preparation

## DSA (Java)
- Valid Parentheses — LeetCode #20
- Min Stack — LeetCode #155

## AI Project
- PDF RAG Chatbot (Chain Architecture)
  - `loader.py` — PDF extraction
  - `splitter.py` — word, sentence, paragraph splitting
  - `embedding.py` — lazy model loading
  - `vector_store.py` — ChromaDB store & search
  - `retriever.py` — retrieve with distance scores
  - `prompt_builder.py` — labeled context prompt
  - `chain.py` — LLM execution layer (NEW)
  - `rag_pipeline.py` — ingest + query orchestrator
  - `app.py` — thin entry point

## Interview Prep
- technical_questions.md — chain architecture, stack DSA
- coding_questions.md — Java & Python problems
- recruiter_notes.md — elevator pitch, projects, questions

## What I Learned
Today I introduced `chain.py` as a dedicated LLM execution layer and added paragraph splitting. The RAG pipeline is now 9 modular files — each independently testable and replaceable.

---

## Folder Structure

```
Day-10/
├── AI/
│   └── pdf-rag-chatbot/
│       ├── app.py
│       ├── loader.py
│       ├── splitter.py
│       ├── embedding.py
│       ├── vector_store.py
│       ├── retriever.py
│       ├── prompt_builder.py
│       ├── chain.py
│       ├── rag_pipeline.py
│       ├── requirements.txt
│       └── README.md
├── DSA/
│   ├── valid_parentheses.java
│   └── min_stack.java
├── Interview/
│   ├── technical_questions.md
│   ├── coding_questions.md
│   └── recruiter_notes.md
├── Notes/
│   └── day10_notes.md
├── Resources.md
└── README.md
```

## How to Run

**DSA (Java):**
```bash
javac DSA/valid_parentheses.java && java -cp DSA valid_parentheses
javac DSA/min_stack.java && java -cp DSA min_stack
```

**PDF RAG Chatbot:**
```bash
cd AI/pdf-rag-chatbot
pip install -r requirements.txt
# Add .env with GROQ_API_KEY and place sample.pdf
python app.py
```
