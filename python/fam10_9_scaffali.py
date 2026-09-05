"""Problema 11.4 -- Libri sugli scaffali: minimizzare la somma delle altezze.

Assegnamento con capacita' (la larghezza dello scaffale) e una variabile di
massimo per scaffale (tecnica 3.5): l'altezza di uno scaffale e' quella del libro
piu' alto che vi si trova. Serve anche a mostrare che l'ordine con cui l'euristica
guarda gli oggetti puo' portarla in un vicolo cieco.
"""
import gurobipy as gp
import pandas as pd
from gurobipy import GRB

from mip import (ammissibile, due_rilassamenti, frazione, nuovo_modello, registra_bound,
                 risolvi, valuta)
from stile import ARANCIO, BLU, GRIGIO, TEAL, intestazione, plt, salva_dati, salva_figura

R = range

# ---------- 1. MODELLO E ISTANZA ----------
intestazione("11.4 Libri sugli scaffali: minimizzare la somma delle altezze")
w4 = [3, 5, 4, 6]      # larghezza dei libri
h4 = [8, 5, 7, 4]      # altezza dei libri
c4 = 10                # larghezza di ogni scaffale
n4, m4 = len(w4), 2    # libri e scaffali
salva_dati(pd.DataFrame({"libro": R(1, n4 + 1), "larghezza": w4, "altezza": h4}),
           "scaffali4_dati")
print(f"  Larghezza totale dei libri: {sum(w4)}; capacita' complessiva: {m4} * {c4} = "
      f"{m4 * c4}.")


def modello_4(w, h, c, m):
    n = len(w)
    mod = nuovo_modello("scaffali")
    x = mod.addVars(n, m, vtype=GRB.BINARY, name="x")
    y = mod.addVars(m, name="y")            # altezza dello scaffale
    mod.setObjective(y.sum(), GRB.MINIMIZE)
    mod.addConstrs((x.sum(b, "*") == 1 for b in R(n)), name="libro")
    mod.addConstrs((gp.quicksum(w[b] * x[b, s] for b in R(n)) <= c for s in R(m)),
                   name="larghezza")
    mod.addConstrs((y[s] - h[b] * x[b, s] >= 0 for b in R(n) for s in R(m)), name="altezza")
    return mod, x, y


def duale_4(w, h, c, m):
    """max sum_b alpha_b + c sum_s beta_s   con  beta_s <= 0  e  gamma >= 0,
       colonna di x_bs: alpha_b + w_b beta_s - h_b gamma_bs <= 0,
       colonna di y_s:  sum_b gamma_bs <= 1."""
    n = len(w)
    dl = nuovo_modello("duale_scaffali")
    alpha = dl.addVars(n, lb=-GRB.INFINITY, name="alpha")
    beta = dl.addVars(m, lb=-GRB.INFINITY, ub=0.0, name="beta")
    gamma = dl.addVars(n, m, name="gamma")
    dl.setObjective(alpha.sum() + c * beta.sum(), GRB.MAXIMIZE)
    dl.addConstrs((gamma.sum("*", s) <= 1 for s in R(m)), name="rcy")
    dl.addConstrs((alpha[b] + w[b] * beta[s] - h[b] * gamma[b, s] <= 0
                   for b in R(n) for s in R(m)), name="rcx")
    return dl


m4mod, x4, y4 = modello_4(w4, h4, c4, m4)

# ---------- 2. DUE ORDINI PER LA STESSA EURISTICA ----------
def first_fit(w, h, c, m, ordine, etichetta):
    """Ogni libro sul primo scaffale in cui entra; se non entra da nessuna parte
    l'euristica fallisce, e restituisce None."""
    n = len(w)
    dove, residuo, passi = {}, [c] * m, []
    for b in ordine:
        posti = [s for s in R(m) if residuo[s] >= w[b]]
        if not posti:
            passi.append(f"libro {b + 1} (largo {w[b]}): non entra in nessuno scaffale "
                         f"(residui {residuo}) -> l'euristica fallisce")
            print(f"  {etichetta}")
            for k, riga in enumerate(passi, 1):
                print(f"    Passo {k}. {riga}")
            return None, None, passi
        s = posti[0]
        dove[b] = s
        residuo[s] -= w[b]
        passi.append(f"libro {b + 1} (largo {w[b]}, alto {h[b]}) sullo scaffale {s + 1}; "
                     f"residui {residuo}")
    altezze = [max((h[b] for b in R(n) if dove[b] == s), default=0) for s in R(m)]
    print(f"  {etichetta}")
    for k, riga in enumerate(passi, 1):
        print(f"    Passo {k}. {riga}")
    print(f"    altezze degli scaffali {altezze}, somma {sum(altezze)}")
    return dove, altezze, passi


ordine_h = sorted(R(n4), key=lambda b: (-h4[b], b))
dove_h, alt_h, _ = first_fit(w4, h4, c4, m4, ordine_h,
                             "Ordine per altezza decrescente (libri 1, 3, 2, 4):")
assert dove_h is None, "su questa istanza l'ordine per altezza deve incastrarsi"
print("  L'ordine per altezza non tiene conto delle larghezze e si blocca. Il criterio giusto")
print("  per un vincolo di capacita' e' la larghezza.")
ordine_w = sorted(R(n4), key=lambda b: (-w4[b], b))
dove_w, alt_w, _ = first_fit(w4, h4, c4, m4, ordine_w,
                             "Ordine per larghezza decrescente (libri 4, 2, 3, 1):")
ub4 = sum(alt_w)
sol_eur = {f"x[{b},{dove_w[b]}]": 1 for b in R(n4)} | {f"y[{s}]": alt_w[s] for s in R(m4)}
assert ammissibile(m4mod, sol_eur), sol_eur
print(f"  ub = {frazione(ub4)}")

# ---------- 3. RILASSAMENTO LP E DUALE (LOWER BOUND) ----------
dl4 = duale_4(w4, h4, c4, m4)
# ricetta: beta = 0, e si concentra tutto il "peso" gamma sul libro piu' alto
alto = max(R(n4), key=lambda b: h4[b])
mano = ({f"gamma[{alto},{s}]": 1.0 for s in R(m4)}
        | {f"alpha[{alto}]": float(h4[alto])})
lb_lp, viol = valuta(dl4, mano)
assert viol <= 1e-9, viol
print(f"  Duale a mano: beta = 0, gamma_bs = 1 solo per il libro piu' alto (il {alto + 1}, alto")
print(f"  {h4[alto]}) e alpha uguale a {h4[alto]} su quel libro, zero sugli altri. I vincoli")
print(f"  duali diventano {h4[alto]} <= {h4[alto]} e 0 <= 0  ->  lb = {frazione(lb_lp)}.")
print("  E' l'osservazione ovvia: lo scaffale che ospita il libro piu' alto e' alto almeno")
print(f"  quanto lui, quindi la somma delle altezze e' almeno {h4[alto]}.")
zlp4, zlp4r, _ = due_rilassamenti(m4mod, dl4)

# ---------- 4. UN BOUND COMBINATORIO PIU' FORTE ----------
intestazione("11.4 Il bound combinatorio: gli scaffali usati sono almeno due")
usati = -(-sum(w4) // c4)     # divisione intera per eccesso
print(f"  La larghezza totale e' {sum(w4)} e ogni scaffale ne regge {c4}: servono almeno")
print(f"  ceil({sum(w4)} / {c4}) = {usati} scaffali non vuoti.")
altre = sorted(h4[b] for b in R(n4) if b != alto)
lb4 = h4[alto] + min(altre)
print(f"  Uno di essi ospita il libro piu' alto e misura almeno {h4[alto]}; l'altro contiene")
print(f"  almeno un libro, quindi misura almeno {min(altre)}, la minima altezza restante.")
print(f"  lb = {h4[alto]} + {min(altre)} = {frazione(lb4)}, meglio del bound duale "
      f"{frazione(lb_lp)}.")
salva_dati(pd.DataFrame([{"argomento": "duale del rilassamento LP", "bound": lb_lp},
                         {"argomento": "scaffali usati e altezze minime", "bound": lb4}]),
           "scaffali4_argomento")

# ---------- 5. OTTIMO DEL MILP ----------
z4 = risolvi(m4mod)
for s in R(m4):
    libri = [b + 1 for b in R(n4) if x4[b, s].X > 0.5]
    largh = sum(w4[b] for b in R(n4) if x4[b, s].X > 0.5)
    print(f"  Scaffale {s + 1}: libri {libri}, larghezza {largh}/{c4}, altezza "
          f"{frazione(y4[s].X)}")
riga = registra_bound("4 scaffali", ub4, lb4, zlp4, zlp4r, z4)
salva_dati(pd.DataFrame([riga]), "scaffali4_bound")
assert lb4 <= z4 <= ub4 + 1e-9

# ---------- 6. DOMANDE DI MODELLAZIONE AGGIUNTIVE ----------
varianti = {}


def variante(nome, m):
    z = risolvi(m)
    print(f"  {nome:70s} z = {frazione(z)}")
    return z


# 4a: uno scaffale in piu'
m, x, y = modello_4(w4, h4, c4, 3)
varianti["4a"] = variante("4a. La biblioteca compra un terzo scaffale (m = 3)", m)
print("       l'ottimo non cambia: uno scaffale vuoto ha altezza zero e non costa nulla, ma")
print("       spezzare i libri su tre scaffali fa pagare tre altezze invece di due.")
# 4b: scaffali piu' larghi
m, x, y = modello_4(w4, h4, 12, m4)
varianti["4b"] = variante("4b. Gli scaffali sono larghi 12 invece di 10", m)
salva_dati(pd.DataFrame({"variante": list(varianti), "z": list(varianti.values())}),
           "scaffali4_varianti")

# ---------- 7. FIGURA ----------
fig, ax = plt.subplots(figsize=(6.4, 3.2))
for s in R(m4):
    sx = 0.0
    for b in R(n4):
        if x4[b, s].X > 0.5:
            ax.bar(sx + w4[b] / 2, h4[b], w4[b] * 0.92, bottom=s * 10, color=TEAL)
            ax.annotate(str(b + 1), (sx + w4[b] / 2, s * 10 + 1), ha="center", fontsize=8,
                        color="white")
            sx += w4[b]
    ax.plot([0, c4], [s * 10 + y4[s].X, s * 10 + y4[s].X], color=ARANCIO, lw=1.6)
    ax.annotate(f"altezza {frazione(y4[s].X)}", (c4 + 0.2, s * 10 + y4[s].X), fontsize=8,
                va="center", color=ARANCIO)
    ax.plot([c4, c4], [s * 10, s * 10 + 9], color=GRIGIO, ls="--", lw=1.2)
ax.set_xlim(0, c4 + 3.6)
ax.set_yticks([1, 11])
ax.set_yticklabels(["scaffale 1", "scaffale 2"])
ax.set_xlabel("larghezza")
ax.set_title(f"11.4: somma delle altezze {frazione(z4)}")
salva_figura(fig, "cap10_scaffali_ottimo")
print("Fine.")
