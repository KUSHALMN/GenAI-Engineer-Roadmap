# Recruiter Questions — Day 13

**Q: Tell me about your RAG project.**
Built a fully modular, Dockerized PDF RAG chatbot in Python. Each component — loading, chunking, embedding, retrieval, prompt building — is a separate module. Includes pytest tests and Docker support for production deployment.

**Q: What is Docker and why use it?**
Docker packages the app and all its dependencies into a container. Runs the same way on any machine — dev, staging, or production.

**Q: What testing have you done?**
Written pytest unit tests for core modules — splitter and prompt builder. Tests verify chunking logic and prompt structure without needing an LLM or database.

**Q: What's the hardest DSA problem you solved?**
Largest Rectangle in Histogram — uses a monotonic increasing stack. The key insight is that for each bar popped, the width extends back to the previous smaller bar. O(n) time despite looking like O(n²).
