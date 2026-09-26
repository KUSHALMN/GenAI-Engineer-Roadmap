"""
System Metrics Tool for MCP Server.
Provides safe, read-only system telemetry (platform, CPU architecture, timestamp).
"""

import os
import platform
import time
from typing import Any, Dict


def get_system_metrics() -> Dict[str, Any]:
    """Retrieve system hardware, OS, and timestamp metrics."""
    return {
        "os": platform.system(),
        "release": platform.release(),
        "architecture": platform.machine(),
        "processor": platform.processor(),
        "python_version": platform.python_version(),
        "timestamp_epoch": time.time(),
        "cpu_count": os.cpu_count() or 1,
    }


def get_tool_definition() -> Dict[str, Any]:
    """MCP tool definition schema."""
    return {
        "name": "get_system_metrics",
        "description": "Returns host OS, CPU architecture, and telemetry data.",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    }
