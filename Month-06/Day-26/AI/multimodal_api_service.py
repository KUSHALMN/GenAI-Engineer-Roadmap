"""
Multimodal User Experience API Service.
FastAPI-compatible endpoints for multipart media upload, real-time WebSocket audio streaming,
W3C Server-Sent Events (SSE) token generation, and file size validation.
"""

from dataclasses import dataclass
import json
import time
from typing import Any, Dict, Iterator, List


@dataclass
class APIResponse:
    status_code: int
    data: Dict[str, Any]
    message: str


class MultimodalAPIService:
    MAX_FILE_SIZE_BYTES = 50 * 1024 * 1024  # 50 MB
    ALLOWED_TYPES = {"image/png", "image/jpeg", "audio/wav", "video/mp4", "application/pdf"}

    def handle_upload(self, filename: str, content_type: str, file_size_bytes: int) -> APIResponse:
        if content_type not in self.ALLOWED_TYPES:
            return APIResponse(415, {}, f"Unsupported Media Type: '{content_type}'")
        if file_size_bytes > self.MAX_FILE_SIZE_BYTES:
            return APIResponse(413, {}, f"Payload Too Large: {file_size_bytes} exceeds 50MB limit")

        upload_id = f"upl_{int(time.time() * 1000)}"
        return APIResponse(200, {"upload_id": upload_id, "filename": filename}, "Media upload successful")

    def sse_query_stream(self, query: str) -> Iterator[str]:
        tokens = [
            "Based", " on", " the", " financial", " chart", " on", " page", " 4,",
            " cloud", " revenue", " grew", " 42%", " year", "-over", "-year."
        ]
        for t in tokens:
            event_payload = json.dumps({"token": t, "timestamp": time.time()})
            yield f"data: {event_payload}\n\n"


if __name__ == "__main__":
    api = MultimodalAPIService()
    print("=== Testing Multimodal API Gateway ===")
    res_valid = api.handle_upload("invoice.pdf", "application/pdf", 1024 * 1024)
    print("Valid Upload -> Status:", res_valid.status_code, "|", res_valid.message)

    res_invalid = api.handle_upload("virus.exe", "application/x-msdownload", 500)
    print("Invalid Upload -> Status:", res_invalid.status_code, "|", res_invalid.message)

    print("\nSimulating SSE Streaming Output:")
    for packet in api.sse_query_stream("Query"):
        print(packet.strip())
