// P1 — Serie planta · Asistente de planta sobre grafo de conocimiento
// Demo 1 (terminal): transcripción real capturada el 2026-10-04 en el repositorio p1-asistente-planta (main), Windows · PowerShell.
// Demo 2 (sistema): grafo de proceso de las áreas 1105 y 1205, generado desde planta-core por scripts/planta/grafo_p01.py,
//   y tres reportes de falla con las salidas reales del agente (p1-asistente-planta/app/demo.json · sin LLM).

const P01_L = (es, en) => (document.documentElement.lang === 'es' ? es : en);

// ── Demo 1: terminal ─────────────────────────────────────────────────────
const P01_TERMINAL_SCRIPT = [
  { t: 0.3, kind: 'caption', text: '01 / Estado del repositorio (main)' },
  { t: 0.6, kind: 'cmd', text: 'git log --oneline' },
  { t: 1.35, kind: 'out', text: '66b4cc5 feat: línea de comandos, demo con la estética del portafolio y corrección del pendiente de Neo4j en RESULTS.md' },
  { t: 1.5, kind: 'out', text: '9e26b20 docs: README con resultados, origen de datos y límites; Makefile, tareas.py, Docker y export Cypher' },
  { t: 1.65, kind: 'out', text: '953a323 feat(app): demo local sin credenciales y versión estática' },
  { t: 1.8, kind: 'out', text: 'f9962cd feat(eval): banco de 100 preguntas, 20 paráfrasis, lista manual de aislamientos y RAG plano como línea base' },
  { t: 1.95, kind: 'out', text: 'fda80e7 test: esquema del grafo, aislamientos, resolutor, agente y aprobación' },
  { t: 2.1, kind: 'out', text: '6b6dcce feat: grafo de conocimiento, extracción con cita, normalización de tags y aislamientos' },

  { t: 3.2, kind: 'caption', text: '02 / Instalar planta-core y el paquete, y generar los datos sintéticos (semilla 14224)' },
  { t: 3.5, kind: 'cmd', text: 'python tareas.py setup' },
  { t: 5.0, kind: 'out', text: '… 19 × Requirement already satisfied …', color: 'accent' },
  { t: 5.5, kind: 'out', text: 'Successfully built planta-core', color: 'success' },
  { t: 5.65, kind: 'out', text: 'Successfully installed planta-core-0.1.0', color: 'success' },
  { t: 5.8, kind: 'out', text: 'Successfully built p1-asistente-planta', color: 'success' },
  { t: 5.95, kind: 'out', text: 'Successfully installed p1-asistente-planta-0.1.0', color: 'success' },
  { t: 6.4, kind: 'out', text: 'datos generados en ~\\GitHub\\planta-core\\datos (semilla 14224)' },
  { t: 6.6, kind: 'out', text: '5699493c446915c685e797fa8417c5f251d48ff3b4fec42ee28810f42f3c428b  topologia.json' },
  { t: 6.7, kind: 'out', text: 'e2c7366f22284dbe2efff99e18a50d9f3bf94b7177db944afa437c8428c6f5ec  catalogos_iso14224.json' },
  { t: 6.8, kind: 'out', text: 'adf3bd37bfb6bc636b16354b7b9f3ea6f0b385701aa4be0d47e8dd95629b8880  historial_fallas.json' },
  { t: 6.9, kind: 'out', text: '642781772e67b047a113b5fbbf93b7c015a6701e4f82a0e3f3fde5543de6ab8e  documentos.json' },
  { t: 7.0, kind: 'out', text: '9b23e65f6d919ebcd1e56328561a554dd371f1fb68be67e792d10421df5042a7  etiquetas_huecos.json' },
  { t: 7.4, kind: 'out', text: '→ misma semilla, mismos archivos: git status de planta-core queda limpio tras regenerar', color: 'accent' },

  { t: 8.6, kind: 'caption', text: '03 / Pruebas' },
  { t: 8.9, kind: 'cmd', text: 'python -m pytest -q' },
  { t: 10.6, kind: 'out', text: '9 passed in 2.46s', color: 'success' },

  { t: 11.8, kind: 'caption', text: '04 / Evaluación: 100 preguntas y 20 paráfrasis · GraphRAG contra RAG plano · sin LLM' },
  { t: 12.1, kind: 'cmd', text: 'python -m evaluacion.run' },
  { t: 14.4, kind: 'out', text: 'run: evaluacion/runs/2026-10-04-deterministico.json' },
  { t: 14.6, kind: 'out', text: 'GraphRAG 100.0 % · RAG plano (cota) 16.0 % · tokens mediana 15.0 vs 189.5 · aislamientos P 100.0 % R 100.0 % · 0.16 s', color: 'success' },

  { t: 16.0, kind: 'caption', text: '05 / evaluacion/RESULTS.md · respuesta exacta por familia; el RAG plano se mide como cota superior' },
  { t: 16.3, kind: 'cmd', text: 'Get-Content evaluacion\\RESULTS.md' },
  { t: 17.4, kind: 'table', cols: ['familia', 'n', 'GraphRAG', 'RAG plano (cota)', 'tokens grafo', 'tokens RAG', 'enrutamiento'], rows: [
    ['Identificación', '25', '100.0 %', '36.0 %', '16', '176', '100.0 %'],
    ['Topología', '25', '100.0 %', '0.0 %', '17', '152', '100.0 %'],
    ['Historial', '25', '100.0 %', '28.0 %', '14', '222', '100.0 %'],
    ['Completitud', '25', '100.0 %', '0.0 %', '14', '216', '100.0 %'],
    ['Total', '100', '100.0 %', '16.0 %', '15.0', '189.5', '100.0 %', 'highlight'],
  ]},
  { t: 22.0, kind: 'table', cols: ['20 paráfrasis fuera de plantilla', 'GraphRAG', 'RAG plano (cota)', 'enrutamiento'], rows: [
    ['redacción libre', '10.0 %', '20.0 %', '20.0 %', 'highlight'],
  ]},
  { t: 24.0, kind: 'out', text: '→ El 100 % se mide dentro del sublenguaje de las plantillas: con redacción libre el enrutador manda 16 de 20 a los manuales.', color: 'warn' },
  { t: 24.3, kind: 'out', text: '  Esa brecha es la que cierra la generación de Cypher con LLM (pendiente de llave).', color: 'warn' },
  { t: 25.6, kind: 'table', cols: ['aislamientos · 21 equipos críticos', 'precisión', 'exhaustividad', 'idénticos'], rows: [
    ['válvulas propuestas vs. lista hecha a mano', '100.0 %', '100.0 %', '21/21', 'highlight'],
  ]},
  { t: 27.4, kind: 'table', cols: ['tags en 202 órdenes', 'mal escritos', 'resueltos bien', 'al reporte de conflictos', 'a un tag equivocado'], rows: [
    ['reglas + similitud', '32', '29', '3', '0', 'highlight'],
  ]},

  { t: 30.0, kind: 'caption', text: '06 / Un reporte de falla de punta a punta · plantilla, sin LLM' },
  { t: 30.3, kind: 'cmd', text: 'python -m asistente "La bomba 1105p01 está botando glicol por el sello"' },
  { t: 34.8, kind: 'json', text: 'BORRADOR · 1105-P-01 · Bomba de glicol pobre A\n  síntoma      ELP · Fuga externa de fluido de proceso\n  intervención SE CAMBIA SELLO MECÁNICO (15 antecedentes en la clase)\n  aislamientos 1105-HV-09, 1105-HV-10\n  permisos     Permiso de trabajo en frío · Aislamiento de proceso (2 válvulas, bloqueo y etiquetado) · Aislamiento eléctrico del motor (LOTO) · Drenaje, despresurización y prueba de atmósfera (gas y glicol)\n  cuadrilla    mecánica + eléctrica (desenergizar motor)\n  duración     8.1 h (mediana de la clase)\n  herramientas buscar_equipo → historial → fallas_similares → aislamientos\n  citas        OT-2024-00092, OT-2025-00141, OT-2025-00166, OT-2026-00186, OT-2026-00193, DS-1105-P-01 …\n  → no se emite sin aprobación humana registrada' },
  { t: 37.2, kind: 'cmd', text: 'python -m asistente "Hay una bomba que vibra mucho en glicol"' },
  { t: 40.2, kind: 'out', text: 'NO_RESUELTA · No se identificó el tag del equipo. Candidatos: 1105-P-01, 1105-P-02, 1405-P-03. Pida al reportante el tag de la placa; el sistema no elige por él.', color: 'warn' },

  { t: 42.0, kind: 'caption', text: '07 / Lo que falta: llave de API, Docker o personas' },
  { t: 42.3, kind: 'cmd', text: 'Select-String evaluacion\\RESULTS.md -Pattern "^\\| (Generación|Carga|Extracción|Minutos|Verificación)"' },
  { t: 45.6, kind: 'out', text: 'evaluacion\\RESULTS.md:88:| Generación de Cypher con LLM y redacción con LLM | ANTHROPIC_API_KEY |', color: 'warn' },
  { t: 45.75, kind: 'out', text: 'evaluacion\\RESULTS.md:89:| Carga y consultas sobre Neo4j 5 (`make neo4j`) | Demonio Docker |', color: 'warn' },
  { t: 45.9, kind: 'out', text: 'evaluacion\\RESULTS.md:90:| Extracción desde PDFs reales con Docling o visión | PDFs del fabricante y llave de API |', color: 'warn' },
  { t: 46.05, kind: 'out', text: 'evaluacion\\RESULTS.md:91:| Minutos para resolver un reporte de falla contra búsqueda manual | Cronometraje con usuarios |', color: 'warn' },
  { t: 46.2, kind: 'out', text: 'evaluacion\\RESULTS.md:92:| Verificación a mano de las 100 respuestas esperadas | Ingeniero de planta |', color: 'warn' },
  { t: 47.4, kind: 'caption', text: '✓ Cada cifra sale de evaluacion/runs/2026-10-04-deterministico.json · datos sintéticos · sin LLM' },
];

const P01TerminalDemo = makeTerminalDemo({
  script: P01_TERMINAL_SCRIPT,
  duration: 50,
  persistKey: 'real-p01-terminal-v1',
  title: 'PowerShell — p1-asistente-planta (main)',
  cwd: '~\\GitHub\\p1-asistente-planta',
  captionPrefix: 'P1',
});

// ── Demo 2: grafo de proceso + agente ────────────────────────────────────
// <grafo:inicio> generado por scripts/planta/grafo_p01.py desde planta-core; no editar a mano
const P01_NODES = [{"id": "1105-PT-01", "k": "pt", "x": 130, "y": 49, "crit": 0}, {"id": "LIM-GAS-ENTRADA", "k": "lim", "x": 30, "y": 92}, {"id": "1105-HV-01", "k": "hv", "x": 78, "y": 92}, {"id": "1105-V-01", "k": "eq", "x": 130, "y": 92, "crit": 1}, {"id": "1105-HV-02", "k": "hv", "x": 186, "y": 92}, {"id": "1105-HV-03", "k": "hv", "x": 352, "y": 92}, {"id": "1105-V-02", "k": "eq", "x": 262, "y": 130, "crit": 1}, {"id": "1105-PT-02", "k": "pt", "x": 300, "y": 180, "crit": 0}, {"id": "1105-HV-05", "k": "hv", "x": 262, "y": 205}, {"id": "1105-HV-13", "k": "hv", "x": 120, "y": 231}, {"id": "1105-PCV-01", "k": "pcv", "x": 262, "y": 275, "crit": 0}, {"id": "1105-V-03", "k": "eq", "x": 262, "y": 350, "crit": 0}, {"id": "1105-HV-06", "k": "hv", "x": 325, "y": 350}, {"id": "1105-E-01", "k": "eq", "x": 390, "y": 350, "crit": 1}, {"id": "1105-HV-07", "k": "hv", "x": 452, "y": 350}, {"id": "1105-E-02", "k": "eq", "x": 45, "y": 369, "crit": 0}, {"id": "1105-HV-04", "k": "hv", "x": 325, "y": 432}, {"id": "1105-HV-08", "k": "hv", "x": 390, "y": 432}, {"id": "1105-V-04", "k": "eq", "x": 452, "y": 432, "crit": 1}, {"id": "1105-HV-10", "k": "hv", "x": 95, "y": 476}, {"id": "1105-P-01", "k": "eq", "x": 150, "y": 476, "crit": 1}, {"id": "1105-HV-09", "k": "hv", "x": 205, "y": 476}, {"id": "HDR-1105-SUC", "k": "hdr", "x": 262, "y": 495}, {"id": "1105-V-05", "k": "eq", "x": 452, "y": 520, "crit": 0}, {"id": "HDR-1105-DES", "k": "hdr", "x": 45, "y": 533}, {"id": "1105-HV-12", "k": "hv", "x": 95, "y": 583}, {"id": "1105-P-02", "k": "eq", "x": 150, "y": 583, "crit": 1}, {"id": "1105-HV-11", "k": "hv", "x": 205, "y": 583}, {"id": "1205-PT-01", "k": "pt", "x": 600, "y": 49, "crit": 0}, {"id": "1205-HV-01", "k": "hv", "x": 540, "y": 92}, {"id": "1205-V-01", "k": "eq", "x": 600, "y": 92, "crit": 1}, {"id": "1205-HV-02", "k": "hv", "x": 715, "y": 130}, {"id": "1205-C-01", "k": "eq", "x": 780, "y": 130, "crit": 1}, {"id": "1205-HV-03", "k": "hv", "x": 845, "y": 130}, {"id": "HDR-1205-SUC", "k": "hdr", "x": 660, "y": 168}, {"id": "HDR-1205-DES", "k": "hdr", "x": 905, "y": 174}, {"id": "1205-HV-04", "k": "hv", "x": 715, "y": 224}, {"id": "1205-C-02", "k": "eq", "x": 780, "y": 224, "crit": 1}, {"id": "1205-HV-05", "k": "hv", "x": 845, "y": 224}, {"id": "1205-E-01", "k": "eq", "x": 945, "y": 275, "crit": 1}, {"id": "1205-HV-07", "k": "hv", "x": 715, "y": 312}, {"id": "1205-PCV-01", "k": "pcv", "x": 845, "y": 312, "crit": 0}, {"id": "1205-V-02", "k": "eq", "x": 945, "y": 369, "crit": 0}, {"id": "1205-PT-02", "k": "pt", "x": 905, "y": 397, "crit": 0}, {"id": "1205-HV-06", "k": "hv", "x": 945, "y": 457}, {"id": "1205-HV-08", "k": "hv", "x": 635, "y": 520}, {"id": "1205-P-01", "k": "eq", "x": 700, "y": 520, "crit": 1}, {"id": "1205-HV-09", "k": "hv", "x": 765, "y": 520}, {"id": "LIM-GAS-EXPORTACION", "k": "lim", "x": 945, "y": 527}, {"id": "1205-V-03", "k": "eq", "x": 575, "y": 568, "crit": 0}, {"id": "HDR-1205-ACE", "k": "hdr", "x": 825, "y": 568}, {"id": "1205-E-02", "k": "eq", "x": 880, "y": 568, "crit": 0}, {"id": "1205-HV-11", "k": "hv", "x": 635, "y": 615}, {"id": "1205-P-02", "k": "eq", "x": 700, "y": 615, "crit": 1}, {"id": "1205-HV-12", "k": "hv", "x": 765, "y": 615}, {"id": "1205-HV-10", "k": "hv", "x": 880, "y": 659}];
const P01_EDGES = [{"a": "LIM-GAS-ENTRADA", "b": "1105-HV-01"}, {"a": "1105-HV-01", "b": "1105-V-01"}, {"a": "1105-V-01", "b": "1105-HV-02"}, {"a": "1105-HV-02", "b": "1105-V-02"}, {"a": "1105-V-02", "b": "1105-HV-03"}, {"a": "1105-HV-03", "b": "1205-HV-01"}, {"a": "1105-V-02", "b": "1105-HV-05"}, {"a": "1105-HV-05", "b": "1105-PCV-01"}, {"a": "1105-PCV-01", "b": "1105-V-03"}, {"a": "1105-V-03", "b": "1105-HV-06"}, {"a": "1105-HV-06", "b": "1105-E-01"}, {"a": "1105-E-01", "b": "1105-HV-07"}, {"a": "1105-HV-07", "b": "1105-V-04"}, {"a": "1105-V-04", "b": "1105-V-05"}, {"a": "1105-V-05", "b": "1105-HV-08"}, {"a": "1105-HV-08", "b": "1105-E-01"}, {"a": "1105-E-01", "b": "1105-HV-04"}, {"a": "1105-HV-04", "b": "HDR-1105-SUC"}, {"a": "HDR-1105-SUC", "b": "1105-HV-09"}, {"a": "1105-HV-09", "b": "1105-P-01"}, {"a": "1105-P-01", "b": "1105-HV-10"}, {"a": "1105-HV-10", "b": "HDR-1105-DES"}, {"a": "HDR-1105-SUC", "b": "1105-HV-11"}, {"a": "1105-HV-11", "b": "1105-P-02"}, {"a": "1105-P-02", "b": "1105-HV-12"}, {"a": "1105-HV-12", "b": "HDR-1105-DES"}, {"a": "HDR-1105-DES", "b": "1105-E-02"}, {"a": "1105-E-02", "b": "1105-HV-13"}, {"a": "1105-HV-13", "b": "1105-V-02"}, {"a": "1205-HV-01", "b": "1205-V-01"}, {"a": "1205-V-01", "b": "HDR-1205-SUC"}, {"a": "HDR-1205-SUC", "b": "1205-HV-02"}, {"a": "1205-HV-02", "b": "1205-C-01"}, {"a": "1205-C-01", "b": "1205-HV-03"}, {"a": "1205-HV-03", "b": "HDR-1205-DES"}, {"a": "HDR-1205-SUC", "b": "1205-HV-04"}, {"a": "1205-HV-04", "b": "1205-C-02"}, {"a": "1205-C-02", "b": "1205-HV-05"}, {"a": "1205-HV-05", "b": "HDR-1205-DES"}, {"a": "HDR-1205-DES", "b": "1205-E-01"}, {"a": "1205-E-01", "b": "1205-V-02"}, {"a": "1205-V-02", "b": "1205-HV-06"}, {"a": "1205-HV-06", "b": "LIM-GAS-EXPORTACION"}, {"a": "HDR-1205-DES", "b": "1205-PCV-01"}, {"a": "1205-PCV-01", "b": "1205-HV-07"}, {"a": "1205-HV-07", "b": "HDR-1205-SUC"}, {"a": "1205-V-03", "b": "1205-HV-08"}, {"a": "1205-HV-08", "b": "1205-P-01"}, {"a": "1205-P-01", "b": "1205-HV-09"}, {"a": "1205-HV-09", "b": "HDR-1205-ACE"}, {"a": "1205-V-03", "b": "1205-HV-11"}, {"a": "1205-HV-11", "b": "1205-P-02"}, {"a": "1205-P-02", "b": "1205-HV-12"}, {"a": "1205-HV-12", "b": "HDR-1205-ACE"}, {"a": "HDR-1205-ACE", "b": "1205-E-02"}, {"a": "1205-E-02", "b": "1205-HV-10"}, {"a": "1205-HV-10", "b": "1205-V-03", "via": [[575, 659]]}, {"a": "1105-PT-01", "b": "1105-V-01", "inst": 1}, {"a": "1105-PT-02", "b": "1105-V-02", "inst": 1}, {"a": "1205-PT-01", "b": "1205-V-01", "inst": 1}, {"a": "1205-PT-02", "b": "1205-V-02", "inst": 1}];
// <grafo:fin>

const P01_NODE = Object.fromEntries(P01_NODES.map(n => [n.id, n]));
const p01Key = (a, b) => (a < b ? `${a}|${b}` : `${b}|${a}`);
P01_NODES.forEach((n, i) => { n.t = 0.35 + i * 0.062; });
P01_EDGES.forEach(e => { e.t = Math.max(P01_NODE[e.a].t, P01_NODE[e.b].t) + 0.1; e.key = p01Key(e.a, e.b); });
const P01_SHORT = (id) => (id.startsWith('HDR-') ? '' : id.startsWith('LIM-') ? '' : id.slice(5));
const P01_LIM_LABEL = { 'LIM-GAS-ENTRADA': ['gas de entrada', 'inlet gas'], 'LIM-GAS-EXPORTACION': ['a exportación', 'to export'] };

const TOOL_GAP = 1.5;
const P01_CASOS = [
  {
    t0: 6.0, t1: 21.0,
    reporte: 'La bomba 1105p01 está botando glicol por el sello',
    escrito: '1105p01', tag: '1105-P-01',
    modo: 'ELP', modoNombre: ['fuga externa de fluido de proceso', 'external leakage of process medium'],
    clase: ['1105-P-02', '1205-P-01', '1205-P-02'],
    recorrido: [['1105-P-01', '1105-HV-09'], ['1105-P-01', '1105-HV-10']],
    valvulas: ['1105-HV-09', '1105-HV-10'],
    fuera: [],
    tools: [
      ["buscar_equipo('1105-P-01')", ['Bomba de glicol pobre A · bomba centrífuga · regeneración de glicol · crítico', 'Lean glycol pump A · centrifugal pump · glycol regeneration · critical']],
      ["historial('1105-P-01')", ['7 órdenes · la última OT-2026-00193, 2026-08-12, falla al arrancar', '7 orders · latest OT-2026-00193, 2026-08-12, fail to start']],
      ["fallas_similares('Bomba centrífuga', 'ELP')", ['15 antecedentes en la clase · lo más frecuente: SE CAMBIA SELLO MECÁNICO', '15 precedents in the class · most frequent: SE CAMBIA SELLO MECÁNICO']],
      ["aislamientos('1105-P-01')", ['1105-HV-09 · 1105-HV-10 · ninguna rama abierta', '1105-HV-09 · 1105-HV-10 · no open branch']],
    ],
    sol: {
      intervencion: 'SE CAMBIA SELLO MECÁNICO',
      aislamiento: ['1105-HV-09, 1105-HV-10', '1105-HV-09, 1105-HV-10'],
      permisos: ['trabajo en frío · aislamiento de proceso · LOTO del motor · prueba de atmósfera', 'cold work · process isolation · motor LOTO · gas test'],
      cuadrilla: ['mecánica + eléctrica', 'mechanical + electrical'],
      duracion: ['8,1 h · mediana de la clase', '8.1 h · class median'],
    },
  },
  {
    t0: 21.5, t1: 36.5,
    reporte: 'Alto diferencial en el aeroenfriador 1205 E 01, posible taponamiento',
    escrito: '1205 E 01', tag: '1205-E-01',
    modo: 'PLU', modoNombre: ['taponamiento', 'plugged / choked'],
    clase: ['1105-E-01', '1105-E-02', '1205-E-02'],
    recorrido: [['1205-E-01', 'HDR-1205-DES'], ['HDR-1205-DES', '1205-HV-03'], ['HDR-1205-DES', '1205-HV-05'],
                ['HDR-1205-DES', '1205-PCV-01'], ['1205-PCV-01', '1205-HV-07'], ['1205-E-01', '1205-V-02'], ['1205-V-02', '1205-HV-06']],
    valvulas: ['1205-HV-03', '1205-HV-05', '1205-HV-06', '1205-HV-07'],
    fuera: ['1205-V-02', '1205-PCV-01'],
    tools: [
      ["buscar_equipo('1205-E-01')", ['Aeroenfriador de descarga · intercambiador · compresión · crítico · sin hoja de datos', 'Discharge air cooler · heat exchanger · compression · critical · no datasheet']],
      ["historial('1205-E-01')", ['11 órdenes · la última OT-2026-00188, 2026-07-02, fuga interna', '11 orders · latest OT-2026-00188, 2026-07-02, internal leakage']],
      ["fallas_similares('Intercambiador de calor', 'PLU')", ['10 antecedentes en la clase · lo más frecuente: SE LIMPIA HAZ DE TUBOS', '10 precedents in the class · most frequent: SE LIMPIA HAZ DE TUBOS']],
      ["aislamientos('1205-E-01')", ['4 válvulas · quedan fuera de servicio 1205-V-02 y 1205-PCV-01', '4 valves · 1205-V-02 and 1205-PCV-01 go out of service']],
    ],
    sol: {
      intervencion: 'SE LIMPIA HAZ DE TUBOS',
      aislamiento: ['HV-03, HV-05, HV-06, HV-07 · fuera: V-02, PCV-01', 'HV-03, HV-05, HV-06, HV-07 · out: V-02, PCV-01'],
      permisos: ['trabajo en frío · aislamiento de proceso (4 válvulas) · prueba de atmósfera', 'cold work · process isolation (4 valves) · gas test'],
      cuadrilla: ['mecánica', 'mechanical'],
      duracion: ['11,6 h · mediana de la clase', '11.6 h · class median'],
    },
  },
  {
    t0: 37.0, t1: 45.0,
    reporte: 'Hay una bomba que vibra mucho en glicol',
    sinTag: true,
    candidatos: ['1105-P-01', '1105-P-02', '1405-P-03'],
  },
];
P01_CASOS.forEach(c => {
  c.tType = c.t0 + 0.25 + c.reporte.length / 34;
  c.tId = c.tType + 0.5;
  if (c.sinTag) return;
  c.tTools = c.tools.map((_, i) => c.tId + 1.3 + i * TOOL_GAP);
  c.tIso = c.tTools[3];
  c.tSol = c.tIso + 1.9;
  c.tAprob = c.tSol + 2.4;
  c.hiNodes = new Set([c.tag, ...c.valvulas, ...c.fuera, ...c.recorrido.flat()]);
  c.hiEdges = new Set(c.recorrido.map(([a, b]) => p01Key(a, b)));
});

const P01_C = { teal: '#00a884', deep: '#0f766e', ink: '#111b21', dim: '#54655d', faint: '#869aa0', sage: '#9db8ac', amber: '#b45309', amberBg: '#fff8e6', tint: '#ccfbf1' };
const P01_MONO = 'IBM Plex Mono';

function p01Caso(t) { return P01_CASOS.find(c => t >= c.t0 && t < c.t1); }

function P01SystemDemo() {
  return (
    <Stage width={1280} height={720} duration={45} background="transparent" persistKey="p01-system" autoplay={true}>
      <div style={{ position: 'absolute', inset: 0, background: 'radial-gradient(900px 600px at 30% 30%, rgba(0,168,132,0.10), transparent 60%), radial-gradient(700px 500px at 80% 80%, rgba(0,168,132,0.08), transparent 60%), #ffffff' }}/>
      <P01TopBar/>
      <P01GraphCanvas/>
      <P01AgentPanel/>
    </Stage>
  );
}

function P01TopBar() {
  const t = useTime();
  const c = p01Caso(t);
  const nodos = P01_NODES.filter(n => t >= n.t).length;
  const tramos = P01_EDGES.filter(e => !e.inst && t >= e.t).length;
  return (
    <div style={{ position: 'absolute', top: 0, left: 0, right: 0, height: 60, padding: '0 28px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', borderBottom: '1px solid rgba(17,27,33,0.06)', background: 'rgba(255,255,255,0.6)' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
        <span style={{ width: 10, height: 10, borderRadius: 5, background: P01_C.teal, boxShadow: `0 0 12px ${P01_C.teal}`, animation: 'p-pulse-dot 1.4s ease-in-out infinite' }}/>
        <span style={{ fontFamily: P01_MONO, fontSize: 12, color: P01_C.dim, letterSpacing: '0.06em', textTransform: 'uppercase' }}>{P01_L('grafo de planta · agente', 'plant graph · agent')}</span>
        <span style={{ color: P01_C.faint }}>·</span>
        <span style={{ fontFamily: P01_MONO, fontSize: 12, color: P01_C.deep }}>{nodos} {P01_L('nodos en vista', 'nodes in view')} · {tramos} {P01_L('tramos de línea', 'line segments')}</span>
      </div>
      <div style={{ fontFamily: P01_MONO, fontSize: 12, color: c ? P01_C.ink : P01_C.faint, maxWidth: 560, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
        {c ? `↳ «${c.reporte}»` : (t < 6 ? P01_L('cargando la topología desde planta-core…', 'loading the topology from planta-core…') : '')}
      </div>
    </div>
  );
}

// Símbolos P&ID simplificados
function P01Valve({ x, y, fill, size = 7 }) {
  const s = size;
  return <path d={`M ${x - s} ${y - s * 0.72} L ${x} ${y} L ${x - s} ${y + s * 0.72} Z M ${x + s} ${y - s * 0.72} L ${x} ${y} L ${x + s} ${y + s * 0.72} Z`} fill={fill} stroke={fill} strokeWidth="1" strokeLinejoin="round"/>;
}

function P01Node({ n, t, c }) {
  const iso = c && !c.sinTag && t >= c.tIso;
  const cerrada = iso && t >= c.tIso + 0.9 && c.valvulas.includes(n.id);
  const fuera = iso && t >= c.tIso + 1.1 && c.fuera.includes(n.id);
  const foco = c && !c.sinTag && t >= c.tId && n.id === c.tag;
  const clase = c && !c.sinTag && t >= c.tTools[2] && t < c.tSol + 0.6 && c.clase.includes(n.id);
  const candidato = c && c.sinTag && t >= c.tId && c.candidatos.includes(n.id);
  const activo = c && t >= (c.sinTag ? c.tId : c.tId);
  const resaltado = foco || cerrada || fuera || clase || candidato || (c && !c.sinTag && iso && c.hiNodes.has(n.id));
  const opacity = activo ? (resaltado ? 1 : 0.24) : 1;
  const label = n.k === 'lim' ? P01_L(...P01_LIM_LABEL[n.id]) : P01_SHORT(n.id);
  const labelCol = foco || cerrada ? P01_C.ink : (fuera || candidato) ? P01_C.amber : P01_C.dim;
  const bold = foco || cerrada || fuera;
  let body;
  if (n.k === 'eq') {
    const r = n.crit ? 11 : 9;
    body = (
      <>
        {foco && (
          <circle cx={n.x} cy={n.y} r={20} fill="none" stroke={P01_C.teal} strokeWidth="1.6">
            <animate attributeName="r" values="14;30;14" dur="2s" repeatCount="indefinite"/>
            <animate attributeName="opacity" values="0.8;0;0.8" dur="2s" repeatCount="indefinite"/>
          </circle>
        )}
        {clase && <circle cx={n.x} cy={n.y} r={r + 6} fill="none" stroke={P01_C.deep} strokeWidth="1.4" strokeDasharray="3 3"/>}
        {candidato && <circle cx={n.x} cy={n.y} r={r + 7} fill="none" stroke={P01_C.amber} strokeWidth="1.5" strokeDasharray="4 3"/>}
        {fuera && <circle cx={n.x} cy={n.y} r={r + 6} fill="none" stroke={P01_C.amber} strokeWidth="1.5" strokeDasharray="4 3"/>}
        <circle cx={n.x} cy={n.y} r={r} fill={fuera ? '#eef2f0' : n.crit ? P01_C.teal : '#8fbfb1'} stroke={fuera ? P01_C.amber : P01_C.deep} strokeWidth={foco ? 2.6 : 1.4}/>
        {candidato && <text x={n.x} y={n.y + 4} textAnchor="middle" fontFamily={P01_MONO} fontSize="11" fontWeight="700" fill="#fff">?</text>}
      </>
    );
  } else if (n.k === 'hv') {
    body = (
      <>
        {cerrada && <circle cx={n.x} cy={n.y} r={13} fill="rgba(180,83,9,0.12)" stroke={P01_C.amber} strokeWidth="1.2"/>}
        <P01Valve x={n.x} y={n.y} fill={cerrada ? P01_C.amber : P01_C.dim}/>
      </>
    );
  } else if (n.k === 'pcv') {
    const col = fuera ? P01_C.amber : P01_C.faint;
    body = (
      <>
        {fuera && <circle cx={n.x} cy={n.y - 3} r={14} fill="none" stroke={P01_C.amber} strokeWidth="1.5" strokeDasharray="4 3"/>}
        <line x1={n.x} y1={n.y} x2={n.x} y2={n.y - 10} stroke={col} strokeWidth="1.4"/>
        <path d={`M ${n.x - 6} ${n.y - 10} A 6 6 0 0 1 ${n.x + 6} ${n.y - 10} Z`} fill={col}/>
        <P01Valve x={n.x} y={n.y} fill={col}/>
      </>
    );
  } else if (n.k === 'pt') {
    body = (
      <>
        <circle cx={n.x} cy={n.y} r={8} fill="#fff" stroke={P01_C.dim} strokeWidth="1.2"/>
        <text x={n.x} y={n.y + 3} textAnchor="middle" fontFamily={P01_MONO} fontSize="7" fill={P01_C.dim}>PT</text>
      </>
    );
  } else if (n.k === 'hdr') {
    body = <circle cx={n.x} cy={n.y} r={3.5} fill={P01_C.sage}/>;
  } else {
    body = <path d={`M ${n.x - 7} ${n.y - 6} L ${n.x + 3} ${n.y - 6} L ${n.x + 8} ${n.y} L ${n.x + 3} ${n.y + 6} L ${n.x - 7} ${n.y + 6} Z`} fill="#fff" stroke={P01_C.dim} strokeWidth="1.2"/>;
  }
  const dy = n.k === 'eq' ? (n.crit ? 25 : 23) : n.k === 'pt' ? 0 : n.k === 'hdr' ? 0 : 19;
  const dx = n.k === 'pt' ? 12 : 0;
  return (
    // la opacidad de foco va en el grupo exterior; la animación de entrada, en el interior, para que su
    // estado final (opacidad 1) no anule la atenuación de los nodos que no participan
    <g opacity={opacity} style={{ transition: 'opacity 0.45s' }}>
      <g style={{ animation: 'p-line-in .35s ease-out both' }}>
        {body}
        {label && (
          <text x={n.x + dx} y={n.y + (n.k === 'pt' ? 3 : dy)} fontFamily={P01_MONO} fontSize={n.k === 'eq' ? 12 : 10}
                fontWeight={bold ? 700 : n.k === 'eq' ? 600 : 400} fill={labelCol} textAnchor={n.k === 'pt' ? 'start' : 'middle'}>{label}</text>
        )}
      </g>
    </g>
  );
}

function P01GraphCanvas() {
  const t = useTime();
  const c = p01Caso(t);
  const iso = c && !c.sinTag && t >= c.tIso;
  const activo = c && t >= c.tId;
  const nodos = P01_NODES.filter(n => t >= n.t);
  const aristas = P01_EDGES.filter(e => t >= e.t);
  const legend = [
    [<circle cx="6" cy="6" r="5" fill={P01_C.teal}/>, P01_L('equipo', 'equipment')],
    [<P01Valve x={6} y={6} fill={P01_C.dim} size={5}/>, P01_L('válvula de bloqueo', 'block valve')],
    [<P01Valve x={6} y={6} fill={P01_C.amber} size={5}/>, P01_L('se cierra', 'to close')],
    [<circle cx="6" cy="6" r="4.5" fill="#eef2f0" stroke={P01_C.amber} strokeDasharray="2 2"/>, P01_L('fuera de servicio', 'out of service')],
  ];
  return (
    <div style={{ position: 'absolute', left: 28, top: 80, bottom: 28, width: 784, background: 'rgba(255,255,255,0.45)', border: '1px solid rgba(17,27,33,0.06)', borderRadius: 14, overflow: 'hidden' }}>
      <div style={{ padding: '10px 18px', borderBottom: '1px solid rgba(17,27,33,0.06)', display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: 16, whiteSpace: 'nowrap' }}>
        <span style={{ fontFamily: P01_MONO, fontSize: 11, color: P01_C.dim, letterSpacing: '0.1em', textTransform: 'uppercase' }}>
          {P01_L('grafo de proceso', 'process graph')}
        </span>
        <div style={{ display: 'flex', gap: 14, fontFamily: P01_MONO, fontSize: 10.5 }}>
          {legend.map(([sym, txt], i) => (
            <span key={i} style={{ display: 'flex', alignItems: 'center', gap: 5, color: P01_C.dim }}>
              <svg width="12" height="12" viewBox="0 0 12 12">{sym}</svg>{txt}
            </span>
          ))}
        </div>
      </div>
      <svg viewBox="0 0 1000 700" style={{ width: '100%', height: 'calc(100% - 42px)' }} xmlns="http://www.w3.org/2000/svg">
        {[[10, '1105 · ' + P01_L('deshidratación con TEG', 'TEG dehydration')], [510, '1205 · ' + P01_L('compresión de gas', 'gas compression')]].map(([x, txt]) => (
          <g key={x} opacity={t > 0.2 ? 1 : 0} style={{ transition: 'opacity .5s' }}>
            <rect x={x} y={34} width={480} height={652} rx={14} fill="rgba(0,168,132,0.025)" stroke={P01_C.deep} strokeOpacity="0.5" strokeWidth="1" strokeDasharray="6 4"/>
            <text x={x + 4} y={24} fontFamily={P01_MONO} fontSize="11" letterSpacing="0.08em" fill={P01_C.deep}>{txt.toUpperCase()}</text>
          </g>
        ))}
        <g>
          {aristas.map((e) => {
            const a = P01_NODE[e.a], b = P01_NODE[e.b];
            const pts = [[a.x, a.y], ...(e.via || []), [b.x, b.y]];
            const d = 'M ' + pts.map(p => p.join(' ')).join(' L ');
            const hi = iso && c.hiEdges.has(e.key);
            const dim = activo && !hi;
            return (
              <g key={e.key + (e.inst ? 'i' : '')} opacity={dim ? 0.22 : 1} style={{ transition: 'opacity .45s' }}>
                <path d={d} fill="none" stroke={hi ? P01_C.teal : P01_C.sage} strokeWidth={hi ? 2.8 : e.inst ? 1 : 1.7}
                      strokeDasharray={e.inst ? '2 3' : undefined} strokeLinejoin="round" style={{ animation: 'p-line-in .4s ease-out both' }}/>
                {hi && (
                  <circle r="3.2" fill={P01_C.teal}>
                    <animateMotion dur="1.6s" repeatCount="indefinite" path={d}/>
                  </circle>
                )}
              </g>
            );
          })}
        </g>
        <g>{nodos.map(n => <P01Node key={n.id} n={n} t={t} c={c}/>)}</g>
      </svg>
    </div>
  );
}

const P01_K = { fontFamily: P01_MONO, fontSize: 10, color: P01_C.deep, letterSpacing: '0.1em', textTransform: 'uppercase', fontWeight: 600, marginBottom: 6 };

function P01AgentPanel() {
  const t = useTime();
  const c = p01Caso(t);
  return (
    <div style={{ position: 'absolute', right: 28, top: 80, bottom: 28, left: 832, background: 'rgba(255,255,255,0.6)', border: '1px solid rgba(17,27,33,0.06)', borderRadius: 14, display: 'flex', flexDirection: 'column' }}>
      <div style={{ padding: '12px 18px', borderBottom: '1px solid rgba(17,27,33,0.06)' }}>
        <span style={{ fontFamily: P01_MONO, fontSize: 11, color: P01_C.dim, letterSpacing: '0.1em', textTransform: 'uppercase' }}>
          {P01_L('reporte · herramientas · solicitud', 'report · tools · request')}
        </span>
      </div>
      <div style={{ flex: 1, padding: '14px 18px', overflow: 'hidden', display: 'flex', flexDirection: 'column', gap: 14 }}>
        {!c && (
          <div style={{ color: P01_C.faint, fontSize: 13, fontStyle: 'italic', textAlign: 'center', marginTop: 90, lineHeight: 1.7 }}>
            ▸ {P01_L('construyendo el grafo…', 'building the graph…')}<br/>
            {t < 6 && P01_L('equipos, líneas y válvulas de las cadenas de línea de planta-core', 'equipment, lines and valves from the planta-core line chains')}
          </div>
        )}
        {c && <P01Caso c={c} t={t}/>}
      </div>
    </div>
  );
}

function P01Caso({ c, t }) {
  const chars = Math.max(0, Math.min(c.reporte.length, Math.floor((t - c.t0 - 0.25) * 34)));
  const typing = chars < c.reporte.length;
  return (
    <>
      <div>
        <div style={P01_K}>{P01_L('reporte de falla', 'fault report')}</div>
        <div style={{ fontSize: 14, lineHeight: 1.5, color: P01_C.ink, background: '#f6f8f7', border: '1px solid rgba(17,27,33,0.08)', borderRadius: 8, padding: '10px 12px', minHeight: 44 }}>
          «{c.reporte.slice(0, chars)}{typing && <span style={{ display: 'inline-block', width: 7, height: 15, background: P01_C.teal, verticalAlign: '-3px', marginLeft: 1, animation: 'p-caret 1s steps(2) infinite' }}/>}{!typing && '»'}
        </div>
      </div>
      {t >= c.tId && (
        <div style={{ animation: 'p-msg-in .4s ease-out both' }}>
          <div style={P01_K}>1 · {P01_L('identificar', 'identify')}</div>
          {c.sinTag ? (
            <div style={{ fontSize: 12.5, lineHeight: 1.6, color: P01_C.ink }}>
              <div style={{ fontFamily: P01_MONO, color: P01_C.amber, fontWeight: 600 }}>{P01_L('sin tag legible en el reporte', 'no legible tag in the report')}</div>
              <div style={{ marginTop: 4 }}>{P01_L('candidatos por descripción:', 'candidates by description:')} <span style={{ fontFamily: P01_MONO }}>{c.candidatos.join(' · ')}</span></div>
              <div style={{ marginTop: 12, padding: '10px 12px', borderRadius: 8, background: P01_C.amberBg, color: P01_C.amber, fontSize: 13, lineHeight: 1.55, animation: 'p-msg-in .4s ease-out .5s both' }}>
                {P01_L('NO RESUELTA · el sistema no elige el equipo: pide al reportante el tag de la placa.', 'NOT RESOLVED · the system does not pick the equipment: it asks the reporter for the nameplate tag.')}
              </div>
            </div>
          ) : (
            <div style={{ fontFamily: P01_MONO, fontSize: 12, lineHeight: 1.75, color: P01_C.ink }}>
              <div>«{c.escrito}» → <b style={{ color: P01_C.deep }}>{c.tag}</b> <span style={{ color: P01_C.faint }}>· {P01_L('regla de normalización', 'normalization rule')}</span></div>
              <div>{P01_L('síntoma', 'symptom')} → <b style={{ color: P01_C.deep }}>{c.modo}</b> <span style={{ color: P01_C.faint }}>· {P01_L(...c.modoNombre)} (ISO 14224)</span></div>
            </div>
          )}
        </div>
      )}
      {!c.sinTag && t >= c.tTools[0] && (
        <div>
          <div style={P01_K}>2 · {P01_L('herramientas · el agente no calcula', 'tools · the agent does not compute')}</div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
            {c.tools.map(([fn, out], i) => t >= c.tTools[i] && (
              <div key={i} style={{ animation: 'p-msg-in .35s ease-out both' }}>
                <div style={{ fontFamily: P01_MONO, fontSize: 11.5, color: P01_C.deep }}>
                  <span style={{ color: t >= c.tTools[i] + 0.6 ? P01_C.teal : P01_C.faint }}>{t >= c.tTools[i] + 0.6 ? '✓' : '…'}</span> {fn}
                </div>
                {t >= c.tTools[i] + 0.6 && <div style={{ fontSize: 12, lineHeight: 1.45, color: P01_C.dim, paddingLeft: 16, animation: 'p-line-in .3s ease-out both' }}>{P01_L(...out)}</div>}
              </div>
            ))}
          </div>
        </div>
      )}
      {!c.sinTag && t >= c.tSol && <P01Solicitud c={c} t={t}/>}
    </>
  );
}

function P01Solicitud({ c, t }) {
  const aprobada = t >= c.tAprob;
  const filas = [
    [P01_L('intervención', 'intervention'), c.sol.intervencion],
    [P01_L('aislamiento', 'isolation'), P01_L(...c.sol.aislamiento)],
    [P01_L('permisos', 'permits'), P01_L(...c.sol.permisos)],
    [P01_L('cuadrilla', 'crew'), P01_L(...c.sol.cuadrilla)],
    [P01_L('duración', 'duration'), P01_L(...c.sol.duracion)],
  ];
  return (
    <div style={{ border: `1px solid ${aprobada ? 'rgba(0,168,132,0.45)' : 'rgba(180,83,9,0.35)'}`, borderRadius: 10, padding: '10px 12px', background: '#fff', animation: 'p-msg-in .4s ease-out both', transition: 'border-color .4s' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 }}>
        <span style={{ ...P01_K, marginBottom: 0 }}>3 · {P01_L('solicitud de entrega', 'handover request')}</span>
        <span style={{ fontFamily: P01_MONO, fontSize: 10, letterSpacing: '0.08em', padding: '3px 8px', borderRadius: 999, fontWeight: 700,
                       background: aprobada ? P01_C.tint : P01_C.amberBg, color: aprobada ? P01_C.deep : P01_C.amber }}>
          {aprobada ? P01_L('APROBADA', 'APPROVED') : P01_L('BORRADOR', 'DRAFT')}
        </span>
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: '92px 1fr', rowGap: 5, columnGap: 10 }}>
        {filas.map(([k, v]) => (
          <React.Fragment key={k}>
            <span style={{ fontFamily: P01_MONO, fontSize: 9.5, color: P01_C.faint, textTransform: 'uppercase', letterSpacing: '0.06em', paddingTop: 2 }}>{k}</span>
            <span style={{ fontSize: 12, lineHeight: 1.45, color: P01_C.ink }}>{v}</span>
          </React.Fragment>
        ))}
      </div>
      <div style={{ marginTop: 9, paddingTop: 8, borderTop: '1px dashed rgba(17,27,33,0.12)', fontFamily: P01_MONO, fontSize: 10.5, color: aprobada ? P01_C.deep : P01_C.amber }}>
        {aprobada
          ? P01_L('✓ aprobada por el ingeniero de turno · nombre y fecha registrados', '✓ approved by the shift engineer · name and date recorded')
          : P01_L('esperando aprobación humana · sin ella no se emite', 'waiting for human approval · not issued without it')}
      </div>
    </div>
  );
}

Object.assign(window, { P01TerminalDemo, P01SystemDemo });
