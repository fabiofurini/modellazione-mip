"""Problema 7.4 -- Lavori in parallelo: il tempo di lavorazione come massimo.

Il pattern della variabile di massimo, in tre passi: imposta dal vincolo (un
lato), imposta dall'ottimo (l'altro lato), sintesi che caratterizza y_m come
il massimo dei tempi dei lavori assegnati.
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
intestazione("4. Lavori in parallelo: y_m = massimo dei tempi dei lavori assegnati")
t4 = [[6, 5, 3], [5, 10, 2], [20, 13, 10]]
p4 = [1, 2, 2]
salva_dati(pd.DataFrame([{"lavoro": j + 1, "macchina": m + 1, "t": t4[j][m]}
                         for j in R(3) for m in R(3)]), "fam07_4_lavori")
salva_dati(pd.DataFrame({"macchina": R(1, 4), "p": p4}), "fam07_4_macchine")


def modello_4(t, p):
    n, k = len(t), len(p)
    m = nuovo_modello("parallelo")
    x = m.addVars(n, k, vtype=GRB.BINARY, name="x")
    y = m.addVars(k, name="y")
    m.setObjective(y.sum(), GRB.MINIMIZE)
    m.addConstrs((x.sum(j, "*") == 1 for j in R(n)), name="assegna")
    m.addConstrs((x.sum("*", mm) <= p[mm] for mm in R(k)), name="cardinalita")
    m.addConstrs((-t[j][mm] * x[j, mm] + y[mm] >= 0 for j in R(n) for mm in R(k)), name="massimo")
    return m, x, y


def duale_4(t, p):
    """max sum mu_j + sum p_m pi_m;  mu_j + pi_m - t_jm lam_jm <= 0;  sum_j lam_jm <= 1."""
    n, k = len(t), len(p)
    d = nuovo_modello("duale_parallelo")
    mu = d.addVars(n, lb=-GRB.INFINITY, name="mu")
    pi = d.addVars(k, lb=-GRB.INFINITY, ub=0.0, name="pi")
    lam = d.addVars(n, k, name="lam")
    d.setObjective(mu.sum() + gp.quicksum(p[mm] * pi[mm] for mm in R(k)), GRB.MAXIMIZE)
    d.addConstrs((mu[j] + pi[mm] - t[j][mm] * lam[j, mm] <= 0 for j in R(n) for mm in R(k)), name="rc_x")
    d.addConstrs((lam.sum("*", mm) <= 1 for mm in R(k)), name="rc_y")
    return d


def euristica_4(t, p):
    """Next-fit sul numero di lavori: si riempie una macchina fino a p_m lavori, poi la successiva."""
    n, k = len(t), len(p)
    x, y, cm, cnt, passi = {}, [0.0] * k, 0, 0, []
    for j in R(n):
        if cnt == p[cm]:
            if cm == k - 1:
                return None
            cm, cnt = cm + 1, 0
        x[(j, cm)] = 1
        cnt += 1
        y[cm] = max(y[cm], t[j][cm])
        passi.append(f"Lavoro {j + 1} sulla macchina {cm + 1} (lavori assegnati {cnt} <= p = {p[cm]}): "
                     f"y[{cm + 1}] = max(y[{cm + 1}], t[{j + 1}][{cm + 1}] = {t[j][cm]}) = {y[cm]:g}.")
    return x, y, passi


m4, x4, y4 = modello_4(t4, p4)
salva_modello(m4, "fam07_4_primale")

# ---------- 2. IL RILASSAMENTO LP ----------
zlp4, zlp4r, _ = rilassamenti(m4)

# ---------- 3. IL DUALE DEL RILASSAMENTO (LOWER BOUND) ----------
d4 = duale_4(t4, p4)
salva_modello(d4, "fam07_4_duale")
mano = {f"lam[{j},{mm}]": 1 / 3 for j in R(3) for mm in R(3)}
mano.update({f"mu[{j}]": min(t4[j][mm] / 3 for mm in R(3)) for j in R(3)})
lb4, viol = valuta(d4, mano)
assert viol <= 1e-9
print("Soluzione duale a mano: lam_jm = 1/3, pi = 0, mu_j = min_m t_jm/3 = "
      + ", ".join(frazione(mano[f"mu[{j}]"]) for j in R(3)) + f"  ->  lb = {frazione(lb4)}")
dualita_forte(d4, zlp4)

# ---------- 4. EURISTICA COSTRUTTIVA (UPPER BOUND) ----------
xe, ye, passi = euristica_4(t4, p4)
print("Euristica next-fit sulle cardinalità:")
for i, s in enumerate(passi, 1):
    print(f"  Passo {i}. {s}")
ub4 = sum(ye)
print(f"  ub = {frazione(ub4)}")

# ---------- 5. SOLUZIONE OTTIMA DEL MILP ----------
z4 = risolvi(m4)
print("Soluzione ottima del MILP:")
stampa_soluzione(m4, solo_non_nulle=True)
riga = registra_bound("4 parallelo", ub4, lb4, zlp4, zlp4r, z4)
salva_dati(pd.DataFrame([riga]), "fam07_4_bound")

# ---------- 6. DOMANDE DI MODELLAZIONE AGGIUNTIVE ----------


varianti = {}


def variante(nome, m):
    z = risolvi(m)
    print(f"  {nome:70s} z = {frazione(z)}")
    return z

# 4a: minimizzare il makespan (massimo dei tempi delle macchine)
m, x, y = modello_4(t4, p4)
w = m.addVar(name="w")
m.addConstrs((w >= y[mm] for mm in R(3)), name="makespan")
m.setObjective(w, GRB.MINIMIZE)
varianti["4a"] = variante("4a. Minimizzare il massimo dei tempi (min-max: w >= y_m)", m)
# 4b: costo fisso se una macchina lavora (y_m > 0 => v_m = 1, big-M = max_j t_jm)
g4 = [4, 4, 4]
m, x, y = modello_4(t4, p4)
vv = m.addVars(3, vtype=GRB.BINARY, name="v")
m.addConstrs((y[mm] <= max(t4[j][mm] for j in R(3)) * vv[mm] for mm in R(3)), name="attiva")
m.setObjective(y.sum() + gp.quicksum(g4[mm] * vv[mm] for mm in R(3)), GRB.MINIMIZE)
varianti["4b"] = variante("4b. Costo fisso 4 se la macchina lavora (y_m <= M_m v_m)", m)
salva_dati(pd.DataFrame({"variante": list(varianti), "z": list(varianti.values())}), "fam07_4_varianti")

# ---------- 7. IL SANDWICH SULLA VARIANTE 4a ----------
intestazione("4a. Il sandwich sulla variante: minimizzare il massimo dei tempi")


def modello_4a(t, p):
    mm_, xx, yy = modello_4(t, p)
    ww = mm_.addVar(name="w")
    mm_.addConstrs((ww - yy[mz] >= 0 for mz in R(len(p))), name="minmax")
    mm_.setObjective(ww, GRB.MINIMIZE)
    return mm_, xx, yy, ww


def duale_4a(t, p):
    """Rispetto al duale di 7.4 cambiano due cose: y_m non ha piu' costo, e
    arriva nu_m >= 0 per il vincolo w - y_m >= 0. Le colonne diventano
    x_jm: mu_j + pi_m - t_jm lam_jm <= 0;  y_m: sum_j lam_jm - nu_m <= 0;
    w: sum_m nu_m <= 1."""
    nn, kk = len(t), len(p)
    d = nuovo_modello("duale_parallelo_4a")
    mu = d.addVars(nn, lb=-GRB.INFINITY, name="mu")
    pi = d.addVars(kk, lb=-GRB.INFINITY, ub=0.0, name="pi")
    lam = d.addVars(nn, kk, name="lam")
    nu = d.addVars(kk, name="nu")
    d.setObjective(mu.sum() + gp.quicksum(p[mz] * pi[mz] for mz in R(kk)), GRB.MAXIMIZE)
    d.addConstrs((mu[j] + pi[mz] - t[j][mz] * lam[j, mz] <= 0
                  for j in R(nn) for mz in R(kk)), name="rc_x")
    d.addConstrs((lam.sum("*", mz) - nu[mz] <= 0 for mz in R(kk)), name="rc_y")
    d.addConstr(nu.sum() <= 1, name="rc_w")
    return d


m4a, x4a, y4a, w4a = modello_4a(t4, p4)
salva_modello(m4a, "fam07_4a_primale")

# -- euristica ammissibile: la stessa assegnazione, letta col nuovo obiettivo --
print("Euristica costruttiva: l'assegnazione del problema base e' ammissibile anche qui;")
print("cambia solo come la si valuta, perche' adesso conta il massimo e non la somma.")
assegnazione = sorted(xe)
carichi = [max([t4[j][mz] for (j, q) in assegnazione if q == mz] + [0]) for mz in R(3)]
ub4a = max(carichi)
sol_4a = ({f"x[{j},{mz}]": 1 for (j, mz) in assegnazione}
          | {f"y[{mz}]": carichi[mz] for mz in R(3)} | {"w": ub4a})
assert ammissibile(m4a, sol_4a), "la soluzione euristica della variante deve essere ammissibile"
print(f"  tempi per macchina {carichi}  ->  ub = {frazione(ub4a)}")

# -- certificato duale: tutto il peso sul lavoro piu' lungo --
d4a = duale_4a(t4, p4)
salva_modello(d4a, "fam07_4a_duale")
# con un solo lavoro valutato, lam_jm = nu_m e mu_j <= min_m t_jm nu_m: il nu che
# massimizza quel minimo rende t_jm nu_m costante, cioe' nu_m proporzionale a 1/t_jm
lungo = max(R(3), key=lambda j: min(t4[j]))
somma_inversi = sum(1 / t4[lungo][mz] for mz in R(3))
nu_b = {mz: (1 / t4[lungo][mz]) / somma_inversi for mz in R(3)}
mano_4a = {f"nu[{mz}]": nu_b[mz] for mz in R(3)}
mano_4a.update({f"lam[{lungo},{mz}]": nu_b[mz] for mz in R(3)})
mano_4a[f"mu[{lungo}]"] = 1 / somma_inversi
lb4a, viol_4a = valuta(d4a, mano_4a)
assert viol_4a <= 1e-9, viol_4a
print(f"Soluzione duale a mano: si valuta il solo lavoro {lungo + 1}, il piu' lungo su ogni")
print("  macchina. Con lam_jm = nu_m il vincolo della colonna di w da' sum_m nu_m <= 1, e")
print("  il nu che massimizza min_m t_jm nu_m rende quel prodotto costante: nu_m e'")
print("  proporzionale a 1/t_jm. Il bound e' la media armonica dei tempi di quel lavoro,")
print(f"  1 / sum_m (1/t_jm) = {frazione(lb4a)}.")
zlp4a, zlp4ar, _ = due_rilassamenti(m4a, d4a)
z4a = risolvi(m4a)
riga_4a = registra_bound("4a min-max dei tempi", ub4a, lb4a, zlp4a, zlp4ar, z4a)
salva_dati(pd.DataFrame([riga_4a]), "fam07_4a_bound")
assert lb4a <= zlp4a <= z4a <= ub4a + 1e-9


print("Fine.")
