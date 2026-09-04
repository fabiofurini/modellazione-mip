"""Problema 7.6 -- Classi con premio di completamento e riduzione se e solo se.

Due "se e solo se": ognuno con un verso imposto dal vincolo (via CNF) e
l'altro dall'ottimo -- lo schema generale per modellare un iff.
"""
import gurobipy as gp
import numpy as np
import pandas as pd
from gurobipy import GRB

from euristiche import best_fit, first_fit, matrice, next_fit
from mip import (ammissibile, due_rilassamenti, frazione, nuovo_modello,
                 registra_bound, risolvi, stampa_soluzione, valuta)
from stile import CICLO, ROSSO, intestazione, plt, salva_dati, salva_figura

R = range

# ---------- 1. MODELLO E ISTANZA ----------
intestazione("6. Premio se tutta la classe è eseguita; riduzione u se e solo se >= 2 classi")
r6 = [10, 5, 20, 12, 10, 22]
t6 = [5, 15, 25, 15, 10, 38]
J6 = [[0, 1], [2, 3], [4, 5]]
v6 = [5, 4, 10]
a6, u6 = 50, 10
salva_dati(pd.DataFrame({"lavoro": R(1, 7), "r": r6, "t": t6,
                         "classe": [c + 1 for j in R(6) for c in R(3) if j in J6[c]]}), "sched6_lavori")
salva_dati(pd.DataFrame({"classe": R(1, 4), "v": v6}), "sched6_classi")


def coppie(J):
    return [(j, i, c, g) for c in R(len(J)) for g in R(c + 1, len(J)) for j in J[c] for i in J[g]]


def modello_6(r, t, J, v, a, u):
    n, q = len(r), len(J)
    m = nuovo_modello("classi_premio")
    x = m.addVars(n, vtype=GRB.BINARY, name="x")
    y = m.addVars(q, vtype=GRB.BINARY, name="y")
    z = m.addVar(vtype=GRB.BINARY, name="z")
    m.setObjective(gp.quicksum(r[j] * x[j] for j in R(n)) + gp.quicksum(v[c] * y[c] for c in R(q)),
                   GRB.MAXIMIZE)
    m.addConstrs((x[j] - y[c] >= 0 for c in R(q) for j in J[c]), name="tutti")
    m.addConstrs((x[j] + x[i] - z <= 1 for (j, i, c, g) in coppie(J)), name="miste")
    m.addConstr(gp.quicksum(t[j] * x[j] for j in R(n)) + u * z <= a, name="disponibilita")
    return m, x, y, z


def duale_6(r, t, J, v, a, u):
    """min sum lam_ji + a mu;  pi_j + sum lam + t_j mu >= r_j;  -sum_{J_c} pi_j >= v_c;
    -sum lam + u mu >= 0;  pi <= 0, lam >= 0, mu >= 0."""
    n, q = len(r), len(J)
    cp = coppie(J)
    d = nuovo_modello("duale_classi_premio")
    pi = d.addVars(n, lb=-GRB.INFINITY, ub=0.0, name="pi")
    lam = d.addVars([(j, i) for (j, i, _, _) in cp], name="lam")
    mu = d.addVar(name="mu")
    d.setObjective(lam.sum() + a * mu, GRB.MINIMIZE)
    for j in R(n):
        d.addConstr(pi[j] + gp.quicksum(lam[jj, ii] for (jj, ii, _, _) in cp if jj == j or ii == j)
                    + t[j] * mu >= r[j], name=f"rc_x[{j}]")
    d.addConstrs((-gp.quicksum(pi[j] for j in J[c]) >= v[c] for c in R(q)), name="rc_y")
    d.addConstr(-lam.sum() + u * mu >= 0, name="rc_z")
    return d


def euristica_6(r, t, J, v, a, u):
    """Classe per classe: dalla seconda classe in poi il primo lavoro paga anche la riduzione u."""
    n, q = len(r), len(J)
    x, y, z, ra, passi = [0] * n, [0] * q, 0, a, []
    for c in R(q):
        cnt = 0
        for j in J[c]:
            if c == 0 or z == 1:
                if t[j] <= ra:
                    x[j], ra, cnt = 1, ra - t[j], cnt + 1
                    passi.append(f"Classe {c + 1}: t[{j + 1}] = {t[j]} <= ra; x[{j + 1}] = 1, ra = {ra}.")
                else:
                    passi.append(f"Classe {c + 1}: t[{j + 1}] = {t[j]} > ra = {ra}; il lavoro {j + 1} viene saltato.")
            else:
                if t[j] + u <= ra:
                    x[j], z, ra, cnt = 1, 1, ra - t[j] - u, cnt + 1
                    passi.append(f"Classe {c + 1}, riduzione non ancora applicata: t[{j + 1}] + u = {t[j] + u} <= ra; "
                                 f"x[{j + 1}] = 1, z = 1, ra = {ra}.")
                else:
                    passi.append(f"Classe {c + 1}, riduzione non ancora applicata: t[{j + 1}] + u = {t[j] + u} > ra = {ra}; "
                                 f"il lavoro {j + 1} viene saltato.")
        if cnt == len(J[c]):
            y[c] = 1
            passi.append(f"Tutti i lavori della classe {c + 1} sono eseguiti: y[{c + 1}] = 1 (premio v = {v[c]}).")
    return x, y, z, passi


m6, x6, y6, z6 = modello_6(r6, t6, J6, v6, a6, u6)

# ---------- 2. EURISTICA COSTRUTTIVA (LOWER BOUND) ----------
xe, ye, ze, passi = euristica_6(r6, t6, J6, v6, a6, u6)
print("Euristica classe per classe:")
for i, s in enumerate(passi, 1):
    print(f"  Passo {i}. {s}")
lb6 = sum(r6[j] * xe[j] for j in R(6)) + sum(v6[c] * ye[c] for c in R(3))
print(f"  lb = {lb6}  (x = {xe}, y = {ye}, z = {ze})")

# ---------- 3. RILASSAMENTO LP E DUALE (UPPER BOUND) ----------
d6 = duale_6(r6, t6, J6, v6, a6, u6)
pi_mano = {f"pi[{J6[c][0]}]": -v6[c] for c in R(3)}      # il primo lavoro di ogni classe porta il premio
mu_mano = max((r6[j] - pi_mano.get(f"pi[{j}]", 0)) / t6[j] for j in R(6))
mano = dict(pi_mano, mu=mu_mano)
ub6, viol = valuta(d6, mano)
assert viol <= 1e-9
print(f"Soluzione duale a mano: pi_1 = -5, pi_3 = -4, pi_5 = -10, lam = 0, "
      f"mu = max_j (r_j - pi_j)/t_j = {frazione(mu_mano)}  ->  ub = {frazione(ub6)}")
zlp6, zlp6r, _ = due_rilassamenti(m6, d6)

# ---------- 4. SOLUZIONE OTTIMA DEL MILP ----------
z6v = risolvi(m6)
print("Soluzione ottima del MILP:")
stampa_soluzione(m6, solo_non_nulle=True)
riga = registra_bound("6 classi premio", ub6, lb6, zlp6, zlp6r, z6v, senso="max")
salva_dati(pd.DataFrame([riga]), "sched6_bound")

# ---------- 5. DOMANDE DI MODELLAZIONE AGGIUNTIVE ----------


varianti = {}


def variante(nome, m):
    z = risolvi(m)
    print(f"  {nome:70s} z = {frazione(z)}")
    return z

# 6a: almeno un lavoro per classe
m, x, y, z = modello_6(r6, t6, J6, v6, a6, u6)
m.addConstrs((gp.quicksum(x[j] for j in J6[c]) >= 1 for c in R(3)), name="almeno_uno")
varianti["6a"] = variante("6a. Almeno un lavoro per classe (quindi z = 1)", m)
# 6b: penalità w per classe iniziata e non completata
w6 = 3
m, x, y, z = modello_6(r6, t6, J6, v6, a6, u6)
st = m.addVars(3, vtype=GRB.BINARY, name="s")
m.addConstrs((st[c] >= x[j] for c in R(3) for j in J6[c]), name="iniziata")
m.update()
m.setObjective(m.getObjective() - w6 * gp.quicksum(st[c] - y[c] for c in R(3)), GRB.MAXIMIZE)
varianti["6b"] = variante("6b. Penalità 3 per classe iniziata e non completata (s_c >= x_j)", m)
salva_dati(pd.DataFrame({"variante": list(varianti), "z": list(varianti.values())}), "sched6_varianti")

print("Fine.")
