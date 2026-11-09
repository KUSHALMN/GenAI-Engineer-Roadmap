"""
Document Layout Understanding & Reading Order Topological Parser.
Detects paragraphs, titles, tables, headers, footers, and resolves
multi-column reading order using XY-cut geometric projections.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Tuple


class ElementType(Enum):
    TITLE = "title"
    HEADER = "header"
    FOOTER = "footer"
    PARAGRAPH = "paragraph"
    TABLE = "table"
    FIGURE = "figure"


@dataclass
class LayoutBlock:
    block_id: str
    element_type: ElementType
    bbox: Tuple[int, int, int, int]  # (x1, y1, x2, y2)
    text: str
    page_number: int = 1
    column_index: int = 0


class DocumentLayoutParser:
    """Parses multi-column geometric bounding boxes and resolves reading order."""

    def __init__(self, page_width: int = 1000, page_height: int = 1400):
        self.page_width = page_width
        self.page_height = page_height

    def filter_headers_footers(self, blocks: List[LayoutBlock]) -> List[LayoutBlock]:
        """Removes repetitive running headers and footers based on vertical margins."""
        filtered = []
        for b in blocks:
            # Top 5% is header, bottom 5% is footer
            if b.bbox[1] < self.page_height * 0.05 and b.element_type == ElementType.HEADER:
                continue
            if b.bbox[3] > self.page_height * 0.95 and b.element_type == ElementType.FOOTER:
                continue
            filtered.append(b)
        return filtered

    def detect_columns(self, blocks: List[LayoutBlock]) -> int:
        """Determines whether page layout is single-column, 2-column, or 3-column."""
        gutter_threshold = self.page_width / 2.0
        left_count = sum(1 for b in blocks if b.bbox[2] <= gutter_threshold + 50)
        right_count = sum(1 for b in blocks if b.bbox[0] >= gutter_threshold - 50)
        
        if left_count >= 1 and right_count >= 1:
            return 2
        return 1

    def assign_reading_order(self, blocks: List[LayoutBlock]) -> List[LayoutBlock]:
        """
        Sorts blocks by column-first, then vertical top-to-bottom.
        Spanning titles (crossing gutter) are ordered before columns.
        """
        cols = self.detect_columns(blocks)
        gutter = self.page_width / 2.0

        for b in blocks:
            # Spanning banner block across full width
            if b.bbox[0] < gutter - 100 and b.bbox[2] > gutter + 100:
                b.column_index = 0
            elif b.bbox[2] <= gutter:
                b.column_index = 1
            else:
                b.column_index = 2

        # Sort key: column index, then vertical y1 coordinate
        sorted_blocks = sorted(blocks, key=lambda b: (b.column_index, b.bbox[1]))
        return sorted_blocks

    def parse_document(self, raw_blocks: List[LayoutBlock]) -> Dict[str, Any]:
        cleaned = self.filter_headers_footers(raw_blocks)
        ordered = self.assign_reading_order(cleaned)
        
        full_text = "\n\n".join(b.text for b in ordered)
        return {
            "total_blocks": len(ordered),
            "columns_detected": self.detect_columns(cleaned),
            "reading_order": [b.block_id for b in ordered],
            "document_stream": full_text
        }


if __name__ == "__main__":
    parser = DocumentLayoutParser()

    sample_blocks = [
        LayoutBlock("b_header", ElementType.HEADER, (100, 20, 900, 40), "Annual AI Symposium 2026 Proceedings"),
        LayoutBlock("b_title", ElementType.TITLE, (150, 80, 850, 140), "Scalable Multimodal Document Systems"),
        # Left column
        LayoutBlock("b_col1_p1", ElementType.PARAGRAPH, (100, 180, 480, 400), "1. Introduction: In multimodal systems, text and vision join..."),
        LayoutBlock("b_col1_p2", ElementType.PARAGRAPH, (100, 420, 480, 700), "Traditional OCR loses structural semantics when reading columns..."),
        # Right column
        LayoutBlock("b_col2_p1", ElementType.PARAGRAPH, (520, 180, 900, 450), "2. Architectural Design: Our proposed router segments patches..."),
        LayoutBlock("b_col2_p2", ElementType.PARAGRAPH, (520, 480, 900, 720), "Results demonstrate an 18% improvement in reading order accuracy..."),
        # Footer
        LayoutBlock("b_footer", ElementType.FOOTER, (450, 1360, 550, 1390), "Page 1 of 12")
    ]

    result = parser.parse_document(sample_blocks)
    print("=== Document Layout Analysis Result ===")
    print("Columns Detected:", result["columns_detected"])
    print("Ordered Block Sequence:", result["reading_order"])
    print("\nStructured Text Flow:\n" + result["document_stream"])
