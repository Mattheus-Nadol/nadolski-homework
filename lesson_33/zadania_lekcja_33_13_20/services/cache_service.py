"""
Cache service module (production-safer version).

Odpowiada za:
- przechowywanie cache w pamięci
- ładowanie cache z pliku JSON przy starcie aplikacji
- zapisywanie cache do JSON przy shutdown

Poprawki:
- bezpieczne zarządzanie plikami (context manager)
- async-safe executor usage
- brak leaków event loop
"""

import json
import os
import asyncio
from typing import Any, Dict


class CacheService:
    def __init__(self, cache_file: str = "data/cache.json"):
        self.cache_file = cache_file
        self._cache: Dict[str, Any] = {}
        self._lock = asyncio.Lock()

    async def load_cache(self) -> None:
        """Load cache from JSON file into memory."""
        if not os.path.exists(self.cache_file):
            self._cache = {}
            return

        async with self._lock:
            try:
                def read_file():
                    with open(self.cache_file, "r", encoding="utf-8") as f:
                        return json.load(f)

                loop = asyncio.get_running_loop()
                data = await loop.run_in_executor(None, read_file)

                self._cache = data if isinstance(data, dict) else {}

            except Exception:
                self._cache = {}

    async def save_cache(self) -> None:
        """Save memory cache into JSON file."""
        os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)

        async with self._lock:
            def write_file():
                with open(self.cache_file, "w", encoding="utf-8") as f:
                    json.dump(
                        self._cache,
                        f,
                        ensure_ascii=False,
                        indent=2
                    )

            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, write_file)

    async def get(self, key: str, default: Any = None) -> Any:
        return self._cache.get(key, default)

    async def set(self, key: str, value: Any) -> None:
        async with self._lock:
            self._cache[key] = value

    async def delete(self, key: str) -> None:
        async with self._lock:
            self._cache.pop(key, None)

    async def clear(self) -> None:
        async with self._lock:
            self._cache.clear()


# Singleton instance
cache_service = CacheService()