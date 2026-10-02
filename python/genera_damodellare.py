"""La pagina del sito con i quaranta problemi da modellare.

Si genera dai sorgenti della dispensa V, cosi' gli enunciati restano una cosa
sola: se cambia la dispensa, cambia la pagina.

Uso:  python3 python/genera_damodellare.py            # scrive docs/da-modellare.md
      python3 python/genera_damodellare.py --verifica # controlla che sia aggiornata
"""
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DIR_CAPITOLI = BASE / "esercizi" / "capitoli"
USCITA = BASE / "docs" / "da-modellare.md"

CAPITOLI = [("cap20_numerici", "Venti problemi numerici",
             "Dati scritti per esteso, come nei quindici modelli numerici: si legge "
             "l'enunciato, si riconoscono le decisioni, si scrive il MILP e lo si risolve."),
            ("cap21_simbolici", "Venti problemi simbolici",
             "Dati dichiarati con il tipo e l'unità, come nei problemi delle famiglie. "
             "Ogni problema mette in gioco due o tre legami fra variabili, e il modello "
             "va scritto in generale, con i quantificatori.")]

TESTA = """# Problemi da modellare

**Quaranta problemi** dati come arrivano davvero — un testo, dei dati, una
domanda — senza il modello già scritto: venti con i dati numerici espliciti e
venti in forma simbolica. Si scaricano anche
[in PDF](pdf/esercizi.pdf).

Le soluzioni sono riservate ai docenti. Il metodo per rispondere è quello di
ogni problema del corso: decisioni e variabili, un vincolo per ogni frase
dell'enunciato, i legami fra le variabili, una soluzione ammissibile e una
duale per i due bound, poi il solver.
"""


def _tabella(testo: str) -> str:
    """`\\begin{tabular}` -> tabella markdown."""
    righe = [r.strip() for r in testo.strip().split("\\\\") if r.strip()]
    fuori = []
    for k, r in enumerate(righe):
        celle = [c.strip() for c in r.split("&")]
        fuori.append("| " + " | ".join(celle) + " |")
        if k == 0:
            fuori.append("|" + "|".join(["---"] * len(celle)) + "|")
    return "\n".join(fuori)


def markdown(corpo: str) -> str:
    """Il corpo di un box `problema` in markdown, con la matematica intatta."""
    # i trattini lunghi prima della tabella: dopo, mangerebbero la riga `|---|`
    corpo = corpo.replace("---", "—").replace("``", "\u201c").replace("''", "\u201d")
    corpo = re.sub(r"\\begin\{center\}\\small\s*\\begin\{tabular\}\{[^}]*\}(.*?)\\end\{tabular\}\s*\\end\{center\}",
                   lambda m: "\n\n" + _tabella(m.group(1).replace("\\toprule", "")
                                               .replace("\\midrule", "").replace("\\bottomrule", "")) + "\n",
                   corpo, flags=re.S)
    corpo = corpo.replace("\\Z", "\\mathbb{Z}").replace("\\Q", "\\mathbb{Q}")
    corpo = re.sub(r"\\textsc\{([^}]*)\}", lambda m: m.group(1).upper(), corpo)
    corpo = re.sub(r"\\emph\{([^}]*)\}", r"*\1*", corpo)
    corpo = re.sub(r"\\textbf\{([^}]*)\}", r"**\1**", corpo)
    corpo = re.sub(r"\\index\{[^}]*\}", "", corpo)
    # la tilde di LaTeX e' uno spazio insecabile: fuori dalla matematica, uno spazio
    corpo = "".join(p if k % 2 else p.replace("~", " ")
                    for k, p in enumerate(re.split(r"(\$[^$]*\$)", corpo)))
    return re.sub(r"\n{3,}", "\n\n", corpo).strip()


# La difficoltà è quella di *ricavare il modello dall'enunciato*: scelta delle
# variabili, numero di famiglie, legami da riconoscere, struttura temporale o
# disgiuntiva. Non misura la dimensione dell'istanza ne' il tempo del solver.
DIFFICOLTA = {
    "N1": 1, "N2": 2, "N3": 1, "N4": 1, "N5": 1, "N6": 3, "N7": 2, "N8": 4,
    "N9": 3, "N10": 3, "N11": 3, "N12": 3, "N13": 4, "N14": 1, "N15": 4,
    "N16": 3, "N17": 3, "N18": 3, "N19": 5, "N20": 3,
    "S1": 3, "S2": 4, "S3": 4, "S4": 4, "S5": 4, "S6": 4, "S7": 5, "S8": 4,
    "S9": 5, "S10": 4, "S11": 5, "S12": 3, "S13": 5, "S14": 5, "S15": 4,
    "S16": 4, "S17": 5, "S18": 4, "S19": 4, "S20": 5,
}


def stelle(etichetta: str) -> str:
    """Le cinque stelle della difficolta', dal codice N3 o S12 dell'enunciato."""
    codice = etichetta.split(None, 1)[0].strip()
    n = DIFFICOLTA.get(codice)
    return "" if n is None else "★" * n + "☆" * (5 - n)


def rientra(testo: str) -> str:
    """Il corpo dentro un box: quattro spazi davanti a ogni riga non vuota."""
    return "\n".join("    " + r if r.strip() else "" for r in testo.split("\n"))


def pagina() -> str:
    pezzi = [TESTA]
    for nome, titolo, intro in CAPITOLI:
        testo = (DIR_CAPITOLI / f"{nome}.tex").read_text(encoding="utf-8")
        pezzi.append(f"\n## {titolo}\n\n{intro}\n")
        for m in re.finditer(r"\\section\*\{(.+?)\}\s*\n\\begin\{problema\}\[(.+?)\]\n(.*?)\n\\end\{problema\}",
                             testo, re.S):
            etichetta, _, corpo = m.group(1), m.group(2), m.group(3)
            d = stelle(etichetta)
            riga = f"    **%s:** {d}\n\n" % "Difficoltà" if d else ""
            pezzi.append(f'!!! abstract "{markdown(etichetta)}"\n\n'
                         + riga + rientra(markdown(corpo)) + "\n")
    return "\n".join(pezzi).rstrip() + "\n"


def main(verifica: bool = False) -> int:
    if not DIR_CAPITOLI.is_dir():
        print("sorgenti della dispensa assenti: pagina dei problemi da modellare saltata")
        return 0
    nuovo = pagina()
    vecchio = USCITA.read_text(encoding="utf-8") if USCITA.exists() else ""
    if verifica:
        if nuovo != vecchio:
            print("docs/da-modellare.md non e' aggiornata: rilanciare genera_damodellare.py")
            return 1
        print("Pagina dei problemi da modellare aggiornata.")
        return 0
    USCITA.write_text(nuovo, encoding="utf-8")
    print(f"  [pagina] docs/{USCITA.name} ({nuovo.count('!!! abstract')} problemi)")
    return 0


if __name__ == "__main__":
    sys.exit(main(verifica="--verifica" in sys.argv))
