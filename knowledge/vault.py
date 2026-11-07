"""
SAORI TACTICAL - Curated Emergency, Medical & Survival Knowledge Vault
Protocolos de acción inmediata pre-procesados para situaciones de desastre y corte total de servicios.
"""

from typing import List, Dict

SURVIVAL_VAULT: List[Dict] = [
    {
        "id": "MED-MARCH-HEMORRAGIA",
        "category": "MEDICINA_TRAUMA",
        "title": "Protocolo MARCH: Control de Hemorragia Masiva (M)",
        "priority": "CRITICO_VITAL",
        "keywords": ["hemorragia", "sangrado", "torniquete", "arterial", "herida", "march", "corte", "torniquete improvisado"],
        "summary": "Pasos obligatorios para detener un sangrado arterial o hemorragia exanguinante antes de que cause shock hipovolémico.",
        "steps": [
            "1. RECONOCIMIENTO: Sangre brillante que brota a borbotones (pulsátil) o charco en rápida expansión requiere acción inmediata.",
            "2. PRESIÓN DIRECTA INMEDIATA: Aplicar todo el peso del cuerpo con gasa, apósito o tela limpia sobre el punto exacto de ruptura.",
            "3. TORNIQUETE DE EXTREMIDAD (CAT / SWAT): Colocar 5-7 cm por encima de la herida (NUNCA sobre la articulación/rodilla/codo). Si no se ve el origen exacto, colocarlo lo más proximal posible ('High and Tight').",
            "4. AJUSTE: Girar la varilla (molinete) hasta que el sangrado arterial se detenga por completo y desaparezca el pulso distal.",
            "5. FIJACIÓN Y HORA: Asegurar el molinete en el clip de retención. Escribir la hora exacta de aplicación en la frente o cinta ('T=15:30').",
            "6. TORNIQUETE IMPROVISADO: Usar tira de tela ancha (mínimo 5 cm, nunca cordón fino) + palo o herramienta resistente como molinete, ajustando hasta cortar pulso."
        ],
        "warnings": "NUNCA aflojar un torniquete por cuenta propia una vez aplicado; solo personal médico quirúrgico calificado debe retirarlo."
    },
    {
        "id": "MED-MARCH-VIA-AEREA",
        "category": "MEDICINA_TRAUMA",
        "title": "Protocolo MARCH: Vía Aérea y Posición de Recuperación (A)",
        "priority": "CRITICO_VITAL",
        "keywords": ["via aerea", "asfixia", "ahogo", "inconsciente", "posicion lateral", "lengua", "obstruccion"],
        "summary": "Manejo de la vía aérea en víctimas inconscientes o con obstrucción mecánica.",
        "steps": [
            "1. EVALUAR CONSCIENCIA: Tocar hombros con firmeza y preguntar '¿Me escucha?'.",
            "2. APERTURA DE VÍA AÉREA: Maniobra Frente-Mentón (Head-Tilt Chin-Lift) si no hay trauma espinal sospechado. En trauma de columna, usar Tracción Mandibular (Jaw-Thrust) sin inclinar el cuello.",
            "3. LIMPIEZA: Extraer objetos visibles o vómito con los dedos en gancho.",
            "4. POSICIÓN LATERAL DE SEGURIDAD (Recuperación): Si respira pero está inconsciente, girar a la persona de costado con la pierna superior flexionada a 90° y la mano bajo la mejilla para evitar broncoaspiración."
        ],
        "warnings": "No realizar compresiones abdominales (Heimlich) en personas inconscientes; si cae inconsciente por atragantamiento, iniciar RCP."
    },
    {
        "id": "AGUA-DESINFECCION-HERVIDO",
        "category": "AGUA_Y_SANEAMIENTO",
        "title": "Purificación de Agua por Ebullición",
        "priority": "ALTA",
        "keywords": ["agua", "hervir", "ebullicion", "potabilizar", "desinfectar", "bacterias", "parasitos"],
        "summary": "Método más seguro y confiable para neutralizar patógenos biológicos (virus, bacterias y quistes de Giardia/Cryptosporidium).",
        "steps": [
            "1. PRE-FILTRADO: Si el agua está turbia, pasarla previamente por un paño, tela de algodón o filtro de café para remover sedimentos.",
            "2. EBULLICIÓN FRANCA: Calentar hasta ebullición viva (burbujas vigorosas y constantes).",
            "3. TIEMPO: Mantener hirviendo a borbotones durante 1 MINUTO COMPLETO a nivel del mar (o 3 MINUTOS si se encuentra a más de 2.000 metros de altitud).",
            "4. ENFRIADO: Dejar enfriar tapada en un recipiente limpio y desinfectado para evitar recontaminación.",
            "5. OXIGENACIÓN: Para quitar el sabor 'plano' del agua hervida, verterla de un contenedor limpio a otro varias veces."
        ],
        "warnings": "Hervir no elimina metales pesados, sales, pesticidas ni químicos industriales; solo mata patógenos biológicos."
    },
    {
        "id": "AGUA-DESINFECCION-CLORO",
        "category": "AGUA_Y_SANEAMIENTO",
        "title": "Desinfección Química con Cloro Doméstico",
        "priority": "ALTA",
        "keywords": ["cloro", "lejia", "lavandina", "gotas de cloro", "potabilizar con cloro", "hipoclorito"],
        "summary": "Dosificación exacta de hipoclorito de sodio sin aditivos ni perfumes para consumo humano seguro.",
        "steps": [
            "1. VERIFICAR COMPOSICIÓN: Usar cloro doméstico tradicional sin perfume, sin jabón y sin colorantes (hipoclorito de sodio al 5% - 6%).",
            "2. AGUA CLARA: Agregar 2 GOTAS de cloro por cada 1 LITRO de agua (o 1/8 de cucharadita por cada 4 litros).",
            "3. AGUA TURBIA O FRÍA: Duplicar la dosis a 4 GOTAS por cada 1 LITRO de agua.",
            "4. TIEMPO DE CONTACTO: Mezclar vigorosamente y DEJAR REPOSAR DURANTE 30 MINUTOS obligatoriamente.",
            "5. VERIFICACIÓN: El agua debe tener un ligero olor a cloro residual. Si no huele nada a cloro, repetir la dosis y esperar otros 15 minutos."
        ],
        "warnings": "NUNCA usar productos con aromatizantes, espesantes o cloro en polvo de piscina para consumo directo sin kit dosificador."
    },
    {
        "id": "DISAST-TERREMOTO-CHILE",
        "category": "DESASTRES_Y_REFUGIO",
        "title": "Protocolo Ante Terremoto Mayor (Grado 8+)",
        "priority": "CRITICO_VITAL",
        "keywords": ["terremoto", "sismo", "temblor", "agacharse", "chile", "fuga de gas", "triangulo de la vida"],
        "summary": "Acciones inmediatas comprobadas científicamente durante y después de un megaterremoto.",
        "steps": [
            "1. DURANTE EL SISMO: AGACHARSE, CUBRIRSE debajo de una mesa o mueble firme, y AFIRMARSE de la estructura (Drop, Cover, Hold On). Mantenerse alejado de ventanas y muros perimetrales de ladrillo.",
            "2. NO SALIR CORRIENDO: La mayor cantidad de muertes en Chile ocurren por desprendimiento de vidrios, mampostería y cornisas al intentar salir a la calle.",
            "3. CORTE INMEDIATO TRAS EL SISMO: Cerrar llave de paso general de GAS y bajar el automático general de ELECTRICIDAD antes de evaluar daños estructurales.",
            "4. EVALUACIÓN DE AGUA: Si hay agua de red, llenar inmediatamente bañeras, baldes y botellas limpias antes de que caiga la presión de matrices urbanas.",
            "5. COMUNICACIONES: Priorizar mensajes de texto (SMS) o datos de mensajería; no saturar llamadas de voz convencionales de red móvil."
        ],
        "warnings": "El 'triángulo de la vida' es un mito desacreditado en ingeniería sísmica moderna; la caída de objetos no estructurales es la causa número 1 de traumatismos craneales."
    },
    {
        "id": "DISAST-TSUNAMI-CHILE",
        "category": "DESASTRES_Y_REFUGIO",
        "title": "Protocolo de Evacuación de Tsunami (Zona Costera)",
        "priority": "CRITICO_VITAL",
        "keywords": ["tsunami", "maremoto", "costa", "evacuacion", "cota 30", "senapred", "ola"],
        "summary": "Evacuación inmediata en zonas costeras ante sismos que dificultan permanecer en pie.",
        "steps": [
            "1. CONDICIÓN DE AUTO-EVACUACIÓN: Si un sismo le impide mantenerse en pie o dura más de 1 minuto, NO ESPERE ALERTA SONORA NI MENSAJE SAE; evacúe de inmediato.",
            "2. DIRECCIÓN: Dirigirse a pie (nunca en automóvil para evitar embotellamientos mortales) hacia zonas de seguridad sobre la COTA 30 (30 metros de altura sobre el nivel del mar).",
            "3. RUTA: Utilizar las vías de evacuación señalizadas por SENAPRED hacia cerros o sectores altos.",
            "4. PERMANENCIA: El tsunami no es una sola ola; son múltiples trenes de olas destructivas separadas por horas. No descender hasta que la autoridad oficial (SHOA / SENAPRED) cancele formalmente el estado de alarma."
        ],
        "warnings": "El recogimiento del mar es señal inminente de llegada de la primera cresta; no pierda tiempo filmando o rescatando pertenencias."
    },
    {
        "id": "ENERGIA-SOLAR-BATERIAS",
        "category": "ENERGIA_Y_COMUNICACIONES",
        "title": "Gestión Táctica de Baterías y Paneles Solares Off-Grid",
        "priority": "MEDIA",
        "keywords": ["solar", "bateria", "inversor", "voltaje", "12v", "litio", "lifepo4", "plomo", "blackout"],
        "summary": "Monitoreo de estado de carga (SoC) y umbrales de descarga para preservar energía de comunicaciones.",
        "steps": [
            "1. LÍMITES BATERÍAS PLOMO/AGM (12V): No descargar por debajo del 50% (12.06V en reposo). Descargar a 11.5V causa daño irreversible y sulfatación.",
            "2. LÍMITES LITIO LiFePO4 (12V): Soporta descarga segura hasta el 10-15% (12.8V - 12.5V en reposo). Entrega potencia estable casi constante.",
            "3. ORIENTACIÓN SOLAR EN CHILE: Paneles orientados hacia el NORTE verdadero. Ángulo de inclinación óptimo en invierno = Latitud + 15° (Santiago ~48°); verano = Latitud - 15° (~18°).",
            "4. AHORRO EN CONSUMOS CRÍTICOS: Los inversores 12V a 220V consumen entre 15W y 30W solo en mantenerse encendidos (eficiencia 85%). Conectar radios y cargadores directamente a 12V DC siempre que sea posible."
        ],
        "warnings": "Bajo ningún concepto cortocircuitar celdas de litio ni cargar baterías de plomo en espacios sellados sin ventilación (emisión de gas hidrógeno explosivo)."
    }
]


def query_vault(query: str, category: str = None) -> List[Dict]:
    """Búsqueda rápida por palabras clave y puntuación en el baúl de supervivencia."""
    q_tokens = set(query.lower().split())
    scored = []
    
    for item in SURVIVAL_VAULT:
        if category and item["category"] != category:
            continue
            
        score = 0
        keywords = [k.lower() for k in item["keywords"]]
        title_lower = item["title"].lower()
        
        for tok in q_tokens:
            if tok in title_lower:
                score += 5
            for kw in keywords:
                if tok in kw:
                    score += 3
            if tok in item["summary"].lower():
                score += 1
                
        if score > 0:
            scored.append((score, item))
            
    scored.sort(key=lambda x: x[0], reverse=True)
    return [item for score, item in scored]
