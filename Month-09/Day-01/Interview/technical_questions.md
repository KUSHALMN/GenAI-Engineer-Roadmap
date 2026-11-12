# 🎯 Technical Interview Questions — Day 01: Tokenizer Pretraining & 0/1 Knapsack

## Question 1: Why did modern LLMs (GPT-4, Llama 3) transition to Byte-level BPE with 100k+ vocabularies instead of WordPiece or character-level tokenization?
**Answer:**
1. **Zero Out-of-Vocabulary (OOV) Guarantee:** By seeding the vocabulary with all 256 byte values, byte-level BPE eliminates the `<UNK>` token completely. Any arbitrary Unicode string, emoji, or binary payload can be tokenized.
2. **Compression Ratio & Inference Latency:** A small vocabulary forces words into numerous sub-token pieces, increasing sequence length $N$ and quadratically inflating Transformer attention compute $O(N^2)$. Expanding the vocabulary to 128k (Llama 3) increases token compression by ~15%, reducing token generation cycles by 15% across all languages.
3. **Multilingual Parity:** Standard WordPiece heavily fragments non-English scripts (e.g. Hindi, Chinese, Arabic). Byte-level BPE with extensive multilingual pretraining merges common non-Latin multi-byte sequences into single tokens.

---

## Question 2: In the 0/1 Knapsack DP space optimization, why is it mandatory to iterate backwards through the weight array?
**Answer:**
- In the 2D recurrence, $DP[i][w]$ depends on $DP[i-1][w]$ and $DP[i-1][w - weight[i]]$.
- When compressing into a 1D array `dp[w]`, iterating forwards ($w = weight[i] \dots capacity$) overwrites `dp[w - weight[i]]` with the value from the *current* item $i$. Subsequent lookups would use the updated value, effectively allowing item $i$ to be selected multiple times (which solves Unbounded Knapsack, not 0/1 Knapsack).
- Iterating **backwards** from $capacity$ down to $weight[i]$ ensures that `dp[w - weight[i]]` still holds the state from iteration $i-1$, strictly enforcing that each item is used at most once.
