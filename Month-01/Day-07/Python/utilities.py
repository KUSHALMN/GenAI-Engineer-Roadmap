import time
import functools
from typing import Any

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f}s")
        return result
    return wrapper

def retry(max_attempts=3, delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Attempt {attempt} failed: {e}")
                    if attempt < max_attempts:
                        time.sleep(delay)
            raise Exception(f"{func.__name__} failed after {max_attempts} attempts")
        return wrapper
    return decorator

def flatten(nested: list) -> list:
    result = []
    for item in nested:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result

def batch(items: list, size: int) -> list:
    return [items[i:i + size] for i in range(0, len(items), size)]

# Test
if __name__ == "__main__":
    @timer
    def slow_function():
        time.sleep(0.1)
        return "done"

    slow_function()
    print(flatten([1, [2, [3, 4]], 5]))
    print(batch([1, 2, 3, 4, 5, 6, 7], 3))
