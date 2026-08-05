SYSTEM_PROMPT = """You are a helpful assistant that answers questions based on the provided context.
If the answer is not in the context, say 'I don't know' instead of making something up.
Be concise and accurate."""

def build_prompt(question: str, context_chunks: list[str]) -> list[dict]:
    context = "\n\n".join(
        f"[Chunk {i+1}]: {chunk}"
        for i, chunk in enumerate(context_chunks)
    )
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
    ]
