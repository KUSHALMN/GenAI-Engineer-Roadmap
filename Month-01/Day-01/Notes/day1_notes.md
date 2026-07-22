# Day 1 Notes — GenAI Engineer Roadmap

## Topics Learned

### AI / Theory
- **Artificial Intelligence** — machines simulating human intelligence
- **Machine Learning** — systems that learn from data without being explicitly programmed
- **Deep Learning** — ML using neural networks with many layers
- **Generative AI** — AI that generates new content (text, images, code)
- **LLM Basics** — Large Language Models trained on massive text data
- **Transformers** — architecture behind modern LLMs (attention mechanism)

---

## Python Practice

### Word Counter
- Used dictionary to count word frequency
- `.split()` to tokenize, `.get()` with default for counting

### Student Management
- Dictionary as a simple in-memory database
- CRUD: add, view, delete students

### Bank Account
- OOP: class with `__init__`, methods for deposit/withdraw
- Encapsulation of balance logic

---

## DSA (Java)

### Two Sum — LeetCode #1
- Approach: HashMap O(n)
- Store complement → index, check if current number exists in map

### Contains Duplicate — LeetCode #217
- Approach: HashSet O(n)
- If `set.add()` returns false → duplicate found

### Valid Anagram — LeetCode #242
- Approach: Frequency Count O(n)
- Count chars in s, decrement for t, check all zero

---

## AI Project — Terminal Chatbot
- Used **Groq API** with **LLaMA 3.3 70B**
- Maintains conversation history in a list
- `.env` file for secure API key storage

---

## Key Takeaway
Today I learned how an LLM processes a prompt end-to-end — from tokenization to attention mechanisms to output generation — while also revisiting Python fundamentals and solving beginner DSA problems.
