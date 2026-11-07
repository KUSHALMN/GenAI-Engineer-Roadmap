# Day 02: Technical Interview Preparation — Instruction Datasets & HashMap Internals

### Q1: Compare Alpaca, ShareGPT, and ChatML formats for instruction tuning.
**Answer:**
- **Alpaca Format:** Flat triplet: `{"instruction": "...", "input": "...", "output": "..."}`. Best for single-turn instructions.
- **ShareGPT Format:** Array of human/gpt conversations: `{"conversations": [{"from": "human", "value": "..."}, {"from": "gpt", "value": "..."}]}`. Standard for multi-turn chats.
- **ChatML Format:** Explicit role-delimited messages: `{"messages": [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}]}`. Industry standard, preserving clear system prompt boundaries.

### Q2: What happens if two unequal Java objects produce the exact same `hashCode()`?
**Answer:**
This is a hash collision. The `HashMap` places both entries into the same bucket. When looking up an entry, the map traverses the bucket's collision chain (LinkedList or Red-Black Tree in Java 8+) and uses `key.equals()` to find the matching key. Performance degrades from $O(1)$ toward $O(n)$ if all keys collide into one bucket.
