"""
SAORI TACTICAL - High-Contrast Terminal Tactical HUD
Interfaz visual para operaciones de emergencia en campo.
"""

from typing import Dict, List


class TacticalHUD:
    @staticmethod
    def render_header(net_status: Dict, active_model_info: Dict, vram_models: List[Dict]):
        status = net_status.get("status", "UNKNOWN")
        color = "\033[92m" if "ONLINE" in status else "\033[91m"
        reset = "\033[0m"
        cyan = "\033[96m"
        yellow = "\033[93m"
        bold = "\033[1m"
        gold = "\033[33m"

        active_adapters = ", ".join(net_status.get("active_adapters", [])) or "Ninguno"
        latency = f"{net_status.get('latency_ms')} ms" if net_status.get('latency_ms') else "N/A"
        data_saver = "ACTIVO" if net_status.get("data_saver_mode") else "INACTIVO"

        vram_info = "0 MB (LIBRE)"
        if vram_models:
            loaded_names = [m.get("name", "model") for m in vram_models]
            vram_info = f"{', '.join(loaded_names)} (OCUPADA)"

        print(f"{bold}{cyan}╔══════════════════════════════════════════════════════════════════════════════════╗{reset}")
        print(f"{bold}{cyan}║           SAORI TACTICAL // SOVEREIGN EMERGENCY & RF OPERATING SYSTEM            ║{reset}")
        print(f"{bold}{cyan}╠══════════════════════════════════════════════════════════════════════════════════╣{reset}")
        print(f"{cyan}║{reset} ESTADO DE RED: {color}{bold}{status}{reset} | LATENCIA: {yellow}{latency}{reset} | DATA SAVER: {yellow}{data_saver}{reset}")
        print(f"{cyan}║{reset} ADAPTADORES: {active_adapters}")
        print(f"{cyan}║{reset} MODELO ACTIVO: {gold}{bold}{active_model_info['name']} [{active_model_info['model']}]{reset}")
        print(f"{cyan}║{reset} ESTADO GPU VRAM (RTX 4060): {yellow}{vram_info}{reset}")
        print(f"{bold}{cyan}╚══════════════════════════════════════════════════════════════════════════════════╝{reset}")

    @staticmethod
    def render_menu():
        bold = "\033[1m"
        yellow = "\033[93m"
        cyan = "\033[96m"
        reset = "\033[0m"
        print(f"\n{bold}CENTRAL DE OPERACIONES DISPONIBLES:{reset}")
        print(f" {yellow}[1]{reset} 🚨 Consulta Táctica de Emergencia (RAG + Grafo + Inferencia)")
        print(f" {yellow}[2]{reset} 📡 Directorio de Frecuencias de Radio (Chile / Internacional)")
        print(f" {yellow}[3]{reset} 📻 Estudio Morse (Traducción Bidireccional, Audio & WAV)")
        print(f" {yellow}[4]{reset} 🛠️  Wiki de Construcción & Ingeniería de Campo (Filtros, Antenas, Refugios)")
        print(f" {yellow}[5]{reset} 💻 Diagnóstico PC & Android (Batería, Telemetría, Poco X3/X8, Wi-Fi)")
        print(f" {yellow}[6]{reset} 🤖 Cambiar Rol de IA (Tactical / Coder / Analyst)")
        print(f" {yellow}[7]{reset} 🧹 Liberar VRAM de la GPU al 100% (Purga Inmediata)")
        print(f" {yellow}[8]{reset} 🌐 Iniciar Servidor Web Táctico (Acceso Móvil sin Router)")
        print(f" {cyan}[q]{reset} Salir de SAORI Tactical (Cierre y Descarga de GPU)\n")
