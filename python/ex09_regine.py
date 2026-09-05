"""EX 9 -- Otto regine sulla scacchiera (famiglia 11).

Set packing su quattro famiglie di rette: righe, colonne e le due diagonali. Il
duale del rilassamento si costruisce a mano in una riga sola (si paga 1 ogni
riga) e vale esattamente quanto l'ottimo: e' un caso in cui il certificato chiude
il problema. L'euristica euristica costruttiva invece si blocca a meno di otto regine.
"""
import gurobipy as gp
import pandas as pd
from gurobipy import GRB

from mip import (ammissibile, due_rilassamenti, frazione, nuovo_modello, registra_bound,
                 risolvi, valuta)
from stile import ARANCIO, BLU, GRIGIO, TEAL, intestazione, plt, salva_dati, salva_figura

R = range

# ---------- 1. MODELLO E ISTANZA ----------
intestazione("EX 9. Otto regine: il massimo numero di regine che non si attaccano")
N = 8
DIAG1 = R(-(N - 1), N)          # i - j costante
DIAG2 = R(2, 2 * N + 1)         # i + j costante (indici da 1)


def modello(n):
    m = nuovo_modello("regine")
    x = m.addVars(n, n, vtype=GRB.BINARY, name="x")
    m.setObjective(x.sum(), GRB.MAXIMIZE)
    m.addConstrs((x.sum(i, "*") <= 1 for i in R(n)), name="riga")
    m.addConstrs((x.sum("*", j) <= 1 for j in R(n)), name="colonna")
    m.addConstrs((gp.quicksum(x[i, j] for i in R(n) for j in R(n) if i - j == k) <= 1
                  for k in R(-(n - 1), n)), name="diag1")
    m.addConstrs((gp.quicksum(x[i, j] for i in R(n) for j in R(n) if i + j == k) <= 1
                  for k in R(0, 2 * n - 1)), name="diag2")
    return m, x


def duale(n):
    """min sum_i alpha_i + sum_j beta_j + sum_k gamma_k + sum_k delta_k
       s.t. alpha_i + beta_j + gamma_{i-j} + delta_{i+j} >= 1 per ogni casella."""
    d = nuovo_modello("duale_regine")
    alpha = d.addVars(n, name="alpha")
    beta = d.addVars(n, name="beta")
    gamma = d.addVars(R(-(n - 1), n), name="gamma")
    delta = d.addVars(R(0, 2 * n - 1), name="delta")
    d.setObjective(alpha.sum() + beta.sum() + gamma.sum() + delta.sum(), GRB.MINIMIZE)
    d.addConstrs((alpha[i] + beta[j] + gamma[i - j] + delta[i + j] >= 1
                  for i in R(n) for j in R(n)), name="rc")
    return d


m8, x8 = modello(N)
print(f"  Scacchiera {N}x{N}: {N * N} variabili binarie e {2 * N + (2 * N - 1) * 2} vincoli")
print("  (una riga, una colonna e due diagonali per ogni retta della scacchiera).")

# ---------- 2. EURISTICA COSTRUTTIVA (LOWER BOUND) ----------
# euristica costruttiva riga per riga: la prima colonna libera che non e' attaccata dalle regine
# gia' piazzate. Non torna mai indietro: se una riga non ha caselle libere, la salta.
def euristica(n):
    pos = []
    passi = []
    for i in R(n):
        scelta = None
        for j in R(n):
            if all(j != jj and abs(i - ii) != abs(j - jj) for ii, jj in pos):
                scelta = j
                break
        if scelta is None:
            passi.append(f"riga {i + 1}: nessuna casella libera, la riga resta vuota")
        else:
            pos.append((i, scelta))
            passi.append(f"riga {i + 1}: prima casella libera in colonna {scelta + 1}")
    return pos, passi


pos, passi = euristica(N)
for k, riga in enumerate(passi, 1):
    print(f"  Passo {k}. {riga}")
lb8 = len(pos)
sol_eur = {f"x[{i},{j}]": 1 for i, j in pos}
assert ammissibile(m8, sol_eur), sol_eur
print(f"  Regine piazzate dall'euristica costruttiva: {lb8}  ->  lb = {frazione(lb8)}")

# ---------- 3. RILASSAMENTO LP E DUALE (UPPER BOUND) ----------
d8 = duale(N)
mano = {f"alpha[{i}]": 1.0 for i in R(N)}       # beta = gamma = delta = 0
ub8, viol = valuta(d8, mano)
assert viol <= 1e-9, viol
print(f"  Duale a mano: alpha_i = 1 su ogni riga, tutto il resto zero. Ogni casella (i, j) ha")
print(f"  alpha_i = 1 >= 1: la soluzione e' ammissibile e vale {frazione(ub8)}.")
print("  E' la traduzione duale della frase «in ogni riga sta al piu' una regina».")
zlp8, zlp8r, _ = due_rilassamenti(m8, d8)

# ---------- 4. OTTIMO DEL MILP ----------
z8 = risolvi(m8)
ott = [(i, j) for i in R(N) for j in R(N) if x8[i, j].X > 0.5]
print("  Soluzione ottima (una regina per riga): "
      + ", ".join(f"riga {i + 1} colonna {j + 1}" for i, j in sorted(ott)))
riga = registra_bound("EX 9 regine", ub8, lb8, zlp8, zlp8r, z8, senso="max")
salva_dati(pd.DataFrame([riga]), "ex09_bound")
salva_dati(pd.DataFrame([{"riga": i + 1, "colonna": j + 1} for i, j in sorted(ott)]),
           "ex09_ottimo")
assert lb8 <= z8 <= zlp8 <= ub8 + 1e-9
print(f"  Il bound duale {frazione(ub8)} e' raggiunto: la soluzione trovata e' ottima, e lo")
print("  sappiamo senza fidarci del solver. L'euristica costruttiva invece si ferma prima: e' l'euristica,")
print("  non il bound, a lasciare il divario.")

# ---------- 5. DUE VARIANTI ----------
intestazione("EX 9. Varianti")
varianti = {}
# 8a: scacchiere piu' piccole; per n = 2 e n = 3 non si arriva a n regine
for n in (4, 5, 6):
    m, x = modello(n)
    z = risolvi(m)
    varianti[f"n = {n}"] = z
    print(f"  Scacchiera {n}x{n}: z = {frazione(z)} (= n)")
    assert abs(z - n) <= 1e-9
for n in (2, 3):
    m, x = modello(n)
    z = risolvi(m)
    varianti[f"n = {n}"] = z
    print(f"  Scacchiera {n}x{n}: z = {frazione(z)} < {n}: il bound duale n non e' raggiungibile")
    assert z < n - 0.5
salva_dati(pd.DataFrame({"scacchiera": list(varianti), "z": list(varianti.values())}),
           "ex09_varianti")
# 8b: le diagonali non contano (torri invece di regine)
m, x = modello(N)
m.update()
for c in [c for c in m.getConstrs() if c.ConstrName.startswith("diag")]:
    m.remove(c)
m.update()
z_torri = risolvi(m)
print(f"  Senza i vincoli sulle diagonali (torri invece di regine): z = {frazione(z_torri)},")
print("  e il modello diventa un assegnamento: la matrice e' totalmente unimodulare e il")
print("  rilassamento lineare da' gia' un valore intero.")

# ---------- 6. FIGURA ----------
fig, ax = plt.subplots(figsize=(4.4, 4.4))
for i in R(N):
    for j in R(N):
        ax.add_patch(plt.Rectangle((j, N - 1 - i), 1, 1,
                                   color="#EFEFEF" if (i + j) % 2 else "#CFD8DC"))
for i, j in pos:
    ax.plot(j + 0.5, N - 1 - i + 0.5, marker="s", color=ARANCIO, ms=13)
for i, j in ott:
    ax.plot(j + 0.5, N - 1 - i + 0.5, marker="*", color=TEAL, ms=17)
ax.plot([], [], marker="s", ls="", color=ARANCIO, label=f"euristica costruttiva ({lb8})")
ax.plot([], [], marker="*", ls="", color=TEAL, label=f"ottimo ({int(z8)})")
ax.set_xlim(0, N)
ax.set_ylim(0, N)
ax.set_xticks([j + 0.5 for j in R(N)])
ax.set_xticklabels([str(j + 1) for j in R(N)])
ax.set_yticks([i + 0.5 for i in R(N)])
ax.set_yticklabels([str(N - i) for i in R(N)])
ax.set_aspect("equal")
ax.set_title("EX 9: euristica costruttiva contro ottimo")
ax.legend(fontsize=8, loc="upper center", bbox_to_anchor=(0.5, -0.06), ncol=2)
salva_figura(fig, "ex09_scacchiera")
print("Fine.")
