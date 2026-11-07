"""
SAORI TACTICAL - Multi-Model Fleet & Zero-VRAM Hogging Controller
Gestión inteligente de la flota de modelos locales en la RTX 4060:
1. TACTICAL (Llama 3.2 3B): Primeros auxilios, supervivencia, frecuencias de radio.
2. CODER (Qwen 2.5 Coder 3B): Scripting PowerShell/Python, diagnóstico de PC, automatización de red.
3. ANALYST (DeepSeek R1 1.5B): Razonamiento deductivo profundo y resolución analítica de problemas.

POLÍTICA ZERO-VRAM HOGGING:
- Cada inferencia usa 'keep_alive: 1m' para que el modelo se descargue solo de la GPU.
- Función unload_all_vram() purga inmediatamente cualquier modelo de la memoria de video.
- Al salir del programa, se garantiza que 0 MB de VRAM quedan ocupados.
"""

import os
import time
import subprocess
import json
import urllib.request
import urllib.error
from typing import Dict, List, Optional, Tuple
from pathlib import Path

OLLAMA_API_URL = "http://127.0.0.1:11434/api/generate"
OLLAMA_PS_URL = "http://127.0.0.1:11434/api/ps"

MODEL_FLEET = {
    "tactical": {
        "model": "llama3.2:3b",
        "name": "Operador Táctico & Supervivencia",
        "description": "Protocolos médicos MARCH, triage, radiofrecuencias y supervivencia off-grid.",
        "system": """Eres SAORI TACTICAL, asistente de operaciones de campo, radio y primeros auxilios de emergencia militar/civil (Manuales FM 21-76 y FM 4-25-11).
Proporcionas información técnica educativa de primeros auxilios y supervivencia bajo protocolos de emergencia estándar (Triage MARCH).
Directrices obligatorias:
1. Responde de forma directa, priorizada y concisa en formato paso a paso numerado.
2. Si la consulta involucra radio o comunicaciones, indica siempre la frecuencia en MHz, modo (FM/AM/LSB), banda y subtonos.
3. Señala advertencias con [PELIGRO] o [PRECAUCIÓN].
4. Idioma: Español claro y técnico."""
    },
    "coder": {
        "model": "qwen2.5-coder:3b",
        "name": "Ingeniero de Sistemas & Codeador SRE",
        "description": "Automatización en Windows, scripts PowerShell/Python, rescate de datos y diagnóstico de red.",
        "system": """Eres SAORI CODER, ingeniero de sistemas táctico y especialista en automatización de emergencias para Windows.
Tu misión es diagnosticar el hardware del PC, crear scripts de PowerShell/Python, reparar configuraciones de red, gestionar adaptadores Wi-Fi/Ethernet y solucionar fallos del sistema sin internet.
Directrices:
1. Entrega código limpio, probado y directamente ejecutable en PowerShell de Windows o Python 3.12.
2. Explica brevemente qué hace cada script sin rodeos.
3. Prioriza comandos nativos de Windows sin dependencias externas."""
    },
    "analyst": {
        "model": "deepseek-r1:1.5b",
        "name": "Analista de Razonamiento Lógico Profundo",
        "description": "Desglose deductivo de problemas complejos, fallas estructurales y planificación táctica.",
        "system": """Eres SAORI ANALYST, especialista en análisis deductivo y resolución de problemas complejos ante catástrofes.
Analizas situaciones ambiguas, evalúas riesgos en cascada y diseñas planes de contingencia paso a paso.
Directrices:
1. Desglosa el problema en premisas, factores de riesgo y cursos de acción alternativos.
2. Evalúa probabilidades y consecuencias críticas."""
    }
}


class LocalLLMEngine:
    def __init__(self, default_role: str = "tactical"):
        self.active_role = default_role
        self.endpoint = OLLAMA_API_URL

    def set_role(self, role: str) -> bool:
        if role in MODEL_FLEET:
            self.active_role = role
            return True
        return False

    def get_active_model_info(self) -> Dict:
        return MODEL_FLEET.get(self.active_role, MODEL_FLEET["tactical"])

    def is_available(self) -> bool:
        """Verifica si Ollama está respondiendo en el puerto local. Si no, lo inicia automáticamente."""
        try:
            req = urllib.request.Request("http://127.0.0.1:11434/api/tags")
            with urllib.request.urlopen(req, timeout=1.5) as resp:
                if resp.status == 200:
                    return True
        except Exception:
            pass

        possible_paths = [
            Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "Ollama" / "ollama.exe",
            Path(os.environ.get("ProgramFiles", "C:\\Program Files")) / "Ollama" / "ollama.exe"
        ]
        for p in possible_paths:
            if p.exists():
                try:
                    subprocess.Popen([str(p), "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    for _ in range(6):
                        time.sleep(1.0)
                        try:
                            req = urllib.request.Request("http://127.0.0.1:11434/api/tags")
                            with urllib.request.urlopen(req, timeout=1.0) as resp:
                                if resp.status == 200:
                                    return True
                        except Exception:
                            pass
                except Exception:
                    pass
        return False

    def generate(self, prompt: str, context: Optional[str] = None, role: Optional[str] = None) -> str:
        """Genera respuesta usando el modelo asignado al rol con política keep_alive de 1 minuto."""
        selected_role = role or self.active_role
        model_info = MODEL_FLEET.get(selected_role, MODEL_FLEET["tactical"])
        model_name = model_info["model"]
        system_prompt = model_info["system"]

        full_prompt = prompt
        if context:
            full_prompt = f"INFORMACIÓN TÁCTICA DE REFERENCIA:\n{context}\n\nCONSULTA:\n{prompt}"

        payload = {
            "model": model_name,
            "system": system_prompt,
            "prompt": full_prompt,
            "stream": False,
            "keep_alive": "1m", # Se auto-descarga de la VRAM tras 1 minuto de inactividad
            "options": {
                "temperature": 0.2 if selected_role != "analyst" else 0.4,
                "num_predict": 500,
                "top_p": 0.9
            }
        }

        data_bytes = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            self.endpoint,
            data=data_bytes,
            headers={"Content-Type": "application/json"}
        )

        try:
            with urllib.request.urlopen(req, timeout=90) as resp:
                if resp.status == 200:
                    body = json.loads(resp.read().decode("utf-8"))
                    return body.get("response", "").strip()
                raise RuntimeError(f"Ollama respondió con HTTP {resp.status}")
        except Exception as e:
            return f"[ERROR LOCAL LLM]: No fue posible obtener respuesta del modelo local ({e})."

    def unload_all_vram(self) -> bool:
        """Fuerza la descarga inmediata de TODOS los modelos de la VRAM (0 MB ocupados)."""
        success = True
        for role_key, info in MODEL_FLEET.items():
            model_name = info["model"]
            payload = json.dumps({"model": model_name, "keep_alive": 0}).encode("utf-8")
            req = urllib.request.Request(self.endpoint, data=payload, headers={"Content-Type": "application/json"})
            try:
                with urllib.request.urlopen(req, timeout=4) as resp:
                    pass
            except Exception:
                success = False
        return success

    def get_vram_status(self) -> List[Dict]:
        """Consulta qué modelos están actualmente cargados en memoria/VRAM."""
        try:
            req = urllib.request.Request(OLLAMA_PS_URL)
            with urllib.request.urlopen(req, timeout=2) as resp:
                if resp.status == 200:
                    data = json.loads(resp.read().decode("utf-8"))
                    return data.get("models", [])
        except Exception:
            pass
        return []
