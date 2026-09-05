"""EX 11 -- Bilanciamento fra due operai (famiglia 7, rimando alla 11).

Quattro lavori indivisibili di durata 2, 3, 6, 7 e due operai: si vogliono
carichi il piu' possibile bilanciati.

Due avvertenze che la bozza dell'archivio confondeva:
1. «carichi bilanciati» si puo' scrivere come min-max oppure come min della
   differenza: le soluzioni ottime sono le stesse (il totale e' costante) ma i
   *valori* dell'obiettivo non coincidono. Qui si riportano entrambi.
2. il duale va scritto con i segni della tabella di conversione: in un minimo
   con vincoli <= le variabili duali sono <= 0. La presentazione con variabili
   >= 0 e' la stessa, a segni cambiati, e si mostra anche quella.
"""
import gurobipy as gp
import pandas as pd
from gurobipy import GRB

from mip import (ammissibile, due_rilassamenti, frazione, nuovo_modello, registra_bound,
                 risolvi, valuta)
from stile import intestazione, plt, salva_dati, salva_figura

R = range

# ---------- 1. MODELLO E ISTANZA ----------
intestazione("EX 11. Bilanciamento: quattro lavori indivisibili su due operai")
d = [2, 3, 6, 7]
n, D = len(d), sum(d)
print(f"  Durate {d}; totale {D}; a carichi perfettamente pari ciascuno farebbe {frazione(D / 2)}")
salva_dati(pd.DataFrame({"lavoro": R(1, n + 1), "durata": d}), "ex11_lavori")


def modello_minmax(d):
    """min z  con  sum_j d_j x_j <= z  e  D - sum_j d_j x_j <= z."""
    n, D = len(d), sum(d)
    m = nuovo_modello("bilanciamento_minmax")
    x = m.addVars(n, vtype=GRB.BINARY, name="x")
    z = m.addVar(name="z")
    m.setObjective(z, GRB.MINIMIZE)
    m.addConstr(gp.quicksum(d[j] * x[j] for j in R(n)) - z <= 0, name="carico1")
    m.addConstr(-gp.quicksum(d[j] * x[j] for j in R(n)) - z <= -D, name="carico2")
    return m, x, z


def modello_differenza(d):
    """min s  con  s >= W1 - W2  e  s >= W2 - W1: la stessa scelta, un altro numero."""
    n, D = len(d), sum(d)
    m = nuovo_modello("bilanciamento_differenza")
    x = m.addVars(n, vtype=GRB.BINARY, name="x")
    s = m.addVar(name="s")
    m.setObjective(s, GRB.MINIMIZE)
    carico1 = gp.quicksum(d[j] * x[j] for j in R(n))
    m.addConstr(s >= 2 * carico1 - D, name="abs_piu")
    m.addConstr(s >= D - 2 * carico1, name="abs_meno")
    return m, x, s


def duale_minmax(d):
    """Duale del rilassamento senza i bound, con la convenzione del corso (pi <= 0):
       max 0*pi1 - D*pi2   s.t.  d_j (pi1 - pi2) <= 0 per ogni j;  -pi1 - pi2 <= 1;  pi <= 0."""
    n, D = len(d), sum(d)
    dl = nuovo_modello("duale_bilanciamento")
    pi1 = dl.addVar(lb=-GRB.INFINITY, ub=0.0, name="pi1")
    pi2 = dl.addVar(lb=-GRB.INFINITY, ub=0.0, name="pi2")
    dl.setObjective(-D * pi2, GRB.MAXIMIZE)
    dl.addConstrs((d[j] * (pi1 - pi2) <= 0 for j in R(n)), name="rc_x")
    dl.addConstr(-pi1 - pi2 <= 1, name="rc_z")
    return dl, pi1, pi2


m, x, z = modello_minmax(d)

# ---------- 2. EURISTICA COSTRUTTIVA (UPPER BOUND) ----------
# LPT su due operai: i lavori in ordine di durata decrescente, ciascuno al meno carico
carico = [0, 0]
assegn = {}
for j in sorted(R(n), key=lambda j: -d[j]):
    k = 0 if carico[0] <= carico[1] else 1
    assegn[j] = k
    print(f"  Lavoro {j + 1} (durata {d[j]}): carichi {carico}; il minore e' l'operaio "
          f"{k + 1}, che passa a {carico[k] + d[j]}")
    carico[k] += d[j]
ub = max(carico)
sol_eur = {f"x[{j}]": 1 for j in R(n) if assegn[j] == 0} | {"z": ub}
assert ammissibile(m, sol_eur)
print(f"  Soluzione euristica: operaio 1 = {[j + 1 for j in R(n) if assegn[j] == 0]}, "
      f"operaio 2 = {[j + 1 for j in R(n) if assegn[j] == 1]}, carichi {carico}")
print(f"  ub = max dei carichi = {frazione(ub)}")

# ---------- 3. RILASSAMENTO LP E DUALE (LOWER BOUND) ----------
dl, pi1, pi2 = duale_minmax(d)
# ricetta: i vincoli d_j (pi1 - pi2) <= 0 impongono pi1 <= pi2; con pi1 = pi2 = t il
# vincolo -pi1 - pi2 <= 1 da' t >= -1/2, e l'obiettivo -D t cresce al calare di t
mano = {"pi1": -0.5, "pi2": -0.5}
lb, viol = valuta(dl, mano)
assert viol <= 1e-9, viol
print("  Duale a mano: i vincoli d_j (pi1 - pi2) <= 0 impongono pi1 <= pi2; ponendo")
print("  pi1 = pi2 = t, il vincolo -pi1 - pi2 <= 1 da' t >= -1/2, e l'obiettivo -D t")
print(f"  e' massimo per t = -1/2:  lb = -{D} * (-1/2) = {frazione(lb)}")
print("  Presentazione equivalente a segni cambiati (alpha = -pi1, beta = -pi2, >= 0):")
print("  max D beta con alpha <= beta e alpha + beta <= 1; alpha = beta = 1/2 da' lo stesso 9.")
print("  Significato: «i due carichi sommano a D, quindi il maggiore vale almeno D/2».")
zlp, zlpr, pi = due_rilassamenti(m, dl)

# ---------- 4. OTTIMO DEL MILP E TABELLA DEI BOUND ----------
zv = risolvi(m)
op1 = [j + 1 for j in R(n) if x[j].X > 0.5]
op2 = [j + 1 for j in R(n) if x[j].X <= 0.5]
c1 = sum(d[j - 1] for j in op1)
print(f"  Soluzione ottima (min-max): operaio 1 = {op1} (carico {c1}), operaio 2 = {op2} "
      f"(carico {D - c1});  z(MILP) = {frazione(zv)}")
riga = registra_bound("EX 11 bilanciamento", ub, lb, zlp, zlpr, zv)
salva_dati(pd.DataFrame([riga]), "ex11_bound")
assert lb <= zlp <= zv <= ub + 1e-9

# ---------- 5. LO STESSO PROBLEMA CON L'OBIETTIVO «DIFFERENZA» ----------
intestazione("EX 11 (seguito). Lo stesso problema scritto come minima differenza")
md, xd, sd = modello_differenza(d)
zd = risolvi(md)
op1d = [j + 1 for j in R(n) if xd[j].X > 0.5]
c1d = sum(d[j - 1] for j in op1d)
print(f"  Soluzione ottima (differenza): operaio 1 = {op1d} (carico {c1d}), carichi "
      f"({c1d}, {D - c1d});  z = {frazione(zd)}")
print(f"  La ripartizione e' la stessa; i due obiettivi valgono {frazione(zv)} e "
      f"{frazione(zd)}.")
print(f"  Il legame e' esatto: max = D/2 + differenza/2, cioe' {frazione(D / 2)} + "
      f"{frazione(zd / 2)} = {frazione(zv)}.")
assert abs(zv - (D / 2 + zd / 2)) < 1e-9
print("  Percio' i due modelli hanno le stesse soluzioni ottime, ma i loro valori non si")
print("  confrontano: chiamare 'differenza' il valore del min-max e' un errore.")
salva_dati(pd.DataFrame([{"obiettivo": "min-max", "z": zv},
                         {"obiettivo": "minima differenza", "z": zd}]), "ex11_obiettivi")

# ---------- 6. FIGURA ----------
fig, ax = plt.subplots(figsize=(6.6, 2.6))
colori = ["#0E7490", "#C0392B", "#1E8449", "#CA6F1E"]
for k, lavori in enumerate([op1, op2]):
    inizio = 0
    for j in lavori:
        ax.barh(k, d[j - 1], left=inizio, color=colori[(j - 1) % 4], edgecolor="white")
        ax.annotate(f"{j}", (inizio + d[j - 1] / 2, k), ha="center", va="center",
                    color="white", fontsize=9, fontweight="bold")
        inizio += d[j - 1]
ax.axvline(D / 2, color="#16324A", ls="--", lw=1.4)
ax.annotate(f"D/2 = {frazione(D / 2)}", (D / 2, -0.62), ha="center", fontsize=9, color="#16324A")
ax.set_yticks([0, 1])
ax.set_yticklabels(["operaio 1", "operaio 2"])
ax.set_xlabel("carico")
ax.set_title(f"EX 11: carichi ottimi ({c1}, {D - c1}); max = {frazione(zv)}, "
             f"differenza = {frazione(zd)}")
ax.invert_yaxis()
salva_figura(fig, "ex11_ottimo")
print("Fine.")
