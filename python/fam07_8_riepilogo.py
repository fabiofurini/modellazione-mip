"""Capitolo 7 -- Il quadro dei bound sui sette problemi.

Non e' un problema a se': raccoglie i bound gia' calcolati dai sette script
`fam07_1_...py`--`fam07_7_...py` (ognuno scrive la propria riga in
`dati/schedN_bound.csv`) e disegna il confronto. Va eseguito dopo gli altri
sette -- da soli in Colab non trovano nulla da leggere.
"""
import pandas as pd

from stile import BLU, DIR_DATI, GRIGIO, TEAL, plt, salva_dati, salva_figura

R = range

# ---------- 1. LETTURA DEI BOUND DEI SETTE PROBLEMI ----------

righe = [pd.read_csv(DIR_DATI / f"sched{i}_bound.csv") for i in R(1, 8)]
df = pd.concat(righe, ignore_index=True)
salva_dati(df, "sched_bound")
print(df.to_string(index=False))

varianti = [pd.read_csv(DIR_DATI / f"sched{i}_varianti.csv") for i in R(1, 8)]
salva_dati(pd.concat(varianti, ignore_index=True), "sched_varianti")

# ---------- 2. FIGURA: IL SANDWICH DEI BOUND ----------

fig, ax = plt.subplots(figsize=(7.2, 3.6))
for i, riga in df.iterrows():
    ax.plot([riga.lb, riga.ub], [i, i], color=GRIGIO, lw=3, solid_capstyle="round")
    ax.plot(riga.z_lp, i, marker="|", color=TEAL, ms=14, mew=2)
    ax.plot(riga.z_milp, i, marker="o", color=BLU, ms=7)
ax.set_yticks(R(len(df)))
ax.set_yticklabels(df.problema)
ax.invert_yaxis()
ax.set_xlabel("valore; segmento grigio = [lb, ub], barra teal = z(LP), punto = z(MILP)")
ax.set_title("Il sandwich dei bound sui sette problemi")
salva_figura(fig, "cap07_bound")
print("Fine.")
