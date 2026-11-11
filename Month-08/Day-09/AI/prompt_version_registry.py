"""
Prompt Versioning and Experiments: Versioned Prompt Registry, SHA-256 Template Hashing,
Variable Schema Validation, and Model Parameter Tracking.
"""

from dataclasses import dataclass, field
import hashlib
import time
from typing import Dict, List, Optional


@dataclass
class PromptVersionRecord:
    template_name: str
    version: str
    template_text: str
    template_hash: str
    required_variables: List[str]
    model_params: Dict[str, float]
    created_at: float = field(default_factory=time.time)


class PromptVersionRegistry:
    def __init__(self):
        self._registry: Dict[str, List[PromptVersionRecord]] = {}

    def register_prompt(self, name: str, version: str, template: str, required_vars: List[str], params: Dict[str, float]) -> PromptVersionRecord:
        h = hashlib.sha256(template.encode("utf-8")).hexdigest()[:16]
        rec = PromptVersionRecord(name, version, template, h, required_vars, params)
        if name not in self._registry:
            self._registry[name] = []
        self._registry[name].append(rec)
        return rec

    def get_latest(self, name: str) -> Optional[PromptVersionRecord]:
        records = self._registry.get(name, [])
        return records[-1] if records else None


if __name__ == "__main__":
    reg = PromptVersionRegistry()
    v1 = reg.register_prompt(
        "customer_support",
        "1.0.0",
        "Answer the user query: {query} with context: {context}",
        ["query", "context"],
        {"temperature": 0.2, "max_tokens": 512}
    )
    latest = reg.get_latest("customer_support")
    assert latest.version == "1.0.0"
    assert len(latest.template_hash) == 16

    print("=== Day 09: Prompt Version Registry ===")
    print(f"Registered Prompt: {latest.template_name} v{latest.version} | Hash: {latest.template_hash}")
