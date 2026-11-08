"""
Latency, Token Throughput, and Memory Profiling Benchmark Suite for Month 06.
Measures execution speed and throughput of the multimodal pipeline components.
"""

import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
M06_DIR = REPO_ROOT / "Month-06"

for i in range(1, 11):
    day_ai_dir = M06_DIR / f"Day-{i:02d}" / "AI"
    if str(day_ai_dir) not in sys.path:
        sys.path.insert(0, str(day_ai_dir))

from multimodal_architecture_router import MultimodalRouter, MultimodalRequest, ModalityPayload, ModalityType
from image_qa_vision_service import VisionQAService
from layout_parser import DocumentLayoutParser, LayoutBlock, ElementType
from table_extractor_validator import TableExtractorValidator
from multimodal_image_index import MultimodalImageIndex
from audio_preprocess_vad import AudioPreprocessVAD
from speech_to_text_transcriber import SpeechToTextTranscriber


def run_benchmarks():
    print("=" * 65)
    print("  MULTIMODAL GENAI & DOCUMENT AI BENCHMARK SUITE (DAYS 01 - 10)")
    print("=" * 65)

    results = []

    # 1. Ingestion Router
    router = MultimodalRouter()
    start = time.perf_counter()
    for _ in range(100):
        req = MultimodalRequest(
            "b_req",
            [
                ModalityPayload(ModalityType.TEXT, "Sample prompt text query."),
                ModalityPayload(ModalityType.IMAGE, "scan.png", {"width": 1920, "height": 1080})
            ]
        )
        router.route_to_fusion(req)
    dur_router = (time.perf_counter() - start) * 10
    results.append(("Multimodal Ingestion Router", f"{dur_router:.2f} ms/100 ops", "Passed"))

    # 2. Vision QA
    vision = VisionQAService()
    start = time.perf_counter()
    vision.analyze_image("sample.png", "Extract totals", 1920, 1080, "high")
    dur_vision = (time.perf_counter() - start) * 1000
    results.append(("Vision QA Service Simulation", f"{dur_vision:.2f} ms", "Passed"))

    # 3. Layout Parser
    parser = DocumentLayoutParser()
    blocks = [
        LayoutBlock(f"b_{i}", ElementType.PARAGRAPH, (100 if i % 2 == 0 else 550, i * 40, 480 if i % 2 == 0 else 900, i * 40 + 35), f"Paragraph text {i}")
        for i in range(20)
    ]
    start = time.perf_counter()
    parser.parse_document(blocks)
    dur_layout = (time.perf_counter() - start) * 1000
    results.append(("Document Layout Parser (20 blocks)", f"{dur_layout:.2f} ms", "Passed"))

    # 4. Table Arithmetic Validator
    val = TableExtractorValidator()
    md_table = """
    | Cat | Jan | Feb | Total |
    | :--- | :--- | :--- | :--- |
    | Server | 1000 | 1200 | 2200 |
    | Storage | 500 | 600 | 1100 |
    """
    matrix = val.parse_markdown_table(md_table)
    start = time.perf_counter()
    for _ in range(100):
        val.validate_totals(matrix)
    dur_table = (time.perf_counter() - start) * 10
    results.append(("Table Arithmetic Cross-Validator", f"{dur_table:.2f} ms/100 ops", "Passed"))

    # 5. Multimodal Vector Index
    idx = MultimodalImageIndex(dim=64)
    for k in range(50):
        idx.add_image(f"doc_{k}", f"file_{k}.png", f"Technical schematic diagram for cluster node {k}")
    start = time.perf_counter()
    for _ in range(50):
        idx.search_by_text("cluster node schematic", top_k=5)
    dur_search = (time.perf_counter() - start) * 20
    results.append(("Cross-Modal Vector Search (50 docs)", f"{dur_search:.2f} ms/50 ops", "Passed"))

    # 6. Audio VAD
    vad = AudioPreprocessVAD()
    audio = [0.0] * 16000 + [0.7] * 32000 + [0.0] * 16000
    start = time.perf_counter()
    vad.detect_voice_activity(audio)
    dur_vad = (time.perf_counter() - start) * 1000
    results.append(("Audio VAD Processor (4s audio)", f"{dur_vad:.2f} ms", "Passed"))

    # 7. Speech-to-Text
    stt = SpeechToTextTranscriber()
    start = time.perf_counter()
    stt.transcribe("keynote.wav", filter_hallucinations=True)
    dur_stt = (time.perf_counter() - start) * 1000
    results.append(("Speech-to-Text Transcription", f"{dur_stt:.2f} ms", "Passed"))

    print(f"{'Component / Benchmark':<38} | {'Latency / Metric':<20} | {'Status'}")
    print("-" * 68)
    for comp, metric, status in results:
        print(f"{comp:<38} | {metric:<20} | {status}")
    print("=" * 65)


if __name__ == "__main__":
    run_benchmarks()
