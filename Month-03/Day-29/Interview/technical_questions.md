# Interview Questions: Production RAG APIs & Mixed Advanced DSA

### Q1: Why should an ingest endpoint be idempotent?
**Answer**:
In distributed architectures, background queue workers (Celery, Kafka, AWS SQS) guarantee *at-least-once delivery*. Network timeouts or transient crashes may cause the same document ingestion payload to be delivered multiple times. If the endpoint is not idempotent, duplicate chunks and redundant vector points are created, skewing search results. Idempotency using SHA-256 content hashes guarantees that duplicate retries result in a safe no-op.

### Q2: What is the optimal time/space complexity of House Robber (LeetCode 198)?
**Answer**:
- **Recurrence**: $dp[i] = \max(dp[i-1], dp[i-2] + nums[i])$.
- **Space Optimization**: Because computing $dp[i]$ only requires the results of the two immediately preceding houses ($dp[i-1]$ and $dp[i-2]$), we don't need a full array of size $N$. Using two scalar variables (`prev1` and `prev2`) reduces space complexity from $\mathcal{O}(N)$ to strictly $\mathcal{O}(1)$ while maintaining $\mathcal{O}(N)$ time.

### Q3: How do you design an OpenAPI contract for citation-grounded RAG responses?
**Answer**:
The response JSON schema should structure citations as an array of verified objects:
```json
{
  "answer": "string",
  "citations": [
    {
      "citation_id": 1,
      "source_document_id": "string",
      "page_number": 4,
      "chunk_id": "string",
      "relevance_score": 0.94
    }
  ],
  "usage": {"prompt_tokens": 450, "completion_tokens": 120}
}
```
This enables frontend clients to render interactive inline pill links that pop open the exact source document page when clicked.
