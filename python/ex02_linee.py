"""EX 2 -- Linee di autobus: assegnamento con capacita' due (famiglia 7).

Quattro linee, tre compagnie, ogni linea a una compagnia, ogni compagnia al piu'
due linee. E' l'assegnamento generalizzato del problema 7.1 con capacita' in
numero di lavori invece che in tempo. Modello, euristica, duale del rilassamento
puro con soluzione costruita a mano, ottimo e tabella dei bound.
"""
import gurobipy as gp
import pandas as pd
from gurobipy import GRB

from mip import (ammissibile, due_rilassamenti, frazione, nuovo_modello, registra_bound,
                 risolvi, stampa_soluzione, valuta)
from stile import intestazione, plt, salva_dati, salva_figura

R = range

# ---------- 1. MODELLO E ISTANZA ----------
intestazione("EX 2. Linee di autobus: quattro linee, tre compagnie, al piu' due linee ciascuna")
c = [[10, 4, 9, 7],      # costo della compagnia 1 sulle quattro linee
     [1, 2, 3, 10],
     [8, 9, 10, 1]]
nc, nl, p = 3, 4, 2      # compagnie, linee, linee al piu' per compagnia
salva_dati(pd.DataFrame([{"compagnia": i + 1, "linea": j + 1, "c": c[i][j]}
                         for i in R(nc) for j in R(nl)]), "ex02_costi")


def modello(c, p):
    nc, nl = len(c), len(c[0])
    m = nuovo_modello("linee_autobus")
    x = m.addVars(nc, nl, vtype=GRB.BINARY, name="x")
    m.setObjective(gp.quicksum(c[i][j] * x[i, j] for i in R(nc) for j in R(nl)), GRB.MINIMIZE)
    m.addConstrs((x.sum("*", j) == 1 for j in R(nl)), name="linea")
    m.addConstrs((x.sum(i, "*") <= p for i in R(nc)), name="capacita")
    return m, x


def duale(c, p):
    """max sum_j alpha_j + p sum_i beta_i;  alpha_j + beta_i <= c_ij;  alpha libera, beta <= 0."""
    nc, nl = len(c), len(c[0])
    d = nuovo_modello("duale_linee")
    alpha = d.addVars(nl, lb=-GRB.INFINITY, name="alpha")
    beta = d.addVars(nc, lb=-GRB.INFINITY, ub=0.0, name="beta")
    d.setObjective(alpha.sum() + p * beta.sum(), GRB.MAXIMIZE)
    d.addConstrs((alpha[j] + beta[i] <= c[i][j] for i in R(nc) for j in R(nl)), name="rc")
    return d


m, x = modello(c, p)

# ---------- 2. EURISTICA COSTRUTTIVA (UPPER BOUND) ----------
# euristica costruttiva sulle linee: ogni linea alla compagnia piu' economica fra quelle non sature
residuo = [p] * nc
scelta = {}
for j in R(nl):
    i = min((i for i in R(nc) if residuo[i] > 0), key=lambda i: (c[i][j], i))
    scelta[j] = i
    residuo[i] -= 1
    print(f"  Linea {j + 1}: compagnie con posti liberi "
          + ", ".join(f"{k + 1} (costo {c[k][j]})" for k in R(nc) if residuo[k] > 0 or k == i)
          + f"; la piu' economica e' la {i + 1}, quindi x[{i + 1}][{j + 1}] = 1")
ub = sum(c[scelta[j]][j] for j in R(nl))
sol_eur = {f"x[{scelta[j]},{j}]": 1 for j in R(nl)}
assert ammissibile(m, sol_eur)
print(f"  Soluzione euristica: " + ", ".join(f"linea {j + 1} -> compagnia {scelta[j] + 1}"
                                             for j in R(nl))
      + f"   ub = {frazione(ub)}")

# ---------- 3. RILASSAMENTO LP E DUALE (LOWER BOUND) ----------
d = duale(c, p)
mano = {f"alpha[{j}]": min(c[i][j] for i in R(nc)) for j in R(nl)}   # beta = 0
lb, viol = valuta(d, mano)
assert viol <= 1e-9, viol
print("  Duale a mano (beta = 0): alpha_j = min_i c_ij = "
      + ", ".join(frazione(mano[f"alpha[{j}]"]) for j in R(nl)) + f"  ->  lb = {frazione(lb)}")
zlp, zlpr, pi = due_rilassamenti(m, d)

# ---------- 4. OTTIMO DEL MILP E TABELLA DEI BOUND ----------
z = risolvi(m)
ott = [(i, j) for i in R(nc) for j in R(nl) if x[i, j].X > 0.5]
print("  Soluzione ottima: " + ", ".join(f"linea {j + 1} -> compagnia {i + 1}" for i, j in sorted(ott, key=lambda t: t[1])))
riga = registra_bound("EX 2 linee di autobus", ub, lb, zlp, zlpr, z)
salva_dati(pd.DataFrame([riga]), "ex02_bound")
assert lb <= zlp <= z <= ub + 1e-9

# ---------- 5. FIGURA ----------
fig, ax = plt.subplots(figsize=(6.4, 2.8))
for i in R(nc):
    linee = [j for (ii, j) in ott if ii == i]
    ax.barh(i, len(linee), color=["#0E7490", "#C0392B", "#CA6F1E"][i], height=0.55)
    if linee:
        ax.annotate("linee " + ", ".join(str(j + 1) for j in linee) +
                    f"  (costo {sum(c[i][j] for j in linee)})",
                    (0.06, i), va="center", fontsize=9, color="white")
ax.axvline(p, color="#16324A", ls="--", lw=1.4)
ax.annotate(f"al più {p}", (p, -0.55), ha="center", fontsize=9, color="#16324A")
ax.set_yticks(R(nc))
ax.set_yticklabels([f"compagnia {i + 1}" for i in R(nc)])
ax.set_xlabel("numero di linee assegnate")
ax.set_xlim(0, p + 0.6)
ax.set_title(f"EX 2: soluzione ottima (z = {frazione(z)})")
ax.invert_yaxis()
salva_figura(fig, "ex02_ottimo")
print("Fine.")
