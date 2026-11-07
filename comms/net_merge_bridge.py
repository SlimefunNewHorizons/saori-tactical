"""
SAORI TACTICAL - Net-Merge Multi-Link Bonding Bridge
Integra net-merge (https://github.com/net-merge/net-merge) para combinar simultáneamente:
- Wi-Fi (Realtek 8821CU)
- Ethernet (Realtek GbE)
- Anclaje USB / Hotspot Móvil (Celular 4G/5G)
Permite sumar el ancho de banda y garantizar failover transparente sin VPN ni servidores externos.
"""

import os
import subprocess
from pathlib import Path
from typing import Dict, Optional

NET_MERGE_DIR = Path(os.environ.get("ProgramFiles", "C:\\Program Files")) / "net-merge"
NET_MERGE_EXE = NET_MERGE_DIR / "net-merge.exe"
NET_MERGE_TRAY = NET_MERGE_DIR / "net-merge-tray.exe"


class NetMergeBridge:
    @staticmethod
    def is_installed() -> bool:
        return NET_MERGE_EXE.exists()

    @staticmethod
    def install():
        """Descarga e instala net-merge de forma desatendida en Windows."""
        ps_cmd = """
$url = 'https://github.com/net-merge/net-merge/releases/latest/download/net-merge-setup.exe'
$setup = Join-Path $env:TEMP 'net-merge-setup.exe'
Write-Host 'Descargando instalador de net-merge...'
Invoke-WebRequest $url -OutFile $setup -UseBasicParsing
Write-Host 'Instalando net-merge en modo silencioso...'
Start-Process $setup -ArgumentList '/SILENT', '/NORESTART' -Wait
"""
        res = subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], capture_output=True, text=True)
        return res.returncode == 0

    @staticmethod
    def start_tray():
        if NET_MERGE_TRAY.exists():
            subprocess.Popen([str(NET_MERGE_TRAY)])
            return True
        return False
