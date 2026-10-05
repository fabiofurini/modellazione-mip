"""Problema 9.1 -- Produzione e lotti con costo fisso di lancio.

Bilancio delle scorte, attivazione della produzione con big-M e magazzino. Il
legame e' quello del costo fisso (sezione 6.2) con il coefficiente ricavato dai
dati: M_t e' la domanda residua, non un numero grande a caso.
"""
import gurobipy as gp
import pandas as pd
from gurobipy import GRB

from euristiche import euristica_lotti
from mip import (ammissibile, dualita_forte, due_rilassamenti, frazione,
                 nuovo_modello, registra_bound, rilassamenti, risolvi, valuta)
from stile import ARANCIO, BLU, ROSSO, TEAL, VERDE, intestazione, plt, salva_dati, salva_figura
from esteso import salva_modello

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
                         "costo_lancio": q1, "M": M1}), "fam09_1_dati")


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
salva_modello(m1, "fam09_1_primale")
print(f"  Domanda totale {sum(d1)}; big-M per giorno (domanda residua): {M1}")

# ---------- 2. IL RILASSAMENTO LP ----------
zlp1, zlp1r, pi1 = rilassamenti(m1)

# ---------- 3. IL DUALE DEL RILASSAMENTO (LOWER BOUND) ----------
dl1 = duale_1(d1, p1, q1, h1, r0, rn)
salva_modello(dl1, "fam09_1_duale")
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
dualita_forte(dl1, zlp1)

# ---------- 4. EURISTICA COSTRUTTIVA (UPPER BOUND) ----------
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

# ---------- 5. OTTIMO DEL MILP ----------
z1 = risolvi(m1)
lanci_ott = [t + 1 for t in R(n1) if y1[t].X > 0.5]
print(f"  Soluzione ottima: lanci nei giorni {lanci_ott}; quantita' "
      + ", ".join(frazione(x1[t].X) for t in R(n1))
      + "; scorte " + ", ".join(frazione(s1[t].X) for t in R(n1 - 1)))
riga = registra_bound("1 lotti con setup", ub1, lb1, zlp1, zlp1r, z1)
salva_dati(pd.DataFrame([riga]), "fam09_1_bound")
assert lb1 <= zlp1 <= z1 <= ub1 + 1e-9

# ---------- 6. DOMANDE DI MODELLAZIONE AGGIUNTIVE ----------
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
           "fam09_1_varianti")

# ---------- 7. IL SANDWICH SULLA VARIANTE 1a ----------
intestazione("9.1a Il sandwich sulla variante: capacita' giornaliera di 35 litri")
CAP = 35


def modello_1a(d, p, q, h, r0, rn, cap=CAP):
    mm, xx, ss, yy = modello_1(d, p, q, h, r0, rn)
    mm.addConstrs((xx[t] <= cap for t in R(len(d))), name="capacita")
    return mm, xx, ss, yy


def duale_1a(d, p, q, h, r0, rn, cap=CAP):
    """Al duale di 9.1 si aggiunge nu_t >= 0 per ogni vincolo di capacita'
    x_t <= cap, scritto come -x_t >= -cap: entra nell'obiettivo con il suo
    termine noto, negativo, e allenta la colonna di x_t."""
    nn = len(d)
    MM = [sum(d[tt:]) + rn for tt in R(nn)]
    b = [d[0] - r0] + d[1:nn - 1] + [d[nn - 1] + rn]
    dl = nuovo_modello("duale_lotti_1a")
    mu = dl.addVars(nn, lb=-GRB.INFINITY, name="mu")
    pi = dl.addVars(nn, name="pi")
    nu = dl.addVars(nn, name="nu")
    dl.setObjective(gp.quicksum(b[tt] * mu[tt] for tt in R(nn))
                    - cap * nu.sum(), GRB.MAXIMIZE)
    dl.addConstrs((mu[tt] - pi[tt] - nu[tt] <= p[tt] for tt in R(nn)), name="rc_x")
    dl.addConstrs((MM[tt] * pi[tt] <= q[tt] for tt in R(nn)), name="rc_y")
    dl.addConstrs((-mu[tt] + mu[tt + 1] <= h[tt] for tt in R(nn - 1)), name="rc_s")
    return dl


m1a, x1a, s1a, y1a = modello_1a(d1, p1, q1, h1, r0, rn)
salva_modello(m1a, "fam09_1a_primale")

# -- euristica ammissibile: lot-for-lot non sfora mai la capacita' se la domanda non la supera --
print("Euristica costruttiva: si produce ogni giorno la domanda del giorno (lot-for-lot). Se")
print("un giorno la domanda supera la capacita', l'eccedenza si anticipa al giorno prima, che")
print("la tiene in magazzino: e' l'unico modo di coprirla rispettando il vincolo.")
prod = list(d1)
for tt in R(n1 - 1, 0, -1):
    if prod[tt] > CAP:
        ecc = prod[tt] - CAP
        prod[tt] -= ecc
        prod[tt - 1] += ecc
        print(f"  giorno {tt + 1}: domanda {d1[tt]} oltre la capacita'; {ecc} unita' anticipate "
              f"al giorno {tt}")
assert max(prod) <= CAP, "l'anticipo non basta: servirebbe spalmare su piu' giorni"
scorte = []
acc = 0
for tt in R(n1 - 1):
    acc += prod[tt] - d1[tt]
    scorte.append(acc)
ub1a = (sum(p1[tt] * prod[tt] for tt in R(n1)) + sum(q1[tt] for tt in R(n1) if prod[tt] > 0)
        + sum(h1[tt] * scorte[tt] for tt in R(n1 - 1)))
sol_1a = ({f"x[{tt}]": prod[tt] for tt in R(n1)}
          | {f"y[{tt}]": (1 if prod[tt] > 0 else 0) for tt in R(n1)}
          | {f"s[{tt}]": scorte[tt] for tt in R(n1 - 1)})
assert ammissibile(m1a, sol_1a), "la soluzione euristica della variante deve essere ammissibile"
print(f"  produzione {prod}, scorte {scorte}  ->  ub = {frazione(ub1a)}")

# -- certificato duale: nu paga cap e incassa la domanda del giorno --
dl1a = duale_1a(d1, p1, q1, h1, r0, rn)
salva_modello(dl1a, "fam09_1a_duale")
b1 = [d1[0] - r0] + d1[1:n1 - 1] + [d1[n1 - 1] + rn]


def valore_duale_1a(nu_val, giorno):
    """Alzando nu_giorno il tetto su mu_giorno sale, ma si paga cap per unita'."""
    nu_v = [nu_val if tt == giorno else 0.0 for tt in R(n1)]
    mu_v = []
    for tt in R(n1):
        tetto = p1[tt] + nu_v[tt]
        mu_v.append(tetto if tt == 0 else min(mu_v[tt - 1] + h1[tt - 1], tetto))
    return sum(b1[tt] * mu_v[tt] for tt in R(n1)) - CAP * sum(nu_v), mu_v, nu_v


giorno_1a = max(R(n1), key=lambda tt: b1[tt])
candidati_1a = [0.0] + [abs(p1[tt] - p1[giorno_1a]) + k for tt in R(n1) for k in (0, 1, 2)]
migliore_1a = max(sorted(set(candidati_1a)), key=lambda v: valore_duale_1a(v, giorno_1a)[0])
lb1a, mu_1a, nu_1a = valore_duale_1a(migliore_1a, giorno_1a)
mano_1a = ({f"mu[{tt}]": mu_1a[tt] for tt in R(n1)}
           | {f"nu[{tt}]": nu_1a[tt] for tt in R(n1)})
lb1a_val, viol_1a = valuta(dl1a, mano_1a)
assert viol_1a <= 1e-9, viol_1a
print("Soluzione duale a mano: pi = 0 come nel problema base. Alzare nu_t di una unita' alza")
print(f"  il tetto su mu_t e incassa b_t, ma costa cap = {CAP}: conviene solo dove la domanda")
print("  supera la capacita'. Si prova sul giorno di domanda massima, il "
      f"{giorno_1a + 1} (b = {b1[giorno_1a]}).")
if migliore_1a > 0:
    print(f"  Il migliore e' nu = {frazione(migliore_1a)}.")
else:
    print("  Qui nu resta a zero: anche sul giorno piu' carico la catena delle scorte tiene")
    print("  mu sotto il tetto, quindi alzare nu costerebbe senza alzare nulla.")
print(f"  ->  lb = {frazione(lb1a_val)}")
zlp1a, zlp1ar, _ = due_rilassamenti(m1a, dl1a)
z1a = risolvi(m1a)
riga_1a = registra_bound("1a capacita' giornaliera", ub1a, lb1a_val, zlp1a, zlp1ar, z1a)
salva_dati(pd.DataFrame([riga_1a]), "fam09_1a_bound")
assert lb1a_val <= zlp1a <= z1a <= ub1a + 1e-9

# ---------- 8. FIGURA ----------
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
