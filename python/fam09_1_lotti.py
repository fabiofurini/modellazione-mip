"""Problema 9.1 -- Produzione e lotti con costo fisso di lancio.

Bilancio delle scorte, attivazione della produzione con big-M e magazzino. Il
legame e' quello del costo fisso (sezione 3.2) con il coefficiente ricavato dai
dati: M_t e' la domanda residua, non un numero grande a caso.
"""
import gurobipy as gp
import pandas as pd
from gurobipy import GRB

from euristiche import euristica_lotti
from mip import (ammissibile, due_rilassamenti, frazione, nuovo_modello, registra_bound,
                 risolvi, valuta)
from stile import ARANCIO, BLU, ROSSO, TEAL, VERDE, intestazione, plt, salva_dati, salva_figura

R = range

# ---------- 1. MODELLO E ISTANZA ----------
intestazione("9.1 Produzione e lotti: bilancio delle scorte, lancio con costo fisso")
d1 = [20, 10, 30, 40, 10]          # domanda dei cinque giorni
p1 = [2, 3, 2, 3, 2]               # costo unitario di produzione
q1 = [50, 50, 50, 50, 50]          # costo fisso di lancio
h1 = [1, 1, 1, 1]                  # costo di magazzino a fine giorno (t = 1..n-1)
r0, rn = 0, 0                      # scorta iniziale e finale richiesta
n1 = len(d1)
# il piu' piccolo big-M valido: in un ottimo non si produce mai piu' della domanda residua
M1 = [sum(d1[t:]) + rn for t in R(n1)]
salva_dati(pd.DataFrame({"giorno": R(1, n1 + 1), "domanda": d1, "costo_unitario": p1,
                         "costo_lancio": q1, "M": M1}), "prod1_dati")


def modello_1(d, p, q, h, r0, rn):
    n = len(d)
    M = [sum(d[t:]) + rn for t in R(n)]
    m = nuovo_modello("lotti")
    x = m.addVars(n, name="x")                       # quantita' prodotta
    s = m.addVars(n - 1, name="s")                   # scorta a fine giorno t
    y = m.addVars(n, vtype=GRB.BINARY, name="y")     # lancio della produzione
    m.setObjective(gp.quicksum(p[t] * x[t] for t in R(n))
                   + gp.quicksum(q[t] * y[t] for t in R(n))
                   + gp.quicksum(h[t] * s[t] for t in R(n - 1)), GRB.MINIMIZE)
    m.addConstr(x[0] - s[0] == d[0] - r0, name="bilancio[0]")
    m.addConstrs((x[t] + s[t - 1] - s[t] == d[t] for t in R(1, n - 1)), name="bilancio")
    m.addConstr(x[n - 1] + s[n - 2] == d[n - 1] + rn, name=f"bilancio[{n - 1}]")
    m.addConstrs((-x[t] + M[t] * y[t] >= 0 for t in R(n)), name="lancio")
    return m, x, s, y


def duale_1(d, p, q, h, r0, rn):
    """max sum_t b_t mu_t;  mu_t - pi_t <= p_t;  M_t pi_t <= q_t;  -mu_t + mu_{t+1} <= h_t;
    mu libere, pi >= 0."""
    n = len(d)
    M = [sum(d[t:]) + rn for t in R(n)]
    b = [d[0] - r0] + d[1:n - 1] + [d[n - 1] + rn]
    dl = nuovo_modello("duale_lotti")
    mu = dl.addVars(n, lb=-GRB.INFINITY, name="mu")
    pi = dl.addVars(n, name="pi")
    dl.setObjective(gp.quicksum(b[t] * mu[t] for t in R(n)), GRB.MAXIMIZE)
    dl.addConstrs((mu[t] - pi[t] <= p[t] for t in R(n)), name="rc_x")
    dl.addConstrs((M[t] * pi[t] <= q[t] for t in R(n)), name="rc_y")
    dl.addConstrs((-mu[t] + mu[t + 1] <= h[t] for t in R(n - 1)), name="rc_s")
    return dl


m1, x1, s1, y1 = modello_1(d1, p1, q1, h1, r0, rn)
print(f"  Domanda totale {sum(d1)}; big-M per giorno (domanda residua): {M1}")

# ---------- 2. EURISTICHE COSTRUTTIVE (UPPER BOUND) ----------
# (a) lot-for-lot: si produce ogni giorno esattamente la domanda, niente scorte
lot_per_lot = sum(p1[t] * d1[t] for t in R(n1)) + sum(q1)
sol_llf = {f"x[{t}]": d1[t] for t in R(n1)} | {f"y[{t}]": 1 for t in R(n1)} \
    | {f"s[{t}]": 0 for t in R(n1 - 1)}
assert ammissibile(m1, sol_llf)
print(f"  (a) lot-for-lot: si lancia ogni giorno, costo "
      f"{sum(p1[t] * d1[t] for t in R(n1))} di produzione + {sum(q1)} di lanci = {lot_per_lot}")
# (b) least unit cost: si copre il numero di giorni che minimizza il costo medio per unita'
e = euristica_lotti(d1, q1[0], h1[0])
e.traccia.stampa()
sol_luc = {f"x[{t}]": e.lanci.get(t, 0) for t in R(n1)} \
    | {f"y[{t}]": 1 if t in e.lanci else 0 for t in R(n1)}
scorta = 0
for t in R(n1 - 1):
    scorta += sol_luc[f"x[{t}]"] - d1[t]
    sol_luc[f"s[{t}]"] = scorta
assert ammissibile(m1, sol_luc)
luc = sum(p1[t] * sol_luc[f"x[{t}]"] for t in R(n1)) + sum(q1[t] for t in e.lanci) \
    + sum(h1[t] * sol_luc[f"s[{t}]"] for t in R(n1 - 1))
print(f"  (b) least unit cost: lanci nei giorni {[t + 1 for t in sorted(e.lanci)]}, costo {luc}")
ub1 = min(lot_per_lot, luc)
print(f"  La migliore delle due: ub = {frazione(ub1)}")

# ---------- 3. RILASSAMENTO LP E DUALE (LOWER BOUND) ----------
dl1 = duale_1(d1, p1, q1, h1, r0, rn)
# ricetta: pi = 0 (i lanci si regalano) e mu_t = costo minimo per avere una unita' al giorno t
mu = []
for t in R(n1):
    mu.append(p1[t] if t == 0 else min(mu[t - 1] + h1[t - 1], p1[t]))
mano = {f"mu[{t}]": mu[t] for t in R(n1)}
lb1, viol = valuta(dl1, mano)
assert viol <= 1e-9, viol
print("  Duale a mano: pi = 0 (i lanci non si pagano) e mu_t = il costo unitario piu' basso")
print("  per avere una unita' disponibile il giorno t, cioe' min(mu_{t-1} + h_{t-1}, p_t):")
print("    mu = " + ", ".join(frazione(v) for v in mu))
print(f"  ->  lb = {frazione(lb1)}: e' il costo di produzione se i lanci fossero gratis.")
zlp1, zlp1r, pi1 = due_rilassamenti(m1, dl1)

# ---------- 4. OTTIMO DEL MILP ----------
z1 = risolvi(m1)
lanci_ott = [t + 1 for t in R(n1) if y1[t].X > 0.5]
print(f"  Soluzione ottima: lanci nei giorni {lanci_ott}; quantita' "
      + ", ".join(frazione(x1[t].X) for t in R(n1))
      + "; scorte " + ", ".join(frazione(s1[t].X) for t in R(n1 - 1)))
riga = registra_bound("1 lotti con setup", ub1, lb1, zlp1, zlp1r, z1)
salva_dati(pd.DataFrame([riga]), "prod1_bound")
assert lb1 <= zlp1 <= z1 <= ub1 + 1e-9

# ---------- 5. DOMANDE DI MODELLAZIONE AGGIUNTIVE ----------
varianti = {}


def variante(nome, m):
    z = risolvi(m)
    print(f"  {nome:70s} z = {frazione(z)}")
    return z


# 1a: capacita' giornaliera di 35 litri
m, x, s, y = modello_1(d1, p1, q1, h1, r0, rn)
m.addConstrs((x[t] <= 35 for t in R(n1)), name="capacita")
varianti["1a"] = variante("1a. Capacita' giornaliera di 35 litri (x_t <= 35)", m)
# 1b: lotto minimo di 25 litri quando si produce (variabile semicontinua)
m, x, s, y = modello_1(d1, p1, q1, h1, r0, rn)
m.addConstrs((x[t] >= 25 * y[t] for t in R(n1)), name="lotto_minimo")
varianti["1b"] = variante("1b. Lotto minimo di 25 litri se si produce (x_t >= 25 y_t)", m)
salva_dati(pd.DataFrame({"variante": list(varianti), "z": list(varianti.values())}),
           "prod1_varianti")

# ---------- 6. FIGURA ----------
fig, ax = plt.subplots(figsize=(7.0, 3.4))
giorni = list(R(1, n1 + 1))
ax.bar(giorni, [x1[t].X for t in R(n1)], color=TEAL, label="produzione $x_t$", width=0.55)
ax.plot(giorni, d1, "o--", color=ROSSO, label="domanda $d_t$")
ax.plot(giorni[:-1], [s1[t].X for t in R(n1 - 1)], "s-", color=ARANCIO,
        label="scorta a fine giorno $s_t$")
for t in lanci_ott:
    ax.annotate("lancio", (t, x1[t - 1].X), textcoords="offset points", xytext=(0, 6),
                ha="center", fontsize=8, color=BLU)
ax.set_xticks(giorni)
ax.set_xlabel("giorno")
ax.set_ylabel("litri")
ax.set_title(f"9.1: piano ottimo (z = {frazione(z1)})")
ax.legend(fontsize=8, ncols=3, loc="upper left")
salva_figura(fig, "cap09_lotti_ottimo")
print("Fine.")
