"""Problema 12.1 -- Alberi di Natale: configurazioni e scatole di luci.

Due decisioni intere legate da un vincolo di disponibilita': quante luci servono
(dalle configurazioni scelte) e quante se ne comprano (dalle scatole). Sopra, il
vincolo di varieta' «almeno f configurazioni diverse», che richiede un indicatore
per configurazione e il legame con il conteggio (tecnica 3.11).
"""
import gurobipy as gp
import pandas as pd
from gurobipy import GRB

from mip import (ammissibile, due_rilassamenti, frazione, nuovo_modello, registra_bound,
                 risolvi, valuta)
from stile import ARANCIO, BLU, GRIGIO, TEAL, intestazione, plt, salva_dati, salva_figura

R = range

# ---------- 1. MODELLO E ISTANZA ----------
intestazione("12.1 Alberi di Natale: configurazioni, luci e scatole")
q1 = 20                          # alberi da decorare
i1 = [7, 6, 8]                   # costo di installazione di una configurazione
u1 = [[4, 2], [2, 3], [2, 2]]    # luci di colore l richieste dalla configurazione c
p1 = [100, 200]                  # costo di una scatola
v1 = [[10, 2], [15, 4]]          # luci di colore l contenute in una scatola di tipo b
f1 = 2                           # configurazioni diverse richieste
nc, nl, nb = len(i1), len(u1[0]), len(p1)
salva_dati(pd.DataFrame({"configurazione": R(1, nc + 1), "costo": i1,
                         "colore_1": [u[0] for u in u1], "colore_2": [u[1] for u in u1]}),
           "luci1_configurazioni")
salva_dati(pd.DataFrame({"scatola": R(1, nb + 1), "costo": p1,
                         "colore_1": [v[0] for v in v1], "colore_2": [v[1] for v in v1]}),
           "luci1_scatole")


def modello_1(q, i, u, p, v, f):
    nc, nl, nb = len(i), len(u[0]), len(p)
    m = nuovo_modello("luci")
    x = m.addVars(nc, vtype=GRB.INTEGER, name="x")        # alberi con la configurazione c
    y = m.addVars(nb, vtype=GRB.INTEGER, name="y")        # scatole comprate del tipo b
    z = m.addVars(nc, vtype=GRB.BINARY, name="z")         # configurazione c usata
    m.setObjective(gp.quicksum(i[c] * x[c] for c in R(nc))
                   + gp.quicksum(p[b] * y[b] for b in R(nb)), GRB.MINIMIZE)
    m.addConstr(x.sum() == q, name="alberi")
    m.addConstrs((gp.quicksum(v[b][l] * y[b] for b in R(nb))
                  - gp.quicksum(u[c][l] * x[c] for c in R(nc)) >= 0 for l in R(nl)),
                 name="luci")
    m.addConstr(z.sum() >= f, name="varieta")
    m.addConstrs((x[c] - z[c] >= 0 for c in R(nc)), name="usata")
    return m, x, y, z


def duale_1(q, i, u, p, v, f):
    """max q alpha + f gamma

    alpha libera (vincolo di uguaglianza sugli alberi), beta_l >= 0 (disponibilita'
    delle luci), gamma >= 0 (varieta'), delta_c >= 0 (legame x_c >= z_c). Colonne:
      x_c:  alpha - sum_l u_cl beta_l + delta_c <= i_c
      y_b:  sum_l v_bl beta_l <= p_b
      z_c:  gamma - delta_c <= 0
    """
    nc, nl, nb = len(i), len(u[0]), len(p)
    dl = nuovo_modello("duale_luci")
    alpha = dl.addVar(lb=-GRB.INFINITY, name="alpha")
    beta = dl.addVars(nl, name="beta")
    gamma = dl.addVar(name="gamma")
    delta = dl.addVars(nc, name="delta")
    dl.setObjective(q * alpha + f * gamma, GRB.MAXIMIZE)
    dl.addConstrs((alpha - gp.quicksum(u[c][l] * beta[l] for l in R(nl)) + delta[c] <= i[c]
                   for c in R(nc)), name="rcx")
    dl.addConstrs((gp.quicksum(v[b][l] * beta[l] for l in R(nl)) <= p[b] for b in R(nb)),
                  name="rcy")
    dl.addConstrs((gamma - delta[c] <= 0 for c in R(nc)), name="rcz")
    return dl


m1, x1, y1, z1 = modello_1(q1, i1, u1, p1, v1, f1)
print("  Prezzo di una luce, colore per colore, in ciascun tipo di scatola:")
for b in R(nb):
    print(f"    scatola {b + 1}: " + ", ".join(
        f"colore {l + 1} a {frazione(p1[b] / v1[b][l])}" for l in R(nl) if v1[b][l] > 0))

# ---------- 2. EURISTICA COSTRUTTIVA (UPPER BOUND) ----------
# Due fasi. Prima le configurazioni: q - f + 1 alberi con quella di installazione
# piu' economica e un albero per ciascuna delle altre f - 1, cosi' la varieta' e'
# soddisfatta al minimo costo di installazione. Poi le scatole: finche' manca
# qualche luce si compra la scatola col prezzo per luce mancante piu' basso.
def euristica(q, i, u, p, v, f):
    nc, nl, nb = len(i), len(u[0]), len(p)
    ordine = sorted(R(nc), key=lambda c: (i[c], c))
    x = [0] * nc
    for c in ordine[1:f]:
        x[c] = 1
    x[ordine[0]] = q - (f - 1)
    altre = ", ".join(str(c + 1) for c in ordine[1:f])
    passi = [f"configurazioni: {x[ordine[0]]} alberi con la {ordine[0] + 1} "
             f"(installazione {i[ordine[0]]} a testa) e un albero con la configurazione "
             f"{altre}, la seconda piu' economica da installare"]
    serve = [sum(u[c][l] * x[c] for c in R(nc)) for l in R(nl)]
    passi.append("luci necessarie: " + ", ".join(f"colore {l + 1} -> {serve[l]}" for l in R(nl)))
    y = [0] * nb
    while True:
        manca = [max(0, serve[l] - sum(v[b][l] * y[b] for b in R(nb))) for l in R(nl)]
        if max(manca) == 0:
            break
        # prezzo per luce ancora mancante: si contano solo le luci utili
        b = min(R(nb), key=lambda b: (p[b] / max(1e-9, sum(min(v[b][l], manca[l])
                                                           for l in R(nl))), b))
        y[b] += 1
        passi.append(f"mancano {manca}: si compra una scatola {b + 1} (costo {p[b]}); "
                     f"scatole {y}")
    return x, y, passi


x_eur, y_eur, passi = euristica(q1, i1, u1, p1, v1, f1)
for k, riga in enumerate(passi[:4], 1):
    print(f"  Passo {k}. {riga}")
print(f"  ... ({len(passi) - 4} acquisti successivi dello stesso tipo)")
print(f"  Passo {len(passi)}. {passi[-1]}")
ub1 = sum(i1[c] * x_eur[c] for c in R(nc)) + sum(p1[b] * y_eur[b] for b in R(nb))
sol_eur = ({f"x[{c}]": x_eur[c] for c in R(nc)} | {f"y[{b}]": y_eur[b] for b in R(nb)}
           | {f"z[{c}]": 1 if x_eur[c] > 0 else 0 for c in R(nc)})
assert ammissibile(m1, sol_eur), sol_eur
print(f"  Soluzione euristica: alberi {x_eur}, scatole {y_eur}   ub = {frazione(ub1)}")
print("  L'euristica sceglie la configurazione con l'installazione piu' economica, la 2, che")
print("  pero' e' la piu' avida di luci del colore costoso: il conto lo pagano le scatole.")
print("  E' il tipico errore di un'euristica costruttiva che guarda una sola voce di costo.")

# ---------- 3. RILASSAMENTO LP E DUALE (LOWER BOUND) ----------
dl1 = duale_1(q1, i1, u1, p1, v1, f1)
# ricetta: gamma = delta = 0; si valuta un solo colore, al prezzo per luce piu'
# basso che nessuna scatola riesce a battere; poi ogni albero costa almeno
# alpha = min_c (i_c + prezzo delle sue luci)
migliore, mano, scelto = float("-inf"), None, None
for l in R(nl):
    prezzo = min(p1[b] / v1[b][l] for b in R(nb) if v1[b][l] > 0)
    prova = {f"beta[{l}]": prezzo}
    prova["alpha"] = min(i1[c] + u1[c][l] * prezzo for c in R(nc))
    val, viol = valuta(dl1, prova)
    if viol <= 1e-9 and val > migliore:
        migliore, mano, scelto = val, prova, l
lb1, viol = valuta(dl1, mano)
assert viol <= 1e-9, viol
prezzo = mano[f"beta[{scelto}]"]
print(f"  Duale a mano: gamma = delta = 0 e un solo colore valutato. Sul colore {scelto + 1}")
print(f"  entrambi i tipi di scatola danno lo stesso prezzo per luce, {frazione(prezzo)}:")
print(f"  e' il piu' alto valore di beta compatibile con sum_l v_bl beta_l <= p_b.")
print("  Allora ogni albero costa almeno alpha = min_c (i_c + u_c" + str(scelto + 1)
      + " * beta) = " + ", ".join(f"{i1[c]} + {u1[c][scelto]} * {frazione(prezzo)} = "
                                  f"{frazione(i1[c] + u1[c][scelto] * prezzo)}"
                                  for c in R(nc)))
print(f"  alpha = {frazione(mano['alpha'])}  ->  lb = {q1} * alpha = {frazione(lb1)}")
zlp1, zlp1r, _ = due_rilassamenti(m1, dl1)

# ---------- 4. OTTIMO DEL MILP ----------
z1v = risolvi(m1)
print("  Soluzione ottima: "
      + ", ".join(f"{int(x1[c].X)} alberi con la configurazione {c + 1}" for c in R(nc)
                  if x1[c].X > 0.5)
      + "; scatole "
      + ", ".join(f"{int(y1[b].X)} di tipo {b + 1}" for b in R(nb) if y1[b].X > 0.5))
for l in R(nl):
    serve = sum(u1[c][l] * x1[c].X for c in R(nc))
    compra = sum(v1[b][l] * y1[b].X for b in R(nb))
    print(f"    colore {l + 1}: servono {int(serve)} luci, se ne comprano {int(compra)}")
riga = registra_bound("1 luci", ub1, lb1, zlp1, zlp1r, z1v)
salva_dati(pd.DataFrame([riga]), "luci1_bound")
assert lb1 <= zlp1 <= z1v <= ub1 + 1e-9

# ---------- 5. DOMANDE DI MODELLAZIONE AGGIUNTIVE ----------
varianti = {}


def variante(nome, m):
    z = risolvi(m)
    print(f"  {nome:70s} z = {frazione(z)}")
    return z


# 1a: si vogliono tutte e tre le configurazioni
m, x, y, z = modello_1(q1, i1, u1, p1, v1, 3)
varianti["1a"] = variante("1a. Devono comparire tutte e tre le configurazioni (f = 3)", m)
# 1b: ogni configurazione usata deve decorare almeno tre alberi (lotto minimo)
m, x, y, z = modello_1(q1, i1, u1, p1, v1, f1)
m.addConstrs((x[c] - 3 * z[c] >= 0 for c in R(nc)), name="lotto_minimo")
varianti["1b"] = variante("1b. Ogni configurazione usata decora almeno tre alberi", m)
salva_dati(pd.DataFrame({"variante": list(varianti), "z": list(varianti.values())}),
           "luci1_varianti")

# ---------- 6. FIGURA ----------
fig, ax = plt.subplots(figsize=(6.8, 3.0))
etichette = ["euristica", "ottimo"]
inst = [sum(i1[c] * x_eur[c] for c in R(nc)),
        sum(i1[c] * x1[c].X for c in R(nc))]
scat = [sum(p1[b] * y_eur[b] for b in R(nb)),
        sum(p1[b] * y1[b].X for b in R(nb))]
ax.barh(R(2), inst, 0.5, color=TEAL, label="installazione")
ax.barh(R(2), scat, 0.5, left=inst, color=ARANCIO, label="scatole di luci")
for k in R(2):
    ax.annotate(f"{frazione(inst[k] + scat[k])}", (inst[k] + scat[k] + 40, k), va="center",
                fontsize=9)
ax.axvline(lb1, color=BLU, ls="--", lw=1.4)
ax.annotate(f"bound duale {frazione(lb1)}", (lb1, 1.55), ha="center", fontsize=8, color=BLU)
ax.set_yticks(R(2))
ax.set_yticklabels(etichette)
ax.set_xlim(0, max(inst[k] + scat[k] for k in R(2)) * 1.18)
ax.set_xlabel("costo (euro)")
ax.set_title("12.1: dove va il costo")
ax.legend(fontsize=8, loc="lower right")
ax.invert_yaxis()
salva_figura(fig, "cap10_luci_ottimo")
print("Fine.")
