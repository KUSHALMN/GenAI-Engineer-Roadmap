"""
Automated Verification Suite for Month 06 (Days 01 - 10).
Tests all 10 Python multimodal microservices, ensuring structural integrity,
error metrics, and algorithmic correctness.
"""

import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
M06_DIR = REPO_ROOT / "Month-06"

# Add all daily AI directories to sys.path
for i in range(1, 11):
    day_ai_dir = M06_DIR / f"Day-{i:02d}" / "AI"
    if str(day_ai_dir) not in sys.path:
        sys.path.insert(0, str(day_ai_dir))

from multimodal_architecture_router import (
    MultimodalRouter, MultimodalRequest, ModalityPayload, ModalityType, FusionStrategy
)
from image_qa_vision_service import VisionQAService, VisionInputProcessor
from ocr_engine_comparator import MetricsCalculator, OCRComparator
from layout_parser import DocumentLayoutParser, LayoutBlock, ElementType
from table_extractor_validator import TableExtractorValidator
from chart_qa_extractor import ChartQAExtractor, ChartType
from multimodal_image_index import MultimodalImageIndex
from multimodal_rag_pipeline import MultimodalRAGPipeline
from audio_preprocess_vad import AudioPreprocessVAD
from speech_to_text_transcriber import SpeechToTextTranscriber


class TestMultimodalDays01To10(unittest.TestCase):

    def test_day01_router(self):
        router = MultimodalRouter(max_context_tokens=8192)
        payloads = [
            ModalityPayload(ModalityType.TEXT, "Check lab report"),
            ModalityPayload(ModalityType.IMAGE, "img.png", {"width": 1024, "height": 1024, "detail": "high"})
        ]
        req = MultimodalRequest("test_req", payloads, FusionStrategy.EARLY_FUSION, 4096)
        res = router.route_to_fusion(req)
        self.assertEqual(res["status"], "accepted")
        self.assertGreater(res["total_tokens"], 0)

    def test_day02_vision_qa(self):
        cost_info = VisionInputProcessor.calculate_token_cost(1920, 1080, "high")
        self.assertGreater(cost_info["total_tokens"], 100)
        self.assertGreater(cost_info["cost_usd"], 0.0)

        service = VisionQAService()
        res = service.analyze_image("sample.png", "What is total?", 1920, 1080, "high")
        self.assertGreater(len(res.detected_objects), 0)

    def test_day03_ocr_comparator(self):
        ref = "INVOICE #100"
        hyp = "INV0ICE #100"
        cer = MetricsCalculator.compute_cer(ref, hyp)
        self.assertAlmostEqual(cer, 1.0 / len(ref), places=3)

    def test_day04_layout_parser(self):
        parser = DocumentLayoutParser(1000, 1400)
        blocks = [
            LayoutBlock("h1", ElementType.HEADER, (50, 10, 950, 40), "Header Title"),
            LayoutBlock("p1", ElementType.PARAGRAPH, (100, 200, 480, 500), "Col 1 paragraph"),
            LayoutBlock("p2", ElementType.PARAGRAPH, (520, 200, 900, 500), "Col 2 paragraph")
        ]
        parsed = parser.parse_document(blocks)
        self.assertEqual(parsed["columns_detected"], 2)
        self.assertNotIn("h1", parsed["reading_order"])  # Header was filtered out

    def test_day05_table_validator(self):
        val = TableExtractorValidator()
        md = """
        | Product | Q1 | Q2 | Total |
        | :--- | :--- | :--- | :--- |
        | Widget A | 100 | 200 | 300 |
        | Widget B | 50 | 50 | 100 |
        """
        matrix = val.parse_markdown_table(md)
        report = val.validate_totals(matrix)
        self.assertTrue(report.is_valid)

        hallucinations = val.detect_hallucinations("Sales totaled 9999 units.", matrix)
        self.assertEqual(len(hallucinations), 1)

    def test_day06_chart_qa(self):
        qa = ChartQAExtractor()
        res = qa.analyze_chart("chart.png")
        self.assertEqual(res.chart_type, ChartType.LINE)
        self.assertGreater(len(res.observed_facts), 0)
        self.assertGreater(len(res.inferred_explanations), 0)

    def test_day07_multimodal_image_index(self):
        idx = MultimodalImageIndex(dim=32)
        idx.add_image("i1", "cat.png", "A cute ginger cat sitting on a rug")
        idx.add_image("i2", "server.png", "Rack of GPU computing servers in a datacenter")
        
        matches = idx.search_by_text("server cluster datacenter", top_k=1)
        self.assertEqual(len(matches), 1)

    def test_day08_multimodal_rag(self):
        rag = MultimodalRAGPipeline()
        res = rag.query("Cloud revenue", use_multimodal=True)
        self.assertTrue(res.is_multimodal)
        self.assertIn("table", res.modality_breakdown)
        self.assertIn("image", res.modality_breakdown)

    def test_day09_audio_vad(self):
        vad = AudioPreprocessVAD()
        samples = [0.0] * 16000 + [0.8] * 16000 + [0.0] * 16000
        voiced = vad.detect_voice_activity(samples)
        self.assertGreaterEqual(len(voiced), 1)
        self.assertAlmostEqual(voiced[0].start_time, 1.0, delta=0.1)

    def test_day10_speech_to_text(self):
        stt = SpeechToTextTranscriber()
        res = stt.transcribe("speech.wav", filter_hallucinations=True)
        self.assertEqual(res.language, "en")
        self.assertGreater(len(res.segments), 0)
        srt = stt.export_srt(res)
        self.assertIn("-->", srt)


if __name__ == "__main__":
    unittest.main()
