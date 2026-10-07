"""Production Observable RAG Pipeline with End-to-End Tracing."""
import os
import sys
import time

# Ensure Day-24 root is on Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from observability.request_id import set_request_id, get_request_id
from observability.logger import get_logger, log_event
from observability.latency import LatencyTracker
from observability.cost_tracker import CostTracker
from observability.metrics import MetricsAggregator

logger = get_logger("observable.rag")


class ObservableRAGPipeline:
    """An end-to-end RAG system instrumented with structured logging, latency spans, and cost tracking."""

    def __init__(self, model_name: str = "llama-3.3-70b-versatile"):
        self.model_name = model_name
        self.cost_tracker = CostTracker()
        self.metrics = MetricsAggregator()
        self.documents = [
            {"id": "doc1", "title": "Vector Databases", "content": "Vector databases index embeddings for nearest neighbor search using HNSW or IVF."},
            {"id": "doc2", "title": "RAG Observability", "content": "Observability in LLMs requires distributed tracing, latency breakdown, cost per token, and hallucination monitoring."},
            {"id": "doc3", "title": "LLM Reliability", "content": "Reliability frameworks employ exponential backoff retry, circuit breakers, and fallback models to prevent downtime."}
        ]

    def retrieve(self, query: str, top_k: int = 2) -> List[Dict[str, Any]]:
        """Simulate semantic retrieval with observability instrumentation."""
        tokens = set(query.lower().split())
        scored = []
        for doc in self.documents:
            doc_tokens = set(doc["content"].lower().split())
            overlap = len(tokens.intersection(doc_tokens))
            score = round(overlap / (len(tokens) + 1e-5), 4)
            scored.append((score, doc))

        scored.sort(key=lambda x: x[0], reverse=True)
        results = [doc for score, doc in scored[:top_k]]
        top_score = scored[0][0] if scored else 0.0
        self.metrics.record_retrieval(top_score)
        return results

    def generate(self, query: str, retrieved_docs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Simulate LLM generation and record token costs."""
        context = " ".join([d["content"] for d in retrieved_docs])
        prompt = f"Context: {context}\nQuery: {query}\nAnswer:"
        
        # Approximate token count (4 chars ~ 1 token)
        prompt_tokens = max(10, len(prompt) // 4)
        
        # Mock LLM generation output
        if "observability" in query.lower():
            answer = "LLM observability requires distributed tracing, latency profiling, token cost calculation, and hallucination evaluation."
        elif "vector" in query.lower():
            answer = "Vector databases utilize HNSW and IVF algorithms to power high-speed semantic similarity search."
        else:
            answer = f"Based on the knowledge base: {context[:120]}..."

        completion_tokens = max(15, len(answer) // 4)
        usage = self.cost_tracker.record_usage(
            model=self.model_name,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            request_id=get_request_id()
        )
        return {
            "answer": answer,
            "usage": usage
        }

    def query(self, user_query: str, request_id: Optional[str] = None) -> Dict[str, Any]:
        """Execute end-to-end query span with full tracing."""
        active_req_id = set_request_id(request_id)
        log_event(logger, "INFO", "Received RAG query", query=user_query, request_id=active_req_id)

        with LatencyTracker("rag_end_to_end", active_req_id) as tracker:
            # Stage 1: Retrieval
            retrieval_start = time.perf_counter()
            docs = self.retrieve(user_query)
            tracker.mark("retrieval_complete")
            log_event(logger, "INFO", "Documents retrieved", count=len(docs), doc_ids=[d["id"] for d in docs])

            # Stage 2: Synthesis
            gen_start = time.perf_counter()
            gen_result = self.generate(user_query, docs)
            tracker.mark("generation_complete")

        self.metrics.record_call(tracker.duration_ms, success=True)
        log_event(logger, "INFO", "RAG query completed successfully",
                  duration_ms=tracker.duration_ms,
                  cost_usd=gen_result["usage"]["cost_usd"])

        return {
            "request_id": active_req_id,
            "query": user_query,
            "answer": gen_result["answer"],
            "retrieved_docs": docs,
            "latency": tracker.to_dict(),
            "cost": gen_result["usage"],
        }


if __name__ == "__main__":
    pipeline = ObservableRAGPipeline()
    response = pipeline.query("How does RAG observability work in production?")
    print("\n--- RAG PIPELINE EXECUTION SUMMARY ---")
    print("Request ID :", response["request_id"])
    print("Answer     :", response["answer"])
    print("Duration   :", response["latency"]["duration_ms"], "ms")
    print("Cost (USD) :", f"${response['cost']['cost_usd']:.6f}")
    print("Aggregate  :", pipeline.metrics.compute_summary())
