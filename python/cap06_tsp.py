"""Commesso viaggiatore con la formulazione MTZ (capitolo 3).

Il terzo dei tre problemi che il capitolo delle euristiche riprende: li' si
costruisce il tour con il vicino piu' vicino, qui si trova l'ottimo.

Le variabili u ordinano le citta' lungo il giro: il vincolo
u_i - u_j + n x_ij <= n - 1 e' vero se x_ij = 0 e obbliga u_j >= u_i + 1 se
x_ij = 1. I sottocicli che non toccano la citta' 1 sono cosi' esclusi, perche'
richiederebbero una catena di u sempre crescenti che si richiude su se stessa.
"""
import gurobipy as gp
import pandas as pd
from gurobipy import GRB

from esteso import salva_modello
from mip import frazione, nuovo_modello, risolvi
from stile import intestazione, salva_dati

R = range

intestazione("Commesso viaggiatore: il giro piu' corto")
D_tsp = [[0, 4, 5, 9],
         [4, 0, 9, 9],
         [5, 9, 0, 4],
         [9, 9, 4, 0]]
n_tsp = len(D_tsp)


def modello_tsp(D):
    n = len(D)
    m = nuovo_modello("tsp")
    x = m.addVars(((i, j) for i in R(n) for j in R(n) if i != j), vtype=GRB.BINARY, name="x")
    u = m.addVars(R(1, n), lb=1, ub=n - 1, name="u")
    m.setObjective(gp.quicksum(D[i][j] * x[i, j] for i, j in x), GRB.MINIMIZE)
    m.addConstrs((gp.quicksum(x[i, j] for j in R(n) if j != i) == 1 for i in R(n)), name="esce")
    m.addConstrs((gp.quicksum(x[i, j] for i in R(n) if i != j) == 1 for j in R(n)), name="entra")
    m.addConstrs((u[i] - u[j] + n * x[i, j] <= n - 1
                  for i in R(1, n) for j in R(1, n) if i != j), name="mtz")
    return m, x, u


m_tsp, x_tsp, u_tsp = modello_tsp(D_tsp)
salva_modello(m_tsp, "cap06_tsp")
z_tsp = risolvi(m_tsp)
seguente = {i: j for (i, j) in x_tsp if x_tsp[i, j].X > 0.5}
giro, citta = [0], 0
while seguente[citta] != 0:
    citta = seguente[citta]
    giro.append(citta)
print(f"  {n_tsp} citta', distanze simmetriche e metriche.")
print("  Giro ottimo: " + " -> ".join(str(c + 1) for c in giro + [0])
      + f", lunghezza {frazione(z_tsp)}.")
salva_dati(pd.DataFrame([{"problema": "TSP", "z_milp": z_tsp}]), "cap06_tsp")
print("Fine.")
