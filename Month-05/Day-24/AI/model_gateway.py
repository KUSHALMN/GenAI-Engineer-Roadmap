"""
Day 24: Model Gateway and Provider Abstraction
Unified multi-provider client with circuit-breaking fallback:
Attempts primary model (local vLLM), falls back to cloud provider on failure.
"""

from typing import Dict, Any, Callable

class ModelGateway:
    def __init__(self):
        self.providers: Dict[str, Callable[[str], str]] = {}

    def register_provider(self, name: str, handler: Callable[[str], str]):
        self.providers[name] = handler

    def complete(self, prompt: str, primary: str = "local_vllm", fallback: str = "cloud_llm") -> Dict[str, Any]:
        try:
            if primary in self.providers:
                res = self.providers[primary](prompt)
                return {"provider_used": primary, "output": res, "fallback": False}
        except Exception:
            pass

        # Fallback
        if fallback in self.providers:
            res = self.providers[fallback](prompt)
            return {"provider_used": fallback, "output": res, "fallback": True}

        raise RuntimeError("All providers in gateway failed.")

if __name__ == "__main__":
    gw = ModelGateway()

    def failing_vllm(p: str): raise ConnectionError("GPU node offline")
    def healthy_cloud(p: str): return f"Cloud response for '{p}'"

    gw.register_provider("local_vllm", failing_vllm)
    gw.register_provider("cloud_llm", healthy_cloud)

    res = gw.complete("Summarize earnings")
    assert res["fallback"] is True
    assert res["provider_used"] == "cloud_llm"
    print(f"Gateway successfully routed with fallback: {res}")
    print("Day 24 AI Model Gateway passed all tests.")
