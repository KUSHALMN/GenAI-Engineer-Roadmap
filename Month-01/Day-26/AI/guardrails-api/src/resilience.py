import asyncio
import random
from typing import Callable, Any, Dict, List

class ModelRateLimitError(Exception):
    pass

class ModelUnavailableError(Exception):
    pass

class ResilienceOrchestrator:
    """
    Manages exponential backoff retries with full jitter and multi-model fallback cascades.
    Primary Model (e.g. gpt-4o / Claude 3.5) -> Fallback Model (e.g. gpt-4o-mini / LLaMA-3)
    """

    def __init__(self, max_retries: int = 3, base_delay: float = 0.05, max_delay: float = 1.0):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay

    async def execute_with_retry(self, func: Callable, *args, **kwargs) -> Any:
        attempts = 0
        while attempts < self.max_retries:
            try:
                return await func(*args, **kwargs)
            except (ModelRateLimitError, TimeoutError) as e:
                attempts += 1
                if attempts >= self.max_retries:
                    raise
                # Exponential backoff with full jitter
                sleep_time = min(self.max_delay, self.base_delay * (2 ** attempts))
                jittered_sleep = random.uniform(0, sleep_time)
                await asyncio.sleep(jittered_sleep)

    async def execute_with_fallback(
        self,
        prompt: str,
        primary_callable: Callable,
        fallback_callable: Callable
    ) -> Dict[str, Any]:
        """
        Executes primary callable with retries; upon exhaustion or fatal outage,
        automatically cascades to fallback callable.
        """
        try:
            res = await self.execute_with_retry(primary_callable, prompt)
            return {"status": "success", "model_used": "primary-frontier-model", "output": res}
        except (ModelRateLimitError, ModelUnavailableError, Exception) as primary_err:
            # Cascade to fallback model
            try:
                fallback_res = await fallback_callable(prompt)
                return {
                    "status": "success",
                    "model_used": "fallback-lightweight-model",
                    "output": fallback_res,
                    "fallback_reason": str(primary_err)
                }
            except Exception as fallback_err:
                return {
                    "status": "error",
                    "error": f"Both primary and fallback failed: {str(fallback_err)}"
                }
