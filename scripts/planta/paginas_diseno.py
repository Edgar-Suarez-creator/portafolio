"""Genera las páginas de diseño de los proyectos P2 a P8 y sincroniza el menú de proyectos de todo el sitio.

Contenido tomado del «Manual de construcción del portafolio — instrucciones por proyecto»: qué hace el sistema,
pasos, datos, métricas con su línea base, demo y criterio de terminado. Las cifras propias quedan «por medir»;
las únicas cifras que aparecen son referencias publicadas que el manual cita, y se marcan como tales.

Uso:  python scripts/planta/paginas_diseno.py
"""
from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECTS = ROOT / "projects"
AUTOR = "Edgar R. Suárez Macías"
PERFIL = ("Planeador e Ingeniero de Sistemas", "Planner and Systems Engineer")
CSS_V = "1791150000"

# (número, archivo, nombre corto es/en)
MENU = [
    ("P1", "01-asistente-planta.html", ("Asistente de planta", "Plant assistant")),
    ("P2", "02-pid-sistemas.html", ("Digitalización de P&ID", "P&ID digitization")),
    ("P3", "03-ordenes-backlog.html", ("Planeación de órdenes y backlog", "Work-order planning and backlog")),
    ("P4", "04-confiabilidad.html", ("Estrategia de confiabilidad", "Reliability strategy")),
    ("P5", "05-materiales.html", ("Materiales y repuestos", "Materials and spares")),
    ("P6", "06-construccion-entrega.html", ("Construcción y entrega por sistemas", "Construction and handover by system")),
    ("P7", "07-calidad.html", ("Calidad en construcción", "Construction quality")),
    ("P8", "08-preservacion.html", ("Preservación de equipos", "Equipment preservation")),
]

PROYECTOS = [
    {
        "num": "P2", "file": "02-pid-sistemas.html",
        "nombre": ("Digitalización de P&ID y definición de sistemas", "P&ID digitization and system definition"),
        "eyebrow": ("Serie planta · del P&ID escaneado al subsistema", "Plant series · from scanned P&ID to subsystem"),
        "one": ("Toma un P&ID escaneado y devuelve el grafo del proceso en formato DEXPI, la lista de tags, una propuesta de límites de subsistema y la lista de aislamientos por equipo.",
                "It takes a scanned P&ID and returns the process graph in DEXPI format, the tag list, a proposal of subsystem boundaries and the isolation list per item."),
        "chips": ["YOLO", "Relationformer", "OCR", "pyDEXPI", ("detección de comunidades", "community detection")],
        "kpi": {"big": ("75,5 %", "75.5 %"), "small": ("mAP de aristas", "edge mAP"),
                "label": ("Referencia publicada · PID2Graph OPEN100", "Published reference · PID2Graph OPEN100"),
                "rows": [("base", ("enfoque modular", "modular approach"), ("45,9 %", "45.9 %")),
                         ("goal", ("Relationformer", "Relationformer"), ("75,5 %", "75.5 %"))],
                "expl": ("Es la cifra que el modelo debe reproducir en planos reales. Un modelo de visión generalista llega a F1 de nodos cercano a 0,96, pero su F1 de aristas ronda 0,03: encuentra los símbolos y pierde las conexiones. Por eso hace falta un modelo especializado.",
                         "This is the figure the model must reproduce on real drawings. A general-purpose vision model reaches a node F1 near 0.96, but its edge F1 is around 0.03: it finds the symbols and loses the connections. That is why a specialized model is needed."),
                "ev": ("Referencia de la literatura, no resultado propio. Las cifras propias se publican al implementar, con su línea base al lado.",
                       "Literature reference, not an own result. Own figures are published once implemented, with their baseline alongside.")},
        "trio": [("Definir sistemas, subsistemas y aislamientos exige recorrer a mano cada P&ID: identificar tags, seguir líneas y decidir dónde cortar. En un plano escaneado no hay datos, solo una imagen.",
                  "Defining systems, subsystems and isolations means walking every P&ID by hand: identifying tags, following lines and deciding where to cut. A scanned drawing has no data, only an image."),
                 ("Un detector de símbolos, la lectura de tags con OCR y un modelo de topología por parches reconstruyen el grafo del plano; el grafo se exporta a DEXPI y los subsistemas se proponen por detección de comunidades, con las válvulas de bloqueo como fronteras.",
                  "A symbol detector, OCR tag reading and a patch-based topology model rebuild the drawing's graph; the graph is exported to DEXPI and subsystems are proposed by community detection, with block valves as boundaries."),
                 ("Visión por computador aplicada a ingeniería: del plano escaneado a datos estructurados que alimentan el comisionamiento, con la lista de tags por subsistema, los aislamientos y la matriz tag → subsistema → ITR.",
                  "Computer vision applied to engineering: from the scanned drawing to structured data that feeds commissioning, with the tag list per subsystem, the isolations and the tag → subsystem → ITR matrix.")],
        "pasos": [(("Preparar los datos", "Prepare the data"),
                   ("Tres conjuntos públicos en un formato común de nodos y aristas: Digitize-PID (500 planos sintéticos, 32 símbolos) para detectar símbolos, SynthPID (665 planos) para afinar la topología y PID2Graph OPEN100 (12 planos reales) reservado solo para la prueba final.",
                    "Three public datasets in a common node-and-edge format: Digitize-PID (500 synthetic drawings, 32 symbols) to detect symbols, SynthPID (665 drawings) to fine-tune topology and PID2Graph OPEN100 (12 real drawings) kept for the final test only.")),
                  (("Detectar símbolos y leer tags", "Detect symbols and read tags"),
                   ("Un detector YOLO entrenado sobre Digitize-PID encuentra los símbolos y se mide por clase; el OCR lee el tag de cada burbuja de instrumento y lo normaliza al formato ISA de la planta.",
                    "A YOLO detector trained on Digitize-PID finds the symbols and is measured per class; OCR reads the tag in each instrument bubble and normalizes it to the plant's ISA format.")),
                  (("Reconstruir la topología", "Rebuild the topology"),
                   ("Relationformer extrae las conexiones por parches, porque a escala de plano completo los símbolos quedan por debajo del tamaño detectable; las predicciones se cosen y se colapsan codos y cruces para quedarse con el grafo físico.",
                    "Relationformer extracts connections patch by patch, because at full-drawing scale the symbols fall below the detectable size; predictions are stitched and elbows and crossings collapsed to keep the physical graph.")),
                  (("Exportar a DEXPI", "Export to DEXPI"),
                   ("El grafo se exporta con pyDEXPI y se verifica que el archivo abre en un visor del estándar.",
                    "The graph is exported with pyDEXPI and the file is checked to open in a viewer of the standard.")),
                  (("Proponer subsistemas y aislamientos", "Propose subsystems and isolations"),
                   ("Detección de comunidades sobre el grafo con las válvulas de bloqueo como fronteras candidatas. Salen la lista de tags por subsistema, los aislamientos por equipo y la matriz de ITR requeridos; la corrección final se hace a mano sobre el plano.",
                    "Community detection on the graph with block valves as candidate boundaries. Out come the tag list per subsystem, the isolations per item and the required ITR matrix; the final correction is made by hand on the drawing."))],
        "metricas": [(("mAP de nodos sobre OPEN100", "Node mAP on OPEN100"), ("detector YOLO solo", "YOLO detector alone"), ("83,6 % con Relationformer", "83.6 % with Relationformer")),
                     (("mAP de aristas sobre OPEN100", "Edge mAP on OPEN100"), ("enfoque modular: detección más trazado de líneas", "modular approach: detection plus line tracing"), ("75,5 % Relationformer · 45,9 % modular", "75.5 % Relationformer · 45.9 % modular")),
                     (("mAP de aristas entrenando solo con sintéticos", "Edge mAP training on synthetic data only"), ("sintéticos de plantilla", "template synthetic data"), ("63,8 % con SynthPID · 33 % con plantilla", "63.8 % with SynthPID · 33 % with templates")),
                     (("Concordancia de subsistemas", "Subsystem agreement"), ("definición manual sobre los mismos planos", "manual definition on the same drawings"), None)],
        "datos": [(("Digitize-PID", "Digitize-PID"), ("público", "public"), ("entrenar la detección de símbolos · 500 planos sintéticos, 32 símbolos", "train symbol detection · 500 synthetic drawings, 32 symbols")),
                  (("SynthPID", "SynthPID"), ("público", "public"), ("afinar la extracción de topología · 665 planos", "fine-tune topology extraction · 665 drawings")),
                  (("PID2Graph OPEN100", "PID2Graph OPEN100"), ("público", "public"), ("evaluación final, nunca entrenamiento · 12 planos reales", "final evaluation, never training · 12 real drawings"))],
        "demo": ("Se carga un plano; se muestra con símbolos y conexiones marcados, el grafo navegable al lado y los subsistemas coloreados, con un botón para descargar el DEXPI.",
                 "A drawing is loaded; it is shown with symbols and connections marked, the navigable graph beside it and the subsystems colored, with a button to download the DEXPI."),
        "terminado": [("El modelo reproduce en OPEN100 un mAP de aristas comparable al publicado.", "The model reproduces on OPEN100 an edge mAP comparable to the published one."),
                      ("El archivo DEXPI valida contra el esquema.", "The DEXPI file validates against the schema."),
                      ("La propuesta de subsistemas se compara con la manual en una tabla de coincidencias y diferencias.", "The subsystem proposal is compared with the manual one in a table of matches and differences.")],
    },
    {
        "num": "P3", "file": "03-ordenes-backlog.html",
        "nombre": ("Agente de planeación de órdenes y control del backlog", "Work-order planning agent and backlog control"),
        "eyebrow": ("Serie planta · del aviso al programa semanal", "Plant series · from notification to weekly schedule"),
        "one": ("Clasifica el aviso en texto libre, arma el paquete de planeación (plan de trabajo, materiales, permisos, aislamientos y horas), construye el programa semanal con un optimizador y publica el tablero de salud del backlog.",
                "It classifies the free-text notification, builds the planning package (work plan, materials, permits, isolations and hours), builds the weekly schedule with an optimizer and publishes the backlog health dashboard."),
        "chips": ["MaintIE", "BERT", "CP-SAT (OR-Tools)", ("órdenes similares", "similar orders"), ("tablero de backlog", "backlog dashboard")],
        "kpi": {"big": ("4", "4"), "small": ("métricas con línea base", "metrics with baseline"),
                "label": ("Lo que se va a medir", "What will be measured"), "rows": [],
                "expl": ("La clasificación de avisos, la búsqueda de órdenes similares, los minutos de planeación por orden y el cumplimiento del programa semanal, cada una contra el método que reemplaza: TF-IDF, palabra clave, planeación manual cronometrada y programación por prioridad.",
                         "Notification classification, similar-order search, planning minutes per order and weekly schedule compliance, each against the method it replaces: TF-IDF, keyword search, timed manual planning and priority-based scheduling."),
                "ev": ("Diseño completo; las cifras se miden al implementar. Nada se emite sin aprobación humana registrada.",
                       "Full design; figures are measured once implemented. Nothing is issued without recorded human approval.")},
        "trio": [("Cada aviso llega en texto libre. El planeador lo clasifica, busca una orden parecida, arma el paquete y lo encaja a mano en el programa semanal, con restricciones de cuadrillas, materiales y ventanas de entrega acordadas con operaciones.",
                  "Each notification arrives as free text. The planner classifies it, looks for a similar order, builds the package and fits it by hand into the weekly schedule, with crew, material and handover-window constraints agreed with operations."),
                 ("Tres clasificadores comparados (TF-IDF con regresión logística, BERT afinado y un LLM con pocos ejemplos), extracción de entidades para llenar la orden, órdenes similares por embeddings, paquete armado con los datos del P1 y del P5, y programa semanal optimizado con CP-SAT.",
                  "Three compared classifiers (TF-IDF with logistic regression, fine-tuned BERT and a few-shot LLM), entity extraction to fill the order, similar orders by embeddings, a package built with data from P1 and P5, and a weekly schedule optimized with CP-SAT."),
                 ("Procesamiento de lenguaje natural y optimización aplicados a la planeación de mantenimiento, con aprobación explícita: el sistema registra quién aprobó permisos y aislamientos, y cuándo.",
                  "Natural language processing and optimization applied to maintenance planning, with explicit approval: the system records who approved permits and isolations, and when.")],
        "pasos": [(("Preparar el conjunto MaintIE", "Prepare the MaintIE dataset"),
                   ("Se carga el esquema de 224 clases finas y 6 gruesas, y se mapean sus clases a la taxonomía ISO 14224 de la planta.",
                    "The schema of 224 fine and 6 coarse classes is loaded and its classes are mapped to the plant's ISO 14224 taxonomy.")),
                  (("Clasificar el aviso", "Classify the notification"),
                   ("Tres clasificadores sobre el mismo conjunto, con partición por entidad: TF-IDF con regresión logística, BERT afinado y un LLM con pocos ejemplos. Se registran F1 por clase, latencia y costo por mil avisos.",
                    "Three classifiers on the same set, split by entity: TF-IDF with logistic regression, fine-tuned BERT and a few-shot LLM. Per-class F1, latency and cost per thousand notifications are recorded.")),
                  (("Llenar la orden y buscar similares", "Fill the order and find similar ones"),
                   ("La extracción de entidades (ítem, problema, acción) llena los campos de la orden sin captura manual; un índice de órdenes similares por embeddings se evalúa con recuperación a 5 contra pares etiquetados a mano.",
                    "Entity extraction (item, problem, action) fills the order fields without manual entry; a similar-order index by embeddings is evaluated with recall at 5 against hand-labeled pairs.")),
                  (("Armar el paquete de planeación", "Build the planning package"),
                   ("Plan de trabajo de la orden similar mejor puntuada, materiales de la lista del equipo, aislamientos del P1 y horas estimadas por la mediana histórica de ese modo de falla.",
                    "Work plan from the best-scored similar order, materials from the equipment list, isolations from P1 and hours estimated from the historical median of that failure mode.")),
                  (("Programar la semana y medir el backlog", "Schedule the week and measure the backlog"),
                   ("CP-SAT asigna técnico, orden y turno con restricciones de habilidad, jornada, prioridad, ventana de entrega y material, y maximiza el valor completado. El tablero muestra semanas de backlog por especialidad, cumplimiento del programa, porcentaje de órdenes reactivas, cumplimiento de preventivos y el Pareto de causas de reprogramación, sobre seis meses simulados.",
                    "CP-SAT assigns technician, order and shift under skill, shift-length, priority, handover-window and material constraints, maximizing completed value. The dashboard shows backlog weeks per craft, schedule compliance, share of reactive orders, preventive compliance and the Pareto of rescheduling causes, over six simulated months."))],
        "metricas": [(("F1 por clase del clasificador", "Classifier per-class F1"), ("TF-IDF con regresión logística", "TF-IDF with logistic regression"), None),
                     (("Recuperación a 5 de órdenes similares", "Recall at 5 of similar orders"), ("búsqueda por palabra clave sobre la descripción", "keyword search on the description"), None),
                     (("Minutos de planeación por orden", "Planning minutes per order"), ("planeación manual cronometrada sobre 20 órdenes", "timed manual planning of 20 orders"), None),
                     (("Cumplimiento del programa semanal", "Weekly schedule compliance"), ("programación por prioridad sin optimizador", "priority scheduling without an optimizer"), None)],
        "datos": [(("MaintIE", "MaintIE"), ("público", "public"), ("entrenar y evaluar el procesamiento de texto de avisos", "train and evaluate notification text processing")),
                  (("Órdenes de la planta de referencia", "Reference-plant orders"), ("sintético", "synthetic"), ("flujo completo del aviso al programa", "full flow from notification to schedule")),
                  (("Ficha y aislamientos del P1", "P1 datasheet and isolations"), ("derivado", "derived"), ("paquete de planeación", "planning package")),
                  (("Disponibilidad de materiales del P5", "P5 material availability"), ("derivado", "derived"), ("restricción de material en el programa", "material constraint in the schedule"))],
        "demo": ("Se escribe un aviso; se ve la clasificación con su confianza, las órdenes similares, el paquete armado y el lugar que ocupa en el programa semanal.",
                 "A notification is typed; you see the classification with its confidence, the similar orders, the built package and its place in the weekly schedule."),
        "terminado": [("Los tres clasificadores quedan comparados en una tabla con costo y latencia.", "The three classifiers are compared in a table with cost and latency."),
                      ("El programa optimizado supera al programa por prioridad en cumplimiento simulado.", "The optimized schedule beats the priority schedule in simulated compliance."),
                      ("Ningún permiso puede emitirse sin registro de aprobación.", "No permit can be issued without an approval record.")],
    },
    {
        "num": "P4", "file": "04-confiabilidad.html",
        "nombre": ("Motor de estrategia de confiabilidad", "Reliability strategy engine"),
        "eyebrow": ("Serie planta · de la falla al intervalo justificado", "Plant series · from failure to justified interval"),
        "one": ("Calcula la criticidad de cada equipo, ajusta Weibull por modo de falla, genera el borrador de FMECA desde los manuales, entrena modelos de condición y produce el plan de mantenimiento con su intervalo justificado.",
                "It computes each item's criticality, fits Weibull per failure mode, drafts the FMECA from the manuals, trains condition models and produces the maintenance plan with its justified interval."),
        "chips": [("Weibull con censura", "Weibull with censoring"), ("FMECA con citas", "cited FMECA"), "C-MAPSS", "MIMII", "CWRU"],
        "kpi": {"big": ("5", "5"), "small": ("métricas con línea base", "metrics with baseline"),
                "label": ("Lo que se va a medir", "What will be measured"), "rows": [],
                "expl": ("Vida remanente, detección acústica de anomalías, fallas de rodamiento, cobertura del FMECA generado y costo esperado por unidad de tiempo, cada una contra su método clásico. En la referencia publicada, los modelos generan bien algo más de la mitad del contenido clave de un FMECA.",
                         "Remaining life, acoustic anomaly detection, bearing faults, coverage of the generated FMECA and expected cost per unit time, each against its classical method. In the published reference, models correctly generate a little over half of the key content of an FMECA."),
                "ev": ("Diseño completo; las cifras se miden al implementar.", "Full design; figures are measured once implemented.")},
        "trio": [("Los intervalos de mantenimiento suelen salir del manual del fabricante o de la costumbre, no del historial real de fallas, y el FMECA se escribe a mano.",
                  "Maintenance intervals usually come from the manufacturer's manual or from habit, not from the real failure history, and the FMECA is written by hand."),
                 ("Matriz de criticidad, Weibull de dos parámetros por familia y modo de falla con censura, estrategia según el parámetro de forma, intervalo óptimo por costo y FMECA redactado con citas a los manuales; además, modelos de condición para vida remanente, acústica y rodamientos.",
                  "Criticality matrix, two-parameter Weibull per family and failure mode with censoring, strategy by shape parameter, cost-optimal interval and an FMECA drafted with citations to the manuals; plus condition models for remaining life, acoustics and bearings."),
                 ("Estadística de confiabilidad y aprendizaje automático al servicio de la estrategia de mantenimiento: cada intervalo queda justificado y comparado con el del fabricante.",
                  "Reliability statistics and machine learning serving maintenance strategy: every interval is justified and compared with the manufacturer's.")],
        "pasos": [(("Calcular la criticidad", "Compute criticality"),
                   ("Escalas de consecuencia en seguridad, ambiente, producción y costo, y escala de probabilidad; la puntuación queda como propiedad del equipo en el grafo.",
                    "Consequence scales for safety, environment, production and cost, and a probability scale; the score becomes a property of the equipment in the graph.")),
                  (("Preparar los datos de vida", "Prepare the life data"),
                   ("Para cada equipo y modo de falla, los tiempos entre fallas y los tiempos censurados de los equipos que no han fallado. La censura es obligatoria: ignorarla sesga el ajuste.",
                    "For each item and failure mode, the times between failures and the censored times of items that have not failed. Censoring is mandatory: ignoring it biases the fit.")),
                  (("Ajustar Weibull y decidir la estrategia", "Fit Weibull and decide the strategy"),
                   ("Weibull de dos parámetros con intervalos de confianza. Forma menor que 1: mortalidad infantil, revisar instalación; cercana a 1: falla aleatoria, monitoreo de condición; mayor que 1: desgaste, reemplazo a intervalo. El intervalo óptimo minimiza el costo esperado por unidad de tiempo y se compara con el del fabricante.",
                    "Two-parameter Weibull with confidence intervals. Shape below 1: infant mortality, review installation; near 1: random failure, condition monitoring; above 1: wear-out, replacement at interval. The optimal interval minimizes expected cost per unit time and is compared with the manufacturer's.")),
                  (("Generar el FMECA desde los manuales", "Generate the FMECA from the manuals"),
                   ("Para cada equipo: función, falla funcional, modo de falla, efecto, detección y tarea propuesta, con cita a la página fuente. El ingeniero valida y corrige, y la cobertura se mide contra un FMECA escrito a mano para dos equipos críticos.",
                    "For each item: function, functional failure, failure mode, effect, detection and proposed task, with a citation to the source page. The engineer validates and corrects, and coverage is measured against a hand-written FMECA for two critical items.")),
                  (("Entrenar los modelos de condición", "Train the condition models"),
                   ("Vida remanente en C-MAPSS con LSTM o CNN frente a un modelo preentrenado de series de tiempo; anomalía acústica en MIMII; falla de rodamiento en CWRU. La criticidad alimenta la política de repuestos del P5 y los planes entran al programa del P3.",
                    "Remaining life on C-MAPSS with LSTM or CNN versus a pretrained time-series model; acoustic anomaly on MIMII; bearing faults on CWRU. Criticality feeds the P5 spares policy and the plans enter the P3 schedule."))],
        "metricas": [(("RMSE y score PHM08 en C-MAPSS", "RMSE and PHM08 score on C-MAPSS"), ("LSTM entrenado desde cero", "LSTM trained from scratch"), None),
                     (("AUC de detección en MIMII", "Detection AUC on MIMII"), ("umbral sobre energía de banda", "band-energy threshold"), None),
                     (("F1 por clase en CWRU", "Per-class F1 on CWRU"), ("características espectrales con gradient boosting", "spectral features with gradient boosting"), None),
                     (("Cobertura del FMECA generado", "Coverage of the generated FMECA"), ("FMECA manual de referencia", "reference manual FMECA"), ("algo más de la mitad del contenido clave", "a little over half of the key content")),
                     (("Costo esperado por unidad de tiempo", "Expected cost per unit time"), ("intervalo del fabricante", "manufacturer's interval"), None)],
        "datos": [(("Historial de fallas del P1", "P1 failure history"), ("sintético", "synthetic"), ("Weibull por modo de falla", "Weibull per failure mode")),
                  (("Manuales OEM", "OEM manuals"), ("público", "public"), ("FMECA con citas", "cited FMECA")),
                  (("NASA C-MAPSS", "NASA C-MAPSS"), ("público", "public"), ("vida remanente", "remaining life")),
                  (("MIMII", "MIMII"), ("público", "public"), ("anomalía acústica", "acoustic anomaly")),
                  (("CWRU", "CWRU"), ("público", "public"), ("fallas de rodamiento", "bearing faults")),
                  (("PHMSA", "PHMSA"), ("público", "public"), ("distribución previa de causas", "prior distribution of causes"))],
        "demo": ("Matriz de criticidad navegable; al elegir un equipo se ven su curva de Weibull con el intervalo óptimo marcado, su FMECA con las citas y la señal de condición si la tiene.",
                 "A navigable criticality matrix; choosing an item shows its Weibull curve with the optimal interval marked, its FMECA with citations and its condition signal if it has one."),
        "terminado": [("Los ajustes de Weibull incluyen censura e intervalos de confianza.", "The Weibull fits include censoring and confidence intervals."),
                      ("El FMECA generado se compara con el de referencia en una tabla de aciertos y omisiones.", "The generated FMECA is compared with the reference in a table of hits and omissions."),
                      ("Cada modelo de condición tiene su línea base al lado.", "Every condition model has its baseline alongside.")],
    },
    {
        "num": "P5", "file": "05-materiales.html",
        "nombre": ("Torre de control de materiales y repuestos", "Materials and spares control tower"),
        "eyebrow": ("Serie planta · del catálogo a la alerta de faltantes", "Plant series · from catalog to shortage alert"),
        "one": ("Limpia y depura el catálogo, pronostica la demanda de repuestos, fija la política de inventario evaluada por nivel de servicio y cruza los materiales de proyecto con el cronograma para alertar faltantes antes de que detengan una actividad.",
                "It cleans and deduplicates the catalog, forecasts spare-part demand, sets the inventory policy evaluated by service level and matches project materials with the schedule to flag shortages before they stop an activity."),
        "chips": [("depuración con LLM", "LLM deduplication"), "Croston · TSB", "LightGBM", ("política (s,S)", "(s,S) policy"), "CP-SAT"],
        "kpi": {"big": ("−0,555", "−0.555"), "small": ("correlación", "correlation"),
                "label": ("Precisión contra servicio · referencia publicada", "Accuracy versus service · published reference"), "rows": [],
                "expl": ("En el benchmark público de 38 métodos sobre 20.330 órdenes reales, la precisión del pronóstico y el servicio se mueven en sentidos opuestos. Por eso cada método se reporta con las dos columnas lado a lado y se dice si el más preciso es o no el de mejor servicio.",
                         "In the public benchmark of 38 methods over 20,330 real orders, forecast accuracy and service move in opposite directions. That is why every method is reported with both columns side by side, stating whether the most accurate is the one with the best service."),
                "ev": ("Referencia de la literatura, no resultado propio. Las cifras propias se publican al implementar.",
                       "Literature reference, not an own result. Own figures are published once implemented.")},
        "trio": [("Catálogos con el mismo ítem escrito de varias formas, repuestos de demanda intermitente que los métodos clásicos pronostican mal y materiales de proyecto que llegan tarde y paran actividades.",
                  "Catalogs with the same item written several ways, intermittent-demand spares that classical methods forecast poorly and project materials that arrive late and stop activities."),
                 ("Normalización y depuración en tres etapas (bloqueo, similitud y decisión del LLM), clasificación de la demanda, cinco métodos de pronóstico comparados, un simulador de inventario (s,S) y un agente que revisa los próximos 90 días, ordena por holgura y propone resecuenciar con CP-SAT.",
                  "Three-stage normalization and deduplication (blocking, similarity and LLM decision), demand classification, five compared forecasting methods, an (s,S) inventory simulator and an agent that reviews the next 90 days, sorts by float and proposes resequencing with CP-SAT."),
                 ("Que el método más preciso no siempre es el que da mejor servicio: cada método se mide dos veces, por precisión y por cumplimiento de órdenes, y la alerta de faltantes se valida contra el cronograma.",
                  "That the most accurate method is not always the one with the best service: each method is measured twice, by accuracy and by order fill rate, and the shortage alert is validated against the schedule.")],
        "pasos": [(("Generar el catálogo con duplicados conocidos", "Generate the catalog with known duplicates"),
                   ("El mismo ítem escrito de varias formas: orden de atributos, abreviaturas, unidades distintas o proveedor en la descripción. Qué pares son duplicados queda guardado y es el conjunto de prueba.",
                    "The same item written several ways: attribute order, abbreviations, different units or supplier in the description. Which pairs are duplicates is stored and becomes the test set.")),
                  (("Normalizar y depurar", "Normalize and deduplicate"),
                   ("El LLM lleva cada descripción al formato sustantivo–modificador–atributos alineado con CFIHOS, con el sustantivo de un catálogo cerrado; luego bloqueo por clase, similitud por embeddings y decisión del LLM sobre los candidatos, contra una línea base con splink.",
                    "The LLM brings each description to the noun–modifier–attributes format aligned with CFIHOS, with the noun from a closed catalog; then blocking by class, embedding similarity and an LLM decision on candidates, against a splink baseline.")),
                  (("Clasificar la demanda y pronosticar", "Classify demand and forecast"),
                   ("Cada repuesto se clasifica como suave, errático, intermitente o grumoso; se comparan media móvil ponderada, Croston, TSB, LightGBM y un modelo preentrenado de series de tiempo, con partición por origen rodante.",
                    "Each spare is classified as smooth, erratic, intermittent or lumpy; weighted moving average, Croston, TSB, LightGBM and a pretrained time-series model are compared, with rolling-origin splits.")),
                  (("Simular el inventario", "Simulate the inventory"),
                   ("Política (s,S) con tiempo de entrega por ítem y órdenes de varias líneas; una orden cuenta como cumplida solo si se surten todas sus líneas. La criticidad del P4 fija el stock de seguridad por clase.",
                    "(s,S) policy with per-item lead time and multi-line orders; an order counts as filled only if all its lines are supplied. P4 criticality sets the safety stock per class.")),
                  (("Conciliar y alertar faltantes", "Reconcile and flag shortages"),
                   ("Requerido, comprado, recibido, despachado e instalado por ítem, unido a las actividades del cronograma; un agente revisa los próximos 90 días, ordena por holgura, propone resecuenciar con CP-SAT y redacta la alerta para compras.",
                    "Required, purchased, received, dispatched and installed per item, joined to the schedule activities; an agent reviews the next 90 days, sorts by float, proposes resequencing with CP-SAT and drafts the alert for procurement."))],
        "metricas": [(("Precisión y exhaustividad de la depuración", "Deduplication precision and recall"), ("splink sobre las mismas descripciones", "splink on the same descriptions"), None),
                     (("Error de pronóstico (MASE) por segmento de demanda", "Forecast error (MASE) per demand segment"), ("media móvil ponderada", "weighted moving average"), None),
                     (("Cumplimiento de órdenes y costo de inventario", "Order fill rate and inventory cost"), ("la misma política con media móvil", "the same policy with a moving average"), None),
                     (("Faltantes en ruta crítica detectados", "Critical-path shortages detected"), ("revisión manual de la lista de materiales", "manual review of the bill of materials"), None)],
        "datos": [(("Catálogo con duplicados inyectados", "Catalog with injected duplicates"), ("sintético", "synthetic"), ("prueba de la depuración", "deduplication test")),
                  (("Consumo de repuestos intermitente", "Intermittent spare-part consumption"), ("sintético", "synthetic"), ("pronóstico e inventario", "forecasting and inventory")),
                  (("Criticidad de equipos del P4", "P4 equipment criticality"), ("derivado", "derived"), ("stock de seguridad", "safety stock")),
                  (("Cronograma y materiales del P6", "P6 schedule and materials"), ("derivado", "derived"), ("alerta de faltantes", "shortage alert"))],
        "demo": ("Tablero con el catálogo antes y después de depurar, la tabla de métodos con precisión y servicio en columnas contiguas, y la lista de actividades en riesgo por falta de material.",
                 "A dashboard with the catalog before and after deduplication, the methods table with accuracy and service in adjacent columns, and the list of activities at risk for lack of material."),
        "terminado": [("La depuración se mide contra los duplicados inyectados.", "Deduplication is measured against the injected duplicates."),
                      ("Cada método de pronóstico aparece con sus dos métricas.", "Every forecasting method appears with both metrics."),
                      ("La alerta de faltantes se valida contra una ejecución simulada del cronograma.", "The shortage alert is validated against a simulated schedule run.")],
    },
    {
        "num": "P6", "file": "06-construccion-entrega.html",
        "nombre": ("Control de construcción y entrega por sistemas", "Construction control and handover by system"),
        "eyebrow": ("Serie planta · del cronograma a la certificación", "Plant series · from schedule to certification"),
        "one": ("Valida la calidad del cronograma, mide el avance con valor ganado, pronostica costo y fecha final con un modelo entrenado en proyectos reales, y traduce el avance por disciplina a entrega por subsistemas con ITR y punch.",
                "It validates schedule quality, measures progress with earned value, forecasts final cost and date with a model trained on real projects, and turns progress by discipline into handover by subsystem with ITRs and punch items."),
        "chips": ["Primavera P6", "DCMA 14", ("valor ganado", "earned value"), "Earned Schedule", "Monte Carlo"],
        "kpi": {"big": ("P63", "P63"), "small": ("percentil del cierre real", "percentile of the actual finish"),
                "label": ("Calibración · referencia publicada", "Calibration · published reference"), "rows": [],
                "expl": ("En el caso publicado de Great Western Main Line, el rango P10–P90 fue de agosto de 2018 a noviembre de 2019 y el proyecto cerró en mayo de 2019: en el percentil 63 de su pronóstico. Es el tipo de evidencia de calibración que se debe mostrar sobre los proyectos de DSLIB.",
                         "In the published Great Western Main Line case, the P10–P90 range ran from August 2018 to November 2019 and the project finished in May 2019: at the 63rd percentile of its forecast. That is the kind of calibration evidence to be shown on the DSLIB projects."),
                "ev": ("Referencia de la literatura, no resultado propio. Las cifras propias se publican al implementar.",
                       "Literature reference, not an own result. Own figures are published once implemented.")},
        "trio": [("El avance se reporta por disciplina, pero la entrega a operaciones se hace por subsistema; y los pronósticos de fecha final suelen ser deterministas, sin decir qué tan probable es cumplirlos.",
                  "Progress is reported by discipline, but handover to operations happens by subsystem; and final-date forecasts are usually deterministic, without saying how likely they are to be met."),
                 ("Lectura de cronogramas P6, los 14 chequeos DCMA, valor ganado y Earned Schedule por periodo, duraciones con un modelo cuantílico, Monte Carlo para P10, P50 y P80, y una capa de entrega por subsistemas con ITR leídos por visión y pronóstico de certificación.",
                  "P6 schedule reading, the 14 DCMA checks, earned value and Earned Schedule per period, durations with a quantile model, Monte Carlo for P10, P50 and P80, and a handover layer by subsystem with ITRs read by vision and a certification forecast."),
                 ("Control de proyectos probabilístico y calibrado: se reporta qué fracción de proyectos cae de verdad dentro de su rango, no solo el error medio.",
                  "Probabilistic, calibrated project control: it reports what fraction of projects actually lands inside its range, not just the mean error.")],
        "pasos": [(("Leer y validar el cronograma", "Read and validate the schedule"),
                   ("Un lector de cronogramas P6 (XER o XML) extrae actividades, relaciones, holguras, restricciones y recursos, y corre los 14 chequeos DCMA: lógica faltante, restricciones duras, holgura negativa, duraciones excesivas, ruta crítica continua, entre otros.",
                    "A P6 schedule reader (XER or XML) extracts activities, relationships, float, constraints and resources, and runs the 14 DCMA checks: missing logic, hard constraints, negative float, excessive durations, continuous critical path, among others.")),
                  (("Medir el avance", "Measure progress"),
                   ("Pesos por disciplina y reglas de crédito por actividad (en tubería: prefabricación, montaje, soldadura y prueba), y por periodo el valor ganado, los índices de cronograma y costo y Earned Schedule, sobre más de 130 proyectos reales de DSLIB.",
                    "Weights per discipline and credit rules per activity (for piping: prefabrication, erection, welding and testing), and per period the earned value, schedule and cost indices and Earned Schedule, over more than 130 real DSLIB projects.")),
                  (("Pronosticar con incertidumbre", "Forecast with uncertainty"),
                   ("Un modelo cuantílico (LightGBM o NGBoost) estima la duración de cada actividad con partición por proyecto; Monte Carlo sobre la red da P10, P50 y P80 de la fecha final, y se mide la cobertura real de esos intervalos.",
                    "A quantile model (LightGBM or NGBoost) estimates each activity's duration with a project-level split; Monte Carlo over the network gives the P10, P50 and P80 of the finish date, and the real coverage of those intervals is measured.")),
                  (("Entregar por sistemas", "Hand over by system"),
                   ("Matriz tag → subsistema → ITR del P2, ITR tipo A y B por tag y punch A y B con su responsable. Los ITR escaneados se leen con visión, con puntaje de confianza y cola de revisión humana, y se validan contra los criterios de aceptación.",
                    "Tag → subsystem → ITR matrix from P2, type A and B ITRs per tag and A and B punch items with their owner. Scanned ITRs are read by vision, with a confidence score and a human review queue, and validated against acceptance criteria.")),
                  (("Pronosticar la certificación", "Forecast certification"),
                   ("Un modelo de colas compara la tasa de cierre de ITR y punch con su tasa de apertura y da la fecha de certificación por subsistema, priorizada por la secuencia de arranque; salen el informe semanal y el dossier de entrega.",
                    "A queueing model compares ITR and punch closing and opening rates and gives the certification date per subsystem, prioritized by the start-up sequence; out come the weekly report and the handover dossier."))],
        "metricas": [(("Error del costo y la fecha final por tramo de avance", "Final cost and date error by progress band"), ("índices clásicos de valor ganado y Earned Schedule", "classical earned value and Earned Schedule indices"), None),
                     (("CRPS y cobertura real de P10–P80", "CRPS and real coverage of P10–P80"), ("simulación de tres puntos con duraciones estimadas", "three-point simulation with estimated durations"), None),
                     (("Exactitud por campo de la lectura de ITR", "Per-field accuracy of ITR reading"), ("captura manual sobre los mismos formularios", "manual entry on the same forms"), None),
                     (("Error de la fecha de certificación por subsistema", "Certification date error per subsystem"), ("extrapolación lineal de la curva de cierre", "linear extrapolation of the closing curve"), None)],
        "datos": [(("DSLIB, Universidad de Gante", "DSLIB, Ghent University"), ("público", "public"), ("más de 130 proyectos reales con línea base, seguimiento y riesgo", "more than 130 real projects with baseline, tracking and risk")),
                  (("PSPLIB", "PSPLIB"), ("público", "public"), ("validar el optimizador", "validate the optimizer")),
                  (("Matriz tag → subsistema → ITR del P2", "P2 tag → subsystem → ITR matrix"), ("derivado", "derived"), ("entrega por sistemas", "handover by system")),
                  (("ITR y punch de la planta", "Plant ITRs and punch items"), ("sintético", "synthetic"), ("certificación por subsistema", "certification by subsystem"))],
        "demo": ("Curva S planeada contra real con los indicadores por periodo; distribución de la fecha final con los percentiles marcados; mapa de la planta coloreado por estado de subsistema con su fecha pronosticada.",
                 "Planned versus actual S-curve with the indicators per period; final-date distribution with the percentiles marked; plant map colored by subsystem status with its forecast date."),
        "terminado": [("La validación DCMA corre sobre un cronograma real.", "DCMA validation runs on a real schedule."),
                      ("El modelo probabilístico reporta cobertura real y no solo error medio.", "The probabilistic model reports real coverage and not only mean error."),
                      ("La curva de entrega de subsistemas se compara contra la planeada.", "The subsystem handover curve is compared against the planned one.")],
    },
    {
        "num": "P7", "file": "07-calidad.html",
        "nombre": ("Aseguramiento de calidad en construcción", "Construction quality assurance"),
        "eyebrow": ("Serie planta · de la radiografía al dossier", "Plant series · from radiograph to dossier"),
        "one": ("Asiste la interpretación radiográfica de soldaduras, lleva el control estadístico de rechazos por soldador, lee los certificados de materiales y verifica que el dossier de calidad no tenga huecos.",
                "It assists weld radiograph interpretation, keeps statistical control of rejections per welder, reads material certificates and checks that the quality dossier has no gaps."),
        "chips": ["RIAWELC", "GDXray", "Grad-CAM", ("cartas p y u", "p and u charts"), ("certificados a datos", "certificates to data")],
        "kpi": {"big": ("75,83 %", "75.83 %"), "small": ("en radiografías reales", "on real radiographs"),
                "label": ("Exactitud · referencia publicada", "Accuracy · published reference"),
                "rows": [("base", ("en entrenamiento", "on training set"), ("98,75 %", "98.75 %")),
                         ("goal", ("en planta real", "on real plant"), ("75,83 %", "75.83 %"))],
                "expl": ("El clasificador publicado llega a 98,75 % en su conjunto de entrenamiento y cae a 75,83 % en radiografías reales de baja calidad. Esa caída se reporta, no se esconde: por eso el sistema se mide aparte fuera de dominio y se abstiene cuando no está seguro.",
                         "The published classifier reaches 98.75 % on its training set and drops to 75.83 % on real low-quality radiographs. That drop is reported, not hidden: that is why the system is measured separately out of domain and abstains when unsure."),
                "ev": ("Referencia de la literatura, no resultado propio. El sistema asiste al inspector certificado y no lo reemplaza.",
                       "Literature reference, not an own result. The system assists the certified inspector and does not replace them.")},
        "trio": [("La interpretación radiográfica depende del inspector, los rechazos por soldador se ven tarde y los huecos del dossier (juntas sin ensayo, certificados sin colada) aparecen al final, cuando ya cuestan.",
                  "Radiograph interpretation depends on the inspector, rejections per welder show up late and dossier gaps (joints without testing, certificates without a heat number) appear at the end, when they already cost money."),
                 ("Un clasificador de defectos con mapa de atención y umbral de abstención calibrado, cartas p y u y un modelo bayesiano por soldador, lectura de certificados de material hacia datos validados y un grafo de trazabilidad junta–soldador–procedimiento–ensayo–certificado.",
                  "A defect classifier with an attention map and a calibrated abstention threshold, p and u charts and a Bayesian model per welder, material certificates read into validated data and a joint–welder–procedure–test–certificate traceability graph."),
                 ("Visión por computador y estadística aplicadas a la calidad, con una regla clara: el sistema asiste al inspector certificado y no lo reemplaza.",
                  "Computer vision and statistics applied to quality, with a clear rule: the system assists the certified inspector and does not replace them.")],
        "pasos": [(("Preparar las radiografías", "Prepare the radiographs"),
                   ("Se normaliza el rango dinámico, se recorta la zona de soldadura y se divide en ventanas; la partición de prueba se hace por placa, nunca por ventana.",
                    "The dynamic range is normalized, the weld area is cropped and split into windows; the test split is made by plate, never by window.")),
                  (("Clasificar con explicación y abstención", "Classify with explanation and abstention"),
                   ("Entrenamiento sobre RIAWELC (24.407 radiografías en cuatro clases) y evaluación aparte en GDXray; Grad-CAM muestra la zona que explica cada predicción, y por debajo de cierta confianza la placa va al inspector nivel II o III. El umbral sale de la curva de riesgo contra cobertura.",
                    "Training on RIAWELC (24,407 radiographs in four classes) and separate evaluation on GDXray; Grad-CAM shows the area behind each prediction, and below a confidence level the plate goes to a level II or III inspector. The threshold comes from the risk-versus-coverage curve.")),
                  (("Controlar por soldador", "Control per welder"),
                   ("Registro de juntas con soldador, procedimiento, proceso, diámetro, espesor, posición y resultado; cartas p y u de tasa de rechazo por soldador y procedimiento, y un modelo beta-binomial que evita señalar a un soldador con pocas juntas.",
                    "A joint register with welder, procedure, process, diameter, thickness, position and result; p and u charts of rejection rate per welder and procedure, and a beta-binomial model that avoids flagging a welder with few joints.")),
                  (("Leer los certificados de material", "Read the material certificates"),
                   ("Un modelo con visión extrae colada, composición química y propiedades mecánicas hacia datos validados, y marca los certificados que no cumplen la especificación.",
                    "A vision model extracts heat number, chemical composition and mechanical properties into validated data, and flags certificates that do not meet the specification.")),
                  (("Cerrar el dossier", "Close the dossier"),
                   ("El grafo de trazabilidad detecta juntas sin ensayo, certificados sin colada coincidente y procedimientos fuera de su rango, y se genera la no conformidad con causa raíz y acción correctiva para aprobación del inspector.",
                    "The traceability graph detects joints without testing, certificates without a matching heat number and procedures outside their range, and the nonconformity is generated with root cause and corrective action for the inspector's approval."))],
        "metricas": [(("Exactitud y F1 en RIAWELC", "Accuracy and F1 on RIAWELC"), ("características clásicas con gradient boosting", "classical features with gradient boosting"), ("98,75 % en la referencia publicada", "98.75 % in the published reference")),
                     (("Exactitud en GDXray, fuera de dominio", "Accuracy on GDXray, out of domain"), ("el mismo modelo sin afinar", "the same model without fine-tuning"), ("75,83 % en radiografías reales", "75.83 % on real radiographs")),
                     (("Riesgo contra cobertura con abstención", "Risk versus coverage with abstention"), ("clasificación sin abstención", "classification without abstention"), None),
                     (("Exactitud por campo del certificado", "Per-field accuracy of the certificate"), ("captura manual sobre los mismos documentos", "manual entry on the same documents"), None),
                     (("Huecos de dossier detectados", "Dossier gaps detected"), ("revisión manual de una muestra", "manual review of a sample"), None)],
        "datos": [(("RIAWELC", "RIAWELC"), ("público", "public"), ("24.407 radiografías en cuatro clases: grieta, poro, falta de penetración y sin defecto", "24,407 radiographs in four classes: crack, porosity, lack of penetration and no defect")),
                  (("GDXray, serie soldaduras", "GDXray, welds series"), ("público", "public"), ("evaluación fuera de dominio", "out-of-domain evaluation")),
                  (("Registro de juntas, soldadores y procedimientos", "Joint, welder and procedure register"), ("sintético", "synthetic"), ("control estadístico y trazabilidad", "statistical control and traceability")),
                  (("Certificados de material con errores inyectados", "Material certificates with injected errors"), ("sintético", "synthetic"), ("lectura y validación", "reading and validation"))],
        "demo": ("Se carga una radiografía; se ve la clase propuesta con su confianza y el mapa de atención, o el aviso de abstención; al lado, el tablero de tasa de rechazo por soldador y la lista de huecos del dossier.",
                 "A radiograph is loaded; you see the proposed class with its confidence and attention map, or the abstention notice; beside it, the rejection-rate dashboard per welder and the list of dossier gaps."),
        "terminado": [("El informe muestra las dos exactitudes, dentro y fuera de dominio.", "The report shows both accuracies, in and out of domain."),
                      ("La curva de abstención está calibrada.", "The abstention curve is calibrated."),
                      ("El verificador de dossier corre sobre una obra simulada de 2.000 juntas.", "The dossier checker runs on a simulated job of 2,000 joints.")],
    },
    {
        "num": "P8", "file": "08-preservacion.html",
        "nombre": ("Programa de preservación de equipos", "Equipment preservation program"),
        "eyebrow": ("Serie planta · del manual al acta de despreservación", "Plant series · from manual to de-preservation record"),
        "one": ("Extrae las rutinas de preservación de los manuales del fabricante, genera el calendario por tag según el estado del equipo, registra la ejecución con evidencia, evalúa fotos de inspección y entrega el dossier al comisionamiento.",
                "It extracts preservation routines from the manufacturers' manuals, builds the calendar per tag according to equipment status, records execution with evidence, assesses inspection photos and hands the dossier over to commissioning."),
        "chips": ["NORSOK Z-006", "ISO 8501-1", ("rutinas con cita", "cited routines"), ("calendario por estado", "status-based calendar"), ("segmentación de corrosión", "corrosion segmentation")],
        "kpi": {"big": ("4", "4"), "small": ("métricas con línea base", "metrics with baseline"),
                "label": ("Lo que se va a medir", "What will be measured"), "rows": [],
                "expl": ("Exactitud de las rutinas extraídas, calidad de la segmentación de corrosión, concordancia del grado ISO 8501-1 con un inspector y horas para armar el plan de preservación, cada una contra el trabajo manual que reemplaza.",
                         "Accuracy of the extracted routines, corrosion segmentation quality, ISO 8501-1 grade agreement with an inspector and hours to build the preservation plan, each against the manual work it replaces."),
                "ev": ("Diseño completo; las cifras se miden al implementar. El ingeniero aprueba cada rutina antes de que entre al plan.",
                       "Full design; figures are measured once implemented. The engineer approves each routine before it enters the plan.")},
        "trio": [("Las rutinas de preservación están repartidas en decenas de manuales, cambian según el equipo esté en tránsito, en bodega, instalado o energizado, y una rutina vencida puede costar la garantía.",
                  "Preservation routines are spread across dozens of manuals, change depending on whether the equipment is in transit, in storage, installed or energized, and an overdue routine can cost the warranty."),
                 ("Extracción de rutinas con un LLM que devuelve un esquema validado y cita la página, una máquina de estados del equipo, calendario por tag cruzado con los hitos del P6, evidencia fotográfica ligada al tag y segmentación de corrosión con su grado.",
                  "Routine extraction with an LLM that returns a validated schema and cites the page, an equipment state machine, a per-tag calendar matched with P6 milestones, photo evidence linked to the tag and corrosion segmentation with its grade."),
                 ("El ciclo completo de NORSOK Z-006, de la preservación inicial a la despreservación antes del arranque, con datos trazables y aprobación del ingeniero.",
                  "The full NORSOK Z-006 cycle, from initial preservation to de-preservation before start-up, with traceable data and engineer approval.")],
        "pasos": [(("Definir la rutina", "Define the routine"),
                   ("Tarea, frecuencia en días, fase aplicable, condición de almacenamiento, consumible, criterio de aceptación y documento de origen con su página.",
                    "Task, frequency in days, applicable phase, storage condition, consumable, acceptance criterion and source document with its page.")),
                  (("Extraer las rutinas de los manuales", "Extract routines from the manuals"),
                   ("Un LLM devuelve ese esquema validado y cada campo trae su cita: sin cita no se guarda. La extracción se valida contra la lectura manual de 20 manuales y el ingeniero aprueba antes de que la rutina entre al plan.",
                    "An LLM returns that validated schema and every field carries its citation: without a citation it is not stored. Extraction is validated against a manual reading of 20 manuals and the engineer approves before the routine enters the plan.")),
                  (("Programar según el estado del equipo", "Schedule by equipment status"),
                   ("Máquina de estados: en tránsito, en bodega, instalado sin energizar, energizado y despreservado. El calendario por tag cruza rutinas, estado e hitos del cronograma del P6, y alerta rutinas vencidas y garantías en riesgo.",
                    "State machine: in transit, in storage, installed not energized, energized and de-preserved. The per-tag calendar matches routines, status and P6 schedule milestones, and flags overdue routines and warranties at risk.")),
                  (("Registrar y evaluar la evidencia", "Record and assess evidence"),
                   ("Cada ejecución queda con foto y firma ligadas al tag en el grafo del P1; un segmentador de corrosión da el porcentaje de área afectada y el grado ISO 8501-1, y las horas sobre el umbral de humedad en bodega priorizan la inspección.",
                    "Each execution is recorded with a photo and signature linked to the tag in the P1 graph; a corrosion segmenter gives the affected-area percentage and the ISO 8501-1 grade, and hours above the storage humidity threshold prioritize inspection.")),
                  (("Entregar al comisionamiento", "Hand over to commissioning"),
                   ("Se emite el acta de despreservación y se transfiere el registro completo de cada tag al sistema de completions del P6.",
                    "The de-preservation record is issued and each tag's full history is transferred to the P6 completions system."))],
        "metricas": [(("Exactitud por campo de la extracción de rutinas", "Per-field accuracy of routine extraction"), ("lectura manual de 20 manuales", "manual reading of 20 manuals"), None),
                     (("Calidad de la segmentación de corrosión (IoU)", "Corrosion segmentation quality (IoU)"), ("umbral de color sobre la imagen", "color threshold on the image"), None),
                     (("Concordancia del grado ISO 8501-1", "ISO 8501-1 grade agreement"), ("clasificación de un inspector sobre la misma muestra", "an inspector's grading of the same sample"), None),
                     (("Horas de armado del plan de preservación", "Hours to build the preservation plan"), ("consolidación manual de manuales", "manual consolidation of manuals"), None)],
        "datos": [(("Manuales de bombas, motores y tableros", "Pump, motor and switchboard manuals"), ("público", "public"), ("extracción de rutinas", "routine extraction")),
                  (("Imágenes de corrosión con grado ISO 8501-1", "Corrosion images with ISO 8501-1 grade"), ("público", "public"), ("segmentación y grado", "segmentation and grading")),
                  (("Humedad y temperatura de bodega", "Storage humidity and temperature"), ("sintético", "synthetic"), ("riesgo por ambiente", "environmental risk"))],
        "demo": ("Se carga un manual y se ven las rutinas extraídas con su cita; el calendario de la planta muestra rutinas al día, vencidas y equipos en riesgo; al subir una foto se ve el área de corrosión segmentada con su grado.",
                 "A manual is loaded and the extracted routines are shown with their citation; the plant calendar shows routines up to date, overdue and items at risk; uploading a photo shows the segmented corrosion area with its grade."),
        "terminado": [("La extracción está medida contra la lectura manual.", "Extraction is measured against the manual reading."),
                      ("El calendario respeta los estados del equipo.", "The calendar respects the equipment states."),
                      ("Existe el acta de transferencia al comisionamiento con el histórico completo de cada tag.", "There is a handover record to commissioning with each tag's full history.")],
    },
]

ICONOS = {
    "prob": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 9v4"/><path d="M12 17h.01"/><path d="M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/></svg>',
    "sol": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18h6"/><path d="M10 22h4"/><path d="M12 2a7 7 0 0 0-4 12.7c.6.5 1 1.3 1 2.1V17h6v-.2c0-.8.4-1.6 1-2.1A7 7 0 0 0 12 2z"/></svg>',
    "dem": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="6"/><path d="M8.2 13.2 7 22l5-3 5 3-1.2-8.8"/></svg>',
}


def e(s: str) -> str:
    return html.escape(s, quote=False)


def bi(par) -> str:
    if isinstance(par, str):
        return e(par)
    es, en = par
    if es == en:
        return e(es)
    return f'<span class="l-es">{e(es)}</span><span class="l-en">{e(en)}</span>'


def menu(activo: str | None, prefijo: str) -> str:
    items = []
    for num, archivo, nombre in MENU:
        clase = ' class="active"' if num == activo else ""
        items.append(f'<a href="{prefijo}{archivo}"{clase}><span class="dd-num">{num}</span>{bi(nombre)}</a>')
    return '<div class="dd-menu">' + "".join(items) + "</div>"


def kpi_html(p: dict) -> str:
    k = p["kpi"]
    filas = "".join(f'<div><span class="sw {c}"></span>{bi(lbl)}<b>{bi(v)}</b></div>' for c, lbl, v in k["rows"])
    cmp_ = f'<div class="kpi3-cmp">{filas}</div>' if filas else ""
    return (f'<div class="kpi3 kpi-dis"><span class="kstate">{bi(("Diseño completo", "Full design"))}</span>'
            f'<div class="kbig">{bi(k["big"])}<small>{bi(k["small"])}</small></div>'
            f'<div class="kpi3-k kleft">{bi(k["label"])}</div>{cmp_}'
            f'<p class="expl">{bi(k["expl"])}</p><p class="ev">{bi(k["ev"])}</p></div>')


def pagina(p: dict, i: int) -> str:
    sig = PROYECTOS[i + 1] if i + 1 < len(PROYECTOS) else None
    titulo_txt = f'{p["num"]} · {p["nombre"][0]} · {AUTOR}'
    chips = "".join(f'<span class="chip">{bi(c)}</span>' for c in p["chips"])
    trio_k = [("El problema", "The problem"), ("La solución", "The solution"), ("Qué demuestra", "What it shows")]
    trio = '<span class="tarrow" aria-hidden="true">→</span>'.join(
        f'<div class="tcard {c}"><div class="thead"><span class="ticon">{ICONOS[c]}</span><span class="tnum">0{n + 1}</span></div>'
        f'<div class="k">{bi(trio_k[n])}</div><p>{bi(texto)}</p></div>'
        for n, (c, texto) in enumerate(zip(("prob", "sol", "dem"), p["trio"])))
    pasos = "".join(f'<li><div class="n">{n + 1}</div><div><b>{bi(t)}</b><p>{bi(d)}</p></div></li>' for n, (t, d) in enumerate(p["pasos"]))
    tarjetas = []
    for nombre, base, ref in p["metricas"]:
        filas = f'<div class="rrow nobar"><span class="rl">{bi(("línea base", "baseline"))}</span><span class="rv">{bi(base)}</span></div>'
        if ref:
            filas += f'<div class="rrow nobar"><span class="rl">{bi(("referencia publicada", "published reference"))}</span><span class="rv">{bi(ref)}</span></div>'
        tarjetas.append(f'<div class="rcard"><div class="rtop"><div class="rk">{bi(nombre)}</div>'
                        f'<span class="rstate rs-obj">{bi(("por medir", "to measure"))}</span></div>'
                        f'<div class="rbars">{filas}</div></div>')
    datos = "".join(f'<li><b>{bi(n)}</b> <span class="origen o-{o[0][:4]}">{bi(o)}</span><br>{bi(u)}</li>' for n, o, u in p["datos"])
    terminado = "".join(f"<li>{bi(t)}</li>" for t in p["terminado"])
    if sig:
        siguiente = (f'<a class="next-card" href="{sig["file"]}"><div><div class="label">{bi(("Siguiente proyecto →", "Next project →"))}</div>'
                     f'<h3>{sig["num"]} · {bi(sig["nombre"])}</h3><p style="color: var(--text-dim); margin-top: 6px;">{bi(sig["one"])}</p></div>'
                     '<span class="arrow">→</span></a>')
    else:
        siguiente = (f'<a class="next-card" href="01-asistente-planta.html"><div><div class="label">{bi(("Volver al primer proyecto →", "Back to the first project →"))}</div>'
                     f'<h3>P1 · {bi(("Asistente de planta sobre grafo de conocimiento", "Plant assistant on a knowledge graph"))}</h3>'
                     f'<p style="color: var(--text-dim); margin-top: 6px;">{bi(("Implementado, con demo interactiva y evaluación medida.", "Built, with an interactive demo and a measured evaluation."))}</p></div>'
                     '<span class="arrow">→</span></a>')
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<meta name="theme-color" content="#eef2f0" />
<title>{e(titulo_txt)}</title>
<meta name="description" content="{e(p["one"][0])}" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet" />
<link rel="icon" type="image/svg+xml" href="../assets/favicon.svg" /><link rel="icon" type="image/png" sizes="32x32" href="../assets/favicon-32.png" /><link rel="apple-touch-icon" href="../assets/apple-touch-icon.png" />
<link rel="stylesheet" href="_styles.css?v={CSS_V}" />
</head>
<body>
<!-- generado por scripts/planta/paginas_diseno.py; editar el contenido allí -->
<nav>
  <div class="nav-inner">
    <a class="logo" href="../index.html"><i></i>Portafolio</a>
    <div class="nav-links">
      <a href="../index.html#about">{bi(("Sobre mí", "About me"))}</a>
      <a href="../index.html#stack">{bi(("Herramientas", "Tools"))}</a>
      <div class="nav-dd"><a href="../index.html#projects" class="dd-trigger active">{bi(("Proyectos", "Projects"))} <i class="dd-caret"></i></a>{menu(p["num"], "")}</div>
      <a href="../index.html#metodologia">{bi(("Metodología", "Methodology"))}</a>
      <a href="../index.html#experiencia">{bi(("Experiencia", "Experience"))}</a>
    </div>
    <div class="lang" id="lang"><button data-lang="es" class="on" type="button">ES</button><button data-lang="en" type="button">EN</button></div>
    <a class="btn btn-teal nav-cta" href="../index.html#contact">{bi(("Contacto →", "Contact →"))}</a>
  </div>
</nav>
<div class="container"><div class="crumbs-bar"><div class="crumbs">
      <a href="../index.html">{bi(("← Portafolio", "← Portfolio"))}</a>
      <span class="sep">/</span>
      <span class="here">{p["num"]} · {bi(p["nombre"])}</span>
    </div></div></div>
<header class="hero3">
  <div class="hero3-bg" aria-hidden="true"><i class="b1"></i><i class="b2"></i><i class="grid"></i></div>
  <div class="container hero3-in">
    <div class="hero3-l">
      <div class="hero3-eyebrow"><span class="dot"></span>{p["num"]} · {bi(p["eyebrow"])}</div>
      <h1>{bi(p["nombre"])}</h1>
      <p class="one">{bi(p["one"])}</p>
      <div class="hero3-cta">
        <a class="btn3 primary" href="#como">{bi(("Ver el diseño", "See the design"))} <span>↓</span></a>
        <a class="btn3 ghost" href="01-asistente-planta.html">{bi(("Ver el P1 en funcionamiento", "See P1 running"))} <span>→</span></a>
      </div>
      <div class="chips">{chips}</div>
    </div>
    <div class="hero3-r">{kpi_html(p)}</div>
  </div>
</header>
<section class="sec2 v2"><div class="container">
  <div class="h"><div class="eyebrow2">{bi(("En corto", "In short"))}</div><h2>{bi(("Qué problema resuelve y cómo", "What problem it solves and how"))}</h2></div>
  <div class="trio3">{trio}</div>
</div></section>
<section class="sec2 v2" id="como"><div class="container">
  <div class="h"><div class="eyebrow2">{bi(("Cómo funciona", "How it works"))}</div><h2>{bi(("Qué hace el sistema, paso a paso", "What the system does, step by step"))}</h2></div>
  <ol class="vsteps reveal2">{pasos}</ol>
</div></section>
<section class="sec2 v2"><div class="container">
  <div class="h"><div class="eyebrow2">{bi(("Métricas", "Metrics"))}</div><h2>{bi(("Cómo se va a medir, contra qué", "How it will be measured, and against what"))}</h2>
  <p class="sub">{bi(("Cada métrica se publica con su línea base al lado: el método clásico que el sistema reemplaza. Sin línea base, el proyecto no se publica.", "Every metric is published with its baseline alongside: the classical method the system replaces. Without a baseline, the project is not published."))}</p></div>
  <div class="rgrid">{"".join(tarjetas)}</div>
  <p class="rnote">{bi(("Las referencias publicadas vienen de la literatura que cita el diseño; no son resultados propios. Las cifras propias se agregan cuando el sistema esté implementado y medido.", "Published references come from the literature cited by the design; they are not own results. Own figures are added once the system is built and measured."))}</p>
</div></section>
<section class="sec2 v2"><div class="container">
  <div class="h"><div class="eyebrow2">{bi(("Datos, demo y terminado", "Data, demo and done"))}</div><h2>{bi(("Con qué datos, qué se va a ver y cuándo está listo", "Which data, what you will see and when it is done"))}</h2></div>
  <div class="dis-grid">
    <div class="dis-card"><div class="k">{bi(("Datos", "Data"))}</div><ul class="dis-list">{datos}</ul></div>
    <div class="dis-card"><div class="k">{bi(("Demo prevista", "Planned demo"))}</div><p>{bi(p["demo"])}</p>
      <div class="k" style="margin-top:18px">{bi(("Terminado cuando", "Done when"))}</div><ul class="dis-list check">{terminado}</ul></div>
  </div>
</div></section>
<section class="sec2 v2"><div class="container">
    {siguiente}
</div></section>
<footer>
  <div class="footer-inner">
    <div>// {e(AUTOR)} · {bi(PERFIL)} · 2026</div>
    <div>github.com/Edgar-Suarez-creator</div>
  </div>
</footer>
<script>
(function(){{
  function setLang(lang){{
    document.documentElement.lang = lang;
    document.querySelectorAll('#lang button').forEach(b => b.classList.toggle('on', b.dataset.lang === lang));
    try {{ sessionStorage.setItem('lang', lang); }} catch(e) {{}}
  }}
  document.querySelectorAll('#lang button').forEach(b => b.addEventListener('click', () => setLang(b.dataset.lang)));
  let saved = 'es'; try {{ saved = sessionStorage.getItem('lang') || 'es'; }} catch(e) {{}}
  setLang(saved);
  const io2 = new IntersectionObserver(es => es.forEach(e => {{ if (e.isIntersecting) {{ e.target.classList.add('in'); io2.unobserve(e.target); }} }}), {{ threshold: .2 }});
  document.querySelectorAll('.reveal2').forEach(el => io2.observe(el));
  setTimeout(() => document.querySelectorAll('.reveal2').forEach(el => el.classList.add('in')), 1200);
}})();
</script>
</body>
</html>
"""


def sincronizar_menu(ruta: Path, activo: str | None, prefijo: str) -> None:
    """Reemplaza el menú desplegable de proyectos en una página existente."""
    src = ruta.read_text(encoding="utf-8")
    nuevo, n = re.subn(r'<div class="dd-menu">.*?</div>(?=</div>)', lambda _m: menu(activo, prefijo), src, count=1, flags=re.S)
    if n != 1:
        raise SystemExit(f"{ruta.name}: no se encontró el menú de proyectos")
    ruta.write_text(nuevo, encoding="utf-8")


def main() -> None:
    for i, p in enumerate(PROYECTOS):
        (PROJECTS / p["file"]).write_text(pagina(p, i), encoding="utf-8")
        print(f'{p["num"]}: projects/{p["file"]}')
    sincronizar_menu(PROJECTS / "01-asistente-planta.html", "P1", "")
    sincronizar_menu(ROOT / "index.html", None, "projects/")
    print("menú sincronizado en index.html y en el P1")


if __name__ == "__main__":
    main()
