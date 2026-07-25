# Month 1 - Day 4

## Topics Learned
- Prompt Engineering (Zero-shot, Few-shot, Chain-of-Thought, System Role)
- Multi-turn Chat with Groq API
- Conversation History Management
- Binary Search Pattern

## Python
- Groq Chat (multi-turn conversation with history)
- Prompt Examples (4 prompting techniques)

## DSA (Java)
- Binary Search — LeetCode #704
- Search Insert Position — LeetCode #35
- First Bad Version — LeetCode #278

## AI Project
- AI Q&A Bot with system prompt and conversation history (Groq + LLaMA 3.3 70B)

## What I Learned
Today I mastered prompt engineering techniques and how to maintain conversation history for multi-turn LLM interactions. On the DSA side, I learned the binary search template that applies to all search-on-sorted-array problems.

---

## Folder Structure

```
Day-04/
├── Python/
│   ├── groq_chat.py
│   └── prompt_examples.py
├── DSA/
│   ├── binary_search.java
│   ├── search_insert_position.java
│   └── first_bad_version.java
├── AI/
│   ├── ai_qa_bot.py
│   └── requirements.txt
├── Notes/
│   └── day4_notes.md
├── Resources.md
└── README.md
```

## How to Run

**Python:**
```bash
# Create .env with: GROQ_API_KEY=your_key_here
python Python/groq_chat.py
python Python/prompt_examples.py
```

**DSA (Java):**
```bash
javac DSA/binary_search.java && java -cp DSA binary_search
javac DSA/search_insert_position.java && java -cp DSA search_insert_position
javac DSA/first_bad_version.java && java -cp DSA first_bad_version
```

**AI Project:**
```bash
cd AI
pip install -r requirements.txt
# Create .env with: GROQ_API_KEY=your_key_here
python ai_qa_bot.py
```
