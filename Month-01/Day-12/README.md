# Month 1 - Day 12

## Topics Learned
- Stack DSA — Valid Parentheses, Daily Temperatures, Evaluate RPN
- Monotonic Stack pattern
- Advanced RAG Pipeline with source_handler, retriever, prompt_builder

## DSA (Java)
- Valid Parentheses — LeetCode #20
- Daily Temperatures — LeetCode #739
- Evaluate Reverse Polish Notation — LeetCode #150

## AI Project
- PDF RAG Chatbot (Modular)
  - `config.py` — centralized settings
  - `source_handler.py` — PDF loading and chunking
  - `retriever.py` — ChromaDB store and semantic search
  - `prompt_builder.py` — context-aware prompt formatting
  - `rag_pipeline.py` — ingest + query orchestrator
  - `app.py` — entry point

## Interview Prep
- `technical_questions.md` — Stack DSA, RAG concepts
- `coding_questions.md` — Java & Python code patterns
- `recruiter_questions.md` — elevator pitch, project walkthrough

## What I Learned
Monotonic stack is the key pattern for "next greater element" problems. RAG pipeline is now fully modular — each file has a single responsibility.

---

## Folder Structure

```
Day-12/
├── AI/
│   └── pdf-rag-chatbot/
│       ├── app.py
│       ├── config.py
│       ├── source_handler.py
│       ├── retriever.py
│       ├── prompt_builder.py
│       ├── rag_pipeline.py
│       ├── requirements.txt
│       └── README.md
├── DSA/
│   ├── valid_parentheses.java
│   ├── daily_temperatures.java
│   └── evaluate_rpn.java
├── Interview/
│   ├── technical_questions.md
│   ├── coding_questions.md
│   └── recruiter_questions.md
├── Notes/
│   └── day12_notes.md
├── Resources.md
└── README.md
```

## How to Run

**DSA (Java):**
```bash
javac DSA/valid_parentheses.java && java -cp DSA valid_parentheses
javac DSA/daily_temperatures.java && java -cp DSA daily_temperatures
javac DSA/evaluate_rpn.java && java -cp DSA evaluate_rpn
```

**PDF RAG Chatbot:**
```bash
cd AI/pdf-rag-chatbot
pip install -r requirements.txt
# Add .env with GROQ_API_KEY and place sample.pdf
python app.py
```
