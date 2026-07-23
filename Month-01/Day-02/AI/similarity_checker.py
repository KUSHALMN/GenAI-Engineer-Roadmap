from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

pairs = [
    ("I love machine learning", "Deep learning is a subset of ML"),
    ("I love machine learning", "I enjoy playing football"),
]

for s1, s2 in pairs:
    e1 = model.encode(s1, convert_to_tensor=True)
    e2 = model.encode(s2, convert_to_tensor=True)
    score = util.cos_sim(e1, e2).item()
    print(f"\n'{s1}'\nvs\n'{s2}'\nSimilarity: {score:.4f}")
