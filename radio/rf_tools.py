"""
SAORI TACTICAL - RF Protocol Tools, Morse Studio & Telecomms Dictionary
Herramientas tácticas de radio:
- Codificador / Decodificador de Código Morse (bidireccional con auto-detección).
- Generador de audio acústico en vivo y exportador de archivos .WAV PCM sin clicks.
- Diccionario de Códigos Q (QTH, QRM, QSL, etc.) y Abreviaturas Telegráficas (73, 88, SOS, CQ).
- Alfabeto Fonético Aeronáutico OACI / OTAN.
- Calculador de offset de repetidoras VHF/UHF y tabla de subtonos CTCSS.
- Calculador de Maidenhead Grid Locator (QTH Locator).
"""

import math
import time
import wave
import struct
from typing import Dict, List, Tuple, Optional
from pathlib import Path

# Alfabeto Fonético Aeronáutico OACI / OTAN
NATO_PHONETIC = {
    'A': 'Alpha', 'B': 'Bravo', 'C': 'Charlie', 'D': 'Delta', 'E': 'Echo',
    'F': 'Foxtrot', 'G': 'Golf', 'H': 'Hotel', 'I': 'India', 'J': 'Juliett',
    'K': 'Kilo', 'L': 'Lima', 'M': 'Mike', 'N': 'November', 'O': 'Oscar',
    'P': 'Papa', 'Q': 'Quebec', 'R': 'Romeo', 'S': 'Sierra', 'T': 'Tango',
    'U': 'Uniform', 'V': 'Victor', 'W': 'Whiskey', 'X': 'X-ray', 'Y': 'Yankee',
    'Z': 'Zulu',
    '0': 'Zero', '1': 'One', '2': 'Two', '3': 'Three', '4': 'Four',
    '5': 'Five', '6': 'Six', '7': 'Seven', '8': 'Eight', '9': 'Niner',
    '.': 'Decimal', '-': 'Dash', '/': 'Slash'
}

# Código Morse Internacional Estándar
MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
    'Z': '--..',
    '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
    '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----',
    ' ': '/', '.': '.-.-.-', ',': '--..--', '?': '..--..', '!': '-.-.--',
    ':': '---...', ';': '-.-.-.', '=': '-...-', '+': '.-.-.', '-': '-....-',
    '_': '..--.-', '"': '.-..-.', '$': '...-..-', '@': '.--.-.',
    '/': '-..-.', '(': '-.--.', ')': '-.--.-', '&': '.-...'
}

# Diccionario de Códigos Q y Señales de Tráfico de Radio
Q_CODES = {
    "QTH": "Mi ubicación / Mi posición geográfica es...",
    "QRM": "Tengo interferencia producida por otras estaciones / señales.",
    "QRN": "Tengo interferencia por ruidos estáticos / atmosféricos (ruido de fondo).",
    "QRO": "Aumentar la potencia del transmisor.",
    "QRP": "Disminuir la potencia del transmisor (operación en baja potencia).",
    "QRT": "Cesar la transmisión / Apagar la estación de radio.",
    "QRZ": "¿Quién me está llamando? (Identifíquese).",
    "QSL": "Acuse de recibo / Confirmo la recepción del mensaje.",
    "QSO": "Comunicación directa establecida entre dos estaciones.",
    "QSY": "Cambiar de frecuencia de transmisión a...",
    "QTR": "La hora exacta es...",
    "QRK": "¿Cuál es la inteligibilidad de mi señal? (Escala 1 a 5).",
    "QSB": "Su señal tiene desvanecimiento (fading / sube y baja).",
    "CQ": "Llamada general a cualquier estación en frecuencia.",
    "SOS": "Señal internacional de auxilio extremo y socorro (... --- ...)",
    "73": "Saludos cordiales entre radioaficionados.",
    "88": "Cariños y abrazos afectuosos.",
    "MAYDAY": "Llamada de socorro por voz en peligro inminente de vida.",
    "PAN-PAN": "Llamada de urgencia médica o de seguridad sin peligro inmediato de hundimiento.",
    "SECURITE": "Aviso de seguridad a la navegación o alerta meteorológica."
}

# Subtonos analógicos estándar CTCSS (EIA/TIA-603) en Hz
CTCSS_TONES = [
    67.0, 69.3, 71.9, 74.4, 77.0, 79.7, 82.5, 85.4, 88.5, 91.5,
    94.8, 97.4, 100.0, 103.5, 107.2, 110.9, 114.8, 118.8, 123.0, 127.3,
    131.8, 136.5, 141.3, 146.2, 151.4, 156.7, 162.2, 167.9, 173.8, 179.9,
    186.2, 192.8, 203.5, 206.5, 210.7, 218.1, 225.7, 233.6, 241.8, 250.3, 254.1
]


def text_to_phonetic(text: str) -> str:
    """Convierte texto o indicativo de radio a deletreo fonético OACI/OTAN."""
    out = []
    for char in text.upper():
        if char in NATO_PHONETIC:
            out.append(NATO_PHONETIC[char])
        elif char == ' ':
            out.append('/')
        else:
            out.append(char)
    return " ".join(out)


def text_to_morse(text: str) -> str:
    """Codifica texto en lenguaje natural a representación Morse estándar."""
    words = text.upper().split(' ')
    morse_words = []
    for word in words:
        morse_letters = [MORSE_CODE_DICT[c] for c in word if c in MORSE_CODE_DICT]
        if morse_letters:
            morse_words.append(" ".join(morse_letters))
    return " / ".join(morse_words)


def morse_to_text(morse: str) -> str:
    """Decodifica código Morse (puntos, rayas y barras) a texto en lenguaje natural."""
    inv_morse = {v: k for k, v in MORSE_CODE_DICT.items()}
    # Limpiar posibles caracteres equivalentes (guiones largos, guiones bajos)
    normalized = morse.replace('_', '-').replace('•', '.').replace('—', '-')
    words = normalized.strip().split('/')
    decoded_words = []
    for word in words:
        letters = word.strip().split()
        decoded_letters = [inv_morse.get(l, '?') for l in letters if l]
        decoded_words.append("".join(decoded_letters))
    return " ".join(decoded_words)


def is_morse_string(text: str) -> bool:
    """Detecta heurísticamente si una cadena de texto es código Morse."""
    stripped = text.strip()
    if not stripped:
        return False
    valid_chars = set(".- /_•—\n\r\t")
    text_chars = set(stripped)
    # Si más del 90% de los caracteres son símbolos morse, es morse
    morse_matches = sum(1 for c in stripped if c in valid_chars)
    return (morse_matches / len(stripped)) > 0.85 and ('.' in stripped or '-' in stripped)


def auto_translate(text: str) -> Dict[str, str]:
    """
    Traductor bidireccional inteligente:
    Si entra Morse -> Decodifica a lenguaje natural y entrega fonético.
    Si entra lenguaje natural -> Codifica a Morse y entrega fonético.
    """
    clean = text.strip()
    if is_morse_string(clean):
        decoded = morse_to_text(clean)
        return {
            "mode": "MORSE_TO_TEXT",
            "input": clean,
            "morse": clean,
            "text": decoded,
            "phonetic": text_to_phonetic(decoded)
        }
    else:
        encoded = text_to_morse(clean)
        return {
            "mode": "TEXT_TO_MORSE",
            "input": clean,
            "text": clean,
            "morse": encoded,
            "phonetic": text_to_phonetic(clean)
        }


def generate_morse_wav(morse: str, output_path: str, wpm: int = 15, freq_hz: int = 700) -> bool:
    """
    Genera un archivo .WAV PCM de onda senoidal pura sin clicks con envolvente trapezoidal.
    100% estándar, reproducible en cualquier dispositivo o transmisor de radio.
    """
    sample_rate = 44100
    dot_duration = 1.2 / max(5, min(wpm, 35))
    dash_duration = dot_duration * 3
    element_gap = dot_duration
    letter_gap = dot_duration * 3
    word_gap = dot_duration * 7

    def generate_tone(duration_sec: float) -> bytearray:
        n_samples = int(sample_rate * duration_sec)
        samples = bytearray()
        ramp_samples = min(int(sample_rate * 0.005), n_samples // 4) # 5ms anti-click ramp
        for i in range(n_samples):
            # Envolvente trapezoidal de ataque y decaimiento
            env = 1.0
            if i < ramp_samples:
                env = i / ramp_samples
            elif i > n_samples - ramp_samples:
                env = (n_samples - i) / ramp_samples

            val = int(32767.0 * env * 0.7 * math.sin(2.0 * math.pi * freq_hz * (i / sample_rate)))
            samples.extend(struct.pack('<h', val))
        return samples

    def generate_silence(duration_sec: float) -> bytearray:
        n_samples = int(sample_rate * duration_sec)
        return bytearray(b'\x00\x00' * n_samples)

    full_audio = bytearray()
    symbols = morse.replace('_', '-').replace('•', '.')

    for s in symbols:
        if s == '.':
            full_audio.extend(generate_tone(dot_duration))
            full_audio.extend(generate_silence(element_gap))
        elif s == '-':
            full_audio.extend(generate_tone(dash_duration))
            full_audio.extend(generate_silence(element_gap))
        elif s == ' ':
            full_audio.extend(generate_silence(letter_gap - element_gap))
        elif s == '/':
            full_audio.extend(generate_silence(word_gap - letter_gap))

    try:
        with wave.open(output_path, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2) # 16-bit
            wf.setframerate(sample_rate)
            wf.writeframes(full_audio)
        return True
    except Exception:
        return False


def play_morse_sound(morse: str, wpm: int = 15, frequency_hz: int = 700):
    """Reproduce tono Morse de emergencia vía winsound en Windows."""
    try:
        import winsound
    except ImportError:
        return False

    dot_duration = int(1200 / max(5, min(wpm, 35)))
    dash_duration = dot_duration * 3
    element_pause = dot_duration
    letter_pause = dot_duration * 3
    word_pause = dot_duration * 7

    for symbol in morse:
        if symbol == '.':
            winsound.Beep(frequency_hz, dot_duration)
            time.sleep(element_pause / 1000.0)
        elif symbol == '-':
            winsound.Beep(frequency_hz, dash_duration)
            time.sleep(element_pause / 1000.0)
        elif symbol == ' ':
            time.sleep(letter_pause / 1000.0)
        elif symbol == '/':
            time.sleep(word_pause / 1000.0)
    return True


def calculate_repeater_offset(rx_freq_mhz: float, direction: str = "+") -> Tuple[float, float, str]:
    """Calcula frecuencia de transmisión TX y offset estándar para repetidoras VHF o UHF."""
    dir_multiplier = 1.0 if direction == "+" else -1.0
    if 144.0 <= rx_freq_mhz <= 148.0:
        band = "VHF (2 Metros)"
        standard_offset = 0.600
    elif 430.0 <= rx_freq_mhz <= 450.0:
        band = "UHF (70 Centímetros)"
        standard_offset = 5.000
    else:
        band = "General / No estándar"
        standard_offset = 0.600

    tx_freq = rx_freq_mhz + (standard_offset * dir_multiplier)
    return tx_freq, standard_offset, band


def latlon_to_maidenhead(lat: float, lon: float) -> str:
    """Convierte Latitud y Longitud al localizador Maidenhead (QTH Locator) de 6 caracteres."""
    adj_lon = lon + 180.0
    adj_lat = lat + 90.0

    field_lon = int(adj_lon / 20.0)
    field_lat = int(adj_lat / 10.0)
    c1 = chr(ord('A') + field_lon)
    c2 = chr(ord('A') + field_lat)

    rem_lon = adj_lon - (field_lon * 20.0)
    rem_lat = adj_lat - (field_lat * 10.0)
    sq_lon = int(rem_lon / 2.0)
    sq_lat = int(rem_lat / 1.0)
    c3 = str(sq_lon)
    c4 = str(sq_lat)

    rem_sub_lon = (rem_lon - (sq_lon * 2.0)) * 60.0
    rem_sub_lat = (rem_lat - (sq_lat * 1.0)) * 60.0
    sub_lon = int(rem_sub_lon / 5.0)
    sub_lat = int(rem_sub_lat / 2.5)
    c5 = chr(ord('a') + max(0, min(sub_lon, 23)))
    c6 = chr(ord('a') + max(0, min(sub_lat, 23)))

    return f"{c1}{c2}{c3}{c4}{c5}{c6}"
