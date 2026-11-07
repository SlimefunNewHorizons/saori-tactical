"""
SAORI TACTICAL - Meshtastic LoRa Mesh Radio Bridge
Puente de comunicación off-grid para redes de radio malladas LoRa (Meshtastic).
Permite recibir alertas, telemetría y consultas de auxilio y responder con respuestas
RAG comprimidas a través de ondas de radio sin depender de internet ni telefonía móvil.
"""

import sys
import os
import time
import logging
from typing import Optional, Callable, Dict

logger = logging.getLogger("saori_mesh")


class MeshtasticBridge:
    def __init__(self, connection_str: Optional[str] = None):
        """
        connection_str:
            None o "auto": Detección automática de puerto COM USB (Windows).
            "serial:COM3": Conexión directa al puerto serie COM3.
            "tcp:192.168.1.50": Conexión TCP a nodo LoRa por Wi-Fi/Ethernet.
        """
        self.connection_str = connection_str or os.environ.get("MESHTASTIC_CONNECTION", "auto")
        self.interface = None
        self.connected = False
        self.message_callback: Optional[Callable[[str, str], None]] = None

    def connect(self) -> bool:
        """Intenta conectar con el nodo Meshtastic local."""
        try:
            import meshtastic
            import meshtastic.serial_interface
            import meshtastic.tcp_interface
        except ImportError:
            logger.warning("[MESH] El paquete 'meshtastic' no está instalado. Ejecute 'pip install meshtastic'.")
            return False

        try:
            if self.connection_str.startswith("tcp:"):
                host = self.connection_str.split("tcp:")[1].strip()
                logger.info(f"[MESH] Conectando a nodo Meshtastic TCP en {host}...")
                self.interface = meshtastic.tcp_interface.TCPInterface(hostname=host)
            elif self.connection_str.startswith("serial:") or self.connection_str.startswith("COM"):
                port = self.connection_str.replace("serial:", "").strip()
                logger.info(f"[MESH] Conectando a nodo Meshtastic Serial en {port}...")
                self.interface = meshtastic.serial_interface.SerialInterface(devPath=port)
            else:
                logger.info("[MESH] Auto-detectando nodo Meshtastic USB...")
                self.interface = meshtastic.serial_interface.SerialInterface()

            self.connected = True
            logger.info("[MESH] ¡Nodo Meshtastic conectado exitosamente!")
            
            # Registrar listener de eventos
            from pubsub import pub
            pub.subscribe(self._on_receive_packet, "meshtastic.receive")
            return True
        except Exception as e:
            logger.warning(f"[MESH] No se pudo conectar al hardware Meshtastic ({e}). Operando en modo simulación/standby.")
            self.connected = False
            return False

    def _on_receive_packet(self, packet, interface):
        """Callback cuando entra un paquete por la red de radio LoRa."""
        try:
            if "decoded" in packet and "text" in packet["decoded"]:
                text = packet["decoded"]["text"]
                sender = packet.get("fromId", "unknown")
                logger.info(f"[MESH RX] De: {sender} | Mensaje: {text}")
                if self.message_callback:
                    self.message_callback(sender, text)
        except Exception as e:
            logger.error(f"[MESH RX ERROR] {e}")

    def send_broadcast(self, text: str, channel_index: int = 0) -> bool:
        """Transmite un mensaje de texto por radio a toda la malla LoRa local."""
        if not self.connected or not self.interface:
            logger.info(f"[MESH SIM-TX] [Canal {channel_index}] Broadcast: {text}")
            return False

        try:
            # Cortar mensajes largos en fragmentos de radio estándar (máx 200 bytes por paquete LoRa)
            chunks = [text[i:i + 190] for i in range(0, len(text), 190)]
            for chunk in chunks:
                self.interface.sendText(chunk, channelIndex=channel_index)
                time.sleep(1.2)  # Respetar ciclo de trabajo (duty-cycle) de radio
            return True
        except Exception as e:
            logger.error(f"[MESH TX ERROR] Fallo al transmitir por radio: {e}")
            return False

    def close(self):
        if self.interface:
            try:
                self.interface.close()
            except Exception:
                pass
        self.connected = False
