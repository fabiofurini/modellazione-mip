"""Incorpora nelle pagine del sito i modelli simbolici delle dispense.

Il modello simbolico di un problema sta scritto una volta sola, nella dispensa,
dentro un ambiente `modello`. Qui lo si estrae, lo si traduce in quello che
MathJax sa leggere e lo si mette nella pagina fra due marcatori: il contenuto
fra i marcatori e' rigenerato, il resto della pagina non si tocca.

Cosi' dispensa e sito non possono divergere --- ed e' divergendo che il sito
aveva perso il formato: righe di dominio schiacciate, piu' vincoli per riga,
`\\forall` spariti.

Nella pagina si scrive soltanto il marcatore di apertura:

    <!-- modello: 7.1 -->          il modello del problema 7.1
    <!-- modello: 7.1-duale -->    il duale del suo rilassamento LP

Uso:  python3 incorpora_simbolici.py             # rigenera i blocchi
      python3 incorpora_simbolici.py --verifica  # controlla che siano aggiornati
"""
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DIR_DOCS = BASE / "docs"
DISPENSE = sorted(BASE.glob("dispensa_*/capitoli"))

APRE = re.compile(r"<!-- modello: ([0-9]+\.[0-9]+[A-Za-z]*(?:-duale)?) -->")
FINE = "<!-- modello: fine -->"

TITOLO = re.compile(r"\\begin\{modello\}\[([^\]]*)\]")


def _mathjax(corpo: str) -> str:
    """Il corpo di un ambiente `modello` come lo legge MathJax."""
    corpo = re.sub(r"\\label\{[^}]*\}", "", corpo)
    corpo = re.sub(r"\\(begin|end)\{subequations\}", "", corpo)
    corpo = re.sub(r"\\vskip\s+-?[0-9.]+\s*mm", "", corpo)
    corpo = corpo.replace("\\begin{align}", "\\begin{aligned}")
    corpo = corpo.replace("\\end{align}", "\\end{aligned}")
    corpo = corpo.replace("\\nonumber", "")
    corpo = re.sub(r"\\\\\[[0-9.]+ex\]", "\\\\\\\\", corpo)
    corpo = re.sub(r"@\{[^{}]*\}", "", corpo)      # MathJax non conosce @{} in array
    corpo = re.sub(r"[ \t]+$", "", corpo, flags=re.M)
    corpo = re.sub(r"\n{2,}", "\n", corpo)
    return corpo.strip()


def modelli() -> dict[str, str]:
    """`{"7.1": corpo, "7.1-duale": corpo, ...}` da tutte le dispense."""
    fuori = {}
    for cartella in DISPENSE:
        for f in sorted(cartella.rglob("*.tex")):
            testo = f.read_text(encoding="utf-8")
            for m in re.finditer(r"\\begin\{modello\}\[([^\]]*)\](.*?)\\end\{modello\}",
                                 testo, re.S):
                titolo, corpo = m.group(1), _mathjax(m.group(2))
                n = re.match(r"Modello ([0-9]+\.[0-9]+[A-Za-z]*)", titolo)
                if n:
                    fuori[n.group(1)] = corpo
                    continue
                d = re.match(r"Duale del rilassamento LP del modello "
                             r"([0-9]+\.[0-9]+[A-Za-z]*)", titolo)
                if d:
                    fuori[d.group(1) + "-duale"] = corpo
    return fuori


def aggiorna(verifica: bool) -> int:
    disponibili = modelli()
    cambiate, mancanti = [], []
    for pagina in sorted(DIR_DOCS.glob("*.md")):
        testo = pagina.read_text(encoding="utf-8")
        if not APRE.search(testo):
            continue
        nuovo = testo
        for m in list(APRE.finditer(testo)):
            nome = m.group(1)
            if nome not in disponibili:
                mancanti.append((pagina.name, nome))
                continue
            inizio = nuovo.index(m.group(0)) + len(m.group(0))
            fine = nuovo.index(FINE, inizio)
            corpo = f"\n\n$$\n{disponibili[nome]}\n$$\n\n"
            nuovo = nuovo[:inizio] + corpo + nuovo[fine:]
        if nuovo != testo:
            cambiate.append(pagina.name)
            if not verifica:
                pagina.write_text(nuovo, encoding="utf-8")
    for pagina, nome in mancanti:
        print(f"  [manca] {pagina}: nessun modello {nome} nelle dispense")
    if verifica:
        if cambiate or mancanti:
            print("Modelli simbolici non aggiornati: " + ", ".join(cambiate))
            return 1
        print("Modelli simbolici: pagine allineate alle dispense.")
        return 0
    print(f"  [modelli] {len(cambiate)} pagine aggiornate, "
          f"{len(disponibili)} modelli disponibili")
    return 1 if mancanti else 0


if __name__ == "__main__":
    sys.exit(aggiorna("--verifica" in sys.argv))
