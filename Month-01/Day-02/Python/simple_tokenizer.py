import re

def tokenize(text):
    text = text.lower()
    tokens = re.findall(r'\b[a-z]+\b', text)
    return tokens

text = "Hello! This is a simple Tokenizer. It splits text into tokens."
tokens = tokenize(text)
print("Tokens:", tokens)
print("Count:", len(tokens))
