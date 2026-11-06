"""
Day 17: MCP Resources and Prompts
Exposes read-only resources (URI-based document access) and reusable prompt templates
as specified by the Model Context Protocol.
"""

from typing import Dict, Any, List
import json

class MCPResourceManager:
    def __init__(self):
        self.resources: Dict[str, Dict[str, Any]] = {}
        self.prompts: Dict[str, Dict[str, Any]] = {}

    def register_resource(self, uri: str, name: str, mime_type: str, content: str):
        self.resources[uri] = {
            "uri": uri,
            "name": name,
            "mimeType": mime_type,
            "content": content
        }

    def register_prompt(self, name: str, description: str, arguments: List[str], template: str):
        self.prompts[name] = {
            "name": name,
            "description": description,
            "arguments": arguments,
            "template": template
        }

    def list_resources(self) -> List[Dict[str, Any]]:
        return [{"uri": r["uri"], "name": r["name"], "mimeType": r["mimeType"]} for r in self.resources.values()]

    def read_resource(self, uri: str) -> Dict[str, Any]:
        if uri not in self.resources:
            raise KeyError(f"Resource '{uri}' not found.")
        r = self.resources[uri]
        return {"contents": [{"uri": uri, "mimeType": r["mimeType"], "text": r["content"]}]}

    def render_prompt(self, name: str, args: Dict[str, str]) -> str:
        if name not in self.prompts:
            raise KeyError(f"Prompt '{name}' not found.")
        template = self.prompts[name]["template"]
        for k, v in args.items():
            template = template.replace(f"{{{k}}}", v)
        return template

if __name__ == "__main__":
    mgr = MCPResourceManager()

    # Register resource
    mgr.register_resource("system://metrics/cpu", "CPU Metrics", "text/plain", "CPU Utilization: 42%")
    # Register prompt
    mgr.register_prompt(
        "summarize_code",
        "Summarize code snippet",
        ["language", "code"],
        "Please provide a concise overview of the following {language} code:\n\n{code}"
    )

    # Read resource
    res = mgr.read_resource("system://metrics/cpu")
    assert "42%" in res["contents"][0]["text"]

    # Render prompt
    rendered = mgr.render_prompt("summarize_code", {"language": "Java", "code": "class Hello {}"})
    assert "Java code" in rendered

    print(f"Read Resource: {res}")
    print(f"Rendered Prompt: {rendered}")
    print("Day 17 AI MCP Resources & Prompts passed all tests.")
