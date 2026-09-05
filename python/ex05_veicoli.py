"""EX 5 -- Produzione di veicoli con lotto minimo (famiglia 9).

Due risorse (acciaio e ore di lavoro) e cinque tipi di veicolo, ciascuno con una
quantita' minima se lo si produce. E' la stessa struttura del problema 9.3 senza
il premio per la varieta': lotto minimo (3.3) piu' attivazione (3.1), cioe' le
variabili semicontinue.
"""
import gurobipy as gp
import pandas as pd
from gurobipy import GRB

from mip import (ammissibile, due_rilassamenti, frazione, nuovo_modello, registra_bound,
                 risolvi, valuta)
from stile import ARANCIO, GRIGIO, TEAL, intestazione, plt, salva_dati, salva_figura

R = range

# ---------- 1. MODELLO E ISTANZA ----------
intestazione("EX 5. Veicoli: due risorse e una quantita' minima per tipo")
NOMI = ["utilitaria", "berlina", "vettura grande", "monovolume", "monovolume grande"]
a4 = [[2, 3, 5, 6, 8],            # acciaio per unita'
      [30, 25, 40, 45, 55]]       # ore di lavoro per unita'
b4 = [1000, 2000]                 # risorse disponibili
RISORSE = ["acciaio (tonnellate)", "ore di lavoro"]
p4 = [200, 250, 300, 550, 700]    # profitto per unita'
q4 = [10, 10, 10, 5, 5]           # quantita' minima se il tipo si produce
ns, nr = len(p4), len(b4)
M4 = [min(b4[i] // a4[i][j] for i in R(nr)) for j in R(ns)]
salva_dati(pd.DataFrame({"tipo": NOMI, "acciaio": a4[0], "ore": a4[1], "profitto": p4,
                         "minimo": q4, "massimo": M4}), "ex05_dati")
print("  Quantita' massima producibile di un solo tipo (il big-M naturale):")
for j in R(ns):
    print(f"    {NOMI[j]:20s} min({b4[0]}/{a4[0][j]}, {b4[1]}/{a4[1][j]}) = {M4[j]}")


def modello(a, b, p, q, M):
    ns, nr = len(p), len(b)
    m = nuovo_modello("veicoli")
    x = m.addVars(ns, vtype=GRB.INTEGER, name="x")
    y = m.addVars(ns, vtype=GRB.BINARY, name="y")
    m.setObjective(gp.quicksum(p[j] * x[j] for j in R(ns)), GRB.MAXIMIZE)
    m.addConstrs((gp.quicksum(a[i][j] * x[j] for j in R(ns)) <= b[i] for i in R(nr)),
                 name="risorsa")
    m.addConstrs((x[j] - q[j] * y[j] >= 0 for j in R(ns)), name="lotto_minimo")
    m.addConstrs((x[j] - M[j] * y[j] <= 0 for j in R(ns)), name="attiva")
    return m, x, y


def duale(a, b, p, q, M):
    """min sum_i b_i pi_i  con pi >= 0, lam <= 0 (lotto minimo, scritto >=) e mu >= 0.

    Colonne:  x_j: sum_i a_ij pi_i + lam_j + mu_j >= p_j
              y_j: -q_j lam_j - M_j mu_j >= 0
    """
    ns, nr = len(p), len(b)
    d = nuovo_modello("duale_veicoli")
    pi = d.addVars(nr, name="pi")
    lam = d.addVars(ns, lb=-GRB.INFINITY, ub=0.0, name="lam")
    mu = d.addVars(ns, name="mu")
    d.setObjective(gp.quicksum(b[i] * pi[i] for i in R(nr)), GRB.MINIMIZE)
    d.addConstrs((gp.quicksum(a[i][j] * pi[i] for i in R(nr)) + lam[j] + mu[j] >= p[j]
                  for j in R(ns)), name="rcx")
    d.addConstrs((-q[j] * lam[j] - M[j] * mu[j] >= 0 for j in R(ns)), name="rcy")
    return d


m4, x4, y4 = modello(a4, b4, p4, q4, M4)

# ---------- 2. EURISTICA COSTRUTTIVA (LOWER BOUND) ----------
# euristica costruttiva sul profitto per ora di lavoro (la risorsa piu' stretta): si accende un
# tipo solo se si riesce a raggiungere la quantita' minima, poi si spinge al massimo
def euristica(a, b, p, q):
    ns, nr = len(p), len(b)
    res = list(map(float, b))
    x = [0] * ns
    passi = [f"profitto per ora di lavoro: "
             + ", ".join(f"{NOMI[j]} {frazione(p[j] / a[1][j])}" for j in R(ns))]
    for j in sorted(R(ns), key=lambda j: (-p[j] / a[1][j], j)):
        if any(a[i][j] * q[j] > res[i] + 1e-9 for i in R(nr)):
            passi.append(f"{NOMI[j]}: non si arriva alla quantita' minima {q[j]}, si scarta")
            continue
        n = min(int(res[i] // a[i][j]) for i in R(nr))
        x[j] = n
        for i in R(nr):
            res[i] -= a[i][j] * n
        passi.append(f"{NOMI[j]}: si producono {n} unita' (minimo {q[j]}); risorse residue "
                     + ", ".join(f"{RISORSE[i]} {frazione(res[i])}" for i in R(nr)))
    return x, passi


x_e, passi = euristica(a4, b4, p4, q4)
for k, riga in enumerate(passi, 1):
    print(f"  Passo {k}. {riga}")
lb4 = sum(p4[j] * x_e[j] for j in R(ns))
sol_eur = ({f"x[{j}]": x_e[j] for j in R(ns)}
           | {f"y[{j}]": 1 if x_e[j] else 0 for j in R(ns)})
assert ammissibile(m4, sol_eur), sol_eur
print(f"  Soluzione euristica: " + ", ".join(f"{x_e[j]} {NOMI[j]}" for j in R(ns) if x_e[j])
      + f"   lb = {frazione(lb4)}")

# ---------- 3. RILASSAMENTO LP E DUALE (UPPER BOUND) ----------
d4 = duale(a4, b4, p4, q4, M4)
# ricetta: lam = mu = 0 (il lotto minimo non si valuta) e una sola risorsa
# valutata al prezzo che nessun veicolo riesce a battere
migliore, mano, scelta = float("inf"), None, None
for i in R(nr):
    prezzo = max(p4[j] / a4[i][j] for j in R(ns))
    prova = {f"pi[{i}]": prezzo}
    val, viol = valuta(d4, prova)
    if viol <= 1e-9 and val < migliore:
        migliore, mano, scelta = val, prova, i
ub4, viol = valuta(d4, mano)
assert viol <= 1e-9, viol
print("  Duale a mano: lam = mu = 0 e una sola risorsa valutata, al prezzo unitario piu' alto")
print("  fra i veicoli (cosi' ogni vincolo a_ij pi_i >= p_j e' soddisfatto):")
for i in R(nr):
    prezzo = max(p4[j] / a4[i][j] for j in R(ns))
    print(f"    {RISORSE[i]:22s} prezzo {frazione(prezzo):>8}  ->  bound "
          f"{frazione(b4[i] * prezzo)}")
print(f"  Il bound migliore viene da: {RISORSE[scelta]}.  ub = {frazione(ub4)}")
zlp4, zlp4r, _ = due_rilassamenti(m4, d4)

# ---------- 4. OTTIMO DEL MILP ----------
z4 = risolvi(m4)
print("  Soluzione ottima: " + ", ".join(f"{int(x4[j].X)} {NOMI[j]}" for j in R(ns)
                                         if x4[j].X > 0.5))
for i in R(nr):
    usato = sum(a4[i][j] * x4[j].X for j in R(ns))
    print(f"    {RISORSE[i]}: {frazione(usato)} su {b4[i]}")
riga = registra_bound("EX 5 veicoli", ub4, lb4, zlp4, zlp4r, z4, senso="max")
salva_dati(pd.DataFrame([riga]), "ex05_bound")
assert lb4 <= z4 <= zlp4 <= ub4 + 1e-9

# ---------- 5. IL LOTTO MINIMO E' UN VINCOLO, NON UN AIUTO ----------
intestazione("EX 5. Che cosa costa il lotto minimo")
m, x, y = modello(a4, b4, p4, [0] * ns, M4)
z_senza = risolvi(m)
print(f"  Senza quantita' minime l'ottimo sale a {frazione(z_senza)} "
      f"(contro {frazione(z4)}): il")
print(f"  lotto minimo costa {frazione(z_senza - z4)} di profitto perche' impedisce di")
print("  produrre poche unita' dei tipi piu' redditizi.")
varianti = {"senza quantita' minime": z_senza}
# 4a: quantita' minime raddoppiate
m, x, y = modello(a4, b4, p4, [2 * v for v in q4], M4)
z_a = risolvi(m)
varianti["4a. quantita' minime raddoppiate"] = z_a
print(f"  4a. Con quantita' minime raddoppiate: z = {frazione(z_a)}")
# 4b: ore di lavoro raddoppiate
b_b = [b4[0], 2 * b4[1]]
m, x, y = modello(a4, b_b, p4, q4,
                  [min(b_b[i] // a4[i][j] for i in R(nr)) for j in R(ns)])
z_b = risolvi(m)
varianti["4b. ore di lavoro raddoppiate"] = z_b
uso_b = [sum(a4[i][j] * x[j].X for j in R(ns)) for i in R(nr)]
print(f"  4b. Con le ore di lavoro raddoppiate: z = {frazione(z_b)}; risorse usate "
      + ", ".join(f"{RISORSE[i]} {frazione(uso_b[i])} su {b_b[i]}" for i in R(nr)))
print("      Le ore restano la risorsa stretta e il profitto raddoppia quasi esattamente.")
salva_dati(pd.DataFrame({"variante": list(varianti), "z": list(varianti.values())}),
           "ex05_varianti")

# ---------- 6. FIGURA ----------
fig, ax = plt.subplots(figsize=(6.8, 3.0))
idx = list(R(ns))
ax.bar([j - 0.2 for j in idx], [x_e[j] for j in idx], 0.4, color=ARANCIO, label="euristica")
ax.bar([j + 0.2 for j in idx], [x4[j].X for j in idx], 0.4, color=TEAL, label="ottimo")
for j in idx:
    ax.plot([j - 0.42, j + 0.42], [q4[j], q4[j]], color=GRIGIO, lw=1.5)
ax.plot([], [], color=GRIGIO, lw=1.5, label="quantita' minima")
ax.set_xticks(idx)
ax.set_xticklabels([n.replace(" ", "\n") for n in NOMI], fontsize=8)
ax.set_ylabel("unita' prodotte")
ax.set_title(f"EX 5: euristica {frazione(lb4)} contro ottimo {frazione(z4)}")
ax.legend(fontsize=8)
salva_figura(fig, "ex05_produzione")
print("Fine.")
