"""Mette le voci dell'indice analitico nei sorgenti della dispensa.

Si lancia una volta sola: inserisce `\\index{...}` dopo la **prima** occorrenza
di ciascun termine in ciascuna sezione, saltando la matematica, il codice, i
titoli dei box e le etichette. Le voci gia' presenti non si duplicano.

Uso:  python3 it/python/strumenti/indicizza.py it     # dispensa italiana
      python3 it/python/strumenti/indicizza.py en     # notes inglesi
      python3 it/python/strumenti/indicizza.py --conta # quante voci ci sono adesso
"""
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[3]   # radice del modulo

# le tre dispense sono indipendenti, una cartella per volume
CARTELLE = {"it": [f"it/dispensa_{i}/capitoli" for i in (1, 2, 3)],
            "en": [f"en/notes_{i}/capitoli" for i in (1, 2, 3)]}

# termine dell'indice -> espressione che lo riconosce nel testo.
# L'ordine conta: i termini piu' lunghi vanno prima, cosi' «dualita' forte» non
# viene mangiato da «dualita'».
TERMINI_IT = [
    ("dualità forte", r"dualit\\`a forte|dualità forte"),
    ("dualità debole", r"dualit\\`a debole|dualità debole"),
    ("rilassamento lineare", r"rilassamento LP|rilassamento lineare"),
    ("branch-and-bound", r"branch-and-bound"),
    ("big-M", r"big-M"),
    ("bound primale", r"bound primale"),
    ("bound duale", r"bound duale"),
    ("euristica costruttiva", r"euristica costruttiva"),
    ("set covering", r"\\emph\{set covering\}|set covering"),
    ("set packing", r"\\emph\{set packing\}|set packing"),
    ("set partitioning", r"\\emph\{set partitioning\}|set partitioning"),
    ("variabile semicontinua", r"semicontinua"),
    ("disuguaglianze valide", r"disuguaglianze valide"),
    ("prezzo dell'interezza", r"prezzo dell'interezza"),
    ("argomento di scambio", r"argomento di scambio"),
    ("costo fisso", r"costo fisso"),
    ("lotto minimo", r"lotto minimo"),
    ("attivazione", r"attivazione"),
    ("precedenze", r"precedenze"),
    ("valore assoluto", r"valore assoluto"),
    ("funzione lineare a tratti", r"lineari a tratti|lineare a tratti"),
    ("espansione binaria", r"espansione binaria"),
    ("vincoli violabili", r"vincoli violabili"),
    ("variabile di massimo", r"variabile di massimo"),
    ("forma normale congiuntiva", r"forma normale congiuntiva"),
    ("prezzi marginali", r"prezzi marginali"),
    ("tolleranze", r"tolleranze"),
    ("certificato duale", r"certificato duale"),
    ("gap di integralità", r"gap certificato"),
    ("bilancio delle scorte", r"bilancio delle scorte|bilanci delle scorte"),
    ("localizzazione capacitata", r"localizzazione capacitata"),
    ("p-mediana", r"\$p\$-mediana|p-mediana"),
    ("asta combinatoria", r"asta combinatoria"),
    ("zaino", r"\\emph\{zaino\}|[Zz]aino binario|[Zz]aino intero"),
]

TERMINI_EN = [
    ("strong duality", r"strong duality"),
    ("weak duality", r"weak duality"),
    ("LP relaxation", r"LP relaxation"),
    ("branch-and-bound", r"branch-and-bound"),
    ("big-M", r"big-M"),
    ("primal bound", r"primal bound"),
    ("dual bound", r"dual bound"),
    ("constructive heuristic", r"constructive heuristic"),
    ("set covering", r"\\emph\{set covering\}|set covering"),
    ("set packing", r"\\emph\{set packing\}|set packing"),
    ("set partitioning", r"\\emph\{set partitioning\}|set partitioning"),
    ("semi-continuous variable", r"semicontinuous|semi-continuous"),
    ("valid inequalities", r"valid inequalities"),
    ("price of integrality", r"price of integrality"),
    ("exchange argument", r"exchange argument"),
    ("fixed cost", r"fixed cost"),
    ("minimum lot", r"minimum lot"),
    ("activation", r"activation"),
    ("precedences", r"precedences"),
    ("absolute value", r"absolute value"),
    ("piecewise linear function", r"piecewise linear"),
    ("binary expansion", r"binary expansion"),
    ("soft constraints", r"soft constraints"),
    ("maximum variable", r"maximum variable"),
    ("conjunctive normal form", r"conjunctive normal form"),
    ("marginal prices", r"marginal prices"),
    ("tolerances", r"tolerances"),
    ("dual certificate", r"dual certificate"),
    ("certified gap", r"certified gap"),
    ("inventory balance", r"inventory balance|inventory balances"),
    ("capacitated location", r"capacitated location"),
    ("p-median", r"\$p\$-median|p-median"),
    ("combinatorial auction", r"combinatorial auction"),
    ("knapsack", r"\\emph\{knapsack\}|[Kk]napsack"),
]

# zone del sorgente in cui non si entra: matematica, codice, argomenti opzionali
ZONE_VIETATE = re.compile(
    r"\$[^$]*\$"                                  # matematica in riga
    r"|\\\[.*?\\\]"                               # matematica fuori riga
    r"|\\begin\{(align\*?|equation\*?|array|lstlisting|tabular|istanza)\}.*?"
    r"\\end\{\1\}"
    r"|\\(label|ref|eqref|index|input|includegraphics|cite)\{[^}]*\}"
    r"|\\begin\{[a-z]+\}\[[^\]]*\]"               # titolo di un box
    r"|\\(sub)*section\*?\{[^}]*\}"               # titoli di sezione
    r"|\\(paragraph|chapter)\*?\{[^}]*\}",
    re.S,
)


def _maschera(testo: str) -> list[bool]:
    """True dove si puo' inserire una voce d'indice."""
    libero = [True] * len(testo)
    for m in ZONE_VIETATE.finditer(testo):
        for i in range(m.start(), m.end()):
            libero[i] = False
    return libero


def indicizza(percorso: Path, termini) -> int:
    testo = percorso.read_text(encoding="utf-8")
    libero = _maschera(testo)
    # una voce per termine e per sezione: si spezza il file sulle sezioni
    tagli = [m.start() for m in re.finditer(r"\\(sub)*section\*?\{", testo)] + [len(testo)]
    inizi = [0] + tagli
    inserimenti = []
    for voce, espressione in termini:
        regola = re.compile(espressione)
        for a, b in zip(inizi, inizi[1:] + [len(testo)]):
            if a >= b:
                continue
            for m in regola.finditer(testo, a, b):
                fine = m.end()
                if not all(libero[m.start():fine]):
                    continue
                if f"\\index{{{voce}}}" in testo[max(0, m.start() - 200):fine + 200]:
                    break
                inserimenti.append((fine, voce))
                break
    if not inserimenti:
        return 0
    for posizione, voce in sorted(inserimenti, reverse=True):
        testo = testo[:posizione] + f"\\index{{{voce}}}" + testo[posizione:]
    percorso.write_text(testo, encoding="utf-8")
    return len(inserimenti)


def main(argv) -> int:
    if "--conta" in argv:
        for lingua, radice in (("it", "it"), ("en", "en")):
            n = sum(f.read_text().count("\\index{")
                    for base in CARTELLE[lingua] for f in (BASE / base).rglob("*.tex"))
            print(f"{lingua}: {n} voci d'indice")
        return 0
    lingua = argv[1] if len(argv) > 1 else "it"
    termini = TERMINI_IT if lingua == "it" else TERMINI_EN
    totale = 0
    for cartella in CARTELLE[lingua]:
        for f in sorted((BASE / cartella).rglob("*.tex")):
            n = indicizza(f, termini)
            if n:
                print(f"  {f.relative_to(BASE)}: {n} voci")
            totale += n
    print(f"{lingua}: {totale} voci inserite")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
