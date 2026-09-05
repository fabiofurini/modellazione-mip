"""Problema 12.2 -- Spedizioni in scatole: flusso multiprodotto e conteggio dei
contenitori.

Le quantita' spedite sono un flusso a piu' prodotti fra stabilimenti e clienti;
sopra ci sono le scatole, che sono un conteggio intero legato al flusso dalla
capacita' (tecnica 3.4: y >= ceil(somma / w)). Il rilassamento lineare vede solo
il rapporto fra unita' e capacita' e perde completamente il fatto che una scatola
non si divide fra due clienti.
"""
import gurobipy as gp
import pandas as pd
from gurobipy import GRB

from mip import (ammissibile, due_rilassamenti, frazione, nuovo_modello, registra_bound,
                 risolvi, valuta)
from stile import ARANCIO, BLU, GRIGIO, TEAL, intestazione, plt, salva_dati, salva_figura

R = range


def scatole(n):
    """"1 scatola" oppure "3 scatole"."""
    return f"{int(n)} scatola" if int(n) == 1 else f"{int(n)} scatole"

# ---------- 1. MODELLO E ISTANZA ----------
intestazione("12.2 Spedizioni in scatole: minimizzare il numero di scatole")
d2 = [[5, 0],       # unita' del prodotto p ordinate dal cliente c
      [2, 4]]
a2 = [[8, 6],       # unita' del prodotto p disponibili nello stabilimento s
      [5, 7]]
w2 = 10             # capacita' di una scatola, in unita' di prodotto
nk, nm, nn = len(d2), len(d2[0]), len(a2[0])   # prodotti, clienti, stabilimenti
D2 = sum(d2[p][c] for p in R(nk) for c in R(nm))
salva_dati(pd.DataFrame([{"prodotto": p + 1, "cliente": c + 1, "domanda": d2[p][c]}
                         for p in R(nk) for c in R(nm)]), "spedizioni2_domanda")
salva_dati(pd.DataFrame([{"prodotto": p + 1, "stabilimento": s + 1, "disponibilita": a2[p][s]}
                         for p in R(nk) for s in R(nn)]), "spedizioni2_disponibilita")
print(f"  Unita' da spedire in tutto: {D2}; capacita' di una scatola: {w2}.")


def modello_2(d, a, w):
    nk, nm, nn = len(d), len(d[0]), len(a[0])
    m = nuovo_modello("spedizioni")
    x = m.addVars(nk, nn, nm, vtype=GRB.INTEGER, name="x")   # unita' p da s a c
    y = m.addVars(nn, nm, vtype=GRB.INTEGER, name="y")       # scatole da s a c
    m.setObjective(y.sum(), GRB.MINIMIZE)
    m.addConstrs((x.sum(p, "*", c) == d[p][c] for p in R(nk) for c in R(nm)), name="domanda")
    m.addConstrs((x.sum(p, s, "*") <= a[p][s] for p in R(nk) for s in R(nn)),
                 name="disponibilita")
    m.addConstrs((w * y[s, c] - x.sum("*", s, c) >= 0 for s in R(nn) for c in R(nm)),
                 name="capacita")
    return m, x, y


def duale_2(d, a, w):
    """max sum_pc d_pc alpha_pc + sum_ps a_ps beta_ps

    alpha libera (domanda con =), beta <= 0 (disponibilita' con <=), gamma >= 0
    (legame con le scatole). Colonne:
      x_psc:  alpha_pc + beta_ps - gamma_sc <= 0
      y_sc:   w gamma_sc <= 1
    """
    nk, nm, nn = len(d), len(d[0]), len(a[0])
    dl = nuovo_modello("duale_spedizioni")
    alpha = dl.addVars(nk, nm, lb=-GRB.INFINITY, name="alpha")
    beta = dl.addVars(nk, nn, lb=-GRB.INFINITY, ub=0.0, name="beta")
    gamma = dl.addVars(nn, nm, name="gamma")
    dl.setObjective(gp.quicksum(d[p][c] * alpha[p, c] for p in R(nk) for c in R(nm))
                    + gp.quicksum(a[p][s] * beta[p, s] for p in R(nk) for s in R(nn)),
                    GRB.MAXIMIZE)
    dl.addConstrs((alpha[p, c] + beta[p, s] - gamma[s, c] <= 0
                   for p in R(nk) for s in R(nn) for c in R(nm)), name="rcx")
    dl.addConstrs((w * gamma[s, c] <= 1 for s in R(nn) for c in R(nm)), name="rcy")
    return dl


m2, x2, y2 = modello_2(d2, a2, w2)

# ---------- 2. EURISTICA COSTRUTTIVA (UPPER BOUND) ----------
# cliente per cliente: si cerca di servirlo da un solo stabilimento, quello che
# ha tutto quello che serve; se nessuno basta si spezza l'ordine.
def euristica(d, a, w):
    nk, nm, nn = len(d), len(d[0]), len(a[0])
    res = [[a[p][s] for s in R(nn)] for p in R(nk)]
    x = {(p, s, c): 0 for p in R(nk) for s in R(nn) for c in R(nm)}
    passi = []
    for c in R(nm):
        completi = [s for s in R(nn) if all(res[p][s] >= d[p][c] for p in R(nk))]
        if completi:
            s = completi[0]
            for p in R(nk):
                x[p, s, c] = d[p][c]
                res[p][s] -= d[p][c]
            passi.append(f"cliente {c + 1}: lo stabilimento {s + 1} ha tutto l'ordine, si "
                         f"spedisce da li'")
        else:
            for p in R(nk):
                manca = d[p][c]
                for s in R(nn):
                    preso = min(manca, res[p][s])
                    x[p, s, c] += preso
                    res[p][s] -= preso
                    manca -= preso
                assert manca == 0, "ordine non soddisfacibile"
            passi.append(f"cliente {c + 1}: nessuno stabilimento basta da solo, l'ordine si "
                         f"spezza")
    y = {(s, c): -(-sum(x[p, s, c] for p in R(nk)) // w) for s in R(nn) for c in R(nm)}
    for s in R(nn):
        for c in R(nm):
            if y[s, c]:
                passi.append(f"stabilimento {s + 1} -> cliente {c + 1}: "
                             f"{sum(x[p, s, c] for p in R(nk))} unita' -> "
                             f"{scatole(y[s, c])}")
    return x, y, passi


x_eur, y_eur, passi = euristica(d2, a2, w2)
for k, riga in enumerate(passi, 1):
    print(f"  Passo {k}. {riga}")
ub2 = sum(y_eur.values())
sol_eur = ({f"x[{p},{s},{c}]": x_eur[p, s, c] for p in R(nk) for s in R(nn) for c in R(nm)}
           | {f"y[{s},{c}]": y_eur[s, c] for s in R(nn) for c in R(nm)})
assert ammissibile(m2, sol_eur), sol_eur
print(f"  Scatole usate dall'euristica: {ub2}  ->  ub = {frazione(ub2)}")

# ---------- 3. RILASSAMENTO LP E DUALE (LOWER BOUND) ----------
dl2 = duale_2(d2, a2, w2)
# ricetta: beta = 0, gamma_sc = 1/w (il massimo consentito da w gamma <= 1) e
# alpha_pc = 1/w: ogni unita' ordinata occupa 1/w di scatola
mano = ({f"gamma[{s},{c}]": 1 / w2 for s in R(nn) for c in R(nm)}
        | {f"alpha[{p},{c}]": 1 / w2 for p in R(nk) for c in R(nm)})
lb_lp, viol = valuta(dl2, mano)
assert viol <= 1e-9, viol
print(f"  Duale a mano: beta = 0, gamma_sc = alpha_pc = 1/{w2}. I vincoli duali diventano")
print(f"  1/{w2} + 0 - 1/{w2} = 0 <= 0 e {w2} * 1/{w2} = 1 <= 1: tutto verificato.")
print(f"  lb = (unita' ordinate) / {w2} = {D2} / {w2} = {frazione(lb_lp)}")
zlp2, zlp2r, _ = due_rilassamenti(m2, dl2)

# ---------- 4. UN BOUND INTERO PIU' FORTE ----------
intestazione("12.2 Il conteggio delle scatole per cliente")
clienti_attivi = [c for c in R(nm) if any(d2[p][c] > 0 for p in R(nk))]
lb2 = float(len(clienti_attivi))
print(f"  Ogni cliente con almeno un'unita' ordinata riceve almeno una scatola, e le scatole")
print(f"  non si dividono fra clienti diversi. I clienti con ordini sono {len(clienti_attivi)}:")
print(f"  lb = {frazione(lb2)}, contro {frazione(lb_lp)} del rilassamento lineare.")
print(f"  Piu' precisamente ogni cliente c riceve almeno ceil(sum_p d_pc / {w2}) scatole:")
per_cliente = [-(-sum(d2[p][c] for p in R(nk)) // w2) for c in R(nm)]
for c in R(nm):
    print(f"    cliente {c + 1}: {sum(d2[p][c] for p in R(nk))} unita' -> almeno "
          f"{scatole(per_cliente[c])}")
lb2 = float(sum(per_cliente))
print(f"  Sommando: lb = {frazione(lb2)}.")
salva_dati(pd.DataFrame([{"argomento": "duale del rilassamento LP", "bound": lb_lp},
                         {"argomento": "scatole per cliente", "bound": lb2}]),
           "spedizioni2_argomento")

# ---------- 5. OTTIMO DEL MILP ----------
z2 = risolvi(m2)
for s in R(nn):
    for c in R(nm):
        if y2[s, c].X > 0.5:
            carico = ", ".join(f"{int(x2[p, s, c].X)} del prodotto {p + 1}" for p in R(nk)
                               if x2[p, s, c].X > 0.5)
            print(f"  Stabilimento {s + 1} -> cliente {c + 1}: "
                  f"{scatole(y2[s, c].X)} con {carico}")
riga = registra_bound("2 spedizioni", ub2, lb2, zlp2, zlp2r, z2)
salva_dati(pd.DataFrame([riga]), "spedizioni2_bound")
assert lb2 <= z2 <= ub2 + 1e-9

# ---------- 6. DOMANDE DI MODELLAZIONE AGGIUNTIVE ----------
varianti = {}


def variante(nome, m):
    z = risolvi(m)
    print(f"  {nome:70s} z = {frazione(z)}")
    return z


# 2a: scatole piu' piccole
m, x, y = modello_2(d2, a2, 4)
varianti["2a"] = variante("2a. Le scatole contengono 4 unita' invece di 10", m)
# 2b: prodotti diversi non possono viaggiare nella stessa scatola
m = nuovo_modello("spedizioni_separate")
x = m.addVars(nk, nn, nm, vtype=GRB.INTEGER, name="x")
y = m.addVars(nk, nn, nm, vtype=GRB.INTEGER, name="y")
m.setObjective(y.sum(), GRB.MINIMIZE)
m.addConstrs((x.sum(p, "*", c) == d2[p][c] for p in R(nk) for c in R(nm)), name="domanda")
m.addConstrs((x.sum(p, s, "*") <= a2[p][s] for p in R(nk) for s in R(nn)), name="disponibilita")
m.addConstrs((w2 * y[p, s, c] - x[p, s, c] >= 0 for p in R(nk) for s in R(nn) for c in R(nm)),
             name="capacita")
varianti["2b"] = variante("2b. Prodotti diversi non possono viaggiare nella stessa scatola", m)
salva_dati(pd.DataFrame({"variante": list(varianti), "z": list(varianti.values())}),
           "spedizioni2_varianti")

# ---------- 7. FIGURA ----------
fig, ax = plt.subplots(figsize=(6.4, 3.0))
for s in R(nn):
    for c in R(nm):
        n = int(y2[s, c].X)
        if n:
            ax.plot([0, 1], [nn - 1 - s, nm - 1 - c], color=TEAL, lw=1 + 2 * n)
            ax.annotate(scatole(n), (0.5, (nn - 1 - s + nm - 1 - c) / 2 + 0.06),
                        ha="center", fontsize=8, color=TEAL)
for s in R(nn):
    ax.plot(0, nn - 1 - s, marker="s", color=BLU, ms=14)
    ax.annotate(f"stab. {s + 1}", (-0.06, nn - 1 - s), ha="right", va="center", fontsize=9)
for c in R(nm):
    ax.plot(1, nm - 1 - c, marker="o", color=ARANCIO, ms=14)
    ax.annotate(f"cliente {c + 1}\n({sum(d2[p][c] for p in R(nk))} unita')",
                (1.06, nm - 1 - c), ha="left", va="center", fontsize=9)
ax.set_xlim(-0.45, 1.5)
ax.set_ylim(-0.6, max(nn, nm) - 0.4)
ax.axis("off")
ax.set_title(f"12.2: piano ottimo con {frazione(z2)} scatole")
salva_figura(fig, "cap10_spedizioni_ottimo")
print("Fine.")
