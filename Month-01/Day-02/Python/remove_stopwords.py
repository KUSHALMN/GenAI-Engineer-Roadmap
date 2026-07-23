import re

STOPWORDS = {"the", "is", "a", "an", "on", "in", "at", "it", "and", "or", "to", "of", "for"}

def remove_stopwords(text):
    words = re.findall(r'\b[a-z]+\b', text.lower())
    return [w for w in words if w not in STOPWORDS]

text = "The cat is sitting on a mat and it is very comfortable"
filtered = remove_stopwords(text)
print("Filtered tokens:", filtered)
