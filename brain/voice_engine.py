"""
SAORI TACTICAL - Hybrid Voice Engine (Offline Windows SAPI + Online ElevenLabs)
Capacidad de síntesis por voz sin depender de la nube:
- Modo Offline: Motor nativo de Windows (System.Speech / SAPI) con 0% de uso de red y 0 tokens.
- Modo Online: ElevenLabs (Sarah / Multilingual v2) o Edge-TTS cuando hay internet disponible.
"""

import os
import subprocess
import threading
from typing import Optional


class TacticalVoiceEngine:
    def __init__(self, elevenlabs_api_key: Optional[str] = None):
        self.elevenlabs_api_key = elevenlabs_api_key or os.environ.get("ELEVENLABS_API_KEY", "")

    def speak_offline_sapi(self, text: str, async_mode: bool = True):
        """Síntesis de voz 100% offline nativa de Windows (System.Speech.Synthesis)."""
        # Limpiar texto de caracteres problemáticos para PowerShell
        clean_text = text.replace('"', ' ').replace("'", " ").replace("\n", " ").strip()
        ps_code = f"""
Add-Type -AssemblyName System.Speech
$speak = New-Object System.Speech.Synthesis.SpeechSynthesizer
$speak.Rate = 1
$speak.Volume = 100
$speak.Speak("{clean_text}")
"""
        cmd = ["powershell", "-NoProfile", "-Command", ps_code]
        if async_mode:
            threading.Thread(target=lambda: subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL), daemon=True).start()
        else:
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def speak(self, text: str, is_online: bool = False):
        """Selecciona inteligentemente el motor según el estado de conectividad."""
        if not is_online or not self.elevenlabs_api_key:
            # Fallback inmediato offline nativo
            self.speak_offline_sapi(text, async_mode=True)
            return

        # Si está online y hay key de ElevenLabs, intentar audio de alta calidad o SAPI de respaldo
        try:
            from elevenlabs import ElevenLabs
            client = ElevenLabs(api_key=self.elevenlabs_api_key)
            audio_generator = client.text_to_speech.convert(
                text=text[:350],
                voice_id="EXAVITQu4vr4xnSDxMaL", # Sarah
                model_id="eleven_multilingual_v2"
            )
            import tempfile
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
                temp_mp3 = f.name
                for chunk in audio_generator:
                    f.write(chunk)
            
            # Reproducir mp3 con ffmpeg o PowerShell
            cmd = ["powershell", "-NoProfile", "-Command", f"(New-Object Media.SoundPlayer '{temp_mp3}').PlaySync()"]
            threading.Thread(target=lambda: subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL), daemon=True).start()
        except Exception:
            self.speak_offline_sapi(text, async_mode=True)
