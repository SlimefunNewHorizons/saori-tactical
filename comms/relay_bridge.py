"""
SAORI TACTICAL - Mobile Relay & Reverse Tethering Bridge
Integra conceptos de Mahdi-mortazavi/relay (https://github.com/Mahdi-mortazavi/relay):
Permite compartir los datos móviles (4G/5G) o Wi-Fi de un teléfono Android con este PC Windows
a través de USB o Hotspot local con túnel cifrado P2P sin necesidad de Root.
"""

from typing import Dict

RELAY_INFO = {
    "project": "Mahdi-mortazavi/relay",
    "url": "https://github.com/Mahdi-mortazavi/relay",
    "description": "Herramienta P2P para compartir conexión móvil Android hacia Windows sin root.",
    "quickstart": [
        "1. Conectar el teléfono Android al PC vía cable USB.",
        "2. En Android: Ajustes -> Conexiones -> Compartir internet -> Anclaje a red por USB (USB Tethering).",
        "3. Windows detectará automáticamente un adaptador 'Remote NDIS based Internet Sharing Device'.",
        "4. SAORI Tactical detectará el anclaje y activará automáticamente el modo DATA_SAVER.",
        "5. Con net-merge activo, el tráfico se balanceará entre la fibra y los datos móviles."
    ]
}


def get_relay_instructions() -> str:
    lines = [
        f"=== PUENTE DE DATOS MÓVILES (RELAY & TETHERING) ===",
        f"Proyecto: {RELAY_INFO['project']} ({RELAY_INFO['url']})",
        f"Descripción: {RELAY_INFO['description']}",
        "\nPasos para activación táctica rápida:"
    ]
    for step in RELAY_INFO["quickstart"]:
        lines.append(f"  {step}")
    return "\n".join(lines)
