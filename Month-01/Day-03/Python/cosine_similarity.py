import math

def dot_product(a, b):
    return sum(x * y for x, y in zip(a, b))

def magnitude(a):
    return math.sqrt(sum(x ** 2 for x in a))

def cosine_similarity(a, b):
    if magnitude(a) == 0 or magnitude(b) == 0:
        return 0.0
    return dot_product(a, b) / (magnitude(a) * magnitude(b))

# Example: simple word vectors (bag of words)
# Vocabulary: [AI, learning, python, food, pizza]
vec1 = [1, 1, 1, 0, 0]  # "AI learning python"
vec2 = [1, 1, 0, 0, 0]  # "AI learning"
vec3 = [0, 0, 0, 1, 1]  # "food pizza"

print(f"vec1 vs vec2: {cosine_similarity(vec1, vec2):.4f}")  # high similarity
print(f"vec1 vs vec3: {cosine_similarity(vec1, vec3):.4f}")  # low similarity
