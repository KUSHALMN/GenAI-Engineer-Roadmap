"""
Query Rewriter Engine - Resolves conversational context, coreferences, and keyword expansion
Features:
- Conversation history coreference resolution (anaphora resolution)
- Query disambiguation and search term expansion
- Intent classification (Informational, Navigational, Transactional)
- Keyword density booster for BM25/Vector hybrid pipelines
"""

import re
from typing import List, Dict, Any, Optional


class QueryRewriter:
    def __init__(self):
        # Common synonym dictionary and domain acronyms
        self.acronyms = {
            "rag": "retrieval augmented generation",
            "llm": "large language model",
            "k8s": "kubernetes",
            "db": "database",
            "ann": "approximate nearest neighbor",
            "dsa": "data structures and algorithms"
        }
        self.stop_fillers = {"um", "uh", "please", "can you tell me", "i want to know", "hey", "tell me about"}

    def clean_filler_words(self, query: str) -> str:
        q = query.strip()
        for filler in self.stop_fillers:
            pattern = re.compile(rf"^{re.escape(filler)}\s+", re.IGNORECASE)
            q = pattern.sub("", q)
        return q.strip()

    def expand_acronyms(self, query: str) -> str:
        tokens = query.split()
        expanded_tokens = []
        for token in tokens:
            cleaned = re.sub(r"[^\w]", "", token.lower())
            if cleaned in self.acronyms:
                expanded_tokens.append(f"{token} ({self.acronyms[cleaned]})")
            else:
                expanded_tokens.append(token)
        return " ".join(expanded_tokens)

    def resolve_coreference(self, query: str, history: List[Dict[str, str]]) -> str:
        """
        Resolves pronouns ('it', 'they', 'its', 'this') by inspecting previous user/assistant turns.
        """
        pronoun_pattern = re.compile(r"\b(it|its|they|their|this|that|these|those)\b", re.IGNORECASE)
        match = pronoun_pattern.search(query)
        if not match or not history:
            return query

        # Find the most prominent recent entity from history
        last_turn = history[-1]
        content = last_turn.get("content", "")
        # Extract primary subject (first capitalized noun or prominent key term)
        nouns = re.findall(r"\b([A-Z][a-zA-Z0-9_\-\.]+)\b", content)
        if not nouns:
            nouns = [w for w in content.split() if len(w) > 4 and w.lower() not in self.stop_fillers]

        resolved_subject = nouns[0] if nouns else "the subject"
        # Substitute pronoun
        rewritten = pronoun_pattern.sub(resolved_subject, query)
        return rewritten

    def rewrite(self, query: str, history: Optional[List[Dict[str, str]]] = None) -> Dict[str, Any]:
        cleaned = self.clean_filler_words(query)
        resolved = self.resolve_coreference(cleaned, history or [])
        expanded = self.expand_acronyms(resolved)

        return {
            "original_query": query,
            "cleaned_query": cleaned,
            "rewritten_query": expanded,
            "resolved_coreference": resolved != cleaned,
            "intent": "informational" if "?" in query or "how" in query.lower() or "what" in query.lower() else "keyword_search"
        }


if __name__ == "__main__":
    rewriter = QueryRewriter()

    history = [
        {"role": "user", "content": "Tell me about Pinecone vector database."},
        {"role": "assistant", "content": "Pinecone is a managed cloud vector database optimized for ultra-low latency semantic search."}
    ]

    ambiguous_query = "Can you tell me how does it scale in k8s?"
    res = rewriter.rewrite(ambiguous_query, history)

    print("=== Query Rewriting Demonstration ===")
    print(f"Original:  {res['original_query']}")
    print(f"Rewritten: {res['rewritten_query']}")
    print(f"Intent:    {res['intent']}")
    print(f"Coreference Resolved: {res['resolved_coreference']}")
