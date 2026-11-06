# Day 28: Technical Interview Preparation — Agent Platform System Design

### Q1: Design a distributed agent execution platform handling 100,000 asynchronous agent tasks daily.
**Answer:**
1. **API Gateway & Rate Limiter:** Authenticates tenant JWTs, validates quotas, and writes tasks to Kafka/RabbitMQ.
2. **Distributed State Store:** Redis for hot ephemeral working memory; PostgreSQL for cold durable checkpoints.
3. **Stateless Worker Pool:** Horizontal Auto-scaling Kubernetes pods consume tasks from queue, invoke models, and dispatch tools.
4. **Tool Gateway & MCP Host:** Manages pooled persistent connections to local/remote MCP servers with circuit breakers and audit logging.

### Q2: How does Trie node pruning prevent unnecessary traversals in Word Search II?
**Answer:**
When a leaf word is found and added to the results, setting `p.word = null` prevents adding duplicates. Furthermore, if a node has no other children, it can be pruned from its parent, preventing subsequent DFS branches from revisiting exhausted prefixes.
