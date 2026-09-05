"""Capitolo 1 -- Che cos'e' un modello MIP: rilassamento, arrotondamento, bound.

Verifica numerica degli esempi del capitolo: il controesempio
dell'arrotondamento, i due rilassamenti (puro e con i bound conservati),
l'ottimo intero e la traccia del branch-and-bound svolto a mano nel testo.
Tutti i numeri citati nella dispensa e sul sito escono da qui.
"""
import gurobipy as gp
import numpy as np
import pandas as pd
from gurobipy import GRB

from mip import (ammissibile, frazione, nuovo_modello, rilassamento, risolvi,
                 stampa_soluzione, valuta, viola_interezza)
from stile import BLU, CICLO, GRIGIO, ROSSO, TEAL, VERDE, intestazione, plt, salva_dati, salva_figura

R = range

# ---------- 1. IL MODELLO DELL'ESEMPIO ----------
intestazione("1. max x1 + x2  s.t.  2x1 + 2x2 <= 3,  x1, x2 binarie")


def modello_esempio(binarie=True, superiore=True):
    """Il modello (1.1) del capitolo.

    binarie=True   -> MILP;  binarie=False -> rilassamento continuo
    superiore=True -> si conserva x <= 1 (rilassamento LP+); False -> solo x >= 0
    """
    m = nuovo_modello("arrotondamento")
    tipo = GRB.BINARY if binarie else GRB.CONTINUOUS
    ub = 1.0 if superiore else GRB.INFINITY
    x = m.addVars(2, vtype=tipo, lb=0.0, ub=ub, name="x")
    m.setObjective(x[0] + x[1], GRB.MAXIMIZE)
    m.addConstr(2 * x[0] + 2 * x[1] <= 3, name="risorsa")
    return m, x


# ---------- 2. I DUE RILASSAMENTI ----------
intestazione("2. I due rilassamenti: puro (x >= 0) e con i bound conservati (x <= 1)")
m_lp, x_lp = modello_esempio(binarie=False, superiore=False)
zlp = risolvi(m_lp)
print(f"Rilassamento senza i bound   z(LP)  = {frazione(zlp)}   soluzione restituita dal solver:")
stampa_soluzione(m_lp)
m_lpp, x_lpp = modello_esempio(binarie=False, superiore=True)
zlpp = risolvi(m_lpp)
vertice = (x_lpp[0].X, x_lpp[1].X)
print(f"Rilassamento LP+    z(LP+) = {frazione(zlpp)}   soluzione restituita dal solver: "
      f"({frazione(vertice[0])}, {frazione(vertice[1])})")
print("Entrambi valgono 3/2: il vincolo di risorsa da' gia' x1 + x2 <= 3/2, e il")
print("limite x <= 1 non taglia nessun punto di quel segmento.")

# tutte le soluzioni ottime del rilassamento LP+ sono il segmento x1 + x2 = 3/2 in [0,1]^2
for punto in [(0.75, 0.75), (1.0, 0.5), (0.5, 1.0)]:
    z, viol = valuta(m_lpp, {"x[0]": punto[0], "x[1]": punto[1]})
    assert viol <= 1e-9 and abs(z - 1.5) <= 1e-9
    print(f"  ({frazione(punto[0])}, {frazione(punto[1])}) e' ammissibile per LP+ e vale "
          f"{frazione(z)}: e' una delle infinite soluzioni ottime.")

# ---------- 3. PERCHE' L'ARROTONDAMENTO FALLISCE ----------
intestazione("3. Arrotondamento delle soluzioni frazionarie")
m_mip, x_mip = modello_esempio(binarie=True)
for base in [(0.75, 0.75), (1.0, 0.5)]:
    for verso, arr in [("piu' vicino", lambda v: round(v)), ("verso il basso", int)]:
        cand = {"x[0]": float(arr(base[0])), "x[1]": float(arr(base[1]))}
        z, viol = valuta(m_mip, cand)
        ok = ammissibile(m_mip, cand)
        print(f"  da ({frazione(base[0])}, {frazione(base[1])}) arrotondando {verso:14s} -> "
              f"({frazione(cand['x[0]'])}, {frazione(cand['x[1]'])})  "
              f"{'ammissibile, valore ' + frazione(z) if ok else f'NON ammissibile (violazione {viol:g})'}")
assert not ammissibile(m_mip, {"x[0]": 1.0, "x[1]": 1.0})
assert ammissibile(m_mip, {"x[0]": 1.0, "x[1]": 0.0})
# il controllo di interezza serve davvero: (1, 1/2) soddisfa i vincoli lineari ma non e' intera
assert valuta(m_mip, {"x[0]": 1.0, "x[1]": 0.5})[1] <= 1e-9
assert viola_interezza(m_mip, {"x[0]": 1.0, "x[1]": 0.5}) == 0.5
assert not ammissibile(m_mip, {"x[0]": 1.0, "x[1]": 0.5})
print("  (1, 1/2) soddisfa i vincoli lineari ma viola l'interezza di 1/2:")
print("  la sola ammissibilita' continua non certifica un bound primale intero.")

# ---------- 4. L'OTTIMO INTERO ----------
intestazione("4. L'ottimo intero")
zmilp = risolvi(m_mip)
print(f"z(MILP) = {frazione(zmilp)}   soluzione ottima:")
stampa_soluzione(m_mip)
print(f"Divario fra rilassamento e ottimo intero: {frazione(zlpp)} - {frazione(zmilp)} = "
      f"{frazione(zlpp - zmilp)}")
salva_dati(pd.DataFrame([{"modello": "esempio 1.1", "z_lp": zlp, "z_lp_rafforzato": zlpp,
                          "z_milp": zmilp}]), "cap01_bound")


# ---------- 5. IL BRANCH-AND-BOUND SVOLTO A MANO ----------
intestazione("5. Branch-and-bound: la traccia riportata nel capitolo")


def nodo(fissa: dict):
    """Rilassamento LP+ del sottoproblema con le variabili limitate da `fissa`.

    `fissa` e' {indice: (lb, ub)}: sono i rami x_j <= floor(v) e x_j >= ceil(v).
    """
    m, x = modello_esempio(binarie=False, superiore=True)
    for j, (lo, hi) in fissa.items():
        x[j].LB, x[j].UB = lo, hi
    m.optimize()
    if m.Status != GRB.OPTIMAL:
        return None, None
    return m.ObjVal, (x[0].X, x[1].X)


passi = []
for etichetta, fissa in [("radice", {}),
                         ("x1 <= 0", {0: (0.0, 0.0)}),
                         ("x1 >= 1", {0: (1.0, 1.0)}),
                         ("x1 >= 1, x2 <= 0", {0: (1.0, 1.0), 1: (0.0, 0.0)}),
                         ("x1 >= 1, x2 >= 1", {0: (1.0, 1.0), 1: (1.0, 1.0)})]:
    z, sol = nodo(fissa)
    if z is None:
        print(f"  {etichetta:20s} inammissibile: il ramo si scarta")
        passi.append({"nodo": etichetta, "z_lp": None, "x1": None, "x2": None, "intera": False})
        continue
    intera = all(abs(v - round(v)) <= 1e-9 for v in sol)
    print(f"  {etichetta:20s} z(LP+) = {frazione(z):>4}   x = ({frazione(sol[0])}, "
          f"{frazione(sol[1])}){'   soluzione intera: candidato incumbent' if intera else '   frazionaria: si ramifica'}")
    passi.append({"nodo": etichetta, "z_lp": z, "x1": sol[0], "x2": sol[1], "intera": intera})
salva_dati(pd.DataFrame(passi), "cap01_branch")
assert passi[0]["z_lp"] == 1.5 and passi[1]["z_lp"] == 1.0 and passi[2]["z_lp"] == 1.5
assert passi[3]["z_lp"] == 1.0 and passi[4]["z_lp"] is None
print("  L'incumbent finale vale 1: e' l'ottimo, e nessun sottoproblema resta aperto.")

# ---------- 6. FIGURA: LA REGIONE AMMISSIBILE E I PUNTI INTERI ----------
fig, ax = plt.subplots(figsize=(5.4, 5.0))
# poligono ammissibile del rilassamento LP+: {0<=x<=1, 2x1+2x2<=3}
poligono = [(0, 0), (1, 0), (1, 0.5), (0.5, 1), (0, 1)]
ax.fill(*zip(*poligono), color=TEAL, alpha=0.16, zorder=1,
        label="rilassamento LP$^+$")
ax.plot([0.25, 1.5], [1.25, 0.0], color=TEAL, lw=1.6, zorder=2,
        label="$2x_1 + 2x_2 = 3$")
for (p, q) in [(0, 0), (1, 0), (0, 1)]:
    ax.plot(p, q, "o", color=VERDE, ms=11, zorder=4)
    ax.annotate(f"({p},{q})", (p, q), textcoords="offset points", xytext=(9, 9),
                fontsize=9, color=VERDE)
ax.plot(1, 1, "X", color=ROSSO, ms=12, zorder=4)
ax.annotate("(1,1): $2+2 > 3$", (1, 1), textcoords="offset points", xytext=(-92, 10),
            fontsize=9, color=ROSSO)
for (p, q), testo in [((0.75, 0.75), "$(3/4,3/4)$"), ((1.0, 0.5), "$(1,1/2)$")]:
    ax.plot(p, q, "s", color=BLU, ms=7, zorder=4)
    ax.annotate(testo, (p, q), textcoords="offset points", xytext=(8, -14), fontsize=9, color=BLU)
ax.plot([], [], "o", color=VERDE, ms=9, label="punti interi ammissibili")
ax.plot([], [], "X", color=ROSSO, ms=9, label="punto intero non ammissibile")
ax.plot([], [], "s", color=BLU, ms=6, label="soluzioni ottime del rilassamento")
ax.set_xlim(-0.15, 1.45)
ax.set_ylim(-0.15, 1.45)
ax.set_xlabel("$x_1$")
ax.set_ylabel("$x_2$")
ax.set_title("Rilassamento LP$^+$ e punti interi\n$z(\\mathrm{LP}^+) = 3/2$, $z(\\mathrm{MILP}) = 1$")
ax.legend(loc="upper right", fontsize=8)
ax.set_aspect("equal")
salva_figura(fig, "cap01_rilassamento")
print("Fine.")
