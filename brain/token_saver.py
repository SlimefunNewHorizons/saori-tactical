"""
SAORI TACTICAL - Token Saver & High-Density Telegraphic Compressor
Diseñado para enlaces móviles restringidos, satélite y máxima velocidad de respuesta.
- Caché semántico local para no repetir consultas idénticas (0 tokens).
- Compresión de prompts eliminando florituras y texto decorativo.
- Presupuestador de ancho de banda y caracteres.
"""

import hashlib
import time
from typing import Dict, Optional


class TokenSaver:
    def __init__(self, ttl_seconds: int = 3600):
        self.cache: Dict[str, Dict] = {}
        self.ttl_seconds = ttl_seconds
        self.total_tokens_saved: int = 0

    def _hash_query(self, query: str) -> str:
        clean = "".join(query.lower().split())
        return hashlib.sha256(clean.encode("utf-8")).hexdigest()

    def get_cached(self, query: str) -> Optional[str]:
        h = self._hash_query(query)
        entry = self.cache.get(h)
        if entry:
            if time.time() - entry["timestamp"] < self.ttl_seconds:
                self.total_tokens_saved += entry.get("estimated_tokens", 50)
                return entry["response"]
            else:
                del self.cache[h]
        return None

    def store_cache(self, query: str, response: str):
        h = self._hash_query(query)
        self.cache[h] = {
            "response": response,
            "timestamp": time.time(),
            "estimated_tokens": len(response.split())
        }

    def compress_prompt(self, text: str) -> str:
        """Comprime el prompt eliminando palabras vacías y formalidades innecesarias."""
        replacements = [
            ("por favor", ""),
            ("podrías decirme", ""),
            ("quisiera saber", ""),
            ("necesito que me digas", ""),
            ("muchas gracias", ""),
            ("hola saori", ""),
            ("hola", "")
        ]
        compressed = text.lower()
        for r, rep in replacements:
            compressed = compressed.replace(r, rep)
        return " ".join(compressed.split())
