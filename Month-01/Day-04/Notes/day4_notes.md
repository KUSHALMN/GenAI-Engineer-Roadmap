# Day 4 Notes — GenAI Engineer Roadmap

## Topics Learned

### Prompt Engineering
- **Zero-Shot** — ask the model directly without examples
- **Few-Shot** — provide examples before the actual question
- **Chain-of-Thought** — ask the model to think step by step
- **System Role** — set model behavior via system message
- **Prompt = Instruction + Context + Input + Output format**

---

## Python Practice

### Groq Chat
- Built a multi-turn chat using Groq API
- Maintained conversation `history` as a list of messages
- Each turn appends user + assistant messages to history

### Prompt Examples
- Demonstrated 4 prompting techniques with Groq API
- Zero-shot, few-shot, chain-of-thought, system role

---

## DSA (Java)

### Binary Search — LeetCode #704
- Approach: Binary Search O(log n)
- `mid = left + (right - left) / 2` avoids integer overflow
- Return -1 if not found

### Search Insert Position — LeetCode #35
- Approach: Binary Search O(log n)
- Same as binary search, but return `left` when not found
- `left` naturally lands at the correct insert position

### First Bad Version — LeetCode #278
- Approach: Binary Search O(log n)
- Use `right = mid` (not mid-1) to avoid skipping the first bad version
- `left < right` condition ensures we converge to one answer

---

## AI Project — Q&A Bot

- Added system prompt to control AI behavior
- Maintained conversation history for multi-turn Q&A
- Model: LLaMA 3.3 70B via Groq API

---

## Key Takeaway
Prompt engineering is how you communicate intent to an LLM. Binary search is the foundation of all search algorithms — master it before moving on.
