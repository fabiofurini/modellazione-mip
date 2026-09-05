"""EX 12 -- Scarpe con soglia minima di produzione (famiglia 9).

Tre risorse, tre tipi di scarpa e una soglia minima per tipo: o se ne producono
almeno q_j paia, oppure zero. E' la variabile semicontinua della tecnica 3.3,
con il big-M scelto in modo naturale come massimo producibile di quel solo tipo.
"""
import gurobipy as gp
import pandas as pd
from gurobipy import GRB

from mip import (ammissibile, due_rilassamenti, frazione, nuovo_modello, registra_bound,
                 risolvi, valuta)
from stile import ARANCIO, BLU, GRIGIO, TEAL, intestazione, plt, salva_dati, salva_figura

R = range

# ---------- 1. MODELLO E ISTANZA ----------
intestazione("EX 12. Scarpe: tre risorse e una soglia minima di produzione")
NOMI = ["scarponi", "mocassini", "scarpe da passeggio"]
RISORSE = ["pelle (g)", "ore macchina", "chiodi"]
a11 = [[850, 600, 700],       # pelle per paio
       [3, 2, 2.5],           # ore macchina per paio
       [20, 15, 20]]          # chiodi per paio
b11 = [120000, 7000, 40000]
p11 = [150, 120, 130]         # prezzo di vendita per paio
q11 = [100, 200, 150]         # soglia minima
ns, nr = len(p11), len(b11)
M11 = [min(int(b11[i] // a11[i][j]) for i in R(nr)) for j in R(ns)]
salva_dati(pd.DataFrame({"tipo": NOMI, "pelle": a11[0], "ore": a11[1], "chiodi": a11[2],
                         "prezzo": p11, "soglia": q11, "massimo": M11}), "ex12_dati")
print("  Massimo producibile di un solo tipo (il big-M naturale):")
for j in R(ns):
    quale = min(R(nr), key=lambda i: b11[i] / a11[i][j])
    print(f"    {NOMI[j]:22s} {M11[j]} paia, limitato da {RISORSE[quale]}")
print("  Per i mocassini soglia e massimo coincidono (200): o se ne fanno esattamente 200,")
print("  oppure nessuno. La variabile e' di fatto binaria moltiplicata per 200.")


def modello(a, b, p, q, M):
    ns, nr = len(p), len(b)
    m = nuovo_modello("scarpe_soglia")
    x = m.addVars(ns, vtype=GRB.INTEGER, name="x")
    y = m.addVars(ns, vtype=GRB.BINARY, name="y")
    m.setObjective(gp.quicksum(p[j] * x[j] for j in R(ns)), GRB.MAXIMIZE)
    m.addConstrs((gp.quicksum(a[i][j] * x[j] for j in R(ns)) <= b[i] for i in R(nr)),
                 name="risorsa")
    m.addConstrs((x[j] - q[j] * y[j] >= 0 for j in R(ns)), name="soglia")
    m.addConstrs((x[j] - M[j] * y[j] <= 0 for j in R(ns)), name="attiva")
    return m, x, y


def duale(a, b, p, q, M):
    """min sum_i b_i pi_i  con pi >= 0, lam <= 0 (soglia, scritta >=) e mu >= 0.

    Colonne:  x_j: sum_i a_ij pi_i + lam_j + mu_j >= p_j
              y_j: -q_j lam_j - M_j mu_j >= 0
    """
    ns, nr = len(p), len(b)
    d = nuovo_modello("duale_scarpe_soglia")
    pi = d.addVars(nr, name="pi")
    lam = d.addVars(ns, lb=-GRB.INFINITY, ub=0.0, name="lam")
    mu = d.addVars(ns, name="mu")
    d.setObjective(gp.quicksum(b[i] * pi[i] for i in R(nr)), GRB.MINIMIZE)
    d.addConstrs((gp.quicksum(a[i][j] * pi[i] for i in R(nr)) + lam[j] + mu[j] >= p[j]
                  for j in R(ns)), name="rcx")
    d.addConstrs((-q[j] * lam[j] - M[j] * mu[j] >= 0 for j in R(ns)), name="rcy")
    return d


m11, x11, y11 = modello(a11, b11, p11, q11, M11)

# ---------- 2. EURISTICA COSTRUTTIVA (LOWER BOUND) ----------
# euristica costruttiva sul prezzo per grammo di pelle (la risorsa piu' stretta), rispettando la
# soglia: un tipo entra solo se si riesce a farne almeno q_j paia
def euristica(a, b, p, q):
    ns, nr = len(p), len(b)
    res = [float(v) for v in b]
    x = [0] * ns
    passi = ["prezzo per grammo di pelle: "
             + ", ".join(f"{NOMI[j]} {frazione(p[j] / a[0][j])}" for j in R(ns))]
    for j in sorted(R(ns), key=lambda j: (-p[j] / a[0][j], j)):
        if any(a[i][j] * q[j] > res[i] + 1e-9 for i in R(nr)):
            passi.append(f"{NOMI[j]}: non si arriva alla soglia {q[j]}, si scarta")
            continue
        n = min(int(res[i] // a[i][j]) for i in R(nr))
        x[j] = n
        for i in R(nr):
            res[i] -= a[i][j] * n
        passi.append(f"{NOMI[j]}: {n} paia (soglia {q[j]}); risorse residue "
                     + ", ".join(f"{RISORSE[i]} {frazione(res[i])}" for i in R(nr)))
    return x, passi


x_e, passi = euristica(a11, b11, p11, q11)
for k, riga in enumerate(passi, 1):
    print(f"  Passo {k}. {riga}")
lb11 = sum(p11[j] * x_e[j] for j in R(ns))
sol_eur = ({f"x[{j}]": x_e[j] for j in R(ns)}
           | {f"y[{j}]": 1 if x_e[j] else 0 for j in R(ns)})
assert ammissibile(m11, sol_eur), sol_eur
print("  Soluzione euristica: " + ", ".join(f"{x_e[j]} {NOMI[j]}" for j in R(ns) if x_e[j])
      + f"   lb = {frazione(lb11)}")

# ---------- 3. RILASSAMENTO LP E DUALE (UPPER BOUND) ----------
d11 = duale(a11, b11, p11, q11, M11)
migliore, mano, scelta = float("inf"), None, None
for i in R(nr):
    prezzo = max(p11[j] / a11[i][j] for j in R(ns))
    prova = {f"pi[{i}]": prezzo}
    val, viol = valuta(d11, prova)
    if viol <= 1e-9 and val < migliore:
        migliore, mano, scelta = val, prova, i
ub11, viol = valuta(d11, mano)
assert viol <= 1e-9, viol
print("  Duale a mano: lam = mu = 0 (la soglia non si valuta) e una sola risorsa valutata,")
print("  al prezzo unitario piu' alto fra i tipi di scarpa:")
for i in R(nr):
    prezzo = max(p11[j] / a11[i][j] for j in R(ns))
    print(f"    {RISORSE[i]:14s} prezzo {frazione(prezzo):>8}  ->  bound "
          f"{frazione(b11[i] * prezzo)}")
print(f"  Il bound migliore viene da: {RISORSE[scelta]}.  ub = {frazione(ub11)}")
zlp11, zlp11r, _ = due_rilassamenti(m11, d11)

# ---------- 4. OTTIMO DEL MILP ----------
z11 = risolvi(m11)
print("  Soluzione ottima: " + ", ".join(f"{int(x11[j].X)} {NOMI[j]}" for j in R(ns)
                                         if x11[j].X > 0.5))
for i in R(nr):
    usato = sum(a11[i][j] * x11[j].X for j in R(ns))
    print(f"    {RISORSE[i]}: {frazione(usato)} su {b11[i]} "
          f"({'satura' if abs(usato - b11[i]) < 1e-6 else 'residua'})")
riga = registra_bound("EX 12 scarpe con soglia", ub11, lb11, zlp11, zlp11r, z11, senso="max")
salva_dati(pd.DataFrame([riga]), "ex12_bound")
assert lb11 <= z11 <= zlp11 <= ub11 + 1e-9

# ---------- 5. QUANTO COSTA LA SOGLIA ----------
intestazione("EX 12. Il prezzo della soglia e quello dell'interezza")
m, x, y = modello(a11, b11, p11, [0] * ns, M11)
z_senza = risolvi(m)
print(f"  ub = lb = z(LP) = z(LP+) = z(MILP) = {frazione(z11)}: su questa istanza il sandwich")
print("  si chiude subito. La ragione e' che una sola risorsa e' stretta, la pelle, e il tipo")
print("  che ne ricava di piu' per grammo (i mocassini, a 1/5 di euro al grammo) la esaurisce")
print("  da solo restando dentro la propria soglia e il proprio massimo.")
print(f"  Senza soglie l'ottimo resta {frazione(z_senza)}: qui la soglia non costa nulla.")
varianti = {"senza soglie": z_senza}
m, x, y = modello(a11, b11, p11, [2 * v for v in q11], M11)
z_a = risolvi(m)
varianti["11a. soglie raddoppiate"] = z_a
print(f"  11a. Con soglie raddoppiate: z = {frazione(z_a)}. La soglia dei mocassini diventa")
print(f"       400 paia, ma la pelle ne consente al massimo {M11[1]}: nessun tipo raggiunge")
print("       piu' la propria soglia e la produzione si ferma del tutto.")
b_alt = [200000, b11[1], b11[2]]
M_alt = [min(int(b_alt[i] // a11[i][j]) for i in R(nr)) for j in R(ns)]
m, x, y = modello(a11, b_alt, p11, q11, M_alt)
z_b = risolvi(m)
varianti["11b. pelle a 200000 g"] = z_b
print(f"  11b. Con 200000 g di pelle: z = {frazione(z_b)}, cioe' "
      + ", ".join(f"{int(x[j].X)} {NOMI[j]}" for j in R(ns) if x[j].X > 0.5))
print("       Il massimo producibile cresce con la risorsa: i big-M vanno ricalcolati "
      f"({M_alt}).")
salva_dati(pd.DataFrame({"variante": list(varianti), "z": list(varianti.values())}),
           "ex12_varianti")

# ---------- 6. FIGURA ----------
fig, ax = plt.subplots(figsize=(6.8, 3.0))
idx = list(R(ns))
ax.bar([j - 0.2 for j in idx], [x_e[j] for j in idx], 0.4, color=ARANCIO, label="euristica")
ax.bar([j + 0.2 for j in idx], [x11[j].X for j in idx], 0.4, color=TEAL, label="ottimo")
for j in idx:
    ax.plot([j - 0.42, j + 0.42], [q11[j], q11[j]], color=GRIGIO, lw=1.5)
    ax.plot([j - 0.42, j + 0.42], [M11[j], M11[j]], color=BLU, lw=1.2, ls=":")
ax.plot([], [], color=GRIGIO, lw=1.5, label="soglia minima")
ax.plot([], [], color=BLU, lw=1.2, ls=":", label="massimo producibile")
ax.set_xticks(idx)
ax.set_xticklabels([n.replace(" ", "\n") for n in NOMI], fontsize=8)
ax.set_ylabel("paia prodotte")
ax.set_title(f"EX 12: euristica {frazione(lb11)} contro ottimo {frazione(z11)}")
ax.legend(fontsize=8)
salva_figura(fig, "ex12_produzione")
print("Fine.")
