def chunk_by_words(text: str, chunk_size: int = 200, overlap: int = 30) -> list[str]:
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk.strip():
            chunks.append(chunk)
        i += chunk_size - overlap
    return chunks

def chunk_by_sentences(text: str, sentences_per_chunk: int = 5) -> list[str]:
    import re
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    chunks = []
    for i in range(0, len(sentences), sentences_per_chunk):
        chunk = " ".join(sentences[i:i + sentences_per_chunk])
        if chunk.strip():
            chunks.append(chunk)
    return chunks

if __name__ == "__main__":
    sample = "This is sentence one. This is sentence two. This is sentence three. " * 5
    word_chunks = chunk_by_words(sample, chunk_size=20, overlap=5)
    sent_chunks = chunk_by_sentences(sample, sentences_per_chunk=3)
    print(f"Word chunks: {len(word_chunks)}")
    print(f"Sentence chunks: {len(sent_chunks)}")
    print(f"\nFirst word chunk:\n{word_chunks[0]}")
    print(f"\nFirst sentence chunk:\n{sent_chunks[0]}")
