"""Le tabelle dei bound delle varianti, generate dai CSV degli script.

P0.6 chiede, per almeno una variante di ciascun esercizio dei capitoli 7 e 8,
un'euristica ammissibile, un certificato duale e la tabella dei bound. I primi
due stanno negli script (`salva_modello`, `valuta`, `due_rilassamenti`); la
tabella si genera qui dai CSV, cosi' i numeri sono quelli verificati e non si
trascrivono a mano.

Uso:  python3 strumenti/tabelle_varianti.py            # scrive le tabelle
      python3 strumenti/tabelle_varianti.py --verifica # controlla che siano aggiornate
"""
import sys
from fractions import Fraction
from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parent.parent

CONF = dict(dati=BASE / "dati", uscita=BASE / "dati/tabelle",
            testa=("", "valore", "che cos'è"),
            voci=[("$\\ub$", "ub", "soluzione euristica"),
                  ("$\\lb$", "lb", "certificato duale costruito a mano"),
                  ("$\\zlp$", "z_lp", "rilassamento senza i bound"),
                  ("$\\zlpp$", "z_lp_rafforzato", "rilassamento con i bound"),
                  ("$\\zmilp$", "z_milp", "ottimo del MILP")])

def numero(x) -> str:
    """Frazione ridotta o intero, come nella dispensa."""
    f = Fraction(float(x)).limit_denominator(10_000)
    return str(f.numerator) if f.denominator == 1 else f"\\frac{{{f.numerator}}}{{{f.denominator}}}"


def tabella(riga, conf) -> str:
    testa = conf["testa"]
    corpo = "\n".join(f"{etichetta} & ${numero(riga[colonna])}$ & {nota} \\\\"
                      for etichetta, colonna, nota in conf["voci"])
    return ("\\begin{center}\\small\n\\begin{tabular}{lrl}\n\\toprule\n"
            f"{testa[0]} & {testa[1]} & {testa[2]} \\\\\n\\midrule\n{corpo}\n"
            "\\bottomrule\n\\end{tabular}\n\\end{center}\n")


def tabella_md(riga, conf) -> str:
    """La stessa tabella, in markdown, per le pagine del sito."""
    testa = conf["testa"]
    righe = [f"| {testa[0]} | {testa[1]} | {testa[2]} |", "|---|---:|---|"]
    for etichetta, colonna, nota in conf["voci"]:
        righe.append(f"| ${etichetta.strip('$')}$ | ${numero(riga[colonna])}$ | {nota} |")
    return "\n".join(righe) + "\n"


def main(verifica: bool = False) -> int:
    diversi = []
    conf = CONF
    if True:
        conf["uscita"].mkdir(parents=True, exist_ok=True)
        for csv in sorted(conf["dati"].glob("fam0[78]_*[ab]_bound.csv")):
            riga = pd.read_csv(csv).iloc[0]
            testo = tabella(riga, conf)
            for suffisso, contenuto in ((".tex", testo), (".md", tabella_md(riga, conf))):
                percorso = conf["uscita"] / f"{csv.stem}{suffisso}"
                vecchio = percorso.read_text(encoding="utf-8") if percorso.exists() else ""
                if contenuto == vecchio:
                    continue
                diversi.append(str(percorso.relative_to(BASE)))
                if not verifica:
                    percorso.write_text(contenuto, encoding="utf-8")
    if verifica:
        if diversi:
            print("Tabelle delle varianti non aggiornate: " + ", ".join(diversi))
            return 1
        print("Tabelle delle varianti aggiornate.")
        return 0
    print(f"Tabelle scritte o aggiornate: {len(diversi)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(verifica="--verifica" in sys.argv))
