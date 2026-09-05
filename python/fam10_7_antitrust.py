"""Problema 11.2 -- Suddivisione antitrust: due societa' il piu' simili possibile.

Le filiali vanno divise in due gruppi minimizzando, sul prodotto peggiore, la
differenza di fatturato fra i due gruppi. E' la tecnica 3.6 (min-max) applicata
a un valore assoluto (3.7): due disuguaglianze per prodotto attorno alla stessa
variabile z.

Il punto del problema e' che il rilassamento lineare vale zero: meta' filiale a
ciascuna societa' pareggia tutti i prodotti. Il bound inferiore utile non viene
dal duale ma da un argomento combinatorio, prodotto per prodotto.
"""
import itertools

import gurobipy as gp
import pandas as pd
from gurobipy import GRB

from mip import (ammissibile, due_rilassamenti, frazione, nuovo_modello, registra_bound,
                 risolvi, valuta)
from stile import ARANCIO, BLU, TEAL, intestazione, plt, salva_dati, salva_figura

R = range

# ---------- 1. MODELLO E ISTANZA ----------
intestazione("11.2 Antitrust: dividere le filiali minimizzando lo squilibrio peggiore")
v2 = [[3, 3, 2],      # fatturato della filiale i sul prodotto j (milioni)
      [6, 8, 5],
      [3, 4, 4],
      [2, 7, 9]]
s2, r2 = len(v2), len(v2[0])
salva_dati(pd.DataFrame(v2, columns=[f"prodotto_{j + 1}" for j in R(r2)],
                        index=[f"filiale_{i + 1}" for i in R(s2)]).reset_index(),
           "antitrust2_dati")


def modello_2(v):
    """Una sola famiglia di binarie: x_i = 1 se la filiale i va alla societa' A.

    La sorgente usa due famiglie x_i e y_i con x_i + y_i = 1. Sono equivalenti:
    y_i = 1 - x_i. Qui si tiene la forma aggregata, piu' compatta; la forma
    disaggregata si ottiene sostituendo, ed e' quella che serve quando le societa'
    diventano piu' di due.
    """
    s, r = len(v), len(v[0])
    m = nuovo_modello("antitrust")
    x = m.addVars(s, vtype=GRB.BINARY, name="x")
    z = m.addVar(lb=-GRB.INFINITY, name="z")
    m.setObjective(z, GRB.MINIMIZE)
    for j in R(r):
        tot = sum(v[i][j] for i in R(s))
        # differenza fra A e B sul prodotto j: 2 * sum_i v_ij x_i - tot
        m.addConstr(z - 2 * gp.quicksum(v[i][j] * x[i] for i in R(s)) + tot >= 0,
                    name=f"sopra[{j}]")
        m.addConstr(z + 2 * gp.quicksum(v[i][j] * x[i] for i in R(s)) - tot >= 0,
                    name=f"sotto[{j}]")
    return m, x, z


def duale_2(v):
    """max sum_j T_j (mu_j - lam_j)  con  sum_j (lam_j + mu_j) = 1  (colonna di z, libera)
       e  2 sum_j v_ij (mu_j - lam_j) <= 0 per ogni filiale i (colonna di x_i >= 0)."""
    s, r = len(v), len(v[0])
    dl = nuovo_modello("duale_antitrust")
    lam = dl.addVars(r, name="lam")     # vincoli "sopra"
    mu = dl.addVars(r, name="mu")       # vincoli "sotto"
    tot = [sum(v[i][j] for i in R(s)) for j in R(r)]
    dl.setObjective(gp.quicksum(tot[j] * (mu[j] - lam[j]) for j in R(r)), GRB.MAXIMIZE)
    dl.addConstr(gp.quicksum(lam[j] + mu[j] for j in R(r)) == 1, name="rcz")
    dl.addConstrs((2 * gp.quicksum(v[i][j] * (mu[j] - lam[j]) for j in R(r)) <= 0
                   for i in R(s)), name="rcx")
    return dl


m2, x2, z2v = modello_2(v2)
tot2 = [sum(v2[i][j] for i in R(s2)) for j in R(r2)]
print("  Fatturato totale per prodotto: "
      + ", ".join(f"prodotto {j + 1} = {tot2[j]}" for j in R(r2)))

# ---------- 2. EURISTICA COSTRUTTIVA (UPPER BOUND) ----------
# euristica costruttiva: le filiali in ordine di fatturato complessivo decrescente, ciascuna
# alla societa' che al momento fattura meno in totale
def euristica(v):
    s, r = len(v), len(v[0])
    tot_i = [sum(v[i]) for i in R(s)]
    gruppo = {}
    somme = [0, 0]
    passi = [f"fatturato complessivo delle filiali: "
             + ", ".join(f"{i + 1} -> {tot_i[i]}" for i in R(s))]
    for i in sorted(R(s), key=lambda i: (-tot_i[i], i)):
        k = 0 if somme[0] <= somme[1] else 1
        gruppo[i] = k
        somme[k] += tot_i[i]
        passi.append(f"filiale {i + 1} ({tot_i[i]}) alla societa' "
                     f"{'AB'[k]}; ora A = {somme[0]}, B = {somme[1]}")
    diff = [abs(sum(v[i][j] for i in R(s) if gruppo[i] == 0)
                - sum(v[i][j] for i in R(s) if gruppo[i] == 1)) for j in R(r)]
    passi.append("differenze per prodotto: "
                 + ", ".join(f"prodotto {j + 1} -> {diff[j]}" for j in R(r)))
    return gruppo, max(diff), passi


gruppo, ub2, passi = euristica(v2)
for k, riga in enumerate(passi, 1):
    print(f"  Passo {k}. {riga}")
sol_eur = {f"x[{i}]": 1 - gruppo[i] for i in R(s2)} | {"z": ub2}
assert ammissibile(m2, sol_eur), sol_eur
print("  Societa' A = " + str([i + 1 for i in R(s2) if gruppo[i] == 0])
      + ", societa' B = " + str([i + 1 for i in R(s2) if gruppo[i] == 1])
      + f"   ub = {frazione(ub2)}")

# ---------- 3. IL RILASSAMENTO LP NON DICE NIENTE ----------
dl2 = duale_2(v2)
mano = {"lam[0]": 0.5, "mu[0]": 0.5}      # lam_1 = mu_1 = 1/2, tutto il resto zero
lb_lp, viol = valuta(dl2, mano)
assert viol <= 1e-9, viol
print(f"  Duale a mano: lam_1 = mu_1 = 1/2 e tutto il resto zero -> valore {frazione(lb_lp)}.")
print("  Qualunque soluzione duale ammissibile qui vale al piu' zero: nell'obiettivo compare")
print("  la differenza mu_j - lam_j, e i vincoli sulle colonne x_i la costringono a essere")
print("  non positiva su ogni filiale.")
zlp2, zlp2r, _ = due_rilassamenti(m2, dl2)
meta = {f"x[{i}]": 0.5 for i in R(s2)} | {"z": 0.0}
val_meta, viol_meta = valuta(m2, meta)
assert viol_meta <= 1e-9 and abs(val_meta) <= 1e-9
print(f"  Infatti z(LP) = {frazione(zlp2)}: basta mettere meta' di ogni filiale in ciascuna")
print("  societa' (x_i = 1/2, z = 0) e ogni prodotto e' pareggiato esattamente. E' ammissibile")
print("  per il rilassamento e inutile per il problema vero: le filiali sono indivisibili.")
assert abs(zlp2) <= 1e-9

# ---------- 4. UN BOUND COMBINATORIO PRODOTTO PER PRODOTTO ----------
intestazione("11.2 Il bound inferiore viene da un argomento combinatorio")
# per ogni prodotto, il minimo squilibrio ottenibile guardando quel solo prodotto
def minimo_squilibrio(colonna, tot):
    s = len(colonna)
    return min(abs(2 * sum(colonna[i] for i in sotto) - tot)
               for k in R(s + 1) for sotto in itertools.combinations(R(s), k))


gj = [minimo_squilibrio([v2[i][j] for i in R(s2)], tot2[j]) for j in R(r2)]
for j in R(r2):
    print(f"  Prodotto {j + 1}: totale {tot2[j]}, migliore squilibrio possibile guardando solo")
    print(f"    questo prodotto = {gj[j]}")
lb2 = max(gj)
print(f"  Ogni partizione deve rispettare tutti i prodotti insieme, quindi z >= max_j g_j = "
      f"{frazione(lb2)}.")
print("  E' un bound valido che il rilassamento lineare non vede: nasce dall'interezza, non")
print("  dai vincoli.")
salva_dati(pd.DataFrame({"prodotto": R(1, r2 + 1), "totale": tot2, "g_j": gj}),
           "antitrust2_argomento")

# ---------- 5. OTTIMO DEL MILP ----------
z2 = risolvi(m2)
A = [i + 1 for i in R(s2) if x2[i].X > 0.5]
B = [i + 1 for i in R(s2) if x2[i].X <= 0.5]
diff_ott = [abs(sum(v2[i - 1][j] for i in A) - sum(v2[i - 1][j] for i in B)) for j in R(r2)]
print(f"  Soluzione ottima: societa' A = {A}, societa' B = {B}")
print("  differenze per prodotto: "
      + ", ".join(f"prodotto {j + 1} -> {diff_ott[j]}" for j in R(r2))
      + f"   z = {frazione(z2)}")
riga = registra_bound("2 antitrust", ub2, lb2, zlp2, zlp2r, z2)
salva_dati(pd.DataFrame([riga]), "antitrust2_bound")
assert lb2 <= z2 <= ub2 + 1e-9
print(f"  Sandwich: {frazione(lb2)} <= z(MILP) = {frazione(z2)} <= {frazione(ub2)}. Attenzione:")
print(f"  qui lb non e' il valore del duale ({frazione(lb_lp)}) ma il bound combinatorio.")

# ---------- 6. DOMANDE DI MODELLAZIONE AGGIUNTIVE ----------
varianti = {}


def variante(nome, m):
    z = risolvi(m)
    print(f"  {nome:70s} z = {frazione(z)}")
    return z


# 2a: le filiali 1 e 2 devono restare nella stessa societa'
m, x, zz = modello_2(v2)
m.addConstr(x[0] - x[1] == 0, name="insieme")
varianti["2a"] = variante("2a. Le filiali 1 e 2 devono restare insieme (x1 = x2)", m)
# 2b: si minimizza la somma delle differenze invece della peggiore
m = nuovo_modello("antitrust_somma")
x = m.addVars(s2, vtype=GRB.BINARY, name="x")
zj = m.addVars(r2, name="z")
m.setObjective(zj.sum(), GRB.MINIMIZE)
for j in R(r2):
    m.addConstr(zj[j] - 2 * gp.quicksum(v2[i][j] * x[i] for i in R(s2)) + tot2[j] >= 0,
                name=f"sopra[{j}]")
    m.addConstr(zj[j] + 2 * gp.quicksum(v2[i][j] * x[i] for i in R(s2)) - tot2[j] >= 0,
                name=f"sotto[{j}]")
varianti["2b"] = variante("2b. Si minimizza la somma delle differenze (min-sum invece di min-max)", m)
A_somma = sorted(min(([i + 1 for i in R(s2) if x[i].X > 0.5],
                      [i + 1 for i in R(s2) if x[i].X <= 0.5])))
A_max = sorted(min((A, B)))
print(f"       partizione min-sum: {A_somma} contro il resto; partizione min-max: {A_max}.")
print("       I due obiettivi non sono confrontabili in valore: cambia la funzione, non")
print("       l'insieme ammissibile.")
assert A_somma == A_max, (A_somma, A_max)
salva_dati(pd.DataFrame({"variante": list(varianti), "z": list(varianti.values())}),
           "antitrust2_varianti")

# ---------- 7. FIGURA ----------
fig, ax = plt.subplots(figsize=(6.8, 3.0))
larg = 0.35
idx = list(R(r2))
ax.bar([j - larg / 2 for j in idx], [sum(v2[i - 1][j] for i in A) for j in idx], larg,
       color=TEAL, label="societa' A")
ax.bar([j + larg / 2 for j in idx], [sum(v2[i - 1][j] for i in B) for j in idx], larg,
       color=BLU, label="societa' B")
for j in idx:
    ax.annotate(f"|diff| = {diff_ott[j]}", (j, max(tot2) / 2 + 1), ha="center", fontsize=8,
                color=ARANCIO)
ax.set_xticks(idx)
ax.set_xticklabels([f"prodotto {j + 1}" for j in idx])
ax.set_ylabel("fatturato (milioni)")
ax.set_title(f"11.2: partizione ottima, squilibrio peggiore {frazione(z2)}")
ax.legend(fontsize=8)
salva_figura(fig, "cap10_antitrust_ottimo")
print("Fine.")
