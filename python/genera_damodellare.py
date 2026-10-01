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
DIR_CAPITOLI = BASE / "dispensa_5" / "capitoli"
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
[in PDF](pdf/dispensa-5-damodellare.pdf).

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
    corpo = re.sub(r"\\begin\{center\}\\small\s*\\begin\{tabular\}\{[^}]*\}(.*?)\\end\{tabular\}\s*\\end\{center\}",
                   lambda m: "\n\n" + _tabella(m.group(1).replace("\\toprule", "")
                                               .replace("\\midrule", "").replace("\\bottomrule", "")) + "\n",
                   corpo, flags=re.S)
    corpo = corpo.replace("\\Z", "\\mathbb{Z}").replace("\\Q", "\\mathbb{Q}")
    corpo = re.sub(r"\\textsc\{([^}]*)\}", lambda m: m.group(1).upper(), corpo)
    corpo = re.sub(r"\\emph\{([^}]*)\}", r"*\1*", corpo)
    corpo = re.sub(r"\\textbf\{([^}]*)\}", r"**\1**", corpo)
    corpo = re.sub(r"\\index\{[^}]*\}", "", corpo)
    corpo = corpo.replace("---", "—").replace("``", "\u201c").replace("''", "\u201d")
    return re.sub(r"\n{3,}", "\n\n", corpo).strip()


def pagina() -> str:
    pezzi = [TESTA]
    for nome, titolo, intro in CAPITOLI:
        testo = (DIR_CAPITOLI / f"{nome}.tex").read_text(encoding="utf-8")
        pezzi.append(f"\n## {titolo}\n\n{intro}\n")
        for m in re.finditer(r"\\section\*\{(.+?)\}\s*\n\\begin\{problema\}\[(.+?)\]\n(.*?)\n\\end\{problema\}",
                             testo, re.S):
            etichetta, _, corpo = m.group(1), m.group(2), m.group(3)
            pezzi.append(f"### {markdown(etichetta)}\n\n{markdown(corpo)}\n")
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
    print(f"  [pagina] docs/{USCITA.name} ({nuovo.count('### ')} problemi)")
    return 0


if __name__ == "__main__":
    sys.exit(main(verifica="--verifica" in sys.argv))
