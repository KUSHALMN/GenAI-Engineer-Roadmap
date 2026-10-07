"""Multimodal RAG indexing both visual screenshots and textual knowledge."""
from typing import List, Dict, Any
from .image_embeddings import ImageEmbeddingGenerator
from .image_qa import ImageQAPipeline


class MultimodalRAG:
    """Retrieves relevant image chunks and textual passages to answer hybrid queries."""

    def __init__(self):
        self.embedding_gen = ImageEmbeddingGenerator()
        self.vlm = ImageQAPipeline()
        self.index: List[Dict[str, Any]] = [
            {
                "id": "item1",
                "type": "image",
                "uri": "s3://docs/invoice_904.png",
                "description": "Invoice showing total due $4,250.00 from CloudScale AI"
            },
            {
                "id": "item2",
                "type": "text",
                "content": "CloudScale AI enterprise SLA guarantees 99.99% monthly availability for GPU clusters."
            }
        ]

    def query(self, prompt: str) -> Dict[str, Any]:
        # For multimodal questions referring to images
        if "invoice" in prompt.lower() or "amount" in prompt.lower():
            vlm_res = self.vlm.answer_question("s3://docs/invoice_904.png", prompt)
            return {
                "response": vlm_res["answer"],
                "source_type": "image_vlm",
                "matched_item": "s3://docs/invoice_904.png"
            }
        return {
            "response": "CloudScale AI enterprise SLA guarantees 99.99% monthly availability for GPU clusters.",
            "source_type": "text_rag",
            "matched_item": "item2"
        }
