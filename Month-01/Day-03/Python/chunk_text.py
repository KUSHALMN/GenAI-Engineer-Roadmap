def chunk_text(text, chunk_size=100, overlap=20):
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
        i += chunk_size - overlap
    return chunks

text = """Retrieval Augmented Generation (RAG) is a technique that combines information retrieval
with text generation. Instead of relying solely on the model's training data, RAG fetches
relevant documents from an external knowledge base and uses them as context for generating answers.
This makes responses more accurate, up-to-date, and grounded in real information."""

chunks = chunk_text(text, chunk_size=20, overlap=5)
for i, chunk in enumerate(chunks):
    print(f"Chunk {i+1}: {chunk}\n")
