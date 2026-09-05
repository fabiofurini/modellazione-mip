"""EX 1 -- Furgone da otto posti: quale gruppo di turisti accettare (famiglia 10).

Uno zaino con due vincoli in piu': al piu' due gruppi accettati e l'implicazione
«se accetto il gruppo 2 devo accettare anche il 4». E' l'occasione per vedere in
un caso minuscolo tutte e tre le tecniche del capitolo 3 che servono qui:
capacita' (3.1), conteggio (3.4) e precedenza logica (3.9).
"""
import gurobipy as gp
import pandas as pd
from gurobipy import GRB

from mip import (ammissibile, due_rilassamenti, frazione, nuovo_modello, registra_bound,
                 risolvi, stampa_lp, valuta)
from stile import ARANCIO, GRIGIO, TEAL, intestazione, plt, salva_dati, salva_figura

R = range

# ---------- 1. MODELLO E ISTANZA ----------
intestazione("EX 1. Furgone da otto posti: quali gruppi accettare")
a0 = [2, 3, 4, 5]          # persone di ciascun gruppo
p0 = [30, 50, 80, 70]      # offerta in euro
K0 = 8                     # posti del furgone
G0 = 2                     # al piu' due gruppi
IMP = (1, 3)               # se accetto il gruppo 2 (indice 1) devo accettare il 4 (indice 3)
n0 = len(a0)
salva_dati(pd.DataFrame({"gruppo": R(1, n0 + 1), "persone": a0, "offerta": p0}), "ex01_dati")


def modello(a, p, K, G, imp):
    n = len(a)
    m = nuovo_modello("furgone")
    x = m.addVars(n, vtype=GRB.BINARY, name="x")
    m.setObjective(gp.quicksum(p[j] * x[j] for j in R(n)), GRB.MAXIMIZE)
    m.addConstr(gp.quicksum(a[j] * x[j] for j in R(n)) <= K, name="posti")
    m.addConstr(gp.quicksum(x[j] for j in R(n)) <= G, name="gruppi")
    m.addConstr(x[imp[0]] - x[imp[1]] <= 0, name="implicazione")
    return m, x


def duale(a, p, K, G, imp):
    """min K alpha + G beta  s.t.  a_j alpha + beta (+gamma se j=2, -gamma se j=4) >= p_j."""
    n = len(a)
    d = nuovo_modello("duale_furgone")
    alpha = d.addVar(name="alpha")     # posti
    beta = d.addVar(name="beta")       # numero di gruppi
    gamma = d.addVar(name="gamma")     # implicazione
    d.setObjective(K * alpha + G * beta, GRB.MINIMIZE)
    for j in R(n):
        segno = 1 if j == imp[0] else (-1 if j == imp[1] else 0)
        d.addConstr(a[j] * alpha + beta + segno * gamma >= p[j], name=f"rc[{j}]")
    return d


m0, x0 = modello(a0, p0, K0, G0, IMP)
print("  Il modello dell'istanza:")
stampa_lp(m0)

# ---------- 2. EURISTICA COSTRUTTIVA (LOWER BOUND) ----------
# euristica costruttiva sull'offerta decrescente: si accetta un gruppo solo se tutti i vincoli
# restano soddisfatti, implicazione compresa (il gruppo 2 entra solo col 4 gia' dentro)
def euristica(a, p, K, G, imp):
    n = len(a)
    x = [0] * n
    passi = []
    for j in sorted(R(n), key=lambda j: (-p[j], j)):
        x[j] = 1
        posti = sum(a[k] * x[k] for k in R(n))
        gruppi = sum(x)
        ok_imp = x[imp[0]] <= x[imp[1]]
        motivi = []
        if posti > K:
            motivi.append(f"servirebbero {posti} posti su {K}")
        if gruppi > G:
            motivi.append(f"sarebbero {gruppi} gruppi su {G}")
        if not ok_imp:
            motivi.append(f"il gruppo {imp[0] + 1} obbliga ad accettare il {imp[1] + 1}")
        if motivi:
            x[j] = 0
            passi.append(f"gruppo {j + 1} (offerta {p[j]}): scartato, " + "; ".join(motivi))
        else:
            passi.append(f"gruppo {j + 1} (offerta {p[j]}): accettato "
                         f"({posti} posti occupati, {gruppi} gruppi)")
    return x, passi


x_eur, passi = euristica(a0, p0, K0, G0, IMP)
for k, riga in enumerate(passi, 1):
    print(f"  Passo {k}. {riga}")
lb0 = sum(p0[j] * x_eur[j] for j in R(n0))
sol_eur = {f"x[{j}]": x_eur[j] for j in R(n0)}
assert ammissibile(m0, sol_eur), sol_eur
print(f"  Soluzione euristica: gruppi {[j + 1 for j in R(n0) if x_eur[j]]}   "
      f"lb = {frazione(lb0)}")

# ---------- 3. RILASSAMENTO LP E DUALE (UPPER BOUND) ----------
d0 = duale(a0, p0, K0, G0, IMP)
# ricetta: si valutano solo i posti (beta = gamma = 0) al prezzo per posto piu' alto
alpha_min = max(p0[j] / a0[j] for j in R(n0))
mano = {"alpha": alpha_min, "beta": 0.0, "gamma": 0.0}
ub0, viol = valuta(d0, mano)
assert viol <= 1e-9, viol
print("  Duale a mano: beta = gamma = 0 e alpha = max_j p_j / a_j (il posto vale quanto il")
print("  gruppo che lo paga meglio), cosi' ogni vincolo a_j alpha >= p_j e' soddisfatto:")
for j in R(n0):
    print(f"    gruppo {j + 1}: {p0[j]} / {a0[j]} = {frazione(p0[j] / a0[j])}")
print(f"  alpha = {frazione(alpha_min)}  ->  ub = {K0} * alpha = {frazione(ub0)}")
zlp0, zlp0r, _ = due_rilassamenti(m0, d0)

# ---------- 4. OTTIMO DEL MILP E TABELLA DEI BOUND ----------
z0 = risolvi(m0)
acc = [j + 1 for j in R(n0) if x0[j].X > 0.5]
print(f"  Soluzione ottima: gruppi {acc}, "
      f"{int(sum(a0[j] * x0[j].X for j in R(n0)))} posti occupati su {K0}, incasso "
      f"{frazione(z0)}")
riga = registra_bound("EX 1 furgone", ub0, lb0, zlp0, zlp0r, z0, senso="max")
salva_dati(pd.DataFrame([riga]), "ex01_bound")
assert lb0 <= z0 <= zlp0r <= zlp0 <= ub0 + 1e-9

# ---------- 5. A COSA SERVE OGNI VINCOLO ----------
intestazione("EX 1. Il contributo di ciascun vincolo")
prove = []
for nome, togli in [("modello completo", []), ("senza il limite sui gruppi", ["gruppi"]),
                    ("senza l'implicazione", ["implicazione"]),
                    ("senza entrambi", ["gruppi", "implicazione"])]:
    m, x = modello(a0, p0, K0, G0, IMP)
    m.update()
    for c in list(m.getConstrs()):
        if c.ConstrName in togli:
            m.remove(c)
    m.update()
    z = risolvi(m)
    scelti = [j + 1 for j in R(n0) if x[j].X > 0.5]
    print(f"  {nome:32s} z = {frazione(z):>4}   gruppi {scelti}")
    prove.append({"variante": nome, "z": z, "gruppi": " ".join(map(str, scelti))})
salva_dati(pd.DataFrame(prove), "ex01_vincoli")
assert prove[0]["z"] <= prove[1]["z"] and prove[0]["z"] <= prove[2]["z"]

# ---------- 6. FIGURA ----------
fig, ax = plt.subplots(figsize=(6.4, 2.9))
idx = list(R(n0))
colori = [TEAL if x0[j].X > 0.5 else GRIGIO for j in idx]
ax.bar(idx, p0, 0.55, color=colori)
for j in idx:
    if x_eur[j]:
        ax.plot(j, p0[j] + 3, marker="v", color=ARANCIO, ms=8)
    ax.annotate(f"{a0[j]} posti", (j, 3), ha="center", fontsize=8, color="white")
ax.plot([], [], marker="v", ls="", color=ARANCIO, label="scelto dall'euristica")
ax.bar([], [], color=TEAL, label="accettato all'ottimo")
ax.bar([], [], color=GRIGIO, label="rifiutato all'ottimo")
ax.set_xticks(idx)
ax.set_xticklabels([f"gruppo {j + 1}" for j in idx])
ax.set_ylabel("offerta (euro)")
ax.set_title(f"EX 1: euristica {frazione(lb0)} <= ottimo {frazione(z0)} <= duale {frazione(ub0)}")
ax.legend(fontsize=8, loc="upper left")
salva_figura(fig, "ex01_ottimo")
print("Fine.")
