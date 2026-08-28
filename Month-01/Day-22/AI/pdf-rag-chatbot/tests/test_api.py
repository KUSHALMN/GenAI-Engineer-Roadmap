from fastapi.testclient import TestClient
from app.main import app, pipeline

client = TestClient(app)

def setup_state():
    """Reset pipeline state before tests."""
    pipeline.clear()

def test_health_endpoint():
    setup_state()
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "indexed_chunks" in data
    print("test_health_endpoint passed")

def test_ingest_text_and_query():
    setup_state()
    # 1. Ingest text
    ingest_payload = {
        "title": "architecture_guide.txt",
        "content": "FastAPI is an asynchronous Python web framework providing high performance on ASGI servers."
    }
    ingest_resp = client.post("/api/v1/ingest-text", json=ingest_payload)
    assert ingest_resp.status_code == 200
    assert ingest_resp.json()["filename"] == "architecture_guide.txt"
    assert ingest_resp.json()["chunk_count"] > 0

    # 2. Query the ingested document
    query_payload = {
        "question": "What is FastAPI?",
        "top_k": 2
    }
    query_resp = client.post("/api/v1/query", json=query_payload)
    assert query_resp.status_code == 200
    result = query_resp.json()
    assert "answer" in result
    assert len(result["citations"]) > 0
    assert result["citations"][0]["source"] == "architecture_guide.txt"
    print("test_ingest_text_and_query passed")

def test_query_empty_error():
    setup_state()
    query_resp = client.post("/api/v1/query", json={"question": "   "})
    assert query_resp.status_code == 400
    print("test_query_empty_error passed")

def test_streaming_query():
    setup_state()
    # Ingest document first
    client.post("/api/v1/ingest-text", json={
        "title": "streaming_doc.txt",
        "content": "Server-Sent Events allow continuous unidirectional streaming from server to browser."
    })

    # Test stream response
    with client.stream("POST", "/api/v1/query/stream", json={"question": "How does SSE work?"}) as response:
        assert response.status_code == 200
        assert "text/event-stream" in response.headers["content-type"]
        events = list(response.iter_lines())
        assert len(events) > 0
    print("test_streaming_query passed")

def test_documents_stats_and_clear():
    setup_state()
    client.post("/api/v1/ingest-text", json={
        "title": "doc1.txt",
        "content": "First indexed piece of content."
    })
    
    # Check stats
    stats_resp = client.get("/api/v1/documents")
    assert stats_resp.status_code == 200
    stats = stats_resp.json()
    assert stats["total_documents"] == 1
    assert stats["total_chunks"] >= 1

    # Clear
    del_resp = client.delete("/api/v1/documents")
    assert del_resp.status_code == 200
    
    empty_stats = client.get("/api/v1/documents").json()
    assert empty_stats["total_documents"] == 0
    assert empty_stats["total_chunks"] == 0
    print("test_documents_stats_and_clear passed")

if __name__ == "__main__":
    test_health_endpoint()
    test_ingest_text_and_query()
    test_query_empty_error()
    test_streaming_query()
    test_documents_stats_and_clear()
    print("All API Integration Tests Passed Successfully!")
