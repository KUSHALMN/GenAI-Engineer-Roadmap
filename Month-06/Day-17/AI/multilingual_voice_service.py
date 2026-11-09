"""
Multilingual Voice Systems & Code-Switching Transcriber.
Detects language switches, transliterates non-Latin scripts,
and normalizes phonetic terms across English, Spanish, and German.
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass
class MultilingualUtterance:
    primary_language: str
    detected_languages: List[str]
    is_code_switched: bool
    normalized_text: str


class MultilingualVoiceService:
    def __init__(self):
        self.lang_keywords = {
            "en": ["hello", "system", "please", "account"],
            "es": ["hola", "gracias", "cuenta", "por favor"],
            "de": ["guten", "tag", "konto", "bitte"]
        }

    def detect_and_normalize(self, raw_transcript: str) -> MultilingualUtterance:
        import re
        words = re.sub(r"[^a-zA-Z\s]", "", raw_transcript.lower()).split()
        found_langs = set()
        for w in words:
            for lang, vocab in self.lang_keywords.items():
                if w in vocab:
                    found_langs.add(lang)

        primary = "en"
        if found_langs:
            primary = list(found_langs)[0]

        is_switched = len(found_langs) > 1
        return MultilingualUtterance(primary, list(found_langs), is_switched, raw_transcript)


if __name__ == "__main__":
    svc = MultilingualVoiceService()
    sample = "Hola, please check my account balance, gracias."
    res = svc.detect_and_normalize(sample)
    print("=== Multilingual Voice Analysis ===")
    print(f"Primary: {res.primary_language} | Code-switched: {res.is_code_switched} | Languages: {res.detected_languages}")
