"""EX 6 -- Hub-and-spoke: il minimo numero di hub che copre otto citta' (famiglia 8).

Un set covering puro, con tutti i costi pari a 1: si minimizza il numero di hub.
Il duale e' il "packing frazionario" dei clienti, e la euristica costruttiva duale sulle citta'
qui trova un bound che coincide con l'ottimo.
"""
import gurobipy as gp
import pandas as pd
from gurobipy import GRB

from euristiche import euristica_copertura
from mip import (ammissibile, due_rilassamenti, frazione, nuovo_modello, registra_bound,
                 risolvi, valuta)
from stile import intestazione, plt, salva_dati, salva_figura

R = range

# ---------- 1. MODELLO E ISTANZA ----------
intestazione("EX 6. Hub-and-spoke: il minimo numero di hub entro 1000 miglia da ogni citta'")
CITTA = ["Atlanta", "Chicago", "Denver", "Houston", "Los Angeles", "New York",
         "San Francisco", "Seattle"]
# copre[i] = citta' che, se scelte come hub, coprono la citta' i (entro 1000 miglia)
copre = [[0, 1, 3, 5],      # Atlanta: Atlanta, Chicago, Houston, New York
         [0, 1, 5],         # Chicago
         [2, 4],            # Denver
         [0, 3],            # Houston
         [2, 4, 6],         # Los Angeles
         [0, 1, 5],         # New York
         [4, 6, 7],         # San Francisco
         [6, 7]]            # Seattle
n = len(CITTA)
salva_dati(pd.DataFrame([{"citta": CITTA[i], "coperta_da": ", ".join(CITTA[j] for j in copre[i])}
                         for i in R(n)]), "ex06_copertura")


def modello(copre):
    n = len(copre)
    m = nuovo_modello("hub_spoke")
    y = m.addVars(n, vtype=GRB.BINARY, name="y")
    m.setObjective(y.sum(), GRB.MINIMIZE)
    m.addConstrs((gp.quicksum(y[j] for j in copre[i]) >= 1 for i in R(n)), name="copri")
    return m, y


def duale(copre):
    """max sum_i u_i;  sum_{i : j copre i} u_i <= 1 per ogni j;  u >= 0."""
    n = len(copre)
    d = nuovo_modello("duale_hub_spoke")
    u = d.addVars(n, name="u")
    d.setObjective(u.sum(), GRB.MAXIMIZE)
    d.addConstrs((gp.quicksum(u[i] for i in R(n) if j in copre[i]) <= 1 for j in R(n)),
                 name="rc")
    return d


m, y = modello(copre)

# ---------- 2. EURISTICA COSTRUTTIVA (UPPER BOUND) ----------
e = euristica_copertura([1] * n, copre)
e.traccia.stampa()
ub = e.valore
scelti = [j for j in R(n) if e.y[j]]
assert ammissibile(m, {f"y[{j}]": e.y[j] for j in R(n)})
print(f"  Soluzione euristica: hub in " + ", ".join(CITTA[j] for j in scelti)
      + f"   ub = {frazione(ub)}")

# ---------- 3. RILASSAMENTO LP E DUALE (LOWER BOUND) ----------
d = duale(copre)
# euristica costruttiva duale sulle citta': si alza u_i fino a saturare il primo vincolo duale che si oppone
residuo = [1.0] * n
mano = {}
for i in R(n):
    incremento = min(residuo[j] for j in copre[i])
    mano[f"u[{i}]"] = incremento
    for j in copre[i]:
        residuo[j] -= incremento
    print(f"  Citta' {i + 1} ({CITTA[i]}): residui degli hub che la coprono "
          + ", ".join(f"{CITTA[j]} = {frazione(residuo[j] + incremento)}" for j in copre[i])
          + f"; il minimo e' {frazione(incremento)}, quindi u_{i + 1} = {frazione(incremento)}")
lb, viol = valuta(d, mano)
assert viol <= 1e-9, viol
print(f"  Duale a mano (euristica costruttiva sulle citta'): lb = {frazione(lb)}")
zlp, zlpr, pi = due_rilassamenti(m, d)

# ---------- 4. OTTIMO DEL MILP E TABELLA DEI BOUND ----------
z = risolvi(m)
ott = [j for j in R(n) if y[j].X > 0.5]
print(f"  Soluzione ottima: {len(ott)} hub in " + ", ".join(CITTA[j] for j in ott))
for i in R(n):
    quali = [CITTA[j] for j in copre[i] if j in ott]
    assert quali, CITTA[i]
print("  Ogni citta' e' coperta da almeno un hub scelto: verificato per tutte e otto.")
riga = registra_bound("EX 6 hub-and-spoke", ub, lb, zlp, zlpr, z)
salva_dati(pd.DataFrame([riga]), "ex06_bound")
assert lb <= zlp <= z <= ub + 1e-9
if abs(lb - z) < 1e-9:
    print("  Qui il duale a mano coincide con l'ottimo intero: il bound chiude il problema")
    print("  senza bisogno del solver (tre citta' a due a due 'lontane' bastano a")
    print("  dimostrare che due hub non possono bastare).")

# ---------- 5. FIGURA ----------
fig, ax = plt.subplots(figsize=(7.2, 3.4))
altezza = [len([i for i in R(n) if j in copre[i]]) for j in R(n)]
colori = ["#0E7490" if j in ott else "#F4F6F7" for j in R(n)]
ax.bar(R(n), altezza, color=colori, edgecolor="#7F8C8D", lw=0.8)
for j in R(n):
    ax.annotate(str(altezza[j]), (j, altezza[j]), ha="center", va="bottom", fontsize=9,
                color="#16324A")
ax.set_xticks(R(n))
ax.set_xticklabels([c.replace(" ", "\n") for c in CITTA], fontsize=7.5)
ax.set_ylabel("citta' coperte se scelta come hub")
ax.set_title(f"EX 6: i {len(ott)} hub scelti (in teal) e quante citta' copre ciascuna sede")
salva_figura(fig, "ex06_ottimo")
print("Fine.")
