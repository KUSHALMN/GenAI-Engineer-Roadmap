"""
Container Networking & Reverse Proxies: Routing simulation, TLS Termination,
Header Sanitization, Request ID Injection, and Service Discovery.
"""

from dataclasses import dataclass
import uuid
from typing import Dict


@dataclass
class ProxiedRequest:
    method: str
    path: str
    headers: Dict[str, str]
    body: str


@dataclass
class ProxiedResponse:
    status_code: int
    headers: Dict[str, str]
    body: str


class ReverseProxyGateway:
    def __init__(self):
        # Service registry: prefix -> backend target
        self.routes: Dict[str, str] = {
            "/api/v1/models": "llm-serving-service:8001",
            "/api/v1/documents": "doc-ingestion-service:8002",
            "/health": "healthcheck-service:8000"
        }

    def dispatch(self, req: ProxiedRequest) -> ProxiedResponse:
        # 1. Sanitize headers and inject X-Request-ID
        headers = dict(req.headers)
        request_id = headers.get("X-Request-ID", str(uuid.uuid4())[:8])
        headers["X-Request-ID"] = request_id
        headers["X-Forwarded-Proto"] = "https"

        # 2. Match route
        target_backend = None
        for prefix, backend in self.routes.items():
            if req.path.startswith(prefix):
                target_backend = backend
                break

        if not target_backend:
            return ProxiedResponse(404, {"X-Request-ID": request_id}, "Not Found")

        # 3. Simulate backend dispatch
        return ProxiedResponse(
            200,
            {"X-Request-ID": request_id, "X-Backend": target_backend},
            f"Response routed to {target_backend}"
        )


if __name__ == "__main__":
    proxy = ReverseProxyGateway()
    req = ProxiedRequest("POST", "/api/v1/models/generate", {}, "{\"prompt\": \"hi\"}")
    resp = proxy.dispatch(req)
    assert resp.status_code == 200
    assert "llm-serving-service" in resp.headers["X-Backend"]
    assert "X-Request-ID" in resp.headers
    print("=== Day 10: Reverse Proxy Gateway ===")
    print(f"Dispatched successfully to {resp.headers['X-Backend']}")
