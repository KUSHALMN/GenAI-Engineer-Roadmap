# Month 1 - Day 11

## Topics Learned
- Config-driven architecture with `config.py`
- Centralized settings — no hardcoded values
- Queue DSA pattern (Stack-based Queue, Sliding Window Queue)

## DSA (Java)
- Implement Queue using Stacks — LeetCode #232
- Number of Recent Calls — LeetCode #933

## AI Project
- PDF RAG Chatbot (Config-Driven)
  - `config.py` — centralized settings (NEW)
  - `loader.py` — PDF extraction
  - `splitter.py` — word, sentence, paragraph splitting
  - `embedding.py` — lazy model loading
  - `vector_store.py` — ChromaDB store & search
  - `retriever.py` — retrieve with distance scores
  - `prompt_builder.py` — labeled context prompt
  - `chain.py` — LLM execution layer
  - `rag_pipeline.py` — ingest + query orchestrator
  - `app.py` — thin entry point

## Interview Prep
- technical_questions.md — config pattern, Queue DSA
- coding_questions.md — Java & Python problems
- recruiter_notes.md — elevator pitch, production-ready highlights

## What I Learned
Today I introduced `config.py` to centralize all settings. The RAG chatbot is now fully config-driven — change any setting in one place and it propagates everywhere.

---

## Folder Structure

```
Day-11/
├── AI/
│   └── pdf-rag-chatbot/
│       ├── app.py
│       ├── config.py
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
│   ├── implement_queue_using_stacks.java
│   └── number_of_recent_calls.java
├── Interview/
│   ├── technical_questions.md
│   ├── coding_questions.md
│   └── recruiter_notes.md
├── Notes/
│   └── day11_notes.md
├── Resources.md
└── README.md
```

## How to Run

**DSA (Java):**
```bash
javac DSA/implement_queue_using_stacks.java && java -cp DSA implement_queue_using_stacks
javac DSA/number_of_recent_calls.java && java -cp DSA number_of_recent_calls
```

**PDF RAG Chatbot:**
```bash
cd AI/pdf-rag-chatbot
pip install -r requirements.txt
# Add .env with GROQ_API_KEY and place sample.pdf
python app.py
```
