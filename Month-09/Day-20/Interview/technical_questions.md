# 🎯 Technical Interview Questions — Day 20: Pretraining Evaluation & Accounts Merge DSU

## Question 1: Why is Bits-Per-Byte (BPB) a fairer metric than Perplexity when comparing models trained with different tokenizers?
**Answer:**
1. **Tokenizer Vocabulary Bias in Perplexity:**
   - Perplexity is $\text{PPL} = \exp(\text{Loss}) = \exp\left(-\frac{1}{N} \sum \log P(w_i)\right)$, measuring the average surprise *per token*.
   - A model with a tiny vocabulary (e.g. character-level) predicts simple small chunks with low cross-entropy per token, while a model with a 128k vocabulary predicts large full words with higher cross-entropy per token.
   - Comparing their raw perplexities is invalid because the denominator (total tokens $N$) differs by up to $3\times$.
2. **Bits-Per-Byte Normalization:**
   $$\text{BPB} = \frac{\text{Total Cross-Entropy in Bits}}{\text{Total Raw UTF-8 Bytes}} = \frac{\sum \log_2 P(w_i)}{\text{Total File Bytes}}$$
   BPB normalizes the total cross-entropy strictly by the original text length in bytes, completely independent of tokenizer vocabulary size or merge strategies.

---

## Question 2: In LeetCode 721 (Accounts Merge), how does DSU achieve efficient graph connected components over emails?
**Answer:**
- **Account Index Union:** Treat each account index ($0 \dots N-1$) as a graph node. A Hash Map `emailToAccount` maps each email to the first account index that introduced it.
- When an email is encountered that already exists in the map, `dsu.union(currentAccount, previousAccount)` merges both accounts into the same connected component.
- In step 2, grouping emails into a `TreeSet` indexed by `dsu.find(i)` automatically sorts emails lexicographically and deduplicates them in $O(M \log M)$ time.
