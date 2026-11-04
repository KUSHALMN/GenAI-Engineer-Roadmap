# Notes: Multilingual Retrieval & Cross-Lingual Semantic Search

## 1. Cross-Lingual Embedding Alignment
Modern multilingual encoders (such as `BGE-M3` and `cohere.embed-multilingual-v3.0`) project sentences from 100+ languages into a shared language-agnostic latent space:
- The vector distance between "Cloud database security" (English) and "Seguridad de bases de datos en la nube" (Spanish) is minimal because their conceptual coordinates align.
- **Transliteration & Romanization**: For languages like Hindi, Arabic, or Russian written in Latin script (e.g. Hinglish / Arabizi), sub-word tokenizers (Byte-Pair Encoding with shared vocabularies) map phonemes and morphemes across scripts.

## 2. Inverted Index Limitations in Multilingual
Sparse keyword search (BM25) fails completely across languages because English tokens ("security") share zero lexical intersection with Spanish tokens ("seguridad"). Cross-lingual search strictly relies on multilingual dense representations or machine translation query pre-processors.
