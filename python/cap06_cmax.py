"""Makespan su macchine identiche (capitolo 3).

Il secondo dei tre problemi che il capitolo delle euristiche riprende: li' si
confronta l'ordine naturale con LPT sugli stessi quattro lavori. L'obiettivo e'
una sola variabile, z, e sono i vincoli di carico a darle significato: e' la
tecnica min-max.
"""
import gurobipy as gp
import pandas as pd
from gurobipy import GRB

from esteso import salva_modello
from mip import frazione, nuovo_modello, risolvi
from stile import intestazione, salva_dati

R = range

intestazione("Makespan: il carico della macchina piu' carica")
d_cmax = [3, 4, 5, 6]            # durate dei lavori
k_cmax = 2                       # macchine identiche


def modello_cmax(d, k):
    n = len(d)
    m = nuovo_modello("makespan")
    x = m.addVars(n, k, vtype=GRB.BINARY, name="x")
    z = m.addVar(name="z")
    m.setObjective(z, GRB.MINIMIZE)
    m.addConstrs((x.sum(j, "*") == 1 for j in R(n)), name="lavoro")
    m.addConstrs((gp.quicksum(d[j] * x[j, mm] for j in R(n)) <= z for mm in R(k)),
                 name="carico")
    return m, x, z


m_cmax, x_cmax, z_var = modello_cmax(d_cmax, k_cmax)
z_cmax = risolvi(m_cmax)
salva_modello(m_cmax, "cap06_cmax")
print(f"  Durate {d_cmax} su {k_cmax} macchine identiche.")
print(f"  Il carico totale e' {sum(d_cmax)}: diviso per {k_cmax} da' "
      f"{frazione(sum(d_cmax) / k_cmax)}, e l'ottimo vale {frazione(z_cmax)}.")
for mm in R(k_cmax):
    lavori = [j + 1 for j in R(len(d_cmax)) if x_cmax[j, mm].X > 0.5]
    print(f"    macchina {mm + 1}: lavori {lavori}, carico "
          f"{sum(d_cmax[j - 1] for j in lavori)}")
assert z_cmax == sum(d_cmax) / k_cmax
salva_dati(pd.DataFrame([{"problema": "makespan", "z_milp": z_cmax}]), "cap06_cmax")
print("Fine.")
