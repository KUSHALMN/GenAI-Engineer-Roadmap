from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

sentences = [
    "Artificial intelligence is transforming industries.",
    "Machine learning helps computers learn from data.",
    "I love eating pizza on weekends."
]

embeddings = model.encode(sentences)

for i, sentence in enumerate(sentences):
    print(f"\nSentence: {sentence}")
    print(f"Embedding shape: {embeddings[i].shape}")
    print(f"First 5 values: {embeddings[i][:5]}")
