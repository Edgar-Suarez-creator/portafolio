"""Especificación del diagrama de cada proyecto, derivada del código de su repositorio.

Every box is a real module or LangGraph node; every arrow is an edge or a
conditional edge that exists in the code. Labels are plain language, in
Spanish and English (``("es", "en")``), without function names or formulas.
The comment above each spec cites where in the code each element comes from.
"""

from __future__ import annotations

from gen_diagrams import Edge, Group, Node, Spec

N = Node
E = Edge

SPECS: dict[str, Spec] = {}

# ----------------------------------------------------------------------------- 01 · P1 asistente de planta
# p1-asistente-planta (main)
#   carga: planta-core/datos (topología, catálogos ISO 14224, historial, documentos) → src/asistente/grafo.py GrafoPlanta
#          · extraccion.extraer (Pydantic, documento y página) · normalizacion.ResolutorTags (reglas + similitud → conflictos)
#          · aislamientos.calcular_aislamiento materializado como AISLA · exportar_cypher → neo4j/planta.cypher
#   consulta: agente.Agente.atender (ResolutorTags + SINTOMAS → modo ISO 14224) | consulta.MotorConsultas.responder
#             (clasificar → plantillas Cypher sobre el grafo | TF-IDF sobre manuales) → herramientas.Herramientas
#             (buscar_equipo · historial · fallas_similares · aislamientos) → plantilla Solicitud → aprobar → emitir
#   pendiente: generación de Cypher con LLM (ANTHROPIC_API_KEY)
SPECS["01"] = Spec(
    explain=(
        "Dos fases. Carga: la planta de referencia (topología, códigos ISO 14224, historial de órdenes y documentos) "
        "entra a un grafo; las propiedades de las hojas de datos se extraen con la cita de documento y página, y los "
        "tags mal escritos se resuelven por reglas y similitud o van a un reporte de conflictos. Consulta: de un "
        "reporte o una pregunta se identifican el equipo y el modo de falla; cuatro herramientas deterministas leen el "
        "grafo y una plantilla redacta la respuesta o el borrador de solicitud, que solo se emite con aprobación "
        "humana. Las preguntas documentales van a los manuales; la generación de Cypher con modelo de lenguaje para "
        "redacción libre está pendiente de llave.",
        "Two phases. Load: the reference plant (topology, ISO 14224 codes, work-order history and documents) goes "
        "into a graph; datasheet properties are extracted with the document and page citation, and misspelled tags "
        "are resolved by rules and similarity or sent to a conflict report. Query: from a report or a question the "
        "equipment and failure mode are identified; four deterministic tools read the graph and a template drafts the "
        "answer or the request draft, which is only issued with human approval. Document questions go to the "
        "manuals; Cypher generation with a language model for free wording is pending a key.",
    ),
    rows=[
        [
            N("core", ("Planta de referencia", "Reference plant"),
              [("topología · ISO 14224 · órdenes · documentos", "topology · ISO 14224 · orders · documents")], "input"),
            N("extract", ("Extraer propiedades con cita", "Extract properties with citation"),
              [("Pydantic · documento y página", "Pydantic · document and page")], "rule"),
            N("norm", ("Resolver tags mal escritos", "Resolve misspelled tags"),
              [("reglas + similitud → conflictos", "rules + similarity → conflicts")], "rule"),
            N("graph", ("Grafo de la planta", "Plant graph"),
              [("memoria · exportable a Neo4j", "in memory · exportable to Neo4j"),
               ("aislamientos como relación AISLA", "isolations as an ISOLATES relation")], "store"),
        ],
        [
            N("in", ("Reporte o pregunta", "Report or question"),
              [("texto libre", "free text")], "input"),
            N("ident", ("Identificar equipo y modo", "Identify equipment and mode"),
              [("tag · modo ISO 14224 · tipo de pregunta", "tag · ISO 14224 mode · question type")], "rule"),
            N("tools", ("Cuatro herramientas", "Four tools"),
              [("ficha · historial · similares · aislamientos", "sheet · history · similar · isolations")], "tool"),
            N("draft", ("Redactar con citas", "Draft with citations"),
              [("plantilla de campos fijos", "fixed-field template")], "rule"),
        ],
        [
            N("manual", ("Búsqueda en manuales", "Manual search"),
              [("TF-IDF · documento y página", "TF-IDF · document and page")], "tool", align="ident"),
            N("llm", ("Cypher con modelo de lenguaje", "Cypher with a language model"),
              [("redacción libre · pendiente de llave", "free wording · pending key")], "llm", align="tools"),
            N("approve", ("Aprobación humana", "Human approval"),
              [("nombre y fecha registrados", "name and date recorded")], "input", align="draft"),
        ],
        [
            N("out", ("Respuesta o solicitud emitida", "Answer or issued request"),
              [("cada dato con su orden, nodo o página", "each fact with its order, node or page")], "output", align="approve"),
        ],
    ],
    edges=[
        E("core", "extract"), E("extract", "norm"), E("norm", "graph"),
        E("graph", "tools", ("el grafo alimenta las herramientas", "the graph feeds the tools"), "alt"),
        E("in", "ident"), E("ident", "tools"), E("tools", "draft"),
        E("ident", "manual", ("pregunta documental", "document question"), "alt"),
        E("llm", "tools", ("pendiente", "pending"), "alt"),
        E("draft", "approve", ("solicitud", "request")),
        E("draft", "out", ("respuesta a pregunta", "answer to a question"), "alt"),
        E("approve", "out"), E("manual", "out"),
    ],
    groups=[Group(("CARGA · por lote de datos", "LOAD · per data batch"), ["core", "extract", "norm", "graph"]),
            Group(("CONSULTA · por reporte o pregunta", "QUERY · per report or question"), ["in", "ident", "tools", "draft"])],
)
