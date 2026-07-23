# Day 2 Notes — GenAI Engineer Roadmap

## Topics Learned

### NLP / Text Processing
- **Tokenization** — splitting text into words/tokens
- **Word Frequency** — counting how often each word appears
- **Stop Words** — common words (the, is, a) that carry little meaning
- **Text File I/O** — reading and processing raw text files in Python

---

## Python Practice

### Simple Tokenizer
- Used `.split()` and `re` module to tokenize text
- Lowercased and stripped punctuation before splitting

### Word Frequency
- Used `collections.Counter` to count word occurrences
- `.most_common(n)` to get top N frequent words

### Remove Stopwords
- Defined a custom stopword set
- Filtered tokens using list comprehension

### Text File Reader
- Used `open()` with context manager to read `.txt` files
- Processed line by line for memory efficiency

---

## DSA (Java)

### Valid Palindrome — LeetCode #125
- Approach: Two Pointers O(n)
- Skip non-alphanumeric, compare chars from both ends

### Ransom Note — LeetCode #383
- Approach: HashMap frequency count O(n)
- Count magazine chars, decrement for ransom note

### Isomorphic Strings — LeetCode #205
- Approach: Two HashMaps O(n)
- Map s→t and t→s, check consistency

### Longest Substring Without Repeating — LeetCode #3
- Approach: Sliding Window + HashSet O(n)
- Expand right, shrink left when duplicate found

---

## AI — Embeddings & Vector Search

### Embeddings Demo
- Used `sentence-transformers` to generate text embeddings
- Embeddings are dense vectors representing semantic meaning

### Similarity Checker
- Used cosine similarity to compare two text embeddings
- Higher score = more semantically similar

### ChromaDB Demo
- Set up a local vector store with ChromaDB
- Added documents, queried by semantic similarity

---

## Key Takeaway
Text is just numbers to an AI — tokenization and embeddings are how raw text becomes something a model can understand and compare.
