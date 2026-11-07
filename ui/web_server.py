"""
SAORI TACTICAL - Emergency Web Dashboard Server & Mobile Station
Servidor HTTP autónomo sin dependencias externas (usa http.server nativo de Python).
Permite conectar cualquier smartphone vía Wi-Fi local o Windows Mobile Hotspot sin router ni internet.
"""

import http.server
import socketserver
import json
import threading
from typing import Optional, Callable
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

HTML_PAGE = r"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>SAORI TACTICAL // OS</title>
    <style>
        :root {
            --bg: #0a0e14;
            --card: #131920;
            --accent: #00e5ff;
            --alert: #ff3366;
            --text: #e6edf3;
            --muted: #8b949e;
            --border: #30363d;
            --green: #3fb950;
            --gold: #f1e05a;
            --purple: #d2a8ff;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            background-color: var(--bg);
            color: var(--text);
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace;
            padding: 14px;
            max-width: 960px;
            margin: auto;
        }
        header {
            border-bottom: 2px solid var(--accent);
            padding-bottom: 12px;
            margin-bottom: 14px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 10px;
        }
        h1 { font-size: 1.35rem; color: var(--accent); letter-spacing: 1px; }
        .badge {
            background: #1f6feb22;
            color: var(--accent);
            border: 1px solid var(--accent);
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: bold;
        }
        .status-bar {
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 10px 14px;
            margin-bottom: 14px;
            font-size: 0.82rem;
            display: flex;
            gap: 14px;
            flex-wrap: wrap;
            align-items: center;
            justify-content: space-between;
        }
        .status-val { font-weight: bold; color: var(--green); }
        .role-selector {
            display: flex;
            gap: 6px;
            align-items: center;
            flex-wrap: wrap;
        }
        .role-btn {
            background: #21262d;
            color: var(--text);
            border: 1px solid var(--border);
            padding: 5px 10px;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: bold;
            cursor: pointer;
        }
        .role-btn.active {
            background: var(--accent);
            color: #000;
            border-color: var(--accent);
        }
        .btn-purge {
            background: #da363322;
            color: #f85149;
            border: 1px solid #da3633;
            padding: 5px 10px;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: bold;
            cursor: pointer;
        }
        .btn-purge:hover { background: #da3633; color: #fff; }
        .tabs { display: flex; gap: 6px; margin-bottom: 14px; flex-wrap: wrap; }
        .tab-btn {
            background: var(--card);
            border: 1px solid var(--border);
            color: var(--text);
            padding: 8px 12px;
            border-radius: 6px;
            cursor: pointer;
            font-weight: bold;
            font-size: 0.8rem;
            transition: all 0.15s ease;
        }
        .tab-btn.active {
            background: var(--accent);
            color: #000;
            border-color: var(--accent);
        }
        .card {
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 16px;
        }
        .search-box {
            display: flex;
            gap: 8px;
            margin-bottom: 14px;
        }
        input[type="text"], textarea {
            width: 100%;
            background: #0d1117;
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 10px 14px;
            color: #fff;
            font-family: monospace;
            font-size: 0.95rem;
        }
        input[type="text"]:focus, textarea:focus {
            outline: none;
            border-color: var(--accent);
        }
        button.btn-action {
            background: var(--accent);
            color: #000;
            border: none;
            border-radius: 6px;
            padding: 10px 16px;
            font-weight: bold;
            cursor: pointer;
            white-space: nowrap;
        }
        button.btn-sec {
            background: #21262d;
            color: var(--text);
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 8px 14px;
            font-weight: bold;
            cursor: pointer;
        }
        button.btn-sec:hover { border-color: var(--accent); color: var(--accent); }
        .result-box {
            background: #0d1117;
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 14px;
            white-space: pre-wrap;
            font-family: monospace;
            font-size: 0.9rem;
            line-height: 1.5;
            min-height: 100px;
        }
        .freq-item {
            border-left: 3px solid var(--accent);
            padding: 8px 12px;
            margin-bottom: 10px;
            background: #0d1117;
            border-radius: 0 4px 4px 0;
        }
        .freq-title { font-weight: bold; color: #fff; }
        .freq-meta { font-size: 0.8rem; color: var(--accent); margin: 3px 0; }
        .freq-desc { font-size: 0.85rem; color: var(--muted); }
        .morse-display {
            font-size: 1.35rem;
            letter-spacing: 3px;
            color: var(--gold);
            background: #0d1117;
            padding: 14px;
            border-radius: 6px;
            border: 1px solid var(--border);
            word-break: break-all;
            margin-bottom: 12px;
        }
        .phonetic-box {
            font-size: 0.9rem;
            color: var(--accent);
            background: #0d1117;
            padding: 10px;
            border-radius: 6px;
            margin-bottom: 12px;
            border: 1px dashed var(--border);
        }
        .controls-row {
            display: flex;
            gap: 10px;
            margin-bottom: 12px;
            align-items: center;
            flex-wrap: wrap;
        }
        .qcode-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
            gap: 10px;
        }
        .qcode-card {
            background: #0d1117;
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 10px;
        }
        .qcode-code { color: var(--gold); font-weight: bold; font-size: 1rem; }
        .qcode-meaning { font-size: 0.85rem; color: var(--text); margin-top: 4px; }
        .wiki-card {
            background: #0d1117;
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 14px;
            margin-bottom: 14px;
        }
        .wiki-cat {
            display: inline-block;
            background: #23863622;
            color: var(--green);
            border: 1px solid var(--green);
            font-size: 0.72rem;
            padding: 2px 6px;
            border-radius: 4px;
            font-weight: bold;
            margin-bottom: 6px;
        }
        .wiki-title { font-size: 1.1rem; color: #fff; font-weight: bold; margin-bottom: 6px; }
        .wiki-summary { font-size: 0.88rem; color: var(--muted); margin-bottom: 10px; }
        .wiki-sub { font-size: 0.82rem; font-weight: bold; color: var(--accent); margin: 8px 0 4px 0; }
        .wiki-list { font-size: 0.85rem; line-height: 1.5; color: var(--text); padding-left: 18px; }
        .wiki-note {
            background: #388bfd15;
            border-left: 3px solid #58a6ff;
            padding: 8px 12px;
            font-size: 0.82rem;
            color: #c9d1d9;
            margin-top: 10px;
            border-radius: 0 4px 4px 0;
        }
        .diag-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 12px;
            margin-bottom: 16px;
        }
        .diag-card {
            background: #0d1117;
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 12px;
        }
        .diag-card h4 { color: var(--accent); font-size: 0.85rem; margin-bottom: 6px; }
        .diag-card .val { font-size: 1.15rem; font-weight: bold; color: #fff; }
    </style>
</head>
<body>
    <header>
        <div>
            <h1>SAORI TACTICAL // OS</h1>
            <div style="font-size: 0.75rem; color: var(--muted);">Emergency Response, Morse, Survival Wiki & RF</div>
        </div>
        <div style="display:flex; gap:8px; align-items:center;">
            <div class="badge" id="vramBadge">VRAM: 0 MB (LIBRE)</div>
            <button class="btn-purge" onclick="purgeVram()" title="Liberar memoria GPU de inmediato">🧹 PURGAR VRAM</button>
        </div>
    </header>

    <div class="status-bar" id="statusBar">
        <div>RED: <span class="status-val" id="netStatus">MONITOREANDO...</span></div>
        <div>LATENCIA: <span id="netLatency">-</span></div>
        <div>ENERGÍA: <span id="pwrStatus" style="color:var(--gold); font-weight:bold;">AC / BATERÍA</span></div>
        <div class="role-selector">
            <span style="color:var(--muted);">ROL IA:</span>
            <button class="role-btn active" id="btnRoleTactical" onclick="setAiRole('tactical')">🚨 TACTICAL (3B)</button>
            <button class="role-btn" id="btnRoleCoder" onclick="setAiRole('coder')">💻 CODER (3B)</button>
            <button class="role-btn" id="btnRoleAnalyst" onclick="setAiRole('analyst')">🧠 ANALYST (1.5B)</button>
        </div>
    </div>

    <div class="tabs">
        <button class="tab-btn active" onclick="switchTab('queryTab')">⚡ CONSULTA TÁCTICA</button>
        <button class="tab-btn" onclick="switchTab('morseTab')">📻 ESTUDIO MORSE</button>
        <button class="tab-btn" onclick="switchTab('radioTab')">📡 FRECUENCIAS</button>
        <button class="tab-btn" onclick="switchTab('wikiTab')">🛠️ WIKI CONSTRUCCIÓN</button>
        <button class="tab-btn" onclick="switchTab('pcTab')">💻 HARDWARE & PC</button>
        <button class="tab-btn" onclick="switchTab('qcodeTab')">📜 CÓDIGOS Q</button>
    </div>

    <!-- PESTAÑA 1: CONSULTAS TÁCTICAS -->
    <div id="queryTab">
        <div class="card">
            <div class="search-box">
                <input type="text" id="queryInput" placeholder="Ej: hemorragia arterial, potabilizar agua con cloro, radio de emergencia..." onkeydown="if(event.key==='Enter') executeQuery()">
                <button class="btn-action" onclick="executeQuery()">CONSULTAR</button>
            </div>
            <div class="result-box" id="resultOutput">Escriba una consulta de emergencia. El sistema buscará primero en el Grafo de Supervivencia (<1ms / 0 tokens) y complementará con el modelo IA local activo en la GPU RTX 4060.</div>
        </div>
    </div>

    <!-- PESTAÑA 2: ESTUDIO MORSE INTERACTIVO -->
    <div id="morseTab" style="display:none;">
        <div class="card">
            <h3 style="margin-bottom: 8px; color: var(--accent);">Traductor Bidireccional de Código Morse</h3>
            <div style="font-size: 0.85rem; color: var(--muted); margin-bottom: 12px;">
                Escriba en lenguaje natural (ej: <code>MAYDAY SOS NECESITO AGUA</code>) o pegue código Morse (ej: <code>... --- ...</code>). Se traduce en tiempo real.
            </div>

            <textarea id="morseInput" rows="3" placeholder="Escriba texto o Morse aquí..." oninput="handleMorseInput()"></textarea>

            <div style="margin-top: 12px;">
                <label style="font-size: 0.8rem; color: var(--muted);">REPRESENTACIÓN EN CÓDIGO MORSE:</label>
                <div class="morse-display" id="morseOutput">... --- ...</div>
            </div>

            <div>
                <label style="font-size: 0.8rem; color: var(--muted);">DELETREO FONÉTICO OACI / OTAN:</label>
                <div class="phonetic-box" id="phoneticOutput">Sierra Oscar Sierra</div>
            </div>

            <div class="controls-row">
                <button class="btn-action" onclick="playMorseWebAudio()">🔊 REPRODUCIR AUDIO MORSE</button>
                <button class="btn-sec" onclick="stopMorseAudio()">⏹ DETENER</button>
                <span style="font-size: 0.85rem; color: var(--muted);">Velocidad:</span>
                <select id="wpmSelect" style="background:#0d1117; color:#fff; border:1px solid var(--border); padding:6px; border-radius:4px;">
                    <option value="12">12 WPM (Lento)</option>
                    <option value="16" selected>16 WPM (Estándar Campo)</option>
                    <option value="20">20 WPM (Rápido)</option>
                    <option value="25">25 WPM (Experto)</option>
                </select>
                <span style="font-size: 0.85rem; color: var(--muted);">Tono: 700 Hz</span>
            </div>
        </div>
    </div>

    <!-- PESTAÑA 3: FRECUENCIAS DE RADIO -->
    <div id="radioTab" style="display:none;">
        <div class="card">
            <h3 style="margin-bottom: 12px; color: var(--accent);">Directorio de Frecuencias de Emergencia (Chile e Internacional)</h3>
            <div id="freqList">Cargando frecuencias...</div>
        </div>
    </div>

    <!-- PESTAÑA 4: WIKI DE CONSTRUCCIÓN & PLANOS -->
    <div id="wikiTab" style="display:none;">
        <div class="card">
            <h3 style="margin-bottom: 8px; color: var(--accent);">Wiki de Construcción & Ingeniería de Campo (Blueprints Offline)</h3>
            <div style="font-size: 0.85rem; color: var(--muted); margin-bottom: 12px;">
                Planos técnicos para fabricar herramientas, antenas de largo alcance, bancos de energía 12V y filtros de agua sin internet.
            </div>
            <div class="search-box">
                <input type="text" id="wikiSearchInput" placeholder="Filtrar por término (ej: antena, bioarena, 12v, destilador, refugio)..." oninput="filterWiki()">
            </div>
            <div id="wikiContainer">Cargando planos...</div>
        </div>
    </div>

    <!-- PESTAÑA 5: DIAGNÓSTICO HARDWARE & PC -->
    <div id="pcTab" style="display:none;">
        <div class="card">
            <h3 style="margin-bottom: 14px; color: var(--accent);">Telemetría y Diagnóstico del PC en Emergencia</h3>
            
            <div class="diag-grid">
                <div class="diag-card">
                    <h4>ENERGÍA / UPS</h4>
                    <div class="val" id="diagBattery">-</div>
                    <div style="font-size:0.75rem; color:var(--muted); margin-top:4px;" id="diagRuntime">Autonomía: -</div>
                </div>
                <div class="diag-card">
                    <h4>CARGA DE CPU</h4>
                    <div class="val" id="diagCPU">-</div>
                </div>
                <div class="diag-card">
                    <h4>MEMORIA RAM</h4>
                    <div class="val" id="diagRAM">-</div>
                    <div style="font-size:0.75rem; color:var(--muted); margin-top:4px;" id="diagRAMFree">Libre: -</div>
                </div>
                <div class="diag-card">
                    <h4>GPU NVIDIA RTX 4060</h4>
                    <div class="val" id="diagVRAM">-</div>
                </div>
            </div>

            <h4 style="color:var(--accent); margin-bottom:8px;">SEÑALES WI-FI SOBREVIVIENTES EN EL ENTORNO:</h4>
            <div id="wifiScanBox" class="result-box" style="min-height:70px; margin-bottom:16px;">Escaneando...</div>

            <h4 style="color:var(--accent); margin-bottom:8px;">📱 ESTACIÓN DE SENSORES ANDROID (ADB - Poco X3 Pro / Poco X8 Pro):</h4>
            <div id="androidBox" class="result-box" style="min-height:70px; margin-bottom:16px;">Verificando dispositivos ADB...</div>

            <h4 style="color:var(--accent); margin-bottom:8px;">CONSOLA DE DIAGNÓSTICO POWERSHELL SEGURA:</h4>
            <div class="search-box">
                <input type="text" id="psCmdInput" placeholder="Ej: Get-NetIPAddress | Select IPAddress, InterfaceAlias" onkeydown="if(event.key==='Enter') executePSCommand()">
                <button class="btn-action" onclick="executePSCommand()">EJECUTAR</button>
            </div>
            <div id="psCmdOutput" class="result-box" style="min-height:90px;">Salida del comando...</div>
        </div>
    </div>

    <!-- PESTAÑA 6: CÓDIGOS Q Y SEÑALES -->
    <div id="qcodeTab" style="display:none;">
        <div class="card">
            <h3 style="margin-bottom: 12px; color: var(--accent);">Glosario Táctico de Códigos Q y Señales de Radioaficionados</h3>
            <div class="qcode-grid" id="qcodeList">Cargando códigos...</div>
        </div>
    </div>

    <script>
        let allWikiEntries = [];

        function switchTab(tabId) {
            ['queryTab', 'morseTab', 'radioTab', 'wikiTab', 'pcTab', 'qcodeTab'].forEach(t => {
                document.getElementById(t).style.display = t === tabId ? 'block' : 'none';
            });
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            event.target.classList.add('active');
            if (tabId === 'radioTab') loadFrequencies();
            if (tabId === 'wikiTab') loadWiki();
            if (tabId === 'pcTab') loadPCDiagnostics();
            if (tabId === 'qcodeTab') loadQCodes();
        }

        async function updateStatus() {
            try {
                const res = await fetch('/api/status');
                const data = await res.json();
                document.getElementById('netStatus').innerText = data.status || 'OK';
                document.getElementById('netLatency').innerText = (data.latency_ms ? data.latency_ms + ' ms' : 'OFFLINE');
                
                // VRAM badge
                const vBadge = document.getElementById('vramBadge');
                if (data.vram_models && data.vram_models.length > 0) {
                    const names = data.vram_models.map(m => m.name).join(', ');
                    vBadge.innerText = 'VRAM: ' + names + ' (CARGADA)';
                    vBadge.style.color = '#f1e05a';
                    vBadge.style.borderColor = '#f1e05a';
                } else {
                    vBadge.innerText = 'VRAM: 0 MB (LIBRE)';
                    vBadge.style.color = '#3fb950';
                    vBadge.style.borderColor = '#3fb950';
                }

                // Active model buttons
                const activeRole = (data.active_model && data.active_model.model) ? data.active_model.model : '';
                updateRoleButtons(activeRole);
            } catch(e) {}
        }
        setInterval(updateStatus, 4000);
        updateStatus();

        function updateRoleButtons(modelStr) {
            const bTac = document.getElementById('btnRoleTactical');
            const bCod = document.getElementById('btnRoleCoder');
            const bAna = document.getElementById('btnRoleAnalyst');
            [bTac, bCod, bAna].forEach(b => b.classList.remove('active'));
            if (modelStr.includes('coder')) bCod.classList.add('active');
            else if (modelStr.includes('deepseek')) bAna.classList.add('active');
            else bTac.classList.add('active');
        }

        async function setAiRole(role) {
            try {
                await fetch('/api/models/set', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({role: role})
                });
                updateStatus();
            } catch(e) {}
        }

        async function purgeVram() {
            const vBadge = document.getElementById('vramBadge');
            vBadge.innerText = 'VRAM: Purgando...';
            try {
                await fetch('/api/vram/unload', {method: 'POST'});
                setTimeout(updateStatus, 800);
            } catch(e) {}
        }

        async function executeQuery() {
            const input = document.getElementById('queryInput');
            const q = input.value.trim();
            if (!q) return;
            const out = document.getElementById('resultOutput');
            out.innerText = "⏳ Procesando en Grafo de Supervivencia y Modelo IA Local...";
            try {
                const res = await fetch('/api/query', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({query: q})
                });
                const data = await res.json();
                out.innerText = data.response;
            } catch(e) {
                out.innerText = "Error al consultar: " + e;
            }
        }

        async function loadWiki() {
            try {
                const res = await fetch('/api/wiki');
                allWikiEntries = await res.json();
                renderWiki(allWikiEntries);
            } catch(e) {}
        }

        function filterWiki() {
            const q = document.getElementById('wikiSearchInput').value.toLowerCase().trim();
            if (!q) {
                renderWiki(allWikiEntries);
                return;
            }
            const filtered = allWikiEntries.filter(item => {
                const text = (item.title + ' ' + item.category + ' ' + item.summary + ' ' + item.materials.join(' ')).toLowerCase();
                return text.includes(q);
            });
            renderWiki(filtered);
        }

        function renderWiki(entries) {
            const container = document.getElementById('wikiContainer');
            if (!entries || entries.length === 0) {
                container.innerHTML = '<div style="color:var(--muted); font-size:0.9rem;">No se encontraron planos de construcción con ese término.</div>';
                return;
            }
            container.innerHTML = entries.map(item => `
                <div class="wiki-card">
                    <span class="wiki-cat">${item.category}</span>
                    <div class="wiki-title">🛠️ ${item.title}</div>
                    <div class="wiki-summary">${item.summary}</div>
                    <div class="wiki-sub">MATERIALES REQUERIDOS:</div>
                    <ul class="wiki-list">${item.materials.map(m => `<li>${m}</li>`).join('')}</ul>
                    <div class="wiki-sub">PLANOS & PASOS DE CONSTRUCCIÓN:</div>
                    <ol class="wiki-list">${item.blueprints_steps.map(s => `<li>${s.replace(/^[0-9]+\.\s*/, '')}</li>`).join('')}</ol>
                    <div class="wiki-note">💡 <b>Nota de Ingeniería:</b> ${item.engineering_notes}</div>
                </div>
            `).join('');
        }

        async function loadPCDiagnostics() {
            try {
                const res = await fetch('/api/pc');
                const data = await res.json();
                
                // Batería
                const bat = data.battery || {};
                document.getElementById('diagBattery').innerText = (bat.percent ? bat.percent + '%' : '100%') + ' · ' + (bat.status || 'AC');
                document.getElementById('diagRuntime').innerText = bat.runtime_min ? `Autonomía: ~${bat.runtime_min} min` : 'Conectado a Red Eléctrica / UPS';
                document.getElementById('pwrStatus').innerText = (bat.status || 'AC');

                // Hardware
                const hw = data.hardware || {};
                document.getElementById('diagCPU').innerText = (hw.cpu_load_pct !== undefined ? hw.cpu_load_pct + '%' : 'N/A');
                document.getElementById('diagRAM').innerText = (hw.used_ram_gb ? `${hw.used_ram_gb} GB / ${hw.total_ram_gb} GB` : 'N/A');
                document.getElementById('diagRAMFree').innerText = hw.free_ram_gb ? `Libre: ${hw.free_ram_gb} GB` : '';

                // VRAM
                const vmods = data.vram || [];
                document.getElementById('diagVRAM').innerText = (vmods.length > 0) ? vmods.map(m => m.name).join(', ') : '0 MB (100% Libre)';

                // Wi-Fi Scan
                const wBox = document.getElementById('wifiScanBox');
                const wifis = data.wifi || [];
                if (wifis.length > 0) {
                    wBox.innerText = wifis.map(w => `• [${w.signal}] SSID: ${w.ssid}`).join('\n');
                } else {
                    wBox.innerText = '(No se detectaron redes Wi-Fi activas en los alrededores o adaptador ocupado)';
                }

                // Android ADB Scan
                try {
                    const resA = await fetch('/api/android');
                    const dataA = await resA.json();
                    const aBox = document.getElementById('androidBox');
                    if (dataA.devices && dataA.devices.length > 0) {
                        aBox.innerHTML = dataA.devices.map((d, i) => {
                            const t = (dataA.telemetry && dataA.telemetry[i]) ? dataA.telemetry[i] : {};
                            const b = t.battery || {};
                            const c = t.cellular || {};
                            return `• <b>${d.model}</b> [${d.status.toUpperCase()}] ID: ${d.id}<br>` +
                                   `  🔋 Batería: ${b.level || '?'}% (${b.temp_c || '?'}°C) | ` +
                                   `  📡 Red: <span style="color:var(--gold);">${c.operator || 'N/A'}</span> (${c.network_type || '-'}) Señal: <b>${c.signal_level || '-'}</b> (${c.signal_dbm || '?'} dBm)`;
                        }).join('<br><br>');
                    } else {
                        aBox.innerHTML = '<span style="color:var(--muted);">(No hay smartphones conectados por USB o Wi-Fi ADB. Conecte su Poco X3 Pro con Depuración USB activa para usar sus sensores de red celular y Wi-Fi)</span>';
                    }
                } catch(e) {}
            } catch(e) {}
        }

        async function executePSCommand() {
            const input = document.getElementById('psCmdInput');
            const cmd = input.value.trim();
            if (!cmd) return;
            const out = document.getElementById('psCmdOutput');
            out.innerText = "⏳ Ejecutando diagnóstico en Windows PowerShell...";
            try {
                const res = await fetch('/api/pc/cmd', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({cmd: cmd})
                });
                const data = await res.json();
                out.innerText = data.output;
            } catch(e) {
                out.innerText = "Error: " + e;
            }
        }

        async function loadFrequencies() {
            try {
                const res = await fetch('/api/radio');
                const list = await res.json();
                const container = document.getElementById('freqList');
                container.innerHTML = list.map(f => `
                    <div class="freq-item">
                        <div class="freq-title">${f.name}</div>
                        <div class="freq-meta">${f.freq_mhz.toFixed(4)} MHz (${f.band}) · Modo: ${f.mode}</div>
                        <div class="freq-desc">${f.usage}</div>
                    </div>
                `).join('');
            } catch(e) {}
        }

        async function loadQCodes() {
            try {
                const res = await fetch('/api/qcodes');
                const qcodes = await res.json();
                const container = document.getElementById('qcodeList');
                container.innerHTML = Object.entries(qcodes).map(([code, desc]) => `
                    <div class="qcode-card">
                        <div class="qcode-code">${code}</div>
                        <div class="qcode-meaning">${desc}</div>
                    </div>
                `).join('');
            } catch(e) {}
        }

        // --- MOTOR MORSE WEB NATIVO (100% OFFLINE VIA WEB AUDIO API) ---
        let audioContext = null;
        let isPlayingMorse = false;
        let morseTimeouts = [];

        async function handleMorseInput() {
            const txt = document.getElementById('morseInput').value;
            if (!txt.trim()) {
                document.getElementById('morseOutput').innerText = "";
                document.getElementById('phoneticOutput').innerText = "";
                return;
            }
            try {
                const res = await fetch('/api/morse', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({text: txt})
                });
                const data = await res.json();
                document.getElementById('morseOutput').innerText = data.morse;
                document.getElementById('phoneticOutput').innerText = data.phonetic;
            } catch(e) {}
        }

        function stopMorseAudio() {
            isPlayingMorse = false;
            morseTimeouts.forEach(t => clearTimeout(t));
            morseTimeouts = [];
        }

        function playTone(freq, durationSec, startTime) {
            const osc = audioContext.createOscillator();
            const gain = audioContext.createGain();
            osc.type = 'sine';
            osc.frequency.value = freq;

            gain.gain.setValueAtTime(0, startTime);
            gain.gain.linearRampToValueAtTime(0.3, startTime + 0.005);
            gain.gain.setValueAtTime(0.3, startTime + durationSec - 0.005);
            gain.gain.linearRampToValueAtTime(0, startTime + durationSec);

            osc.connect(gain);
            gain.connect(audioContext.destination);

            osc.start(startTime);
            osc.stop(startTime + durationSec);
        }

        function playMorseWebAudio() {
            stopMorseAudio();
            const morseStr = document.getElementById('morseOutput').innerText.trim();
            if (!morseStr) return;

            if (!audioContext) {
                audioContext = new (window.AudioContext || window.webkitAudioContext)();
            }
            if (audioContext.state === 'suspended') {
                audioContext.resume();
            }

            isPlayingMorse = true;
            const wpm = parseInt(document.getElementById('wpmSelect').value) || 16;
            const dotDuration = 1.2 / wpm;
            const dashDuration = dotDuration * 3;
            const elementGap = dotDuration;
            const letterGap = dotDuration * 3;
            const wordGap = dotDuration * 7;
            const freqHz = 700;

            let currentTime = audioContext.currentTime + 0.05;

            for (let char of morseStr) {
                if (!isPlayingMorse) break;
                if (char === '.') {
                    playTone(freqHz, dotDuration, currentTime);
                    currentTime += dotDuration + elementGap;
                } else if (char === '-') {
                    playTone(freqHz, dashDuration, currentTime);
                    currentTime += dashDuration + elementGap;
                } else if (char === ' ') {
                    currentTime += (letterGap - elementGap);
                } else if (char === '/') {
                    currentTime += (wordGap - letterGap);
                }
            }
        }
    </script>
</body>
</html>
"""


class TacticalWebHandler(http.server.BaseHTTPRequestHandler):
    dispatcher = None

    def log_message(self, format, *args):
        return

    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode("utf-8"))
        elif self.path == "/api/status":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            status = self.dispatcher.get_status() if self.dispatcher else {"status": "STANDBY"}
            self.wfile.write(json.dumps(status, ensure_ascii=False).encode("utf-8"))
        elif self.path == "/api/radio":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            from radio.freq_db import FREQUENCIES
            self.wfile.write(json.dumps(FREQUENCIES, ensure_ascii=False).encode("utf-8"))
        elif self.path == "/api/qcodes":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            from radio.rf_tools import Q_CODES
            self.wfile.write(json.dumps(Q_CODES, ensure_ascii=False).encode("utf-8"))
        elif self.path == "/api/wiki":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            from knowledge.offline_wiki import OFFLINE_WIKI_ENTRIES
            self.wfile.write(json.dumps(OFFLINE_WIKI_ENTRIES, ensure_ascii=False).encode("utf-8"))
        elif self.path == "/api/pc":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            from brain.pc_tools import PCTacticalTools
            bat = PCTacticalTools.get_battery_status()
            hw = PCTacticalTools.get_hardware_telemetry()
            wifis = PCTacticalTools.scan_surviving_wifi()
            vmods = self.dispatcher.llm.get_vram_status() if self.dispatcher else []
            data = {"battery": bat, "hardware": hw, "wifi": wifis, "vram": vmods}
            self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))
        elif self.path == "/api/models":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            from brain.local_llm import MODEL_FLEET
            active_role = self.dispatcher.llm.active_role if self.dispatcher else "tactical"
            self.wfile.write(json.dumps({"active_role": active_role, "fleet": MODEL_FLEET}, ensure_ascii=False).encode("utf-8"))
        elif self.path == "/api/android":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            data = {"available": False, "devices": [], "telemetry": []}
            if self.dispatcher and hasattr(self.dispatcher, "android") and self.dispatcher.android.is_adb_available():
                devs = self.dispatcher.android.list_devices()
                telem = [self.dispatcher.android.get_device_telemetry(d["id"]) for d in devs if d.get("is_ready")]
                data = {"available": True, "devices": devs, "telemetry": telem}
            self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))
        elif self.path == "/api/android/wifi":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            res = []
            if self.dispatcher and hasattr(self.dispatcher, "android") and self.dispatcher.android.is_adb_available():
                devs = self.dispatcher.android.list_devices()
                if devs:
                    res = self.dispatcher.android.scan_wifi_from_device(devs[0]["id"])
            self.wfile.write(json.dumps(res, ensure_ascii=False).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8")
        data = json.loads(body or "{}")

        if self.path == "/api/query":
            query = data.get("query", "")
            role = data.get("role")
            resp_text = self.dispatcher.process_query(query, role=role) if self.dispatcher else "Servicio no listo."
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"response": resp_text}, ensure_ascii=False).encode("utf-8"))

        elif self.path == "/api/morse":
            text = data.get("text", "")
            from radio.rf_tools import auto_translate
            trans = auto_translate(text)
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(trans, ensure_ascii=False).encode("utf-8"))

        elif self.path == "/api/models/set":
            role = data.get("role", "tactical")
            ok = self.dispatcher.set_ai_role(role) if self.dispatcher else False
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"success": ok, "role": role}, ensure_ascii=False).encode("utf-8"))

        elif self.path == "/api/vram/unload":
            ok = self.dispatcher.unload_vram() if self.dispatcher else False
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"success": ok, "message": "VRAM purgada al 100%"}, ensure_ascii=False).encode("utf-8"))

        elif self.path == "/api/pc/cmd":
            cmd = data.get("cmd", "")
            from brain.pc_tools import PCTacticalTools
            output = PCTacticalTools.execute_powershell_safely(cmd)
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"output": output}, ensure_ascii=False).encode("utf-8"))

        else:
            self.send_response(404)
            self.end_headers()


def start_emergency_web_server(dispatcher, port: int = 8090) -> threading.Thread:
    """Inicia el servidor web táctico en un hilo secundario."""
    TacticalWebHandler.dispatcher = dispatcher
    server = socketserver.TCPServer(("0.0.0.0", port), TacticalWebHandler)
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()
    return t
