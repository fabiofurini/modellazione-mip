"""Le slide dei modelli e dei problemi, generate dalle stesse fonti della dispensa.

Regola zero del corso: un modello esiste in un posto solo. Le slide non fanno
eccezione --- i modelli simbolici si estraggono dall'ambiente `modello` delle
dispense, quelli dell'istanza dai `.tex` che genera `esteso.py`, i bound dai CSV
degli script. Qui si scrive soltanto la cornice.

Produce `slides/capitoli/*.tex`, inclusi dal mazzo principale:

    modelli_numerici.tex    una slide per EX 1--15
    problemi_famiglie.tex   una slide per ciascuno dei 23 problemi
    da_modellare.tex        una slide per ciascuno dei 40 problemi da modellare

Uso:  python3 genera_slide.py
      python3 genera_slide.py --verifica
"""
import re
import sys
from pathlib import Path

import pandas as pd

TITOLO_ENUNCIATO = "L'enunciato"
TITOLO_DOMANDA = "Che cosa si chiede"

BASE = Path(__file__).resolve().parent.parent
DIR_SLIDE = BASE / "slides" / "capitoli"
DIR_DATI = BASE / "dati"
DIR_MODELLI = DIR_DATI / "modelli"
DISPENSE = sorted(BASE.glob("dispensa_*/capitoli"))
ESERCIZI = BASE / "esercizi" / "capitoli"

NOME_EX = {
    1: "ex01", 2: "ex02", 3: "ex03", 4: "ex04", 5: "ex05", 6: "ex06", 7: "ex07",
    8: "ex08", 9: "ex09", 10: "ex10", 11: "ex11", 12: "ex12", 13: "ex13",
    14: "ex14", 15: "ex15",
}
FAMIGLIE = ([(f"7.{i}", f"fam07_{i}") for i in range(1, 8)]
            + [(f"8.{i}", f"fam08_{i}") for i in range(1, 5)]
            + [(f"9.{i}", f"fam09_{i}") for i in range(1, 4)]
            + [(f"10.{i}", f"fam10_{i}") for i in range(1, 10)])


# ---------------------------------------------------------------- estrazione

def _tutti_i_tex() -> list[Path]:
    fuori = []
    for cartella in DISPENSE:
        fuori += sorted(cartella.rglob("*.tex"))
    if ESERCIZI.exists():
        fuori += sorted(ESERCIZI.glob("*.tex"))
    return fuori


def ambienti(nome: str) -> dict[str, str]:
    """`{titolo: corpo}` di tutti gli ambienti `nome` delle dispense."""
    fuori = {}
    for f in _tutti_i_tex():
        testo = f.read_text(encoding="utf-8")
        for m in re.finditer(r"\\begin\{" + nome + r"\}\[([^\]]*)\](.*?)\\end\{" + nome + r"\}",
                             testo, re.S):
            fuori[m.group(1).strip()] = m.group(2).strip()
    return fuori


def per_beamer(corpo: str) -> str:
    """Il corpo di un ambiente della dispensa, ripulito per una slide."""
    corpo = re.sub(r"\\label\{[^}]*\}", "", corpo)
    corpo = re.sub(r"\\index\{[^}]*\}", "", corpo)
    corpo = re.sub(r"\\(begin|end)\{subequations\}", "", corpo)
    corpo = re.sub(r"\\vskip\s+-?[0-9.]+\s*mm", "", corpo)
    corpo = corpo.replace("\\begin{align}", "\\begin{aligned}").replace("\\end{align}", "\\end{aligned}")
    corpo = corpo.replace("\\begin{align*}", "\\begin{aligned}").replace("\\end{align*}", "\\end{aligned}")
    corpo = corpo.replace("\\nonumber", "")
    corpo = re.sub(r"\\\\\[[0-9.]+ex\]", "\\\\\\\\", corpo)
    corpo = re.sub(r"[ \t]+$", "", corpo, flags=re.M)
    corpo = re.sub(r"\n{2,}", "\n", corpo)
    return corpo.strip()


def domande_degli_esercizi() -> dict[str, str]:
    """`{titolo del problema: corpo della domanda}`: la domanda segue il suo problema."""
    import re as _re
    fuori = {}
    if not ESERCIZI.exists():
        return fuori
    for f in sorted(ESERCIZI.glob("*.tex")):
        testo = f.read_text(encoding="utf-8")
        ultimo = None
        for m in _re.finditer(r"\\begin\{(problema|domanda)\}(?:\[([^\]]*)\])?(.*?)\\end\{\1\}",
                              testo, _re.S):
            if m.group(1) == "problema":
                ultimo = (m.group(2) or "").strip()
            elif ultimo:
                fuori[ultimo] = m.group(3).strip()
                ultimo = None
    return fuori


def bound(nome_csv: str) -> dict | None:
    f = DIR_DATI / f"{nome_csv}_bound.csv"
    if not f.exists():
        return None
    r = pd.read_csv(f).iloc[-1].to_dict()
    return r


def numero(x) -> str:
    from fractions import Fraction
    if pd.isna(x):
        return "---"
    fr = Fraction(float(x)).limit_denominator(10_000)
    return str(fr.numerator) if fr.denominator == 1 else f"\\tfrac{{{fr.numerator}}}{{{fr.denominator}}}"


def riga_bound(r: dict) -> str:
    """I cinque numeri su una riga sola: sulla slide la tabella ruba spazio al modello."""
    massimo = str(r.get("senso", "min")) == "max"
    eur, duale = ("\\lb", "\\ub") if massimo else ("\\ub", "\\lb")
    v_eur = numero(r["lb"] if massimo else r["ub"])
    v_duale = numero(r["ub"] if massimo else r["lb"])
    pezzi = [f"${eur} = {v_eur}$", f"${duale} = {v_duale}$",
             f"$\\zlp = {numero(r['z_lp'])}$"]
    if not pd.isna(r.get("z_lp_rafforzato")):
        pezzi.append(f"$\\zlpp = {numero(r['z_lp_rafforzato'])}$")
    pezzi.append(f"$\\zmilp = {numero(r['z_milp'])}$")
    return ("\\begin{center}\\scriptsize\n" + " \\;$\\cdot$\\; ".join(pezzi)
            + "\n\\end{center}")


def tabella_bound(r: dict) -> str:
    massimo = str(r.get("senso", "min")) == "max"
    eur, duale = ("$\\lb$", "$\\ub$") if massimo else ("$\\ub$", "$\\lb$")
    v_eur = numero(r["lb"] if massimo else r["ub"])
    v_duale = numero(r["ub"] if massimo else r["lb"])
    righe = [f"{eur} (euristica) & ${v_eur}$ \\\\",
             f"{duale} (duale a mano) & ${v_duale}$ \\\\",
             f"$\\zlp$ & ${numero(r['z_lp'])}$ \\\\"]
    if not pd.isna(r.get("z_lp_rafforzato")):
        righe.append(f"$\\zlpp$ & ${numero(r['z_lp_rafforzato'])}$ \\\\")
    righe.append(f"$\\zmilp$ & ${numero(r['z_milp'])}$ \\\\")
    return ("\\begin{center}\\footnotesize\n\\begin{tabular}{lr}\n\\toprule\n"
            + "\n".join(righe) + "\n\\bottomrule\n\\end{tabular}\n\\end{center}")



LEGENDA = r"""\begin{itemize}\footnotesize
  \item $\lb$ e $\ub$ sono i due lati del sandwich costruiti \emph{a mano}: la
        soluzione euristica da un lato, il certificato duale dall'altro.
  \item $\zlp$ è il rilassamento senza i bound, $\zlpp$ quello con i bound,
        $\zmilp$ l'ottimo intero.
  \item In un minimo l'euristica dà $\ub$ e il duale $\lb$; in un massimo i due
        ruoli si scambiano.
\end{itemize}"""

APERTURA_EX = r"""\begin{frame}{Quindici modelli numerici}
Dati espliciti, poche variabili, una tecnica per modello. Ogni slide mostra il
modello dell'istanza scritto per esteso --- una colonna per variabile, come lo
genera lo script --- e i cinque numeri del sandwich.
\vfill
""" + LEGENDA + r"""
\end{frame}
"""

APERTURA_FAM = r"""\begin{frame}{Ventitre problemi con modello simbolico}
Per ciascun problema: l'enunciato come arriva, il modello simbolico e i cinque
numeri del sandwich. I modelli sono quelli della dispensa, generati dalla stessa
sorgente.
\vfill
""" + LEGENDA + r"""
\end{frame}
"""

APERTURA_MOD = r"""\begin{frame}{Quaranta problemi da modellare}
Qui ci sono soltanto gli enunciati: venti con i dati numerici espliciti e venti
in forma simbolica. Il modello va scritto, non letto --- sono i problemi su cui
esercitarsi, e le soluzioni sono riservate ai docenti.
\end{frame}
"""

# ---------------------------------------------------------------- le slide

def slide_numerici(problemi: dict) -> str:
    pezzi = ["\\section{I quindici modelli numerici}\n", APERTURA_EX]
    for n in range(1, 16):
        titolo = next((t for t in problemi if t.startswith(f"EX {n} ---")), None)
        modello = DIR_MODELLI / f"{NOME_EX[n]}_primale.tex"
        r = bound(NOME_EX[n])
        if titolo is None or not modello.exists() or r is None:
            print(f"  [salto] EX {n}")
            continue
        nome = titolo.split("---", 1)[1].strip()
        pezzi.append(f"""\\begin{{frame}}{{EX {n} --- {nome}}}
\\begin{{center}}
\\adjustbox{{max width=\\textwidth, max totalheight=0.66\\textheight}}{{$\\displaystyle
\\input{{../dati/modelli/{NOME_EX[n]}_primale}}
$}}
\\end{{center}}
\\vfill
{riga_bound(r)}
\\end{{frame}}
""")
    return "\n".join(pezzi)


def slide_famiglie(modelli: dict, problemi: dict) -> str:
    pezzi = ["\\section{I ventitre problemi}\n", APERTURA_FAM]
    for numero_p, csv in FAMIGLIE:
        chiave_m = next((t for t in modelli
                         if t.startswith(f"Modello {numero_p} ---")
                         or t.startswith(f"Modello {numero_p}A ---")), None)
        chiave_p = next((t for t in problemi if t.startswith(f"Problema {numero_p} ---")), None)
        r = bound(csv)
        if chiave_m is None or r is None:
            print(f"  [salto] problema {numero_p}")
            continue
        nome = chiave_m.split("---", 1)[1].strip()
        enunciato = per_beamer(problemi[chiave_p]) if chiave_p else ""
        if enunciato:
            pezzi.append(f"""\\begin{{frame}}[allowframebreaks]{{Problema {numero_p} --- {nome}}}
\\begin{{block}}{{L'enunciato}}
\\footnotesize {enunciato}
\\end{{block}}
\\end{{frame}}
""")
        pezzi.append(f"""\\begin{{frame}}{{Modello {numero_p} --- {nome}}}
\\begin{{center}}
\\adjustbox{{max width=\\textwidth, max totalheight=0.66\\textheight}}{{$\\displaystyle
{per_beamer(modelli[chiave_m])}
$}}
\\end{{center}}
\\vfill
{riga_bound(r)}
\\end{{frame}}
""")
    return "\n".join(pezzi)


def slide_da_modellare(problemi: dict, domande: dict) -> str:
    pezzi = ["\\section{I quaranta problemi da modellare}\n", APERTURA_MOD]
    for prefisso, titolo_sezione in (("N", "Venti problemi numerici"),
                                     ("S", "Venti problemi simbolici")):
        pezzi.append(f"\\subsection{{{titolo_sezione}}}\n")
        for i in range(1, 21):
            chiave = next((t for t in problemi if t.startswith(f"{prefisso}{i} ---")), None)
            if chiave is None:
                continue
            nome = chiave.split("---", 1)[1].strip()
            chiave_d = next((d for d in domande if d.startswith(f"{prefisso}{i} ---")), None)
            domanda = ("\n\\begin{block}{" + TITOLO_DOMANDA + "}\n\\footnotesize "
                       + per_beamer(domande[chiave_d]) + "\n\\end{block}") if chiave_d else ""
            pezzi.append(f"""\\begin{{frame}}[allowframebreaks]{{{prefisso}{i} --- {nome}}}
\\begin{{block}}{{{TITOLO_ENUNCIATO}}}
\\footnotesize {per_beamer(problemi[chiave])}
\\end{{block}}{domanda}
\\end{{frame}}
""")
    return "\n".join(pezzi)


def main() -> int:
    verifica = "--verifica" in sys.argv
    modelli = ambienti("modello")
    problemi = ambienti("problema")
    DIR_SLIDE.mkdir(parents=True, exist_ok=True)
    attesi = {
        "modelli_numerici.tex": slide_numerici(problemi),
        "problemi_famiglie.tex": slide_famiglie(modelli, problemi),
        "da_modellare.tex": slide_da_modellare(problemi, domande_degli_esercizi()),
    }
    cambiati = []
    for nome, testo in attesi.items():
        f = DIR_SLIDE / nome
        if not f.exists() or f.read_text(encoding="utf-8") != testo:
            cambiati.append(nome)
            if not verifica:
                f.write_text(testo, encoding="utf-8")
        n = testo.count("\\begin{frame}")
        print(f"  [slide] {nome}: {n} slide")
    if verifica and cambiati:
        print("Slide non aggiornate: " + ", ".join(cambiati))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
