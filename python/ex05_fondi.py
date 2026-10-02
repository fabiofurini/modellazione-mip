"""EX 5 -- Fondi acquistabili a lotti (famiglia 10).

Uno zaino intero (non binario) con quattro tipi di lotto e un vincolo di
proporzione riscritto in forma lineare. Serve anche a mostrare come si verifica
una soluzione duale: se ne esibisce prima una non ammissibile, come
controesempio, e poi si costruisce quella giusta.

La quota morde: il secondo fondo rende piu' del doppio degli altri per milione
investito, ma non si puo' comprare da solo. L'euristica ci casca --- parte dal
fondo migliore, non riesce a comprarne nemmeno un lotto e ripiega sul primo ---
e si ferma a 16 contro un ottimo di 23.
"""
import gurobipy as gp
import pandas as pd
from gurobipy import GRB

from mip import (ammissibile, due_rilassamenti, frazione, nuovo_modello, registra_bound,
                 risolvi, stampa_lp, valuta)
from stile import ARANCIO, BLU, GRIGIO, TEAL, intestazione, plt, salva_dati, salva_figura
from esteso import salva_modello

R = range

# ---------- 1. MODELLO E ISTANZA ----------
intestazione("EX 5. Fondi a lotti: massimizzare il rendimento annuo entro il budget")
c12 = [12, 15, 18, 25]         # costo di un lotto (milioni)
t12 = [1 / 6, 1 / 3, 1 / 9, 0.16]   # rendimento annuo, frazione del capitale investito
nf = len(c12)
p12 = [c12[j] * t12[j] for j in R(nf)]  # rendimento di un lotto: 2, 5, 2 e 4 milioni
B12 = 100                      # budget disponibile
QUOTA = 0.5                    # il fondo 2 non puo' superare meta' dei lotti totali
# nel vincolo di quota il fondo 2 ha coefficiente +1 e gli altri -1
QC = [1 if j == 1 else -1 for j in R(nf)]
salva_dati(pd.DataFrame({"fondo": list(R(1, nf + 1)), "costo_lotto": c12,
                         "rendimento": t12, "rendimento_lotto": p12}), "ex05_dati")
print("  Rendimento di un lotto: "
      + ", ".join(f"fondo {j + 1} = {c12[j]} * {frazione(t12[j])} = {frazione(p12[j])}"
                  for j in R(nf)) + " milioni.")
print(f"  Il vincolo x2 <= {QUOTA} (x1 + x2 + x3 + x4) diventa, moltiplicando per 2 e "
      "portando a sinistra, -x1 + x2 - x3 - x4 <= 0.")


def modello(c, p, B):
    m = nuovo_modello("fondi")
    x = m.addVars(nf, vtype=GRB.INTEGER, name="x")
    m.setObjective(gp.quicksum(p[j] * x[j] for j in R(nf)), GRB.MAXIMIZE)
    m.addConstr(gp.quicksum(c[j] * x[j] for j in R(nf)) <= B, name="budget")
    m.addConstr(gp.quicksum(QC[j] * x[j] for j in R(nf)) <= 0, name="quota")
    return m, x


def duale(c, p, B):
    """min B alpha  s.t.  c_j alpha + QC_j beta >= p_j per ogni fondo,  alpha, beta >= 0."""
    d = nuovo_modello("duale_fondi")
    alpha = d.addVar(name="alpha")     # budget
    beta = d.addVar(name="beta")       # quota
    d.setObjective(B * alpha, GRB.MINIMIZE)
    d.addConstrs((c[j] * alpha + QC[j] * beta >= p[j] for j in R(nf)), name="rc")
    return d


m12, x12 = modello(c12, p12, B12)
salva_modello(m12, "ex05_primale")
print("  Il modello dell'istanza:")
stampa_lp(m12)

# ---------- 2. EURISTICA COSTRUTTIVA (LOWER BOUND) ----------
# euristica costruttiva sul rendimento per milione investito, rispettando la quota a ogni acquisto
def euristica(c, p, B):
    x = [0] * nf
    ordine = sorted(R(nf), key=lambda j: (-p[j] / c[j], j))
    passi = ["rendimento per milione investito: "
             + ", ".join(f"fondo {j + 1} = {frazione(p[j])}/{c[j]} = {frazione(p[j] / c[j])}"
                         for j in R(nf))
             + f"; si parte dal fondo {ordine[0] + 1}"]
    for j in ordine:
        comprati = 0
        while True:
            prova = list(x)
            prova[j] += 1
            if (sum(c[k] * prova[k] for k in R(nf)) > B
                    or sum(QC[k] * prova[k] for k in R(nf)) > 0):
                break
            x, comprati = prova, comprati + 1
        residuo = B - sum(c[k] * x[k] for k in R(nf))
        motivo = ("il budget residuo non basta per un altro lotto"
                  if residuo < c[j] else "un altro lotto violerebbe la quota")
        passi.append(f"fondo {j + 1}: si comprano {comprati} lotti e ci si ferma perche' "
                     f"{motivo} (residuo {residuo} milioni)")
    return x, passi


x_eur, passi = euristica(c12, p12, B12)
for k, riga in enumerate(passi, 1):
    print(f"  Passo {k}. {riga}")
lb12 = sum(p12[j] * x_eur[j] for j in R(nf))
sol_eur = {f"x[{j}]": x_eur[j] for j in R(nf)}
assert ammissibile(m12, sol_eur), sol_eur
print("  Soluzione euristica: "
      + ", ".join(f"{x_eur[j]} lotti del fondo {j + 1}" for j in R(nf))
      + f"   lb = {frazione(lb12)}")

# ---------- 3. RILASSAMENTO LP E DUALE (UPPER BOUND) ----------
d12 = duale(c12, p12, B12)
salva_modello(d12, "ex05_duale")
# controesempio: la scelta alpha = 5/32, beta = 1/8 non e' ammissibile
tentativo = {"alpha": 5 / 32, "beta": 1 / 8}
val_t, viol_t = valuta(d12, tentativo)
print(f"  Tentativo NON ammissibile: alpha = 5/32, beta = 1/8 da' "
      f"{c12[0]} * 5/32 - 1/8 = {frazione(c12[0] * 5 / 32 - 1 / 8)} < {frazione(p12[0])}: "
      f"il primo vincolo duale e' violato di {frazione(viol_t)}.")
print("  Un valore duale si legge come bound solo dopo aver verificato TUTTI i vincoli.")
assert viol_t > 1e-9
# ricetta corretta: beta = 0 e alpha pari al rendimento per milione piu' alto
alpha_min = max(p12[j] / c12[j] for j in R(nf))
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
print("  Soluzione ottima: "
      + ", ".join(f"{int(x12[j].X)} lotti del fondo {j + 1}" for j in R(nf))
      + f", spesa {int(sum(c12[j] * x12[j].X for j in R(nf)))} su {B12}, "
      f"rendimento {frazione(z12)}")
riga = registra_bound("EX 5 fondi", ub12, lb12, zlp12, zlp12r, z12, senso="max")
salva_dati(pd.DataFrame([riga]), "ex05_bound")
assert lb12 <= z12 <= zlp12 <= ub12 + 1e-9

# ---------- 5. IL PREZZO DELL'INTEREZZA ----------
intestazione("EX 5. Il prezzo dell'interezza e il ruolo della quota")
print(f"  z(LP) = {frazione(zlp12)} contro z(MILP) = {frazione(z12)}: il rilassamento compra")
print(f"  {frazione(B12 / c12[0])} lotti del fondo 1, che non si possono acquistare a pezzi.")
print(f"  La differenza {frazione(zlp12 - z12)} e' il costo dell'indivisibilita' dei lotti.")
print()
print("  La quota morde: il fondo 2 rende piu' del doppio degli altri per milione investito, e")
print("  senza il vincolo si comprerebbe soltanto quello. Con la quota, ogni lotto del fondo 2")
print("  va accompagnato da un lotto di un altro fondo:")
p_povero = [3.0 if j == 1 else p12[j] for j in R(nf)]   # il fondo 2 scende al 20 per cento
prove = []
for nome, p_alt, quota in [("dati originali, con quota", p12, True),
                           ("dati originali, senza quota", p12, False),
                           ("fondo 2 meno redditizio, con quota", p_povero, True),
                           ("fondo 2 meno redditizio, senza quota", p_povero, False)]:
    m, x = modello(c12, p_alt, B12)
    if not quota:
        m.update()
        m.remove([c for c in m.getConstrs() if c.ConstrName == "quota"][0])
        m.update()
    z = risolvi(m)
    print(f"  {nome:38s} z = {frazione(z):>4}   "
          f"x = ({', '.join(str(int(x[j].X)) for j in R(nf))})")
    prove.append({"variante": nome, "z": z, "x1": int(x[0].X), "x2": int(x[1].X)})
salva_dati(pd.DataFrame(prove), "ex05_quota")
assert prove[2]["z"] < prove[3]["z"], "col fondo 2 piu' redditizio la quota deve mordere"

# ---------- 6. FIGURA: LA SOLUZIONE ----------
# stessa veste delle altre figure del capitolo: un gruppo di barre per fondo,
# euristica contro ottimo, e la spesa che ciascuna soluzione impegna
fig, ax = plt.subplots(figsize=(6.4, 3.0))
idx = list(R(nf))
ax.bar([j - 0.2 for j in idx], [x_eur[j] for j in idx], 0.4, color=ARANCIO,
       label=f"euristica ({frazione(lb12)})")
ax.bar([j + 0.2 for j in idx], [x12[j].X for j in idx], 0.4, color=TEAL,
       label=f"ottimo ({frazione(z12)})")
for j in idx:
    massimo = B12 // c12[j]
    ax.plot([j - 0.42, j + 0.42], [massimo, massimo], color=GRIGIO, lw=1.3, ls=":")
ax.plot([], [], color=GRIGIO, lw=1.3, ls=":", label="lotti comprabili col solo budget")
ax.set_xticks(idx)
ax.set_xticklabels([f"fondo {j + 1}\n{c12[j]} mln al lotto" for j in idx], fontsize=8)
ax.set_ylabel("lotti comprati")
ax.set_title(f"EX 5: la soluzione, {int(sum(c12[j] * x12[j].X for j in R(nf)))} milioni "
             f"impegnati su {B12}")
salva_figura(fig, "ex05_regione")
print("Fine.")
