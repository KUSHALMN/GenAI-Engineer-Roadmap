"""
Core Agent & RAG Service for Day-20 Capstone.
Integrates Caching, Hybrid Knowledge Retrieval, Tool Calling, and Telemetry.
"""

import hashlib
import json
import time
from typing import Any, Dict, List, Optional, Tuple
from schemas import AgentTaskType, CapstoneQueryRequest, CapstoneQueryResponse, CitationItem
from security_guardrails import SecurityGuardrails


class CapstoneAgentService:
    """Production service coordinating RAG, Tools, and Caching."""

    def __init__(self):
        self.cache: Dict[str, Tuple[Dict[str, Any], float]] = {}  # key -> (response_dict, expiry_time)
        self.start_epoch = time.time()
        self.cache_ttl_seconds = 3600.0

        # In-memory knowledge base
        self.knowledge_base = [
            {"id": "kb_01", "topic": "caching", "content": "Exact match caching uses SHA-256 hashes of canonical query parameters to reduce latency to <1ms."},
            {"id": "kb_02", "topic": "rag", "content": "Advanced RAG utilizes HyDE, BM25 + dense hybrid search, and cross-encoder reranking to achieve high recall."},
            {"id": "kb_03", "topic": "security", "content": "GenAI security requires input sanitization, XML framing, output secret validation, and least-privilege tool execution."},
            {"id": "kb_04", "topic": "inference", "content": "Dynamic continuous batching and PagedAttention in vLLM maximize GPU throughput while minimizing KV cache memory fragmentation."},
        ]

    def _generate_cache_key(self, request: CapstoneQueryRequest) -> str:
        payload = f"{request.query.strip().lower()}:{request.task_type.value}:{request.temperature}"
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def _execute_calculator(self, query: str) -> Optional[float]:
        """Simple calculator tool parsing basic arithmetic."""
        words = query.split()
        for i, w in enumerate(words):
            if w in ("+", "-", "*", "/") and i > 0 and i < len(words) - 1:
                try:
                    a = float(words[i - 1].strip("(),"))
                    b = float(words[i + 1].strip("(),"))
                    if w == "+": return a + b
                    if w == "-": return a - b
                    if w == "*": return a * b
                    if w == "/" and b != 0: return a / b
                except ValueError:
                    continue
        return None

    def _search_knowledge(self, query: str) -> List[Dict[str, str]]:
        """Hybrid term overlap retrieval."""
        q_words = set(query.lower().split())
        scored = []
        for doc in self.knowledge_base:
            doc_words = set(doc["content"].lower().split())
            overlap = len(q_words.intersection(doc_words))
            if overlap > 0:
                scored.append((doc, overlap))
        scored.sort(key=lambda x: x[1], reverse=True)
        return [item[0] for item in scored[:2]]

    def process_query(self, request: CapstoneQueryRequest) -> CapstoneQueryResponse:
        start_time = time.perf_counter()

        # 1. Guardrail input validation
        is_safe, reason = SecurityGuardrails.validate_input(request.query)
        if not is_safe:
            return CapstoneQueryResponse(
                query=request.query,
                answer=f"Request blocked by safety policy: {reason}",
                task_type=request.task_type.value,
                cached=False,
                latency_ms=round((time.perf_counter() - start_time) * 1000, 2),
                estimated_cost_usd=0.0,
                session_id=request.session_id or "sess_default",
                status="blocked",
            )

        # 2. Check Cache
        cache_key = self._generate_cache_key(request)
        now = time.time()
        if not request.bypass_cache and cache_key in self.cache:
            cached_data, expiry = self.cache[cache_key]
            if now < expiry:
                cached_resp = CapstoneQueryResponse(**cached_data)
                cached_resp.cached = True
                cached_resp.latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
                return cached_resp

        # 3. Mask PII in user query
        sanitized_query, _ = SecurityGuardrails.mask_pii(request.query)

        tools_executed = []
        citations = []
        answer = ""

        # 4. Routing & Execution
        if request.task_type == AgentTaskType.CALCULATION:
            calc_val = self._execute_calculator(sanitized_query)
            if calc_val is not None:
                tools_executed.append("calculator_engine")
                answer = f"Calculation result: {calc_val}"
            else:
                answer = f"Processed calculation request: {sanitized_query}"
        elif request.task_type in (AgentTaskType.RESEARCH, AgentTaskType.DOCUMENT_QA):
            tools_executed.append("hybrid_vector_retriever")
            relevant_docs = self._search_knowledge(sanitized_query)
            if relevant_docs:
                for doc in relevant_docs:
                    citations.append(CitationItem(source_id=doc["id"], snippet=doc["content"][:100]))
                snippets_text = " ".join(d["content"] for d in relevant_docs)
                answer = f"Synthesis from verified knowledge: {snippets_text}"
            else:
                answer = f"General knowledge answer for query: '{sanitized_query}'."
        else:
            # General task
            answer = f"Processed general instruction: '{sanitized_query}' with zero-temperature greedy decoding."

        duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
        token_count = len(sanitized_query.split()) + len(answer.split())
        cost = round((token_count / 1000.0) * 0.0002, 6)

        response = CapstoneQueryResponse(
            query=request.query,
            answer=answer,
            task_type=request.task_type.value,
            cached=False,
            latency_ms=duration_ms,
            estimated_cost_usd=cost,
            citations=citations,
            tools_executed=tools_executed,
            session_id=request.session_id or "sess_default",
            status="success",
        )

        # Store in cache
        self.cache[cache_key] = (response.model_dump(), now + self.cache_ttl_seconds)

        return response

    def get_cache_size(self) -> int:
        return len(self.cache)

    def get_uptime_seconds(self) -> float:
        return round(time.time() - self.start_epoch, 2)
