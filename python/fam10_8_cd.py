"""Problema 11.3 -- Brani su piu' CD: minimizzare la differenza fra il piu' lungo
e il piu' corto.

Due variabili ausiliarie: y di massimo (tecnica 3.5) e z di minimo, con obiettivo
y - z. Come in 11.2 il rilassamento lineare vale zero, e il bound inferiore utile
si ottiene da un argomento di parita' che decide da solo l'ottimalita'.
"""
import gurobipy as gp
import pandas as pd
from gurobipy import GRB

from mip import (ammissibile, due_rilassamenti, frazione, nuovo_modello, registra_bound,
                 risolvi, valuta)
from stile import ARANCIO, BLU, TEAL, intestazione, plt, salva_dati, salva_figura

R = range

# ---------- 1. MODELLO E ISTANZA ----------
intestazione("11.3 Brani sui CD: pareggiare la durata del CD piu' lungo e del piu' corto")
d3 = [5, 6, 7, 3, 4, 10]     # durata dei brani, in minuti
w3 = [1, 1]                  # brani minimi per CD
n3, m3 = len(d3), len(w3)
D3 = sum(d3)
salva_dati(pd.DataFrame({"brano": R(1, n3 + 1), "durata": d3}), "cd3_dati")
print(f"  Durata totale della raccolta: {D3} minuti su {m3} CD.")


def modello_3(d, w):
    n, m = len(d), len(w)
    mod = nuovo_modello("cd")
    x = mod.addVars(n, m, vtype=GRB.BINARY, name="x")
    y = mod.addVar(name="y")     # durata del CD piu' lungo
    z = mod.addVar(name="z")     # durata del CD piu' corto
    mod.setObjective(y - z, GRB.MINIMIZE)
    mod.addConstrs((x.sum(i, "*") == 1 for i in R(n)), name="brano")
    mod.addConstrs((x.sum("*", j) >= w[j] for j in R(m)), name="minimo")
    mod.addConstrs((y - gp.quicksum(d[i] * x[i, j] for i in R(n)) >= 0 for j in R(m)),
                   name="massimo")
    mod.addConstrs((gp.quicksum(d[i] * x[i, j] for i in R(n)) - z >= 0 for j in R(m)),
                   name="minimo_durata")
    return mod, x, y, z


def duale_3(d, w):
    """max sum_i alpha_i + sum_j w_j beta_j

    alpha_i libera (vincolo di uguaglianza), beta_j >= 0 (>= w_j), gamma_j >= 0
    (colonna di y: sum_j gamma_j = 1) e delta_j >= 0 (colonna di z:
    sum_j delta_j = 1). Colonna di x_ij: alpha_i + beta_j - d_i gamma_j + d_i delta_j <= 0.
    """
    n, m = len(d), len(w)
    dl = nuovo_modello("duale_cd")
    alpha = dl.addVars(n, lb=-GRB.INFINITY, name="alpha")
    beta = dl.addVars(m, name="beta")
    gamma = dl.addVars(m, name="gamma")
    delta = dl.addVars(m, name="delta")
    dl.setObjective(alpha.sum() + gp.quicksum(w[j] * beta[j] for j in R(m)), GRB.MAXIMIZE)
    dl.addConstr(gamma.sum() == 1, name="rcy")
    dl.addConstr(delta.sum() == 1, name="rcz")
    dl.addConstrs((alpha[i] + beta[j] - d[i] * gamma[j] + d[i] * delta[j] <= 0
                   for i in R(n) for j in R(m)), name="rcx")
    return dl


m3mod, x3, y3, z3v = modello_3(d3, w3)

# ---------- 2. DUE EURISTICHE A CONFRONTO (UPPER BOUND) ----------
def riempi(d, m, ordine, etichetta):
    """Si scorrono i brani nell'ordine dato e si mette ognuno sul CD piu' corto."""
    carichi = [0] * m
    dove = {}
    passi = []
    for i in ordine:
        j = min(R(m), key=lambda j: (carichi[j], j))
        dove[i] = j
        carichi[j] += d[i]
        passi.append(f"brano {i + 1} ({d[i]} min) sul CD {j + 1}; durate {carichi}")
    diff = max(carichi) - min(carichi)
    print(f"  {etichetta}")
    for k, riga in enumerate(passi, 1):
        print(f"    Passo {k}. {riga}")
    print(f"    durate finali {carichi}, differenza {diff}")
    return dove, carichi, diff


ordine_lpt = sorted(R(n3), key=lambda i: (-d3[i], i))
dove, carichi, ub3 = riempi(d3, m3, ordine_lpt,
                            "Euristica LPT: brani in ordine di durata decrescente.")
dove_nat, carichi_nat, diff_nat = riempi(d3, m3, list(R(n3)),
                                         "Euristica ingenua: brani nell'ordine dato.")
sol_eur = ({f"x[{i},{dove[i]}]": 1 for i in R(n3)}
           | {"y": max(carichi), "z": min(carichi)})
assert ammissibile(m3mod, sol_eur), sol_eur
print(f"  L'ordine decrescente da' {frazione(ub3)}, l'ordine naturale {frazione(diff_nat)}: la")
print("  stessa regola di inserimento cambia di molto a seconda dell'ordine dei brani.")
print(f"  Si tiene il migliore dei due:  ub = {frazione(ub3)}")
assert diff_nat >= ub3

# ---------- 3. IL RILASSAMENTO LP NON DICE NIENTE ----------
dl3 = duale_3(d3, w3)
mano = {f"gamma[{j}]": 1 / m3 for j in R(m3)} | {f"delta[{j}]": 1 / m3 for j in R(m3)}
lb_lp, viol = valuta(dl3, mano)
assert viol <= 1e-9, viol
print(f"  Duale a mano: gamma_j = delta_j = 1/{m3}, alpha = beta = 0 -> valore "
      f"{frazione(lb_lp)}.")
zlp3, zlp3r, _ = due_rilassamenti(m3mod, dl3)
meta = ({f"x[{i},{j}]": 1 / m3 for i in R(n3) for j in R(m3)}
        | {"y": D3 / m3, "z": D3 / m3})
val_meta, viol_meta = valuta(m3mod, meta)
assert viol_meta <= 1e-9 and abs(val_meta) <= 1e-9
print(f"  E infatti z(LP) = {frazione(zlp3)}: mettendo 1/{m3} di ogni brano su ogni CD tutti i")
print(f"  CD durano {frazione(D3 / m3)} minuti e la differenza e' nulla. Un brano pero' non si")
print("  spezza.")
assert abs(zlp3) <= 1e-9

# ---------- 4. IL BOUND DI PARITA' ----------
intestazione("11.3 Un argomento di parita' che chiude il problema")
print(f"  Le durate sono numeri interi e i CD sono {m3}: le due durate sommano a {D3}, che e'")
print(f"  {'dispari' if D3 % 2 else 'pari'}. Due interi che sommano a un numero dispari non")
print("  possono essere uguali, e la loro differenza e' essa stessa dispari: quindi vale")
print("  almeno 1.")
lb3 = 1 if D3 % 2 else 0
assert m3 == 2, "l'argomento di parita' vale cosi' com'e' per due soli CD"
print(f"  lb = {frazione(lb3)}, e l'euristica LPT raggiunge {frazione(ub3)}: i due bound")
print("  coincidono e la soluzione euristica e' gia' ottima, senza bisogno del solver.")
salva_dati(pd.DataFrame([{"argomento": "parita' della durata totale", "bound": lb3},
                         {"argomento": "duale del rilassamento LP", "bound": lb_lp}]),
           "cd3_argomento")

# ---------- 5. OTTIMO DEL MILP ----------
z3 = risolvi(m3mod)
carichi_ott = [sum(d3[i] * x3[i, j].X for i in R(n3)) for j in R(m3)]
for j in R(m3):
    brani = [i + 1 for i in R(n3) if x3[i, j].X > 0.5]
    print(f"  CD {j + 1}: brani {brani}, durata {frazione(carichi_ott[j])} minuti")
riga = registra_bound("3 cd", ub3, lb3, zlp3, zlp3r, z3)
salva_dati(pd.DataFrame([riga]), "cd3_bound")
assert lb3 <= z3 <= ub3 + 1e-9 and abs(z3 - lb3) <= 1e-9

# ---------- 6. DOMANDE DI MODELLAZIONE AGGIUNTIVE ----------
varianti = {}


def variante(nome, m):
    z = risolvi(m)
    print(f"  {nome:70s} z = {frazione(z)}")
    return z


# 3a: il CD 1 e' un supporto piu' piccolo e non supera i 15 minuti
m, x, y, z = modello_3(d3, w3)
m.addConstr(gp.quicksum(d3[i] * x[i, 0] for i in R(n3)) <= 15, name="capacita_cd1")
varianti["3a"] = variante("3a. Il CD 1 non puo' superare i 15 minuti", m)
print(f"       il CD 2 deve allora contenere almeno {D3} - 15 = {D3 - 15} minuti e la")
print(f"       differenza non puo' scendere sotto {D3 - 2 * 15}: il bound si legge dai dati.")
# 3b: tre CD invece di due
m, x, y, z = modello_3(d3, [1, 1, 1])
varianti["3b"] = variante("3b. La raccolta si distribuisce su tre CD", m)
print(f"       con tre CD la durata totale {D3} non e' piu' divisibile in parti uguali:")
print("       l'argomento di parita' va rifatto e non basta piu' a dimostrare l'ottimalita'.")
salva_dati(pd.DataFrame({"variante": list(varianti), "z": list(varianti.values())}),
           "cd3_varianti")

# ---------- 7. FIGURA ----------
fig, ax = plt.subplots(figsize=(6.8, 2.9))
for k, (nome, car, colore) in enumerate([("euristica ingenua", carichi_nat, ARANCIO),
                                         ("euristica LPT", carichi, TEAL),
                                         ("ottimo", carichi_ott, BLU)]):
    for j in R(m3):
        ax.barh(k + (j - 0.5) * 0.34, car[j], 0.3, color=colore)
        ax.annotate(f"CD {j + 1}: {frazione(car[j])}", (0.6, k + (j - 0.5) * 0.34),
                    va="center", fontsize=8, color="white")
    ax.annotate(f"differenza {frazione(max(car) - min(car))}", (max(car) + 0.6, k),
                va="center", fontsize=8)
ax.set_yticks(R(3))
ax.set_yticklabels(["ingenua", "LPT", "ottimo"])
ax.set_xlim(0, max(carichi_nat) + 9)
ax.set_xlabel("durata del CD (minuti)")
ax.set_title(f"11.3: la differenza scende da {frazione(diff_nat)} a {frazione(z3)}")
ax.invert_yaxis()
salva_figura(fig, "cap10_cd_ottimo")
print("Fine.")
