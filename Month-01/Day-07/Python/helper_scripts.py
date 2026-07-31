import os
import re
from datetime import datetime

def clean_text(text):
    text = text.lower().strip()
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s]', '', text)
    return text

def chunk_text(text, chunk_size=200, overlap=30):
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunks.append(" ".join(words[i:i + chunk_size]))
        i += chunk_size - overlap
    return chunks

def save_to_file(content, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Saved to {filename}")

def load_from_file(filename):
    if not os.path.exists(filename):
        raise FileNotFoundError(f"{filename} not found")
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Test
if __name__ == "__main__":
    text = "  Hello,   World!  This is a TEST.  "
    print(clean_text(text))
    print(timestamp())
