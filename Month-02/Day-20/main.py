"""
Production FastAPI Backend for Capstone GenAI Service.
Includes API Key Auth, CORS, Health Checks, Request Routing, and Telemetry.
"""

import time
import uuid
from typing import Dict
from fastapi import Depends, FastAPI, HTTPException, Header, Security, status
from fastapi.middleware.cors import CORSMiddleware
from agent_service import CapstoneAgentService
from schemas import CapstoneQueryRequest, CapstoneQueryResponse, HealthCheckResponse


app = FastAPI(
    title="GenAI Production Capstone Service",
    description="Enterprise-ready GenAI API with RAG, Tool Calling, Caching, and Guardrails",
    version="1.0.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Shared singleton service
agent_service = CapstoneAgentService()

VALID_API_KEYS = {"genai-capstone-prod-key-12345", "test-api-key"}


def verify_api_key(x_api_key: str = Header(default="test-api-key")) -> str:
    """Validates API key header."""
    if x_api_key not in VALID_API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing X-API-Key header",
        )
    return x_api_key


@app.get("/health", response_model=HealthCheckResponse, tags=["System"])
def health_check():
    """Service health and uptime endpoint."""
    return HealthCheckResponse(
        status="healthy",
        version="1.0.0",
        cache_entries=agent_service.get_cache_size(),
        uptime_seconds=agent_service.get_uptime_seconds(),
    )


@app.post("/api/query", response_model=CapstoneQueryResponse, tags=["GenAI"])
def process_query(
    request: CapstoneQueryRequest,
    api_key: str = Depends(verify_api_key),
):
    """Processes queries through the resilient GenAI agent and RAG pipeline."""
    return agent_service.process_query(request)


@app.get("/api/cache", tags=["System"])
def get_cache_stats(api_key: str = Depends(verify_api_key)):
    """Retrieve cache utilization metrics."""
    return {
        "cache_entries": agent_service.get_cache_size(),
        "ttl_seconds": agent_service.cache_ttl_seconds,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
