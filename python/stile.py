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

# Il titolo sta a sinistra e staccato dagli assi: cosi' non tocca mai il bordo
# della figura, per quanto sia lungo, e la figura resta leggibile anche piccola.
plt.rcParams.update({
    "figure.figsize": (7.2, 4.2),
    "figure.dpi": 120,
    "font.size": 10,
    "font.family": "DejaVu Sans",
    "axes.prop_cycle": plt.cycler(color=CICLO),
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.edgecolor": "#B9C2C9",
    "axes.linewidth": 0.8,
    "axes.labelcolor": BLU,
    "axes.labelsize": 9.5,
    "axes.grid": True,
    "axes.axisbelow": True,
    "grid.color": "#C9D2D8",
    "grid.alpha": 0.55,
    "grid.linewidth": 0.5,
    "axes.titlesize": 11,
    "axes.titleweight": "bold",
    "axes.titlecolor": BLU,
    "axes.titlelocation": "left",
    "axes.titlepad": 10,
    "xtick.color": "#5B6B77",
    "ytick.color": "#5B6B77",
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "xtick.direction": "out",
    "ytick.direction": "out",
    "text.color": BLU,
    "legend.frameon": False,
    "legend.fontsize": 9,
    "lines.linewidth": 1.9,
    "lines.markersize": 6,
    "patch.linewidth": 0.8,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.08,
})


def _legenda_fuori(fig):
    """Sposta le legende fuori dall'area del grafico, sotto tutta la figura.

    Una legenda dentro il grafico copre le linee e i punti: si perde
    informazione proprio dove serve. Qui si raccolgono le voci di tutti gli
    assi e si ricostruisce una legenda sola, sotto la figura, cosi' non
    finisce mai sopra l'etichetta dell'asse orizzontale.
    """
    maniglie, etichette = [], []
    for ax in fig.get_axes():
        leg = ax.get_legend()
        if leg is not None:
            leg.remove()
        m, e = ax.get_legend_handles_labels()
        for mm, ee in zip(m, e):
            if ee and not ee.startswith("_") and ee not in etichette:
                maniglie.append(mm)
                etichette.append(ee)
    if not etichette:
        return
    colonne = len(etichette) if len(etichette) <= 4 else 3
    fig.legend(maniglie, etichette, fontsize=9, frameon=False,
               loc="upper center", bbox_to_anchor=(0.5, -0.08),
               bbox_transform=fig.transFigure,
               ncol=colonne, borderaxespad=0.0)

def salva_figura(fig, nome: str) -> None:
    """Salva la figura come PDF (anteprima) e come PNG per il sito (docs/img/).

    Nel notebook non salva niente: mostra la figura sotto la cella.
    """
    if NOTEBOOK:
        plt.show()
        return
    _legenda_fuori(fig)
    DIR_FIGURE.mkdir(parents=True, exist_ok=True)
    percorso = DIR_FIGURE / f"{nome}.pdf"
    fig.savefig(percorso, bbox_inches="tight")
    img = BASE / "docs" / "img"
    img.mkdir(parents=True, exist_ok=True)
    fig.savefig(img / f"{nome}.png", dpi=150, bbox_inches="tight")
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
