# Recruiter Questions — Day 14

**Q: What did you build today?**
Extended the RAG chatbot to support multiple PDFs — it now ingests all documents from a folder and answers questions across all of them using semantic search and Groq LLM.

**Q: How does your RAG chatbot handle multiple documents?**
All PDFs are chunked and stored in the same ChromaDB vector store. When a question is asked, the retriever finds the most relevant chunks across all documents regardless of source.

**Q: What is sliding window and where is it used?**
A technique to process contiguous subarrays/substrings in O(n) instead of O(n²). Used in problems like maximum average subarray, longest substring without repeating characters, and minimum window substring.

**Q: How do you ensure no duplicate chunks in ChromaDB?**
Using `upsert` instead of `add` — it inserts new chunks and updates existing ones based on ID, so re-running ingestion doesn't create duplicates.
