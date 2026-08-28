import math
import re
from typing import List, Dict, Any, Tuple
from collections import Counter
from .vector_store import VectorStore

class BM25Retriever:
    """
    In-memory Okapi BM25 implementation for lexical keyword search.
    """

    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.corpus: List[Dict[str, Any]] = []
        self.doc_tokens: List[List[str]] = []
        self.doc_lens: List[int] = []
        self.avg_doc_len: float = 0.0
        self.doc_freqs: Dict[str, int] = Counter()
        self.idf: Dict[str, float] = {}

    def _tokenize(self, text: str) -> List[str]:
        return re.findall(r'\b\w+\b', text.lower())

    def index(self, chunks: List[Dict[str, Any]]) -> None:
        self.corpus = chunks
        self.doc_tokens = [self._tokenize(c.get("text", "")) for c in chunks]
        self.doc_lens = [len(tokens) for tokens in self.doc_tokens]
        self.avg_doc_len = (sum(self.doc_lens) / len(self.doc_lens)) if self.doc_lens else 0.0

        # Calculate document frequencies
        self.doc_freqs = Counter()
        for tokens in self.doc_tokens:
            unique_terms = set(tokens)
            for term in unique_terms:
                self.doc_freqs[term] += 1

        # Calculate IDF (Inverse Document Frequency)
        N = len(chunks)
        self.idf = {}
        for term, freq in self.doc_freqs.items():
            self.idf[term] = math.log((N - freq + 0.5) / (freq + 0.5) + 1.0)

    def search(self, query: str, top_k: int = 4) -> List[Tuple[Dict[str, Any], float]]:
        if not self.corpus:
            return []

        query_tokens = self._tokenize(query)
        scores = []

        for idx, tokens in enumerate(self.doc_tokens):
            score = 0.0
            doc_len = self.doc_lens[idx]
            token_counts = Counter(tokens)

            for q_term in query_tokens:
                if q_term not in self.idf:
                    continue
                tf = token_counts[q_term]
                idf = self.idf[q_term]
                numerator = tf * (self.k1 + 1)
                denominator = tf + self.k1 * (1 - self.b + self.b * (doc_len / (self.avg_doc_len or 1.0)))
                score += idf * (numerator / denominator)

            if score > 0.0:
                scores.append((self.corpus[idx], score))

        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]


class HybridRetriever:
    """
    Production Hybrid Retriever fusing Dense Semantic Vector Retrieval + Sparse BM25 Lexical Retrieval
    using Reciprocal Rank Fusion (RRF).
    """

    def __init__(self, vector_store: VectorStore, rrf_k: int = 60, bm25_weight: float = 0.4, dense_weight: float = 0.6):
        self.vector_store = vector_store
        self.bm25 = BM25Retriever()
        self.rrf_k = rrf_k
        self.bm25_weight = bm25_weight
        self.dense_weight = dense_weight

    def index(self, chunks: List[Dict[str, Any]]) -> int:
        """Add chunks to both VectorStore and BM25 index."""
        dense_added = self.vector_store.add_chunks(chunks)
        self.bm25.index(self.vector_store.chunks)
        return dense_added

    def retrieve(self, query: str, top_k: int = 4) -> List[Dict[str, Any]]:
        """
        Execute Hybrid Retrieval using Reciprocal Rank Fusion (RRF).
        RRF Score(d) = sum( weight_i / (k + rank_i(d)) )
        """
        dense_results = self.vector_store.search(query, top_k=top_k * 2)
        bm25_results = self.bm25.search(query, top_k=top_k * 2)

        rrf_scores: Dict[str, float] = {}
        chunk_map: Dict[str, Dict[str, Any]] = {}

        # Process Dense results
        for rank, (chunk, score) in enumerate(dense_results):
            cid = chunk["chunk_id"]
            chunk_map[cid] = chunk
            rrf_score = self.dense_weight / (self.rrf_k + rank + 1)
            rrf_scores[cid] = rrf_scores.get(cid, 0.0) + rrf_score

        # Process BM25 results
        for rank, (chunk, score) in enumerate(bm25_results):
            cid = chunk["chunk_id"]
            chunk_map[cid] = chunk
            rrf_score = self.bm25_weight / (self.rrf_k + rank + 1)
            rrf_scores[cid] = rrf_scores.get(cid, 0.0) + rrf_score

        # Sort aggregated chunks by combined RRF score
        sorted_chunks = sorted(rrf_scores.items(), key=lambda item: item[1], reverse=True)
        
        final_results = []
        for cid, score in sorted_chunks[:top_k]:
            enriched_chunk = dict(chunk_map[cid])
            enriched_chunk["hybrid_rrf_score"] = round(score, 6)
            final_results.append(enriched_chunk)

        return final_results
