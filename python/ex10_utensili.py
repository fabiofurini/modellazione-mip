"""EX 10 -- Utensili CNC: selezione delle operazioni con magazzino limitato (famiglia 8).

Attivazione disaggregata al rovescio: un'operazione si esegue solo se *tutti* i
suoi utensili sono caricati, e il magazzino ne tiene al piu' quattro. E' un
massimo, quindi l'euristica da' il lower bound e il duale l'upper.

La bozza dell'archivio proponeva alpha = 2000 con tutti i moltiplicatori a 900:
quella soluzione duale *non e' ammissibile*, perche' alcuni utensili servono a
piu' di due operazioni. Qui la ricetta duale e' diversa e viene verificata.
"""
import gurobipy as gp
import pandas as pd
from gurobipy import GRB

from mip import (ammissibile, due_rilassamenti, frazione, nuovo_modello, registra_bound,
                 risolvi, valuta)
from stile import intestazione, plt, salva_dati, salva_figura

R = range

# ---------- 1. MODELLO E ISTANZA ----------
intestazione("EX 10. Utensili CNC: quali operazioni eseguire con al piu' quattro utensili")
pr = [2000, 1500, 1800, 1700, 800]            # profitto delle cinque operazioni
T = [[0, 2, 3, 4], [0, 1, 5], [0, 1, 2, 4], [1, 3, 4], [4, 5]]   # utensili richiesti (0-based)
no, nu, K = 5, 6, 4
salva_dati(pd.DataFrame([{"operazione": i + 1,
                          "utensili": ", ".join(str(j + 1) for j in T[i]),
                          "profitto": pr[i]} for i in R(no)]), "ex10_operazioni")


def modello(pr, T, K):
    no, nu = len(pr), max(max(t) for t in T) + 1
    m = nuovo_modello("utensili_cnc")
    x = m.addVars(no, vtype=GRB.BINARY, name="x")
    y = m.addVars(nu, vtype=GRB.BINARY, name="y")
    m.setObjective(gp.quicksum(pr[i] * x[i] for i in R(no)), GRB.MAXIMIZE)
    m.addConstr(y.sum() <= K, name="magazzino")
    for i in R(no):
        for j in T[i]:
            m.addConstr(x[i] - y[j] <= 0, name=f"link[{i},{j}]")
    return m, x, y


def duale(pr, T, K):
    """min K alpha;  sum_{j in T_i} beta_ij >= p_i;  sum_{i : j in T_i} beta_ij <= alpha;
    alpha, beta >= 0."""
    no, nu = len(pr), max(max(t) for t in T) + 1
    d = nuovo_modello("duale_utensili")
    alpha = d.addVar(name="alpha")
    beta = d.addVars([(i, j) for i in R(no) for j in T[i]], name="beta")
    d.setObjective(K * alpha, GRB.MINIMIZE)
    d.addConstrs((gp.quicksum(beta[i, j] for j in T[i]) >= pr[i] for i in R(no)), name="rc_x")
    d.addConstrs((gp.quicksum(beta[i, j] for i in R(no) if j in T[i]) <= alpha for j in R(nu)),
                 name="rc_y")
    return d


m, x, y = modello(pr, T, K)

# ---------- 2. EURISTICA COSTRUTTIVA (LOWER BOUND: E' UN MASSIMO) ----------
# euristica costruttiva: si scandiscono le operazioni per profitto decrescente e si carica il
# corredo di utensili di ciascuna, finche' il magazzino lo permette
carichi, eseguite = set(), []
for i in sorted(R(no), key=lambda i: -pr[i]):
    nuovi = set(T[i]) - carichi
    if len(carichi) + len(nuovi) <= K:
        carichi |= nuovi
        eseguite.append(i)
        print(f"  Operazione {i + 1} (profitto {pr[i]}, utensili "
              + ", ".join(str(j + 1) for j in T[i])
              + f"): ne servono {len(nuovi)} nuovi, il magazzino arriva a {len(carichi)} <= {K}: si esegue")
    else:
        print(f"  Operazione {i + 1} (profitto {pr[i]}): servirebbero {len(nuovi)} utensili nuovi, "
              f"il magazzino arriverebbe a {len(carichi) + len(nuovi)} > {K}: si scarta")
lb = sum(pr[i] for i in eseguite)
sol_eur = {f"x[{i}]": 1 for i in eseguite} | {f"y[{j}]": 1 for j in carichi}
assert ammissibile(m, sol_eur)
print(f"  Soluzione euristica: operazioni " + ", ".join(str(i + 1) for i in sorted(eseguite))
      + " con utensili " + ", ".join(str(j + 1) for j in sorted(carichi))
      + f"   lb = {frazione(lb)}")

# ---------- 3. RILASSAMENTO LP E DUALE (UPPER BOUND) ----------
d = duale(pr, T, K)
# ricetta: si spalma il profitto di ogni operazione in parti uguali sui suoi utensili,
# e alpha e' il carico massimo che un utensile riceve
mano = {f"beta[{i},{j}]": pr[i] / len(T[i]) for i in R(no) for j in T[i]}
carico = {j: sum(mano[f"beta[{i},{j}]"] for i in R(no) if j in T[i]) for j in R(nu)}
mano["alpha"] = max(carico.values())
ub, viol = valuta(d, mano)
assert viol <= 1e-9, viol
print("  Duale a mano: beta_ij = p_i / |T_i| (il profitto spalmato sugli utensili che servono)")
for i in R(no):
    print(f"    operazione {i + 1}: {pr[i]} / {len(T[i])} = "
          f"{frazione(pr[i] / len(T[i]))} su ciascuno dei suoi utensili")
print("  Carico di ciascun utensile: "
      + ", ".join(f"{j + 1}: {frazione(carico[j])}" for j in R(nu)))
utensile_critico = max(carico, key=carico.get)
print(f"  Il massimo e' l'utensile {utensile_critico + 1}, quindi alpha = "
      f"{frazione(mano['alpha'])} e ub = {K} alpha = {frazione(ub)}")
# la ricetta della bozza dell'archivio NON e' ammissibile: si verifica
bozza = {f"beta[{i},{j}]": 900 for i in R(no) for j in T[i]} | {"alpha": 2000}
_, viol_bozza = valuta(d, bozza)
assert viol_bozza > 1e-6
peggiore = max(R(nu), key=lambda j: sum(900 for i in R(no) if j in T[i]))
print(f"  Controllo della ricetta della bozza (alpha = 2000, tutti i beta = 900): NON")
print(f"  ammissibile, violazione massima {frazione(viol_bozza)}. L'utensile "
      f"{peggiore + 1} serve a "
      f"{sum(1 for i in R(no) if peggiore in T[i])} operazioni, quindi riceve "
      f"{sum(900 for i in R(no) if peggiore in T[i])} > 2000.")
zlp, zlpr, pi = due_rilassamenti(m, d)

# ---------- 4. OTTIMO DEL MILP E TABELLA DEI BOUND ----------
z = risolvi(m)
op_ott = [i for i in R(no) if x[i].X > 0.5]
ut_ott = [j for j in R(nu) if y[j].X > 0.5]
print(f"  Soluzione ottima: operazioni " + ", ".join(str(i + 1) for i in op_ott)
      + " con utensili " + ", ".join(str(j + 1) for j in ut_ott)
      + f"   z(MILP) = {frazione(z)}")
riga = registra_bound("EX 10 utensili CNC", ub, lb, zlp, zlpr, z, senso="max")
salva_dati(pd.DataFrame([riga]), "ex10_bound")
assert lb <= z <= zlp + 1e-9 <= ub + 1e-9
print(f"  Il sandwich: {frazione(lb)} <= z(MILP) = {frazione(z)} <= z(LP) = {frazione(zlp)} "
      f"<= ub = {frazione(ub)}")
print("  Qui il rilassamento e' molto debole: nel continuo si puo' caricare 'un po'' di")
print("  ogni utensile ed eseguire frazioni di tutte le operazioni.")

# ---------- 5. FIGURA ----------
fig, ax = plt.subplots(figsize=(7.0, 3.2))
for i in R(no):
    for j in R(nu):
        serve = j in T[i]
        colore = ("#0E7490" if i in op_ott else "#F4F6F7") if serve else "white"
        ax.add_patch(plt.Rectangle((j - 0.45, i - 0.4), 0.9, 0.8, facecolor=colore,
                                   edgecolor="#7F8C8D" if serve else "#E5E8E8", lw=0.8))
for j in ut_ott:
    ax.annotate("caricato", (j, no - 0.35), ha="center", va="bottom", fontsize=7.5,
                color="#C0392B", rotation=0)
ax.set_xlim(-0.6, nu - 0.4)
ax.set_ylim(-0.6, no + 0.1)
ax.set_xticks(R(nu))
ax.set_xticklabels([f"ut. {j + 1}" for j in R(nu)], fontsize=8)
ax.set_yticks(R(no))
ax.set_yticklabels([f"op. {i + 1} ({pr[i]})" for i in R(no)], fontsize=8)
ax.set_title(f"EX 10: le operazioni eseguite (in teal) e i {K} utensili caricati "
             f"(z = {frazione(z)})")
ax.invert_yaxis()
ax.grid(False)
salva_figura(fig, "ex10_ottimo")
print("Fine.")
