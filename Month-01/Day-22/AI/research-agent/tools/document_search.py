"""
Document Search Tool
Provides BM25-based lexical retrieval over an indexed corpus of seminal
AI research papers and architectural specifications.
"""

import math
import re
from typing import List, Dict, Any, Tuple
from schemas import Citation


RESEARCH_CORPUS = [
    {
        "id": "deepseek_v3_2024",
        "title": "DeepSeek-V3 Technical Report (DeepSeek AI, 2024)",
        "content": (
            "DeepSeek-V3 is a 671B total parameter Mixture-of-Experts (MoE) model with 37B activated parameters per token. "
            "It incorporates Multi-Head Latent Attention (MLA) to drastically compress Key-Value (KV) cache memory footprint, "
            "reducing KV cache size per token by over 93.3% compared to standard MHA. "
            "The model utilizes DeepSeekMoE architecture with fine-grained experts: 1 shared expert and 256 routed experts, "
            "where 8 routed experts are activated per token. DeepSeek-V3 was trained on 14.8 Trillion tokens using FP8 mixed precision, "
            "costing only $5.58M in compute budget (2.788M H800 GPU hours)."
        )
    },
    {
        "id": "attention_all_you_need_2017",
        "title": "Attention Is All You Need (Vaswani et al., 2017)",
        "content": (
            "The Transformer architecture replaces recurrent and convolutional layers entirely with multi-head self-attention. "
            "Multi-Head Attention computes Scaled Dot-Product Attention: Attention(Q, K, V) = softmax(Q K^T / sqrt(d_k)) V. "
            "Computational complexity per layer is O(N^2 * d) where N is sequence length and d is representation dimension. "
            "Positional encodings are added to input embeddings to retain sequential token positions."
        )
    },
    {
        "id": "chinchilla_scaling_laws_2022",
        "title": "Training Compute-Optimal Large Language Models (Hoffmann et al., 2022)",
        "content": (
            "Chinchilla scaling laws determine compute-optimal training allocation. For a compute budget C, "
            "model size N and training tokens D should scale in equal proportion: N ~ C^0.5 and D ~ C^0.5. "
            "Specifically, an optimal model requires approximately 20 tokens per parameter. "
            "Training compute is estimated by FLOPs = 6 * N * D for forward and backward passes."
        )
    },
    {
        "id": "flashattention_2022",
        "title": "FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness (Dao et al., 2022)",
        "content": (
            "FlashAttention optimizes standard self-attention by minimizing High Bandwidth Memory (HBM) IO reads and writes. "
            "Using GPU SRAM tiling and online softmax rescaling, FlashAttention computes exact attention with O(N) memory complexity "
            "instead of O(N^2) memory footprint, resulting in a 2x to 4x wall-clock speedup without any approximation."
        )
    },
    {
        "id": "llama3_herd_of_models_2024",
        "title": "The Llama 3 Herd of Models (Meta AI, 2024)",
        "content": (
            "Llama 3 405B is a flagship dense Transformer trained on over 15.6 Trillion multilingual tokens with an 8K context window, "
            "scaled to 128K via RoPE frequency base modification (theta = 500,000). "
            "It uses Grouped-Query Attention (GQA) with 8 Key-Value heads across 128 query heads to minimize inference KV cache consumption. "
            "Total training FLOPs exceeded 3.8 x 10^25."
        )
    },
    {
        "id": "graphrag_microsoft_2024",
        "title": "From Local to Global: A Graph RAG Approach to Query-Focused Summarization (Edge et al., 2024)",
        "content": (
            "GraphRAG combines knowledge graph extraction with hierarchical community detection (Leiden algorithm) "
            "to perform global dataset summarization and multi-hop reasoning. "
            "While vector RAG struggles with global dataset-wide themes ('What are the top 5 emerging themes across all reports?'), "
            "GraphRAG builds modular community reports at multiple hierarchical levels to answer holistic questions."
        )
    },
    {
        "id": "mixture_of_experts_switch_2022",
        "title": "Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity (Fedus et al., 2022)",
        "content": (
            "Switch Transformers simplify Mixture of Experts by routing each token to only 1 expert (Top-1 routing), "
            "maximizing parameter capacity while keeping FLOPs per token constant. "
            "Auxiliary load-balancing losses prevent routing collapse where a small subset of experts receives all tokens."
        )
    }
]


class BM25SearchEngine:
    """Inverted Index BM25 search engine for lexical retrieval."""
    
    def __init__(self, corpus: List[Dict[str, str]], k1: float = 1.5, b: float = 0.75):
        self.corpus = corpus
        self.k1 = k1
        self.b = b
        self.doc_len = [len(self._tokenize(doc["content"])) for doc in corpus]
        self.avg_doc_len = sum(self.doc_len) / max(len(corpus), 1)
        self.inverted_index: Dict[str, Dict[int, int]] = {}
        self.doc_count = len(corpus)
        self._build_index()

    def _tokenize(self, text: str) -> List[str]:
        return re.findall(r'\b[a-zA-Z0-9_\-\.]+\b', text.lower())

    def _build_index(self):
        for doc_id, doc in enumerate(self.corpus):
            tokens = self._tokenize(doc["content"] + " " + doc["title"])
            for token in tokens:
                if token not in self.inverted_index:
                    self.inverted_index[token] = {}
                self.inverted_index[token][doc_id] = self.inverted_index[token].get(doc_id, 0) + 1

    def search(self, query: str, top_k: int = 3) -> List[Tuple[Dict[str, str], float]]:
        query_tokens = self._tokenize(query)
        scores: Dict[int, float] = {}

        for token in query_tokens:
            if token in self.inverted_index:
                n_docs_with_token = len(self.inverted_index[token])
                idf = math.log((self.doc_count - n_docs_with_token + 0.5) / (n_docs_with_token + 0.5) + 1.0)

                for doc_id, freq in self.inverted_index[token].items():
                    denom = freq + self.k1 * (1 - self.b + self.b * (self.doc_len[doc_id] / self.avg_doc_len))
                    bm25_term = idf * ((freq * (self.k1 + 1)) / denom)
                    scores[doc_id] = scores.get(doc_id, 0.0) + bm25_term

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
        return [(self.corpus[doc_id], score) for doc_id, score in ranked]


_engine = BM25SearchEngine(RESEARCH_CORPUS)


def search_documents(query: str, top_k: int = 2) -> Dict[str, Any]:
    """
    Executes a lexical BM25 search against the research corpus.
    
    Args:
        query (str): The search phrase or technical topic.
        top_k (int): Number of top documents to return.
        
    Returns:
        Dict[str, Any]: Formatted findings with citations and text excerpts.
    """
    results = _engine.search(query, top_k=top_k)
    
    if not results:
        return {
            "results_found": 0,
            "query": query,
            "citations": [],
            "summary": f"No relevant research documents found for query: '{query}'"
        }

    citations = []
    formatted_excerpts = []

    for doc, score in results:
        citation = Citation(
            source_id=doc["id"],
            title=doc["title"],
            snippet=doc["content"][:240] + "...",
            score=round(score, 3)
        )
        citations.append(citation)
        formatted_excerpts.append(f"[{doc['title']}] (Relevance: {round(score, 2)}):\n{doc['content']}")

    return {
        "results_found": len(results),
        "query": query,
        "citations": [c.model_dump() for c in citations],
        "content": "\n\n".join(formatted_excerpts)
    }
