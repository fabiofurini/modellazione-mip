"""Stile grafico comune e utilità per gli script del laboratorio.

Tutti gli script importano da qui: palette coerente con la dispensa,
salvataggio figure in dispensa/figure/, salvataggio dati in dati/.
"""
import sys
from pathlib import Path

import matplotlib


def _dentro_notebook() -> bool:
    """True in Jupyter/Colab: lì le figure si mostrano, non si salvano."""
    if "google.colab" in sys.modules:
        return True
    try:
        from IPython import get_ipython
        return type(get_ipython()).__name__ == "ZMQInteractiveShell"
    except Exception:
        return False


NOTEBOOK = _dentro_notebook()

if not NOTEBOOK:
    matplotlib.use("Agg")     # nei notebook resta il backend inline
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parent.parent
DIR_FIGURE = BASE / "dispensa" / "figure"
DIR_DATI = BASE / "dati"

# Palette istituzionale della dispensa
BLU = "#16324A"      # blu notte (titoli)
TEAL = "#0E7490"     # teal (accento principale)
ROSSO = "#C0392B"
VERDE = "#1E8449"
ARANCIO = "#CA6F1E"
GRIGIO = "#7F8C8D"
CICLO = [TEAL, ROSSO, VERDE, ARANCIO, BLU, GRIGIO, "#8E44AD", "#B7950B"]

plt.rcParams.update({
    "figure.figsize": (7.2, 4.2),
    "figure.dpi": 120,
    "font.size": 10,
    "font.family": "DejaVu Sans",
    "axes.prop_cycle": plt.cycler(color=CICLO),
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.25,
    "grid.linewidth": 0.6,
    "axes.titlesize": 11,
    "axes.titleweight": "bold",
    "axes.titlecolor": BLU,
    "legend.frameon": False,
    "savefig.bbox": "tight",
})


def salva_figura(fig, nome: str) -> None:
    """Salva la figura come PDF (anteprima) e come PNG per il sito (docs/img/).

    Nel notebook non salva niente: mostra la figura sotto la cella.
    """
    if NOTEBOOK:
        plt.show()
        return
    DIR_FIGURE.mkdir(parents=True, exist_ok=True)
    percorso = DIR_FIGURE / f"{nome}.pdf"
    fig.savefig(percorso)
    img = BASE / "docs" / "img"
    img.mkdir(parents=True, exist_ok=True)
    fig.savefig(img / f"{nome}.png", dpi=150)
    plt.close(fig)
    print(f"  [figura] {percorso.relative_to(BASE)} (+ docs/img/{nome}.png)")


def salva_dati(df, nome: str) -> None:
    """Salva un DataFrame in dati/<nome>.csv (nel notebook stampa solo le dimensioni)."""
    if NOTEBOOK:
        print(f"  [dati]   {nome}: {len(df)} righe x {len(df.columns)} colonne")
        return
    DIR_DATI.mkdir(parents=True, exist_ok=True)
    percorso = DIR_DATI / f"{nome}.csv"
    df.to_csv(percorso, index=False)
    print(f"  [dati]   {percorso.relative_to(BASE)}")


def salva_dat(df, nome: str) -> None:
    """Salva un CSV pronto per pgfplots in dispensa/figure/dat/<nome>.csv.

    Serve solo alla dispensa stampata: nel notebook non fa niente.
    """
    if NOTEBOOK:
        return
    d = DIR_FIGURE / "dat"
    d.mkdir(parents=True, exist_ok=True)
    percorso = d / f"{nome}.csv"
    df.to_csv(percorso, index=False)
    print(f"  [dat]    {percorso.relative_to(BASE)}")


def salva_tikz(codice: str, nome: str) -> None:
    """Salva codice TikZ generato in dispensa/figure/<nome>.tex.

    Serve solo alla dispensa stampata: nel notebook non fa niente.
    """
    if NOTEBOOK:
        return
    DIR_FIGURE.mkdir(parents=True, exist_ok=True)
    percorso = DIR_FIGURE / f"{nome}.tex"
    percorso.write_text(codice)
    print(f"  [tikz]   {percorso.relative_to(BASE)}")


def intestazione(titolo: str) -> None:
    print("\n" + "=" * 72)
    print(titolo)
    print("=" * 72)
