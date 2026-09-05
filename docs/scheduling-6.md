# Classi con premio di completamento e riduzione «se e solo se»

**Classe:** BIP · **Legami:** se e solo se (due), CNF · **Script:** `python/fam07_6_classipremio.py`

[![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/fam07_6_classipremio.ipynb)

!!! abstract "Problema 7.6"
    Un'azienda ha $n$ lavori eseguibili su una macchina con disponibilità $a$.
    Per ogni lavoro $j$, $t_j$ è il tempo e $r_j$ il ricavo. I lavori sono
    partizionati in $q \ge 2$ classi. La disponibilità si riduce di $u > 0$ minuti
    *se e solo se* la macchina esegue lavori di almeno due classi diverse. Per ogni
    classe $c$ si ottiene un ricavo extra $v_c > 0$ *se e solo se* tutti i lavori
    della classe sono eseguiti. Massimizzare il ricavo totale.

**Il problema a parole.** Due «se e solo se»: uno premia (il completamento),
uno penalizza (la mescolanza). Di ciascuno basta imporre un verso: l'altro lo
impone l'obiettivo.

## Modello

**Variabili.** $n + q + 1$ binarie: $x_j$ (lavoro eseguito), $y_c$ (classe
completa), $z$ (lavori di almeno due classi).

$$
\begin{aligned}
\max ~~ \sum_{j=1}^{n} r_j\, x_j + \sum_{c=1}^{q} v_c\, y_c & & \\
\text{soggetto a} \quad x_j - y_c &\ge 0, & \forall c,\ \forall j \in \mathscr{J}_c, \\
x_j + x_i - z &\le 1, & \forall c < g,\ \forall j \in \mathscr{J}_c,\ \forall i \in \mathscr{J}_g, \\
\sum_{j=1}^{n} t_j\, x_j + u\, z &\le a, & \\
x_j,\ y_c,\ z &\in \{0, 1\}. &
\end{aligned}
$$

- l'obiettivo massimizza ricavi dei lavori più premi delle classi complete;
- i vincoli **tutti**: se una classe è dichiarata completa, tutti i suoi lavori
  sono eseguiti ($n$ vincoli);
- i vincoli **miste**: se si eseguono due lavori di classi diverse, $z = 1$
  ($\sum_{c<g} |\mathscr{J}_c|\,|\mathscr{J}_g|$ vincoli);
- il vincolo di **disponibilità** con la riduzione $u z$ ($1$ vincolo);
- i vincoli di dominio.

!!! note "Legame fra le variabili: quattro implicazioni"
    **$y_c$, dal vincolo.** $y_c \Rightarrow (x_j \,\mathtt{AND}\, x_i \,\mathtt{AND}\, \dots)$:
    l'espressione $(x_j \,\mathtt{AND}\, \dots) \,\mathtt{OR}\, \mathtt{NOT}\,y_c$ diventa
    per distributività la CNF $(x_j \,\mathtt{OR}\, \mathtt{NOT}\,y_c) \,\mathtt{AND}\, \dots$,
    cioè $x_j \ge y_c$. **$y_c$, dall'ottimo.** Se tutti i lavori sono
    eseguiti allora $y_c = 1$: porre $y_c = 1$ resta ammissibile e aumenta
    l'obiettivo di $v_c > 0$.

    **$z$, dal vincolo.** $x_j \,\mathtt{AND}\, x_i \Rightarrow z$ per ogni coppia
    mista: De Morgan dà $\mathtt{NOT}\,x_j \,\mathtt{OR}\, \mathtt{NOT}\,x_i \,\mathtt{OR}\, z$,
    cioè $x_j + x_i - z \le 1$. **$z$, dall'ottimo.** Se i lavori eseguiti
    stanno in una sola classe, $z = 0$: porre $z = 0$ resta ammissibile, libera
    $u$ minuti e non cambia l'obiettivo (dove $z$ non compare) — «esiste un
    ottimo», non «in ogni ottimo».

## Il modello in gurobipy

```python
coppie = [(j, i) for c in range(q) for g in range(c + 1, q) for j in J[c] for i in J[g]]
m = gp.Model("classi_premio");  m.Params.OutputFlag = 0
x = m.addVars(n, vtype=GRB.BINARY, name="x")
y = m.addVars(q, vtype=GRB.BINARY, name="y")
z = m.addVar(vtype=GRB.BINARY, name="z")
m.setObjective(gp.quicksum(r[j] * x[j] for j in range(n))
               + gp.quicksum(v[c] * y[c] for c in range(q)), GRB.MAXIMIZE)
m.addConstrs((x[j] - y[c] >= 0 for c in range(q) for j in J[c]), name="tutti")
m.addConstrs((x[j] + x[i] - z <= 1 for (j, i) in coppie), name="miste")
m.addConstr(gp.quicksum(t[j] * x[j] for j in range(n)) + u * z <= a, name="disponibilita")
m.optimize()
```

## L'istanza

$n = 6$, $q = 3$: $\mathscr{J}_1 = \{1, 2\}$, $\mathscr{J}_2 = \{3, 4\}$,
$\mathscr{J}_3 = \{5, 6\}$, $a = 50$, $u = 10$.

| | $j=1$ | $j=2$ | $j=3$ | $j=4$ | $j=5$ | $j=6$ |
|---|---:|---:|---:|---:|---:|---:|
| $r_j$ | 10 | 5 | 20 | 12 | 10 | 22 |
| $t_j$ | 5 | 15 | 25 | 15 | 10 | 38 |

| | $c=1$ | $c=2$ | $c=3$ |
|---|---:|---:|---:|
| $v_c$ | 5 | 4 | 10 |

## Euristica costruttiva: il bound primale

Classe per classe; dalla seconda classe il primo lavoro paga anche $u$.

- **Passi 1–2.** Classe 1: $x[1] = x[2] = 1$, $ra = 30$; classe completa, $y[1] = 1$.
- **Passo 3.** Classe 2: $t_3 + u = 35 > 30$, saltato. **Passo 4.**
  $t_4 + u = 25 \le 30$: $x[4] = 1$, $z = 1$, $ra = 5$.
- **Passi 5–6.** Classe 3: $t_5, t_6 > 5$, saltati.

Ricavo $10 + 5 + 12 + 5 = 32$: $z(\mathit{MILP}) \ge 32$.

## Rilassamento LP e duale: il bound duale

Con $\pi_j \le 0$ (tutti), $\lambda_{ji} \ge 0$ (miste), $\mu \ge 0$
(disponibilità):

$$
\begin{aligned}
\min ~~ \sum_{\text{coppie miste}} \lambda_{ji} + a\, \mu & & \\
\text{soggetto a} \quad \pi_j + \sum_{i \notin \mathscr{J}_c} \lambda_{ji} + t_j\, \mu &\ge r_j, & \forall c,\ \forall j \in \mathscr{J}_c, \\
-\sum_{j \in \mathscr{J}_c} \pi_j &\ge v_c, & \forall c, \\
-\sum_{\text{coppie miste}} \lambda_{ji} + u\, \mu &\ge 0. &
\end{aligned}
$$

**Una soluzione duale a mano.** Il premio di ogni classe caricato su un solo
lavoro: $\bar\pi_1 = -5$, $\bar\pi_3 = -4$, $\bar\pi_5 = -10$; $\bar\lambda = 0$;
$\bar\mu = \max_j (r_j - \bar\pi_j)/t_j = \max\{3, \tfrac{1}{3}, \tfrac{24}{25}, \tfrac{4}{5}, 2, \tfrac{11}{19}\} = 3$;
valore $150$: $32 \le z(\mathit{MILP}) \le 150$.

**Quello che dice il solver.** $z(\mathit{LP}) = 5280/113 = 46{,}7$. Ottimo
intero $42$: la sola classe 3 completa, lavori 5 e 6 ($48 \le 50$, $z = 0$),
ricavo $10 + 22 + 10$. Gap dell'euristica $24\%$.

| $LB$ | $UB$ (duale a mano) | $z(\mathit{LP})$ | $z(\mathit{MILP})$ | gap euristica |
|---:|---:|---:|---:|---:|
| 32 | 150 | $5280/113$ | 42 | $23{,}8\%$ |

## Considerazioni aggiuntive

- Il verso di ottimalità per $y_c$ si impone con
  $\sum_{j \in \mathscr{J}_c} x_j - y_c \le |\mathscr{J}_c| - 1$ ($q$ vincoli che
  preservano l'ottimo, non validi).
- Il verso di ottimalità per $z$: $z \le \sum_{j \notin \mathscr{J}_c} x_j$ per
  ogni $c$.
- Una forma aggregata con variabili di classe $w_c \ge x_j$ e
  $\sum_c w_c - 1 \le (q-1) z$ sostituisce le coppie: stesso insieme intero,
  rilassamento diverso.

## Domande di modellazione aggiuntive

??? question "7.6.1 — Almeno un lavoro per classe"
    Eseguire almeno un lavoro di ogni classe. Che succede a $z$?

    !!! tip "Soluzione"
        La soluzione è nel documento delle soluzioni, riservato ai docenti.
??? question "7.6.2 — Penalità per classe iniziata e non finita"
    Iniziare una classe senza completarla costa $w = 3$.

    !!! tip "Soluzione"
        La soluzione è nel documento delle soluzioni, riservato ai docenti.
## Codice

Script completo: [`python/fam07_6_classipremio.py`](https://github.com/fabiofurini/modellazione-mip/blob/main/python/fam07_6_classipremio.py);
notebook: [`notebooks/fam07_6_classipremio.ipynb`](https://github.com/fabiofurini/modellazione-mip/blob/main/notebooks/fam07_6_classipremio.ipynb).

<!-- script-incorporato: inizio (rigenerato da python/incorpora_codice.py) -->

??? example "Mostra lo script completo — `python/fam07_6_classipremio.py` (146 righe)"

    ```python
    """Problema 7.6 -- Classi con premio di completamento e riduzione se e solo se.

    Due "se e solo se": ognuno con un verso imposto dal vincolo (via CNF) e
    l'altro dall'ottimo -- lo schema generale per modellare un iff.
    """
    import gurobipy as gp
    import numpy as np
    import pandas as pd
    from gurobipy import GRB

    from euristiche import best_fit, first_fit, matrice, next_fit
    from mip import (ammissibile, due_rilassamenti, frazione, nuovo_modello,
                     registra_bound, risolvi, stampa_soluzione, valuta)
    from stile import CICLO, ROSSO, intestazione, plt, salva_dati, salva_figura

    R = range

    # ---------- 1. MODELLO E ISTANZA ----------
    intestazione("6. Premio se tutta la classe è eseguita; riduzione u se e solo se >= 2 classi")
    r6 = [10, 5, 20, 12, 10, 22]
    t6 = [5, 15, 25, 15, 10, 38]
    J6 = [[0, 1], [2, 3], [4, 5]]
    v6 = [5, 4, 10]
    a6, u6 = 50, 10
    salva_dati(pd.DataFrame({"lavoro": R(1, 7), "r": r6, "t": t6,
                             "classe": [c + 1 for j in R(6) for c in R(3) if j in J6[c]]}), "sched6_lavori")
    salva_dati(pd.DataFrame({"classe": R(1, 4), "v": v6}), "sched6_classi")


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

    # ---------- 2. EURISTICA COSTRUTTIVA (LOWER BOUND) ----------
    xe, ye, ze, passi = euristica_6(r6, t6, J6, v6, a6, u6)
    print("Euristica classe per classe:")
    for i, s in enumerate(passi, 1):
        print(f"  Passo {i}. {s}")
    lb6 = sum(r6[j] * xe[j] for j in R(6)) + sum(v6[c] * ye[c] for c in R(3))
    print(f"  lb = {lb6}  (x = {xe}, y = {ye}, z = {ze})")

    # ---------- 3. RILASSAMENTO LP E DUALE (UPPER BOUND) ----------
    d6 = duale_6(r6, t6, J6, v6, a6, u6)
    pi_mano = {f"pi[{J6[c][0]}]": -v6[c] for c in R(3)}      # il primo lavoro di ogni classe porta il premio
    mu_mano = max((r6[j] - pi_mano.get(f"pi[{j}]", 0)) / t6[j] for j in R(6))
    mano = dict(pi_mano, mu=mu_mano)
    ub6, viol = valuta(d6, mano)
    assert viol <= 1e-9
    print(f"Soluzione duale a mano: pi_1 = -5, pi_3 = -4, pi_5 = -10, lam = 0, "
          f"mu = max_j (r_j - pi_j)/t_j = {frazione(mu_mano)}  ->  ub = {frazione(ub6)}")
    zlp6, zlp6r, _ = due_rilassamenti(m6, d6)

    # ---------- 4. SOLUZIONE OTTIMA DEL MILP ----------
    z6v = risolvi(m6)
    print("Soluzione ottima del MILP:")
    stampa_soluzione(m6, solo_non_nulle=True)
    riga = registra_bound("6 classi premio", ub6, lb6, zlp6, zlp6r, z6v, senso="max")
    salva_dati(pd.DataFrame([riga]), "sched6_bound")

    # ---------- 5. DOMANDE DI MODELLAZIONE AGGIUNTIVE ----------


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
    salva_dati(pd.DataFrame({"variante": list(varianti), "z": list(varianti.values())}), "sched6_varianti")

    print("Fine.")
    ```

<!-- script-incorporato: fine -->
