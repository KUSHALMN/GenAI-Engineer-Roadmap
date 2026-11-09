"""
Multimodal Image Embeddings & Vector Index Engine.
Simulates dual-encoder (CLIP/SigLIP) vector spaces, normalized cosine
similarity, and cross-modal (Text-to-Image and Image-to-Image) retrieval.
"""

from dataclasses import dataclass, field
import math
import random
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class ImageDocument:
    image_id: str
    file_path: str
    caption: str
    embedding: List[float]
    metadata: Dict[str, Any] = field(default_factory=dict)


class MultimodalImageIndex:
    """Manages cross-modal vector indexing and cosine retrieval."""

    def __init__(self, dim: int = 128):
        self.dim = dim
        self.index: Dict[str, ImageDocument] = {}

    @staticmethod
    def _normalize(vec: List[float]) -> List[float]:
        norm = math.sqrt(sum(x * x for x in vec))
        if norm == 0:
            return vec
        return [x / norm for x in vec]

    @staticmethod
    def cosine_similarity(v1: List[float], v2: List[float]) -> float:
        return sum(a * b for a, b in zip(v1, v2))

    def _simulate_clip_embedding(self, text_or_label: str) -> List[float]:
        # Deterministic pseudo-embedding based on hash
        rng = random.Random(hash(text_or_label) & 0xFFFFFFFF)
        raw = [rng.gauss(0, 1) for _ in range(self.dim)]
        return self._normalize(raw)

    def add_image(self, image_id: str, file_path: str, caption: str, metadata: Optional[Dict[str, Any]] = None):
        emb = self._simulate_clip_embedding(caption)
        doc = ImageDocument(
            image_id=image_id,
            file_path=file_path,
            caption=caption,
            embedding=emb,
            metadata=metadata or {}
        )
        self.index[image_id] = doc

    def search_by_text(self, text_query: str, top_k: int = 3) -> List[Tuple[ImageDocument, float]]:
        query_emb = self._simulate_clip_embedding(text_query)
        scored = []
        for doc in self.index.values():
            sim = self.cosine_similarity(query_emb, doc.embedding)
            scored.append((doc, sim))
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_k]

    def search_by_image(self, target_image_id: str, top_k: int = 3) -> List[Tuple[ImageDocument, float]]:
        if target_image_id not in self.index:
            raise KeyError(f"Image ID '{target_image_id}' not found in index.")
        target_doc = self.index[target_image_id]
        
        scored = []
        for doc in self.index.values():
            if doc.image_id == target_image_id:
                continue
            sim = self.cosine_similarity(target_doc.embedding, doc.embedding)
            scored.append((doc, sim))
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_k]


if __name__ == "__main__":
    idx = MultimodalImageIndex(dim=64)

    # Ingest catalog of technical diagrams and documents
    idx.add_image("img_01", "arch_vllm.png", "vLLM PagedAttention virtual memory block allocation flowchart")
    idx.add_image("img_02", "arch_rag.png", "Hybrid RAG search pipeline with BM25 dense fusion and reranker")
    idx.add_image("img_03", "chart_perf.png", "Bar chart showing latency vs throughput benchmarks for H100 clusters")
    idx.add_image("img_04", "invoice_scan.png", "Medical laboratory invoice showing patient lipid profile test totals")

    print("=== Text-to-Image Cross-Modal Retrieval ===")
    query = "memory allocation virtual paging"
    results = idx.search_by_text(query, top_k=2)
    for doc, score in results:
        print(f"Match [{score:.4f}]: {doc.image_id} - '{doc.caption}'")
