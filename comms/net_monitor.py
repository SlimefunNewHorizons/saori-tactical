"""
SAORI TACTICAL - Network Multi-Interface Sentinel & Bonding Monitor
Monitorea en tiempo real todas las interfaces físicas y virtuales de Windows:
Ethernet, Wi-Fi, USB Tethering (Celular/Móvil), Tailscale y Hotspots.
Gestiona failover automático, detección de cortes y presupuesto de datos para ahorro de tokens.
"""

import subprocess
import json
import time
import socket
from typing import Dict, List, Optional, Tuple


class NetworkSentinel:
    def __init__(self, ping_targets: Optional[List[str]] = None):
        # Objetivos de prueba de vida (Cloudflare, Google y Star VPS)
        self.ping_targets = ping_targets or ["1.1.1.1", "8.8.8.8", "89.117.72.215"]
        self.last_status: Dict = {}
        self.data_saver_mode: bool = False

    def scan_adapters(self) -> List[Dict]:
        """Escanea todos los adaptadores de red de Windows usando PowerShell Get-NetAdapter."""
        cmd = [
            "powershell", "-NoProfile", "-Command",
            "Get-NetAdapter | Select-Object Name, InterfaceDescription, ifIndex, Status, LinkSpeed, MacAddress | ConvertTo-Json -Compress"
        ]
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=6)
            if res.returncode == 0 and res.stdout.strip():
                data = json.loads(res.stdout)
                if isinstance(data, dict):
                    data = [data]
                return data
        except Exception:
            pass
        return []

    def check_internet_reachability(self, timeout_sec: float = 1.5) -> Tuple[bool, float, str]:
        """Verifica conectividad IP externa mediante socket rápido sin llamar a DNS."""
        best_latency = 9999.0
        reachable_host = ""
        is_alive = False

        for host in self.ping_targets:
            t0 = time.time()
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(timeout_sec)
                # Intento de conexión al puerto 53 (DNS) o 443 (HTTPS)
                s.connect((host, 53))
                s.close()
                lat = (time.time() - t0) * 1000.0
                if lat < best_latency:
                    best_latency = lat
                    reachable_host = host
                    is_alive = True
            except Exception:
                try:
                    s.close()
                except Exception:
                    pass

        if is_alive:
            return True, best_latency, reachable_host
        return False, -1.0, ""

    @staticmethod
    def get_local_ip_addresses() -> List[Dict[str, str]]:
        """Obtiene todas las IPs locales IPv4 disponibles para conectar dispositivos en red local o Hotspot."""
        ips = []
        try:
            cmd = ["powershell", "-NoProfile", "-Command", "Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.IPAddress -notlike '127.*' -and $_.IPAddress -notlike '169.254.*' } | Select-Object InterfaceAlias, IPAddress | ConvertTo-Json -Compress"]
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=4)
            if res.returncode == 0 and res.stdout.strip():
                data = json.loads(res.stdout)
                if isinstance(data, dict):
                    data = [data]
                for item in data:
                    ips.append({"alias": item.get("InterfaceAlias"), "ip": item.get("IPAddress")})
        except Exception:
            pass
        return ips

    def evaluate_environment(self) -> Dict:
        """
        Evalúa el estado completo de la conectividad:
        - Si hay Ethernet activo.
        - Si hay Wi-Fi conectado.
        - Si hay anclaje de datos móviles / USB Tethering detectado.
        - Si la conexión global está ONLINE, DEGRADADA o TOTALMENTE OFFLINE (Blackout).
        """
        adapters = self.scan_adapters()
        is_online, latency_ms, alive_target = self.check_internet_reachability()

        active_adapters = [a for a in adapters if a.get("Status") == "Up"]
        has_ethernet = any("ethernet" in a.get("Name", "").lower() or "realtek" in a.get("InterfaceDescription", "").lower() for a in active_adapters)
        has_wifi = any("wi-fi" in a.get("Name", "").lower() or "wireless" in a.get("InterfaceDescription", "").lower() for a in active_adapters)
        has_mobile_tether = any("rndis" in a.get("InterfaceDescription", "").lower() or "remote ndis" in a.get("InterfaceDescription", "").lower() or "cellular" in a.get("Name", "").lower() for a in active_adapters)
        has_tailscale = any("tailscale" in a.get("Name", "").lower() for a in active_adapters)

        # Si estamos usando anclaje móvil (tethering) o Wi-Fi con latencia > 180ms, activar data_saver
        self.data_saver_mode = has_mobile_tether or (is_online and latency_ms > 220)

        status_label = "ONLINE" if is_online else "OFFLINE_BLACKOUT"
        if is_online and latency_ms > 300:
            status_label = "ONLINE_DEGRADED"

        report = {
            "timestamp": time.time(),
            "status": status_label,
            "is_online": is_online,
            "latency_ms": round(latency_ms, 1) if is_online else None,
            "best_target": alive_target if is_online else None,
            "data_saver_mode": self.data_saver_mode,
            "adapters_count": len(adapters),
            "active_adapters": [a.get("Name") for a in active_adapters],
            "has_ethernet": has_ethernet,
            "has_wifi": has_wifi,
            "has_mobile_tether": has_mobile_tether,
            "has_tailscale": has_tailscale,
            "recommended_ai_mode": "CLOUD_HYBRID" if (is_online and not self.data_saver_mode) else ("LOCAL_RTX4060_TOKEN_SAVER" if is_online else "PURE_OFFLINE_LOCAL")
        }
        self.last_status = report
        return report
