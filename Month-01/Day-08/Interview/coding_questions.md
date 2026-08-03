# Coding Questions — Day 08

## Q1: Implement Binary Search (Java)
```java
public int binarySearch(int[] nums, int target) {
    int left = 0, right = nums.length - 1;
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (nums[mid] == target) return mid;
        else if (nums[mid] < target) left = mid + 1;
        else right = mid - 1;
    }
    return -1;
}
```

## Q2: Lazy Singleton Pattern (Python)
```python
_model = None

def get_model():
    global _model
    if _model is None:
        _model = load_heavy_model()
    return _model
```

## Q3: Chunk Text with Overlap (Python)
```python
def chunk_text(text, chunk_size=200, overlap=30):
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunks.append(" ".join(words[i:i + chunk_size]))
        i += chunk_size - overlap
    return chunks
```

## Q4: Search Insert Position (Java)
```java
public int searchInsert(int[] nums, int target) {
    int left = 0, right = nums.length - 1;
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (nums[mid] == target) return mid;
        else if (nums[mid] < target) left = mid + 1;
        else right = mid - 1;
    }
    return left; // insert position
}
```

## Q5: Read and Process a PDF (Python)
```python
from pypdf import PdfReader

def load_pdf(filepath):
    reader = PdfReader(filepath)
    return "\n".join(page.extract_text() or "" for page in reader.pages)
```

## Q6: Cosine Similarity from Scratch (Python)
```python
import math

def cosine_similarity(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    mag_a = math.sqrt(sum(x**2 for x in a))
    mag_b = math.sqrt(sum(x**2 for x in b))
    return dot / (mag_a * mag_b) if mag_a and mag_b else 0.0
```
