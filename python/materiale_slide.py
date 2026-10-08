"""Slide dei capitoli: copia i PDF sul sito e scrive la sezione «Le slide»
della pagina del materiale (it: docs/materiale.md, en: docs/downloads.md).

Le slide stanno in slides/<nome>/<nome>.tex (it/slides e en/slides), una
cartella per gruppo di slide, compilate lì; sul sito va solo il PDF.
La sezione è fra i segnaposto <!-- slide:inizio --> e <!-- slide:fine -->.

Uso: python3 python/materiale_slide.py     (fa italiano e inglese)
"""
import re
import shutil
from pathlib import Path

RADICE = Path(__file__).resolve().parents[2]

# (titolo del gruppo it, en), [(nome it, nome en, titolo it, titolo en)]
GRUPPI = [
    (("Modellazione", "Modelling"), [
        ("slide-01-modelli-mip", "slides-01-mip-models", "Che cos'è un modello MIP", "What is a MIP model"),
        ("slide-02-bound-duali", "slides-02-dual-bounds", "Rilassamenti, dualità e bound", "Relaxations, duality and bounds"),
        ("slide-03-gurobi", "slides-03-gurobi", "Dal modello a Python/Gurobi", "From the model to Python/Gurobi"),
        ("slide-04-euristiche", "slides-04-heuristics", "Euristiche costruttive", "Constructive heuristics"),
        ("slide-05-logica-binarie", "slides-05-logic-binaries", "Logica e variabili binarie", "Logic and binary variables"),
        ("slide-06-legami", "slides-06-links", "Legami fra variabili", "Links between variables"),
    ]),
    (("Problemi numerici", "Numerical problems"), [
        ("slide-07-modelli-numerici-1", "slides-07-numerical-models-1", "Modelli numerici: EX 1–5", "Numerical models: EX 1–5"),
        ("slide-07-modelli-numerici-2", "slides-07-numerical-models-2", "Modelli numerici: EX 6–10", "Numerical models: EX 6–10"),
        ("slide-07-modelli-numerici-3", "slides-07-numerical-models-3", "Modelli numerici: EX 11–15", "Numerical models: EX 11–15"),
    ]),
    (("Problemi con modello simbolico", "Problems with a symbolic model"), [
        ("slide-08-famiglie", "slides-08-problem-families", "Le famiglie di problemi", "The problem families"),
        ("slide-09-scheduling", "slides-09-scheduling", "Assegnamento e scheduling", "Assignment and scheduling"),
        ("slide-10-localizzazione", "slides-10-location", "Localizzazione e copertura", "Location and coverage"),
        ("slide-11-produzione", "slides-11-production", "Pianificazione della produzione", "Production planning"),
        ("slide-12-problemi-misti-1", "slides-12-mixed-problems-1", "Problemi misti: 10.1–10.3", "Mixed problems: 10.1–10.3"),
        ("slide-12-problemi-misti-2", "slides-12-mixed-problems-2", "Problemi misti: 10.4–10.6", "Mixed problems: 10.4–10.6"),
        ("slide-12-problemi-misti-3", "slides-12-mixed-problems-3", "Problemi misti: 10.7–10.9", "Mixed problems: 10.7–10.9"),
    ]),
]
PAGINA = {"it": "materiale.md", "en": "downloads.md"}
TESTO = {
    "it": ("## Le slide", "Le slide delle lezioni, una per capitolo delle dispense (PDF)."),
    "en": ("## Slides", "The lecture slides, one deck per chapter of the notes (PDF)."),
}


def sezione(lingua):
    k = 0 if lingua == "it" else 1
    repo = RADICE / lingua
    titolo, intro = TESTO[lingua]
    righe = ["<!-- slide:inizio -->", titolo, "", intro, "", '<div class="grid cards" markdown>', ""]
    n = 0
    for nome_gruppo, decks in GRUPPI:
        voci = []
        for d in decks:
            nome, tit = d[k], d[2 + k]
            pdf = repo / "slides" / nome / f"{nome}.pdf"
            if pdf.exists():
                shutil.copy(pdf, repo / "docs" / "pdf" / f"{nome}.pdf")
                voci.append(f"    - [{tit}](pdf/{nome}.pdf)")
                n += 1
        if voci:
            righe += [f"-   :material-presentation: **{nome_gruppo[k]}**", "", "    ---", ""] + voci + [""]
    righe += ["</div>", "", "<!-- slide:fine -->"]
    return "\n".join(righe), n


if __name__ == "__main__":
    for lingua in ("it", "en"):
        p = RADICE / lingua / "docs" / PAGINA[lingua]
        s = p.read_text()
        blocco, n = sezione(lingua)
        if "<!-- slide:inizio -->" in s:
            s = re.sub(r"<!-- slide:inizio -->.*?<!-- slide:fine -->", lambda m: blocco, s, flags=re.S)
        else:
            raise SystemExit(f"{p}: manca il segnaposto <!-- slide:inizio -->")
        p.write_text(s)
        print(f"[{lingua}] {p.name}: {n} gruppi di slide")
