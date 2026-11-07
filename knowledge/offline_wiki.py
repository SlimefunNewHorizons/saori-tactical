"""
SAORI TACTICAL - Offline Construction & Emergency Engineering Wiki
Inspirado en Project N.O.M.A.D., Appropedia y manuales técnicos de campo (CD3WD / Field Engineering).
Planos y guías paso a paso para construir herramientas, filtros, antenas y refugios 100% offline.
"""

from typing import List, Dict

OFFLINE_WIKI_ENTRIES: List[Dict] = [
    {
        "id": "WIKI-ANTENA-SLIMJIM",
        "category": "CONSTRUCCION_TELECOM",
        "title": "Construcción de Antena Slim-Jim VHF 2m (146 MHz) con Cable Coaxial",
        "summary": "Antena omnidireccional de polarización vertical y bajo ángulo de radiación. Triplica el alcance de un radio portátil (Baofeng/Yaesu) de 3 km a más de 25 km.",
        "materials": [
            "Línea paralela bifilar de 300 o 450 ohms (o cable coaxial RG-58 pelado)",
            "Conector PL-259 o BNC macho",
            "Tubo de PVC de 1 pulgada para protección contra lluvia",
            "Cuerda de paracaídas (paracord) para izarla a un árbol",
            "Soldador de estaño o conectores mecánicos"
        ],
        "blueprints_steps": [
            "1. CÁLCULO DE LONGITUD: A 146.500 MHz, la longitud total es de 147 cm (3/4 de onda).",
            "2. CORTE SUPERIOR: Unir ambos conductores en el extremo superior mediante soldadura.",
            "3. VENTANA DE AJUSTE (GAP): A 49 cm desde la parte inferior, cortar una brecha de 2.5 cm en uno de los conductores (dejar el otro continuo).",
            "4. PUNTO DE ALIMENTACIÓN: Soldar el vivo del cable coaxial al lado largo a 10 cm del fondo, y la malla al lado corto.",
            "5. IZADO TÁCTICO: Introducir dentro del tubo de PVC y colgar lo más alto posible en una rama despejada."
        ],
        "engineering_notes": "El bajo ángulo de radiación concentra toda la señal hacia el horizonte en lugar de perder potencia hacia las nubes."
    },
    {
        "id": "WIKI-ANTENA-YAGI-3E",
        "category": "CONSTRUCCION_TELECOM",
        "title": "Construcción de Antena Yagi Direccional de 3 Elementos VHF (144-148 MHz)",
        "summary": "Antena de haz direccional con ganancia de +7 dBi. Permite enlazar con repetidoras o bases a más de 50 km apuntando hacia el objetivo.",
        "materials": [
            "Listón de madera o tubo de PVC de 1 metro (Boom central)",
            "3 varillas de aluminio, alambre de cobre grueso o cinta métrica metálica de carpintero",
            "Cable coaxial RG-58 de 50 ohms"
        ],
        "blueprints_steps": [
            "1. REFLECTOR (Atrás): Longitud 103 cm. Montar en el extremo trasero del boom (posición 0 cm).",
            "2. DIPOLO RADIADOR (Centro): Longitud total 98 cm (dos mitades de 48 cm con 2 cm de espacio en el centro). Montar a 41 cm del reflector.",
            "3. DIRECTOR (Frente): Longitud 92 cm. Montar a 35 cm por delante del radiador (posición 76 cm del boom).",
            "4. CONEXIÓN: Conectar el conductor central del coaxial a una mitad del radiador y la malla a la otra mitad.",
            "5. OPERACIÓN: Apuntar el extremo del director directamente hacia la estación o repetidora lejana."
        ],
        "engineering_notes": "Si se usan segmentos de cinta métrica metálica, los elementos se pueden enrollar facilitando el transporte en mochila de emergencia."
    },
    {
        "id": "WIKI-FILTRO-BIOARENA",
        "category": "AGUA_Y_SANEAMIENTO",
        "title": "Filtro Lento de Bio-Arena y Carbón Activado Casero",
        "summary": "Sistema de purificación mecánica y bacteriológica capaz de filtrar hasta 20 litros de agua por día removiendo sedimentos, protozoos y toxinas.",
        "materials": [
            "Tubo de PVC de 110 mm o balde plástico de 20 litros limpio",
            "Grava pequeña limpia (fondo de drenaje)",
            "Arena gruesa lavada (capa media)",
            "Carbón vegetal triturado (no briquetas químicas de asado)",
            "Arena fina de río o cuarzo muy lavada (capa superior biológica)",
            "Tela de algodón o gasa en la salida"
        ],
        "blueprints_steps": [
            "1. BASE: Perforar orificio de drenaje en el fondo del balde e insertar tela o malla fina para retener material.",
            "2. CAPA 1 (DRENAJE): Colocar 5 cm de grava limpia de 5-10 mm.",
            "3. CAPA 2 (ADSORCIÓN): Colocar 8 cm de carbón vegetal triturado en trozos pequeños de 2-3 mm para absorber pesticidas, químicos y malos olores.",
            "4. CAPA 3 (FILTRACIÓN MEDIA): Colocar 5 cm de arena gruesa.",
            "5. CAPA 4 (FILTRACIÓN FINA): Colocar 15-20 cm de arena fina lavada en la parte superior.",
            "6. DIFUSOR: Colocar una tapa con agujeros en la parte superior para que el agua caiga como llovizna sin destruir la capa superficial de arena fina."
        ],
        "engineering_notes": "El filtro requiere 1 a 2 semanas de uso constante para que se forme la biocapa superior (Schmutzdecke) que neutraliza virus y bacterias; antes de eso, el agua filtrada debe hervirse."
    },
    {
        "id": "WIKI-BANCO-12V-OFFGRID",
        "category": "ENERGIA_Y_COMUNICACIONES",
        "title": "Instalación de Banco de Baterías 12V con Inversor y Fusibles de Protección",
        "summary": "Esquema seguro para alimentar iluminación LED, transceptores de radio y laptops durante blackouts prolongados.",
        "materials": [
            "Batería de ciclo profundo (AGM o LiFePO4 de 12V)",
            "Fusible ANL o automotriz de 30A a 60A cerca del borne positivo",
            "Cable de cobre de 6 AWG o 10 mm²",
            "Inversor de onda pura 12V a 220V (300W a 600W)",
            "Regulador solar PWM o MPPT si hay panel disponible"
        ],
        "blueprints_steps": [
            "1. UBICACIÓN: Batería sobre superficie nivelada y ventilada. NUNCA en dormitorios cerrados si es de plomo/ácido.",
            "2. PROTECCIÓN POR FUSIBLE: Instalar el portafusible a no más de 15 cm del borne POSITIVO (+) de la batería.",
            "3. CONEXIÓN INVERSOR: Conectar primero POSITIVO (+ rojo) al inversor y luego NEGATIVO (- negro). Puede haber una pequeña chispa inocua al cargar los condensadores.",
            "4. CARGAS DIRECTAS DC: Conectar radios y cargadores de teléfono a tomas de 12V DC (mechero de auto o puertos USB de 12V); el inversor desperdicia hasta un 15-20% de energía por calor en reposo.",
            "5. CONTROL DE DESCARGA: Detener el consumo si el voltaje en reposo baja de 12.0V (Plomo) o 12.5V (LiFePO4)."
        ],
        "engineering_notes": "100 Ah a 12V entregan 1.2 kWh teóricos. Con LiFePO4 rinden ~1.0 kWh útiles; suficiente para mantener un transceptor de radio y laptop encendidos por 2 días completos."
    },
    {
        "id": "WIKI-DESTILADOR-SOLAR",
        "category": "AGUA_Y_SANEAMIENTO",
        "title": "Construcción de Destilador Solar de Tierra / Agua Salada",
        "summary": "Aparato solar pasivo que evapora y condensa agua pura al 100% a partir de tierra húmeda, follaje o agua de mar.",
        "materials": [
            "Lámina de plástico transparente de 2 x 2 metros (polietileno)",
            "Recipiente colector central (taza, olla o botella cortada)",
            "Piedra pequeña o peso central",
            "Tubo flexible para beber sin desarmar la estructura (opcional)"
        ],
        "blueprints_steps": [
            "1. EXCAVACIÓN: Cavar un hoyo cónico de 1 metro de diámetro y 50 cm de profundidad en terreno expuesto al sol.",
            "2. MATERIA PRIMA: Colocar vegetación verde fresca no venenosa o verter agua salada/sucia en el fondo del foso (sin tocar el colector central).",
            "3. COLECTOR: Ubicar el vaso limpio en el centro exacto del fondo del hoyo.",
            "4. SELLADO: Extender el plástico transparente sobre el hoyo, sellando los bordes perimetrales con tierra y piedras para evitar fugas de vapor.",
            "5. PUNTO DE CONDENSACIÓN: Colocar una piedra pequeña en el centro del plástico, justo sobre el vaso, creando un cono invertido hacia abajo.",
            "6. FUNCIONAMIENTO: El calor solar evapora el agua, que se condensa en la cara inferior del plástico frío y gotea por gravedad directo al vaso."
        ],
        "engineering_notes": "Rinde entre 0.5 y 1.5 litros por día según la radiación solar y la humedad del terreno."
    },
    {
        "id": "WIKI-REFUGIO-AFRAME",
        "category": "DESASTRES_Y_REFUGIO",
        "title": "Construcción de Refugio Térmico A-Frame (Trinchera Aislada)",
        "summary": "Refugio de emergencia para condiciones de frío extremo e intemperie. Retiene el calor corporal mediante aislamiento por capas de aire atrapado.",
        "materials": [
            "1 tronco largo y resistente de 3 a 4 metros (viga cumbrera)",
            "Ramas gruesas de soporte",
            "Manto espeso de hojas secas, ramas de pino o helechos (mínimo 60 cm de espesor)"
        ],
        "blueprints_steps": [
            "1. VIGA PRINCIPAL: Apoyar un extremo del tronco de 3m en la horqueta de un árbol o soporte de 1 metro de alto, apoyando el otro extremo en el suelo.",
            "2. COSTILLAS: Apoyar ramas a 45 grados a ambos lados de la viga para formar una estructura en 'A' ajustada al tamaño del cuerpo.",
            "3. LECHO AISLANTE DEL SUELO: Llenar el suelo interior con 30 cm de hojas secas o ramas esponjosas. NUNCA dormir directamente sobre la tierra (conduce el frío 20 veces más rápido que el aire).",
            "4. CUBIERTA TÉRMICA: Colocar una capa masiva de ramas pequeñas y cubrirla con mínimo 60 cm a 1 metro de hojas secas, tierra o nieve exterior.",
            "5. PUERTA PEQUEÑA: Bloquear la entrada con la mochila o un tapón de ramas para retener el aire tibio interior."
        ],
        "engineering_notes": "El aislamiento no lo dan las hojas sino el aire inmóvil atrapado entre ellas. Un refugio bien hecho mantiene +10°C en el interior con 0°C en el exterior solo con el calor del cuerpo."
    },
    {
        "id": "WIKI-ENERGIA-AUTO-12V-220V",
        "category": "ENERGIA_Y_COMUNICACIONES",
        "title": "Generación de 220V AC con Alternador de Automóvil (Ej: Kia Morning 2014)",
        "summary": "Uso del motor del auto en ralentí como generador eléctrico continuo de 220V AC con inversor directo a bornes. Entrega de 500W a 600W útiles continuos.",
        "materials": [
            "Automóvil (Ej: Kia Morning 2014 con estanque de 35L)",
            "Inversor de Corriente 12V DC a 220V AC (500W a 1000W Onda Pura / Pure Sine Wave)",
            "Cables con pinzas tipo caimán de batería de alta presión (mínimo 6 AWG / 16 mm²)",
            "Alargador eléctrico convencional de 220V con zapatilla de enchufes",
            "Cinta aisladora o manguera plástica para empalmes de emergencia"
        ],
        "blueprints_steps": [
            "1. CONCEPTO: ¿DE DÓNDE SALE LA ENERGÍA? El alternador del auto está conectado directamente por cables gruesos de fábrica a los bornes de la batería. No existe un enchufe aparte para el alternador: al conectar las pinzas a los bornes (+) y (-) de la batería con el motor encendido, estás extrayendo directamente la energía que el alternador genera en tiempo real.",
            "2. CAPACIDAD DEL KIA MORNING 2014: Su alternador de fábrica entrega 70 Amperios (70A) a 14V = 980W brutos. El vehículo consume ~250W para su propia inyección y bujías. Te quedan entre 500W y 600W NETOS continuos (suficiente para PC de escritorio RTX 4060, router, luces LED y recarga de celulares).",
            "3. ¿DÓNDE SE COLOCAN LAS PINZAS? El inversor tiene dos cables: Pinza ROJA al borne POSITIVO (+) de la batería del auto; Pinza NEGRA al borne NEGATIVO (-) de la batería. El inversor es el 'adaptador' intermedio: recibe los 12V DC del auto y los transforma internamente a 220V AC en sus enchufes hembra.",
            "4. SECUENCIA DE ENCENDIDO: (a) Conectar pinzas con el inversor apagado. (b) Arrancar el motor del Kia Morning y dejarlo en ralentí (700-900 RPM al aire libre). (c) Encender el interruptor del inversor. (d) Conectar el enchufe del computador o alargador a la toma de 220V del inversor.",
            "5. AUTONOMÍA DE COMBUSTIBLE: El motor 1.0L/1.2L del Kia Morning al ralentí gasta aprox. 0.6 litros de bencina por hora. Con el estanque lleno de 35 litros, tienes hasta 58 HORAS CONTINUAS de electricidad (más de 2 días seguidos)."
        ],
        "engineering_notes": "NUNCA usar el enchufe del encendedor de cigarrillos interior para más de 120W porque se quema el fusible. Las pinzas SIEMPRE van al compartimento del motor directo a los bornes de la batería."
    },
    {
        "id": "WIKI-INYECCION-CASA-LUCES",
        "category": "ENERGIA_Y_COMUNICACIONES",
        "title": "Inyección de Energía a la Red de la Casa para Encender Luces (Protocolo Seguro)",
        "summary": "Método para energizar los circuitos de iluminación del hogar desde el inversor del auto sin quemar equipos ni electrocutar a técnicos de la red pública.",
        "materials": [
            "Inversor 12V a 220V conectado al auto",
            "Cable de inyección con enchufe macho de 220V (o cable conectado directo a la salida de un automático de luces)",
            "Acceso al Tablero Eléctrico General de la vivienda"
        ],
        "blueprints_steps": [
            "1. REGLA DE ORO OBLIGATORIA (AISLAMIENTO TOTAL): Ir al tablero eléctrico general y BAJAR EL AUTOMÁTICO GENERAL (Disyuntor principal de la compañía eléctrica y diferencial). Si no se baja, la corriente del auto saldrá hacia los postes de la calle pudiendo electrocutar mortalmente a los linieros que reparan las líneas caídas, y cuando vuelva la luz de la calle, tu inversor EXPLOTARÁ en llamas al chocar las dos fases.",
            "2. APAGAR CIRCUITOS DE FUERZA: Bajar los automáticos de enchufes de alto consumo (horno, hervidor, lavadora, secadora, estufas eléctricas). El alternador del Kia Morning no soporta electrodomésticos de calor (1500W-2000W).",
            "3. DEJAR ARRIBA SOLO EL CIRCUITO DE ILUMINACIÓN: Mantener arriba únicamente el disyuntor pequeño (generalmente de 6A o 10A) etiquetado como 'ALUMBRADO' o 'LUCES'.",
            "4. CONEXIÓN DEL INVERSOR AL CIRCUITO: Conectar un alargador desde la salida de 220V del inversor del auto hacia un enchufe de la casa perteneciente al circuito que se desea energizar. Con ampolletas LED (que consumen solo 7W a 9W cada una), encender 10 ampolletas en toda la casa consume apenas 80 Watts, trabajando el auto totalmente descansado.",
            "5. RESTABLECIMIENTO DE RED PÚBLICA: Cuando regrese la luz a los vecinos, ANTES de subir el automático general de la calle: (a) Desconectar el inversor del auto por completo, (b) Subir el automático general."
        ],
        "engineering_notes": "La forma profesional y permanente de hacer esto es instalar un Conmutador de Transferencia Manual (Transfer Switch 1-0-2) en el tablero eléctrico, el cual físicamente imposibilita que la red pública y el auto se toquen jamás."
    },
    {
        "id": "WIKI-ROUTER-12V-DIRECTO",
        "category": "ENERGIA_Y_COMUNICACIONES",
        "title": "Alimentación Directa de Routers / ONT de Fibra a Batería 12V DC (Zero-Inverter)",
        "summary": "Conexión de routers Wi-Fi directamente a baterías de 12V sin pasar por inversor de 220V, eliminando un 25% de pérdida por calor y ruido eléctrico.",
        "materials": [
            "Batería de 12V (auto, moto o alarma/UPS de gel)",
            "Cable con conector macho Jack barril DC 5.5mm x 2.1mm (el estándar del 95% de los routers de Chile)",
            "Portafusible aéreo con fusible automotriz de 2A o 3A",
            "Multímetro o voltímetro digital"
        ],
        "blueprints_steps": [
            "1. VERIFICACIÓN DE VOLTAJE: Revisar la etiqueta trasera del router (VTR, Movistar, Entel, Claro, etc.). Debe indicar: 'Input: 12V DC === 1.0A' (o 1.5A / 2.0A).",
            "2. VERIFICACIÓN DE POLARIDAD: Verificar el diagrama de polaridad en la etiqueta: el símbolo muestra un círculo exterior (-) y un punto central (+), que es el estándar positivo al centro.",
            "3. CONFECCIÓN DEL CABLE: Cortar el cable del transformador original que va al enchufe. El cable con línea blanca, rayas o texto suele ser el POSITIVO (+). Verificar continuidad con multímetro.",
            "4. FUSIBLE DE PROTECCIÓN: Intercalar un fusible de 2A en el cable positivo cerca del borne de la batería.",
            "5. CONEXIÓN: Conectar positivo (+) y negativo (-) a la batería. El router encenderá inmediatamente emitiendo señal Wi-Fi local aunque no haya luz en el vecindario."
        ],
        "engineering_notes": "Al saltarse la conversión 12V -> 220V -> 12V, un router de 12W dura más de 5 días seguidos conectado a una batería de auto común de 60Ah sin necesidad de recargarla."
    },
    {
        "id": "WIKI-PANEL-SOLAR-EMERGENCIA",
        "category": "ENERGIA_Y_COMUNICACIONES",
        "title": "Uso Rústico de Paneles Solares sin Regulador Comercial (Diodo Schottky)",
        "summary": "Esquema para cargar baterías de 12V y celulares con paneles solares recuperados en caso de no contar con controlador PWM o MPPT.",
        "materials": [
            "Panel solar de 12V o 24V (Voc entre 18V y 22V)",
            "Diodo de potencia Schottky de 10A a 15A (o diodo rectificador de fuente de PC rota)",
            "Multímetro para control de tensión",
            "Batería de 12V"
        ],
        "blueprints_steps": [
            "1. IDENTIFICACIÓN DEL PANEL: En la caja trasera, medir con multímetro al sol el voltaje de circuito abierto (Voc) entre terminales (+) y (-).",
            "2. INSTALACIÓN DE DIODO DE BLOQUEO: Soldar o empalmar el diodo Schottky en serie en el cable POSITIVO del panel, con el cátodo (la banda plateada) apuntando hacia la batería. Esto permite que la corriente fluya hacia la batería de día, pero IMPIDE que la batería se descargue hacia el panel de noche.",
            "3. CONEXIÓN A BATERÍA: Conectar el panel al borne positivo (después del diodo) y el negativo directo.",
            "4. MONITOREO MANUAL: Sin regulador, el panel continuará empujando corriente. Medir con multímetro periódicamente: si la batería llega a 14.4V (plomo-ácido), DESCONECTAR el panel manualmente para evitar que el electrolito hierva y emita gas hidrógeno inflamable.",
            "5. CARGA DE CELULARES: Para cargar teléfonos celulares (5V USB) directo desde el panel sin batería, se puede usar el adaptador de encendedor de auto de 12V a 5V conectado a las salidas del panel (soportan hasta 24V de entrada)."
        ],
        "engineering_notes": "Un diodo Schottky tiene una caída de voltaje de solo 0.3V a 0.4V (frente a 0.7V de un diodo de silicio común), desperdiciando menos energía solar en forma de calor."
    },
    {
        "id": "WIKI-BANOS-SECOS-SANITARIOS",
        "category": "AGUA_Y_SANEAMIENTO",
        "title": "Sanidad y Baño Seco de Emergencia (Twin-Bucket System)",
        "summary": "Sistema de dos baldes para evitar colapso biológico, cólera y malos olores en viviendas durante cortes de agua potable o destrucción de cañerías.",
        "materials": [
            "2 baldes plásticos de 20 litros (con tapa o asiento improvisado)",
            "Bolsas de basura resistentes de 50 litros",
            "Aserrín de madera seco, tierra de jardín seca, ceniza de estufa/fogata o cal apagada",
            "Carbón vegetal molido en trozos pequeños"
        ],
        "blueprints_steps": [
            "1. REGLA FUNDAMENTAL DE HIGIENE: NUNCA tirar la cadena con agua limpia del estanque en un terremoto si las cañerías pueden estar rotas o el colector colapsado (inunda los pisos bajos de heces).",
            "2. SEPARACIÓN EN ORIGEN (DOS BALDES): BALDE 1 (LÍQUIDOS / ORINA): La orina es 100% estéril al salir y NO genera olor fétido si no entra en contacto con bacterias fecales; se vacía en tierra diluida con agua 1:5. BALDE 2 (SÓLIDOS / HECES): Forrado con bolsa de basura resistente; usar exclusivamente para defecar y depositar papel higiénico.",
            "3. TÉCNICA DE COBERTURA ANTI-OLOR (BIO-TAPA): Inmediatamente después de defecar, cubrir la deposición con dos tazas generosas de la mezcla seca (50% aserrín o tierra seca + 50% ceniza o carbón molido).",
            "4. CONTROL QUÍMICO Y BACTERIANO: El carbón y la ceniza vegetal absorben el sulfuro de hidrógeno y el amoníaco por adsorción porosa, y la alcalinidad de la ceniza inhibe la reproducción de bacterias anaeróbicas y moscas, eliminando el 95% del mal olor.",
            "5. CIERRE Y DISPOSICIÓN: Cuando el balde de sólidos alcance 2/3 de su capacidad, cerrar la bolsa con nudo firme y enterrar en foso a mínimo 50 cm de profundidad y a más de 30 metros de cualquier pozo o curso de agua."
        ],
        "engineering_notes": "En el terremoto de Christchurch (2011), este protocolo de dos baldes evitó epidemias gastrointestinales en más de 50.000 hogares durante meses sin alcantarillado."
    },
    {
        "id": "WIKI-ANTENA-CHATARRA-ZINC",
        "category": "CONSTRUCCION_TELECOM",
        "title": "Construcción de Antenas con Chatarra de Zinc, Aluminio y Parábolas de TV",
        "summary": "Fabricación de dipolos de emergencia y reflectores de esquina directivos de alta ganancia (+10 a +12 dBi) a partir de escombros metálicos y planchas de techumbre.",
        "materials": [
            "Plancha de zinc acanalado (calamina) o plancha metálica de 1x1 m",
            "Alambre de cobre grueso o tubos de aluminio de antena vieja",
            "Cable coaxial de TV (RG-6 de 75 ohms o RG-58 de 50 ohms)",
            "Conector o empalme directo al transceptor de radio"
        ],
        "blueprints_steps": [
            "1. DIPOLO DE MEDIA ONDA: Cortar dos varillas de alambre o tubos de aluminio con la fórmula: Longitud de cada brazo = 71.25 / Frecuencia (MHz). Para 146 MHz (VHF), cada brazo mide 49 cm.",
            "2. REFLECTOR DE ESQUINA CON PLANCHA DE ZINC: Doblar una plancha de zinc en ángulo de 90° formando una 'V'. Montar el dipolo en el vértice interior de la 'V', separado a 30 cm de la pared metálica.",
            "3. GANANCIA Y DIRECTIVIDAD: La plancha de zinc actúa como un espejo reflector parabólico plano. Toda la señal que antes se dispersaba hacia atrás se proyecta hacia el frente, otorgando una ganancia de +10 dB a +12 dB (multiplica la potencia efectiva por 10 a 15 veces).",
            "4. REUTILIZACIÓN DE PARÁBOLA SATELITAL (DIRECTV / ENTEL): Retirar el LNB del soporte central de la antena parabólica. Colocar la antena de un radio portátil (Baofeng) o un dipolo de 2.4 GHz en el punto focal exacto apuntando hacia la parábola. Permite enlaces Wi-Fi o radio VHF/UHF a más de 10 kilómetros apuntando hacia la cima del cerro o repetidora."
        ],
        "engineering_notes": "La polarización debe coincidir con la de la estación receptora: si es radio VHF/UHF o repetidora, el dipolo debe montarse en posición VERTICAL."
    },
    {
        "id": "WIKI-RED-CYBERPUNK-MESH-LOCAL",
        "category": "ENERGIA_Y_COMUNICACIONES",
        "title": "Arquitectura de Red Mesh Cyberpunk P2P (Blackwall Citadel Off-Grid)",
        "summary": "Creación de una red local autosuficiente punto a punto (P2P) y malla sin router ni internet entre PC RTX 4060, Laptop Nova, Poco X3 Pro, Poco X8 Pro y Galaxy Tab S6 Lite.",
        "materials": [
            "Dispositivos Wi-Fi del usuario (Laptop Nova, Poco X3 Pro, Poco X8 Pro, Tab S6 Lite, PC RTX 4060)",
            "Software P2P abierto: Reticulum Network Stack (RNS), Briar, Syncthing, Kiwix, OsmAnd",
            "Hardware opcional de expansión: Módulos ESP32 LoRa 915MHz (Meshtastic) o Baofeng UV-5R con cable APRS-K1"
        ],
        "blueprints_steps": [
            "1. CONCEPTO CYBERPUNK (EL MURO NEGRO / BLACKWALL): En el colapso de la red global, la supervivencia digital se basa en 'Citadelas' locales: redes autónomas cerradas donde cada dispositivo actúa como nodo emisor, repetidor y receptor sin depender de proveedores de internet (ISP) ni servidores centrales.",
            "2. NODO CENTRAL DE DATOS (CITADEL VAULT): PC local con RTX 4060 corriendo SAORI Tactical, Ollama y el Dashboard Web (:8090). Emite la red Wi-Fi 'SAORI-CITADEL' mediante el Punto de acceso móvil de Windows (Hotspot) o router de 12V.",
            "3. NODO REPETIDOR DE FRONTERA (LAPTOP NOVA): Ubicar la laptop Nova en un punto alto (segundo piso, balcón o ventana alta). Conectada por Wi-Fi o cable Ethernet al PC central, Nova repite la señal Wi-Fi hacia el exterior mediante puente de red (Network Bridging) o un segundo adaptador Wi-Fi USB, extendiendo la cobertura a 150-300 metros a la redonda.",
            "4. NODOS SCOUT DE PATRULLA (POCO X3 PRO Y POCO X8 PRO): Llevan instaladas aplicaciones P2P como Briar (mensajería encriptada por Wi-Fi local y Bluetooth Mesh). Si un operador camina fuera del alcance del Wi-Fi de la casa, se activa el protocolo Store-and-Forward (DTN / Sneakernet): los mensajes y reportes se guardan en la memoria flash del teléfono y, al cruzarse con otro teléfono o regresar al radio de la casa, los paquetes se sincronizan de forma invisible.",
            "5. CONSOLA TÁCTIL DE MANDO (GALAXY TAB S6 LITE): Conectada a la red Wi-Fi, muestra el panel web de SAORI, el buzón de reportes de campo (SITREP) y mapas topográficos compartidos, permitiendo apagar el monitor grande del PC para ahorrar 150W de electricidad.",
            "6. PROTOCOLO RETICULUM (RNS / NOMADNET / SIDEBAND): Protocolo de red criptográfico P2P para el apocalipsis. No usa IPs ni DNS; las direcciones son hashes criptográficos. Funciona sobre Wi-Fi, Bluetooth o radio LoRa, enrutando paquetes automáticamente a través de múltiples saltos (multi-hop).",
            "7. SALIR DE LA LIMITACIÓN DEL WI-FI (RADIO DE LARGO ALCANCE 10-50 KM): Para romper el límite de 100m del Wi-Fi convencional de los teléfonos, se acopla un módulo Meshtastic LoRa de 915 MHz ($25) por Bluetooth al Poco X3 Pro o por USB al PC. Con una pequeña antena en el techo, los mensajes de chat P2P viajan a más de 15 km rebotando de cerro a cerro sin red celular."
        ],
        "engineering_notes": "Wi-Fi y Bluetooth no requieren permisos ni licencias. Una red mesh de 4 saltos (PC -> Nova -> Poco X8 -> Poco X3) cubre más de 800 metros lineales en línea visual usando solo los chips de fábrica de tus dispositivos."
    }
]


def _normalize_txt(txt: str) -> str:
    """Normaliza tildes y diacríticos para búsqueda robusta sin importar acentos o eñes."""
    table = str.maketrans("áéíóúÁÉÍÓÚñÑüÜ", "aeiouaeiounnuu")
    return txt.lower().translate(table)


def search_wiki(query: str) -> List[Dict]:
    """Búsqueda de texto en los planos de construcción y guías de ingeniería."""
    q_norm = _normalize_txt(query)
    q_tokens = q_norm.split()
    results = []
    for item in OFFLINE_WIKI_ENTRIES:
        searchable_raw = f"{item['title']} {item['category']} {item['summary']} {' '.join(item['materials'])} {' '.join(item['blueprints_steps'])}"
        searchable = _normalize_txt(searchable_raw)
        title_norm = _normalize_txt(item['title'])
        score = sum(4 for t in q_tokens if t in title_norm) + sum(1 for t in q_tokens if t in searchable)
        if score > 0:
            results.append((score, item))
    results.sort(key=lambda x: x[0], reverse=True)
    return [item for score, item in results]


def format_wiki_card(entry: Dict) -> str:
    """Formatea una entrada de la wiki técnica para lectura en terminal."""
    materials_str = "\n".join([f"  • {m}" for m in entry["materials"]])
    steps_str = "\n".join([f"  {s}" for s in entry["blueprints_steps"]])
    return (
        f"╔════════════════════════════════════════════════════════════════════════════╗\n"
        f"║ 🛠️  {entry['title'].upper()}\n"
        f"╠════════════════════════════════════════════════════════════════════════════╣\n"
        f"  Categoría: {entry['category']}\n"
        f"  Resumen:   {entry['summary']}\n\n"
        f"  MATERIALES REQUERIDOS:\n{materials_str}\n\n"
        f"  PLANOS Y PASOS DE CONSTRUCCIÓN:\n{steps_str}\n\n"
        f"  NOTA DE INGENIERÍA:\n  💡 {entry.get('engineering_notes', 'N/A')}\n"
        f"╚════════════════════════════════════════════════════════════════════════════╝"
    )
