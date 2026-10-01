"""Raccolta dei soli enunciati: i testi dei problemi, senza soluzione.

Serve per esercitarsi: gli stessi problemi della dispensa, nell'ordine dei
capitoli, ma senza modelli, bound e discussione. Si genera dai sorgenti della
dispensa --- non si scrive a mano --- cosi' resta allineato a ogni correzione.

Uso:  python3 genera_raccolta.py             # scrive dispensa/raccolta.tex
      python3 genera_raccolta.py --verifica  # controlla che sia aggiornata
"""
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DIR_CAPITOLI = BASE / "dispensa" / "capitoli"
USCITA = BASE / "dispensa" / "raccolta.tex"

# l'ordine dei capitoli e' quello di main.tex
ORDINE = [
    ("Modellazione", ["cap01_modelli_mip", "cap02_logica_binarie", "cap03_legami",
                      "cap04_bound_duali", "cap05_euristiche", "cap06_gurobi"]),
    ("I problemi", ["cap00_numerici", "cap07_scheduling", "cap08_localizzazione",
                    "cap09_produzione", "cap10_misti"]),
]

TITOLO_CAPITOLO = re.compile(r"\\chapter\*?\{([^}]*)\}")
PROBLEMA = re.compile(r"\\begin\{problema\}(\[[^\]]*\])?(.*?)\\end\{problema\}", re.S)
# i cinque esercizi di logica booleana del capitolo 2 sono enunciati a tutti gli
# effetti: entrano nella raccolta come gli altri
ESERCIZIO = re.compile(r"\\begin\{esercizio\}(\[[^\]]*\])?(.*?)\\end\{esercizio\}", re.S)


def sorgenti(nome: str):
    """Il file del capitolo piu' i suoi `\\input` (gli esercizi delle famiglie)."""
    principale = DIR_CAPITOLI / f"{nome}.tex"
    yield principale
    testo = principale.read_text(encoding="utf-8")
    for incluso in re.findall(r"\\input\{capitoli/([^}]+)\}", testo):
        percorso = DIR_CAPITOLI / f"{incluso.split('/', 1)[-1]}.tex" \
            if "/" not in incluso else DIR_CAPITOLI / f"{incluso}.tex"
        if percorso.exists():
            yield percorso


def enunciati(nome: str):
    """(titolo, corpo) di ogni `problema` del capitolo, nell'ordine del testo."""
    for percorso in sorgenti(nome):
        testo = percorso.read_text(encoding="utf-8")
        for regola in (PROBLEMA, ESERCIZIO):
            for m in regola.finditer(testo):
                titolo = (m.group(1) or "[]")[1:-1]
                yield titolo, m.group(2).strip()


def titolo_capitolo(nome: str) -> str:
    testo = (DIR_CAPITOLI / f"{nome}.tex").read_text(encoding="utf-8")
    m = TITOLO_CAPITOLO.search(testo)
    return m.group(1) if m else nome


def documento() -> str:
    righe = [
        "% Generato da python/genera_raccolta.py --- non si modifica a mano.",
        "\\documentclass[11pt,a4paper,oneside]{book}",
        "\\input{preambolo}",
        "\\title{Modellazione MIP --- raccolta degli enunciati}",
        "\\author{Fabio Furini}",
        "\\begin{document}",
        "\\begin{titlepage}",
        "  \\centering",
        "  \\vspace*{1.2cm}",
        "  \\href{https://www.diag.uniroma1.it/}{%",
        "    \\includegraphics[width=0.40\\textwidth]{figure/sapienza.jpeg}}\\\\[1.0cm]",
        "  {\\color{blunotte}\\rule{\\textwidth}{2pt}}\\\\[1.0cm]",
        "  {\\Huge\\bfseries\\color{blunotte} Raccolta degli enunciati\\par}",
        "  \\vspace{0.7cm}",
        "  {\\Large\\color{teal} Modellazione MIP --- i problemi del corso,\\\\"
        "senza soluzione\\par}",
        "  \\vspace{0.7cm}",
        "  {\\color{blunotte}\\rule{\\textwidth}{2pt}}\\\\[1.2cm]",
        "  \\begin{tcolorbox}[colback=tealchiaro,colframe=teal,width=0.86\\textwidth,arc=2mm]",
        "    \\small Gli stessi problemi della dispensa, nello stesso ordine, con i soli",
        "    testi: per esercitarsi prima di leggere la soluzione. Per ciascuno si chiede",
        "    il modello, il modello dell'istanza, un'euristica costruttiva con il suo",
        "    bound e il duale del rilassamento LP con una soluzione duale ammissibile.",
        "  \\end{tcolorbox}",
        "  \\vfill",
        "  {\\Large\\bfseries Fabio Furini\\par}",
        "  \\vspace{0.3cm}",
        "  {\\small Sapienza Universit\\`a di Roma --- A.A. 2026--2027\\par}",
        "\\end{titlepage}",
        "\\tableofcontents",
    ]
    quanti = 0
    for parte, capitoli in ORDINE:
        contenuto = [(c, list(enunciati(c))) for c in capitoli]
        contenuto = [(c, e) for c, e in contenuto if e]
        if not contenuto:
            continue
        righe.append(f"\\part{{{parte}}}")
        for capitolo, blocchi in contenuto:
            righe.append(f"\\chapter{{{titolo_capitolo(capitolo)}}}")
            for titolo, corpo in blocchi:
                quanti += 1
                apri = f"\\begin{{problema}}[{titolo}]" if titolo else "\\begin{problema}"
                righe += [apri, corpo, "\\end{problema}", ""]
    righe.append("\\end{document}")
    righe.insert(1, f"% {quanti} enunciati")
    return "\n".join(righe) + "\n"


def main(verifica: bool = False) -> int:
    nuovo = documento()
    vecchio = USCITA.read_text(encoding="utf-8") if USCITA.exists() else ""
    if verifica:
        if nuovo != vecchio:
            print("dispensa/raccolta.tex non e' aggiornata: rilanciare genera_raccolta.py")
            return 1
        print("Raccolta degli enunciati aggiornata.")
        return 0
    USCITA.write_text(nuovo, encoding="utf-8")
    print(f"Scritta {USCITA.relative_to(BASE)} "
          f"({nuovo.count(chr(92) + 'begin{problema}')} enunciati)")
    return 0


if __name__ == "__main__":
    sys.exit(main(verifica="--verifica" in sys.argv))
