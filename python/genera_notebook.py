"""Genera i notebook Jupyter/Colab dei capitoli a partire dagli script.

Un notebook per capitolo in `notebooks/labNN_nome.ipynb`, ricavato dallo script
corrispondente di `python/`: il codice del corso resta uno solo — gli script sono
la sorgente, i notebook si rigenerano. Le sezioni dello script (i blocchi
`# ---- n. TITOLO ----`) diventano celle di codice separate, precedute dal loro
titolo in una cella di testo.

Genera anche la pagina del sito che li elenca (`docs/notebook.md`).

Uso:  python3 genera_notebook.py             # rigenera notebook e pagina del sito
      python3 genera_notebook.py --verifica  # controlla che siano aggiornati
"""
import json
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DIR_SCRIPT = BASE / "python"
DIR_NOTEBOOK = BASE / "notebooks"
DIR_DOCS = BASE / "docs"

REPO = "fabiofurini/modellazione-mip"
SITO = "https://fabiofurini.github.io/modellazione-mip"
RAW = f"https://raw.githubusercontent.com/{REPO}/main/python"
MODULI = ("stile", "mip", "euristiche")      # i moduli comuni che ogni notebook scarica se mancano
BADGE = "https://colab.research.google.com/assets/colab-badge.svg"

RIGA = re.compile(r"^# [-=]{10,}$")
VOCE = re.compile(r"^\s+(\d+)\. ")

PREPARAZIONE = f"""## Preparazione

La cella qui sotto installa `gurobipy` e scarica i tre moduli comuni del corso:
`stile.py` (palette), `mip.py` (rilassamento, duale, bound) ed `euristiche.py`
(next-fit, first-fit, best-fit). La licenza inclusa nel pacchetto pip è limitata a **2000
variabili e 2000 vincoli**: le istanze del corso sono piccole e ci stanno tutte
con ampio margine. Per istanze più grandi si attiva la licenza accademica
gratuita da [portal.gurobi.com](https://portal.gurobi.com).
"""

CODICE_PREPARAZIONE = f'''# Ambiente: il solver e i moduli comuni del corso.
# In locale usa il python/stile.py del repository; su Colab installa e scarica quello che manca.
import importlib.util
import subprocess
import sys
import urllib.request
from pathlib import Path

if importlib.util.find_spec("gurobipy") is None:
    subprocess.run([sys.executable, "-m", "pip", "install", "-q",
                    "gurobipy", "matplotlib", "pandas", "scipy"], check=True)

for modulo in {MODULI}:                     # stile grafico e utilità del corso
    if importlib.util.find_spec(modulo) is None:
        locale = next((p for p in (Path(f"../python/{{modulo}}.py"), Path(f"python/{{modulo}}.py"))
                       if p.exists()), None)
        if locale is not None:
            sys.path.insert(0, str(locale.parent.resolve()))   # notebook aperto nel repository
        else:
            urllib.request.urlretrieve(f"{RAW}/{{modulo}}.py", f"{{modulo}}.py")   # Colab
'''

CHIUSURA = f"""---

Notebook generato da `python/{{nome}}.py` con `python3 python/genera_notebook.py`:
le modifiche si fanno sullo script, non qui.

Materiale didattico di [Fabio Furini]({{sito}}) — DIAG, Sapienza Università di Roma.
Testi, figure e dati [CC BY 4.0](https://github.com/{REPO}/blob/main/LICENSE),
codice [MIT](https://github.com/{REPO}/blob/main/LICENSE-CODE).
"""


INDICE = """# I notebook del corso

Ogni capitolo con dei modelli ha il suo **notebook**: si apre in Google Colab con
un clic sul badge, installa il solver da sé e gira nel browser — sul computer non
serve installare niente. È lo stesso codice degli script di `python/`, cella per
cella, con le figure che compaiono sotto le celle invece di finire in un file.

!!! tip "La licenza del pacchetto pip basta"
    La licenza inclusa in `gurobipy` è limitata a 2000 variabili e 2000 vincoli:
    le istanze del corso sono piccole e ci stanno tutte con ampio margine. Per
    istanze più grandi si attiva la licenza accademica gratuita da
    [portal.gurobi.com](https://portal.gurobi.com).

| Capitolo | Classe | Notebook |
|---|---|---|
{righe}

## Come sono fatti

I notebook non si scrivono a mano: si generano dagli script con

```bash
python3 python/genera_notebook.py
```

Lo script del capitolo resta l'unica sorgente del codice — il notebook ne riprende
docstring, sezioni e commenti — e chi preferisce la riga di comando continua a
lanciare, dalla cartella `python/`:

```bash
python3 fam07_scheduling.py
```
"""


def pagina_del_capitolo(nome: str) -> str | None:
    """Trova la pagina del sito che presenta questo script (il campo «Script:»)."""
    for pagina in sorted(DIR_DOCS.glob("*.md")):
        if f"python/{nome}.py" in pagina.read_text():
            return pagina.stem
    return None


def titolo_e_classe(slug: str) -> tuple[str, str]:
    """Titolo (H1) e classe di modello dichiarata nell'intestazione della pagina."""
    righe = (DIR_DOCS / f"{slug}.md").read_text().splitlines()
    titolo = next(r[2:].strip() for r in righe if r.startswith("# "))
    classe = ""
    for r in righe:
        if "Classe" in r and "·" in r:
            testo = r.split("·")[0].replace("*", "").strip()
            classe = testo.removeprefix("Classe:").strip()
            break
    return titolo, classe


def pagina_indice() -> str:
    """La pagina del sito che elenca i notebook, con un badge per capitolo."""
    righe = []
    for percorso in sorted(list(DIR_SCRIPT.glob("cap*.py")) + list(DIR_SCRIPT.glob("fam*.py"))):
        nome = percorso.stem
        slug = pagina_del_capitolo(nome)
        if not slug:
            continue
        titolo, classe = titolo_e_classe(slug)
        colab = (f"https://colab.research.google.com/github/{REPO}"
                 f"/blob/main/notebooks/{nome}.ipynb")
        righe.append(f"| [{titolo}]({slug}.md) | {classe} | "
                     f"[![Apri in Colab]({BADGE})]({colab}) |")
    return INDICE.format(righe="\n".join(righe))


def testa_e_corpo(sorgente: str) -> tuple[str, str, str]:
    """Separa il docstring del modulo (titolo, corpo) dal resto del codice."""
    fine = sorgente.index('"""', 3)
    doc = sorgente[3:fine].strip()
    titolo, _, corpo = doc.partition("\n")
    return titolo.rstrip("."), corpo.strip(), sorgente[fine + 3:].lstrip("\n")


def sezioni(codice: str) -> list[tuple[str | None, str]]:
    """Divide il codice nei blocchi `# ---- titolo ----`: [(titolo, codice), ...]."""
    righe = codice.splitlines()
    blocchi: list[tuple[str | None, list[str]]] = [(None, [])]
    i = 0
    while i < len(righe):
        if RIGA.match(righe[i]):
            j = i + 1
            titolo = []
            while j < len(righe) and righe[j].startswith("#") and not RIGA.match(righe[j]):
                titolo.append(righe[j].lstrip("#").strip())
                j += 1
            if titolo and j < len(righe) and RIGA.match(righe[j]):
                blocchi.append((" ".join(titolo), []))
                i = j + 1
                continue
        blocchi[-1][1].append(righe[i])
        i += 1
    return [(t, "\n".join(c).strip()) for t, c in blocchi if "\n".join(c).strip()]


def cella_testo(testo: str) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": righe_json(testo)}


def cella_codice(codice: str) -> dict:
    return {"cell_type": "code", "execution_count": None, "metadata": {},
            "outputs": [], "source": righe_json(codice)}


def righe_json(testo: str) -> list[str]:
    """Testo come lista di righe con il newline in coda, tranne l'ultima (uso nbformat)."""
    righe = testo.rstrip("\n").split("\n")
    return [r + "\n" for r in righe[:-1]] + righe[-1:]


def notebook(percorso: Path) -> dict:
    nome = percorso.stem
    titolo, corpo, codice = testa_e_corpo(percorso.read_text())
    slug = pagina_del_capitolo(nome)
    colab = f"https://colab.research.google.com/github/{REPO}/blob/main/notebooks/{nome}.ipynb"

    intro = [f"# {titolo}", "", f"[![Apri in Colab]({BADGE})]({colab})", ""]
    intro.append("\n".join(VOCE.sub(r"\1. ", r) for r in corpo.splitlines()))
    if slug:
        intro += ["", f"Il capitolo completo — modello, dati, risultati e analisi di "
                      f"sensitività — è [sul sito]({SITO}/{slug}/)."]

    celle = [cella_testo("\n".join(intro)),
             cella_testo(PREPARAZIONE),
             cella_codice(CODICE_PREPARAZIONE.strip())]
    for t, c in sezioni(codice):
        if t:
            celle.append(cella_testo(f"## {t}"))
        celle.append(cella_codice(c))
    celle.append(cella_testo(CHIUSURA.format(
        nome=nome, sito="https://sites.google.com/view/fabiofurini/home-page")))

    return {"cells": celle,
            "metadata": {"colab": {"provenance": []},
                         "kernelspec": {"display_name": "Python 3",
                                        "language": "python", "name": "python3"},
                         "language_info": {"name": "python"}},
            "nbformat": 4, "nbformat_minor": 5}


def main() -> int:
    verifica = "--verifica" in sys.argv
    DIR_NOTEBOOK.mkdir(exist_ok=True)
    disallineati = []
    indice = DIR_DOCS / "notebook.md"
    if verifica:
        if not indice.exists() or indice.read_text() != pagina_indice():
            disallineati.append(indice.name)
    else:
        indice.write_text(pagina_indice())
        print(f"  [pagina]   docs/{indice.name}")
    for percorso in sorted(list(DIR_SCRIPT.glob("cap*.py")) + list(DIR_SCRIPT.glob("fam*.py"))):
        atteso = json.dumps(notebook(percorso), ensure_ascii=False, indent=1) + "\n"
        uscita = DIR_NOTEBOOK / f"{percorso.stem}.ipynb"
        if verifica:
            if not uscita.exists() or uscita.read_text() != atteso:
                disallineati.append(uscita.name)
        else:
            uscita.write_text(atteso)
            print(f"  [notebook] notebooks/{uscita.name}")
    if verifica:
        if disallineati:
            print("Notebook non aggiornati: " + ", ".join(disallineati))
            print("Rigenerali con: python3 python/genera_notebook.py")
            return 1
        print("Tutti i notebook sono allineati agli script.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
