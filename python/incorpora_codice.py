"""Incorpora nelle pagine del sito lo script completo del capitolo.

Lo stile del corso vuole che ogni pagina sia leggibile da sola: oltre al
collegamento al file su GitHub, la pagina contiene lo script per intero dentro un
blocco richiudibile. Copiarlo a mano significa farlo divergere; qui si rigenera.

Come funziona: ogni pagina che dichiara `**Script:** `python/NOME.py`` riceve, in
fondo, un blocco delimitato da due marcatori HTML. Se l'intestazione nomina piu'
script --- la sezione 3.4 ne ha tre --- il blocco li contiene tutti, uno per
riquadro richiudibile. Il contenuto fra i marcatori
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
INTESTAZIONE = re.compile(r"\*\*Script:\*\*(.*)")       # la riga dell'intestazione
SCRIPT = re.compile(r"`python/([A-Za-z0-9_]+)\.py`")       # gli script che nomina


def blocco(nomi: list[str]) -> str:
    """Il blocco con gli script per intero, un riquadro richiudibile ciascuno."""
    parti = [INIZIO, ""]
    for nome in nomi:
        codice = (DIR_SCRIPT / f"{nome}.py").read_text().rstrip("\n")
        righe = codice.count("\n") + 1
        parti += [
            f'??? example "Mostra lo script completo — `python/{nome}.py` ({righe} righe)"',
            "",
            "    ```python",
            *[f"    {r}" if r else "" for r in codice.splitlines()],
            "    ```",
            "",
        ]
    return "\n".join(parti + [FINE])


def corpo(testo: str) -> str:
    """La pagina senza il blocco incorporato: il codice non deve contare."""
    if INIZIO in testo and FINE in testo:
        prima, resto = testo.split(INIZIO, 1)
        return prima + resto.split(FINE, 1)[1]
    return testo


def pagina_principale(nome: str) -> str | None:
    """La pagina che «possiede» lo script: quella che lo cita piu' volte.

    Le sottopagine di un capitolo (per esempio le quattordici tecniche del
    capitolo 3) citano lo stesso script nell'intestazione: lo script per intero
    si incorpora una volta sola, sulla pagina principale.
    """
    candidate = []
    for pagina in sorted(DIR_DOCS.glob("*.md")):
        quante = corpo(pagina.read_text()).count(f"python/{nome}.py")
        if quante:
            candidate.append((-quante, len(pagina.stem), pagina.stem))
    return min(candidate)[2] if candidate else None


def aggiorna(pagina: Path) -> str | None:
    """Il testo della pagina con il blocco aggiornato, o None se non va toccata."""
    testo = pagina.read_text()
    m = INTESTAZIONE.search(testo)
    nominati = SCRIPT.findall(m.group(1)) if m else []
    nomi = [n for n in nominati
            if (DIR_SCRIPT / f"{n}.py").exists() and pagina_principale(n) == pagina.stem]
    if not nomi:
        if INIZIO not in testo:                       # sottopagina: niente da fare
            return None
        prima, resto = testo.split(INIZIO, 1)         # blocco da togliere
        return (prima.rstrip("\n") + "\n" + resto.split(FINE, 1)[1].lstrip("\n"))
    nuovo = blocco(nomi)
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
