"""Problema 7.6 -- Classi con premio di completamento e riduzione se e solo se.

Due "se e solo se": ognuno con un verso imposto dal vincolo (via CNF) e
l'altro dall'ottimo -- lo schema generale per modellare un iff.
"""
import gurobipy as gp
import numpy as np
import pandas as pd
from gurobipy import GRB

from euristiche import best_fit, first_fit, matrice, next_fit
from mip import (ammissibile, dualita_forte, due_rilassamenti, frazione,
                 nuovo_modello, registra_bound, rilassamenti, risolvi,
                 stampa_soluzione, valuta)
from stile import CICLO, ROSSO, intestazione, plt, salva_dati, salva_figura
from esteso import salva_modello

R = range

# ---------- 1. MODELLO E ISTANZA ----------
intestazione("6. Premio se tutta la classe è eseguita; riduzione u se e solo se >= 2 classi")
r6 = [10, 5, 20, 12, 10, 22]
t6 = [5, 15, 25, 15, 10, 38]
J6 = [[0, 1], [2, 3], [4, 5]]
v6 = [5, 4, 10]
a6, u6 = 50, 10
salva_dati(pd.DataFrame({"lavoro": R(1, 7), "r": r6, "t": t6,
                         "classe": [c + 1 for j in R(6) for c in R(3) if j in J6[c]]}), "fam07_6_lavori")
salva_dati(pd.DataFrame({"classe": R(1, 4), "v": v6}), "fam07_6_classi")


def coppie(J):
    return [(j, i, c, g) for c in R(len(J)) for g in R(c + 1, len(J)) for j in J[c] for i in J[g]]


def modello_6(r, t, J, v, a, u):
    n, q = len(r), len(J)
    m = nuovo_modello("classi_premio")
    x = m.addVars(n, vtype=GRB.BINARY, name="x")
    y = m.addVars(q, vtype=GRB.BINARY, name="y")
    z = m.addVar(vtype=GRB.BINARY, name="z")
    m.setObjective(gp.quicksum(r[j] * x[j] for j in R(n)) + gp.quicksum(v[c] * y[c] for c in R(q)),
                   GRB.MAXIMIZE)
    m.addConstrs((x[j] - y[c] >= 0 for c in R(q) for j in J[c]), name="tutti")
    m.addConstrs((x[j] + x[i] - z <= 1 for (j, i, c, g) in coppie(J)), name="miste")
    m.addConstr(gp.quicksum(t[j] * x[j] for j in R(n)) + u * z <= a, name="disponibilita")
    return m, x, y, z


def duale_6(r, t, J, v, a, u):
    """min sum lam_ji + a mu;  pi_j + sum lam + t_j mu >= r_j;  -sum_{J_c} pi_j >= v_c;
    -sum lam + u mu >= 0;  pi <= 0, lam >= 0, mu >= 0."""
    n, q = len(r), len(J)
    cp = coppie(J)
    d = nuovo_modello("duale_classi_premio")
    pi = d.addVars(n, lb=-GRB.INFINITY, ub=0.0, name="pi")
    lam = d.addVars([(j, i) for (j, i, _, _) in cp], name="lam")
    mu = d.addVar(name="mu")
    d.setObjective(lam.sum() + a * mu, GRB.MINIMIZE)
    for j in R(n):
        d.addConstr(pi[j] + gp.quicksum(lam[jj, ii] for (jj, ii, _, _) in cp if jj == j or ii == j)
                    + t[j] * mu >= r[j], name=f"rc_x[{j}]")
    d.addConstrs((-gp.quicksum(pi[j] for j in J[c]) >= v[c] for c in R(q)), name="rc_y")
    d.addConstr(-lam.sum() + u * mu >= 0, name="rc_z")
    return d


def euristica_6(r, t, J, v, a, u):
    """Classe per classe: dalla seconda classe in poi il primo lavoro paga anche la riduzione u."""
    n, q = len(r), len(J)
    x, y, z, ra, passi = [0] * n, [0] * q, 0, a, []
    for c in R(q):
        cnt = 0
        for j in J[c]:
            if c == 0 or z == 1:
                if t[j] <= ra:
                    x[j], ra, cnt = 1, ra - t[j], cnt + 1
                    passi.append(f"Classe {c + 1}: t[{j + 1}] = {t[j]} <= ra; x[{j + 1}] = 1, ra = {ra}.")
                else:
                    passi.append(f"Classe {c + 1}: t[{j + 1}] = {t[j]} > ra = {ra}; il lavoro {j + 1} viene saltato.")
            else:
                if t[j] + u <= ra:
                    x[j], z, ra, cnt = 1, 1, ra - t[j] - u, cnt + 1
                    passi.append(f"Classe {c + 1}, riduzione non ancora applicata: t[{j + 1}] + u = {t[j] + u} <= ra; "
                                 f"x[{j + 1}] = 1, z = 1, ra = {ra}.")
                else:
                    passi.append(f"Classe {c + 1}, riduzione non ancora applicata: t[{j + 1}] + u = {t[j] + u} > ra = {ra}; "
                                 f"il lavoro {j + 1} viene saltato.")
        if cnt == len(J[c]):
            y[c] = 1
            passi.append(f"Tutti i lavori della classe {c + 1} sono eseguiti: y[{c + 1}] = 1 (premio v = {v[c]}).")
    return x, y, z, passi


m6, x6, y6, z6 = modello_6(r6, t6, J6, v6, a6, u6)
salva_modello(m6, "fam07_6_primale")

# ---------- 2. IL RILASSAMENTO LP ----------
zlp6, zlp6r, _ = rilassamenti(m6)

# ---------- 3. IL DUALE DEL RILASSAMENTO (LOWER BOUND) ----------
d6 = duale_6(r6, t6, J6, v6, a6, u6)
salva_modello(d6, "fam07_6_duale")
pi_mano = {f"pi[{J6[c][0]}]": -v6[c] for c in R(3)}      # il primo lavoro di ogni classe porta il premio
mu_mano = max((r6[j] - pi_mano.get(f"pi[{j}]", 0)) / t6[j] for j in R(6))
mano = dict(pi_mano, mu=mu_mano)
ub6, viol = valuta(d6, mano)
assert viol <= 1e-9
print(f"Soluzione duale a mano: pi_1 = -5, pi_3 = -4, pi_5 = -10, lam = 0, "
      f"mu = max_j (r_j - pi_j)/t_j = {frazione(mu_mano)}  ->  ub = {frazione(ub6)}")
dualita_forte(d6, zlp6)

# ---------- 4. EURISTICA COSTRUTTIVA (UPPER BOUND) ----------
xe, ye, ze, passi = euristica_6(r6, t6, J6, v6, a6, u6)
print("Euristica classe per classe:")
for i, s in enumerate(passi, 1):
    print(f"  Passo {i}. {s}")
lb6 = sum(r6[j] * xe[j] for j in R(6)) + sum(v6[c] * ye[c] for c in R(3))
print(f"  lb = {lb6}  (x = {xe}, y = {ye}, z = {ze})")

# ---------- 5. SOLUZIONE OTTIMA DEL MILP ----------
z6v = risolvi(m6)
print("Soluzione ottima del MILP:")
stampa_soluzione(m6, solo_non_nulle=True)
riga = registra_bound("6 classi premio", ub6, lb6, zlp6, zlp6r, z6v, senso="max")
salva_dati(pd.DataFrame([riga]), "fam07_6_bound")

# ---------- 6. DOMANDE DI MODELLAZIONE AGGIUNTIVE ----------


varianti = {}


def variante(nome, m):
    z = risolvi(m)
    print(f"  {nome:70s} z = {frazione(z)}")
    return z

# 6a: almeno un lavoro per classe
m, x, y, z = modello_6(r6, t6, J6, v6, a6, u6)
m.addConstrs((gp.quicksum(x[j] for j in J6[c]) >= 1 for c in R(3)), name="almeno_uno")
varianti["6a"] = variante("6a. Almeno un lavoro per classe (quindi z = 1)", m)
# 6b: penalità w per classe iniziata e non completata
w6 = 3
m, x, y, z = modello_6(r6, t6, J6, v6, a6, u6)
st = m.addVars(3, vtype=GRB.BINARY, name="s")
m.addConstrs((st[c] >= x[j] for c in R(3) for j in J6[c]), name="iniziata")
m.update()
m.setObjective(m.getObjective() - w6 * gp.quicksum(st[c] - y[c] for c in R(3)), GRB.MAXIMIZE)
varianti["6b"] = variante("6b. Penalità 3 per classe iniziata e non completata (s_c >= x_j)", m)
salva_dati(pd.DataFrame({"variante": list(varianti), "z": list(varianti.values())}), "fam07_6_varianti")

# ---------- 7. IL SANDWICH SULLA VARIANTE 6a ----------
intestazione("6a. Il sandwich sulla variante: almeno un lavoro per classe")


def modello_6a(r, t, J, v, a, u):
    mm_, xx, yy, zz = modello_6(r, t, J, v, a, u)
    mm_.addConstrs((gp.quicksum(xx[j] for j in J[c]) >= 1 for c in R(len(J))), name="almeno_uno")
    return mm_, xx, yy, zz


def duale_6a(r, t, J, v, a, u):
    """Al duale di 7.6 si aggiunge omega_c <= 0 per ogni vincolo
    sum_{j in J_c} x_j >= 1 (verso >= in un massimo). Il termine noto e' 1,
    quindi omega entra nell'obiettivo --- e, essendo non positivo, lo abbassa."""
    nn, q = len(r), len(J)
    cp = coppie(J)
    d = nuovo_modello("duale_classi_premio_6a")
    pi = d.addVars(nn, lb=-GRB.INFINITY, ub=0.0, name="pi")
    lam = d.addVars([(j, i) for (j, i, _, _) in cp], name="lam")
    mu = d.addVar(name="mu")
    om = d.addVars(q, lb=-GRB.INFINITY, ub=0.0, name="omega")
    d.setObjective(lam.sum() + a * mu + om.sum(), GRB.MINIMIZE)
    for c in R(q):
        for j in J[c]:
            d.addConstr(pi[j] + gp.quicksum(lam[jj, ii] for (jj, ii, _, _) in cp
                                            if jj == j or ii == j)
                        + t[j] * mu + om[c] >= r[j], name=f"rc_x[{j}]")
    d.addConstrs((-gp.quicksum(pi[j] for j in J[c]) >= v[c] for c in R(q)), name="rc_y")
    d.addConstr(-lam.sum() + u * mu >= 0, name="rc_z")
    return d


m6a, x6a, y6a, z6a = modello_6a(r6, t6, J6, v6, a6, u6)
salva_modello(m6a, "fam07_6a_primale")

# -- euristica ammissibile: la base, riparata aggiungendo il lavoro mancante --
print("Euristica costruttiva: il vincolo nuovo obbliga ogni classe, quindi si parte dal")
print("lavoro piu' corto di ciascuna classe --- cosi' la soluzione e' ammissibile per")
print("costruzione --- e poi si aggiungono gli altri per rapporto r_j/t_j decrescente.")


def tempo_6a(scelti):
    """Il tempo speso: i lavori piu' la riduzione u, che scatta con due classi."""
    classi = {c for c in R(3) for j in J6[c] if j in scelti}
    return sum(t6[j] for j in scelti) + (u6 if len(classi) >= 2 else 0)


scelti_6a = [min(J6[c], key=lambda j: t6[j]) for c in R(3)]
print(f"  un lavoro per classe: {sorted(j + 1 for j in scelti_6a)}, "
      f"tempo {tempo_6a(scelti_6a)} su {a6}")
for j in sorted(set(R(6)) - set(scelti_6a), key=lambda j: -r6[j] / t6[j]):
    if tempo_6a(scelti_6a + [j]) <= a6:
        scelti_6a.append(j)
        print(f"  entra anche il lavoro {j + 1}, tempo {tempo_6a(scelti_6a)}")
y_6a = [1 if all(j in scelti_6a for j in J6[c]) else 0 for c in R(3)]
z_6a = 1 if len({c for c in R(3) if any(j in scelti_6a for j in J6[c])}) >= 2 else 0
lb6a = sum(r6[j] for j in scelti_6a) + sum(v6[c] * y_6a[c] for c in R(3))
sol_6a = ({f"x[{j}]": 1 for j in scelti_6a}
          | {f"y[{c}]": y_6a[c] for c in R(3)} | {"z": z_6a})
assert ammissibile(m6a, sol_6a), "la soluzione euristica della variante deve essere ammissibile"
print(f"  lavori {sorted(j + 1 for j in scelti_6a)}  ->  lb = {frazione(lb6a)}")

# -- certificato duale: omega sconta ogni classe --
d6a = duale_6a(r6, t6, J6, v6, a6, u6)
salva_modello(d6a, "fam07_6a_duale")
pi_6a = {f"pi[{J6[c][0]}]": -v6[c] for c in R(3)}
mu_6a = max((r6[j] - pi_6a.get(f"pi[{j}]", 0)) / t6[j] for j in R(6))
om_6a = {c: min(0.0, max(r6[j] - pi_6a.get(f"pi[{j}]", 0) - t6[j] * mu_6a for j in J6[c]))
         for c in R(3)}
mano_6a = dict(pi_6a, mu=mu_6a) | {f"omega[{c}]": om_6a[c] for c in R(3)}
ub6a, viol_6a = valuta(d6a, mano_6a)
assert viol_6a <= 1e-9, viol_6a
print("Soluzione duale a mano: pi e mu come nel problema base; poi si abbassa omega_c fin")
print("  dove le colonne della classe c lo permettono, cioe'")
print("  omega_c = max_{j in J_c} (r_j - pi_j - t_j mu), che e' non positivo.")
print(f"  omega = {[frazione(om_6a[c]) for c in R(3)]}")
print(f"  ->  ub = {frazione(ub6a)}  (con omega = 0 si avrebbe {frazione(a6 * mu_6a)})")
zlp6a, zlp6ar, _ = due_rilassamenti(m6a, d6a)
z6a_val = risolvi(m6a)
riga_6a = registra_bound("6a almeno un lavoro per classe", ub6a, lb6a, zlp6a, zlp6ar, z6a_val,
                         senso="max")
salva_dati(pd.DataFrame([riga_6a]), "fam07_6a_bound")
assert lb6a <= z6a_val <= zlp6a + 1e-9 <= ub6a + 1e-9


print("Fine.")
