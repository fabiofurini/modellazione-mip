"""Esegue in sequenza tutti gli script del corso.

Rigenera: dati (dati/*.csv), dati per le figure pgfplots (dispensa/figure/dat/*.csv),
anteprime matplotlib (dispensa/figure/*.pdf), immagini per il sito (docs/img/*.png)
e i notebook dei capitoli (notebooks/*.ipynb).

Uso:  python3 esegui_tutti.py
"""
import subprocess
import sys
import time
from pathlib import Path

SCRIPT = [
    # Parte I — modellazione
    # Parte II — i problemi
    "fam07_1_assegnamento.py",
    "fam07_2_costofisso.py",
    "fam07_3_selezione.py",
    "fam07_4_parallelo.py",
    "fam07_5_classisetup.py",
    "fam07_6_classipremio.py",
    "fam07_7_ritardo.py",
    "fam07_8_riepilogo.py",
]

base = Path(__file__).resolve().parent
inizio = time.time()
for s in SCRIPT:
    print(f"\n{'#' * 72}\n# {s}\n{'#' * 72}")
    esito = subprocess.run([sys.executable, str(base / s)], cwd=base)
    if esito.returncode != 0:
        print(f"ERRORE in {s}: interrompo.")
        sys.exit(1)
print(f"\n{'#' * 72}\n# genera_notebook.py\n{'#' * 72}")
esito = subprocess.run([sys.executable, str(base / "genera_notebook.py")], cwd=base)
if esito.returncode != 0:
    print("ERRORE nella generazione dei notebook: interrompo.")
    sys.exit(1)

print(f"\nTutti gli script completati in {time.time() - inizio:.1f} s.")
