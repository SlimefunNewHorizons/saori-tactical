"""
SAORI TACTICAL - Emergency Radio & RF Frequency Database
Base de datos exhaustiva de frecuencias de emergencia, auxilio y coordinación.
Enfocada en Chile (SENAPRED, Bomberos, RNE, CE3) e internacional (Marítimo, Aéreo, CB, PMR446, Satélites).
"""

from typing import List, Dict, Optional

CATEGORIES = [
    "CHILE_EMERGENCIA",
    "RADIOAFICIONADOS_HAM",
    "MARITIMO",
    "AERONAUTICO",
    "BANDA_CIUDADANA_CB",
    "PMR446_MONTAÑA",
    "SATELITAL_SAR"
]

FREQUENCIES: List[Dict] = [
    # --- CHILE: EMERGENCIAS Y SERVICIOS PÚBLICOS ---
    {
        "id": "CL-BOMBEROS-NAC",
        "category": "CHILE_EMERGENCIA",
        "name": "Bomberos de Chile - Frecuencia Nacional",
        "freq_mhz": 155.000,
        "mode": "FM",
        "band": "VHF",
        "usage": "Coordinación y despacho de emergencias estructurales, rescate y forestales a nivel nacional.",
        "chile_specific": True
    },
    {
        "id": "CL-BOMBEROS-ALT",
        "category": "CHILE_EMERGENCIA",
        "name": "Bomberos de Chile - Canal Táctico Alternativo",
        "freq_mhz": 155.050,
        "mode": "FM",
        "band": "VHF",
        "usage": "Trabajo en terreno y comando de incidentes inter-compañías.",
        "chile_specific": True
    },
    {
        "id": "CL-RNE-1",
        "category": "CHILE_EMERGENCIA",
        "name": "Red Nacional de Emergencia (RNE Chile) - Canal 1",
        "freq_mhz": 154.570,
        "mode": "FM",
        "band": "VHF",
        "usage": "Comunicaciones civiles de alerta temprana y reporte comunitario ante terremotos y desastres.",
        "chile_specific": True
    },
    {
        "id": "CL-RNE-2",
        "category": "CHILE_EMERGENCIA",
        "name": "Red Nacional de Emergencia (RNE Chile) - Canal 2",
        "freq_mhz": 155.250,
        "mode": "FM",
        "band": "VHF",
        "usage": "Enlace regional de ayuda humanitaria y reporte de cortes de suministro.",
        "chile_specific": True
    },
    {
        "id": "CL-SENAPRED-HF",
        "category": "CHILE_EMERGENCIA",
        "name": "SENAPRED / Red de Emergencia Estatal HF",
        "freq_mhz": 7.150,
        "mode": "LSB",
        "band": "HF (40m)",
        "usage": "Enlace interregional entre direcciones regionales de SENAPRED cuando caen las telecomunicaciones móviles.",
        "chile_specific": True
    },

    # --- RADIOAFICIONADOS (HAM RADIO) ---
    {
        "id": "HAM-VHF-CALLING",
        "category": "RADIOAFICIONADOS_HAM",
        "name": "VHF 2 Metros - Frecuencia Nacional de Llamada Simplex",
        "freq_mhz": 146.520,
        "mode": "FM",
        "band": "VHF",
        "usage": "Frecuencia principal de contacto simplex y socorro entre radioaficionados (FM sin subtono).",
        "chile_specific": False
    },
    {
        "id": "HAM-UHF-CALLING",
        "category": "RADIOAFICIONADOS_HAM",
        "name": "UHF 70 Centímetros - Frecuencia de Llamada Simplex",
        "freq_mhz": 433.500,
        "mode": "FM",
        "band": "UHF",
        "usage": "Llamada directa en 70cm para enlaces locales urbanos y penetración en estructuras.",
        "chile_specific": False
    },
    {
        "id": "HAM-HF-EMERGENCY-40M",
        "category": "RADIOAFICIONADOS_HAM",
        "name": "Red Chilena de Emergencia (FEDERACHI / CE3) - 40 Metros",
        "freq_mhz": 7.090,
        "mode": "LSB",
        "band": "HF (40m)",
        "usage": "Rueda nacional de emergencia diurna de radioaficionados chilenos en catástrofes.",
        "chile_specific": True
    },
    {
        "id": "HAM-HF-EMERGENCY-80M",
        "category": "RADIOAFICIONADOS_HAM",
        "name": "Red Chilena de Emergencia (FEDERACHI / CE3) - 80 Metros",
        "freq_mhz": 3.750,
        "mode": "LSB",
        "band": "HF (80m)",
        "usage": "Rueda nacional de emergencia nocturna en HF ante pérdida total de red celular.",
        "chile_specific": True
    },
    {
        "id": "HAM-APRS-CHILE",
        "category": "RADIOAFICIONADOS_HAM",
        "name": "APRS (Automatic Packet Reporting System) Chile / Región 2",
        "freq_mhz": 144.390,
        "mode": "1200 bps AFSK",
        "band": "VHF",
        "usage": "Transmisión de paquetes digitales con coordenadas GPS, telemetría y mensajes cortos sin internet.",
        "chile_specific": False
    },

    # --- MARÍTIMO (DIRECTEMAR / COSTAS / LAGOS) ---
    {
        "id": "MAR-CH16",
        "category": "MARITIMO",
        "name": "VHF Marino Canal 16 (Distress & Safety)",
        "freq_mhz": 156.800,
        "mode": "FM",
        "band": "VHF",
        "usage": "Canal internacional de SOCORRO, URGENCIA Y LLAMADA marítima (MAYDAY / PAN-PAN). Monitoreado 24/7 por DIRECTEMAR y naves.",
        "chile_specific": False
    },
    {
        "id": "MAR-CH09",
        "category": "MARITIMO",
        "name": "VHF Marino Canal 9 (Alternativo de Emergencia / Recreativo)",
        "freq_mhz": 156.450,
        "mode": "FM",
        "band": "VHF",
        "usage": "Canal secundario de auxilio y coordinación de embarcaciones menores.",
        "chile_specific": False
    },
    {
        "id": "MAR-CH70-DSC",
        "category": "MARITIMO",
        "name": "VHF Marino Canal 70 (Digital Selective Calling - DSC)",
        "freq_mhz": 156.525,
        "mode": "FSK Digital",
        "band": "VHF",
        "usage": "Señalización digital de socorro automática con ID MMSI y posición GPS.",
        "chile_specific": False
    },

    # --- AERONÁUTICO (DGAC / BÚSQUEDA Y SALVAMENTO SAR) ---
    {
        "id": "AIR-GUARD-CIVIL",
        "category": "AERONAUTICO",
        "name": "Frecuencia de Emergencia Aeronáutica Civil (Guard)",
        "freq_mhz": 121.500,
        "mode": "AM",
        "band": "VHF Airband",
        "usage": "Canal mundial de emergencia civil para aeronaves en peligro y radiobalizas ELT clásicas.",
        "chile_specific": False
    },
    {
        "id": "AIR-GUARD-MIL",
        "category": "AERONAUTICO",
        "name": "Frecuencia de Emergencia Militar (SAR)",
        "freq_mhz": 243.000,
        "mode": "AM",
        "band": "UHF Airband",
        "usage": "Segundo canal de socorro aéreo internacional para fuerzas militares y operaciones de búsqueda.",
        "chile_specific": False
    },

    # --- BANDA CIUDADANA (CB / 11 METROS) ---
    {
        "id": "CB-CH09",
        "category": "BANDA_CIUDADANA_CB",
        "name": "Banda Ciudadana (CB) Canal 9 - Emergencia",
        "freq_mhz": 27.065,
        "mode": "AM",
        "band": "HF (11m)",
        "usage": "Canal oficial y mundial de socorro, seguridad vial y auxilio para usuarios de radios CB.",
        "chile_specific": False
    },
    {
        "id": "CB-CH19",
        "category": "BANDA_CIUDADANA_CB",
        "name": "Banda Ciudadana (CB) Canal 19 - Carretera / Camioneros",
        "freq_mhz": 27.185,
        "mode": "AM",
        "band": "HF (11m)",
        "usage": "Monitoreo de tráfico, cortes de ruta, derrumbes y advertencias meteorológicas en carretera.",
        "chile_specific": False
    },

    # --- PMR446 / MONTAÑA & OUTDOOR ---
    {
        "id": "PMR-CANAL-7-7",
        "category": "PMR446_MONTAÑA",
        "name": "Canal 7-7 de Seguridad en Montaña (PMR446)",
        "freq_mhz": 446.08125,
        "mode": "FM",
        "subtone_ctcss": "85.4 Hz (Subtono 7)",
        "band": "UHF",
        "usage": "Iniciativa internacional de seguridad en montaña y senderismo. Canal 7 con CTCSS 7.",
        "chile_specific": False
    },
    {
        "id": "PMR-CANAL-8-16",
        "category": "PMR446_MONTAÑA",
        "name": "Canal 8-16 de Emergencia en Montaña (PMR446)",
        "freq_mhz": 446.09375,
        "mode": "FM",
        "subtone_ctcss": "114.8 Hz (Subtono 16)",
        "band": "UHF",
        "usage": "Canal de radio de auxilio en trekking, cordillera y rescate agreste.",
        "chile_specific": False
    },

    # --- SATELITAL / BALIZAS SAR ---
    {
        "id": "SAR-COSPAS-406",
        "category": "SATELITAL_SAR",
        "name": "COSPAS-SARSAT Radiobalizas EPIRB / ELT / PLB",
        "freq_mhz": 406.037,
        "mode": "Digital FSK",
        "band": "UHF",
        "usage": "Balizas personales de rescate vía constelación de satélites internacionales.",
        "chile_specific": False
    }
]


def search_frequencies(query: str = "", category: str = "", chile_only: bool = False) -> List[Dict]:
    """Busca frecuencias por texto libre, categoría o filtro territorial."""
    q = query.lower().strip()
    results = []
    for item in FREQUENCIES:
        if category and item["category"] != category:
            continue
        if chile_only and not item.get("chile_specific", False):
            continue
        if not q:
            results.append(item)
            continue
        
        searchable_text = f"{item['id']} {item['name']} {item['freq_mhz']} {item['band']} {item['mode']} {item['usage']}".lower()
        if q in searchable_text:
            results.append(item)
    return results


def format_frequency_card(freq_entry: Dict) -> str:
    """Genera una ficha táctica de frecuencia formateada para terminal o reporte."""
    subtone_str = f" | Subtono: {freq_entry['subtone_ctcss']}" if "subtone_ctcss" in freq_entry else ""
    chile_tag = " [CHILE]" if freq_entry.get("chile_specific") else ""
    return (
        f"┌─ [{freq_entry['id']}]{chile_tag} {freq_entry['name']}\n"
        f"│  Frecuencia: {freq_entry['freq_mhz']:.4f} MHz ({freq_entry['band']}) | Modo: {freq_entry['mode']}{subtone_str}\n"
        f"│  Uso: {freq_entry['usage']}\n"
        f"└─────────────────────────────────────────────────────────────"
    )
