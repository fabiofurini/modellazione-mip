"""Capitolo 4 -- Rilassamenti, dualita' e bound: gli esempi verificati.

Un problema di minimo e uno di massimo, scritti con il loro duale; una soluzione
duale costruita a mano e la verifica della dualita' debole; il confronto fra il
rilassamento senza i bound e quello con i bound conservati; un taglio di copertura; il
bound letto da Gurobi a fine risoluzione; e il controesempio che mostra perche'
i duali dell'LP non sono i prezzi marginali del MILP.
"""
import gurobipy as gp
import pandas as pd
from gurobipy import GRB

from mip import (ammissibile, due_rilassamenti, frazione, nuovo_modello, registra_bound,
                 rilassamento, risolvi, stampa_soluzione, valuta, viola_interezza)
from stile import (ARANCIO, BLU, CICLO, GRIGIO, ROSSO, TEAL, VERDE, intestazione,
                   plt, salva_dati, salva_figura)

R = range

# ---------- 1. UN MINIMO, IL SUO DUALE, UNA SOLUZIONE DUALE A MANO ----------
intestazione("4.1  Copertura a costo minimo: primale, duale e bound costruito a mano")
# min sum c_j x_j   s.t.  sum_{j in S_i} x_j >= 1 per ogni i,  x binaria
c41 = [4, 3, 5, 3]                       # costo delle quattro squadre
# sei zone, ciascuna al confine fra due distretti: la zona i e' coperta dalle due
# squadre dei distretti che confina
S41 = [[0, 1], [1, 2], [0, 2], [0, 3], [1, 3], [2, 3]]
n41, m41 = len(c41), len(S41)


def primale_41():
    m = nuovo_modello("copertura")
    x = m.addVars(n41, vtype=GRB.BINARY, name="x")
    m.setObjective(gp.quicksum(c41[j] * x[j] for j in R(n41)), GRB.MINIMIZE)
    m.addConstrs((gp.quicksum(x[j] for j in S41[i]) >= 1 for i in R(m41)), name="copri")
    return m, x


def duale_41():
    """max sum u_i  s.t.  sum_{i : j in S_i} u_i <= c_j,  u >= 0."""
    d = nuovo_modello("duale_copertura")
    u = d.addVars(m41, name="u")
    d.setObjective(u.sum(), GRB.MAXIMIZE)
    d.addConstrs((gp.quicksum(u[i] for i in R(m41) if j in S41[i]) <= c41[j] for j in R(n41)),
                 name="rc")
    return d, u


m41p, x41 = primale_41()
z41 = risolvi(m41p)
scelte41 = [j + 1 for j in R(n41) if x41[j].X > 0.5]
print(f"  Ottimo intero: z(MILP) = {frazione(z41)}, squadre scelte {scelte41}")

# soluzione duale costruita a mano: si assegna a ogni zona il minimo costo unitario
# disponibile, rispettando i vincoli duali una colonna alla volta (euristica costruttiva duale)
u_mano = {i: 0.0 for i in R(m41)}
residuo = {j: c41[j] for j in R(n41)}
for i in R(m41):
    incremento = min(residuo[j] for j in S41[i])
    u_mano[i] = incremento
    for j in S41[i]:
        residuo[j] -= incremento
d41, u41 = duale_41()
lb41, viol = valuta(d41, {f"u[{i}]": u_mano[i] for i in R(m41)})
assert viol <= 1e-9, viol
print("  Soluzione duale a mano (euristica costruttiva sulle zone): u = "
      + ", ".join(f"u_{i+1} = {frazione(u_mano[i])}" for i in R(m41))
      + f"   ->  lb = {frazione(lb41)}")
zlp41, zlp41r, pi41 = due_rilassamenti(m41p, d41)
print(f"  Dualita' debole verificata: {frazione(lb41)} <= {frazione(zlp41)} <= "
      f"{frazione(z41)}")
assert lb41 <= zlp41 + 1e-9 <= z41 + 1e-9
# upper bound primale: la soluzione euristica costruttiva di copertura (una zona scoperta alla volta)
scoperte = set(R(m41))
presi41 = []
while scoperte:
    j = min(R(n41), key=lambda j: c41[j] / max(1, len({i for i in scoperte if j in S41[i]}))
            if any(j in S41[i] for i in scoperte) else float("inf"))
    presi41.append(j)
    scoperte -= {i for i in scoperte if j in S41[i]}
ub41_primale = sum(c41[j] for j in presi41)
assert ammissibile(m41p, {f"x[{j}]": 1 for j in presi41})
print(f"  Euristica euristica costruttiva di copertura: squadre {sorted(j + 1 for j in presi41)}, "
      f"ub = {frazione(ub41_primale)}")
riga41 = registra_bound("copertura a costo minimo", ub41_primale, lb41, zlp41, zlp41r, z41)
salva_dati(pd.DataFrame([riga41]), "cap04_copertura")

# ---------- 2. UN MASSIMO: I RUOLI SI SCAMBIANO ----------
intestazione("4.2  Uno zaino di massimo: l'euristica da' il lower bound, il duale l'upper")
p42 = [10, 7, 6, 4]                      # valori
w42 = [5, 4, 3, 3]                       # pesi
C42 = 9


def primale_42():
    m = nuovo_modello("zaino")
    x = m.addVars(4, vtype=GRB.BINARY, name="x")
    m.setObjective(gp.quicksum(p42[j] * x[j] for j in R(4)), GRB.MAXIMIZE)
    m.addConstr(gp.quicksum(w42[j] * x[j] for j in R(4)) <= C42, name="capacita")
    return m, x


def duale_42():
    """Duale del rilassamento senza i bound (x >= 0): min C v  s.t.  w_j v >= p_j, v >= 0."""
    d = nuovo_modello("duale_zaino")
    v = d.addVar(name="v")
    d.setObjective(C42 * v, GRB.MINIMIZE)
    d.addConstrs((w42[j] * v >= p42[j] for j in R(4)), name="rc")
    return d, v


m42, x42 = primale_42()
z42 = risolvi(m42)
scelte42 = [j + 1 for j in R(4) if x42[j].X > 0.5]
print(f"  Ottimo intero: z(MILP) = {frazione(z42)}, oggetti {scelte42}, "
      f"peso {sum(w42[j] for j in R(4) if x42[j].X > 0.5)} su {C42}")
# euristica euristica costruttiva per rapporto valore/peso: da' un LOWER bound
ordine = sorted(R(4), key=lambda j: -p42[j] / w42[j])
carico, presi = 0, []
for j in ordine:
    if carico + w42[j] <= C42:
        presi.append(j)
        carico += w42[j]
lb42 = sum(p42[j] for j in presi)
assert ammissibile(m42, {f"x[{j}]": 1 for j in presi})
print(f"  Euristica costruttiva per rapporto p_j/w_j: prende {sorted(j + 1 for j in presi)}, "
      f"lb = {frazione(lb42)}")
# duale a mano: v = max_j p_j / w_j  (il rapporto migliore) e' ammissibile
v_mano = max(p42[j] / w42[j] for j in R(4))
d42, v42 = duale_42()
ub42, viol = valuta(d42, {"v": v_mano})
assert viol <= 1e-9, viol
print(f"  Soluzione duale a mano: v = max_j p_j/w_j = {frazione(v_mano)}  ->  "
      f"ub = C v = {frazione(ub42)}")
zlp42, zlp42r, _ = due_rilassamenti(m42, d42)
print(f"  Il sandwich del massimo: {frazione(lb42)} <= z(MILP) = {frazione(z42)} <= "
      f"z(LP) = {frazione(zlp42)} <= ub = {frazione(ub42)}")
assert lb42 <= z42 <= zlp42 + 1e-9 <= ub42 + 1e-9
riga42 = registra_bound("zaino di massimo", ub42, lb42, zlp42, zlp42r, z42, senso="max")
salva_dati(pd.DataFrame([riga42]), "cap04_zaino")

# ---------- 3. UN TAGLIO DI COPERTURA ----------
intestazione("4.3  Una disuguaglianza valida: il taglio di copertura")
# {1,2} e' una copertura: w_1 + w_2 = 9 > 8 = C, quindi x_1 + x_2 <= 1
from itertools import combinations
tutte = [s for k in R(2, 5) for s in combinations(R(4), k) if sum(w42[j] for j in s) > C42]
coperture = [s for s in tutte                                   # solo le minimali
             if all(sum(w42[j] for j in t) <= C42
                    for t in combinations(s, len(s) - 1))]
print("  Coperture minimali trovate: "
      + "; ".join("{" + ", ".join(str(j + 1) for j in s) + "}" for s in coperture))
m43, x43 = primale_42()
zlp43_prima, sol43, _ = rilassamento(m43, rafforzato=True)
print("  Soluzione ottima del rilassamento senza tagli: "
      + ", ".join(f"x_{j+1} = {frazione(sol43[f'x[{j}]'])}" for j in R(4)))
for s in coperture:
    somma = sum(sol43[f"x[{j}]"] for j in s)
    stato = "VIOLATO" if somma > len(s) - 1 + 1e-9 else "soddisfatto"
    print(f"    taglio su {{{', '.join(str(j + 1) for j in s)}}}: "
          f"somma = {frazione(somma)} contro {len(s) - 1}  ->  {stato}")
for s in coperture:
    m43.addConstr(gp.quicksum(x43[j] for j in s) <= len(s) - 1, name="cover" + "".join(map(str, s)))
z43 = risolvi(m43)
zlp43_dopo, _, _ = rilassamento(m43, rafforzato=True)
print(f"  z(LP+) senza tagli = {frazione(zlp43_prima)}   con i tagli di copertura = "
      f"{frazione(zlp43_dopo)}   z(MILP) = {frazione(z43)}")
assert z43 == z42, "i tagli non devono cambiare l'ottimo intero"
assert zlp43_dopo <= zlp43_prima + 1e-9
salva_dati(pd.DataFrame([{"modello": "zaino", "z_lp_senza_tagli": zlp43_prima,
                          "z_lp_con_tagli": zlp43_dopo, "z_milp": z43}]), "cap04_tagli")

# ---------- 4. QUELLO CHE FA IL SOLVER: relax() E ObjBound ----------
intestazione("4.4  Il primo rilassamento e il bound finale del solver")
m44, x44 = primale_41()          # la copertura: qui il solver deve lavorare
m44.Params.OutputFlag = 0
m44.optimize()
print(f"  Status = {m44.Status} (2 = OPTIMAL), SolCount = {m44.SolCount}")
print(f"  ObjVal   = {frazione(m44.ObjVal)}   (la migliore soluzione intera trovata)")
print(f"  ObjBound = {frazione(m44.ObjBound)} (il miglior bound dimostrato)")
print(f"  MIPGap   = {m44.MIPGap:.4f}          NodeCount = {int(m44.NodeCount)}")
zrad, _, _ = rilassamento(m44, rafforzato=True)
print(f"  Rilassamento del modello scritto da noi, con relax(): {frazione(zrad)}")
assert abs(m44.ObjBound - m44.ObjVal) <= 1e-6
assert zrad <= m44.ObjVal + 1e-9         # minimo: il rilassamento sta sotto l'ottimo
print(f"  Il rilassamento vale {frazione(zrad)}, l'ottimo intero {frazione(m44.ObjVal)}: il")
print("  gap c'e', ma NodeCount = 0. Gurobi lo chiude *nella radice*, con presolve,")
print("  tagli propri ed euristiche, senza mai ramificare.")
# per vedere il solver al lavoro si spengono presolve, tagli ed euristiche
m45, x45 = primale_41()
m45.Params.Presolve = 0
m45.Params.Cuts = 0
m45.Params.Heuristics = 0
m45.optimize()
print(f"  Con Presolve = Cuts = Heuristics = 0: z = {frazione(m45.ObjVal)}, "
      f"NodeCount = {int(m45.NodeCount)}")
print("  Stesso ottimo, ma ora i nodi si contano: 'quanto e' difficile' non e' una")
print("  proprieta' del solo modello, dipende anche da cosa il solver mette in campo.")
assert m45.ObjVal == m44.ObjVal
salva_dati(pd.DataFrame([{"configurazione": "impostazioni predefinite", "z": m44.ObjVal,
                          "z_lp_scritto": zrad, "nodi": int(m44.NodeCount)},
                         {"configurazione": "senza presolve, tagli ed euristiche",
                          "z": m45.ObjVal, "z_lp_scritto": zrad,
                          "nodi": int(m45.NodeCount)}]), "cap04_solver")

# ---------- 5. I DUALI DELL'LP NON SONO I PREZZI MARGINALI DEL MILP ----------
intestazione("4.5  Perche' i duali dell'LP non sono i prezzi marginali del MILP")
righe = []
for C in (8, 9, 10, 11, 12):
    m = nuovo_modello("zaino_C")
    x = m.addVars(4, vtype=GRB.BINARY, name="x")
    m.setObjective(gp.quicksum(p42[j] * x[j] for j in R(4)), GRB.MAXIMIZE)
    con = m.addConstr(gp.quicksum(w42[j] * x[j] for j in R(4)) <= C, name="capacita")
    z = risolvi(m)
    zr, _, pi = rilassamento(m, rafforzato=True)
    righe.append({"capacita": C, "z_milp": z, "z_lp": zr, "duale_lp": pi["capacita"]})
print("   C   z(MILP)   z(LP+)   duale dell'LP   variazione vera di z(MILP)")
for k, r in enumerate(righe):
    delta = "" if k == 0 else frazione(r["z_milp"] - righe[k - 1]["z_milp"])
    print(f"  {r['capacita']:2d}    {frazione(r['z_milp']):>5}   {frazione(r['z_lp']):>6}   "
          f"{r['duale_lp']:>10.4f}      {delta:>6}")
salva_dati(pd.DataFrame(righe), "cap04_prezzi")
print("  Il duale dell'LP e' il rapporto p_j/w_j dell'oggetto 'critico': 2 quando la")
print("  capacita' si esaurisce sull'oggetto 1, 7/4 quando avanza spazio per l'oggetto 2.")
print("  Dice quanto vale una unita' di capacita' in piu' *nel continuo*. Sull'intero la")
print("  variazione vera e' a scatti (1, 0, 3, 3) e non coincide mai con quel valore:")
print("  passando da C = 9 a C = 10 l'ottimo intero non cambia affatto, mentre il duale")
print("  continua a promettere 7/4. Il duale dell'LP non e' il prezzo marginale del")
print("  MILP, e usarlo come tale e' un errore, non un'approssimazione.")

# ---------- 6. FIGURA: IL SANDWICH DEI DUE PROBLEMI ----------
fig, ax = plt.subplots(figsize=(7.2, 3.4))
etichette = ["copertura (min)", "zaino (max)"]
lb = [lb41, lb42]
ub = [ub41_primale, ub42]
zl = [zlp41, zlp42]
zm = [z41, z42]
for i in R(2):
    ax.plot([lb[i], ub[i]], [i, i], color=GRIGIO, lw=2, solid_capstyle="round")
    ax.plot(lb[i], i, "|", color=TEAL, ms=18, mew=2.5)
    ax.plot(ub[i], i, "|", color=ARANCIO, ms=18, mew=2.5)
    ax.plot(zl[i], i, "d", color=BLU, ms=8)
    ax.plot(zm[i], i, "o", color=ROSSO, ms=9)
ax.plot([], [], "|", color=TEAL, ms=12, mew=2.5, label="lower bound")
ax.plot([], [], "|", color=ARANCIO, ms=12, mew=2.5, label="upper bound")
ax.plot([], [], "d", color=BLU, ms=7, label="$z(\\mathrm{LP})$")
ax.plot([], [], "o", color=ROSSO, ms=8, label="$z(\\mathrm{MILP})$")
ax.set_yticks(R(2))
ax.set_yticklabels(etichette)
ax.set_xlabel("valore dell'obiettivo")
ax.set_title("Il sandwich: in un minimo il duale sta a sinistra, in un massimo a destra")
ax.legend(fontsize=8, ncols=4, loc="lower center", bbox_to_anchor=(0.5, -0.42))
ax.set_ylim(-0.6, 1.6)
salva_figura(fig, "cap04_sandwich")
print("Fine.")
