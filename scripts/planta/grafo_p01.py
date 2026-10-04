"""Escribe P01_NODES / P01_EDGES en projects/p01.jsx desde la topología real de planta-core.

Las coordenadas son de diseño (1000×560, estiradas a un lienzo de 1000×700); las aristas salen de planta_core.planta.LINEAS
restringidas a las áreas 1105 y 1205, así que la animación no dibuja ninguna tubería que no exista.
Falla si la topología tiene un nodo sin coordenadas o si sobra alguna coordenada.

Uso:  python scripts/planta/grafo_p01.py          (planta-core como carpeta hermana de ai-portfolio)
      PLANTA_CORE=/ruta/a/planta-core python scripts/planta/grafo_p01.py
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CORE = Path(os.environ.get("PLANTA_CORE", ROOT.parent / "planta-core"))
sys.path.insert(0, str(CORE))
from planta_core import planta  # noqa: E402

JSX = ROOT / "projects" / "p01.jsx"
AREAS = ("1105", "1205")
EXTRA = {"LIM-GAS-ENTRADA", "LIM-GAS-EXPORTACION", "HDR-1105-SUC", "HDR-1105-DES", "HDR-1205-SUC", "HDR-1205-DES", "HDR-1205-ACE"}

POS = {
    # 1105 · deshidratación con TEG
    "LIM-GAS-ENTRADA": (30, 80), "1105-HV-01": (78, 80), "1105-V-01": (130, 80), "1105-PT-01": (130, 46),
    "1105-HV-02": (186, 80), "1105-V-02": (262, 110), "1105-PT-02": (300, 150), "1105-HV-03": (352, 80),
    "1105-HV-05": (262, 170), "1105-PCV-01": (262, 225), "1105-V-03": (262, 285), "1105-HV-06": (325, 285),
    "1105-E-01": (390, 285), "1105-HV-07": (452, 285), "1105-V-04": (452, 350), "1105-V-05": (452, 420),
    "1105-HV-08": (390, 350), "1105-HV-04": (325, 350), "HDR-1105-SUC": (262, 400), "1105-HV-09": (205, 385),
    "1105-P-01": (150, 385), "1105-HV-10": (95, 385), "HDR-1105-DES": (45, 430), "1105-HV-11": (205, 470),
    "1105-P-02": (150, 470), "1105-HV-12": (95, 470), "1105-E-02": (45, 300), "1105-HV-13": (120, 190),
    # 1205 · compresión
    "1205-HV-01": (540, 80), "1205-V-01": (600, 80), "1205-PT-01": (600, 46), "HDR-1205-SUC": (660, 140),
    "1205-HV-02": (715, 110), "1205-C-01": (780, 110), "1205-HV-03": (845, 110), "1205-HV-04": (715, 185),
    "1205-C-02": (780, 185), "1205-HV-05": (845, 185), "HDR-1205-DES": (905, 145), "1205-E-01": (945, 225),
    "1205-V-02": (945, 300), "1205-PT-02": (905, 322), "1205-HV-06": (945, 370), "LIM-GAS-EXPORTACION": (945, 425),
    "1205-PCV-01": (845, 255), "1205-HV-07": (715, 255), "1205-V-03": (575, 458), "1205-HV-08": (635, 420),
    "1205-P-01": (700, 420), "1205-HV-09": (765, 420), "HDR-1205-ACE": (825, 458), "1205-HV-11": (635, 495),
    "1205-P-02": (700, 495), "1205-HV-12": (765, 495), "1205-E-02": (880, 458), "1205-HV-10": (880, 530),
}
VIA = {("1205-HV-10", "1205-V-03"): [[575, 530]]}  # retorno de aceite por debajo, sin cruzar las bombas
# El lienzo de la animación es 1000×700 (la proporción del panel); las coordenadas de diseño se estiran en vertical.
Y0, ESCALA_Y = 34, 1.26


def y_lienzo(y: float) -> int:
    return round(Y0 + (y - Y0) * ESCALA_Y)


def en_vista(n: str) -> bool:
    return n[:4] in AREAS or n in EXTRA


def tipo(n: str) -> str:
    return {"HDR": "hdr", "LIM": "lim", "HV": "hv", "PCV": "pcv", "PT": "pt"}.get(planta.tipo_de(n), "eq")


def main() -> None:
    nodos = {n for c in planta.LINEAS for n in c if en_vista(n)} | {t for t in planta.INSTRUMENTOS if t[:4] in AREAS}
    faltan, sobran = sorted(nodos - set(POS)), sorted(set(POS) - nodos)
    if faltan or sobran:
        raise SystemExit(f"coordenadas desalineadas con planta-core · faltan {faltan} · sobran {sobran}")
    out = []
    for n in sorted(nodos, key=lambda n: (POS[n][0] > 500, POS[n][1], POS[n][0])):
        d = {"id": n, "k": tipo(n), "x": POS[n][0], "y": y_lienzo(POS[n][1])}
        if n in planta.EQUIPOS:
            d["crit"] = int(planta.EQUIPOS[n][2])
        out.append(d)
    aristas = [{"a": a, "b": b, **({"via": [[x, y_lienzo(y)] for x, y in VIA[(a, b)]]} if (a, b) in VIA else {})}
               for a, b in planta.conexiones() if en_vista(a) and en_vista(b)]
    aristas += [{"a": pt, "b": eq, "inst": 1} for pt, eq in planta.INSTRUMENTOS.items() if pt[:4] in AREAS]
    bloque = ("// <grafo:inicio> generado por scripts/planta/grafo_p01.py desde planta-core; no editar a mano\n"
              f"const P01_NODES = {json.dumps(out, ensure_ascii=False)};\n"
              f"const P01_EDGES = {json.dumps(aristas, ensure_ascii=False)};\n// <grafo:fin>")
    src = JSX.read_text(encoding="utf-8")
    nuevo, n = re.subn(r"// <grafo:inicio>.*?// <grafo:fin>", lambda _m: bloque, src, flags=re.S)
    if n != 1:
        raise SystemExit("projects/p01.jsx: no se encontró el bloque <grafo:inicio> … <grafo:fin>")
    JSX.write_text(nuevo, encoding="utf-8")
    print(f"p01.jsx: {len(out)} nodos · {sum('inst' not in e for e in aristas)} tramos · {sum('inst' in e for e in aristas)} instrumentos")


if __name__ == "__main__":
    main()
