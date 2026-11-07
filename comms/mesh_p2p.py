"""
SAORI TACTICAL - Cyberpunk Blackwall P2P Mesh & Peer Discovery
Motor de red local autónoma para entornos sin internet (Blackout / Air-gapped Citadel).
- Descubrimiento automático de nodos vecinos por Multicast / Broadcast UDP sin router ni DNS.
- Buzón táctico Store-and-Forward (DTN) para intercambio asíncrono de mensajes y reportes (SITREP).
- Enrutamiento y directorio de nodos vivos (PC, Laptop Nova, Poco X3 Pro, Poco X8 Pro, Tab S6 Lite).
"""

import socket
import json
import time
import threading
from typing import Dict, List, Optional
from pathlib import Path

BROADCAST_PORT = 53530
DISCOVERY_MAGIC = "SAORI_CITADEL_NODE"
MAILBOX_FILE = Path(__file__).resolve().parent.parent / "data" / "mesh_mailbox.json"


class TacticalMeshP2P:
    def __init__(self, node_id: str = "SAORI_CORE", node_role: str = "VAULT_SERVER", web_port: int = 8090):
        self.node_id = node_id
        self.node_role = node_role
        self.web_port = web_port
        self.known_peers: Dict[str, Dict] = {}
        self.mailbox: List[Dict] = self._load_mailbox()
        self.running = False
        self._lock = threading.Lock()
        self._sock: Optional[socket.socket] = None

    def _load_mailbox(self) -> List[Dict]:
        if MAILBOX_FILE.exists():
            try:
                with open(MAILBOX_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return []

    def _save_mailbox(self):
        try:
            MAILBOX_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(MAILBOX_FILE, "w", encoding="utf-8") as f:
                json.dump(self.mailbox, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def start(self):
        """Inicia el servicio de descubrimiento y escucha de la malla P2P."""
        self.running = True
        try:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            self._sock.bind(("", BROADCAST_PORT))
        except Exception as e:
            # En caso de fallo de enlace
            return

        # Hilo 1: Escucha de balizas y mensajes
        t_listener = threading.Thread(target=self._listener_loop, daemon=True)
        t_listener.start()

        # Hilo 2: Transmisión periódica de baliza de presencia
        t_beacon = threading.Thread(target=self._beacon_loop, daemon=True)
        t_beacon.start()

    def stop(self):
        self.running = False
        if self._sock:
            try:
                self._sock.close()
            except Exception:
                pass

    def _beacon_loop(self):
        """Emite baliza de presencia cada 4 segundos a la subred local."""
        while self.running:
            try:
                beacon_payload = {
                    "magic": DISCOVERY_MAGIC,
                    "type": "BEACON",
                    "node_id": self.node_id,
                    "role": self.node_role,
                    "web_port": self.web_port,
                    "timestamp": time.time(),
                    "msg_count": len(self.mailbox)
                }
                data = json.dumps(beacon_payload).encode("utf-8")
                # Enviar a broadcast local
                self._sock.sendto(data, ("<broadcast>", BROADCAST_PORT))
            except Exception:
                pass
            time.sleep(4.0)

    def _listener_loop(self):
        """Recibe balizas y mensajes de otros dispositivos de la malla."""
        while self.running:
            try:
                data, addr = self._sock.recvfrom(4096)
                ip = addr[0]
                text = data.decode("utf-8", errors="replace")
                payload = json.loads(text)

                if payload.get("magic") != DISCOVERY_MAGIC:
                    continue

                p_type = payload.get("type")
                sender = payload.get("node_id", "UNKNOWN")

                # Ignorar nuestras propias balizas
                if sender == self.node_id:
                    continue

                if p_type == "BEACON":
                    with self._lock:
                        self.known_peers[sender] = {
                            "node_id": sender,
                            "ip": ip,
                            "role": payload.get("role", "PEER"),
                            "web_port": payload.get("web_port", 8090),
                            "last_seen": time.time(),
                            "status": "ONLINE"
                        }
                elif p_type == "SITREP_MSG":
                    # Mensaje Store-and-Forward
                    with self._lock:
                        msg = {
                            "id": payload.get("msg_id", f"msg_{int(time.time()*1000)}"),
                            "sender": sender,
                            "sender_ip": ip,
                            "timestamp": payload.get("timestamp", time.time()),
                            "content": payload.get("content", ""),
                            "priority": payload.get("priority", "NORMAL")
                        }
                        self.mailbox.append(msg)
                        self._save_mailbox()
            except Exception:
                time.sleep(0.5)

    def get_active_peers(self) -> List[Dict]:
        """Devuelve los nodos de la malla activos en los últimos 15 segundos."""
        now = time.time()
        active = []
        with self._lock:
            for node_id, info in self.known_peers.items():
                elapsed = now - info["last_seen"]
                if elapsed < 18.0:
                    info_copy = dict(info)
                    info_copy["latency_sec"] = round(elapsed, 1)
                    active.append(info_copy)
                else:
                    info["status"] = "OFFLINE"
        return active

    def broadcast_message(self, content: str, priority: str = "NORMAL") -> bool:
        """Emite un mensaje o alerta SITREP a todos los nodos de la malla."""
        msg_payload = {
            "magic": DISCOVERY_MAGIC,
            "type": "SITREP_MSG",
            "msg_id": f"sitrep_{int(time.time()*1000)}",
            "node_id": self.node_id,
            "timestamp": time.time(),
            "priority": priority,
            "content": content
        }
        # Guardar en buzón local
        with self._lock:
            self.mailbox.append({
                "id": msg_payload["msg_id"],
                "sender": self.node_id,
                "sender_ip": "127.0.0.1",
                "timestamp": msg_payload["timestamp"],
                "content": content,
                "priority": priority
            })
            self._save_mailbox()

        if not self._sock:
            return False
        try:
            data = json.dumps(msg_payload).encode("utf-8")
            self._sock.sendto(data, ("<broadcast>", BROADCAST_PORT))
            return True
        except Exception:
            return False

    def get_mailbox(self) -> List[Dict]:
        with self._lock:
            return list(self.mailbox)
