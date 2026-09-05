# Lavori in parallelo: il tempo di lavorazione come massimo

**Classe:** MILP · **Legami:** variabile di massimo · **Script:** `python/fam07_4_parallelo.py`

[![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/fam07_4_parallelo.ipynb)

!!! abstract "Problema 7.4"
    Un'azienda deve eseguire $n$ lavori con $k$ macchine. Per ogni lavoro $j$ e
    macchina $m$, $t_{jm} \in \mathbb{Q}_{>0}$ è il tempo di lavorazione. Ogni
    macchina $m$ può eseguire al più $p_m \in \mathbb{Z}_{\ge 1}$ lavori, in
    parallelo: tutti i lavori assegnati alla stessa macchina partono insieme.
    Minimizzare la somma dei tempi di lavorazione delle macchine, dove il tempo di
    una macchina è il tempo del lavoro più lungo fra quelli assegnati.

**Il problema a parole.** *Decidiamo* su quale macchina va ogni lavoro.
*L'obiettivo*: somma dei tempi di lavorazione delle macchine, ciascuno pari al
**massimo** dei tempi dei lavori assegnati. *I vincoli*: ogni lavoro a una
macchina; al più $p_m$ lavori sulla macchina $m$. Un massimo non è lineare, ma
si linearizza con una variabile continua e $n$ vincoli «$\ge$» per macchina.

## Modello

| Simbolo | Tipo | Significato |
|---|---|---|
| $n$ | $\in \mathbb{Z}_{\ge 1}$ | numero di lavori |
| $k$ | $\in \mathbb{Z}_{\ge 1}$ | numero di macchine |
| $t_{jm}$ | $\in \mathbb{Q}_{>0}$ | tempo del lavoro $j$ sulla macchina $m$ |
| $p_m$ | $\in \mathbb{Z}_{\ge 1}$ | numero massimo di lavori sulla macchina $m$ |

**Variabili.** $n\,k$ binarie $x_{jm}$ (lavoro $j$ sulla macchina $m$) e $k$
continue non negative $y_m$ = tempo di lavorazione della macchina $m$.

$$
\begin{aligned}
\min ~~ \sum_{m=1}^{k} y_m & & \\
\text{soggetto a} \quad \sum_{m=1}^{k} x_{jm} &= 1, & \forall j, \\
\sum_{j=1}^{n} x_{jm} &\le p_m, & \forall m, \\
-t_{jm}\, x_{jm} + y_m &\ge 0, & \forall j,\ \forall m, \\
x_{jm} \in \{0, 1\},\quad y_m &\ge 0. &
\end{aligned}
$$

- l'obiettivo minimizza la somma dei tempi di lavorazione;
- i vincoli di **assegnamento** ($n$) e di **cardinalità** ($k$);
- i vincoli di **massimo** collegano assegnamenti e tempi: se il lavoro $j$ è
  sulla macchina $m$, il tempo della macchina è almeno $t_{jm}$ ($n\,k$ vincoli
  lineari);
- i vincoli di dominio definiscono le variabili.

!!! note "Legame fra le variabili: la variabile di massimo in tre passi"
    1. **Dal vincolo.** $x_{jm} = 1 \Rightarrow y_m \ge t_{jm}$ e, per
       contronominale, $y_m < t_{jm} \Rightarrow x_{jm} = 0$: il vincolo dà
       $y_m \ge t_{jm} x_{jm}$; se $x_{jm} = 1$, $y_m \ge t_{jm}$; se
       $y_m < t_{jm}$, $x_{jm}$ non può valere $1$. Valendo per ogni $j$:
       $y_m \ge \max_j t_{jm} x_{jm}$.
    2. **Dall'ottimo.** $\sum_j x_{jm} = 0 \Rightarrow y_m = 0$: non imposta dai
       vincoli (si riducono a $y_m \ge 0$), segue dall'obiettivo perché $y_m$ ha
       coefficiente $1 > 0$: abbassarla a $0$ resta ammissibile e riduce
       l'obiettivo.
    3. **Sintesi.** In ogni ottimo $y_m = \max_j t_{jm} x_{jm}$: se $y_m$
       superasse il massimo, porla uguale al massimo manterrebbe tutti i
       vincoli e ridurrebbe l'obiettivo.

## Il modello in gurobipy

```python
m = gp.Model("parallelo");  m.Params.OutputFlag = 0
x = m.addVars(n, k, vtype=GRB.BINARY, name="x")
y = m.addVars(k, name="y")                                   # continue, >= 0
m.setObjective(y.sum(), GRB.MINIMIZE)
m.addConstrs((x.sum(j, "*") == 1 for j in range(n)), name="assegna")
m.addConstrs((x.sum("*", mm) <= p[mm] for mm in range(k)), name="cardinalita")
m.addConstrs((-t[j][mm] * x[j, mm] + y[mm] >= 0
              for j in range(n) for mm in range(k)), name="massimo")
m.optimize()
```

## L'istanza

| $t_{jm}$ | $m=1$ | $m=2$ | $m=3$ |
|---|---:|---:|---:|
| $j=1$ | 6 | 5 | 3 |
| $j=2$ | 5 | 10 | 2 |
| $j=3$ | 20 | 13 | 10 |

| | $m=1$ | $m=2$ | $m=3$ |
|---|---:|---:|---:|
| $p_m$ | 1 | 2 | 2 |

## Euristica costruttiva: il bound primale

Next-fit sulle cardinalità: si riempie la macchina 1 fino a $p_1$ lavori, poi la
2, e così via.

- **Passo 1.** Lavoro 1 sulla macchina 1: $y[1] = 6$.
- **Passo 2.** La macchina 1 è piena ($p_1 = 1$): lavoro 2 sulla macchina 2,
  $y[2] = 10$.
- **Passo 3.** Lavoro 3 sulla macchina 2: $y[2] = \max(10, 13) = 13$.

$\bar y = (6, 13, 0)$, valore $19$: $z(\mathrm{MILP}) \le 19$.

## Rilassamento LP e duale: il bound duale

Con $\mu_j$ libere (assegnamento), $\pi_m \le 0$ (cardinalità) e
$\lambda_{jm} \ge 0$ (massimo):

$$
\begin{aligned}
\max ~~ \sum_{j=1}^{n} \mu_j + \sum_{m=1}^{k} p_m\, \pi_m & & \\
\text{soggetto a} \quad \mu_j + \pi_m - t_{jm}\, \lambda_{jm} &\le 0, & \forall j,\ \forall m, \\
\sum_{j=1}^{n} \lambda_{jm} &\le 1, & \forall m, \\
\mu_j \gtreqless 0,\quad \pi_m \le 0,\quad \lambda_{jm} &\ge 0. &
\end{aligned}
$$

Il secondo vincolo è il costo ridotto di $y_m$: il coefficiente $1$
nell'obiettivo primale limita la somma dei $\lambda_{jm}$.

**Una soluzione duale a mano.** $\bar\lambda_{jm} = 1/3$, $\bar\pi_m = 0$,
$\bar\mu_j = \min_m t_{jm}/3$: $1, \tfrac{2}{3}, \tfrac{10}{3}$, valore $5$:
$5 \le z(\mathrm{MILP}) \le 19$.

**Quello che dice il solver.** $z(\mathrm{LP}) = 520/49 = 10{,}61$. Ottimo
intero $15$: il lavoro 1 sulla macchina 2, i lavori 2 e 3 sulla macchina 3,
$\tilde y = (0, 5, 10)$. La ripartizione uniforme dei $\lambda$ è la prima che
viene in mente, non la migliore.

| $UB$ | $LB$ (duale a mano) | $z(\mathrm{LP})$ | $z(\mathrm{MILP})$ | gap euristica |
|---:|---:|---:|---:|---:|
| 19 | 5 | $520/49$ | 15 | $26{,}7\%$ |

## Considerazioni aggiuntive

- Con $\bar t_m = \max_j t_{jm}$, i vincoli $\bar t_m \sum_j x_{jm} - y_m \ge 0$
  forzano $y_m = 0$ a macchina vuota: **non** sono validi (il modello ammette
  $y_m > 0$ a macchina vuota) ma **preservano l'ottimo**. La distinzione fra
  «valido» e «preserva l'ottimo» è la stessa fra i due passi del legame.

## Domande di modellazione aggiuntive

??? question "7.4.1 — Minimizzare il tempo della macchina più lenta"
    Minimizzare il massimo dei tempi di lavorazione (makespan), non la somma.

    !!! tip "Soluzione"
        La soluzione è nel documento delle soluzioni, riservato ai docenti.
??? question "7.4.2 — Costo fisso se la macchina lavora"
    Accendere una macchina costa $g_m = 4$ euro, un minuto costa $1$ euro.
    Quale legame serve e qual è il big-M più piccolo?

    !!! tip "Soluzione"
        La soluzione è nel documento delle soluzioni, riservato ai docenti.
## Codice

Script completo: [`python/fam07_4_parallelo.py`](https://github.com/fabiofurini/modellazione-mip/blob/main/python/fam07_4_parallelo.py);
notebook: [`notebooks/fam07_4_parallelo.ipynb`](https://github.com/fabiofurini/modellazione-mip/blob/main/notebooks/fam07_4_parallelo.ipynb).

<!-- script-incorporato: inizio (rigenerato da python/incorpora_codice.py) -->

??? example "Mostra lo script completo — `python/fam07_4_parallelo.py` (123 righe)"

    ```python
    """Problema 7.4 -- Lavori in parallelo: il tempo di lavorazione come massimo.

    Il pattern della variabile di massimo, in tre passi: imposta dal vincolo (un
    lato), imposta dall'ottimo (l'altro lato), sintesi che caratterizza y_m come
    il massimo dei tempi dei lavori assegnati.
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
    intestazione("4. Lavori in parallelo: y_m = massimo dei tempi dei lavori assegnati")
    t4 = [[6, 5, 3], [5, 10, 2], [20, 13, 10]]
    p4 = [1, 2, 2]
    salva_dati(pd.DataFrame([{"lavoro": j + 1, "macchina": m + 1, "t": t4[j][m]}
                             for j in R(3) for m in R(3)]), "sched4_lavori")
    salva_dati(pd.DataFrame({"macchina": R(1, 4), "p": p4}), "sched4_macchine")


    def modello_4(t, p):
        n, k = len(t), len(p)
        m = nuovo_modello("parallelo")
        x = m.addVars(n, k, vtype=GRB.BINARY, name="x")
        y = m.addVars(k, name="y")
        m.setObjective(y.sum(), GRB.MINIMIZE)
        m.addConstrs((x.sum(j, "*") == 1 for j in R(n)), name="assegna")
        m.addConstrs((x.sum("*", mm) <= p[mm] for mm in R(k)), name="cardinalita")
        m.addConstrs((-t[j][mm] * x[j, mm] + y[mm] >= 0 for j in R(n) for mm in R(k)), name="massimo")
        return m, x, y


    def duale_4(t, p):
        """max sum mu_j + sum p_m pi_m;  mu_j + pi_m - t_jm lam_jm <= 0;  sum_j lam_jm <= 1."""
        n, k = len(t), len(p)
        d = nuovo_modello("duale_parallelo")
        mu = d.addVars(n, lb=-GRB.INFINITY, name="mu")
        pi = d.addVars(k, lb=-GRB.INFINITY, ub=0.0, name="pi")
        lam = d.addVars(n, k, name="lam")
        d.setObjective(mu.sum() + gp.quicksum(p[mm] * pi[mm] for mm in R(k)), GRB.MAXIMIZE)
        d.addConstrs((mu[j] + pi[mm] - t[j][mm] * lam[j, mm] <= 0 for j in R(n) for mm in R(k)), name="rc_x")
        d.addConstrs((lam.sum("*", mm) <= 1 for mm in R(k)), name="rc_y")
        return d


    def euristica_4(t, p):
        """Next-fit sul numero di lavori: si riempie una macchina fino a p_m lavori, poi la successiva."""
        n, k = len(t), len(p)
        x, y, cm, cnt, passi = {}, [0.0] * k, 0, 0, []
        for j in R(n):
            if cnt == p[cm]:
                if cm == k - 1:
                    return None
                cm, cnt = cm + 1, 0
            x[(j, cm)] = 1
            cnt += 1
            y[cm] = max(y[cm], t[j][cm])
            passi.append(f"Lavoro {j + 1} sulla macchina {cm + 1} (lavori assegnati {cnt} <= p = {p[cm]}): "
                         f"y[{cm + 1}] = max(y[{cm + 1}], t[{j + 1}][{cm + 1}] = {t[j][cm]}) = {y[cm]:g}.")
        return x, y, passi


    m4, x4, y4 = modello_4(t4, p4)

    # ---------- 2. EURISTICA COSTRUTTIVA (UPPER BOUND) ----------
    xe, ye, passi = euristica_4(t4, p4)
    print("Euristica next-fit sulle cardinalità:")
    for i, s in enumerate(passi, 1):
        print(f"  Passo {i}. {s}")
    ub4 = sum(ye)
    print(f"  ub = {frazione(ub4)}")

    # ---------- 3. RILASSAMENTO LP E DUALE (LOWER BOUND) ----------
    d4 = duale_4(t4, p4)
    mano = {f"lam[{j},{mm}]": 1 / 3 for j in R(3) for mm in R(3)}
    mano.update({f"mu[{j}]": min(t4[j][mm] / 3 for mm in R(3)) for j in R(3)})
    lb4, viol = valuta(d4, mano)
    assert viol <= 1e-9
    print("Soluzione duale a mano: lam_jm = 1/3, pi = 0, mu_j = min_m t_jm/3 = "
          + ", ".join(frazione(mano[f"mu[{j}]"]) for j in R(3)) + f"  ->  lb = {frazione(lb4)}")
    zlp4, zlp4r, _ = due_rilassamenti(m4, d4)

    # ---------- 4. SOLUZIONE OTTIMA DEL MILP ----------
    z4 = risolvi(m4)
    print("Soluzione ottima del MILP:")
    stampa_soluzione(m4, solo_non_nulle=True)
    riga = registra_bound("4 parallelo", ub4, lb4, zlp4, zlp4r, z4)
    salva_dati(pd.DataFrame([riga]), "sched4_bound")

    # ---------- 5. DOMANDE DI MODELLAZIONE AGGIUNTIVE ----------


    varianti = {}


    def variante(nome, m):
        z = risolvi(m)
        print(f"  {nome:70s} z = {frazione(z)}")
        return z

    # 4a: minimizzare il makespan (massimo dei tempi delle macchine)
    m, x, y = modello_4(t4, p4)
    w = m.addVar(name="w")
    m.addConstrs((w >= y[mm] for mm in R(3)), name="makespan")
    m.setObjective(w, GRB.MINIMIZE)
    varianti["4a"] = variante("4a. Minimizzare il massimo dei tempi (min-max: w >= y_m)", m)
    # 4b: costo fisso se una macchina lavora (y_m > 0 => v_m = 1, big-M = max_j t_jm)
    g4 = [4, 4, 4]
    m, x, y = modello_4(t4, p4)
    vv = m.addVars(3, vtype=GRB.BINARY, name="v")
    m.addConstrs((y[mm] <= max(t4[j][mm] for j in R(3)) * vv[mm] for mm in R(3)), name="attiva")
    m.setObjective(y.sum() + gp.quicksum(g4[mm] * vv[mm] for mm in R(3)), GRB.MINIMIZE)
    varianti["4b"] = variante("4b. Costo fisso 4 se la macchina lavora (y_m <= M_m v_m)", m)
    salva_dati(pd.DataFrame({"variante": list(varianti), "z": list(varianti.values())}), "sched4_varianti")

    print("Fine.")
    ```

<!-- script-incorporato: fine -->
