"""Capitolo 8 -- Il quadro dei bound sui quattro problemi.

Non e' un problema a se': raccoglie i bound gia' calcolati dai quattro script
`fam08_1_...py`--`fam08_4_...py` (ognuno scrive la propria riga in
`dati/*_bound.csv`) e disegna il confronto. Va eseguito dopo gli altri
quattro -- da solo in Colab non trova nulla da leggere.
"""
import pandas as pd

from stile import BLU, DIR_DATI, GRIGIO, TEAL, plt, salva_dati, salva_figura

R = range

# ---------- 1. LETTURA DEI BOUND DEI QUATTRO PROBLEMI ----------

PREFISSI = ["loc1", "loc2", "loc3", "hub4"]

righe = [pd.read_csv(DIR_DATI / f"{p}_bound.csv") for p in PREFISSI]
df = pd.concat(righe, ignore_index=True)
salva_dati(df, "loc_bound")
print(df.to_string(index=False))

varianti = [pd.read_csv(DIR_DATI / f"{p}_varianti.csv") for p in PREFISSI]
salva_dati(pd.concat(varianti, ignore_index=True), "loc_varianti")

# ---------- 2. FIGURA: IL SANDWICH DEI BOUND ----------

fig, ax = plt.subplots(figsize=(7.2, 3.2))
for i, riga in df.iterrows():
    ax.plot([riga.lb, riga.ub], [i, i], color=GRIGIO, lw=3, solid_capstyle="round")
    ax.plot(riga.z_lp, i, marker="|", color=TEAL, ms=14, mew=2)
    ax.plot(riga.z_milp, i, marker="o", color=BLU, ms=7)
ax.set_yticks(R(len(df)))
ax.set_yticklabels(df.problema)
ax.invert_yaxis()
ax.set_xlabel("valore; segmento grigio = [lb, ub], barra teal = z(LP), punto = z(MILP)")
ax.set_title("Il sandwich dei bound sui quattro problemi di localizzazione")
salva_figura(fig, "cap08_bound")
print("Fine.")
