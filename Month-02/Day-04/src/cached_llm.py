"""
cached_llm.py — LLM wrapper that checks cache before making API calls.
Tracks cost savings from cache hits.
"""
import os
import time
from groq import Groq
from llm_cache import LLMCache

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# Approximate cost per 1M tokens (input) for LLaMA3-8B on Groq
COST_PER_1M_TOKENS = 0.05
AVG_TOKENS_PER_REQUEST = 350


class CachedLLM:
    def __init__(self, model: str = "llama3-8b-8192", ttl: float = 3600.0):
        self.model = model
        self.cache = LLMCache(default_ttl=ttl)
        self.client = Groq(api_key=GROQ_API_KEY)
        self.api_calls = 0
        self.tokens_saved = 0

    def complete(self, prompt: str, temperature: float = 0.0) -> dict:
        cached = self.cache.get(prompt, self.model, temperature)
        if cached:
            self.tokens_saved += AVG_TOKENS_PER_REQUEST
            return {"response": cached, "source": "cache", "latency_ms": 0}

        start = time.time()
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
        )
        latency = round((time.time() - start) * 1000, 2)
        text = resp.choices[0].message.content
        self.cache.set(prompt, self.model, text, temperature)
        self.api_calls += 1
        return {"response": text, "source": "api", "latency_ms": latency}

    @property
    def cost_saved(self) -> float:
        return round(self.tokens_saved / 1_000_000 * COST_PER_1M_TOKENS, 6)

    @property
    def stats(self) -> dict:
        return {
            **self.cache.stats,
            "api_calls": self.api_calls,
            "tokens_saved": self.tokens_saved,
            "cost_saved_usd": self.cost_saved,
        }


if __name__ == "__main__":
    llm = CachedLLM()
    prompts = [
        "What is RAG in AI?",
        "What is RAG in AI?",   # cache hit
        "Explain LoRA fine-tuning.",
        "What is RAG in AI?",   # cache hit again
    ]
    for p in prompts:
        result = llm.complete(p)
        print(f"[{result['source'].upper()}] {p[:40]}... ({result['latency_ms']}ms)")
    print("\nStats:", llm.stats)
