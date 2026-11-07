"""
SAORI TACTICAL - Android Sensor & Hardware Bridge (ADB)
Permite utilizar smartphones Android (ej: Poco X3 Pro, Poco X8 Pro) conectados por USB o Wi-Fi
como estaciones de sensores de señal celular, escáneres Wi-Fi avanzados, telemetría y módem de radio.
"""

import subprocess
import os
import re
from pathlib import Path
from typing import List, Dict, Optional

# Rutas conocidas de adb.exe en Windows
KNOWN_ADB_PATHS = [
    Path(os.environ.get("LOCALAPPDATA", "")) / "Microsoft" / "WinGet" / "Packages" / "Google.PlatformTools_Microsoft.Winget.Source_8wekyb3d8bbwe" / "platform-tools" / "adb.exe",
    Path(os.environ.get("LOCALAPPDATA", "")) / "Android" / "Sdk" / "platform-tools" / "adb.exe",
    Path("C:/platform-tools/adb.exe"),
    Path(os.environ.get("USERPROFILE", "")) / "scoop" / "shims" / "adb.exe"
]


def find_adb_executable() -> Optional[str]:
    """Busca el ejecutable adb.exe en el sistema."""
    # 1. Comprobar PATH
    try:
        res = subprocess.run(["adb", "version"], capture_output=True, text=True, timeout=2)
        if res.returncode == 0:
            return "adb"
    except Exception:
        pass

    # 2. Comprobar rutas fijas
    for p in KNOWN_ADB_PATHS:
        if p.exists():
            return str(p)

    # 3. Buscar en WinGet Packages si fue instalado recientemente
    winget_dir = Path(os.environ.get("LOCALAPPDATA", "")) / "Microsoft" / "WinGet" / "Packages"
    if winget_dir.exists():
        found = list(winget_dir.glob("**/platform-tools/adb.exe"))
        if found:
            return str(found[0])

    return None


class AndroidSensorBridge:
    def __init__(self):
        self.adb_path = find_adb_executable()

    def is_adb_available(self) -> bool:
        return self.adb_path is not None

    def _run_adb(self, args: List[str], timeout: int = 6) -> Optional[str]:
        if not self.adb_path:
            return None
        try:
            cmd = [self.adb_path] + args
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
            if res.returncode == 0:
                return res.stdout.strip()
            return None
        except Exception:
            return None

    def list_devices(self) -> List[Dict]:
        """Lista dispositivos Android conectados vía USB o Wi-Fi ADB."""
        out = self._run_adb(["devices", "-l"])
        if not out:
            return []

        devices = []
        for line in out.splitlines()[1:]:
            line = line.strip()
            if not line or line.startswith("*"):
                continue
            parts = line.split()
            if len(parts) >= 2:
                dev_id = parts[0]
                status = parts[1]
                model = "Android Device"
                for p in parts[2:]:
                    if p.startswith("model:"):
                        model = p.split(":", 1)[1]
                devices.append({
                    "id": dev_id,
                    "status": status, # 'device', 'unauthorized', 'offline'
                    "model": model,
                    "is_ready": status == "device"
                })
        return devices

    def get_device_telemetry(self, device_id: Optional[str] = None) -> Dict:
        """
        Extrae telemetría táctica del teléfono:
        - Batería, temperatura
        - Señal Celular (Operador, dBm, tipo de red LTE/3G)
        - Estado de Wi-Fi y Punto de Acceso (Hotspot)
        """
        prefix = ["-s", device_id] if device_id else []

        # 1. Batería
        bat_out = self._run_adb(prefix + ["shell", "dumpsys", "battery"])
        battery = {"level": 100, "temp_c": 25, "charging": False}
        if bat_out:
            for l in bat_out.splitlines():
                l = l.strip()
                if l.startswith("level:"):
                    battery["level"] = int(l.split(":", 1)[1].strip())
                elif l.startswith("temperature:"):
                    raw_t = int(l.split(":", 1)[1].strip())
                    battery["temp_c"] = round(raw_t / 10, 1)
                elif l.startswith("status:"):
                    battery["charging"] = l.split(":", 1)[1].strip() == "2"

        # 2. Información de red celular (Señal dBm y operador)
        telecom_out = self._run_adb(prefix + ["shell", "dumpsys", "telephony.registry"])
        cell_info = {
            "operator": "Desconocido",
            "signal_dbm": None,
            "signal_level": "Sin Señal",
            "network_type": "Desconectado"
        }
        if telecom_out:
            # Buscar operador
            m_op = re.search(r'mVoiceOperatorAlphaLong=([^\r\n,]+)', telecom_out)
            if m_op and m_op.group(1).strip():
                cell_info["operator"] = m_op.group(1).strip()

            # Buscar dBm
            m_dbm = re.search(r'rsrp\s*=\s*(-?\d+)', telecom_out, re.IGNORECASE)
            if not m_dbm:
                m_dbm = re.search(r'mSignalStrength=.*?(?:lte\s*rsrp|rsrp)\s*[:=]\s*(-?\d+)', telecom_out, re.IGNORECASE)
            if m_dbm:
                dbm = int(m_dbm.group(1))
                if -140 <= dbm <= -40:
                    cell_info["signal_dbm"] = dbm
                    if dbm >= -80:
                        cell_info["signal_level"] = "Excelente"
                    elif dbm >= -95:
                        cell_info["signal_level"] = "Buena"
                    elif dbm >= -110:
                        cell_info["signal_level"] = "Media / Débil"
                    else:
                        cell_info["signal_level"] = "Crítica (Borde de Cobertura)"

            # Tipo de red
            if "LTE" in telecom_out:
                cell_info["network_type"] = "4G LTE"
            elif "NR" in telecom_out or "5G" in telecom_out:
                cell_info["network_type"] = "5G NR"
            elif "UMTS" in telecom_out or "HSPA" in telecom_out:
                cell_info["network_type"] = "3G HSPA"

        # 3. Propiedades del modelo y ROM
        brand = self._run_adb(prefix + ["shell", "getprop", "ro.product.brand"]) or "Android"
        model = self._run_adb(prefix + ["shell", "getprop", "ro.product.model"]) or "Device"
        rom_ver = self._run_adb(prefix + ["shell", "getprop", "ro.build.display.id"]) or "AOSP"

        return {
            "device_id": device_id or "default",
            "device_name": f"{brand.upper()} {model}",
            "rom": rom_ver,
            "battery": battery,
            "cellular": cell_info
        }

    def scan_wifi_from_device(self, device_id: Optional[str] = None) -> List[Dict]:
        """Usa las antenas Wi-Fi del teléfono móvil para escanear redes circundantes."""
        prefix = ["-s", device_id] if device_id else []
        out = self._run_adb(prefix + ["shell", "cmd", "wifi", "list-scan-results"])
        results = []
        if out:
            lines = out.splitlines()
            for line in lines[1:]:
                line = line.strip()
                if not line:
                    continue
                parts = re.split(r'\s{2,}', line)
                if len(parts) >= 4:
                    bssid = parts[0]
                    freq = parts[1]
                    level = parts[2]
                    ssid = parts[-1]
                    results.append({
                        "ssid": ssid,
                        "bssid": bssid,
                        "freq_mhz": freq,
                        "level_dbm": level
                    })
        return results

    def execute_custom_command(self, cmd: str, device_id: Optional[str] = None) -> str:
        """Ejecuta un comando shell seguro dentro del teléfono Android."""
        prefix = ["-s", device_id] if device_id else []
        out = self._run_adb(prefix + ["shell", cmd], timeout=8)
        return out or "(Sin salida o error de ejecución)"
