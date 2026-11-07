#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SAORI TACTICAL // Sovereign Emergency, Survival & RF Spectrum AI Operator
PC Local / RTX 4060 Accelerated / 100% Offline Capable

Diferenciadores clave:
- Especializada en Señales de Radio (VHF/UHF, HF, SENAPRED, Bomberos, CB, Marino 16, Morse, Repetidoras).
- Multiplexación y Resiliencia de Red (Ethernet, Wi-Fi, Anclaje Móvil/Tethering, Failover, Token Saver).
- RAG y Grafo de Conocimiento de Supervivencia y Medicina de Trauma (Protocolo MARCH, Terremoto, Tsunami, Agua).
- Motor de IA Híbrido: Local RTX 4060 (Llama 3.2 3B en Ollama) + Nube (ElevenLabs / NVIDIA NIM).
"""

import sys
import os
import time
import argparse
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# Agregar raíz del proyecto al path
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from comms.net_monitor import NetworkSentinel
from radio.freq_db import search_frequencies, format_frequency_card, FREQUENCIES
from radio.rf_tools import (
    text_to_morse,
    morse_to_text,
    auto_translate,
    is_morse_string,
    text_to_phonetic,
    play_morse_sound,
    generate_morse_wav,
    calculate_repeater_offset,
    latlon_to_maidenhead,
    Q_CODES
)
from radio.mesh_bridge import MeshtasticBridge
from knowledge.vault import query_vault
from knowledge.graph_engine import EmergencyKnowledgeGraph
from knowledge.hybrid_search import TacticalSearchEngine
from knowledge.offline_wiki import search_wiki, format_wiki_card, OFFLINE_WIKI_ENTRIES
from brain.local_llm import LocalLLMEngine, MODEL_FLEET
from brain.pc_tools import PCTacticalTools
from brain.voice_engine import TacticalVoiceEngine
from brain.token_saver import TokenSaver
from comms.android_bridge import AndroidSensorBridge
from comms.mesh_p2p import TacticalMeshP2P
from ui.hud_terminal import TacticalHUD
from ui.web_server import start_emergency_web_server


class SaoriTacticalCore:
    def __init__(self):
        self.net_sentinel = NetworkSentinel()
        self.graph = EmergencyKnowledgeGraph()
        self.search = TacticalSearchEngine()
        self.llm = LocalLLMEngine()
        self.voice = TacticalVoiceEngine()
        self.token_saver = TokenSaver()
        self.mesh = MeshtasticBridge()
        self.pc_tools = PCTacticalTools()
        self.android = AndroidSensorBridge()
        self.mesh_p2p = TacticalMeshP2P(node_id="SAORI_CITADEL_CORE", node_role="VAULT_SERVER", web_port=8090)
        self.mesh_p2p.start()

    def get_status(self) -> dict:
        status = self.net_sentinel.evaluate_environment()
        status["active_model"] = self.llm.get_active_model_info()
        status["vram_models"] = self.llm.get_vram_status()
        status["android_devices"] = self.android.list_devices() if self.android.is_adb_available() else []
        status["mesh_peers"] = self.mesh_p2p.get_active_peers()
        status["mailbox_count"] = len(self.mesh_p2p.mailbox)
        return status

    def set_ai_role(self, role: str) -> bool:
        return self.llm.set_role(role)

    def unload_vram(self) -> bool:
        return self.llm.unload_all_vram()

    def process_query(self, query: str, voice_reply: bool = False, role: str = None) -> str:
        """
        Canal de resolución de consultas prioritarias en cascada:
        1. Cache Semántico (0 tokens / 0 ms)
        2. Grafo de Conocimiento Táctico (0 tokens / <5 ms)
        3. Motor de Búsqueda FTS5 (0 tokens / <10 ms)
        4. Motor de Inferencia Local RTX 4060 (Llama 3.2 / Qwen 2.5 Coder / DeepSeek R1)
        """
        q_clean = query.strip()
        if not q_clean:
            return "Indique una consulta o situación de emergencia."

        target_role = role or self.llm.active_role
        cache_key = f"[{target_role}]:{q_clean}"

        # 1. Caché semántico local
        cached = self.token_saver.get_cached(cache_key)
        if cached:
            return f"[MEMORIA CACHÉ LOCAL - 0 TOKENS]\n{cached}"

        # 2. Resolución por Grafo de Conocimiento Táctico (Zero-Token Path para rol táctico)
        graph_text = ""
        if target_role == "tactical":
            graph_res = self.graph.resolve_query(q_clean)
            if graph_res:
                lines = [
                    f"🚨 {graph_res['threat_label'].upper()}",
                    "─" * 55,
                    "ACCIONES INMEDIATAS PRIORIZADAS:"
                ]
                for act in graph_res["actions"]:
                    lines.append(f" • [{act['rel'].upper()}] {act['action']}")
                if graph_res["tools"]:
                    lines.append("\nHERRAMIENTAS / INSUMOS REQUERIDOS:")
                    for tool in graph_res["tools"]:
                        lines.append(f" 🛠️  {tool}")
                if graph_res["frequencies"]:
                    lines.append("\nCANALES DE RADIO RECOMENDADOS:")
                    for freq in graph_res["frequencies"]:
                        lines.append(f" 📻 {freq}")
                graph_text = "\n".join(lines)

                # Si el grafo resolvió la amenaza con alta certeza médica/vital, devolvemos directo
                if len(graph_res["actions"]) >= 2:
                    self.token_saver.store_cache(cache_key, graph_text)
                    if voice_reply:
                        is_online = self.net_sentinel.evaluate_environment().get("is_online", False)
                        short_voice = graph_res['actions'][0]['action'] if graph_res['actions'] else "Atención al protocolo de emergencia."
                        self.voice.speak(short_voice, is_online=is_online)
                    return graph_text

        # 3. Búsqueda Híbrida en Base de Supervivencia, Wiki FTS5 y Frecuencias
        context_parts = []
        if graph_text:
            context_parts.append(graph_text)

        search_res = self.search.search_all(q_clean, limit=2)
        for s in search_res.get("survival", []):
            context_parts.append(f"[{s['category']}] {s['title']}:\n{s['summary']}\nPasos:\n" + "\n".join(s["steps"]))
        for r in search_res.get("radio", []):
            context_parts.append(f"[RADIO] {r['name']} ({r['freq_mhz']:.4f} MHz {r['mode']}): {r['usage']}")

        wiki_res = search_wiki(q_clean)
        if wiki_res:
            top_w = wiki_res[0]
            context_parts.append(f"[WIKI CONSTRUCCIÓN] {top_w['title']}:\nMateriales: {', '.join(top_w['materials'])}\nPasos:\n" + "\n".join(top_w['blueprints_steps']))

        context_str = "\n\n".join(context_parts)

        # 4. Inferencia Local en RTX 4060 con contexto RAG inyectado
        if self.llm.is_available():
            llm_response = self.llm.generate(prompt=q_clean, context=context_str, role=target_role)
            final_response = llm_response
        elif context_str:
            final_response = f"[MODO RAG LOCAL PURO SIN LLM]\n\n{context_str}"
        else:
            final_response = "No se encontraron protocolos exactos en el baúl. Verifique frecuencias o use radio en canal 16 VHF o 146.520 MHz."

        self.token_saver.store_cache(cache_key, final_response)

        if voice_reply:
            is_online = self.net_sentinel.evaluate_environment().get("is_online", False)
            self.voice.speak(final_response[:200], is_online=is_online)

        return final_response


def interactive_cli():
    core = SaoriTacticalCore()

    while True:
        net = core.get_status()
        active_model = core.llm.get_active_model_info()
        vram_models = core.llm.get_vram_status()

        TacticalHUD.render_header(net, active_model, vram_models)
        TacticalHUD.render_menu()
        choice = input("\033[96mSAORI-TACTICAL>\033[0m ").strip()

        if choice.lower() in ("q", "quit", "exit"):
            print("\n🧹 Purgando VRAM de la GPU RTX 4060 antes de salir...")
            core.unload_vram()
            print("✅ VRAM liberada al 100% (0 MB).")
            print("Desconectando SAORI Tactical... Operaciones en standby.\n")
            break

        elif choice == "1":
            print(f"\n[ROL ACTUAL: {active_model['name']}]")
            q = input("🚨 Describa la situación o síntoma: ").strip()
            if q:
                print("\n" + "=" * 65)
                resp = core.process_query(q, voice_reply=True)
                print(resp)
                print("=" * 65)
                input("\nPresione Enter para continuar...")

        elif choice == "2":
            q = input("\n[RADIO] Término o canal (Ej: Bomberos, 146.520, Chile, Marino): ").strip()
            res = search_frequencies(query=q)
            print(f"\nSe encontraron {len(res)} frecuencias:\n")
            for f in res:
                print(format_frequency_card(f))
            input("\nPresione Enter para continuar...")

        elif choice == "3":
            print("\n╔══════════════════════════════════════════════════════════╗")
            print("║     ESTUDIO TÁCTICO DE MORSE, FONÉTICO Y CÓDIGOS Q       ║")
            print("╚══════════════════════════════════════════════════════════╝")
            print("1. Traductor Universal Morse (Lenguaje Natural <-> Morse)")
            print("2. Generar Archivo de Audio .WAV de Código Morse")
            print("3. Deletreo Fonético Aeronáutico OACI / OTAN")
            print("4. Diccionario de Códigos Q (QTH, QRM, QSL, 73, etc.)")
            print("5. Calculador de Offset de Repetidoras VHF / UHF")
            sub_c = input("\nSeleccione opción [1-5]: ").strip()

            if sub_c == "1":
                txt = input("\nEscriba texto en lenguaje natural o pegue código Morse: ").strip()
                if txt:
                    res = auto_translate(txt)
                    print("\n" + "─" * 55)
                    print(f"Modo Detectado: {res['mode']}")
                    print(f"Texto Natural:  {res['text']}")
                    print(f"Código Morse:   {res['morse']}")
                    print(f"Deletreo OACI:  {res['phonetic']}")
                    print("─" * 55)
                    snd = input("¿Reproducir beeps de audio Morse en parlante? (s/n): ").strip().lower()
                    if snd == "s":
                        play_morse_sound(res['morse'])

            elif sub_c == "2":
                txt = input("\nTexto a convertir en archivo de audio .WAV: ").strip()
                if txt:
                    res = auto_translate(txt)
                    out_dir = ROOT_DIR / "data"
                    out_dir.mkdir(parents=True, exist_ok=True)
                    out_wav = out_dir / "morse_signal.wav"
                    if generate_morse_wav(res['morse'], str(out_wav)):
                        print(f"✅ Archivo WAV generado exitosamente en:")
                        print(f"   👉 {out_wav} ({out_wav.stat().st_size} bytes)")
                    else:
                        print("❌ Error al generar archivo WAV.")

            elif sub_c == "3":
                txt = input("\nTexto o indicativo a deletrear en fonético OACI: ").strip()
                print(f"\nDeletreo Fonético: {text_to_phonetic(txt)}")

            elif sub_c == "4":
                q_filter = input("\nBuscar Código Q (dejar vacío para ver todos): ").strip().upper()
                print("\nGLOSARIO DE CÓDIGOS Q Y SEÑALES:")
                for code, meaning in Q_CODES.items():
                    if not q_filter or q_filter in code or q_filter in meaning.upper():
                        print(f" • \033[93m{code:<8}\033[0m: {meaning}")

            elif sub_c == "5":
                f_str = input("\nFrecuencia de recepción (RX) en MHz: ").strip()
                try:
                    f_val = float(f_str)
                    tx, off, b = calculate_repeater_offset(f_val, "+")
                    print(f"\nBanda: {b}")
                    print(f"Offset Estándar: +{off:.3f} MHz")
                    print(f"Frecuencia TX Calculada: {tx:.4f} MHz")
                except ValueError:
                    print("Frecuencia inválida.")
            input("\nPresione Enter para continuar...")

        elif choice == "4":
            print("\n╔════════════════════════════════════════════════════════════════════════════╗")
            print("║     WIKI DE CONSTRUCCIÓN & INGENIERÍA DE CAMPO (OFFLINE BLUEPRINTS)        ║")
            print("╚════════════════════════════════════════════════════════════════════════════╝")
            print("Planos disponibles:")
            for idx, item in enumerate(OFFLINE_WIKI_ENTRIES, 1):
                print(f" [{idx}] {item['title']} ({item['category']})")
            print(" [B] Buscar por palabra clave (ej: filtro, antena, bateria, refugio)")
            
            sub_w = input("\nSeleccione número o 'B' para buscar: ").strip().lower()
            if sub_w == "b":
                q_w = input("Término de búsqueda: ").strip()
                results = search_wiki(q_w)
                print(f"\nEncontrados {len(results)} planos:\n")
                for r in results:
                    print(format_wiki_card(r))
                    print()
            elif sub_w.isdigit() and 1 <= int(sub_w) <= len(OFFLINE_WIKI_ENTRIES):
                entry = OFFLINE_WIKI_ENTRIES[int(sub_w) - 1]
                print("\n" + format_wiki_card(entry))
            input("\nPresione Enter para continuar...")

        elif choice == "5":
            print("\n╔══════════════════════════════════════════════════════════╗")
            print("║       DIAGNÓSTICO TÁCTICO DEL PC Y ENTORNO DE RED        ║")
            print("╚══════════════════════════════════════════════════════════╝")
            
            # 1. Batería
            bat = PCTacticalTools.get_battery_status()
            print(f"🔋 BATERÍA / UPS: {bat['status']} ({bat['percent']}%)")
            if bat.get("runtime_min"):
                print(f"   Autonomía estimada: ~{bat['runtime_min']} minutos")

            # 2. Hardware
            hw = PCTacticalTools.get_hardware_telemetry()
            if "error" not in hw:
                print(f"🧠 CPU: {hw['cpu_load_pct']}% carga | RAM: {hw['used_ram_gb']} GB usados / {hw['total_ram_gb']} GB total ({hw['free_ram_gb']} GB libres)")

            # 3. GPU VRAM
            v_mods = core.llm.get_vram_status()
            if v_mods:
                loaded = [m.get("name", "model") for m in v_mods]
                print(f"🎮 GPU RTX 4060: Modelo en VRAM: {', '.join(loaded)}")
            else:
                print(f"🎮 GPU RTX 4060: VRAM 100% LIBRE (0 MB en uso por modelos)")

            # 4. Redes Wi-Fi sobrevivientes
            print("\n📶 ESCANEANDO SEÑALES WI-FI EN EL ENTORNO (netsh):")
            wifis = PCTacticalTools.scan_surviving_wifi()
            if wifis:
                for w in wifis:
                    print(f"   • SSID: {w['ssid']:<25} Señal: {w['signal']}")
            else:
                print("   (No se detectaron redes inalámbricas activas en los alrededores)")

            # 5. Dispositivos Android Conectados (ADB)
            print("\n📱 ESTACIÓN DE SENSORES ANDROID (ADB - Poco X3 Pro / Poco X8 Pro):")
            if core.android.is_adb_available():
                devices = core.android.list_devices()
                if devices:
                    for d in devices:
                        print(f"   • Dispositivo: {d['model']} (ID: {d['id']}) Estado: {d['status']}")
                        if d['is_ready']:
                            telem = core.android.get_device_telemetry(d['id'])
                            bat_d = telem.get('battery', {})
                            cell = telem.get('cellular', {})
                            print(f"     Batería Celular: {bat_d.get('level')}% ({bat_d.get('temp_c')}°C)")
                            print(f"     Red Móvil: {cell.get('operator')} · {cell.get('network_type')} · Señal: {cell.get('signal_level')} ({cell.get('signal_dbm')} dBm)")
                else:
                    print("   (No hay teléfonos conectados por USB o Wi-Fi ADB. Conecte su Poco X3 Pro con Depuración USB)")
            else:
                print("   (ADB no encontrado en el sistema)")

            # 6. Opción PowerShell
            run_ps = input("\n¿Ejecutar un comando PowerShell seguro? (s/n): ").strip().lower()
            if run_ps == "s":
                cmd = input("PS> ").strip()
                if cmd:
                    out = PCTacticalTools.execute_powershell_safely(cmd)
                    print("\n--- SALIDA POWERSHELL ---")
                    print(out)
                    print("-------------------------")
            input("\nPresione Enter para continuar...")

        elif choice == "6":
            print("\n╔══════════════════════════════════════════════════════════╗")
            print("║          FLOTA DE MODELOS DE INTELIGENCIA LOCAL          ║")
            print("╚══════════════════════════════════════════════════════════╝")
            print("Seleccione el rol de IA activo para la RTX 4060:")
            for k, info in MODEL_FLEET.items():
                active_mark = "👉 [ACTIVO]" if k == core.llm.active_role else "  "
                print(f" {active_mark} [{k.upper()}]: {info['name']} ({info['model']})")
                print(f"      {info['description']}")
            
            new_role = input("\nEscriba el rol a activar (tactical / coder / analyst): ").strip().lower()
            if new_role in MODEL_FLEET:
                core.set_ai_role(new_role)
                print(f"✅ Rol cambiado exitosamente a: {MODEL_FLEET[new_role]['name']}")
            else:
                print("Rol no reconocido. Se mantiene el actual.")
            input("\nPresione Enter para continuar...")

        elif choice == "7":
            print("\n🧹 Purgando modelos de la VRAM en la GPU NVIDIA RTX 4060...")
            core.unload_vram()
            time.sleep(0.5)
            v_mods = core.llm.get_vram_status()
            if not v_mods:
                print("✅ VRAM 100% LIBERADA: 0 MB de memoria de video ocupada.")
            else:
                print(f"⚠️ Aún figuran modelos en memoria: {[m.get('name') for m in v_mods]}")
            input("\nPresione Enter para continuar...")

        elif choice == "8":
            port = 8090
            print(f"\nIniciando Servidor Web Táctico en http://0.0.0.0:{port} ...")
            start_emergency_web_server(core, port=port)
            print(f"✅ ¡Servidor Activo! Abra en su navegador local o desde su teléfono:")
            print(f"   👉 http://localhost:{port}")
            local_ips = NetworkSentinel.get_local_ip_addresses()
            if local_ips:
                print(f"   👉 Direcciones IP para conectar teléfonos móviles vía Wi-Fi o Hotspot:")
                for item in local_ips:
                    print(f"      • [{item['alias']}]: http://{item['ip']}:{port}")
            else:
                print(f"   👉 O conecte el teléfono al Wi-Fi/Hotspot de esta PC y abra http://<IP_DE_ESTA_PC>:{port}")
            input("\nPresione Enter para volver al menú principal...")


def main():
    parser = argparse.ArgumentParser(description="SAORI TACTICAL // Emergency, Survival & RF AI Operator")
    parser.add_argument("command", nargs="?", choices=["query", "radio", "morse", "wiki", "pc", "role", "unload", "web", "android", "mesh"], help="Comando rápido de ejecución directa")
    parser.add_argument("args", nargs="*", help="Argumentos del comando")
    parser.add_argument("--role", type=str, default="tactical", choices=["tactical", "coder", "analyst"], help="Rol de modelo IA a emplear")
    parser.add_argument("--port", type=int, default=8090, help="Puerto del servidor web táctico")
    parser.add_argument("--voice", action="store_true", help="Activar respuesta por voz")
    parser.add_argument("--audio", action="store_true", help="Reproducir beeps de audio Morse")
    parser.add_argument("--wav", type=str, default="", help="Ruta para exportar archivo de audio .wav de Morse")

    parsed = parser.parse_args()

    if not parsed.command:
        interactive_cli()
        return

    core = SaoriTacticalCore()
    if parsed.role:
        core.set_ai_role(parsed.role)

    if parsed.command == "query":
        q = " ".join(parsed.args)
        resp = core.process_query(q, voice_reply=parsed.voice, role=parsed.role)
        print(resp)

    elif parsed.command == "radio":
        q = " ".join(parsed.args)
        res = search_frequencies(query=q)
        for f in res:
            print(format_frequency_card(f))

    elif parsed.command == "morse":
        txt = " ".join(parsed.args)
        if not txt:
            print("Uso: saori.bat morse <texto_o_morse> [--audio] [--wav salida.wav]")
            return
        res = auto_translate(txt)
        print("─" * 55)
        print(f"Modo Detectado: {res['mode']}")
        print(f"Texto Natural:  {res['text']}")
        print(f"Código Morse:   {res['morse']}")
        print(f"Deletreo OACI:  {res['phonetic']}")
        print("─" * 55)
        if parsed.wav:
            if generate_morse_wav(res['morse'], parsed.wav):
                print(f"✅ Archivo WAV generado: {parsed.wav}")
            else:
                print(f"❌ Error al generar WAV: {parsed.wav}")
        if parsed.audio or parsed.voice:
            play_morse_sound(res['morse'])

    elif parsed.command == "wiki":
        q = " ".join(parsed.args)
        if q:
            results = search_wiki(q)
            for r in results:
                print(format_wiki_card(r))
        else:
            for item in OFFLINE_WIKI_ENTRIES:
                print(format_wiki_card(item))

    elif parsed.command == "pc":
        bat = PCTacticalTools.get_battery_status()
        hw = PCTacticalTools.get_hardware_telemetry()
        vram = core.llm.get_vram_status()
        print(f"🔋 Batería: {bat['status']} ({bat['percent']}%)")
        print(f"🧠 Hardware: {hw}")
        print(f"🎮 VRAM GPU: {vram or '0 MB (Libre)'}")

    elif parsed.command == "android":
        if not core.android.is_adb_available():
            print("❌ ADB no está disponible o no se encontró en el sistema.")
            return
        devs = core.android.list_devices()
        sub = parsed.args[0].lower() if parsed.args else "status"
        if sub == "wifi":
            if not devs:
                print("❌ No hay teléfonos conectados con depuración USB.")
                return
            target_id = devs[0]["id"]
            print(f"📶 Escaneando redes Wi-Fi usando el chip de radio del teléfono ({devs[0]['model']}):")
            wifis = core.android.scan_wifi_from_device(target_id)
            if wifis:
                for w in wifis:
                    print(f" • SSID: {w['ssid']:<22} RSSI: {w['level_dbm']} dBm Canal: {w['freq_mhz']} MHz BSSID: {w['bssid']}")
            else:
                print(" (No se obtuvieron resultados o se requiere permiso de ubicación en el celular)")
        elif sub == "cmd":
            cmd_str = " ".join(parsed.args[1:])
            if not cmd_str:
                print("Uso: saori.bat android cmd <comando_shell>")
                return
            target_id = devs[0]["id"] if devs else None
            out = core.android.execute_custom_command(cmd_str, target_id)
            print(f"📱 Salida Android:\n{out}")
        else:
            print(f"📱 Dispositivos Android conectados vía ADB: {len(devs)}")
            if not devs:
                print(" (Conecte su Poco X3 Pro o Poco X8 Pro por USB y active 'Depuración USB' en Opciones de Desarrollador)")
            for d in devs:
                status_icon = "✅" if d['is_ready'] else "⚠️"
                print(f" {status_icon} [{d['status'].upper()}] Modelo: {d['model']} (ID: {d['id']})")
                if d['is_ready']:
                    telem = core.android.get_device_telemetry(d['id'])
                    bat_d = telem.get('battery', {})
                    cell = telem.get('cellular', {})
                    print(f"    🔋 Batería: {bat_d.get('level')}% | Temp: {bat_d.get('temp_c')}°C | Cargando: {bat_d.get('charging')}")
                    print(f"    📡 Red Celular: {cell.get('operator')} · Tipo: {cell.get('network_type')} · Señal: {cell.get('signal_level')} ({cell.get('signal_dbm')} dBm)")
                    print(f"    🤖 ROM: {telem.get('rom')}")

    elif parsed.command == "role":
        if parsed.args:
            role_to_set = parsed.args[0].lower()
            if core.set_ai_role(role_to_set):
                print(f"✅ Rol cambiado a: {role_to_set}")
            else:
                print(f"❌ Rol inválido. Opciones: {list(MODEL_FLEET.keys())}")
        else:
            info = core.llm.get_active_model_info()
            print(f"Rol activo: {core.llm.active_role} -> {info['name']} ({info['model']})")

    elif parsed.command == "mesh":
        sub = parsed.args[0].lower() if parsed.args else "status"
        if sub == "send":
            msg_text = " ".join(parsed.args[1:])
            if not msg_text:
                print("Uso: saori.bat mesh send <mensaje_alerta>")
                return
            if core.mesh_p2p.broadcast_message(msg_text, priority="ALERTA"):
                print(f"📡 Mensaje SITREP emitido a la malla local: '{msg_text}'")
            else:
                print("❌ Error al emitir mensaje por broadcast.")
        else:
            peers = core.mesh_p2p.get_active_peers()
            print("╔══════════════════════════════════════════════════════════╗")
            print("║     RED MALLADA CYBERPUNK P2P (BLACKWALL CITADEL)        ║")
            print("╚══════════════════════════════════════════════════════════╝")
            print(f"Nodo Local: {core.mesh_p2p.node_id} [{core.mesh_p2p.node_role}]")
            print(f"Nodos Activos en la Malla Local: {len(peers)}")
            if peers:
                for p in peers:
                    print(f" • [{p['status']}] {p['node_id']} (IP: {p['ip']}:{p['web_port']}) Rol: {p['role']} Latencia: {p['latency_sec']}s")
            else:
                print(" (Esperando balizas UDP de Laptop Nova, tablets o teléfonos en la subred)")
            
            box = core.mesh_p2p.get_mailbox()
            print(f"\nBuzón de Mensajes & SITREP (Store-and-Forward): {len(box)} mensajes")
            for m in box[-5:]:
                print(f" 📨 [{m['sender']} @ {m['sender_ip']}]: {m['content']}")

    elif parsed.command == "unload":
        core.unload_vram()
        print("✅ VRAM de la GPU NVIDIA purgada al 100%.")

    elif parsed.command == "web":
        print(f"Iniciando Servidor Web Táctico en puerto {parsed.port}...")
        t = start_emergency_web_server(core, port=parsed.port)
        print(f"✅ Acceso Local: http://localhost:{parsed.port}")
        local_ips = NetworkSentinel.get_local_ip_addresses()
        if local_ips:
            print("📱 Direcciones para acceder desde teléfonos móviles (Wi-Fi / Hotspot):")
            for item in local_ips:
                print(f"   • [{item['alias']}]: http://{item['ip']}:{parsed.port}")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nDeteniendo servidor web táctico...")


if __name__ == "__main__":
    main()
