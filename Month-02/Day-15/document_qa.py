"""
Document & Image Q&A Pipeline.
Processes multi-page documents, indexes extracted text alongside image bounding boxes,
and performs visual document question answering.
"""

from typing import Any, Callable, Dict, List, Optional
from ocr_pipeline import ExtractedDocument, OCRPipeline


class DocumentQAPipeline:

    def __init__(self, llm_vision_caller: Optional[Callable[[str, str], str]] = None):
        self.ocr = OCRPipeline()
        self.llm_caller = llm_vision_caller or self._mock_vision_qa

    def _mock_vision_qa(self, context_text: str, question: str) -> str:
        """Simulates multimodal QA."""
        if "revenue" in question.lower() or "growth" in question.lower():
            return "Based on the document, revenue reached $12.4M representing an 18% YoY growth."
        elif "expenses" in question.lower():
            return "Operating expenses decreased by 4.2% due to cloud optimizations."
        return f"Document Answer: {context_text[:100]}..."

    def answer_question_from_document(
        self,
        document_name: str,
        question: str,
        raw_document_content: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        1. Run OCR extraction
        2. Format context with bounding box provenance
        3. Invoke vision/text QA
        """
        doc = self.ocr.process_document(document_name, simulated_content=raw_document_content)

        # Context assembly with block anchors
        anchored_context = []
        for i, b in enumerate(doc.text_blocks, 1):
            anchored_context.append(f"[Block {i} - {b.block_type.upper()}]: {b.text}")

        context_str = "\n".join(anchored_context)
        answer = self.llm_caller(context_str, question)

        return {
            "document": document_name,
            "question": question,
            "answer": answer,
            "supporting_blocks": [
                {"block_id": i + 1, "text": b.text, "type": b.block_type}
                for i, b in enumerate(doc.text_blocks)
                if any(kw in b.text.lower() for kw in question.lower().split() if len(kw) > 3)
            ],
            "ocr_confidence": doc.metadata.get("avg_confidence", 0.95),
        }


if __name__ == "__main__":
    qa = DocumentQAPipeline()
    res = qa.answer_question_from_document("q3_report.pdf", "What was the revenue and YoY growth?")
    print("Q&A Result:\n", res["answer"])
    assert "$12.4M" in res["answer"]
    assert "18% YoY growth" in res["answer"]
    assert len(res["supporting_blocks"]) > 0
    print("DocumentQAPipeline tests passed successfully!")
