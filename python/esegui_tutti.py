"""Esegue in sequenza tutti gli script del corso.

Rigenera: dati (dati/*.csv), dati per le figure pgfplots (dispensa/figure/dat/*.csv),
anteprime matplotlib (dispensa/figure/*.pdf), immagini per il sito (docs/img/*.png),
i notebook dei capitoli (notebooks/*.ipynb) e i blocchi di codice incorporati
nelle pagine del sito (docs/*.md).

Uso:  python3 esegui_tutti.py
"""
import subprocess
import sys
import time
from pathlib import Path

SCRIPT = [
    # Parte I — modellazione
    "cap01_modelli.py",
    "cap02_logica.py",
    "cap03_legami.py",
    "cap04_bound.py",
    "cap05_euristiche.py",
    "cap06_gurobi.py",
    # Parte II — i problemi
    "fam07_1_assegnamento.py",
    "fam07_2_costofisso.py",
    "fam07_3_selezione.py",
    "fam07_4_parallelo.py",
    "fam07_5_classisetup.py",
    "fam07_6_classipremio.py",
    "fam07_7_ritardo.py",
    "fam08_1_capacitata.py",
    "fam08_2_pmediana.py",
    "fam08_3_copertura.py",
    "fam08_4_hub.py",
    "fam09_1_lotti.py",
    "fam09_2_manodopera.py",
    "fam09_3_veicoli.py",
    "fam10_1_premi.py",
    "fam10_3_dieta.py",
    "fam10_2_asta.py",
    "fam10_6_campi.py",
    "fam10_7_antitrust.py",
    "fam10_8_cd.py",
    "fam10_9_scaffali.py",
    "fam10_4_luci.py",
    "fam10_5_spedizioni.py",
    # i quindici modelli numerici
    "ex01_furgone.py",
    "ex02_linee.py",
    "ex03_staffetta.py",
    "ex04_scarpe.py",
    "ex05_veicoli.py",
    "ex06_hub.py",
    "ex07_aerei.py",
    "ex08_seminari.py",
    "ex09_regine.py",
    "ex10_utensili.py",
    "ex11_bilanciamento.py",
    "ex12_scarpe_soglia.py",
    "ex13_fondi.py",
    "ex14_turni.py",
    "ex15_orario.py",
]

base = Path(__file__).resolve().parent
inizio = time.time()
for s in SCRIPT:
    print(f"\n{'#' * 72}\n# {s}\n{'#' * 72}")
    esito = subprocess.run([sys.executable, str(base / s)], cwd=base)
    if esito.returncode != 0:
        print(f"ERRORE in {s}: interrompo.")
        sys.exit(1)
for finale, messaggio in [("genera_notebook.py", "generazione dei notebook"),
                          ("incorpora_codice.py", "incorporazione del codice nelle pagine")]:
    print(f"\n{'#' * 72}\n# {finale}\n{'#' * 72}")
    esito = subprocess.run([sys.executable, str(base / finale)], cwd=base)
    if esito.returncode != 0:
        print(f"ERRORE nella {messaggio}: interrompo.")
        sys.exit(1)

print(f"\nTutti gli script completati in {time.time() - inizio:.1f} s.")
