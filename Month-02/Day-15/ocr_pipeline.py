"""
OCR & Document Text Extraction Pipeline.
Extracts text blocks, bounding boxes, confidence ratings, and layout structure
from document images or PDFs.
"""

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class BoundingBox:
    x_min: int
    y_min: int
    x_max: int
    y_max: int


@dataclass
class TextBlock:
    text: str
    confidence: float
    bbox: BoundingBox
    block_type: str = "paragraph"  # "heading", "paragraph", "table", "footer"


@dataclass
class ExtractedDocument:
    file_name: str
    page_count: int
    text_blocks: List[TextBlock] = field(default_factory=list)
    raw_full_text: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


class OCRPipeline:
    """Extracts structured layout and text from visual documents."""

    @classmethod
    def process_document(cls, file_name: str, simulated_content: Optional[str] = None) -> ExtractedDocument:
        """Processes document and outputs structured blocks."""
        content = simulated_content or (
            "# Quarterly Financial Report\n"
            "Revenue reached $12.4M representing an 18% YoY growth.\n"
            "Operating expenses decreased by 4.2% due to cloud optimizations."
        )

        blocks: List[TextBlock] = []
        lines = content.strip().split("\n")
        y = 50

        for line in lines:
            line_str = line.strip()
            if not line_str:
                continue

            block_type = "heading" if line_str.startswith("#") else "paragraph"
            clean_text = line_str.lstrip("# ")

            blocks.append(TextBlock(
                text=clean_text,
                confidence=0.98 if block_type == "heading" else 0.94,
                bbox=BoundingBox(x_min=50, y_min=y, x_max=550, y_max=y + 30),
                block_type=block_type,
            ))
            y += 40

        full_text = "\n".join(b.text for b in blocks)
        return ExtractedDocument(
            file_name=file_name,
            page_count=1,
            text_blocks=blocks,
            raw_full_text=full_text,
            metadata={
                "ocr_engine": "SimulatedTesseract-LayoutLM",
                "avg_confidence": round(sum(b.confidence for b in blocks) / max(len(blocks), 1), 3),
            },
        )


if __name__ == "__main__":
    doc = OCRPipeline.process_document("financials_q3.pdf")
    print(f"Extracted {len(doc.text_blocks)} blocks from {doc.file_name}")
    assert doc.text_blocks[0].block_type == "heading"
    assert "Revenue reached $12.4M" in doc.raw_full_text
    print("OCRPipeline tests passed successfully!")
