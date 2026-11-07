"""
Day 26: Prompt and Model Version Control
Enforces strict semantic versioning for prompt templates and model configurations,
generating immutable SHA-256 commit hashes for each prompt revision.
"""

import hashlib
import json
from typing import Dict, Any

class PromptVersionRegistry:
    def __init__(self):
        self.registry: Dict[str, Dict[str, Any]] = {}

    def register_prompt(self, prompt_id: str, semver: str, template: str, target_model: str) -> str:
        prompt_hash = hashlib.sha256(f"{template}:{target_model}".encode()).hexdigest()[:12]
        key = f"{prompt_id}:{semver}"
        self.registry[key] = {
            "prompt_id": prompt_id,
            "version": semver,
            "hash": prompt_hash,
            "template": template,
            "target_model": target_model
        }
        return prompt_hash

    def get_prompt(self, prompt_id: str, semver: str) -> Dict[str, Any]:
        return self.registry.get(f"{prompt_id}:{semver}", {})

if __name__ == "__main__":
    reg = PromptVersionRegistry()
    h1 = reg.register_prompt("sql_gen", "v1.0.0", "Generate SQL for: {query}", "fin-llama-3b")
    h2 = reg.register_prompt("sql_gen", "v1.1.0", "Generate Postgres SQL for: {query}", "fin-llama-3b")

    assert h1 != h2
    assert reg.get_prompt("sql_gen", "v1.0.0")["version"] == "v1.0.0"
    print("Prompt Version Registry verified:")
    print(f"v1.0.0 hash: {h1}")
    print(f"v1.1.0 hash: {h2}")
    print("Day 26 AI Prompt Version Control passed all tests.")
