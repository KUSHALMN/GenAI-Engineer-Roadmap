"""MCP Resources provider exposing read-only data assets via URIs."""
from typing import Dict, Any, List, Optional
from .schemas import MCPResourceDefinition


class MCPResourceManager:
    """Manages static and dynamic context resources under URI schemes."""

    def __init__(self):
        self.resources = {
            "system://config/environment": {
                "name": "Environment Configuration",
                "description": "Cluster runtime environment and hardware telemetry",
                "content": '{"cluster": "production-us-east", "gpu_type": "H100", "cuda_version": "12.4"}'
            },
            "docs://company/policy": {
                "name": "Corporate AI Guidelines",
                "description": "Safety protocols and data privacy rules",
                "content": "All customer PII must be encrypted in transit and scrubbed prior to model training."
            }
        }

    def list_resources(self) -> List[MCPResourceDefinition]:
        return [
            MCPResourceDefinition(
                uri=uri,
                name=data["name"],
                description=data["description"],
                mime_type="application/json" if uri.startswith("system://") else "text/plain"
            )
            for uri, data in self.resources.items()
        ]

    def read_resource(self, uri: str) -> Optional[str]:
        if uri in self.resources:
            return self.resources[uri]["content"]
        return None
