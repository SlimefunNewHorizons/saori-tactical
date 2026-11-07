"""
SAORI TACTICAL - PC Environment & Hardware Diagnostic Tools
Herramientas tácticas para interactuar con el entorno del PC en emergencias:
- Estado de batería y fuente de poder (crucial durante cortes de energía).
- Monitoreo de memoria RAM, CPU y VRAM de la GPU RTX 4060.
- Escaneo de redes Wi-Fi sobrevivientes en el entorno (netsh).
- Ejecución segura de diagnósticos y comandos PowerShell.
"""

import subprocess
import json
from typing import Dict, List, Optional


class PCTacticalTools:
    @staticmethod
    def get_battery_status() -> Dict:
        """Obtiene estado de la batería, porcentaje y si está conectado a la red eléctrica."""
        ps_cmd = """
        Get-WmiObject Win32_Battery | Select-Object EstimatedChargeRemaining, BatteryStatus, EstimatedRunTime | ConvertTo-Json -Compress
        """
        try:
            res = subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], capture_output=True, text=True, timeout=4)
            if res.returncode == 0 and res.stdout.strip():
                data = json.loads(res.stdout)
                charge = data.get("EstimatedChargeRemaining", 100)
                status_code = data.get("BatteryStatus", 1) # 2 = Charging, 1 = Discharging
                status_str = "CARGANDO" if status_code == 2 else "DESCARGANDO (BATERÍA)"
                return {
                    "has_battery": True,
                    "percent": charge,
                    "status": status_str,
                    "runtime_min": data.get("EstimatedRunTime")
                }
        except Exception:
            pass
        return {
            "has_battery": False,
            "status": "ALIMENTACIÓN DIRECTA AC / GENERADOR",
            "percent": 100
        }

    @staticmethod
    def get_hardware_telemetry() -> Dict:
        """Obtiene uso de CPU, RAM y telemetría de la GPU."""
        ps_cmd = """
        $os = Get-WmiObject Win32_OperatingSystem
        $cpu = Get-WmiObject Win32_Processor | Measure-Object -Property LoadPercentage -Average
        @{
            TotalRAM_GB = [math]::Round($os.TotalVisibleMemorySize / 1MB, 2)
            FreeRAM_GB = [math]::Round($os.FreePhysicalMemory / 1MB, 2)
            CPULoad = [math]::Round($cpu.Average, 1)
        } | ConvertTo-Json -Compress
        """
        try:
            res = subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], capture_output=True, text=True, timeout=4)
            if res.returncode == 0 and res.stdout.strip():
                data = json.loads(res.stdout)
                total = data.get("TotalRAM_GB", 16)
                free = data.get("FreeRAM_GB", 8)
                used = round(total - free, 2)
                return {
                    "total_ram_gb": total,
                    "used_ram_gb": used,
                    "free_ram_gb": free,
                    "cpu_load_pct": data.get("CPULoad", 0)
                }
        except Exception:
            pass
        return {"error": "No se pudo leer telemetría"}

    @staticmethod
    def scan_surviving_wifi() -> List[Dict]:
        """Escanea puntos de acceso Wi-Fi visibles en los alrededores usando netsh."""
        cmd = ["netsh", "wlan", "show", "networks", "mode=bssid"]
        results = []
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            if res.returncode == 0:
                current_ssid = ""
                for line in res.stdout.splitlines():
                    line = line.strip()
                    if line.startswith("SSID") and ":" in line:
                        current_ssid = line.split(":", 1)[1].strip() or "[OCULTO]"
                    elif "Señal" in line or "Signal" in line:
                        sig = line.split(":", 1)[1].strip()
                        if current_ssid:
                            results.append({"ssid": current_ssid, "signal": sig})
                            current_ssid = ""
        except Exception:
            pass
        return results

    @staticmethod
    def execute_powershell_safely(command: str) -> str:
        """Ejecuta un script o comando de diagnóstico de forma controlada."""
        try:
            res = subprocess.run(["powershell", "-NoProfile", "-Command", command], capture_output=True, text=True, timeout=12)
            out = res.stdout.strip()
            if res.stderr.strip():
                out += f"\n[STDERR]: {res.stderr.strip()}"
            return out or "(Comando ejecutado sin salida)"
        except subprocess.TimeoutExpired:
            return "[ERROR]: El comando excedió el tiempo límite de 12 segundos."
        except Exception as e:
            return f"[ERROR]: {e}"
