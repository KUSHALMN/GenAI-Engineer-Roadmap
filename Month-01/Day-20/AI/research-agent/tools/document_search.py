import math
import re
from typing import List, Dict, Any

try:
    from schemas import SearchResult
except ImportError:
    from ..schemas import SearchResult



# Seminal AI Research Corpus
RESEARCH_CORPUS = [
    {
        "id": "PAPER-001",
        "title": "Attention Is All You Need (Vaswani et al., 2017)",
        "source": "https://arxiv.org/abs/1706.03762",
        "category": "Transformer Architecture",
        "text": """The dominant sequence transduction models are based on complex recurrent or convolutional neural networks.
We propose the Transformer, a network architecture based solely on attention mechanisms, dispensing with recurrence and convolutions.
Multi-Head Attention allows the model to jointly attend to information from different representation subspaces at different positions.
Scaled Dot-Product Attention computes: Attention(Q, K, V) = softmax(Q * K^T / sqrt(d_k)) * V.
Computational complexity per layer for standard self-attention is O(N^2 * d), where N is sequence length and d is representation dimension."""
    },
    {
        "id": "PAPER-002",
        "title": "LoRA: Low-Rank Adaptation of Large Language Models (Hu et al., 2021)",
        "source": "https://arxiv.org/abs/2106.09685",
        "category": "Parameter-Efficient Fine-Tuning (PEFT)",
        "text": """An important paradigm of natural language processing consists of large-scale pre-training on general domain data and adaptation to specific tasks.
When fine-tuning large models like GPT-3 175B, fine-tuning all parameters is computationally prohibitive.
LoRA freezes the pre-trained model weights W_0 in R^(d x k) and injects trainable rank decomposition matrices: W = W_0 + Delta_W = W_0 + B * A, where B in R^(d x r) and A in R^(r x k), with rank r << min(d, k).
During training, W_0 is frozen and receives no gradient updates, while A and B contain trainable parameters.
LoRA can reduce the number of trainable parameters by 10,000 times and GPU VRAM memory requirements by 3 times compared to full fine-tuning without inference latency."""
    },
    {
        "id": "PAPER-003",
        "title": "Direct Preference Optimization: Your Language Model is Secretly a Reward Model (Rafailov et al., 2023)",
        "source": "https://arxiv.org/abs/2305.18290",
        "category": "Alignment & RLHF",
        "text": """Reinforcement Learning from Human Feedback (RLHF) is a complex and often unstable procedure, first fitting a reward model that reflects human preferences, and then fine-tuning the large unsupervised LM using reinforcement learning (PPO).
We introduce Direct Preference Optimization (DPO), a stable, performant, and computationally lightweight algorithm.
DPO mathematically proves that the constrained RL problem can be optimized exactly with a simple binary cross-entropy loss directly over preference pairs (y_w > y_l) using the implicit reward formulation r(x, y) = beta * log(pi_theta(y|x) / pi_ref(y|x)).
DPO eliminates the need to train a separate reward model, sample from the LM during training, or perform extensive hyperparameter tuning required by PPO."""
    },
    {
        "id": "PAPER-004",
        "title": "DeepSeek-V3 Technical Report & Mixture-of-Experts Architecture (DeepSeek-AI, 2024)",
        "source": "https://github.com/deepseek-ai/DeepSeek-V3",
        "category": "MoE & Architecture",
        "text": """DeepSeek-V3 is a strong Mixture-of-Experts (MoE) language model with 671B total parameters with 37B activated for each token.
It adopts Multi-head Latent Attention (MLA) for efficient inference by compressing KV cache into low-dimensional latent vectors.
DeepSeekMoE architecture utilizes fine-grained expert segmentation (e.g., 256 routed experts + 1 shared expert) with top-8 routing.
To prevent routing collapse without hurting performance, DeepSeek-V3 introduces an auxiliary-loss-free strategy for load balancing via dynamic bias terms.
DeepSeek-V3 was trained on 14.8 trillion tokens using only 2.788 million H800 GPU hours at an estimated total cost of $5.576 million."""
    },
    {
        "id": "PAPER-005",
        "title": "FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning (Dao, 2023)",
        "source": "https://arxiv.org/abs/2307.08691",
        "category": "Hardware Optimization",
        "text": """Standard attention implementations materialize the intermediate N x N attention matrix in high-bandwidth memory (HBM), resulting in high memory traffic and slow execution on GPUs.
FlashAttention is an IO-aware exact attention algorithm that uses tiling to load blocks of Q, K, V from HBM to fast on-chip SRAM, computes attention incrementally, and writes results back without ever materializing the full N x N matrix in HBM.
FlashAttention-2 improves work partitioning across thread blocks and warps on GPUs, reaching up to 73% of theoretical peak FLOPs on NVIDIA A100/H100 GPUs and providing 2x to 4x wall-clock speedup over standard attention."""
    },
    {
        "id": "PAPER-006",
        "title": "ReAct: Synergizing Reasoning and Acting in Language Models (Yao et al., 2022)",
        "source": "https://arxiv.org/abs/2210.03629",
        "category": "Agentic Reasoning",
        "text": """While large language models (LLMs) demonstrate impressive reasoning (Chain-of-Thought) and acting capabilities, these two modes have predominantly remained isolated.
ReAct explores the synergy of interleaving reasoning traces (Thoughts) with task-specific actions (Actions) and environment feedback (Observations).
Thoughts help the model induce, track, and update action plans as well as handle exceptions. Actions allow the model to interface with external sources such as knowledge bases and calculators.
On question answering (HotpotQA) and decision-making benchmarks (ALFWorld), ReAct overcomes issues of hallucination and error propagation common in pure Chain-of-Thought reasoning."""
    },
    {
        "id": "PAPER-007",
        "title": "Training Compute-Optimal Large Language Models (Chinchilla / Hoffmann et al., 2022)",
        "source": "https://arxiv.org/abs/2203.15556",
        "category": "Scaling Laws",
        "text": """We investigate the optimal model size and number of tokens for training a transformer language model under a given compute budget.
We find that current large language models (like GPT-3 175B and Gopher 280B) are significantly undertrained relative to their compute budget.
For compute-optimal training, model size (number of parameters N) and training dataset size (number of tokens D) should be scaled equally: both N and D should double for every 4x increase in total FLOP compute.
The empirical compute-optimal rule is approximately D ~= 20 * N tokens.
The total compute budget in FLOPs is approximated by C ~= 6 * N * D."""
    },
    {
        "id": "PAPER-008",
        "title": "GraphRAG: Unlocking LLM Discovery on Complex Information Networks (Microsoft Research, 2024)",
        "source": "https://arxiv.org/abs/2404.16130",
        "category": "Retrieval Augmented Generation",
        "text": """Standard RAG systems using naive semantic vector search excel at local retrieval (fetching specific facts from distinct chunks), but fail at global sensemaking questions (such as 'What are the top 5 emerging themes across the entire dataset?').
GraphRAG builds an extracted entity-relation knowledge graph from the document corpus, uses Leiden community detection algorithms to generate hierarchical graph cluster summaries, and provides comprehensive global answers by querying community reports.
GraphRAG significantly improves answer comprehensiveness and diversity on complex multi-document reasoning tasks."""
    },
    {
        "id": "PAPER-009",
        "title": "LLM Quantization & Memory Mechanics (AWQ, GPTQ, GGUF)",
        "source": "https://arxiv.org/abs/2306.00978",
        "category": "Model Compression & Serving",
        "text": """Inference of Large Language Models is predominantly memory-bandwidth bound during the autoregressive token generation phase.
Model weight VRAM memory footprint formula: VRAM_weights = Num_Parameters * Bytes_Per_Weight.
In FP16 / BF16, Bytes_Per_Weight = 2 bytes (e.g. 70B parameter model requires 70 * 2 = 140 GB VRAM).
In INT8 quantization, Bytes_Per_Weight = 1 byte (70B model requires 70 GB VRAM).
In INT4 (AWQ / GPTQ / GGUF Q4_K_M), Bytes_Per_Weight ~= 0.55 - 0.6 bytes (70B model requires ~40 GB VRAM, fitting on 2x RTX 3090 or single A100 80GB).
Quantization reduces memory bandwidth pressure, directly increasing per-user token generation throughput."""
    }
]


class DocumentSearchEngine:
    """
    Inverted index and BM25-style lexical ranking engine for AI research papers.
    """

    def __init__(self, corpus: List[Dict[str, Any]] = None):
        self.corpus = corpus or RESEARCH_CORPUS
        self.stop_words = {
            "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't",
            "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can't",
            "cannot", "could", "did", "do", "does", "doing", "don't", "down", "during", "each", "few", "for", "from",
            "further", "had", "has", "have", "having", "he", "her", "here", "hers", "herself", "him", "himself",
            "his", "how", "i", "if", "in", "into", "is", "isn't", "it", "its", "itself", "let's", "me", "more",
            "most", "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought",
            "our", "ours", "ourselves", "out", "over", "own", "same", "shan't", "she", "should", "so", "some", "such",
            "than", "that", "the", "their", "theirs", "them", "themselves", "then", "there", "these", "they", "this",
            "those", "through", "to", "too", "under", "until", "up", "very", "was", "we", "were", "what", "when",
            "where", "which", "while", "who", "whom", "why", "with", "would", "you", "your", "yours", "yourself"
        }
        self._build_index()

    def _tokenize(self, text: str) -> List[str]:
        words = re.findall(r"\b[a-zA-Z0-9_\-\.\^]+\b", text.lower())
        return [w for w in words if w not in self.stop_words and len(w) > 1]

    def _build_index(self):
        self.doc_tokens = []
        self.doc_lengths = []
        self.inverted_index = {}  # term -> list of (doc_id, tf)

        total_length = 0
        for doc_idx, doc in enumerate(self.corpus):
            full_text = f"{doc['title']} {doc['category']} {doc['text']}"
            tokens = self._tokenize(full_text)
            self.doc_tokens.append(tokens)
            self.doc_lengths.append(len(tokens))
            total_length += len(tokens)

            tf_map = {}
            for t in tokens:
                tf_map[t] = tf_map.get(t, 0) + 1

            for term, count in tf_map.items():
                if term not in self.inverted_index:
                    self.inverted_index[term] = []
                self.inverted_index[term].append((doc_idx, count))

        self.num_docs = len(self.corpus)
        self.avg_doc_len = total_length / self.num_docs if self.num_docs > 0 else 1.0

    def search(self, query: str, top_k: int = 3) -> List[SearchResult]:
        """
        Calculates BM25-based similarity score for query against indexed documents.
        """
        query_tokens = self._tokenize(query)
        if not query_tokens:
            return []

        scores = [0.0] * self.num_docs
        k1 = 1.5
        b = 0.75

        for term in query_tokens:
            if term in self.inverted_index:
                postings = self.inverted_index[term]
                df = len(postings)
                # BM25 IDF formula
                idf = math.log((self.num_docs - df + 0.5) / (df + 0.5) + 1.0)

                for doc_idx, tf in postings:
                    doc_len = self.doc_lengths[doc_idx]
                    tf_norm = (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * (doc_len / self.avg_doc_len)))
                    scores[doc_idx] += idf * tf_norm

        # Rank documents
        ranked_indices = sorted(range(self.num_docs), key=lambda i: scores[i], reverse=True)

        results = []
        max_score = max(scores) if scores and max(scores) > 0 else 1.0

        for doc_idx in ranked_indices[:top_k]:
            if scores[doc_idx] <= 0:
                continue

            doc = self.corpus[doc_idx]
            norm_score = round(min(1.0, scores[doc_idx] / max_score), 4)

            # Generate smart excerpt snippet based on matched tokens
            snippet = self._generate_snippet(doc["text"], query_tokens)

            results.append(
                SearchResult(
                    id=doc["id"],
                    title=doc["title"],
                    snippet=snippet,
                    relevance_score=norm_score,
                    source=doc["source"],
                    category=doc["category"]
                )
            )

        return results

    def _generate_snippet(self, text: str, query_tokens: List[str], max_len: int = 250) -> str:
        sentences = text.split("\n")
        best_sentence = sentences[0]
        max_overlap = -1

        for sentence in sentences:
            stok = set(self._tokenize(sentence))
            overlap = len(stok.intersection(set(query_tokens)))
            if overlap > max_overlap:
                max_overlap = overlap
                best_sentence = sentence

        clean = best_sentence.strip()
        if len(clean) > max_len:
            clean = clean[:max_len] + "..."
        return clean


# Global search engine instance
_search_engine = DocumentSearchEngine()


def document_search(query: str, top_k: int = 3) -> List[SearchResult]:
    """Module-level function exposed to tools registry."""
    return _search_engine.search(query=query, top_k=top_k)
