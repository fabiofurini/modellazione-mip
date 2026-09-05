"""Problema 11.1 -- Campi estivi: bambini di piu' nazionalita' in piu' campi.

Variabili di conteggio (non binarie), capacita' per campo e due vincoli di
composizione: in ogni campo le bambine non devono essere meno dei bambini, e la
nazionalita' c non deve essere meno di ogni altra. Il secondo si scrive una volta
sola perche' le nazionalita' sono due; con s > 2 servono s - 1 disuguaglianze.
"""
import gurobipy as gp
import pandas as pd
from gurobipy import GRB

from mip import (ammissibile, due_rilassamenti, frazione, nuovo_modello, registra_bound,
                 risolvi, valuta)
from stile import ARANCIO, BLU, GRIGIO, TEAL, intestazione, plt, salva_dati, salva_figura

R = range

# ---------- 1. MODELLO E ISTANZA ----------
intestazione("11.1 Campi estivi: accettare il maggior numero di bambini")
f1 = [8, 10]        # bambine disponibili per nazionalita'
g1 = [4, 12]        # bambini disponibili per nazionalita'
d1 = [15, 8]        # capacita' dei campi
c1 = 0              # nazionalita' che deve essere maggioritaria (indice 0 = nazionalita' 1)
s1, r1 = len(f1), len(d1)
salva_dati(pd.DataFrame({"nazionalita": R(1, s1 + 1), "bambine": f1, "bambini": g1}),
           "campi1_dati")
salva_dati(pd.DataFrame({"campo": R(1, r1 + 1), "capacita": d1}), "campi1_capacita")


def modello_1(f, g, d, c):
    s, r = len(f), len(d)
    m = nuovo_modello("campi")
    x = m.addVars(s, r, vtype=GRB.INTEGER, name="x")    # bambine di nazionalita' i nel campo j
    y = m.addVars(s, r, vtype=GRB.INTEGER, name="y")    # bambini di nazionalita' i nel campo j
    m.setObjective(gp.quicksum(x[i, j] + y[i, j] for i in R(s) for j in R(r)), GRB.MAXIMIZE)
    m.addConstrs((x.sum(i, "*") <= f[i] for i in R(s)), name="bambine")
    m.addConstrs((y.sum(i, "*") <= g[i] for i in R(s)), name="bambini")
    m.addConstrs((gp.quicksum(x[i, j] + y[i, j] for i in R(s)) <= d[j] for j in R(r)),
                 name="capacita")
    m.addConstrs((gp.quicksum(x[i, j] - y[i, j] for i in R(s)) >= 0 for j in R(r)),
                 name="parita")
    m.addConstrs((x[c, j] + y[c, j]
                  - gp.quicksum(x[i, j] + y[i, j] for i in R(s) if i != c) >= 0 for j in R(r)),
                 name="maggioranza")
    return m, x, y


def duale_1(f, g, d, c):
    """min sum_i f_i alpha_i + sum_i g_i beta_i + sum_j d_j gamma_j

    con alpha, beta, gamma >= 0 per i tre vincoli di <=, e delta_j, eps_j >= 0 per
    i due vincoli di composizione (scritti come >= 0, quindi entrano con segno
    meno nei vincoli duali). Il segno che moltiplica eps_j dipende da i: e' -1
    per la nazionalita' maggioritaria c e +1 per tutte le altre.
    """
    s, r = len(f), len(d)
    dl = nuovo_modello("duale_campi")
    alpha = dl.addVars(s, name="alpha")
    beta = dl.addVars(s, name="beta")
    gamma = dl.addVars(r, name="gamma")
    delta = dl.addVars(r, name="delta")
    eps = dl.addVars(r, name="eps")
    dl.setObjective(gp.quicksum(f[i] * alpha[i] for i in R(s))
                    + gp.quicksum(g[i] * beta[i] for i in R(s))
                    + gp.quicksum(d[j] * gamma[j] for j in R(r)), GRB.MINIMIZE)
    for i in R(s):
        segno = -1 if i == c else 1
        for j in R(r):
            dl.addConstr(alpha[i] + gamma[j] - delta[j] + segno * eps[j] >= 1, name=f"rcx[{i},{j}]")
            dl.addConstr(beta[i] + gamma[j] + delta[j] + segno * eps[j] >= 1, name=f"rcy[{i},{j}]")
    return dl


m1, x1, y1 = modello_1(f1, g1, d1, c1)

# ---------- 2. EURISTICA COSTRUTTIVA (LOWER BOUND) ----------
# euristica costruttiva campo per campo: si riempie il campo corrente prendendo prima la
# nazionalita' maggioritaria (bambine e bambini) e poi le altre, senza mai
# violare capacita', parita' e maggioranza.
def euristica(f, g, d, c):
    s, r = len(f), len(d)
    x = {(i, j): 0 for i in R(s) for j in R(r)}
    y = {(i, j): 0 for i in R(s) for j in R(r)}
    rf, rg = list(f), list(g)
    passi = []
    ordine = [c] + [i for i in R(s) if i != c]
    for j in R(r):
        for i in ordine:
            for quale, res, var in (("bambine", rf, x), ("bambini", rg, y)):
                while res[i] > 0:
                    var[i, j] += 1
                    tot = sum(x[k, j] + y[k, j] for k in R(s))
                    par = sum(x[k, j] - y[k, j] for k in R(s))
                    magg = (x[c, j] + y[c, j]
                            - sum(x[k, j] + y[k, j] for k in R(s) if k != c))
                    if tot > d[j] or par < 0 or magg < 0:
                        var[i, j] -= 1
                        break
                    res[i] -= 1
        occupati = sum(x[k, j] + y[k, j] for k in R(s))
        passi.append(f"campo {j + 1} (capacita' {d[j]}): "
                     + ", ".join(f"naz. {i + 1} -> {x[i, j]} bambine e {y[i, j]} bambini"
                                 for i in R(s))
                     + f"; occupati {occupati} posti")
    return x, y, passi


x_eur, y_eur, passi = euristica(f1, g1, d1, c1)
for k, riga in enumerate(passi, 1):
    print(f"  Passo {k}. {riga}")
lb1 = sum(x_eur[i, j] + y_eur[i, j] for i in R(s1) for j in R(r1))
sol_eur = ({f"x[{i},{j}]": x_eur[i, j] for i in R(s1) for j in R(r1)}
           | {f"y[{i},{j}]": y_eur[i, j] for i in R(s1) for j in R(r1)})
assert ammissibile(m1, sol_eur), sol_eur
print(f"  Bambine e bambini accettati dall'euristica: lb = {frazione(lb1)}")
print("  L'euristica esaurisce la nazionalita' maggioritaria nel primo campo: nel secondo non")
print("  resta nessuno che possa fare da maggioranza e il campo resta vuoto.")

# ---------- 3. RILASSAMENTO LP E DUALE (UPPER BOUND) ----------
dl1 = duale_1(f1, g1, d1, c1)
# ricetta: alpha = beta = delta = eps = 0 e gamma_j = 1, cioe' si valuta solo la
# capacita': ogni bambino accettato occupa un posto, quindi non se ne possono
# accettare piu' di sum_j d_j
mano = {f"gamma[{j}]": 1.0 for j in R(r1)}
ub1, viol = valuta(dl1, mano)
assert viol <= 1e-9, viol
print("  Duale a mano: alpha = beta = delta = eps = 0 e gamma_j = 1 (ogni bambino occupa un")
print("  posto). Tutti i vincoli duali diventano gamma_j >= 1 e sono soddisfatti:")
print(f"  ub = sum_j d_j = {' + '.join(map(str, d1))} = {frazione(ub1)}")
zlp1, zlp1r, _ = due_rilassamenti(m1, dl1)

# ---------- 4. OTTIMO DEL MILP ----------
z1 = risolvi(m1)
print("  Soluzione ottima:")
for j in R(r1):
    tot = sum(x1[i, j].X + y1[i, j].X for i in R(s1))
    print(f"    campo {j + 1}: " + ", ".join(
        f"naz. {i + 1} -> {int(x1[i, j].X)} bambine e {int(y1[i, j].X)} bambini" for i in R(s1))
        + f"; {int(tot)} posti su {d1[j]}")
riga = registra_bound("1 campi", ub1, lb1, zlp1, zlp1r, z1, senso="max")
salva_dati(pd.DataFrame([riga]), "campi1_bound")
assert lb1 <= z1 <= zlp1 <= ub1 + 1e-9
print(f"  Il bound duale {frazione(ub1)} coincide con l'ottimo: la capacita' e' satura e il")
print("  certificato chiude il gap. Il divario da colmare era tutto dal lato dell'euristica.")

# ---------- 5. IL LIMITE VERO E' LA NAZIONALITA' MAGGIORITARIA ----------
intestazione("11.1 Due argomenti combinatori sui bound")
tot_c = f1[c1] + g1[c1]
print(f"  In ogni campo la nazionalita' {c1 + 1} non e' meno di tutte le altre messe insieme,")
print(f"  quindi in ogni campo occupa almeno meta' dei posti. Ne ha {tot_c} in tutto:")
print(f"  gli accettati sono al piu' 2 * {tot_c} = {2 * tot_c}. E' un secondo bound superiore,")
print(f"  peggiore di quello di capacita' ({frazione(ub1)}) su questa istanza ma non in generale.")
print(f"  Analogamente le bambine sono {sum(f1)}: con bambine >= bambini in ogni campo, gli")
print(f"  accettati sono al piu' 2 * {sum(f1)} = {2 * sum(f1)}.")
salva_dati(pd.DataFrame([{"argomento": "capacita' dei campi", "bound": ub1},
                         {"argomento": "nazionalita' maggioritaria", "bound": 2 * tot_c},
                         {"argomento": "bambine disponibili", "bound": 2 * sum(f1)}]),
           "campi1_argomenti")

# ---------- 6. DOMANDE DI MODELLAZIONE AGGIUNTIVE ----------
varianti = {}


def variante(nome, m):
    z = risolvi(m)
    print(f"  {nome:70s} z = {frazione(z)}")
    return z


# 1a: il campo 1 si ingrandisce; il limite passa dalla capacita' alla nazionalita' 1
m, x, y = modello_1(f1, g1, [20, d1[1]], c1)
varianti["1a"] = variante("1a. Il campo 1 arriva a 20 posti (d1 = 20)", m)
print(f"       ora la capacita' totale e' 28 ma l'ottimo si ferma a 2 * {f1[c1] + g1[c1]} = "
      f"{2 * (f1[c1] + g1[c1])}: comanda la nazionalita' maggioritaria.")
# 1b: la nazionalita' maggioritaria non puo' essere divisa fra piu' campi
m, x, y = modello_1(f1, g1, d1, c1)
M1 = f1[c1] + g1[c1]
w = m.addVars(r1, vtype=GRB.BINARY, name="w")
m.addConstrs((x[c1, j] + y[c1, j] - M1 * w[j] <= 0 for j in R(r1)), name="unico_campo")
m.addConstr(w.sum() <= 1, name="al_piu_un_campo")
varianti["1b"] = variante("1b. La nazionalita' 1 non puo' essere divisa fra piu' campi", m)
print("       e' esattamente cio' che fa l'euristica: il secondo campo resta vuoto e si torna")
print(f"       al valore {frazione(lb1)}.")
salva_dati(pd.DataFrame({"variante": list(varianti), "z": list(varianti.values())}),
           "campi1_varianti")

# ---------- 7. FIGURA ----------
fig, ax = plt.subplots(figsize=(6.8, 3.0))
etichette, base = [], []
for j in R(r1):
    etichette.append(f"campo {j + 1}")
for k, (nome, sol) in enumerate([("euristica", (x_eur, y_eur)),
                                 ("ottimo", ({(i, j): x1[i, j].X for i in R(s1) for j in R(r1)},
                                             {(i, j): y1[i, j].X for i in R(s1) for j in R(r1)}))]):
    xs, ys = sol
    off = -0.2 + 0.4 * k
    for j in R(r1):
        naz1 = xs[c1, j] + ys[c1, j]
        altre = sum(xs[i, j] + ys[i, j] for i in R(s1) if i != c1)
        ax.bar(j + off, naz1, 0.36, color=TEAL if k else ARANCIO)
        ax.bar(j + off, altre, 0.36, bottom=naz1, color=BLU if k else GRIGIO)
        ax.annotate(nome, (j + off, -1.2), ha="center", fontsize=7)
for j in R(r1):
    ax.plot([j - 0.45, j + 0.45], [d1[j], d1[j]], color="black", lw=1.4, ls="--")
ax.plot([], [], color=ARANCIO, lw=6, label="euristica: naz. maggioritaria")
ax.plot([], [], color=GRIGIO, lw=6, label="euristica: altre")
ax.plot([], [], color=TEAL, lw=6, label="ottimo: naz. maggioritaria")
ax.plot([], [], color=BLU, lw=6, label="ottimo: altre")
ax.plot([], [], color="black", ls="--", label="capacita'")
ax.set_xticks(R(r1))
ax.set_xticklabels(etichette)
ax.set_ylim(-2, max(d1) + 2)
ax.set_ylabel("bambini accettati")
ax.set_title(f"11.1: euristica {frazione(lb1)} contro ottimo {frazione(z1)}")
ax.legend(fontsize=7, ncol=2)
salva_figura(fig, "cap10_campi_ottimo")
print("Fine.")
