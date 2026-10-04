# Portafolio · Edgar Suárez

Planeación y control: ocho sistemas sobre una misma planta de referencia, una estación de compresión de gas
con cuatro unidades y tags ISA 5.1. Todos leen y escriben sobre los mismos tags.

## Serie planta de referencia

| # | Proyecto | Estado | Código |
|---|---|---|---|
| P1 | Asistente de planta sobre grafo de conocimiento | listo · demo y evaluación | `planta-core` + `p1-asistente-planta` |
| P2 | Digitalización de P&ID y definición de sistemas | en construcción | — |
| P3 | Agente de planeación de órdenes y control del backlog | en construcción | — |
| P4 | Motor de estrategia de confiabilidad | en construcción | — |
| P5 | Torre de control de materiales y repuestos | en construcción | — |
| P6 | Control de construcción y entrega por sistemas | en construcción | — |
| P7 | Aseguramiento de calidad en construcción | en construcción | — |
| P8 | Programa de preservación de equipos | en construcción | — |

## Ver el sitio en su computador

```bash
python -m http.server 8002
```

y abrir http://127.0.0.1:8002 . No requiere compilar nada: las páginas cargan React y Babel desde unpkg.

## Regenerar lo que sale del código

- Diagrama del sistema del P1: `python scripts/diagrams/gen_diagrams.py 01` (especificación en `scripts/diagrams/specs.py`).
- Grafo de la animación del P1, desde la topología real de `planta-core`: `python scripts/planta/grafo_p01.py`
  (espera `planta-core` como carpeta hermana o la variable `PLANTA_CORE`).

## Pendiente de completar con sus datos

- Foto: hoy hay un círculo con las iniciales (`index.html`, bloque `hero-photo`).
- Sobre mí: el recuadro marcado como «Pendiente».
- Experiencia y formación: un bloque de ejemplo en cada sección para copiar por cada cargo o título.
- Contacto: correo y LinkedIn.

## Créditos y licencia

El diseño y los componentes del sitio (`projects/_styles.css`, `projects/animations.jsx`, `projects/_shared.jsx`,
`scripts/diagrams/gen_diagrams.py` y la estructura y estilos de `index.html`) provienen de la plantilla
*ai-portfolio* de Juan David Suárez Sánchez, publicada con licencia MIT; su aviso se conserva en `LICENSE`.
El contenido del portafolio y los proyectos de la serie planta son de Edgar Suárez.
