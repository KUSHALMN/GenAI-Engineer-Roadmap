import asyncio
import random
from typing import Callable, Any, Dict

class ModelRateLimitError(Exception):
    pass

class ResilienceOrchestrator:
    def __init__(self, max_retries: int = 3, base_delay: float = 0.05, max_delay: float = 1.0):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay

    async def execute_with_retry(self, func: Callable, *args, **kwargs) -> Any:
        attempts = 0
        while attempts < self.max_retries:
            try:
                return await func(*args, **kwargs)
            except (ModelRateLimitError, TimeoutError):
                attempts += 1
                if attempts >= self.max_retries:
                    raise
                sleep_time = min(self.max_delay, self.base_delay * (2 ** attempts))
                await asyncio.sleep(random.uniform(0, sleep_time))

    async def execute_with_fallback(
        self, prompt: str, primary_fn: Callable, fallback_fn: Callable
    ) -> Dict[str, Any]:
        try:
            res = await self.execute_with_retry(primary_fn, prompt)
            return {"status": "success", "model_used": "primary-frontier-model", "output": res}
        except Exception as e:
            try:
                fallback_res = await fallback_fn(prompt)
                return {
                    "status": "success",
                    "model_used": "fallback-lightweight-model",
                    "output": fallback_res,
                    "fallback_reason": str(e)
                }
            except Exception as err:
                return {"status": "error", "error": str(err)}
