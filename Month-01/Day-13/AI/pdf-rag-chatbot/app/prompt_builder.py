def build_prompt(query: str, chunks: list[str]) -> str:
    context = "\n\n".join(f"[{i+1}] {c}" for i, c in enumerate(chunks))
    return f"""You are a helpful assistant. Answer using only the context below.

Context:
{context}

Question: {query}
Answer:"""
