"""Capitolo 3 -- Dal modello a Python/Gurobi: come si scrive e come si legge.

Le quattro classi di variabili, una addConstrs per famiglia di vincoli, e
soprattutto la lettura dei risultati: Status, SolCount, ObjVal, ObjBound,
MIPGap, NodeCount, il limite di tempo, le tolleranze e relax(). Chiude con il
protocollo completo del corso su un'istanza minima.
"""
import gurobipy as gp
import pandas as pd
from gurobipy import GRB

from euristiche import best_fit
from mip import (ammissibile, due_rilassamenti, frazione, nuovo_modello, registra_bound,
                 rilassamento, risolvi, stampa_lp, stampa_soluzione, valuta, viola_interezza)
from esteso import salva_modello
from stile import (ARANCIO, BLU, CICLO, GRIGIO, ROSSO, TEAL, VERDE, intestazione,
                   plt, salva_dati, salva_figura)

R = range

# ---------- 1. LE QUATTRO CLASSI DI VARIABILI ----------
intestazione("1. Le quattro classi di variabili e i loro domini")
m = nuovo_modello("tipi_di_variabile")
b = m.addVar(vtype=GRB.BINARY, name="binaria")
i = m.addVar(vtype=GRB.INTEGER, lb=0, ub=10, name="intera")
c = m.addVar(lb=0.0, ub=GRB.INFINITY, name="continua")
l = m.addVar(lb=-GRB.INFINITY, ub=GRB.INFINITY, name="libera")
m.update()
for v in m.getVars():
    print(f"  {v.VarName:9s} VType = {v.VType}   lb = {v.LB:>6.1f}   ub = "
          f"{'+inf' if v.UB >= GRB.INFINITY else f'{v.UB:.1f}':>6s}")
print("  GRB.BINARY implica gia' lb = 0 e ub = 1: non serve dichiararli.")
print("  Una variabile continua ha lb = 0 per default: le variabili libere vanno")
print("  dichiarate esplicitamente con lb = -GRB.INFINITY (i duali di un'uguaglianza).")

# ---------- 2. UN MODELLO, UNA FAMIGLIA DI VINCOLI ALLA VOLTA ----------
intestazione("2. Il modello si scrive una famiglia di vincoli per blocco")
t = [[2, 1, 3], [3, 4, 2], [4, 5, 3]]
co = [[5, 10, 2], [5, 4, 6], [5, 4, 6]]
a = [5, 6, 7]
n, k = 3, 3


def modello(t, co, a):
    """Un assegnamento: una addConstrs per famiglia, con il nome dell'etichetta."""
    mm = nuovo_modello("assegnamento")
    x = mm.addVars(n, k, vtype=GRB.BINARY, name="x")          # dati -> variabili
    mm.setObjective(gp.quicksum(co[j][h] * x[j, h] for j in R(n) for h in R(k)), GRB.MINIMIZE)
    mm.addConstrs((x.sum(j, "*") == 1 for j in R(n)), name="assegna")
    mm.addConstrs((gp.quicksum(t[j][h] * x[j, h] for j in R(n)) <= a[h] for h in R(k)),
                  name="disponibilita")
    return mm, x


m2, x2 = modello(t, co, a)
m2.update()
print(f"  Variabili: {m2.NumVars}   vincoli: {m2.NumConstrs}   non zeri: {m2.NumNZs}")
print("  Nomi dei vincoli (le stesse etichette del modello matematico):")
print("   " + ", ".join(cc.ConstrName for cc in m2.getConstrs()))
print("  Il modello dell'istanza in formato LP, per controllare i tabulari della dispensa:")
import io
import os
import tempfile
with tempfile.TemporaryDirectory() as d:
    percorso = os.path.join(d, "modello.lp")
    m2.write(percorso)
    testo_lp = open(percorso).read()
for riga in [r for r in testo_lp.splitlines() if r.strip()][:8]:
    print("    " + riga)
print("    ...")

# ---------- 3. LEGGERE I RISULTATI: IL CASO NORMALE ----------
intestazione("3. Leggere i risultati quando tutto va bene")
m2.optimize()
print(f"  Status   = {m2.Status}   (2 = OPTIMAL)")
print(f"  SolCount = {m2.SolCount}   (quante soluzioni intere sono state trovate)")
print(f"  ObjVal   = {frazione(m2.ObjVal)}   ObjBound = {frazione(m2.ObjBound)}   "
      f"MIPGap = {m2.MIPGap:.6f}")
print(f"  NodeCount = {int(m2.NodeCount)}   Runtime = {m2.Runtime:.3f} s")
print("  Soluzione ottima (solo le variabili non nulle):")
stampa_soluzione(m2, solo_non_nulle=True)
z_ott = m2.ObjVal

# ---------- 4. LEGGERE I RISULTATI QUANDO NON VA BENE ----------
intestazione("4. I tre casi in cui ObjVal non si puo' leggere")
# (a) inammissibile
m3, x3 = modello(t, co, [1, 1, 1])          # disponibilita' insufficienti
m3.optimize()
print(f"  (a) disponibilita' (1,1,1): Status = {m3.Status} (3 = INFEASIBLE), "
      f"SolCount = {m3.SolCount}")
print("      ObjVal non esiste: leggerlo solleva un errore. Si legge Status, sempre prima.")
assert m3.Status == GRB.INFEASIBLE
# (b) limite di tempo con nessuna soluzione trovata
m4, x4 = modello(t, co, a)
m4.Params.TimeLimit = 0.0
m4.optimize()
print(f"  (b) TimeLimit = 0: Status = {m4.Status} (9 = TIME_LIMIT), SolCount = {m4.SolCount}")
print(f"      ObjBound = {m4.ObjBound if m4.ObjBound > -GRB.INFINITY else '-inf'}: "
      f"nemmeno il bound e' stato calcolato.")
# (c) limite di tempo con una soluzione trovata: il caso utile
m5, x5 = modello(t, co, a)
m5.Params.SolutionLimit = 1                 # si ferma alla prima soluzione intera
m5.optimize()
print(f"  (c) SolutionLimit = 1: Status = {m5.Status} (10 = SOLUTION_LIMIT), "
      f"SolCount = {m5.SolCount}")
if m5.SolCount > 0:
    print(f"      ObjVal = {frazione(m5.ObjVal)}  ObjBound = {frazione(m5.ObjBound)}  "
          f"MIPGap = {m5.MIPGap:.4f}")
    print("      Questo e' l'unico caso in cui si riporta un intervallo: l'ottimo sta")
    print("      fra ObjBound e ObjVal, e il MIPGap ne misura l'ampiezza.")
salva_dati(pd.DataFrame([
    {"caso": "ottimo", "status": m2.Status, "sol_count": m2.SolCount, "obj_val": m2.ObjVal,
     "obj_bound": m2.ObjBound, "mip_gap": m2.MIPGap},
    {"caso": "inammissibile", "status": m3.Status, "sol_count": m3.SolCount,
     "obj_val": None, "obj_bound": None, "mip_gap": None},
    {"caso": "limite di tempo, nessuna soluzione", "status": m4.Status,
     "sol_count": m4.SolCount, "obj_val": None, "obj_bound": None, "mip_gap": None},
    {"caso": "prima soluzione", "status": m5.Status, "sol_count": m5.SolCount,
     "obj_val": m5.ObjVal if m5.SolCount else None,
     "obj_bound": m5.ObjBound, "mip_gap": m5.MIPGap if m5.SolCount else None},
]), "cap06_stati")

# ---------- 5. TOLLERANZE ----------
intestazione("5. Le tolleranze: 'intero' vuol dire 'intero entro IntFeasTol'")
m6, x6 = modello(t, co, a)
print(f"  IntFeasTol  = {m6.Params.IntFeasTol:g}  (quanto una binaria puo' distare da 0 o 1)")
print(f"  FeasibilityTol = {m6.Params.FeasibilityTol:g}  (violazione ammessa sui vincoli)")
print(f"  OptimalityTol  = {m6.Params.OptimalityTol:g}  (tolleranza sui costi ridotti)")
print(f"  MIPGap (obiettivo) = {m6.Params.MIPGap:g}  (si ferma quando il gap scende sotto)")
m6.optimize()
peggiore = max(min(abs(v.X - round(v.X)), 1) for v in m6.getVars())
print(f"  Sulla soluzione restituita, la distanza massima da un intero e' {peggiore:.2e}")
print("  Nel testo si scrive 1, non 0.9999999997: i valori si arrotondano quando si")
print("  riportano, e i confronti si fanno con una tolleranza (nel corso, 1e-6).")

# ---------- 6. IL RILASSAMENTO CON relax() ----------
intestazione("6. relax(): il rilassamento del modello che abbiamo scritto")
zlp_r, sol_r, pi_r = rilassamento(m6, rafforzato=True)
zlp_p, _, _ = rilassamento(m6, rafforzato=False)
print(f"  z(LP+) = {frazione(zlp_r)}   (relax(): le binarie diventano 0 <= x <= 1)")
print(f"  z(LP)  = {frazione(zlp_p)}   (rilassamento senza i bound: si toglie anche x <= 1)")
print("  Duali del rilassamento letti da Gurobi:")
for nome, valore in pi_r.items():
    if abs(valore) > 1e-9:
        print(f"    {nome}: {valore:.4f}")
print("  relax() copia il modello: le modifiche pendenti vanno applicate prima con")
print("  m.update(), altrimenti si rilassa una versione vecchia.")

# ---------- 7. IL PROTOCOLLO DEL CORSO, DALL'INIZIO ALLA FINE ----------
intestazione("7. Il protocollo: dati -> modello -> euristica -> LP e duale -> MIP -> tabella")
# (1) dati  ->  (2) modello
m7, x7 = modello(t, co, a)
# (3) euristica e sua verifica
e = best_fit(t, a, lambda j, h, ra: co[j][h], "costo")
ub = sum(co[j][h] for (j, h) in e.x)
sol_eur = {f"x[{j},{h}]": 1 for (j, h) in e.x}
assert ammissibile(m7, sol_eur), "la soluzione euristica deve essere ammissibile E intera"
print(f"  (3) euristica best-fit: ub = {frazione(ub)}, ammissibilita' verificata "
      f"(vincoli, bound e interezza)")
# (4) LP e duale scritto a mano
d = nuovo_modello("duale")
mu = d.addVars(n, lb=-GRB.INFINITY, name="mu")
pi = d.addVars(k, lb=-GRB.INFINITY, ub=0.0, name="pi")
d.setObjective(mu.sum() + gp.quicksum(a[h] * pi[h] for h in R(k)), GRB.MAXIMIZE)
d.addConstrs((mu[j] + t[j][h] * pi[h] <= co[j][h] for j in R(n) for h in R(k)), name="rc")
mano = {f"mu[{j}]": min(co[j]) for j in R(n)}
lb, viol = valuta(d, mano)
assert viol <= 1e-9
print(f"  (4) soluzione duale a mano: lb = {frazione(lb)}, ammissibile per il duale")
zlp, zlp_raff, _ = due_rilassamenti(m7, d)
# (5) MIP
z = risolvi(m7)
# (6) tabella
riga = registra_bound("7.1 assegnamento", ub, lb, zlp, zlp_raff, z)
salva_dati(pd.DataFrame([riga]), "cap06_protocollo")
assert lb <= zlp <= z <= ub + 1e-9
print("  (7) la riga della tabella e' quella qui sopra, ed e' salvata in CSV: da li'")
print("      la leggono la dispensa, il sito e verifica_numeri.py.")

# ---------- 8. TRE PROBLEMI CHE IL CORSO RIUSA ----------
# Bin packing, makespan su macchine identiche e commesso viaggiatore: sono i tre
# problemi su cui il capitolo delle euristiche costruisce next-fit, first-fit,
# best-fit, LPT e vicino piu' vicino. Qui si scrivono i modelli, cosi' quel
# capitolo ha qualcosa con cui confrontare le sue soluzioni.
intestazione("8. Bin packing, makespan e TSP: i modelli che le euristiche useranno")

# --- bin packing: quanti contenitori bastano ---
w_bpp = [5, 4, 3, 3]             # peso degli oggetti
c_bpp = 7                        # capacita' di un contenitore
n_bpp = len(w_bpp)
k_bpp = n_bpp                    # al piu' un contenitore per oggetto


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


# con sei contenitori possibili il modello dell'istanza avrebbe 42 colonne: per
# scriverlo per esteso bastano i tre che servono davvero, e il conto sotto lo
# dimostra
m_bpp, x_bpp, y_bpp = modello_bpp(w_bpp, c_bpp, k_bpp)
z_bpp = risolvi(m_bpp)
minimo_teorico = -(-sum(w_bpp) // c_bpp)        # arrotondamento all'insu'
print(f"  Bin packing: pesi {w_bpp}, capacita' {c_bpp}.")
print(f"  Il peso totale e' {sum(w_bpp)}: nessuna soluzione usa meno di "
      f"{sum(w_bpp)}/{c_bpp} = {minimo_teorico} contenitori, e l'ottimo ne usa {int(z_bpp)}.")
m_bpp3, x_bpp3, y_bpp3 = modello_bpp(w_bpp, c_bpp, int(z_bpp))
risolvi(m_bpp3)
salva_modello(m_bpp3, "cap06_bpp")
assert z_bpp == minimo_teorico

# --- P||Cmax: il makespan su macchine identiche ---
d_cmax = [5, 5, 4, 4, 3, 3, 3]   # durate dei lavori
k_cmax = 3                       # macchine identiche


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


m_cmax, x_cmax, z_cmax_var = modello_cmax(d_cmax, k_cmax)
z_cmax = risolvi(m_cmax)
salva_modello(m_cmax, "cap06_cmax")
print(f"  Makespan: durate {d_cmax} su {k_cmax} macchine identiche.")
print(f"  Il carico totale e' {sum(d_cmax)}: diviso per {k_cmax} da' "
      f"{frazione(sum(d_cmax) / k_cmax)}, e l'ottimo vale {frazione(z_cmax)}.")

# --- TSP con la formulazione MTZ ---
D_tsp = [[0, 4, 5, 9],
         [4, 0, 9, 9],
         [5, 9, 0, 4],
         [9, 9, 4, 0]]
n_tsp = len(D_tsp)


def modello_tsp(D):
    """TSP con i vincoli di Miller-Tucker-Zemlin.

    Le variabili u ordinano le citta' lungo il tour: il vincolo
    u_i - u_j + n x_ij <= n - 1 e' vero se x_ij = 0 e obbliga u_j >= u_i + 1 se
    x_ij = 1. I sottocicli che non toccano la citta' 1 sono cosi' esclusi, perche'
    richiederebbero una catena di u sempre crescenti che si richiude su se stessa.
    """
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
print(f"  TSP su {n_tsp} citta': tour ottimo "
      + " -> ".join(str(c + 1) for c in giro + [0])
      + f", lunghezza {frazione(z_tsp)}.")
salva_dati(pd.DataFrame([{"problema": "bin packing", "z_milp": z_bpp},
                         {"problema": "makespan", "z_milp": z_cmax},
                         {"problema": "TSP", "z_milp": z_tsp}]), "cap06_tre_problemi")

# ---------- 8. FIGURA: I QUATTRO NUMERI DEL PROTOCOLLO ----------
fig, ax = plt.subplots(figsize=(7.6, 3.0))
ax.plot([lb, ub], [0, 0], color=GRIGIO, lw=3, solid_capstyle="round")
# z(MILP) e ub cadono sullo stesso punto quando l'euristica e' ottima: il pallino
# piu' grande sta sotto, cosi' si vede che sono due numeri e non uno solo, e le
# etichette si scostano a sinistra e a destra per non sovrapporsi
for valore, colore, testo, dx, dy, ha, ms in [
        (lb, TEAL, "$\\mathrm{lb}$ (duale a mano)", 0, 16, "center", 10),
        (zlp, BLU, "$z(\\mathrm{LP})$", -8, -30, "right", 10),
        (ub, ARANCIO, "$\\mathrm{ub}$ (euristica)", 8, -30, "left", 15),
        (z, ROSSO, "$z(\\mathrm{MILP})$", 0, 16, "center", 9)]:
    ax.plot(valore, 0, "o", color=colore, ms=ms)
    ax.annotate(f"{testo}\n{frazione(valore)}", (valore, 0), textcoords="offset points",
                xytext=(dx, dy), ha=ha, fontsize=9, color=colore)
ax.set_yticks([])
ax.set_ylim(-1.1, 1.0)
ax.set_xlim(lb - 0.7, ub + 0.7)
ax.set_xlabel("valore dell'obiettivo")
ax.set_title("I quattro numeri che ogni esercizio produce")
ax.spines["left"].set_visible(False)
ax.grid(False)
salva_figura(fig, "cap06_protocollo")
print("Fine.")
