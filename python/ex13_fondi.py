"""EX 13 -- Fondi acquistabili a lotti (famiglia 10).

Uno zaino intero (non binario) con due soli tipi di lotto e un vincolo di
proporzione riscritto in forma lineare. Serve anche a mostrare come si verifica
una soluzione duale: la bozza di partenza ne proponeva una non ammissibile, qui
la si esibisce come controesempio e poi si costruisce quella giusta.
"""
import gurobipy as gp
import pandas as pd
from gurobipy import GRB

from mip import (ammissibile, due_rilassamenti, frazione, nuovo_modello, registra_bound,
                 risolvi, stampa_lp, valuta)
from stile import ARANCIO, BLU, GRIGIO, TEAL, intestazione, plt, salva_dati, salva_figura

R = range

# ---------- 1. MODELLO E ISTANZA ----------
intestazione("EX 13. Fondi a lotti: massimizzare il rendimento annuo entro il budget")
c12 = [12, 20]                 # costo di un lotto (milioni)
t12 = [1 / 6, 0.15]            # rendimento annuo, frazione del capitale investito
p12 = [c12[j] * t12[j] for j in R(2)]   # rendimento di un lotto: 2 e 3 milioni
B12 = 100                      # budget disponibile
QUOTA = 0.5                    # il fondo 2 non puo' superare meta' dei lotti totali
salva_dati(pd.DataFrame({"fondo": [1, 2], "costo_lotto": c12, "rendimento": t12,
                         "rendimento_lotto": p12}), "ex13_dati")
print(f"  Rendimento di un lotto: fondo 1 = 12 * 1/6 = {frazione(p12[0])}, "
      f"fondo 2 = 20 * 0,15 = {frazione(p12[1])} milioni.")
print(f"  Il vincolo x2 <= {QUOTA} (x1 + x2) diventa, moltiplicando per 2 e portando a "
      "sinistra, -x1 + x2 <= 0.")


def modello(c, p, B):
    m = nuovo_modello("fondi")
    x = m.addVars(2, vtype=GRB.INTEGER, name="x")
    m.setObjective(gp.quicksum(p[j] * x[j] for j in R(2)), GRB.MAXIMIZE)
    m.addConstr(gp.quicksum(c[j] * x[j] for j in R(2)) <= B, name="budget")
    m.addConstr(-x[0] + x[1] <= 0, name="quota")
    return m, x


def duale(c, p, B):
    """min B alpha  s.t.  c_1 alpha - beta >= p_1,  c_2 alpha + beta >= p_2,  alpha, beta >= 0."""
    d = nuovo_modello("duale_fondi")
    alpha = d.addVar(name="alpha")     # budget
    beta = d.addVar(name="beta")       # quota
    d.setObjective(B * alpha, GRB.MINIMIZE)
    d.addConstr(c[0] * alpha - beta >= p[0], name="rc[0]")
    d.addConstr(c[1] * alpha + beta >= p[1], name="rc[1]")
    return d


m12, x12 = modello(c12, p12, B12)
print("  Il modello dell'istanza:")
stampa_lp(m12)

# ---------- 2. EURISTICA COSTRUTTIVA (LOWER BOUND) ----------
# euristica costruttiva sul rendimento per milione investito, rispettando la quota a ogni acquisto
def euristica(c, p, B):
    x = [0, 0]
    ordine = sorted(R(2), key=lambda j: (-p[j] / c[j], j))
    passi = ["rendimento per milione investito: "
             + ", ".join(f"fondo {j + 1} = {frazione(p[j])}/{c[j]} = {frazione(p[j] / c[j])}"
                         for j in R(2))
             + f"; si parte dal fondo {ordine[0] + 1}"]
    for j in ordine:
        comprati = 0
        while True:
            prova = list(x)
            prova[j] += 1
            if sum(c[k] * prova[k] for k in R(2)) > B or -prova[0] + prova[1] > 0:
                break
            x, comprati = prova, comprati + 1
        residuo = B - sum(c[k] * x[k] for k in R(2))
        motivo = ("il budget residuo non basta per un altro lotto"
                  if residuo < c[j] else "un altro lotto violerebbe la quota")
        passi.append(f"fondo {j + 1}: si comprano {comprati} lotti e ci si ferma perche' "
                     f"{motivo} (residuo {residuo} milioni)")
    return x, passi


x_eur, passi = euristica(c12, p12, B12)
for k, riga in enumerate(passi, 1):
    print(f"  Passo {k}. {riga}")
lb12 = sum(p12[j] * x_eur[j] for j in R(2))
sol_eur = {f"x[{j}]": x_eur[j] for j in R(2)}
assert ammissibile(m12, sol_eur), sol_eur
print(f"  Soluzione euristica: {x_eur[0]} lotti del fondo 1 e {x_eur[1]} del fondo 2   "
      f"lb = {frazione(lb12)}")

# ---------- 3. RILASSAMENTO LP E DUALE (UPPER BOUND) ----------
d12 = duale(c12, p12, B12)
# controesempio: la scelta alpha = 5/32, beta = 1/8 non e' ammissibile
tentativo = {"alpha": 5 / 32, "beta": 1 / 8}
val_t, viol_t = valuta(d12, tentativo)
print(f"  Tentativo NON ammissibile: alpha = 5/32, beta = 1/8 da' "
      f"{c12[0]} * 5/32 - 1/8 = {frazione(c12[0] * 5 / 32 - 1 / 8)} < {frazione(p12[0])}: "
      f"il primo vincolo duale e' violato di {frazione(viol_t)}.")
print("  Un valore duale si legge come bound solo dopo aver verificato TUTTI i vincoli.")
assert viol_t > 1e-9
# ricetta corretta: beta = 0 e alpha pari al rendimento per milione piu' alto
alpha_min = max(p12[j] / c12[j] for j in R(2))
mano = {"alpha": alpha_min, "beta": 0.0}
ub12, viol = valuta(d12, mano)
assert viol <= 1e-9, viol
print(f"  Duale a mano: beta = 0 e alpha = max_j p_j / c_j = {frazione(alpha_min)} "
      "(il milione vale quanto rende nel fondo migliore),")
print(f"  quindi ogni vincolo c_j alpha >= p_j e' soddisfatto  ->  ub = {B12} * alpha = "
      f"{frazione(ub12)}")
zlp12, zlp12r, _ = due_rilassamenti(m12, d12)

# ---------- 4. OTTIMO DEL MILP E TABELLA DEI BOUND ----------
z12 = risolvi(m12)
print(f"  Soluzione ottima: {int(x12[0].X)} lotti del fondo 1 e {int(x12[1].X)} del fondo 2, "
      f"spesa {int(sum(c12[j] * x12[j].X for j in R(2)))} su {B12}, rendimento {frazione(z12)}")
riga = registra_bound("EX 13 fondi", ub12, lb12, zlp12, zlp12r, z12, senso="max")
salva_dati(pd.DataFrame([riga]), "ex13_bound")
assert lb12 <= z12 <= zlp12 <= ub12 + 1e-9

# ---------- 5. IL PREZZO DELL'INTEREZZA ----------
intestazione("EX 13. Il prezzo dell'interezza e il ruolo della quota")
print(f"  z(LP) = {frazione(zlp12)} contro z(MILP) = {frazione(z12)}: il rilassamento compra")
print(f"  {frazione(B12 / c12[0])} lotti del fondo 1, che non si possono acquistare a pezzi.")
print(f"  La differenza {frazione(zlp12 - z12)} e' il costo dell'indivisibilita' dei lotti.")
print()
print("  Sui dati dell'istanza la quota non morde: il fondo 1 rende di piu' per milione investito e")
print("  la soluzione ottima non compra affatto il fondo 2. La quota diventa attiva appena il")
print("  fondo 2 rende il 20 per cento, cioe' 4 milioni a lotto:")
prove = []
for nome, p_alt, quota in [("dati originali, con quota", p12, True),
                           ("dati originali, senza quota", p12, False),
                           ("fondo 2 al 20 per cento, con quota", [p12[0], 4.0], True),
                           ("fondo 2 al 20 per cento, senza quota", [p12[0], 4.0], False)]:
    m, x = modello(c12, p_alt, B12)
    if not quota:
        m.update()
        m.remove([c for c in m.getConstrs() if c.ConstrName == "quota"][0])
        m.update()
    z = risolvi(m)
    print(f"  {nome:38s} z = {frazione(z):>4}   x = ({int(x[0].X)}, {int(x[1].X)})")
    prove.append({"variante": nome, "z": z, "x1": int(x[0].X), "x2": int(x[1].X)})
salva_dati(pd.DataFrame(prove), "ex13_quota")
assert prove[2]["z"] < prove[3]["z"], "col fondo 2 piu' redditizio la quota deve mordere"

# ---------- 6. FIGURA: LA REGIONE AMMISSIBILE ----------
fig, ax = plt.subplots(figsize=(5.4, 4.2))
punti = [(i, j) for i in R(10) for j in R(10)
         if c12[0] * i + c12[1] * j <= B12 and -i + j <= 0]
ax.plot([q[0] for q in punti], [q[1] for q in punti], "o", color=GRIGIO, ms=5,
        label="soluzioni intere ammissibili")
xs = [0, B12 / c12[0]]
ax.plot(xs, [(B12 - c12[0] * v) / c12[1] for v in xs], color=BLU, lw=1.6, label="budget")
ax.plot([0, 9], [0, 9], color=ARANCIO, lw=1.6, label="quota $x_2 \\leq x_1$")
ax.plot(x_eur[0], x_eur[1], marker="^", color=ARANCIO, ms=11, ls="",
        label=f"euristica ({frazione(lb12)})")
ax.plot(x12[0].X, x12[1].X, marker="*", color=TEAL, ms=17, ls="",
        label=f"ottimo ({frazione(z12)})")
ax.set_xlim(-0.4, 9.4)
ax.set_ylim(-0.4, 6.4)
ax.set_xlabel("lotti del fondo 1")
ax.set_ylabel("lotti del fondo 2")
ax.set_title("EX 13: la regione ammissibile intera")
ax.legend(fontsize=8, loc="upper right")
salva_figura(fig, "ex13_regione")
print("Fine.")
