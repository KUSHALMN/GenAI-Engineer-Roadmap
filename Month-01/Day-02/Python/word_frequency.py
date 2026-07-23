from collections import Counter
import re

def word_frequency(text, top_n=5):
    words = re.findall(r'\b[a-z]+\b', text.lower())
    freq = Counter(words)
    return freq.most_common(top_n)

text = "the cat sat on the mat the cat is on the mat"
print("Top words:", word_frequency(text))
