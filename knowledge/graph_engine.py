"""
SAORI TACTICAL - Graph-Augmented Emergency Engine (Zero-Token Rapid Response)
Inspirado en OmniAST y Graphify: representa conocimiento de supervivencia, frecuencias y protocolos
como un grafo de conocimiento multidimensional (NetworkX).
Permite resolver consultas críticas en <10 milisegundos sin consumir tokens de LLM.
"""

import networkx as nx
from typing import Dict, List, Optional, Set, Tuple


class EmergencyKnowledgeGraph:
    def __init__(self):
        self.g = nx.DiGraph()
        self._build_graph()

    def _build_graph(self):
        """Construye los nodos y aristas semánticas del grafo táctico."""
        # --- NODOS DE SITUACIÓN / AMENAZA (SITUATION) ---
        self.g.add_node("HEMORRAGIA_ARTERIAL", type="threat", label="Hemorragia Arterial Masiva / Sangrado Pulsátil")
        self.g.add_node("VIA_AEREA_OBSTRUIDA", type="threat", label="Asfixia / Obstrucción de Vía Aérea / Inconsciencia")
        self.g.add_node("AGUA_CONTAMINADA", type="threat", label="Falta de Agua Potable / Sospecha de Patógenos")
        self.g.add_node("TERREMOTO_MAYOR", type="threat", label="Megaterremoto / Sismo 8.0+ en Chile")
        self.g.add_node("TSUNAMI_INMINENTE", type="threat", label="Riesgo de Tsunami en Borde Costero")
        self.g.add_node("CORTE_ELECTRICO_TOTAL", type="threat", label="Blackout Prolongado / Falla de Red Eléctrica")

        # --- NODOS DE PROTOCOLO DE ACCIÓN (ACTION) ---
        self.g.add_node("ACCION_TORNIQUETE", type="action", label="Aplicar Torniquete CAT/SWAT o improvisado 5-7cm sobre herida, ajustar molinete y anotar hora")
        self.g.add_node("ACCION_PRESION_DIRECTA", type="action", label="Presión directa con apósito limpio sobre el vaso sangrante")
        self.g.add_node("ACCION_POSICION_RECUPERACION", type="action", label="Colocar en Posición Lateral de Seguridad y despejar boca")
        self.g.add_node("ACCION_EBULLICION", type="action", label="Hervir a borbotones durante 1 min (o 3 min sobre 2000 msnm)")
        self.g.add_node("ACCION_CLORACION", type="action", label="Dosificar 2 gotas de cloro sin perfume por litro (4 si está turbia) y esperar 30 min")
        self.g.add_node("ACCION_AGACHARSE_CUBRIRSE", type="action", label="Agacharse, Cubrirse bajo mesa firme y Afirmarse (Drop, Cover, Hold On)")
        self.g.add_node("ACCION_EVACUAR_COTA30", type="action", label="Evacuar a pie a zonas seguras sobre la COTA 30 (30 metros de altura)")
        self.g.add_node("ACCION_CORTE_SUMINISTROS", type="action", label="Cerrar llave de paso de gas y bajar interruptor eléctrico general")
        self.g.add_node("ACCION_GESTION_BATERIAS", type="action", label="Proteger baterías 12V: plomo no bajar de 12.0V, desconectar inversores AC no esenciales")

        # --- NODOS DE EQUIPO / HERRAMIENTAS (TOOL) ---
        self.g.add_node("TOOL_TORNIQUETE_CAT", type="tool", label="Torniquete de combate CAT Gen 7 / Banda elástica ancha")
        self.g.add_node("TOOL_CLORO_DOMESTICO", type="tool", label="Hipoclorito de Sodio 5% sin perfume")
        self.g.add_node("TOOL_RECEPTACULO_EBULLICION", type="tool", label="Olla metálica / Fuente de calor o fuego")
        self.g.add_node("TOOL_RADIO_VHF_UHF", type="tool", label="Transceptor de radio VHF/UHF (Baofeng, Yaesu, Kenwood)")
        self.g.add_node("TOOL_BATERIA_12V", type="tool", label="Batería 12V LiFePO4 o AGM / Panel Solar")

        # --- NODOS DE RADIO / FRECUENCIA (FREQUENCY) ---
        self.g.add_node("FREQ_BOMBEROS_155000", type="frequency", label="155.000 MHz (VHF Bomberos Chile)")
        self.g.add_node("FREQ_RNE_154570", type="frequency", label="154.570 MHz (RNE Red Nacional de Emergencia)")
        self.g.add_node("FREQ_HAM_146520", type="frequency", label="146.520 MHz (VHF 2m Llamada / Ham Simplex)")
        self.g.add_node("FREQ_MAR_156800", type="frequency", label="156.800 MHz (VHF Marino Canal 16 Socorro)")
        self.g.add_node("FREQ_SENAPRED_7150", type="frequency", label="7.150 MHz LSB (HF SENAPRED / Emergencia Estatal)")
        self.g.add_node("FREQ_CB_27065", type="frequency", label="27.065 MHz AM (Canal 9 CB Auxilio)")

        # --- CONEXIONES SEMÁNTICAS (EDGES) ---
        # Hemorragia -> Acciones, Herramientas y Frecuencia de auxilio
        self.g.add_edge("HEMORRAGIA_ARTERIAL", "ACCION_PRESION_DIRECTA", rel="paso_inmediato_1")
        self.g.add_edge("HEMORRAGIA_ARTERIAL", "ACCION_TORNIQUETE", rel="paso_inmediato_2")
        self.g.add_edge("ACCION_TORNIQUETE", "TOOL_TORNIQUETE_CAT", rel="requiere_equipo")
        self.g.add_edge("HEMORRAGIA_ARTERIAL", "FREQ_BOMBEROS_155000", rel="canal_socorro_medico")
        self.g.add_edge("HEMORRAGIA_ARTERIAL", "FREQ_HAM_146520", rel="canal_socorro_radioaficionado")

        # Vía Aérea
        self.g.add_edge("VIA_AEREA_OBSTRUIDA", "ACCION_POSICION_RECUPERACION", rel="paso_inmediato")
        self.g.add_edge("VIA_AEREA_OBSTRUIDA", "FREQ_BOMBEROS_155000", rel="canal_socorro_medico")

        # Agua
        self.g.add_edge("AGUA_CONTAMINADA", "ACCION_EBULLICION", rel="metodo_primario")
        self.g.add_edge("AGUA_CONTAMINADA", "ACCION_CLORACION", rel="metodo_quimico")
        self.g.add_edge("ACCION_CLORACION", "TOOL_CLORO_DOMESTICO", rel="requiere_insumo")
        self.g.add_edge("ACCION_EBULLICION", "TOOL_RECEPTACULO_EBULLICION", rel="requiere_equipo")

        # Terremoto
        self.g.add_edge("TERREMOTO_MAYOR", "ACCION_AGACHARSE_CUBRIRSE", rel="durante_el_sismo")
        self.g.add_edge("TERREMOTO_MAYOR", "ACCION_CORTE_SUMINISTROS", rel="tras_el_sismo")
        self.g.add_edge("TERREMOTO_MAYOR", "FREQ_RNE_154570", rel="canal_monitoreo_sismico")
        self.g.add_edge("TERREMOTO_MAYOR", "FREQ_SENAPRED_7150", rel="enlace_regional_hf")

        # Tsunami
        self.g.add_edge("TSUNAMI_INMINENTE", "ACCION_EVACUAR_COTA30", rel="evacuacion_obligatoria")
        self.g.add_edge("TSUNAMI_INMINENTE", "FREQ_MAR_156800", rel="alerta_maritima_directemar")

        # Blackout / Electricidad
        self.g.add_edge("CORTE_ELECTRICO_TOTAL", "ACCION_GESTION_BATERIAS", rel="preservar_comunicaciones")
        self.g.add_edge("ACCION_GESTION_BATERIAS", "TOOL_BATERIA_12V", rel="requiere_equipo")
        self.g.add_edge("CORTE_ELECTRICO_TOTAL", "TOOL_RADIO_VHF_UHF", rel="comunicacion_alternativa")

    def resolve_query(self, query: str) -> Optional[Dict]:
        """
        Búsqueda rápida en el grafo: busca coincidencias directas de conceptos
        y realiza un recorrido de 1 y 2 saltos para generar un resumen ejecutable.
        """
        q = query.lower()
        matched_threats = []

        # Mapeo de términos de entrada a nodos de amenaza
        keywords_map = {
            "HEMORRAGIA_ARTERIAL": ["sangre", "sangrando", "hemorragia", "torniquete", "corte profundo", "herida grave", "arteria"],
            "VIA_AEREA_OBSTRUIDA": ["ahogo", "asfixia", "no respira", "inconsciente", "atragantado", "vía aérea"],
            "AGUA_CONTAMINADA": ["agua", "potable", "hervir", "cloro", "desinfectar agua", "sed", "purificar"],
            "TERREMOTO_MAYOR": ["terremoto", "sismo", "temblor", "derrumbe", "terremoto chile", "grado 8"],
            "TSUNAMI_INMINENTE": ["tsunami", "maremoto", "mar", "costa", "cota 30", "olas"],
            "CORTE_ELECTRICO_TOTAL": ["corte de luz", "blackout", "sin electricidad", "bateria", "inversor", "solar", "energia"]
        }

        for node_id, words in keywords_map.items():
            if any(w in q for w in words):
                matched_threats.append(node_id)

        if not matched_threats:
            return None

        # Tomar la amenaza más relevante
        primary_threat = matched_threats[0]
        threat_data = self.g.nodes[primary_threat]

        actions = []
        tools = []
        frequencies = []

        # Recorrer vecinos salientes en el grafo
        for neighbor in self.g.successors(primary_threat):
            rel = self.g.edges[primary_threat, neighbor].get("rel", "")
            node_info = self.g.nodes[neighbor]
            node_type = node_info.get("type")
            label = node_info.get("label", neighbor)

            if node_type == "action":
                actions.append({"rel": rel, "action": label})
                # Explorar herramientas de segundo salto
                for sub_neighbor in self.g.successors(neighbor):
                    sub_info = self.g.nodes[sub_neighbor]
                    if sub_info.get("type") == "tool":
                        tools.append(sub_info.get("label"))
            elif node_type == "frequency":
                frequencies.append(label)
            elif node_type == "tool":
                tools.append(label)

        return {
            "source": "TACTICAL_KNOWLEDGE_GRAPH (0 Tokens / <1ms)",
            "threat_id": primary_threat,
            "threat_label": threat_data.get("label"),
            "actions": actions,
            "tools": list(set(tools)),
            "frequencies": frequencies
        }
