"""
Multilingual & Cross-Lingual Retrieval Engine
Demonstrates:
1. ISO language identification (English, Spanish, French, German)
2. Cross-lingual dense semantic alignment
3. Transliteration / vocabulary normalization
4. Cross-language search: query in English, retrieve matching conceptual documents in Spanish/French
"""

import math
from typing import List, Dict, Any, Tuple


class MultilingualSearchEngine:
    def __init__(self, corpus: List[Dict[str, Any]]):
        self.corpus = corpus
        # Cross-lingual semantic dictionary mapping concepts across languages to a shared semantic ID
        self.semantic_concept_map = {
            "database": 1, "base de datos": 1, "base de données": 1, "datenbank": 1,
            "search": 2, "búsqueda": 2, "recherche": 2, "suche": 2,
            "security": 3, "seguridad": 3, "sécurité": 3, "sicherheit": 3,
            "cloud": 4, "nube": 4, "nuage": 4, "wolke": 4
        }

    def detect_language(self, text: str) -> str:
        """Fast heuristic language detection based on common function words"""
        t = text.lower()
        if any(w in t.split() for w in ["el", "la", "de", "en", "para", "datos", "búsqueda"]):
            return "es"
        elif any(w in t.split() for w in ["le", "la", "des", "données", "sécurité", "pour"]):
            return "fr"
        elif any(w in t.split() for w in ["der", "die", "das", "und", "für", "datenbank"]):
            return "de"
        return "en"

    def _cross_lingual_embed(self, text: str) -> List[float]:
        """
        Simulates multilingual embedding (e.g. Cohere Multilingual v3 / BGE-M3)
        mapping cross-lingual synonyms to identical vector coordinates.
        """
        vec = [0.0] * 8
        words = text.lower().split()
        for i in range(len(words)):
            # Check single word or bigram in concept map
            w1 = words[i]
            w2 = f"{words[i]} {words[i+1]}" if i + 1 < len(words) else ""
            w3 = f"{words[i]} {words[i+1]} {words[i+2]}" if i + 2 < len(words) else ""

            for phrase in [w3, w2, w1]:
                if phrase in self.semantic_concept_map:
                    cid = self.semantic_concept_map[phrase]
                    vec[cid % 8] += 2.0

        # Base lexical hash for residual words
        for w in words:
            vec[hash(w) % 8] += 0.2

        norm = math.sqrt(sum(x * x for x in vec)) or 1.0
        return [x / norm for x in vec]

    def search_cross_lingual(self, query: str, top_k: int = 3) -> Dict[str, Any]:
        q_lang = self.detect_language(query)
        q_vec = self._cross_lingual_embed(query)

        scored = []
        for doc in self.corpus:
            d_vec = self._cross_lingual_embed(doc["text"])
            sim = sum(a * b for a, b in zip(q_vec, d_vec))
            scored.append({
                "id": doc["id"],
                "text": doc["text"],
                "doc_language": self.detect_language(doc["text"]),
                "similarity": round(sim, 4)
            })

        scored.sort(key=lambda x: x["similarity"], reverse=True)

        return {
            "query": query,
            "detected_query_language": q_lang,
            "results": scored[:top_k]
        }


if __name__ == "__main__":
    multilingual_corpus = [
        {"id": "doc_en", "text": "Cloud database search engine with vector similarity and security encryption."},
        {"id": "doc_es", "text": "Motor de búsqueda para base de datos en la nube con seguridad avanzada."},
        {"id": "doc_fr", "text": "Base de données cloud avec recherche vectorielle et sécurité des données."},
        {"id": "doc_de", "text": "Sichere Datenbank in der Wolke mit schneller Suche."},
        {"id": "doc_unrelated", "text": "Recipe for chocolate chip cookies with organic butter and flour."}
    ]

    engine = MultilingualSearchEngine(multilingual_corpus)

    # Query in English, expecting relevant hits in Spanish, French, and German!
    q = "cloud database search security"
    out = engine.search_cross_lingual(q, top_k=4)

    print("=== Multilingual Cross-Lingual Retrieval Demonstration ===")
    print(f"Query: \"{out['query']}\" (Detected: {out['detected_query_language']})")
    print("\nRetrieved Cross-Lingual Documents:")
    for doc in out["results"]:
        print(f"  * [{doc['id']} | Lang: {doc['doc_language']} | Sim: {doc['similarity']}] -> \"{doc['text']}\"")
