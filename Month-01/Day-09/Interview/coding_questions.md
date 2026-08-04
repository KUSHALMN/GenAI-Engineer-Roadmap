# Coding Questions — Day 09

## Q1: Valid Palindrome (Java)
```java
public boolean isPalindrome(String s) {
    int left = 0, right = s.length() - 1;
    while (left < right) {
        while (left < right && !Character.isLetterOrDigit(s.charAt(left))) left++;
        while (left < right && !Character.isLetterOrDigit(s.charAt(right))) right--;
        if (Character.toLowerCase(s.charAt(left)) != Character.toLowerCase(s.charAt(right)))
            return false;
        left++; right--;
    }
    return true;
}
```

## Q2: Merge Sorted Array (Java)
```java
public void merge(int[] nums1, int m, int[] nums2, int n) {
    int p1 = m - 1, p2 = n - 1, p = m + n - 1;
    while (p2 >= 0) {
        if (p1 >= 0 && nums1[p1] > nums2[p2]) nums1[p--] = nums1[p1--];
        else nums1[p--] = nums2[p2--];
    }
}
```

## Q3: Build RAG Prompt (Python)
```python
def build_prompt(question, context_chunks):
    context = "\n\n".join(f"[Chunk {i+1}]: {c}" for i, c in enumerate(context_chunks))
    return [
        {"role": "system", "content": "Answer using only the context provided."},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
    ]
```

## Q4: Retrieve with Scores (Python)
```python
results = collection.query(
    query_embeddings=[embed_query(query)],
    n_results=3,
    include=["documents", "distances"]
)
chunks = results["documents"][0]
distances = results["distances"][0]
```

## Q5: Check Palindrome (Python)
```python
def is_palindrome(s):
    s = ''.join(c.lower() for c in s if c.isalnum())
    return s == s[::-1]
```

## Q6: Merge Two Sorted Lists (Python)
```python
def merge_sorted(a, b):
    result = []
    i = j = 0
    while i < len(a) and j < len(b):
        if a[i] <= b[j]: result.append(a[i]); i += 1
        else: result.append(b[j]); j += 1
    return result + a[i:] + b[j:]
```
