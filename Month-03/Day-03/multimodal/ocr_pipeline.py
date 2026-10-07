"""OCR (Optical Character Recognition) pipeline for scanned documents & receipts."""
import re
from typing import Dict, Any, List


class OCRPipeline:
    """Simulates multi-engine OCR extraction with bounding-box structure parsing."""

    def extract_text(self, document_path_or_bytes: str) -> Dict[str, Any]:
        # Simulated high-fidelity OCR parse
        lines = [
            {"text": "INVOICE #INV-2026-904", "bbox": [50, 40, 250, 60], "confidence": 0.99},
            {"text": "Vendor: CloudScale AI Inc.", "bbox": [50, 70, 300, 90], "confidence": 0.98},
            {"text": "Total Due: $4,250.00", "bbox": [50, 120, 220, 140], "confidence": 0.97},
            {"text": "Due Date: 2026-11-01", "bbox": [50, 150, 200, 170], "confidence": 0.96}
        ]
        full_text = "\n".join([line["text"] for line in lines])
        return {
            "source": document_path_or_bytes,
            "raw_text": full_text,
            "lines": lines,
            "avg_confidence": 0.975
        }
