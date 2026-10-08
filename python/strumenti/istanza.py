"""Genera i box `istanza` in LaTeX: una colonna per variabile, come nei
sorgenti di Fabio.

Uso: si passa l'elenco ordinato dei nomi delle variabili e le righe del
modello (obiettivo, vincoli, dominio). Ogni riga e' un dizionario
{nome variabile: coefficiente} piu' il verso e il termine noto. Il generatore
si occupa dell'incolonnamento, dei segni e degli spazi.
"""


def _termine(coef, nome, primo):
    if coef == 0:
        return ""
    segno = "" if primo else ("+" if coef > 0 else "-")
    if not primo and coef < 0:
        coef = -coef
    elif primo and coef < 0:
        segno = "-"
        coef = -coef
    testo = "" if coef == 1 else _num(coef)
    return f"{segno}{testo}{nome}"


def _num(x):
    if isinstance(x, float) and x == int(x):
        x = int(x)
    if isinstance(x, tuple):          # frazione (num, den)
        return f"\\frac{{{x[0]}}}{{{x[1]}}}"
    return str(x)


def dominio(variabili, verso, rhs):
    """Riga di dominio: le variabili elencate, una per colonna, separate da
    virgola, con il verso e il dominio nelle ultime due colonne."""
    celle = [""]
    for k, v in enumerate(variabili):
        celle.append(v + ("," if k < len(variabili) - 1 else ""))
    celle.append(verso)
    celle.append(rhs)
    return " & ".join(celle)


def box(titolo, variabili, righe, small=False, domini=()):
    """Restituisce il codice LaTeX del box.

    `righe` e' una lista di tuple (etichetta, coefficienti, verso, rhs):
    l'etichetta va nella prima colonna (per esempio ``\\min`` o vuota),
    `coefficienti` e' un dizionario {variabile: coefficiente}, `verso` una
    stringa come ``\\le`` (vuota per l'obiettivo) e `rhs` il termine noto.
    """
    n = len(variabili)
    spec = "r" + "@{\\,}r" * n + " c r"
    fuori = ["\\begin{istanza}[" + titolo + "]"]
    if small:
        fuori.append("\\small\\setlength{\\arraycolsep}{1pt}")
    fuori.append("\\begin{array}{" + spec + "}")
    for etichetta, coef, verso, rhs in righe:
        celle = [etichetta]
        primo = True
        for v in variabili:
            t = _termine(coef.get(v, 0), v, primo)
            if t:
                primo = False
            celle.append(t)
        celle.append(verso)
        celle.append("" if rhs is None else _num(rhs))
        fuori.append(" & ".join(celle) + "\\\\")
    for riga in domini:
        fuori.append(riga + "\\\\")
    fuori[-1] = fuori[-1][:-2]
    fuori.append("\\end{array}")
    fuori.append("\\end{istanza}")
    return "\n".join(fuori)
