from retrieval.chunking import RecursiveChunker
from retrieval.vector_store import VectorStore
from retrieval.hybrid_retriever import HybridRetriever, BM25Retriever
from retrieval.pdf_loader import PDFLoader
from app.rag_pipeline import RAGPipeline

def test_recursive_chunker():
    chunker = RecursiveChunker(chunk_size=100, chunk_overlap=20)
    sample_text = (
        "Retrieval-Augmented Generation (RAG) combines dense semantic vector search "
        "with modern generative models to ground responses in verified external knowledge. "
        "It prevents hallucination and allows dynamic knowledge updates."
    )
    pages = [{"page_number": 1, "text": sample_text, "source": "test.pdf"}]
    chunks = chunker.split_pages(pages)

    assert len(chunks) >= 2
    assert all("chunk_id" in c for c in chunks)
    assert all(c["page_number"] == 1 for c in chunks)
    assert all(c["source"] == "test.pdf" for c in chunks)
    print("test_recursive_chunker passed")


def test_vector_store():
    store = VectorStore(dimension=64)
    chunks = [
        {"chunk_id": "c1", "text": "Python is a high level programming language for AI and machine learning.", "source": "py.txt", "page_number": 1},
        {"chunk_id": "c2", "text": "Java is an object oriented language compiled to bytecode on JVM.", "source": "java.txt", "page_number": 1},
        {"chunk_id": "c3", "text": "Kubernetes is an open source container orchestration platform.", "source": "k8s.txt", "page_number": 1}
    ]
    store.add_chunks(chunks)
    assert store.count() == 3

    results = store.search("Python machine learning", top_k=1)
    assert len(results) == 1
    assert results[0][0]["chunk_id"] == "c1"
    assert results[0][1] > 0.0
    print("test_vector_store passed")


def test_hybrid_retriever():
    store = VectorStore(dimension=64)
    retriever = HybridRetriever(vector_store=store, rrf_k=60)
    chunks = [
        {"chunk_id": "doc1", "text": "FastAPI is a modern web framework for building APIs with Python 3.8+.", "source": "fastapi.md", "page_number": 1},
        {"chunk_id": "doc2", "text": "PostgreSQL is a powerful relational database supporting JSON queries.", "source": "postgres.md", "page_number": 1}
    ]
    retriever.index(chunks)

    retrieved = retriever.retrieve("FastAPI web framework", top_k=2)
    assert len(retrieved) == 2
    assert retrieved[0]["chunk_id"] == "doc1"
    assert "hybrid_rrf_score" in retrieved[0]
    print("test_hybrid_retriever passed")


def test_rag_pipeline_end_to_end():
    pipeline = RAGPipeline()
    pipeline.clear()
    
    doc_content = (
        "Transformer architecture relies on self-attention mechanisms to compute "
        "representations of input sequences without using sequence-aligned RNNs or convolution."
    )
    meta = pipeline.ingest_text(doc_content, filename="attention.txt")
    assert meta["chunk_count"] > 0

    res = pipeline.query("What does Transformer architecture rely on?", top_k=2)
    assert "answer" in res
    assert len(res["citations"]) > 0
    assert res["citations"][0]["source"] == "attention.txt"
    assert res["latency_ms"] >= 0.0
    print("test_rag_pipeline_end_to_end passed")

if __name__ == "__main__":
    test_recursive_chunker()
    test_vector_store()
    test_hybrid_retriever()
    test_rag_pipeline_end_to_end()
    print("All RAG Unit Tests Passed Successfully!")
