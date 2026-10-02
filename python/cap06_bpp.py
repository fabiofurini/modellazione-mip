"""Bin packing: quanti contenitori bastano (capitolo 3).

Il primo dei tre problemi che il capitolo delle euristiche riprende: li' si
costruiscono a mano next-fit, first-fit e best-fit, qui si scrive il modello che
dice qual e' l'ottimo. La capacita' e' scritta come attivazione: finche' il
contenitore non si apre non puo' ricevere niente.
"""
import gurobipy as gp
import pandas as pd
from gurobipy import GRB

from esteso import salva_modello
from mip import frazione, nuovo_modello, risolvi
from stile import intestazione, salva_dati

R = range

intestazione("Bin packing: il minimo numero di contenitori")
w_bpp = [5, 4, 3, 3]             # peso degli oggetti
c_bpp = 7                        # capacita' di un contenitore
n_bpp = len(w_bpp)


def modello_bpp(w, c, k):
    n = len(w)
    m = nuovo_modello("bin_packing")
    x = m.addVars(n, k, vtype=GRB.BINARY, name="x")
    y = m.addVars(k, vtype=GRB.BINARY, name="y")
    m.setObjective(y.sum(), GRB.MINIMIZE)
    m.addConstrs((x.sum(j, "*") == 1 for j in R(n)), name="oggetto")
    m.addConstrs((gp.quicksum(w[j] * x[j, b] for j in R(n)) <= c * y[b] for b in R(k)),
                 name="capacita")
    return m, x, y


# con un contenitore per oggetto si trova quanti ne servono davvero; il modello
# che si stampa usa poi solo quelli, perche' gli altri resterebbero vuoti
m_largo, _, _ = modello_bpp(w_bpp, c_bpp, n_bpp)
z_bpp = risolvi(m_largo)
minimo_teorico = -(-sum(w_bpp) // c_bpp)        # arrotondamento all'insu'
print(f"  Pesi {w_bpp}, capacita' {c_bpp}.")
print(f"  Il peso totale e' {sum(w_bpp)}: nessuna soluzione usa meno di "
      f"{sum(w_bpp)}/{c_bpp} = {minimo_teorico} contenitori, e l'ottimo ne usa {int(z_bpp)}.")
assert z_bpp == minimo_teorico
m_bpp, x_bpp, y_bpp = modello_bpp(w_bpp, c_bpp, int(z_bpp))
risolvi(m_bpp)
salva_modello(m_bpp, "cap06_bpp")
print("  Il rilassamento compra frazioni di contenitore e scende a "
      f"{frazione(sum(w_bpp) / c_bpp)}: non sa che un contenitore si apre tutto intero.")
salva_dati(pd.DataFrame([{"problema": "bin packing", "z_milp": z_bpp}]), "cap06_bpp")
print("Fine.")
