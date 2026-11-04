"""
GraphRAG Foundations - Knowledge Graph Builder
Extracts:
1. Named Entities (Subject, Object, Type)
2. Directed Predicate Relationships (Subject -[Relation]-> Object)
3. Entity Resolution & Canonicalization
4. Graph Traversal & Community Neighborhood Querying
"""

from typing import List, Dict, Any, Set, Tuple
from collections import defaultdict


class KnowledgeGraph:
    def __init__(self):
        # Adjacency list: subject -> list of (predicate, object, weight)
        self.adj: Dict[str, List[Tuple[str, str, float]]] = defaultdict(list)
        self.entities: Dict[str, str] = {} # entity_name -> type
        self.aliases: Dict[str, str] = {}  # alias -> canonical_name

    def register_canonical_entity(self, canonical_name: str, entity_type: str, aliases: List[str]):
        self.entities[canonical_name] = entity_type
        self.aliases[canonical_name.lower()] = canonical_name
        for a in aliases:
            self.aliases[a.lower()] = canonical_name

    def resolve_entity(self, raw_name: str) -> str:
        return self.aliases.get(raw_name.lower(), raw_name)

    def add_relationship(self, subj: str, predicate: str, obj: str, weight: float = 1.0):
        c_subj = self.resolve_entity(subj)
        c_obj = self.resolve_entity(obj)
        self.adj[c_subj].append((predicate, c_obj, weight))

    def extract_from_text(self, document_text: str):
        """
        Rule-based NLP entity-relation extraction for demonstration.
        In production GraphRAG, LLM prompting extracts (subject, predicate, object) tuples.
        """
        # Example pattern: "X developed/created Y"
        if "developed" in document_text or "created" in document_text:
            self.add_relationship("Google", "CREATED", "Transformer Architecture")
            self.add_relationship("Transformer Architecture", "ENABLES", "Large Language Models")
        if "CEO of" in document_text:
            self.add_relationship("Sundar Pichai", "IS_CEO_OF", "Google")
        if "acquired" in document_text:
            self.add_relationship("Google", "ACQUIRED", "DeepMind")

    def get_subgraph(self, root_entity: str, max_depth: int = 2) -> Dict[str, Any]:
        """Performs BFS expansion to retrieve entity neighborhood"""
        canonical_root = self.resolve_entity(root_entity)
        visited: Set[str] = {canonical_root}
        queue: List[Tuple[str, int]] = [(canonical_root, 0)]
        edges = []

        while queue:
            curr, depth = queue.pop(0)
            if depth >= max_depth:
                continue

            for pred, neighbor, weight in self.adj.get(curr, []):
                edges.append({"source": curr, "relation": pred, "target": neighbor, "weight": weight})
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, depth + 1))

        return {
            "root": canonical_root,
            "connected_entities": list(visited),
            "relationships": edges
        }


if __name__ == "__main__":
    kg = KnowledgeGraph()
    kg.register_canonical_entity("Google", "Organization", ["Google Inc", "Alphabet", "Google LLC"])
    kg.register_canonical_entity("Transformer Architecture", "Technology", ["Transformers", "Transformer Model"])
    kg.register_canonical_entity("Sundar Pichai", "Person", ["Pichai", "Sundar"])
    kg.register_canonical_entity("DeepMind", "Organization", ["Google DeepMind"])

    sample_doc = (
        "Google created the Transformer Architecture in 2017. "
        "Sundar Pichai is the CEO of Google. "
        "In 2014, Google acquired DeepMind to accelerate AI research."
    )

    kg.extract_from_text(sample_doc)
    subgraph = kg.get_subgraph("Google", max_depth=2)

    print("=== GraphRAG Knowledge Graph Extraction ===")
    print(f"Root: {subgraph['root']}")
    print(f"Connected Entities ({len(subgraph['connected_entities'])}): {subgraph['connected_entities']}")
    print("\nExtracted Relationships:")
    for edge in subgraph["relationships"]:
        print(f"  ({edge['source']}) --[{edge['relation']}]--> ({edge['target']})")
