# Month 1 - Day 3

## Topics Learned
- RAG (Retrieval Augmented Generation) Pipeline
- Text Chunking with Overlap
- Cosine Similarity from Scratch
- PDF Processing with pypdf
- Semantic Search with ChromaDB

## Python
- Chunk Text (with overlap)
- Cosine Similarity (manual implementation)

## DSA (Java)
- Best Time to Buy and Sell Stock — LeetCode #121
- Longest Common Prefix — LeetCode #14
- Longest Substring Without Repeating Characters — LeetCode #3

## AI Project
- PDF Similarity Search (pypdf + ChromaDB + Sentence Transformers)

## What I Learned
Today I built a mini RAG pipeline — chunking text, embedding it, storing in ChromaDB, and retrieving by semantic similarity. Also implemented cosine similarity from scratch to understand how vector comparison works under the hood.

---

## Folder Structure

```
Day-03/
├── Python/
│   ├── chunk_text.py
│   └── cosine_similarity.py
├── DSA/
│   ├── best_time_to_buy_stock.java
│   ├── longest_common_prefix.java
│   └── longest_substring.java
├── AI/
│   ├── pdf_similarity_search.py
│   └── requirements.txt
├── Notes/
│   └── day3_notes.md
├── Resources.md
└── README.md
```

## How to Run

**Python:**
```bash
python Python/chunk_text.py
python Python/cosine_similarity.py
```

**DSA (Java):**
```bash
javac DSA/best_time_to_buy_stock.java && java -cp DSA best_time_to_buy_stock
javac DSA/longest_common_prefix.java && java -cp DSA longest_common_prefix
javac DSA/longest_substring.java && java -cp DSA longest_substring
```

**AI Project:**
```bash
cd AI
pip install -r requirements.txt
python pdf_similarity_search.py
```
