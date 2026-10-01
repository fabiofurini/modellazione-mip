"""Problema 7.3 -- Selezione di lavori con ricavo e macchine a costo fisso.

Stesso legame di attivazione del problema 7.2, letto in un problema di
massimo: l'euristica da' un lower bound, il duale un upper bound -- i ruoli
si scambiano rispetto ai problemi di minimo.
"""
import gurobipy as gp
import numpy as np
import pandas as pd
from gurobipy import GRB

from euristiche import best_fit, first_fit, matrice, next_fit
from mip import (ammissibile, dualita_forte, due_rilassamenti, frazione,
                 nuovo_modello, registra_bound, rilassamenti, risolvi,
                 stampa_soluzione, valuta)
from stile import CICLO, ROSSO, intestazione, plt, salva_dati, salva_figura
from esteso import salva_modello

R = range

# ---------- 1. MODELLO E ISTANZA ----------
intestazione("3. Selezione di lavori: massimo profitto = ricavi - costi fissi")
t3 = [25, 40, 75]
r3 = [10, 15, 30]
c3 = [20, 30, 15]
a3 = [105, 110, 100]
salva_dati(pd.DataFrame({"lavoro": R(1, 4), "t": t3, "r": r3}), "fam07_3_lavori")
salva_dati(pd.DataFrame({"macchina": R(1, 4), "c": c3, "a": a3}), "fam07_3_macchine")


def modello_3(t, r, c, a):
    n, k = len(t), len(a)
    m = nuovo_modello("selezione")
    x = m.addVars(n, k, vtype=GRB.BINARY, name="x")
    y = m.addVars(k, vtype=GRB.BINARY, name="y")
    m.setObjective(gp.quicksum(r[j] * x[j, mm] for j in R(n) for mm in R(k))
                   - gp.quicksum(c[mm] * y[mm] for mm in R(k)), GRB.MAXIMIZE)
    m.addConstrs((x.sum(j, "*") <= 1 for j in R(n)), name="al_piu_una")
    m.addConstrs((gp.quicksum(t[j] * x[j, mm] for j in R(n)) - a[mm] * y[mm] <= 0 for mm in R(k)),
                 name="link")
    return m, x, y


def duale_3(t, r, c, a):
    """min sum mu_j;  mu_j + t_j pi_m >= r_j;  -a_m pi_m >= -c_m;  mu, pi >= 0."""
    n, k = len(t), len(a)
    d = nuovo_modello("duale_selezione")
    mu = d.addVars(n, name="mu")
    pi = d.addVars(k, name="pi")
    d.setObjective(mu.sum(), GRB.MINIMIZE)
    d.addConstrs((mu[j] + t[j] * pi[mm] >= r[j] for j in R(n) for mm in R(k)), name="rc_x")
    d.addConstrs((-a[mm] * pi[mm] >= -c[mm] for mm in R(k)), name="rc_y")
    return d


def valore_3(e, r, c):
    return sum(r[j] for (j, mm) in e.x) - sum(c[mm] * y for mm, y in enumerate(e.y))


m3, x3, y3 = modello_3(t3, r3, c3, a3)
salva_modello(m3, "fam07_3_primale")

# ---------- 2. IL RILASSAMENTO LP ----------
zlp3, zlp3r, _ = rilassamenti(m3)

# ---------- 3. IL DUALE DEL RILASSAMENTO (LOWER BOUND) ----------
d3 = duale_3(t3, r3, c3, a3)
salva_modello(d3, "fam07_3_duale")
mano = {f"pi[{mm}]": c3[mm] / a3[mm] for mm in R(3)}
mano.update({f"mu[{j}]": max([0] + [r3[j] - t3[j] * c3[mm] / a3[mm] for mm in R(3)]) for j in R(3)})
ub3, viol = valuta(d3, mano)
assert viol <= 1e-9
print("Soluzione duale a mano: pi_m = c_m/a_m; mu_j = max{0, r_j - t_j pi_m} = "
      + ", ".join(frazione(mano[f"mu[{j}]"]) for j in R(3)) + f"  ->  ub = {frazione(ub3)}")
dualita_forte(d3, zlp3)

# ---------- 4. EURISTICA COSTRUTTIVA (UPPER BOUND) ----------
T3 = matrice(t3, 3)
eur3 = [("next-fit (salta se non ci sta)", next_fit(T3, a3, salta=True)),
        ("first-fit", first_fit(T3, a3, salta=True)),
        ("best-fit (macchina più piena)", best_fit(T3, a3, lambda j, mm, ra: ra[mm], "ra", salta=True))]
print("Euristiche costruttive (qui danno un LOWER bound: il problema è di massimo):")
for nome, e in eur3:
    print(f"  {nome:32s} lb = {valore_3(e, r3, c3):3d}")
print("Esecuzione passo-passo del best-fit:")
eur3[2][1].traccia.stampa()
lb3 = max(valore_3(e, r3, c3) for _, e in eur3)

# ---------- 5. SOLUZIONE OTTIMA DEL MILP ----------
z3 = risolvi(m3)
print("Soluzione ottima del MILP:")
stampa_soluzione(m3, solo_non_nulle=True)
riga = registra_bound("3 selezione", ub3, lb3, zlp3, zlp3r, z3, senso="max")
salva_dati(pd.DataFrame([riga]), "fam07_3_bound")

# ---------- 6. DOMANDE DI MODELLAZIONE AGGIUNTIVE ----------


varianti = {}


def variante(nome, m):
    z = risolvi(m)
    print(f"  {nome:70s} z = {frazione(z)}")
    return z

# 3a: tutti i lavori devono essere eseguiti (torna il vincolo di assegnamento)
m, x, y = modello_3(t3, r3, c3, a3)
m.addConstrs((x.sum(j, "*") == 1 for j in R(3)), name="tutti")
varianti["3a"] = variante("3a. Tutti i lavori eseguiti (sum_m x_jm = 1)", m)
# 3b: il lavoro 3 solo se il lavoro 2
m, x, y = modello_3(t3, r3, c3, a3)
m.addConstr(x.sum(2, "*") <= x.sum(1, "*"), name="3_solo_se_2")
varianti["3b"] = variante("3b. Il lavoro 3 si esegue solo se si esegue il lavoro 2", m)
salva_dati(pd.DataFrame({"variante": list(varianti), "z": list(varianti.values())}), "fam07_3_varianti")

# ---------- 7. IL SANDWICH SULLA VARIANTE 3b ----------
intestazione("3b. Il sandwich sulla variante: il lavoro 3 solo se anche il lavoro 2")


def modello_3b(t, r, c, a):
    mm_, xx, yy = modello_3(t, r, c, a)
    mm_.addConstr(xx.sum(2, "*") - xx.sum(1, "*") <= 0, name="3_solo_se_2")
    return mm_, xx, yy


def duale_3b(t, r, c, a):
    """Al duale di 7.3 si aggiunge lambda >= 0 per il vincolo
    sum_m x_3m - sum_m x_2m <= 0: compare con segno piu' nelle colonne del
    lavoro 3 e con segno meno in quelle del lavoro 2. Il termine noto e' zero,
    quindi l'obiettivo resta min sum_j mu_j."""
    nn, kk = len(t), len(a)
    d = nuovo_modello("duale_selezione_3b")
    mu = d.addVars(nn, name="mu")
    pi = d.addVars(kk, name="pi")
    lam = d.addVar(name="lambda")
    d.setObjective(mu.sum(), GRB.MINIMIZE)
    for mz in R(kk):
        d.addConstr(mu[0] + t[0] * pi[mz] >= r[0], name=f"rc_x0{mz}")
        d.addConstr(mu[1] + t[1] * pi[mz] - lam >= r[1], name=f"rc_x1{mz}")
        d.addConstr(mu[2] + t[2] * pi[mz] + lam >= r[2], name=f"rc_x2{mz}")
    d.addConstrs((-a[mz] * pi[mz] >= -c[mz] for mz in R(kk)), name="rc_y")
    return d


m3b, x3b, y3b = modello_3b(t3, r3, c3, a3)
salva_modello(m3b, "fam07_3b_primale")

# -- euristica ammissibile: la base, riparata togliendo il lavoro 3 se il 2 manca --
print("Euristica costruttiva: si parte dalla soluzione del problema base e, se esegue il")
print("lavoro 3 senza il 2, si toglie il lavoro 3 (la riparazione e' sempre ammissibile).")
e_base3 = max((e for _, e in eur3), key=lambda e: valore_3(e, r3, c3))
scelti = {j for (j, _) in e_base3.x}
print(f"  soluzione base: lavori {sorted(j + 1 for j in scelti)}, valore "
      f"{frazione(valore_3(e_base3, r3, c3))}")
tenuti = [(j, mz) for (j, mz) in e_base3.x if not (j == 2 and 1 not in scelti)]
macchine = sorted({mz for (_, mz) in tenuti})
lb3b = sum(r3[j] for (j, _) in tenuti) - sum(c3[mz] for mz in macchine)
sol_3b = {f"x[{j},{mz}]": 1 for (j, mz) in tenuti} | {f"y[{mz}]": 1 for mz in macchine}
assert ammissibile(m3b, sol_3b), "la soluzione euristica della variante deve essere ammissibile"
print(f"  dopo la riparazione: lavori {sorted(j + 1 for (j, _) in tenuti)}  ->  "
      f"lb = {frazione(lb3b)}")

# -- certificato duale: lambda sposta valore dal lavoro 3 al lavoro 2 --
d3b = duale_3b(t3, r3, c3, a3)
salva_modello(d3b, "fam07_3b_duale")
pi_b = {mz: c3[mz] / a3[mz] for mz in R(3)}
# il lambda piu' grande che non costringe mu_2 a crescere: mu_2 resta a zero
# finche' lambda <= min_m (t_2 pi_m - r_2); oltre, quello che si guadagna su mu_3
# si ripaga su mu_2, quindi ci si ferma li'.
lam_b = max(0.0, min(t3[1] * pi_b[mz] - r3[1] for mz in R(3)))
mano_3b = {f"pi[{mz}]": pi_b[mz] for mz in R(3)} | {"lambda": lam_b}
mano_3b["mu[0]"] = max([0] + [r3[0] - t3[0] * pi_b[mz] for mz in R(3)])
mano_3b["mu[1]"] = max([0] + [r3[1] + lam_b - t3[1] * pi_b[mz] for mz in R(3)])
mano_3b["mu[2]"] = max([0] + [r3[2] - lam_b - t3[2] * pi_b[mz] for mz in R(3)])
ub3b, viol_3b = valuta(d3b, mano_3b)
assert viol_3b <= 1e-9, viol_3b
print("Soluzione duale a mano: pi_m = c_m/a_m come nel problema base; poi si alza lambda")
print("  fin dove il lavoro 2 lo regge a costo zero, cioe' lambda = min_m (t_2 pi_m - r_2).")
if lam_b > 0:
    print(f"  Qui lambda = {frazione(lam_b)}: sconta il lavoro 3 senza far crescere mu_2.")
else:
    print("  Qui quel minimo e' negativo, quindi lambda resta a zero: sul lavoro 2 non c'e'")
    print("  margine da spendere, e il certificato della variante coincide con quello del")
    print("  problema base. L'implicazione alza l'ottimo intero ma non tocca il rilassamento.")
print(f"  ->  ub = {frazione(ub3b)}")
zlp3b, zlp3br, _ = due_rilassamenti(m3b, d3b)
z3b = risolvi(m3b)
riga_3b = registra_bound("3b lavoro 3 solo con il lavoro 2", ub3b, lb3b, zlp3b, zlp3br, z3b,
                         senso="max")
salva_dati(pd.DataFrame([riga_3b]), "fam07_3b_bound")
assert lb3b <= z3b <= zlp3b + 1e-9 <= ub3b + 1e-9


print("Fine.")
