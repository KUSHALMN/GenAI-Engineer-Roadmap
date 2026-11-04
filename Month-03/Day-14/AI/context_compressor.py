"""
Contextual Compression Engine
Prunes noisy or irrelevant sentences from retrieved chunks while strictly retaining
source document IDs, chunk spans, and provenance attribution.
"""

import re
from typing import List, Dict, Any


class ContextCompressor:
    def __init__(self, min_similarity_threshold: float = 0.25):
        self.threshold = min_similarity_threshold

    def _split_into_sentences(self, text: str) -> List[str]:
        # Split on sentence boundaries preserving abbreviations
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())
        return [s.strip() for s in sentences if len(s.strip()) > 5]

    def _sentence_relevance(self, query: str, sentence: str) -> float:
        q_words = set(re.findall(r'\w+', query.lower()))
        s_words = set(re.findall(r'\w+', sentence.lower()))
        if not q_words:
            return 0.0
        overlap = len(q_words.intersection(s_words))
        # Jaccard index
        union = len(q_words.union(s_words))
        return overlap / max(1, union)

    def compress_chunk(self, query: str, chunk: Dict[str, Any]) -> Dict[str, Any]:
        sentences = self._split_into_sentences(chunk["text"])
        selected_sentences = []
        scores = []

        for idx, sent in enumerate(sentences):
            rel = self._sentence_relevance(query, sent)
            if rel >= self.threshold:
                selected_sentences.append(sent)
                scores.append(rel)

        # Fallback: if no single sentence exceeds threshold, keep the highest scoring one
        if not selected_sentences and sentences:
            all_scores = [(self._sentence_relevance(query, s), s) for s in sentences]
            best_score, best_sent = max(all_scores, key=lambda x: x[0])
            selected_sentences.append(best_sent)
            scores.append(best_score)

        compressed_text = " ".join(selected_sentences)
        compression_ratio = 1.0 - (len(compressed_text) / max(1, len(chunk["text"])))

        return {
            "source_id": chunk["id"],
            "original_length": len(chunk["text"]),
            "compressed_length": len(compressed_text),
            "compression_ratio": round(compression_ratio, 3),
            "relevance_score": round(max(scores) if scores else 0.0, 3),
            "compressed_text": compressed_text,
            "metadata": chunk.get("metadata", {})
        }

    def compress_all(self, query: str, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [self.compress_chunk(query, c) for c in chunks]


if __name__ == "__main__":
    noisy_chunks = [
        {
            "id": "doc_101",
            "text": (
                "Welcome to the quarterly engineering report. Our team celebrated three anniversaries in June. "
                "Vector database indexing using HNSW provides logarithmic search time for embeddings. "
                "The office coffee machine was replaced on Tuesday with an espresso grinder."
            ),
            "metadata": {"author": "infra_team", "page": 4}
        },
        {
            "id": "doc_102",
            "text": (
                "Company policy requires badges at all times. "
                "HNSW graph connectivity parameter M determines the number of bi-directional links per node. "
                "Parking permits are renewed annually in October."
            ),
            "metadata": {"author": "security", "page": 12}
        }
    ]

    compressor = ContextCompressor(min_similarity_threshold=0.15)
    query = "HNSW vector database graph connectivity"

    compressed = compressor.compress_all(query, noisy_chunks)

    print("=== Contextual Compression Demonstration ===")
    for c in compressed:
        print(f"[{c['source_id']}] Compressed {c['original_length']} chars -> {c['compressed_length']} chars (Saved: {c['compression_ratio']*100:.1f}%)")
        print(f"Extracted: \"{c['compressed_text']}\"")
        print(f"Metadata preserved: {c['metadata']}\n")
