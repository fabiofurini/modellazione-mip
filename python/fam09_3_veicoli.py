"""Problema 9.3 -- Veicoli: lotto minimo e premio per la varieta'.

Tre tecniche insieme: la variabile semicontinua del lotto minimo (3.3), il
conteggio dei tipi attivi (3.11) e un premio «se e solo se» si producono almeno
due tipi (3.10). Il premio si incassa solo se il conteggio arriva a due: il
verso mancante segue dall'ottimalita' perche' il premio e' positivo.
"""
import gurobipy as gp
import pandas as pd
from gurobipy import GRB

from mip import (ammissibile, due_rilassamenti, frazione, nuovo_modello, registra_bound,
                 risolvi, valuta)
from stile import ARANCIO, BLU, ROSSO, TEAL, VERDE, intestazione, plt, salva_dati, salva_figura

R = range

# ---------- 1. MODELLO E ISTANZA ----------
intestazione("9.3 Veicoli: lotto minimo per tipo e premio se si producono almeno due tipi")
a3 = [[2, 3, 5],        # acciaio (tonnellate) per unita' dei tre tipi
      [30, 25, 40]]     # ore di manodopera per unita'
b3 = [100, 1200]        # acciaio e ore disponibili
p3 = [200, 250, 300]    # profitto per unita'
q3 = [10, 10, 10]       # quantita' minima se il tipo si produce
r3 = 500                # premio se si producono almeno due tipi
n3, m3 = 3, 2
# il piu' piccolo big-M valido per tipo: quante unita' al massimo consentono le risorse
M3 = [min(b3[i] // a3[i][j] for i in R(m3)) for j in R(n3)]
salva_dati(pd.DataFrame({"tipo": R(1, n3 + 1), "acciaio": a3[0], "ore": a3[1],
                         "profitto": p3, "minimo": q3, "M": M3}), "veic3_dati")
print(f"  Risorse: {b3[0]} t di acciaio, {b3[1]} ore. Big-M per tipo (dai soli dati): {M3}")


def modello_3(a, b, p, q, r):
    n, m = len(p), len(b)
    M = [min(b[i] // a[i][j] for i in R(m)) for j in R(n)]
    mm = nuovo_modello("veicoli")
    x = mm.addVars(n, vtype=GRB.INTEGER, name="x")     # unita' prodotte
    y = mm.addVars(n, vtype=GRB.BINARY, name="y")      # tipo attivato
    z = mm.addVar(vtype=GRB.BINARY, name="z")          # premio per la varieta'
    mm.setObjective(gp.quicksum(p[j] * x[j] for j in R(n)) + r * z, GRB.MAXIMIZE)
    mm.addConstrs((gp.quicksum(a[i][j] * x[j] for j in R(n)) <= b[i] for i in R(m)),
                  name="risorsa")
    mm.addConstrs((x[j] - q[j] * y[j] >= 0 for j in R(n)), name="lotto_minimo")
    mm.addConstrs((x[j] - M[j] * y[j] <= 0 for j in R(n)), name="attiva")
    mm.addConstr(-gp.quicksum(y[j] for j in R(n)) + 2 * z <= 0, name="premio")
    return mm, x, y, z


def duale_3(a, b, p, q, r):
    """min sum_i b_i pi_i;  sum_i a_ij pi_i - alpha_j + beta_j >= p_j;
    q_j alpha_j - M_j beta_j + gamma >= 0;  -2 gamma >= r;  pi, alpha, beta >= 0, gamma <= 0.
    (scritto con i segni della tabella di conversione per un primale di massimo)"""
    n, m = len(p), len(b)
    M = [min(b[i] // a[i][j] for i in R(m)) for j in R(n)]
    dl = nuovo_modello("duale_veicoli")
    pi = dl.addVars(m, name="pi")                                  # risorse (<= in un max)
    alpha = dl.addVars(n, lb=-GRB.INFINITY, ub=0.0, name="alpha")   # lotto minimo (>= in un max)
    beta = dl.addVars(n, name="beta")                              # attivazione (<=)
    gamma = dl.addVar(name="gamma")                                # premio (<=)
    dl.setObjective(gp.quicksum(b[i] * pi[i] for i in R(m)), GRB.MINIMIZE)
    dl.addConstrs((gp.quicksum(a[i][j] * pi[i] for i in R(m)) + alpha[j] + beta[j] >= p[j]
                   for j in R(n)), name="rc_x")
    dl.addConstrs((-q[j] * alpha[j] - M[j] * beta[j] - gamma >= 0 for j in R(n)), name="rc_y")
    dl.addConstr(2 * gamma >= r, name="rc_z")
    return dl


m3m, x3, y3, z3 = modello_3(a3, b3, p3, q3, r3)

# ---------- 2. EURISTICA COSTRUTTIVA (LOWER BOUND: E' UN MASSIMO) ----------
# euristica costruttiva: si attivano due tipi (per incassare il premio) partendo dai profitti per
# unita' di risorsa piu' scarsa, poi si riempie con il tipo migliore
def euristica(a, b, p, q, r):
    n, m = len(p), len(b)
    # rapporto profitto / consumo della risorsa piu' stretta
    ordine = sorted(R(n), key=lambda j: -p[j] / max(a[i][j] / b[i] for i in R(m)))
    x = [0] * n
    res = list(b)
    attivi = []
    for j in ordine:                       # prima il lotto minimo dei due tipi migliori
        if len(attivi) < 2 and all(res[i] >= a[i][j] * q[j] for i in R(m)):
            x[j] = q[j]
            for i in R(m):
                res[i] -= a[i][j] * q[j]
            attivi.append(j)
    for j in ordine:                       # poi si riempie con il tipo piu' redditizio
        if x[j] == 0:
            continue
        extra = min(res[i] // a[i][j] for i in R(m))
        x[j] += extra
        for i in R(m):
            res[i] -= a[i][j] * extra
    return x, attivi, res


x_eur, attivi, res = euristica(a3, b3, p3, q3, r3)
lb3 = sum(p3[j] * x_eur[j] for j in R(n3)) + (r3 if len(attivi) >= 2 else 0)
sol_eur = {f"x[{j}]": x_eur[j] for j in R(n3)} \
    | {f"y[{j}]": 1 if x_eur[j] > 0 else 0 for j in R(n3)} | {"z": 1 if len(attivi) >= 2 else 0}
assert ammissibile(m3m, sol_eur)
print(f"  Euristica: si attivano i tipi {[j + 1 for j in attivi]} al lotto minimo, poi si")
print(f"  riempie col piu' redditizio; produzione {x_eur}, risorse residue {res}")
print(f"  lb = {sum(p3[j] * x_eur[j] for j in R(n3))} + {r3} di premio = {frazione(lb3)}")

# ---------- 3. RILASSAMENTO LP E DUALE (UPPER BOUND) ----------
dl3 = duale_3(a3, b3, p3, q3, r3)
# ricetta: gamma = r/2 (il minimo ammesso dal vincolo 2 gamma >= r), beta = 0, e
# lambda_j = gamma / q_j (ogni tipo attivato "porta" la sua quota di premio); poi si
# valuta una sola risorsa al prezzo che copre tutti i tipi, e si sceglie la migliore
gamma = r3 / 2
lam = [gamma / q3[j] for j in R(n3)]
bound = {}
for i in R(m3):
    prezzo = max((p3[j] + lam[j]) / a3[i][j] for j in R(n3))
    bound[i] = b3[i] * prezzo
critica = min(bound, key=bound.get)
prezzo = max((p3[j] + lam[j]) / a3[critica][j] for j in R(n3))
mano = {"gamma": gamma} | {f"pi[{i}]": 0.0 for i in R(m3)} \
    | {f"alpha[{j}]": -lam[j] for j in R(n3)} | {f"beta[{j}]": 0.0 for j in R(n3)}
mano[f"pi[{critica}]"] = prezzo
ub3, viol = valuta(dl3, mano)
assert viol <= 1e-9, (viol, mano)
print(f"  Duale a mano: gamma = r/2 = {frazione(gamma)} (il minimo che soddisfa 2 gamma >= r),")
print(f"  beta = 0 e lambda_j = gamma / q_j = " + ", ".join(frazione(v) for v in lam)
      + ": ogni tipo")
print("  attivato porta la sua quota di premio. Poi si valuta una sola risorsa al prezzo")
print("  che copre tutti i tipi, max_j (p_j + lambda_j) / a_ij, e si tiene la piu' stretta:")
for i in R(m3):
    print(f"    risorsa {i + 1}: prezzo {frazione(max((p3[j] + lam[j]) / a3[i][j] for j in R(n3)))}"
          f"  ->  b_i * prezzo = {frazione(bound[i])}")
print(f"  Il minimo e' la risorsa {critica + 1}:  ub = {frazione(ub3)}")
zlp3, zlp3r, _ = due_rilassamenti(m3m, dl3)

# ---------- 4. OTTIMO DEL MILP ----------
z3v = risolvi(m3m)
print("  Soluzione ottima: produzione " + ", ".join(str(round(x3[j].X)) for j in R(n3))
      + f"; tipi attivi {[j + 1 for j in R(n3) if y3[j].X > 0.5]}; premio incassato: "
      + ("si" if z3.X > 0.5 else "no"))
print("  Risorse usate: " + ", ".join(
    f"{frazione(sum(a3[i][j] * round(x3[j].X) for j in R(n3)))} su {b3[i]}" for i in R(m3)))
riga = registra_bound("3 veicoli", ub3, lb3, zlp3, zlp3r, z3v, senso="max")
salva_dati(pd.DataFrame([riga]), "veic3_bound")
assert lb3 <= z3v <= zlp3 + 1e-6 <= ub3 + 1e-6

# ---------- 5. DOMANDE DI MODELLAZIONE AGGIUNTIVE ----------
varianti = {}


def variante(nome, m):
    z = risolvi(m)
    print(f"  {nome:70s} z = {frazione(z)}")
    return z


# 3a: il premio richiede almeno tre tipi diversi
m, x, y, z = modello_3(a3, b3, p3, q3, r3)
m.update()
m.remove([c for c in m.getConstrs() if c.ConstrName == "premio"])
m.addConstr(-gp.quicksum(y[j] for j in R(n3)) + 3 * z <= 0, name="premio3")
varianti["3a"] = variante("3a. Il premio si incassa solo con almeno tre tipi diversi", m)
# 3b: il premio e' nullo -- che cosa succede al legame "se e solo se"?
m, x, y, z = modello_3(a3, b3, p3, q3, 0)
zz = risolvi(m)
print(f"  {'3b. Il premio vale 0: z non e piu un indicatore fedele':70s} z = {frazione(zz)}")
print(f"      tipi attivi {[j + 1 for j in R(n3) if y[j].X > 0.5]}, ma z = {round(z.X)}: con")
print("      premio nullo l'ottimo non ha alcun motivo di alzare z, e il vincolo da solo")
print("      non lo impone. Per farne un indicatore fedele serve anche il verso opposto.")
varianti["3b"] = zz
salva_dati(pd.DataFrame({"variante": list(varianti), "z": list(varianti.values())}),
           "veic3_varianti")

# ---------- 6. FIGURA ----------
fig, ax = plt.subplots(figsize=(6.8, 3.0))
tipi = list(R(1, n3 + 1))
colori = [TEAL if y3[j].X > 0.5 else "#F4F6F7" for j in R(n3)]
ax.bar(tipi, [x3[j].X for j in R(n3)], color=colori, edgecolor="#7F8C8D", width=0.55)
for j in R(n3):
    ax.plot([j + 0.72, j + 1.28], [q3[j], q3[j]], color=ROSSO, lw=2)
ax.plot([], [], color=ROSSO, lw=2, label="lotto minimo $q_j$")
for j in R(n3):
    ax.annotate(str(round(x3[j].X)), (j + 1, x3[j].X), ha="center", va="bottom", fontsize=9)
ax.set_xticks(tipi)
ax.set_xticklabels([f"tipo {j}" for j in tipi])
ax.set_ylabel("unita' prodotte")
ax.set_title(f"9.3: piano ottimo (z = {frazione(z3v)}, premio incassato)")
ax.legend(fontsize=8)
salva_figura(fig, "cap09_veicoli_ottimo")
print("Fine.")
