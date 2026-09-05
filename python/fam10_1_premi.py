"""Problema 10.1 -- Premi acquistabili con due modalita'.

Ogni premio si ottiene o con soli punti oppure con meno punti piu' un contributo
in euro: due variabili binarie per premio e un vincolo di mutua esclusione. Il
legame e' quello del capitolo 2: x_i + y_i <= 1 e' un set packing, e le converse
vanno confutate esplicitamente con x_i = y_i = 0.
"""
import gurobipy as gp
import pandas as pd
from gurobipy import GRB

from mip import (ammissibile, due_rilassamenti, frazione, nuovo_modello, registra_bound,
                 risolvi, valuta)
from stile import ARANCIO, BLU, ROSSO, TEAL, intestazione, plt, salva_dati, salva_figura

R = range

# ---------- 1. MODELLO E ISTANZA ----------
intestazione("10.1 Premi: soli punti oppure meno punti piu' un contributo in euro")
a1 = [8, 6, 10, 5, 7]        # punti se si usa la sola modalita' a punti
b1 = [4, 3, 6, 2, 4]         # punti se si aggiunge il contributo
c1 = [10, 8, 15, 5, 9]       # contributo in euro
d1 = [5, 4, 7, 3, 6]         # valore di preferenza
p1, ell1 = 20, 16            # punti disponibili e preferenza minima richiesta
s1 = len(a1)
salva_dati(pd.DataFrame({"premio": R(1, s1 + 1), "a": a1, "b": b1, "c": c1, "d": d1}),
           "premi1_dati")
print(f"  {s1} premi, {p1} punti disponibili, preferenza minima richiesta {ell1}")


def modello_1(a, b, c, d, p, ell):
    s = len(a)
    m = nuovo_modello("premi")
    x = m.addVars(s, vtype=GRB.BINARY, name="x")     # premio con soli punti
    y = m.addVars(s, vtype=GRB.BINARY, name="y")     # premio con punti + contributo
    m.setObjective(gp.quicksum(c[i] * y[i] for i in R(s)), GRB.MINIMIZE)
    m.addConstrs((x[i] + y[i] <= 1 for i in R(s)), name="una_modalita")
    m.addConstr(gp.quicksum(a[i] * x[i] + b[i] * y[i] for i in R(s)) <= p, name="punti")
    m.addConstr(gp.quicksum(d[i] * (x[i] + y[i]) for i in R(s)) >= ell, name="preferenza")
    return m, x, y


def duale_1(a, b, c, d, p, ell):
    """max -sum_i sigma_i - p pi + ell rho;  -sigma_i - a_i pi + d_i rho <= 0;
    -sigma_i - b_i pi + d_i rho <= c_i;  sigma, pi >= 0, rho >= 0.
    (sigma sono i duali di x_i + y_i <= 1, pi quello dei punti, rho quello della preferenza;
    in un minimo i vincoli <= danno duali <= 0: qui si scrive -sigma con sigma >= 0.)"""
    s = len(a)
    dl = nuovo_modello("duale_premi")
    sigma = dl.addVars(s, name="sigma")
    pi = dl.addVar(name="pi")
    rho = dl.addVar(name="rho")
    dl.setObjective(-gp.quicksum(sigma[i] for i in R(s)) - p * pi + ell * rho, GRB.MAXIMIZE)
    dl.addConstrs((-sigma[i] - a[i] * pi + d[i] * rho <= 0 for i in R(s)), name="rc_x")
    dl.addConstrs((-sigma[i] - b[i] * pi + d[i] * rho <= c[i] for i in R(s)), name="rc_y")
    return dl


m1, x1, y1 = modello_1(a1, b1, c1, d1, p1, ell1)

# ---------- 2. EURISTICA COSTRUTTIVA (UPPER BOUND) ----------
# euristica costruttiva: si scorrono i premi per preferenza decrescente; ciascuno si prende con i soli
# punti se bastano, altrimenti con il contributo se bastano i punti ridotti, e ci si ferma
# appena la preferenza richiesta e' raggiunta
punti, pref = p1, 0
scelta = {}
for i in sorted(R(s1), key=lambda i: (-d1[i], i)):
    if pref >= ell1:
        break
    if punti >= a1[i]:
        scelta[i], punti, pref = "punti", punti - a1[i], pref + d1[i]
        print(f"  Premio {i + 1} (preferenza {d1[i]}): bastano i soli punti ({a1[i]} <= "
              f"{punti + a1[i]}): si prende; preferenza {pref}, punti residui {punti}")
    elif punti >= b1[i]:
        scelta[i], punti, pref = "contributo", punti - b1[i], pref + d1[i]
        print(f"  Premio {i + 1} (preferenza {d1[i]}): i punti non bastano per la modalita' a "
              f"({a1[i]} > {punti + b1[i]}), si usa la b: {b1[i]} punti e {c1[i]} euro; "
              f"preferenza {pref}, punti residui {punti}")
    else:
        print(f"  Premio {i + 1} (preferenza {d1[i]}): i punti residui {punti} non bastano "
              f"per nessuna delle due modalita': si salta")
assert pref >= ell1, "la euristica costruttiva non raggiunge la preferenza richiesta"
ub1 = sum(c1[i] for i, mod in scelta.items() if mod == "contributo")
sol_eur = {f"x[{i}]": 1 for i, mod in scelta.items() if mod == "punti"} \
    | {f"y[{i}]": 1 for i, mod in scelta.items() if mod == "contributo"}
assert ammissibile(m1, sol_eur)
print(f"  Soluzione euristica: preferenza {pref} >= {ell1}, contributo totale ub = {frazione(ub1)}")

# ---------- 3. RILASSAMENTO LP E DUALE (LOWER BOUND) ----------
dl1 = duale_1(a1, b1, c1, d1, p1, ell1)
# ricetta: si scelgono il prezzo pi di un punto e il prezzo rho di una unita' di
# preferenza; i duali della mutua esclusione si ricavano da questi ponendo
# sigma_i = max(0, d_i rho - a_i pi), cioe' il minimo che rende ammissibile il vincolo
# sulla modalita' a. Restano da controllare i vincoli sulla modalita' b. La coppia
# (pi, rho) si sceglie su una griglia: l'obiettivo e' concavo e lineare a tratti.
def duale_da(pi_v, rho_v):
    sig = [max(0.0, d1[i] * rho_v - a1[i] * pi_v) for i in R(s1)]
    ok = all(-sig[i] - b1[i] * pi_v + d1[i] * rho_v <= c1[i] + 1e-9 for i in R(s1))
    val = -sum(sig) - p1 * pi_v + ell1 * rho_v
    return (val if ok else float("-inf")), sig


griglia = [k / 100 for k in R(0, 301)]
coppie = [(pi_v, rho_v) for pi_v in griglia for rho_v in griglia]
pi_star, rho_star = max(coppie, key=lambda c: duale_da(*c)[0])
_, sigma_star = duale_da(pi_star, rho_star)
mano = {"pi": pi_star, "rho": rho_star} | {f"sigma[{i}]": sigma_star[i] for i in R(s1)}
lb1, viol = valuta(dl1, mano)
assert viol <= 1e-9, (viol, mano)
print("  Duale a mano: si scelgono il prezzo pi di un punto e il prezzo rho di una unita'")
print("  di preferenza; i duali della mutua esclusione si ricavano da questi ponendo")
print("  sigma_i = max(0, d_i rho - a_i pi), il minimo che rende ammissibile il vincolo")
print("  sulla modalita' a. Restano da controllare i vincoli sulla modalita' b.")
print(f"    pi = {frazione(pi_star)} euro per punto, rho = {frazione(rho_star)} euro per unita'")
print(f"    di preferenza, sigma = " + ", ".join(frazione(v) for v in sigma_star))
print(f"  ->  lb = -sum(sigma) - p pi + l rho = {frazione(lb1)}")
zlp1, zlp1r, _ = due_rilassamenti(m1, dl1)

# ---------- 4. OTTIMO DEL MILP ----------
z1 = risolvi(m1)
soli_punti = [i + 1 for i in R(s1) if x1[i].X > 0.5]
con_contributo = [i + 1 for i in R(s1) if y1[i].X > 0.5]
print(f"  Soluzione ottima: con i soli punti {soli_punti}, con contributo {con_contributo}; "
      f"contributo totale {frazione(z1)}")
print(f"  Punti usati: {sum(a1[i - 1] for i in soli_punti) + sum(b1[i - 1] for i in con_contributo)}"
      f" su {p1}; preferenza "
      f"{sum(d1[i - 1] for i in soli_punti + con_contributo)} >= {ell1}")
riga = registra_bound("1 premi", ub1, lb1, zlp1, zlp1r, z1)
salva_dati(pd.DataFrame([riga]), "premi1_bound")
assert lb1 <= zlp1 <= z1 <= ub1 + 1e-9

# ---------- 5. DOMANDE DI MODELLAZIONE AGGIUNTIVE ----------
varianti = {}


def variante(nome, m):
    z = risolvi(m)
    print(f"  {nome:70s} z = {frazione(z)}")
    return z


# 1a: i premi 3 e 5 sono alternativi (al piu' uno dei due, in qualunque modalita')
m, x, y = modello_1(a1, b1, c1, d1, p1, ell1)
m.addConstr(x[2] + y[2] + x[4] + y[4] <= 1, name="alternativi")
varianti["1a"] = variante("1a. I premi 3 e 5 sono alternativi (x3+y3+x5+y5 <= 1)", m)
# 1b: si vogliono almeno quattro premi, oltre alla soglia di preferenza
m, x, y = modello_1(a1, b1, c1, d1, p1, ell1)
m.addConstr(gp.quicksum(x[i] + y[i] for i in R(s1)) >= 4, name="almeno_quattro")
varianti["1b"] = variante("1b. Si vogliono almeno quattro premi (sum_i (x_i+y_i) >= 4)", m)
salva_dati(pd.DataFrame({"variante": list(varianti), "z": list(varianti.values())}),
           "premi1_varianti")

# ---------- 6. FIGURA ----------
fig, ax = plt.subplots(figsize=(6.8, 3.0))
premi = list(R(1, s1 + 1))
larghezza = 0.38
ax.bar([i - larghezza / 2 for i in premi], a1, larghezza, color=TEAL, label="punti (modalita' a)")
ax.bar([i + larghezza / 2 for i in premi], b1, larghezza, color=ARANCIO,
       label="punti (modalita' b, + contributo)")
for i in R(s1):
    if x1[i].X > 0.5:
        ax.annotate("scelto", (i + 1 - larghezza / 2, a1[i]), ha="center", va="bottom",
                    fontsize=8, color=BLU)
    if y1[i].X > 0.5:
        ax.annotate(f"scelto\n{c1[i]} EUR", (i + 1 + larghezza / 2, b1[i]), ha="center",
                    va="bottom", fontsize=8, color=ROSSO)
ax.set_xticks(premi)
ax.set_xticklabels([f"premio {i}\n(pref. {d1[i - 1]})" for i in premi], fontsize=8)
ax.set_ylabel("punti richiesti")
ax.set_ylim(0, max(a1) + 3)
ax.set_title(f"10.1: le modalita' scelte (contributo totale {frazione(z1)} EUR)")
ax.legend(fontsize=8)
salva_figura(fig, "cap10_premi_ottimo")
print("Fine.")
