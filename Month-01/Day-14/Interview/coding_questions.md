# Coding Questions — Day 14

## Java — Sliding Window

### Maximum Average Subarray I (Easy)
```java
// Fixed window of size k
double sum = 0;
for (int i = 0; i < k; i++) sum += nums[i];
double maxSum = sum;
for (int i = k; i < nums.length; i++) {
    sum += nums[i] - nums[i - k];  // slide: add right, remove left
    maxSum = Math.max(maxSum, sum);
}
return maxSum / k;
```

## Python — Multi-Document Ingestion

### Ingest all PDFs in a folder
```python
for filename in os.listdir("sample_documents"):
    if filename.endswith(".pdf"):
        ingest(os.path.join("sample_documents", filename))
```

### Why use upsert instead of add in ChromaDB?
```python
# upsert = insert if not exists, update if exists
# prevents duplicate chunks on re-run
col.upsert(documents=chunks, embeddings=embeddings, ids=ids)
```
