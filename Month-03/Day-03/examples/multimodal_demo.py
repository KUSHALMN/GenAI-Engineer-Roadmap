"""Multimodal System Integration Demo (OCR, Audio, TTS, Image QA, Multimodal RAG)."""
import sys
import os

# Ensure Day-03 root is on python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from multimodal.ocr_pipeline import OCRPipeline
from multimodal.audio_to_text import AudioToTextTranscriber
from multimodal.text_to_speech import TextToSpeechSynthesizer
from multimodal.image_qa import ImageQAPipeline
from multimodal.multimodal_rag import MultimodalRAG


def run_demo():
    print("==================================================")
    print(" Month 03 Day 03: Multimodal GenAI Pipeline Demo")
    print("==================================================")

    # 1. OCR Extraction
    ocr = OCRPipeline()
    ocr_result = ocr.extract_text("invoice_sample.pdf")
    print(f"\n[1] OCR Pipeline Result:")
    print(f"    Extracted: {ocr_result['raw_text'].splitlines()[:2]}")

    # 2. Audio Transcription
    asr = AudioToTextTranscriber()
    audio_res = asr.transcribe("speech_sample.wav")
    print(f"\n[2] Audio ASR Transcription:")
    print(f"    Transcript: '{audio_res['full_transcript'][:60]}...'")

    # 3. Text to Speech
    tts = TextToSpeechSynthesizer()
    tts_res = tts.synthesize("Your invoice payment was received successfully.")
    print(f"\n[3] Text-To-Speech Synthesis:")
    print(f"    Format: {tts_res['format']}, Duration: {tts_res['duration_sec']}s, Status: {tts_res['status']}")

    # 4. Image QA
    vlm = ImageQAPipeline()
    vlm_res = vlm.answer_question("invoice_sample.png", "What is the total due amount?")
    print(f"\n[4] Vision-Language Model QA:")
    print(f"    Answer: {vlm_res['answer']}")

    # 5. Multimodal RAG
    mm_rag = MultimodalRAG()
    rag_res = mm_rag.query("What is the invoice amount due?")
    print(f"\n[5] Multimodal RAG Query:")
    print(f"    Response: {rag_res['response']} (Source: {rag_res['source_type']})")

    print("\nAll multimodal components executed successfully! [OK]")


if __name__ == "__main__":
    run_demo()
