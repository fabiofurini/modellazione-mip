"""Problema 10.2 -- Dieta con conteggio dei cibi e lotto minimo.

Una dieta classica (quantita' continue, vincoli nutrizionali a due versi) con
sopra tre tecniche intere: attivazione (3.2), lotto minimo (3.3) e conteggio dei
tipi (3.11). Senza il lotto minimo il conteggio «almeno t cibi diversi» sarebbe
vuoto: si accenderebbero indicatori con quantita' nulla.
"""
import gurobipy as gp
import pandas as pd
from gurobipy import GRB

from mip import (ammissibile, due_rilassamenti, frazione, nuovo_modello, registra_bound,
                 rilassamento, risolvi, valuta)
from stile import ARANCIO, BLU, ROSSO, TEAL, VERDE, intestazione, plt, salva_dati, salva_figura

R = range

# ---------- 1. MODELLO E ISTANZA ----------
intestazione("10.2 Dieta: costo minimo con almeno t cibi diversi e lotto minimo per cibo")
CIBI = ["latte", "riso", "pane", "patate"]
NUTRIENTI = ["ferro", "calcio"]
w2 = [2, 3, 1, 4]                      # costo al chilo
g2 = [[10, 5], [20, 10], [5, 15], [25, 5]]   # grammi di nutriente j per chilo di cibo i
a2 = [60, 40]                          # minimo mensile di ciascun nutriente
b2 = [200, 150]                        # massimo mensile
c2 = [1, 1, 1, 1]                      # quantita' minima se il cibo e' scelto
d2 = [8, 8, 8, 8]                      # quantita' massima
t2 = 3                                 # almeno tre cibi diversi
s2, r2 = len(w2), len(a2)
salva_dati(pd.DataFrame({"cibo": CIBI, "costo": w2,
                         "ferro": [g[0] for g in g2], "calcio": [g[1] for g in g2],
                         "min": c2, "max": d2}), "dieta2_dati")


def modello_2(w, g, a, b, c, d, t):
    s, r = len(w), len(a)
    m = nuovo_modello("dieta")
    x = m.addVars(s, name="x")                        # chili di ciascun cibo
    y = m.addVars(s, vtype=GRB.BINARY, name="y")      # cibo presente nella dieta
    m.setObjective(gp.quicksum(w[i] * x[i] for i in R(s)), GRB.MINIMIZE)
    m.addConstrs((gp.quicksum(g[i][j] * x[i] for i in R(s)) >= a[j] for j in R(r)), name="minimo")
    m.addConstrs((gp.quicksum(g[i][j] * x[i] for i in R(s)) <= b[j] for j in R(r)), name="massimo")
    m.addConstrs((x[i] - c[i] * y[i] >= 0 for i in R(s)), name="lotto_minimo")
    m.addConstrs((x[i] - d[i] * y[i] <= 0 for i in R(s)), name="attiva")
    m.addConstr(gp.quicksum(y[i] for i in R(s)) >= t, name="varieta")
    return m, x, y


def duale_2(w, g, a, b, c, d, t):
    """max sum_j a_j alpha_j - sum_j b_j beta_j + t tau
       s.t.  sum_j g_ij (alpha_j - beta_j) + lam_i - mu_i <= w_i        (colonna x_i)
             -c_i lam_i + d_i mu_i + tau <= 0                            (colonna y_i)
             alpha, beta, lam, mu, tau >= 0."""
    s, r = len(w), len(a)
    dl = nuovo_modello("duale_dieta")
    alpha = dl.addVars(r, name="alpha")
    beta = dl.addVars(r, name="beta")
    lam = dl.addVars(s, name="lam")
    mu = dl.addVars(s, name="mu")
    tau = dl.addVar(name="tau")
    dl.setObjective(gp.quicksum(a[j] * alpha[j] for j in R(r))
                    - gp.quicksum(b[j] * beta[j] for j in R(r)) + t * tau, GRB.MAXIMIZE)
    dl.addConstrs((gp.quicksum(g[i][j] * (alpha[j] - beta[j]) for j in R(r))
                   + lam[i] - mu[i] <= w[i] for i in R(s)), name="rc_x")
    dl.addConstrs((-c[i] * lam[i] + d[i] * mu[i] + tau <= 0 for i in R(s)), name="rc_y")
    return dl


m2, x2, y2 = modello_2(w2, g2, a2, b2, c2, d2, t2)

# ---------- 2. EURISTICA COSTRUTTIVA (UPPER BOUND) ----------
# euristica costruttiva: si parte dal lotto minimo di tutti i cibi piu' economici fino a raggiungere t,
# poi si copre il fabbisogno residuo col cibo di costo per grammo piu' basso
def euristica(w, g, a, b, c, d, t):
    s, r = len(w), len(a)
    x = [0.0] * s
    scelti = sorted(R(s), key=lambda i: (w[i], i))[:t]
    for i in scelti:
        x[i] = c[i]
    passi = [f"si accendono i {t} cibi piu' economici al lotto minimo: "
             + ", ".join(f"{CIBI[i]} ({c[i]} kg)" for i in scelti)]
    for j in R(r):
        while sum(g[i][j] * x[i] for i in R(s)) < a[j] - 1e-9:
            # il cibo, gia' acceso, col costo per grammo di nutriente j piu' basso
            cand = [i for i in scelti if g[i][j] > 0 and x[i] < d[i] - 1e-9]
            if not cand:
                return None, passi + [f"nessun cibo acceso puo' coprire il {NUTRIENTI[j]}"]
            i = min(cand, key=lambda i: w[i] / g[i][j])
            manca = a[j] - sum(g[k][j] * x[k] for k in R(s))
            aggiunta = min(manca / g[i][j], d[i] - x[i])
            x[i] += aggiunta
            passi.append(f"{NUTRIENTI[j]}: mancano {manca:.4g} g; si aggiungono "
                         f"{aggiunta:.4g} kg di {CIBI[i]} (costo per grammo "
                         f"{w[i] / g[i][j]:.4g})")
    return x, passi


x_eur, passi = euristica(w2, g2, a2, b2, c2, d2, t2)
for k, riga in enumerate(passi, 1):
    print(f"  Passo {k}. {riga}")
ub2 = sum(w2[i] * x_eur[i] for i in R(s2))
sol_eur = {f"x[{i}]": x_eur[i] for i in R(s2)} | {f"y[{i}]": 1 if x_eur[i] > 1e-9 else 0
                                                 for i in R(s2)}
assert ammissibile(m2, sol_eur), sol_eur
print("  Soluzione euristica: " + ", ".join(f"{CIBI[i]} {x_eur[i]:.4g} kg" for i in R(s2)
                                            if x_eur[i] > 1e-9)
      + f"   ub = {frazione(ub2)}")

# ---------- 3. RILASSAMENTO LP E DUALE (LOWER BOUND) ----------
dl2 = duale_2(w2, g2, a2, b2, c2, d2, t2)
# ricetta: beta = mu = tau = 0 (i massimi, i tetti e la varieta' non si valutano);
# alpha_j = il piu' grande prezzo del nutriente j che nessun cibo riesce a battere
# si tiene un solo nutriente per volta e si sceglie quello che da' il bound migliore
mano, migliore, scelto = {}, -1.0, None
for j in R(r2):
    prova = {f"alpha[{jj}]": (min(w2[i] / g2[i][jj] for i in R(s2) if g2[i][jj] > 0)
                              if jj == j else 0.0) for jj in R(r2)}
    val, viol = valuta(dl2, prova)
    if viol <= 1e-9 and val > migliore:
        migliore, scelto, mano = val, j, prova
lb2, viol = valuta(dl2, mano)
assert viol <= 1e-9, viol
print("  Duale a mano: beta = mu = tau = 0 (massimi, tetti e varieta' non si valutano) e")
print("  un solo alpha_j positivo, pari al costo per grammo piu' basso fra i cibi:")
for j in R(r2):
    prezzo = min(w2[i] / g2[i][j] for i in R(s2) if g2[i][j] > 0)
    print(f"    {NUTRIENTI[j]}: prezzo {frazione(prezzo)} EUR/g  ->  a_j * prezzo = "
          f"{frazione(a2[j] * prezzo)}")
print(f"  Il migliore e' il {NUTRIENTI[scelto]}:  lb = {frazione(lb2)}")
zlp2, zlp2r, _ = due_rilassamenti(m2, dl2)

# ---------- 4. OTTIMO DEL MILP ----------
z2 = risolvi(m2)
print("  Soluzione ottima: " + ", ".join(f"{CIBI[i]} {x2[i].X:.4g} kg" for i in R(s2)
                                         if x2[i].X > 1e-9)
      + f"   ({int(sum(y2[i].X for i in R(s2)))} cibi diversi, richiesti {t2})")
for j in R(r2):
    print(f"    {NUTRIENTI[j]}: {sum(g2[i][j] * x2[i].X for i in R(s2)):.4g} g "
          f"(fra {a2[j]} e {b2[j]})")
riga = registra_bound("2 dieta", ub2, lb2, zlp2, zlp2r, z2)
salva_dati(pd.DataFrame([riga]), "dieta2_bound")
assert lb2 <= zlp2 <= z2 <= ub2 + 1e-9

# ---------- 5. SENZA IL LOTTO MINIMO IL CONTEGGIO E' VUOTO ----------
intestazione("10.2 Perche' il lotto minimo serve al conteggio")
m, x, y = modello_2(w2, g2, a2, b2, [0] * s2, d2, t2)   # c_i = 0: nessun lotto minimo
z_senza = risolvi(m)
accesi = [CIBI[i] for i in R(s2) if y[i].X > 0.5]
vuoti = [CIBI[i] for i in R(s2) if y[i].X > 0.5 and x[i].X < 1e-9]
print(f"  Con c_i = 0 l'ottimo scende a {frazione(z_senza)} e i cibi 'accesi' sono {accesi},")
print(f"  ma di questi hanno quantita' nulla: {vuoti}. Il vincolo di varieta' e' soddisfatto")
print("  da indicatori vuoti: senza lotto minimo il conteggio non dice niente.")
assert vuoti, "con c = 0 devono comparire indicatori vuoti"

# ---------- 6. DOMANDE DI MODELLAZIONE AGGIUNTIVE ----------
varianti = {}


def variante(nome, m):
    z = risolvi(m)
    print(f"  {nome:70s} z = {frazione(z)}")
    return z


# 2a: il lotto minimo sale a 2 kg per ogni cibo scelto
m, x, y = modello_2(w2, g2, a2, b2, [2] * s2, d2, t2)
varianti["2a"] = variante("2a. Il lotto minimo sale a 2 kg per cibo (c_i = 2)", m)
# 2b: si vogliono almeno quattro cibi diversi
m, x, y = modello_2(w2, g2, a2, b2, c2, d2, 4)
varianti["2b"] = variante("2b. Si vogliono almeno quattro cibi diversi (t = 4)", m)
salva_dati(pd.DataFrame({"variante": list(varianti), "z": list(varianti.values())}),
           "dieta2_varianti")

# ---------- 7. FIGURA ----------
fig, ax = plt.subplots(figsize=(6.8, 3.0))
idx = list(R(s2))
ax.bar([i - 0.2 for i in idx], [x_eur[i] for i in idx], 0.4, color=ARANCIO, label="euristica")
ax.bar([i + 0.2 for i in idx], [x2[i].X for i in idx], 0.4, color=TEAL, label="ottimo")
for i in idx:
    ax.plot([i - 0.42, i + 0.42], [c2[i], c2[i]], color=ROSSO, lw=1.5)
ax.plot([], [], color=ROSSO, lw=1.5, label="lotto minimo $c_i$")
ax.set_xticks(idx)
ax.set_xticklabels(CIBI)
ax.set_ylabel("chili al mese")
ax.set_title(f"10.2: dieta euristica ({frazione(ub2)} EUR) e ottima ({frazione(z2)} EUR)")
ax.legend(fontsize=8)
salva_figura(fig, "cap10_dieta_ottimo")
print("Fine.")
