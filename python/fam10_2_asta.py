"""Problema 10.2 -- Asta combinatoria (set packing).

Un banditore ha n oggetti e riceve r offerte: l'offerta j chiede il sottoinsieme
B_j e paga p_j, e vale tutto o niente. E' il set packing puro: un vincolo per
oggetto, una variabile per offerta. Essendo un massimo, l'euristica da' il lower
bound e il duale a mano il bound superiore: i ruoli si scambiano rispetto a 10.1
e 10.2.
"""
import gurobipy as gp
import pandas as pd
from gurobipy import GRB

from mip import (ammissibile, due_rilassamenti, frazione, nuovo_modello, registra_bound,
                 risolvi, stampa_lp, valuta)
from stile import ARANCIO, GRIGIO, TEAL, intestazione, plt, salva_dati, salva_figura
from esteso import salva_modello

R = range

# ---------- 1. MODELLO E ISTANZA ----------
intestazione("10.2 Asta combinatoria: scegliere le offerte di profitto massimo")
n3 = 4                                                     # oggetti in vendita
B3 = [[0], [1], [2, 3], [0, 2], [1, 3], [0, 2, 3]]         # oggetti chiesti da ogni offerta
p3 = [6, 3, 12, 12, 10, 16]                                # profitto dell'offerta
r3 = len(p3)
salva_dati(pd.DataFrame({"offerta": [j + 1 for j in R(r3)],
                         "oggetti": ["{" + ",".join(str(i + 1) for i in B3[j]) + "}"
                                     for j in R(r3)],
                         "profitto": p3}), "fam10_2_dati")


def modello_3(n, B, p, extra=None):
    r = len(p)
    m = nuovo_modello("asta")
    x = m.addVars(r, vtype=GRB.BINARY, name="x")           # 1 se l'offerta e' accettata
    m.setObjective(gp.quicksum(p[j] * x[j] for j in R(r)), GRB.MAXIMIZE)
    m.addConstrs((gp.quicksum(x[j] for j in R(r) if i in B[j]) <= 1 for i in R(n)),
                 name="oggetto")
    return m, x


def duale_3(n, B, p):
    """min sum_i lam_i  s.t.  sum_{i in B_j} lam_i >= p_j per ogni offerta j, lam >= 0.

    Il duale ha una variabile per oggetto: lam_i e' il prezzo che il banditore
    attribuisce all'oggetto i, e ogni offerta deve costare almeno quanto paga.
    """
    r = len(p)
    dl = nuovo_modello("duale_asta")
    lam = dl.addVars(n, name="lam")
    dl.setObjective(gp.quicksum(lam[i] for i in R(n)), GRB.MINIMIZE)
    dl.addConstrs((gp.quicksum(lam[i] for i in B[j]) >= p[j] for j in R(r)), name="offerta")
    return dl, lam


m3, x3 = modello_3(n3, B3, p3)
salva_modello(m3, "fam10_2_primale")
print("  Il modello dell'istanza:")
stampa_lp(m3)

# ---------- 2. EURISTICA COSTRUTTIVA (LOWER BOUND) ----------
# euristica costruttiva sul profitto per oggetto: si accettano le offerte piu' redditizie fra
# quelle i cui oggetti sono ancora liberi. Costo O(r log r + r n).
def euristica(n, B, p):
    r = len(p)
    x = [0] * r
    libero = [True] * n
    passi = []
    for j in sorted(R(r), key=lambda j: (-p[j] / len(B[j]), j)):
        oggetti = "{" + ",".join(str(i + 1) for i in B[j]) + "}"
        occupati = [i + 1 for i in B[j] if not libero[i]]
        if occupati:
            passi.append(f"offerta {j + 1} {oggetti}, {p[j] / len(B[j]):.4g} per oggetto: "
                         f"scartata, gli oggetti {occupati} sono gia' venduti")
            continue
        x[j] = 1
        for i in B[j]:
            libero[i] = False
        passi.append(f"offerta {j + 1} {oggetti}, {p[j] / len(B[j]):.4g} per oggetto: "
                     f"accettata (profitto {p[j]})")
    return x, passi


x_eur, passi = euristica(n3, B3, p3)
for k, riga in enumerate(passi, 1):
    print(f"  Passo {k}. {riga}")
lb3 = sum(p3[j] * x_eur[j] for j in R(r3))
sol_eur = {f"x[{j}]": x_eur[j] for j in R(r3)}
assert ammissibile(m3, sol_eur), sol_eur
accettate = [j + 1 for j in R(r3) if x_eur[j]]
print(f"  Soluzione euristica: offerte {accettate}   lb = {frazione(lb3)}")

# ---------- 3. RILASSAMENTO LP E DUALE (UPPER BOUND) ----------
dl3, lam3 = duale_3(n3, B3, p3)
salva_modello(dl3, "fam10_2_duale")
# Ricetta a mano: si spalma ogni offerta sui suoi oggetti e si prende il massimo,
# lam_i = max_{j : i in B_j} p_j / |B_j|. E' sempre ammissibile perche' per ogni
# offerta j vale sum_{i in B_j} lam_i >= |B_j| * p_j / |B_j| = p_j.
mano = {f"lam[{i}]": max(p3[j] / len(B3[j]) for j in R(r3) if i in B3[j]) for i in R(n3)}
ub3, viol = valuta(dl3, mano)
assert viol <= 1e-9, viol
print("  Duale a mano: lam_i = max_{j : i in B_j} p_j / |B_j| (il profitto di ogni offerta")
print("  spalmato sui suoi oggetti; la somma su B_j vale allora almeno p_j):")
for i in R(n3):
    quote = ", ".join(f"{p3[j]}/{len(B3[j])}" for j in R(r3) if i in B3[j])
    print(f"    oggetto {i + 1}: max({quote}) = {frazione(mano[f'lam[{i}]'])}")
print(f"  ub = somma dei prezzi = {frazione(ub3)}")
# per confronto: la ricetta della dispensa di partenza, lam_i = max p_j sulle offerte
grezza = {f"lam[{i}]": max(p3[j] for j in R(r3) if i in B3[j]) for i in R(n3)}
ub_grezzo, viol_g = valuta(dl3, grezza)
assert viol_g <= 1e-9
print(f"  (con la ricetta piu' grossolana lam_i = max_j p_j si otterrebbe soltanto "
      f"{frazione(ub_grezzo)})")
zlp3, zlp3r, _ = due_rilassamenti(m3, dl3)

# ---------- 4. OTTIMO DEL MILP ----------
z3 = risolvi(m3)
ottime = [j + 1 for j in R(r3) if x3[j].X > 0.5]
venduti = sorted({i + 1 for j in R(r3) if x3[j].X > 0.5 for i in B3[j]})
print(f"  Soluzione ottima: offerte {ottime}, oggetti venduti {venduti}, profitto "
      f"{frazione(z3)}")
invenduti = [i + 1 for i in R(n3) if i + 1 not in venduti]
print(f"  Oggetti invenduti: {invenduti if invenduti else 'nessuno'}. Il banditore vende tutto,")
print("  ma non perche' un vincolo lo imponga: i vincoli sono <=, non =. Con altre offerte la")
print("  soluzione ottima potrebbe lasciare oggetti sullo scaffale.")
riga = registra_bound("3 asta", ub3, lb3, zlp3, zlp3r, z3, senso="max")
salva_dati(pd.DataFrame([riga]), "fam10_2_bound")
assert lb3 <= z3 <= zlp3r <= zlp3 <= ub3 + 1e-9

# ---------- 5. I DUE RILASSAMENTI E L'INTEREZZA ----------
intestazione("10.2 I due rilassamenti e l'interezza del rilassamento")
print(f"  z(LP) = {frazione(zlp3)} e z(LP+) = {frazione(zlp3r)} coincidono: i vincoli")
print("  sum_{j : i in B_j} x_j <= 1 implicano gia' x_j <= 1 per ogni offerta con B_j non")
print("  vuoto. Le disuguaglianze valide x_j <= 1 sono dunque ridondanti e non rafforzano.")
assert abs(zlp3 - zlp3r) <= 1e-9
print(f"  Su questa istanza si ha anche z(LP) = z(MILP) = {frazione(z3)}: il rilassamento")
print("  cade in un vertice intero. E' un caso fortunato dell'istanza, non una proprieta'")
print("  del set packing. Il controesempio minimo e' il triangolo: tre oggetti e tre offerte")
print("  che ne chiedono due ciascuna, tutte di profitto 1.")
m_tri, _ = modello_3(3, [[0, 1], [1, 2], [0, 2]], [1, 1, 1])
dl_tri, _ = duale_3(3, [[0, 1], [1, 2], [0, 2]], [1, 1, 1])
z_tri = risolvi(m_tri)
zlp_tri, zlp_tri_r, _ = due_rilassamenti(m_tri, dl_tri)
print(f"  Triangolo: z(LP) = {frazione(zlp_tri)} (x = 1/2 su tutte e tre) contro "
      f"z(MILP) = {frazione(z_tri)}.")
assert zlp_tri > z_tri + 1e-9
salva_dati(pd.DataFrame([{"istanza": "asta 10.2", "z_lp": zlp3, "z_milp": z3},
                         {"istanza": "triangolo", "z_lp": zlp_tri, "z_milp": z_tri}]),
           "fam10_2_triangolo")

# ---------- 6. DOMANDE DI MODELLAZIONE AGGIUNTIVE ----------
varianti = {}


def variante(nome, m):
    z = risolvi(m)
    print(f"  {nome:70s} z = {frazione(z)}")
    return z


# 3a: le offerte 4 e 5 vengono dallo stesso partecipante, che ne puo' vincere al piu' una
m, x = modello_3(n3, B3, p3)
m.addConstr(x[3] + x[4] <= 1, name="stesso_partecipante")
varianti["2a"] = variante("2a. Le offerte 4 e 5 sono dello stesso partecipante (x4+x5 <= 1)", m)
# 3b: il banditore consegna al piu' due oggetti in questa tornata
m, x = modello_3(n3, B3, p3)
m.addConstr(gp.quicksum(len(B3[j]) * x[j] for j in R(r3)) <= 2, name="consegne")
varianti["2b"] = variante("2b. Si consegnano al piu' due oggetti (sum_j |B_j| x_j <= 2)", m)
salva_dati(pd.DataFrame({"variante": list(varianti), "z": list(varianti.values())}),
           "fam10_2_varianti")

# ---------- 7. FIGURA ----------
fig, ax = plt.subplots(figsize=(6.8, 3.2))
idx = list(R(r3))
colori = [TEAL if x3[j].X > 0.5 else GRIGIO for j in idx]
ax.bar(idx, p3, 0.55, color=colori)
for j in idx:
    if x_eur[j]:
        ax.plot(j, p3[j] + 0.6, marker="v", color=ARANCIO, ms=8)
ax.plot([], [], marker="v", ls="", color=ARANCIO, label="scelta dall'euristica")
ax.bar([], [], color=TEAL, label="accettata all'ottimo")
ax.bar([], [], color=GRIGIO, label="rifiutata all'ottimo")
ax.set_xticks(idx)
ax.set_xticklabels(["{" + ",".join(str(i + 1) for i in B3[j]) + "}" for j in idx])
ax.set_xlabel("oggetti chiesti dall'offerta")
ax.set_ylabel("profitto")
ax.set_title(f"10.2: euristica {frazione(lb3)} <= ottimo {frazione(z3)} <= duale {frazione(ub3)}")
ax.legend(fontsize=8, loc="upper left")
salva_figura(fig, "cap10_asta_offerte")
print("Fine.")

# ---------- 5bis. IL SANDWICH SULLA VARIANTE 3b ----------
intestazione("10.2b Il sandwich sulla variante: al piu' due oggetti consegnati")
MAX_OGG = 2


def modello_3b(n, B, p, massimo=MAX_OGG):
    mm, xx = modello_3(n, B, p)
    mm.addConstr(gp.quicksum(len(B[j]) * xx[j] for j in R(len(p))) <= massimo, name="consegne")
    return mm, xx


def duale_3b(n, B, p, massimo=MAX_OGG):
    """Al duale di 10.2 si aggiunge mu >= 0 per il vincolo sum_j |B_j| x_j <= 2.
    Il termine noto e' 2, quindi mu entra nell'obiettivo, e nella colonna di
    ogni offerta compare moltiplicato per quanti oggetti quell'offerta chiede."""
    rr = len(p)
    dl = nuovo_modello("duale_asta_3b")
    lam = dl.addVars(n, name="lam")
    mu = dl.addVar(name="mu")
    dl.setObjective(lam.sum() + massimo * mu, GRB.MINIMIZE)
    dl.addConstrs((gp.quicksum(lam[i] for i in B[j]) + len(B[j]) * mu >= p[j] for j in R(rr)),
                  name="rc_x")
    return dl


m3b, x3b = modello_3b(n3, B3, p3)
salva_modello(m3b, "fam10_2b_primale")

# -- euristica ammissibile: si prende l'offerta migliore che non sfora i due oggetti --
print("Euristica costruttiva: le offerte in ordine di profitto decrescente; si accetta")
print("un'offerta se i suoi oggetti sono liberi e il totale consegnato resta entro due.")
presi, consegnati, valore_3b = set(), 0, 0
for j in sorted(R(r3), key=lambda j: -p3[j]):
    if consegnati + len(B3[j]) > MAX_OGG:
        continue
    if any(i in presi for i in B3[j]):
        continue
    presi |= set(B3[j])
    consegnati += len(B3[j])
    valore_3b += p3[j]
    print(f"  offerta {j + 1} (oggetti {sorted(i + 1 for i in B3[j])}, profitto {p3[j]}): "
          f"accettata, consegnati {consegnati}")
lb3b = valore_3b
accettate_3b = [j for j in R(r3) if set(B3[j]) <= presi and len(B3[j]) <= MAX_OGG]
sol_3b = {f"x[{j}]": 0 for j in R(r3)}
presi2, cons2 = set(), 0
for j in sorted(R(r3), key=lambda j: -p3[j]):
    if cons2 + len(B3[j]) <= MAX_OGG and not (set(B3[j]) & presi2):
        sol_3b[f"x[{j}]"] = 1
        presi2 |= set(B3[j]); cons2 += len(B3[j])
assert ammissibile(m3b, sol_3b), "la soluzione euristica della variante deve essere ammissibile"
print(f"  lb = {frazione(lb3b)}")

# -- certificato duale: mu si paga due volte e sconta ogni offerta --
dl3b = duale_3b(n3, B3, p3)
salva_modello(dl3b, "fam10_2b_duale")


def valore_duale_3b(mu_val):
    lam_v = {i: max([0.0] + [(p3[j] - len(B3[j]) * mu_val) / len(B3[j])
                             for j in R(r3) if i in B3[j]]) for i in R(n3)}
    return sum(lam_v.values()) + MAX_OGG * mu_val, lam_v


candidati_3b = sorted({0.0} | {p3[j] / len(B3[j]) for j in R(r3)})
scelto_3b = min(candidati_3b, key=lambda v: valore_duale_3b(v)[0])
ub3b, lam_3b = valore_duale_3b(scelto_3b)
mano_3b = {f"lam[{i}]": lam_3b[i] for i in R(n3)} | {"mu": scelto_3b}
ub3b_val, viol_3b = valuta(dl3b, mano_3b)
assert viol_3b <= 1e-9, (viol_3b, mano_3b)
print("Soluzione duale a mano: fissato mu, ogni offerta si spalma sui suoi oggetti al netto")
print("  di mu, e lam_i e' il massimo fra le offerte che chiedono l'oggetto i. Si prova mu")
print("  fra i profitti per oggetto delle offerte e si tiene il valore piu' basso:")
print(f"  mu = {frazione(scelto_3b)}, lam = {[frazione(lam_3b[i]) for i in R(n3)]}")
print(f"  ->  ub = {frazione(ub3b_val)}")
zlp3b, zlp3br, _ = due_rilassamenti(m3b, dl3b)
z3b = risolvi(m3b)
riga_3b = registra_bound("2b al piu' due oggetti", ub3b_val, lb3b, zlp3b, zlp3br, z3b, senso="max")
salva_dati(pd.DataFrame([riga_3b]), "fam10_2b_bound")
assert lb3b <= z3b <= zlp3b + 1e-9 <= ub3b_val + 1e-9

