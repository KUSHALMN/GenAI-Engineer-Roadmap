import time
import uuid
import json
import asyncio
from typing import AsyncGenerator, Tuple, Optional
from pydantic import BaseModel, Field

class CopilotQuery(BaseModel):
    query: str = Field(..., min_length=1)
    tenant_id: str = "acme_corp"

class EnterpriseCopilotEngine:
    KNOWLEDGE_STORE = [
        {"id": "KB-101", "topic": "Enterprise SSO", "content": "SAML 2.0 and OIDC single sign-on can be configured in the Enterprise Admin console."},
        {"id": "KB-102", "topic": "Billing & Invoicing", "content": "Invoices are generated on the 1st of every month in Billing Settings."}
    ]

    def __init__(self):
        self._cache = {}

    def security_check(self, query: str) -> Tuple[bool, Optional[str]]:
        if "ignore previous instructions" in query.lower() or "system override" in query.lower():
            return False, "Prompt injection threat detected"
        return True, None

    async def execute_stream(self, req: CopilotQuery) -> AsyncGenerator[str, None]:
        start_t = time.perf_counter()
        is_safe, threat = self.security_check(req.query)
        if not is_safe:
            yield f"event: error\ndata: {json.dumps({'error': threat})}\n\n"
            return

        if req.query in self._cache:
            yield f"event: cache_hit\ndata: {json.dumps({'answer': self._cache[req.query]})}\n\n"
            return

        matched = self.KNOWLEDGE_STORE[0]
        yield f"event: context\ndata: {json.dumps({'citation': matched['id']})}\n\n"

        full_answer = f"According to [{matched['id']}]: {matched['content']}"
        tokens = full_answer.split(" ")
        for idx, token in enumerate(tokens):
            await asyncio.sleep(0.01)
            yield f"event: token\ndata: {json.dumps({'token': token + ' ', 'index': idx})}\n\n"

        self._cache[req.query] = full_answer
        yield f"event: done\ndata: {json.dumps({'duration_ms': round((time.perf_counter() - start_t) * 1000, 2)})}\n\n"
