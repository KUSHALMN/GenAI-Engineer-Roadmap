# Month 1 - Day 7

## Topics Learned
- Full PDF RAG Chatbot (Extract → Chunk → Embed → Retrieve → Answer)
- Python Decorators (timer, retry)
- Utility functions (flatten, batch)
- DSA — Sliding Window, Greedy
- Interview Preparation (Technical + Coding + Recruiter)

## Python
- helper_scripts.py — text cleaning, chunking, file I/O, timestamp
- utilities.py — timer decorator, retry decorator, flatten, batch

## DSA (Java)
- Longest Substring Without Repeating Characters — LeetCode #3
- Best Time to Buy and Sell Stock — LeetCode #121

## AI Project
- PDF RAG Chatbot (pypdf + ChromaDB + Sentence Transformers + Groq)

## Interview Prep
- technical_questions.md — GenAI, Python, FastAPI, SQL Q&A
- coding_questions.md — Python & Java coding problems
- recruiter_notes.md — HR answers, projects, strengths

## What I Learned
Today I built a complete PDF RAG chatbot from scratch and practiced interview questions covering everything learned in Week 1.

---

## Folder Structure

```
Day-07/
├── Python/
│   ├── helper_scripts.py
│   └── utilities.py
├── DSA/
│   ├── longest_substring.java
│   └── best_time_buy_sell_stock.java
├── AI/
│   └── pdf-rag-chatbot/
│       ├── app.py
│       ├── pdf_loader.py
│       ├── chunking.py
│       ├── requirements.txt
│       └── README.md
├── Interview/
│   ├── technical_questions.md
│   ├── coding_questions.md
│   └── recruiter_notes.md
├── Notes/
│   └── day7_notes.md
├── Resources.md
└── README.md
```

## How to Run

**Python:**
```bash
python Python/helper_scripts.py
python Python/utilities.py
```

**DSA (Java):**
```bash
javac DSA/longest_substring.java && java -cp DSA longest_substring
javac DSA/best_time_buy_sell_stock.java && java -cp DSA best_time_buy_sell_stock
```

**PDF RAG Chatbot:**
```bash
cd AI/pdf-rag-chatbot
pip install -r requirements.txt
# Add .env with GROQ_API_KEY and place sample.pdf
python app.py
```
