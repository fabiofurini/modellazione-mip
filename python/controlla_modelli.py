"""Controlla che i modelli delle pagine del sito rispettino il formato del corso.

Le regole sono quelle dei sorgenti di Fabio, e valgono in ogni forma --- dispense,
sito, fascicolo delle soluzioni:

1. il simbolo di relazione sta sul punto di allineamento (`lhs &\\le rhs`), non
   prima: cosi' `=`, `\\le`, `\\ge` e `\\in` finiscono incolonnati;
2. una riga di dominio per famiglia di variabili, ciascuna con il suo `\\forall`;
3. mai piu' di un vincolo per riga;
4. ogni abbreviazione del preambolo usata nelle pagine (`\\Z`, `\\ub`, ...) e'
   definita anche per MathJax, altrimenti il browser stampa il comando invece
   del simbolo.

Esce con stato non nullo se trova una riga fuori formato, cosi' la CI si ferma.

    python3 python/controlla_modelli.py
"""
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DOCS = BASE / "docs"
PREAMBOLO = BASE / "dispensa_1" / "preambolo.tex"
MATHJAX = DOCS / "javascripts" / "mathjax.js"

# Le abbreviazioni definite dal preambolo delle dispense. L'elenco sta qui, e non
# si legge dal `.tex`, perche' le dispense sono private e in CI non ci sono; se il
# preambolo e' a portata di mano si controlla anche che i due elenchi coincidano.
MACRO_DEL_CORSO = frozenset({
    "AND", "E", "NOT", "OR", "Prob", "Q", "R", "Z", "cvar", "false", "figdat",
    "lb", "true", "ub", "var", "zdual", "zlp", "zlpp", "zlppp", "zmilp",
})

# un dominio: `\in \{0, 1\}`, `\ge 0`, `\le 0`, `\gtreqless 0`, `\in \Z_{\ge 0}`
DOMINIO = re.compile(r"\\in\s*\\\{0|\\ge\s*0|\\le\s*0|\\gtreqless\s*0|\\in\s*\\(Z|Q|R)")
RELAZIONE = re.compile(r"\\le|\\ge|\\in|\\gtreqless|(?<![<>!=])=(?!=)")
APRE = re.compile(r"(\\le|\\ge|\\in|\\gtreqless|=)")


def _nudo(s: str) -> str:
    """Via gli argomenti fra graffe: il `=` di `\\sum_{j=1}^{n}` e l'`\\in` di
    `\\sum_{j \\in J}` non sono il simbolo di relazione della riga."""
    while True:
        senza = re.sub(r"\{[^{}]*\}", "", s)
        if senza == s:
            return s
        s = senza


def righe(blocco: str):
    corpo = re.sub(r"\\(begin|end)\{(aligned|array)\}(\{[^}]*\})?", "", blocco)
    for riga in re.split(r"\\\\(?:\[[^\]]*\])?", corpo):
        riga = riga.strip()
        if riga:
            yield riga


def problemi(riga: str) -> list[str]:
    fuori = []
    colonne = riga.split("&")
    sinistra = colonne[0].replace("\\text{soggetto a}", "").replace("\\quad", " ", 1).strip()
    dopo = colonne[1].lstrip().lstrip("~") if len(colonne) > 1 else ""

    if dopo and not APRE.match(dopo) and not dopo.startswith("\\forall"):
        if RELAZIONE.search(_nudo(dopo)):
            fuori.append("relazione non sul punto di allineamento")
    if RELAZIONE.search(_nudo(sinistra)):
        fuori.append("piu' di una relazione prima del punto di allineamento")
    nucleo = (sinistra + " & " + dopo) if dopo else sinistra
    # `\Z_{\ge 0}` e' un dominio solo, non `\in` piu' `\ge 0`
    nucleo = re.sub(r"\\(Z|Q|R)_\{\\ge 0\}", r"\\\1", nucleo)
    if len(DOMINIO.findall(nucleo)) > 1:
        fuori.append("piu' famiglie di variabili su una riga di dominio")
    return fuori


def macro_non_definite() -> list[str]:
    """Le abbreviazioni del corso che le pagine usano e MathJax non conosce.

    Senza la definizione il browser stampa `\\Z` al posto di Z, e il modello
    sembra sbagliato anche quando non lo e'.
    """
    if PREAMBOLO.exists():   # in locale: l'elenco qui sopra deve restare allineato
        nel_tex = set(re.findall(r"\\newcommand\{\\([A-Za-z]+)\}",
                                 PREAMBOLO.read_text(encoding="utf-8")))
        if nel_tex != set(MACRO_DEL_CORSO):
            return [f"MACRO_DEL_CORSO non coincide con {PREAMBOLO.name}: "
                    f"solo nel tex {sorted(nel_tex - MACRO_DEL_CORSO)}, "
                    f"solo qui {sorted(MACRO_DEL_CORSO - nel_tex)}"]
    per_mathjax = set(re.findall(r"^\s*([A-Za-z]+):\s*\"",
                                 MATHJAX.read_text(encoding="utf-8"), re.M))
    mancanti: dict[str, list[str]] = {}
    for pagina in sorted(DOCS.glob("*.md")):
        for nome in set(re.findall(r"\\([A-Za-z]+)", pagina.read_text(encoding="utf-8"))):
            if nome in MACRO_DEL_CORSO and nome not in per_mathjax:
                mancanti.setdefault(nome, []).append(pagina.name)
    return [f"\\{n} usata in {len(p)} pagine ({', '.join(sorted(p)[:3])}...) "
            f"ma non definita in {MATHJAX.name}" for n, p in sorted(mancanti.items())]


def modelli_mancanti() -> list[str]:
    """Ogni pagina numerica mostra il primale e, se esiste, il duale.

    Il modello generato puo' esserci senza che nessuno lo incorpori: in quel caso
    la pagina parla di un duale che il lettore non vede.
    """
    fuori = []
    for pagina in sorted(DOCS.glob("ex-*.md")):
        n = pagina.stem.removeprefix("ex-")
        testo = pagina.read_text(encoding="utf-8")
        for verso in ("primale", "duale"):
            nome = f"ex{n}_{verso}"
            if (BASE / "dati" / "modelli" / f"{nome}.tex").exists() \
                    and f"modello-esteso: {nome}" not in testo:
                fuori.append(f"{pagina.name}: il modello {nome} esiste ma la pagina non lo mostra")
    return fuori


def main() -> int:
    trovati = 0
    for guaio in macro_non_definite():
        print(guaio)
        trovati += 1
    for guaio in modelli_mancanti():
        print(guaio)
        trovati += 1
    for pagina in sorted(DOCS.glob("*.md")):
        testo = pagina.read_text(encoding="utf-8")
        for n, blocco in enumerate(re.findall(r"\$\$\n(.*?)\n\$\$", testo, re.S), 1):
            if "begin{aligned}" not in blocco and "begin{array}" not in blocco:
                continue
            if "\\text{min-max:}" in blocco:   # confronto fra formulazioni, non un modello
                continue
            for riga in righe(blocco):
                for p in problemi(riga):
                    print(f"{pagina.name} (modello {n}): {p}\n    {riga[:110]}")
                    trovati += 1
    if trovati:
        print(f"\n{trovati} punti da sistemare.")
        return 1
    print("Formato dei modelli: tutte le pagine a posto.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
