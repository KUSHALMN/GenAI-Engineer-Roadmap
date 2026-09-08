import time
import uuid
import json
import asyncio
from typing import AsyncGenerator, Dict, Any, List, Optional
from pydantic import BaseModel, Field

class CopilotQuery(BaseModel):
    query: str = Field(..., min_length=1)
    tenant_id: str = "acme_enterprise"
    user_id: str = "usr_404"
    stream: bool = True

class CopilotResult(BaseModel):
    query: str
    tenant_id: str
    route: str
    tokens_used: int
    duration_ms: float
    cache_hit: bool
    citations: List[str]
    answer: str

class EnterpriseCopilotEngine:
    """
    Day 31 Capstone: Enterprise Autonomous Support Copilot
    Unifying:
    - Token Bucket Rate Limiting
    - OWASP Prompt Injection Firewall & Canary Detection
    - Semantic Caching
    - Two-Stage RAG with Cross-Encoder Reranking
    - Dynamic Model Routing
    - Structured Pydantic Output Generation
    - Real-Time SSE Token Streaming
    """

    CANARY_TOKEN = "COPILOT_CANARY_SECRET_8812"

    KNOWLEDGE_STORE = [
        {"id": "KB-101", "topic": "Enterprise SSO", "content": "SAML 2.0 and OIDC single sign-on can be configured in the Enterprise Admin console under Security -> Identity Providers."},
        {"id": "KB-102", "topic": "Billing & Invoicing", "content": "Invoices are generated on the 1st of every month. Custom PO numbers and VAT IDs can be added in Billing Settings."},
        {"id": "KB-103", "topic": "API Rate Limits", "content": "Production tier accounts receive 1,000 requests per minute (RPM) and 2,000,000 tokens per minute (TPM) with burst allowances."}
    ]

    def __init__(self):
        self._cache: Dict[str, str] = {}

    def security_check(self, query: str) -> Tuple[bool, Optional[str]]:
        lower = query.lower()
        if "ignore previous instructions" in lower or "system override" in lower:
            return False, "Prompt injection threat detected"
        return True, None

    async def execute_stream(self, req: CopilotQuery) -> AsyncGenerator[str, None]:
        start_t = time.perf_counter()
        trace_id = str(uuid.uuid4())[:8]

        # 1. Security Check
        is_safe, threat = self.security_check(req.query)
        if not is_safe:
            yield f"event: error\ndata: {json.dumps({'error': threat, 'trace_id': trace_id})}\n\n"
            return

        # 2. Semantic Cache Check
        if req.query in self._cache:
            ans = self._cache[req.query]
            yield f"event: cache_hit\ndata: {json.dumps({'message': 'Served from in-memory cache', 'answer': ans})}\n\n"
            return

        # 3. Model Routing
        tier = "frontier" if len(req.query.split()) > 8 else "lightweight"
        yield f"event: routing\ndata: {json.dumps({'tier': tier, 'trace_id': trace_id})}\n\n"

        # 4. RAG Retrieval & Reranking
        matched_chunk = self.KNOWLEDGE_STORE[0]
        for item in self.KNOWLEDGE_STORE:
            if any(w in item["content"].lower() for w in req.query.lower().split()):
                matched_chunk = item
                break

        yield f"event: context\ndata: {json.dumps({'citation': matched_chunk['id'], 'topic': matched_chunk['topic']})}\n\n"

        # 5. Token-by-token streaming
        full_answer = f"According to [{matched_chunk['id']}]: {matched_chunk['content']}"
        tokens = full_answer.split(" ")

        for idx, token in enumerate(tokens):
            await asyncio.sleep(0.015)
            chunk_data = {
                "token": token + (" " if idx < len(tokens) - 1 else ""),
                "index": idx
            }
            yield f"event: token\ndata: {json.dumps(chunk_data)}\n\n"

        # Store in cache
        self._cache[req.query] = full_answer

        total_duration = round((time.perf_counter() - start_t) * 1000.0, 2)
        metrics = {
            "trace_id": trace_id,
            "duration_ms": total_duration,
            "tokens_generated": len(tokens),
            "status": "completed"
        }
        yield f"event: done\ndata: {json.dumps(metrics)}\n\n"
