"""
Graph Retrieval vs Vector Retrieval Benchmark Engine
Compares:
1. Vector Retrieval: Measures semantic similarity via dense vector cosine distance.
2. Graph Traversal: Traverses multi-hop entity relationships and path connectivity.
3. Hybrid Graph-Vector Retrieval: Combines entity-linked neighborhood expansion with vector scoring.
"""

from typing import List, Dict, Any, Set


class GraphVsVectorBenchmark:
    def __init__(self):
        # Knowledge Graph edges
        self.graph = {
            "OpenAI": [("FOUNDED_BY", "Sam Altman"), ("RELEASED", "ChatGPT"), ("PARTNERED_WITH", "Microsoft")],
            "Microsoft": [("INVESTED_IN", "OpenAI"), ("INTEGRATED", "ChatGPT")],
            "Sam Altman": [("LED", "OpenAI"), ("FOUNDED", "Worldcoin")]
        }

        # Text chunks for Vector Retrieval
        self.chunks = [
            {"id": "doc_1", "text": "OpenAI was co-founded by Sam Altman in San Francisco and released ChatGPT."},
            {"id": "doc_2", "text": "Microsoft invested billions of dollars into OpenAI and integrated ChatGPT into Office products."},
            {"id": "doc_3", "text": "Sam Altman also co-founded Worldcoin to provide biometric proof-of-personhood."}
        ]

    def vector_search(self, query: str) -> List[Dict[str, Any]]:
        """Simulates bi-encoder dense keyword/semantic matching"""
        q_words = set(query.lower().split())
        scored = []
        for c in self.chunks:
            d_words = set(c["text"].lower().split())
            sim = len(q_words.intersection(d_words)) / max(1, len(q_words))
            scored.append({"id": c["id"], "score": round(sim, 3), "text": c["text"]})
        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored

    def graph_traversal(self, start_entity: str, hops: int = 2) -> List[str]:
        """Breadth-first relationship expansion across knowledge graph"""
        visited: Set[str] = {start_entity}
        queue = [(start_entity, 0)]
        paths = []

        while queue:
            curr, depth = queue.pop(0)
            if depth >= hops:
                continue

            for rel, target in self.graph.get(curr, []):
                paths.append(f"{curr} -[{rel}]-> {target}")
                if target not in visited:
                    visited.add(target)
                    queue.append((target, depth + 1))

        return paths

    def hybrid_graph_vector(self, query: str, seed_entity: str) -> Dict[str, Any]:
        """Combines structural relational paths with retrieved evidence text"""
        graph_facts = self.graph_traversal(seed_entity, hops=2)
        vector_hits = self.vector_search(query)

        return {
            "query": query,
            "seed_entity": seed_entity,
            "structured_relationships": graph_facts,
            "top_vector_evidence": vector_hits[:2]
        }


if __name__ == "__main__":
    benchmark = GraphVsVectorBenchmark()

    query = "How is Microsoft connected to Sam Altman?"

    print("=== Pure Vector Retrieval ===")
    v_results = benchmark.vector_search(query)
    for r in v_results:
        print(f"[{r['id']}] Score: {r['score']} -> {r['text']}")

    print("\n=== Pure Graph Traversal ===")
    g_results = benchmark.graph_traversal("Microsoft", hops=2)
    for path in g_results:
        print(f"Path: {path}")

    print("\n=== Hybrid Graph-Vector Retrieval ===")
    hybrid = benchmark.hybrid_graph_vector(query, "Microsoft")
    print("Graph Context:")
    for fact in hybrid["structured_relationships"]:
        print(f"  * {fact}")
    print("Vector Documents:")
    for doc in hybrid["top_vector_evidence"]:
        print(f"  * [{doc['id']}] {doc['text']}")
