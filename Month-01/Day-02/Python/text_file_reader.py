import re
from collections import Counter

def read_and_analyze(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    words = re.findall(r'\b[a-z]+\b', text.lower())
    print(f"Total words: {len(words)}")
    print(f"Unique words: {len(set(words))}")
    print(f"Top 5: {Counter(words).most_common(5)}")

# Usage: read_and_analyze("sample.txt")
# Create a sample.txt to test
with open("sample.txt", "w") as f:
    f.write("Generative AI is transforming the world. AI models learn from data. Data is the new oil.")

read_and_analyze("sample.txt")
