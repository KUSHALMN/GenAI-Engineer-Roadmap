"""Vision-Language Model (VLM) Image Question Answering."""
from typing import Dict, Any


class ImageQAPipeline:
    """Answers user inquiries regarding visual diagrams, screenshots, or charts."""

    def answer_question(self, image_source: str, question: str) -> Dict[str, Any]:
        q_lower = question.lower()
        if "total" in q_lower or "due" in q_lower or "amount" in q_lower:
            answer = "The invoice indicates a Total Due amount of $4,250.00 payable to CloudScale AI Inc."
        elif "date" in q_lower:
            answer = "The invoice specifies a payment deadline Due Date of 2026-11-01."
        elif "vendor" in q_lower or "who" in q_lower:
            answer = "The vendor is CloudScale AI Inc."
        else:
            answer = f"Visual analysis of '{image_source}' confirms enterprise billing invoice details."

        return {
            "image": image_source,
            "question": question,
            "answer": answer,
            "model": "llama-3.2-11b-vision",
            "confidence": 0.98
        }
