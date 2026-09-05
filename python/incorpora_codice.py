"""Incorpora nelle pagine del sito lo script completo del capitolo.

Lo stile del corso vuole che ogni pagina sia leggibile da sola: oltre al
collegamento al file su GitHub, la pagina contiene lo script per intero dentro un
blocco richiudibile. Copiarlo a mano significa farlo divergere; qui si rigenera.

Come funziona: ogni pagina che dichiara `**Script:** `python/NOME.py`` riceve, in
fondo, un blocco delimitato da due marcatori HTML. Il contenuto fra i marcatori
e' rigenerato da questo script; tutto il resto della pagina non si tocca.

Uso:  python3 incorpora_codice.py             # rigenera i blocchi
      python3 incorpora_codice.py --verifica  # controlla che siano aggiornati
"""
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DIR_SCRIPT = BASE / "python"
DIR_DOCS = BASE / "docs"

INIZIO = "<!-- script-incorporato: inizio (rigenerato da python/incorpora_codice.py) -->"
FINE = "<!-- script-incorporato: fine -->"
INTESTAZIONE = re.compile(r"\*\*Script:\*\*\s*`python/([A-Za-z0-9_]+)\.py`")


def blocco(nome: str) -> str:
    """Il blocco richiudibile con lo script per intero."""
    codice = (DIR_SCRIPT / f"{nome}.py").read_text().rstrip("\n")
    righe = codice.count("\n") + 1
    return "\n".join([
        INIZIO,
        "",
        f'??? example "Mostra lo script completo — `python/{nome}.py` ({righe} righe)"',
        "",
        "    ```python",
        *[f"    {r}" if r else "" for r in codice.splitlines()],
        "    ```",
        "",
        FINE,
    ])


def pagina_principale(nome: str) -> str | None:
    """La pagina che «possiede» lo script: quella che lo cita piu' volte.

    Le sottopagine di un capitolo (per esempio le quattordici tecniche del
    capitolo 3) citano lo stesso script nell'intestazione: lo script per intero
    si incorpora una volta sola, sulla pagina principale.
    """
    candidate = []
    for pagina in sorted(DIR_DOCS.glob("*.md")):
        testo = pagina.read_text()
        quante = testo.replace(INIZIO, "").split(FINE)[0].count(f"python/{nome}.py") \
            if INIZIO in testo else testo.count(f"python/{nome}.py")
        if quante:
            candidate.append((-quante, len(pagina.stem), pagina.stem))
    return min(candidate)[2] if candidate else None


def aggiorna(pagina: Path) -> str | None:
    """Il testo della pagina con il blocco aggiornato, o None se non va toccata."""
    testo = pagina.read_text()
    m = INTESTAZIONE.search(testo)
    if not m or not (DIR_SCRIPT / f"{m.group(1)}.py").exists():
        return None
    if pagina_principale(m.group(1)) != pagina.stem:
        if INIZIO not in testo:                       # sottopagina: niente da fare
            return None
        prima, resto = testo.split(INIZIO, 1)         # blocco da togliere
        return (prima.rstrip("\n") + "\n" + resto.split(FINE, 1)[1].lstrip("\n"))
    nuovo = blocco(m.group(1))
    if INIZIO in testo:
        prima, resto = testo.split(INIZIO, 1)
        dopo = resto.split(FINE, 1)[1]
        return prima + nuovo + dopo
    return testo.rstrip("\n") + "\n\n" + nuovo + "\n"


def main() -> int:
    verifica = "--verifica" in sys.argv
    disallineate = []
    for pagina in sorted(DIR_DOCS.glob("*.md")):
        atteso = aggiorna(pagina)
        if atteso is None:
            continue
        if verifica:
            if pagina.read_text() != atteso:
                disallineate.append(pagina.name)
        elif pagina.read_text() != atteso:
            pagina.write_text(atteso)
            print(f"  [pagina] docs/{pagina.name}")
    if verifica:
        if disallineate:
            print("Pagine con lo script incorporato non aggiornato: "
                  + ", ".join(disallineate))
            print("Rigenerale con: python3 python/incorpora_codice.py")
            return 1
        print("Tutte le pagine hanno lo script incorporato aggiornato.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
