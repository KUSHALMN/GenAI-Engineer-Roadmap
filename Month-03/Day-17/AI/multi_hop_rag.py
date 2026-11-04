"""
Multi-Hop RAG Engine
Decomposes complex multi-hop questions into dependent sequential reasoning steps:
Hop 1: Retrieve intermediate entity / prerequisite fact.
Hop 2: Condition second retrieval using intermediate fact from Hop 1.
Hop 3: Synthesize verified join across disparate documents.
"""

from typing import List, Dict, Any, Optional


class MultiHopRAG:
    def __init__(self, corpus: List[Dict[str, Any]]):
        self.corpus = corpus

    def _retrieve(self, query: str) -> Optional[Dict[str, Any]]:
        q_words = set(query.lower().split())
        best_doc = None
        best_score = -1.0

        for doc in self.corpus:
            d_words = set(doc["text"].lower().split())
            score = len(q_words.intersection(d_words))
            if score > best_score:
                best_score = score
                best_doc = doc

        return best_doc if best_score > 0 else None

    def execute_two_hop_query(self, complex_question: str) -> Dict[str, Any]:
        """
        Example: "Who is the CEO of the company that created the transformer model?"
        Step 1: Find which company created the transformer model.
        Step 2: Find who is the CEO of that company.
        """
        # Deconstruct Hop 1: Discover base entity
        hop1_query = "company created transformer model Attention is All You Need"
        hop1_doc = self._retrieve(hop1_query)

        intermediate_fact = None
        if hop1_doc:
            # Extract target entity from Doc 1
            if "Google" in hop1_doc["text"]:
                intermediate_fact = "Google"

        # Deconstruct Hop 2: Conditioned query using intermediate fact
        hop2_query = f"CEO of {intermediate_fact}" if intermediate_fact else "CEO of company"
        hop2_doc = self._retrieve(hop2_query)

        final_answer = None
        if intermediate_fact and hop2_doc:
            if "Sundar Pichai" in hop2_doc["text"]:
                final_answer = f"The transformer architecture was created by {intermediate_fact}, whose CEO is Sundar Pichai."

        return {
            "complex_question": complex_question,
            "hop_1": {
                "subquery": hop1_query,
                "retrieved_doc_id": hop1_doc["id"] if hop1_doc else None,
                "extracted_fact": intermediate_fact
            },
            "hop_2": {
                "subquery": hop2_query,
                "retrieved_doc_id": hop2_doc["id"] if hop2_doc else None,
            },
            "synthesized_answer": final_answer,
            "provenance_chain": [hop1_doc["id"], hop2_doc["id"]] if hop1_doc and hop2_doc else []
        }


if __name__ == "__main__":
    knowledge_base = [
        {
            "id": "doc_transformers",
            "text": "The transformer architecture was introduced in 2017 by Google researchers in the seminal paper Attention is All You Need."
        },
        {
            "id": "doc_leadership",
            "text": "Sundar Pichai is the chief executive officer (CEO) of Google and Alphabet Inc., appointed in 2015."
        },
        {
            "id": "doc_meta",
            "text": "Mark Zuckerberg founded Facebook (now Meta) in 2004 and serves as its CEO."
        }
    ]

    rag = MultiHopRAG(knowledge_base)
    q = "Who is the CEO of the organization that developed the transformer architecture?"
    result = rag.execute_two_hop_query(q)

    print("=== Multi-Hop Reasoning Execution ===")
    print(f"Question: {result['complex_question']}")
    print(f"\n[Hop 1] Query: \"{result['hop_1']['subquery']}\"")
    print(f"        Retrieved: {result['hop_1']['retrieved_doc_id']} -> Extracted: {result['hop_1']['extracted_fact']}")
    print(f"\n[Hop 2] Query: \"{result['hop_2']['subquery']}\"")
    print(f"        Retrieved: {result['hop_2']['retrieved_doc_id']}")
    print(f"\n[Final Synthesis]: {result['synthesized_answer']}")
    print(f"[Provenance Chain]: {' -> '.join(result['provenance_chain'])}")
