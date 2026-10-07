"""Model Context Protocol (MCP) JSON-RPC 2.0 Schemas."""
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict


@dataclass
class MCPToolDefinition:
    name: str
    description: str
    input_schema: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class MCPResourceDefinition:
    uri: str
    name: str
    description: str
    mime_type: str = "text/plain"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class JSONRPCRequest:
    jsonrpc: str = "2.0"
    id: str = "1"
    method: str = ""
    params: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class JSONRPCResponse:
    jsonrpc: str = "2.0"
    id: str = "1"
    result: Optional[Any] = None
    error: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
