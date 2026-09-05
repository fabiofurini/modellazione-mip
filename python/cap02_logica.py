"""Capitolo 2 -- Logica e variabili binarie: da CNF a vincoli lineari.

Trasforma in forma normale congiuntiva e poi in vincoli lineari le implicazioni
dei cinque esercizi del capitolo, e *dimostra per enumerazione* che la
traduzione e' esatta: per ogni assegnazione delle binarie, la formula e' vera se
e solo se il sistema lineare e' soddisfatto. Conclude con un modello di
selezione di progetti che usa quei vincoli.
"""
import gurobipy as gp
import pandas as pd
from gurobipy import GRB

from booleane import (AND, IMP, NOT, OR, V, cnf, equivalenti, scrivi, testo_cnf,
                      valuta, variabili, verifica, vincolo)
from mip import ammissibile, frazione, nuovo_modello, rilassamento, risolvi, stampa_soluzione
from stile import BLU, CICLO, ROSSO, TEAL, VERDE, intestazione, plt, salva_dati, salva_figura

R = range
x = {p: V(f"x{p}") for p in R(1, 11)}

# ---------- 1. LE PROPRIETA' DELL'ALGEBRA BOOLEANA ----------
intestazione("1. De Morgan, distributivita', assorbimento: verifica per enumerazione")
a, b, c = V("xa"), V("xb"), V("xc")
PROPRIETA = [
    ("distributivita' (C)", AND(a, OR(b, c)), OR(AND(a, b), AND(a, c))),
    ("distributivita' (D)", OR(a, AND(b, c)), AND(OR(a, b), OR(a, c))),
    ("De Morgan (A)", NOT(OR(a, b)), AND(NOT(a), NOT(b))),
    ("De Morgan (B)", NOT(AND(a, b)), OR(NOT(a), NOT(b))),
    ("assorbimento (E)", OR(a, AND(a, b)), a),
    ("assorbimento (F)", AND(a, OR(a, b)), a),
    ("doppia negazione", NOT(NOT(a)), a),
]
for nome, sinistra, destra in PROPRIETA:
    assert equivalenti(sinistra, destra), nome
    print(f"  {nome:24s} verificata su tutte le {2 ** len(variabili(sinistra) | variabili(destra))} assegnazioni")

# ---------- 2. LE SCISSIONI AMMESSE E QUELLA NON AMMESSA ----------
intestazione("2. Scindere un'implicazione: quando si puo' e quando no")
scissioni = [
    ("antecedente disgiunzione", IMP(OR(a, b), c), AND(IMP(a, c), IMP(b, c)), True),
    ("conseguente congiunzione", IMP(a, AND(b, c)), AND(IMP(a, b), IMP(a, c)), True),
    ("antecedente congiunzione", IMP(AND(a, b), c), AND(IMP(a, c), IMP(b, c)), False),
]
for nome, sinistra, destra, attesa in scissioni:
    ok = equivalenti(sinistra, destra)
    assert ok == attesa, nome
    print(f"  {nome:26s} scissione {'valida' if ok else 'NON valida'}")
contro = {"xa": 1, "xb": 0, "xc": 0}
assert valuta(IMP(AND(a, b), c), contro) and not valuta(AND(IMP(a, c), IMP(b, c)), contro)
print("  controesempio alla terza: xa = 1, xb = 0, xc = 0 rende vera l'implicazione")
print("  originale (antecedente falso) ma falsa la congiunzione delle due scisse.")

# ---------- 3. I CINQUE ESERCIZI: CNF E VINCOLI LINEARI ----------
intestazione("3. Esercizi 2.1-2.5: forma normale congiuntiva e vincoli lineari")
ESERCIZI = {
    "2.1": [("se si sceglie 2, si sceglie 3", IMP(x[2], x[3])),
            ("se si sceglie 2, non si sceglie 4", IMP(x[2], NOT(x[4]))),
            ("se si scelgono 1 e 6, si sceglie 7", IMP(AND(x[1], x[6]), x[7])),
            ("se si sceglie 1 o 6, si sceglie 8", IMP(OR(x[1], x[6]), x[8])),
            ("se si scelgono 2 e 3, non si sceglie 9", IMP(AND(x[2], x[3]), NOT(x[9]))),
            ("se si sceglie 2 o 3, non si sceglie 10", IMP(OR(x[2], x[3]), NOT(x[10])))],
    "2.2": [("se non si sceglie 3, si sceglie 2", IMP(NOT(x[3]), x[2])),
            ("se non si sceglie 4, non si sceglie 2", IMP(NOT(x[4]), NOT(x[2]))),
            ("se si sceglie 7, si scelgono 1 e 6", IMP(x[7], AND(x[1], x[6]))),
            ("se si sceglie 8, si sceglie 1 o 6", IMP(x[8], OR(x[1], x[6]))),
            ("se non si sceglie 9, si scelgono 2 e 3", IMP(NOT(x[9]), AND(x[2], x[3]))),
            ("se non si sceglie 10, si sceglie 2 o 3", IMP(NOT(x[10]), OR(x[2], x[3])))],
    "2.3": [("se si sceglie 7 o 3, si scelgono 1 e 2", IMP(OR(x[7], x[3]), AND(x[1], x[2]))),
            ("se si scelgono 1, 6 e 7, si sceglie 8", IMP(AND(x[1], x[6], x[7]), x[8])),
            ("se si scelgono 5 e 2 e non 4, non si sceglie 3",
             IMP(AND(x[5], x[2], NOT(x[4])), NOT(x[3]))),
            ("se si sceglie 6 e (1 o 4), si sceglie 2 e (5 o 7)",
             IMP(AND(OR(x[1], x[4]), x[6]), AND(x[2], OR(x[5], x[7])))),
            ("se si sceglie (2 o 5) e non 8, si sceglie 3 o non 6",
             IMP(AND(OR(x[2], x[5]), NOT(x[8])), OR(x[3], NOT(x[6])))),
            ("se (1 o 4) e (2 o 5) e non 8, allora 3 e (non 6 o 7)",
             IMP(AND(OR(x[1], x[4]), OR(x[2], x[5]), NOT(x[8])),
                 AND(x[3], OR(NOT(x[6]), x[7]))))],
    "2.4": [("se si sceglie 4, almeno due fra 1, 2, 3",
             IMP(x[4], OR(AND(x[1], x[2]), AND(x[1], x[3]), AND(x[2], x[3])))),
            ("se almeno due fra 6, 7, 8, allora 5",
             IMP(OR(AND(x[6], x[7]), AND(x[6], x[8]), AND(x[7], x[8])), x[5])),
            ("se non si sceglie 4, almeno due fra 1, 2, 3, 9",
             IMP(NOT(x[4]), OR(AND(x[1], x[2]), AND(x[1], x[3]), AND(x[1], x[9]),
                               AND(x[2], x[3]), AND(x[2], x[9]), AND(x[3], x[9])))),
            ("se si sceglie 8, allora (1 e 6) o (1 e 7) o (2 e 6)",
             IMP(x[8], OR(AND(x[1], x[6]), AND(x[1], x[7]), AND(x[2], x[6])))),
            ("se almeno due fra 1, 3, 5, non si sceglie 9",
             IMP(OR(AND(x[1], x[3]), AND(x[1], x[5]), AND(x[3], x[5])), NOT(x[9]))),
            ("se (1 e 2) o (3 e 4), allora 5",
             IMP(OR(AND(x[1], x[2]), AND(x[3], x[4])), x[5]))],
    "2.5": [("se si sceglie 1 o 2, si sceglie 3", IMP(OR(x[1], x[2]), x[3])),
            ("se si sceglie 4, si scelgono 5 e 6", IMP(x[4], AND(x[5], x[6]))),
            ("se si sceglie 1 o 2, si scelgono 3 e 4",
             IMP(OR(x[1], x[2]), AND(x[3], x[4]))),
            ("se si scelgono 1 e 2, si sceglie 3", IMP(AND(x[1], x[2]), x[3])),
            ("se si sceglie 5 o 6, non si sceglie 7", IMP(OR(x[5], x[6]), NOT(x[7]))),
            ("se non si sceglie 8 o non si sceglie 9, si sceglie 10",
             IMP(OR(NOT(x[8]), NOT(x[9])), x[10]))],
}
righe = []
for es, voci in ESERCIZI.items():
    print(f"\nEsercizio {es}")
    for i, (testo, formula) in enumerate(voci, 1):
        clausole = cnf(formula)
        vincoli = [vincolo(c) for c in clausole]
        totali, vere = verifica(formula, vincoli)
        print(f"  {es}.{i}  {testo}")
        print(f"        CNF ({len(clausole)} clausole) -> "
              + " ;  ".join(scrivi(v, mat=False) for v in vincoli))
        print(f"        equivalenza verificata su {totali} assegnazioni "
              f"({vere} rendono vera la formula)")
        righe.append({"esercizio": es, "punto": i, "descrizione": testo,
                      "clausole": len(clausole),
                      "vincoli": " ; ".join(scrivi(v, mat=False) for v in vincoli),
                      "assegnazioni": totali, "vere": vere})
salva_dati(pd.DataFrame(righe), "cap02_implicazioni")

# ---------- 4. CLAUSOLE O CONTEGGIO: DUE FORMULAZIONI DELLO STESSO INSIEME ----------
intestazione("4. 'Almeno due fra 1, 2, 3 se si sceglie 4': clausole contro conteggio")


def confronta(clausole=True):
    """max x1+x2+x3+3 x4 con l'implicazione x4 => almeno due fra 1,2,3."""
    m = nuovo_modello("almeno_due")
    v = m.addVars(R(1, 5), vtype=GRB.BINARY, name="x")
    m.setObjective(v[1] + v[2] + v[3] + 3 * v[4], GRB.MAXIMIZE)
    m.addConstr(v[1] + v[2] + v[3] + 2 * v[4] <= 3, name="budget")
    if clausole:                       # tre clausole: x_i + x_j >= x4 per ogni coppia
        for i, j in [(1, 2), (1, 3), (2, 3)]:
            m.addConstr(v[i] + v[j] - v[4] >= 0, name=f"coppia{i}{j}")
    else:                              # forma contata: x1 + x2 + x3 >= 2 x4
        m.addConstr(v[1] + v[2] + v[3] - 2 * v[4] >= 0, name="conteggio")
    return m, v


for nome, cl in [("tre clausole", True), ("un vincolo contato", False)]:
    m, v = confronta(cl)
    z = risolvi(m)
    zr, sol, _ = rilassamento(m, rafforzato=True)
    print(f"  {nome:20s} z(MILP) = {frazione(z)}   z(LP+) = {frazione(zr)}   "
          + "  ".join(f"x{p}={frazione(sol[f'x[{p}]'])}" for p in R(1, 5)))
# stesso insieme intero, rilassamenti diversi: si verifica per enumerazione
from itertools import product as _p
for valori in _p((0, 1), repeat=4):
    a = dict(zip(R(1, 5), valori))
    cl3 = all(a[i] + a[j] - a[4] >= 0 for i, j in [(1, 2), (1, 3), (2, 3)])
    cnt = a[1] + a[2] + a[3] - 2 * a[4] >= 0
    assert cl3 == cnt, a
print("  Le due formulazioni hanno le stesse 16 soluzioni binarie (verificato per")
print("  enumerazione) ma rilassamenti diversi: il vincolo contato e' piu' forte.")

# ---------- 5. UN MODELLO DI SELEZIONE CON I VINCOLI LOGICI ----------
intestazione("5. Selezione di progetti soggetta alle implicazioni dell'esercizio 2.1")
r = {1: 9, 2: 7, 3: 4, 4: 8, 5: 3, 6: 6, 7: 2, 8: 5, 9: 7, 10: 6}   # ricavi
b = {1: 4, 2: 3, 3: 2, 4: 4, 5: 2, 6: 3, 7: 1, 8: 3, 9: 4, 10: 3}   # costi
budget = 14
salva_dati(pd.DataFrame({"progetto": list(r), "ricavo": list(r.values()),
                         "costo": list(b.values())}), "cap02_progetti")


def modello_selezione(con_logica=True):
    m = nuovo_modello("selezione_progetti")
    xv = m.addVars(R(1, 11), vtype=GRB.BINARY, name="x")
    m.setObjective(gp.quicksum(r[p] * xv[p] for p in R(1, 11)), GRB.MAXIMIZE)
    m.addConstr(gp.quicksum(b[p] * xv[p] for p in R(1, 11)) <= budget, name="budget")
    if con_logica:
        for i, (_, formula) in enumerate(ESERCIZI["2.1"], 1):
            for j, cl in enumerate(cnf(formula), 1):
                coef, verso, rhs = vincolo(cl)
                lhs = gp.quicksum(k * xv[int(n[1:])] for n, k in coef.items())
                m.addConstr(lhs <= rhs if verso == "<=" else lhs >= rhs, name=f"logica{i}_{j}")
    return m, xv


m_libero, _ = modello_selezione(con_logica=False)
z_libero = risolvi(m_libero)
m_log, x_log = modello_selezione(con_logica=True)
z_log = risolvi(m_log)
zlp_log, _, _ = rilassamento(m_log, rafforzato=True)
scelti = sorted(p for p in R(1, 11) if x_log[p].X > 0.5)
print(f"Senza i vincoli logici:  z = {frazione(z_libero)}")
print(f"Con i vincoli logici:    z = {frazione(z_log)}   progetti scelti: {scelti}")
print(f"                         costo {sum(b[p] for p in scelti)} su un budget di {budget}")
print(f"Rilassamento LP+ del modello con i vincoli logici: {frazione(zlp_log)}")
for _, formula in ESERCIZI["2.1"]:
    assert valuta(formula, {f"x{p}": int(p in scelti) for p in R(1, 11)})
print("Tutte e sei le implicazioni sono soddisfatte dalla soluzione ottima.")
salva_dati(pd.DataFrame([{"modello": "senza vincoli logici", "z": z_libero, "z_lp": None},
                         {"modello": "con vincoli logici", "z": z_log, "z_lp": zlp_log}]),
           "cap02_selezione")

# ---------- 6. FIGURA: QUANTE ASSEGNAZIONI SOPRAVVIVONO A OGNI IMPLICAZIONE ----------
sopravvivono = []
etichette = []
for i, (testo, formula) in enumerate(ESERCIZI["2.1"], 1):
    totali, vere = verifica(formula, nomi=[f"x{p}" for p in R(1, 11)])
    sopravvivono.append(vere)
    etichette.append(f"2.1.{i}")
cumulate = []
insieme = None
from itertools import product as _prod
tutte = [dict(zip([f"x{p}" for p in R(1, 11)], v)) for v in _prod((0, 1), repeat=10)]
vive = tutte
for testo, formula in ESERCIZI["2.1"]:
    vive = [ass for ass in vive if valuta(formula, ass)]
    cumulate.append(len(vive))
print(f"Assegnazioni delle 10 binarie: {len(tutte)}; dopo le sei implicazioni: {cumulate[-1]}")
fig, ax = plt.subplots(figsize=(7.2, 3.6))
ax.bar(etichette, sopravvivono, color=TEAL, label="singola implicazione")
ax.plot(etichette, cumulate, "o-", color=ROSSO, label="tutte le implicazioni imposte insieme")
ax.axhline(len(tutte), color=BLU, lw=1, ls="--")
ax.annotate(f"$2^{{10}} = {len(tutte)}$ assegnazioni", (0, len(tutte)),
            textcoords="offset points", xytext=(4, -14), fontsize=9, color=BLU)
ax.set_ylabel("assegnazioni ammissibili")
ax.set_title("Esercizio 2.1: quante delle $2^{10}$ assegnazioni sopravvivono")
ax.legend(loc="lower left", fontsize=9)
salva_figura(fig, "cap02_implicazioni")
salva_dati(pd.DataFrame({"implicazione": etichette, "singola": sopravvivono,
                         "cumulata": cumulate}), "cap02_ammissibili")
print("Fine.")
