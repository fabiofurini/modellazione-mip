# Selezione di lavori con ricavo e macchine a costo fisso

**Classe:** BIP · **Legami:** attivazione (aggregata), problema di massimo · **Script:** `python/fam07_3_selezione.py`

[![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/fam07_3_selezione.ipynb)

!!! abstract "Problema 7.3"
    Un'azienda può eseguire $n \in \mathbb{Z}_{\ge 1}$ lavori e dispone di
    $k \in \mathbb{Z}_{\ge 1}$ macchine. Per ogni lavoro $j$, $t_j \in \mathbb{Q}_{>0}$
    è il tempo di lavorazione (uguale su tutte le macchine) e $r_j \in \mathbb{Q}_{>0}$
    il ricavo se il lavoro viene eseguito. Per ogni macchina $m$, $a_m \in \mathbb{Q}_{>0}$
    è la disponibilità e $c_m \in \mathbb{Q}_{>0}$ il costo se la macchina viene
    usata. Ogni macchina esegue un lavoro alla volta. L'azienda vuole scegliere
    quali lavori eseguire, e su quali macchine, per massimizzare il profitto:
    ricavi dei lavori eseguiti meno costi delle macchine usate.

**Il problema a parole.** *Decidiamo* quali lavori eseguire, su quali macchine,
e quali macchine accendere. *L'obiettivo*: profitto massimo. *I vincoli*: ogni
lavoro al più su una macchina; nessun lavoro su una macchina spenta;
disponibilità rispettata. È il [problema 7.2](scheduling-2.md) in cui i lavori
non sono più obbligatori e hanno un ricavo: un problema di **massimo**, e i
ruoli dei bound si scambiano.

## Modello

**Dati (input del modello).**

| Simbolo | Tipo | Significato |
|---|---|---|
| $n$ | $\in \mathbb{Z}_{\ge 1}$ | numero di lavori, $j \in \{1, 2, \dots, n\}$ |
| $k$ | $\in \mathbb{Z}_{\ge 1}$ | numero di macchine, $m \in \{1, 2, \dots, k\}$ |
| $t_j$ | $\in \mathbb{Q}_{>0}$ | tempo di lavorazione del lavoro $j$ |
| $r_j$ | $\in \mathbb{Q}_{>0}$ | ricavo se il lavoro $j$ è eseguito |
| $a_m$ | $\in \mathbb{Q}_{>0}$ | disponibilità della macchina $m$ |
| $c_m$ | $\in \mathbb{Q}_{>0}$ | costo fisso se la macchina $m$ è usata |

**Variabili decisionali.** $n\,k + k$ variabili binarie: $x_{jm} = 1$ se il
lavoro $j$ è eseguito dalla macchina $m$; $y_m = 1$ se la macchina $m$ è usata.

$$
\begin{aligned}
\max ~~ \sum_{j=1}^{n} \sum_{m=1}^{k} r_j\, x_{jm} - \sum_{m=1}^{k} c_m\, y_m & & \\
\text{soggetto a} \quad \sum_{m=1}^{k} x_{jm} &\le 1, & \forall j \in \{1, 2, \dots, n\}, \\
\sum_{j=1}^{n} t_j\, x_{jm} - a_m\, y_m &\le 0, & \forall m \in \{1, 2, \dots, k\}, \\
x_{jm} &\in \{0, 1\}, & \forall j,\ \forall m, \\
y_m &\in \{0, 1\}, & \forall m \in \{1, 2, \dots, k\}.
\end{aligned}
$$

- la funzione obiettivo massimizza il profitto, ricavi dei lavori eseguiti meno
  costi delle macchine usate;
- i vincoli **al più una** assicurano che ogni lavoro sia assegnato ad al più
  una macchina ($n$ vincoli lineari);
- i vincoli di **link** collegano assegnamenti e utilizzi e impongono la
  capacità ($k$ vincoli lineari);
- i vincoli di dominio definiscono le variabili.

!!! note "Legame fra le variabili"
    Lo stesso del problema 7.2, con $t_j$ al posto di $t_{jm}$. Il verso «di
    ottimalità» cambia segno: poiché $c_m > 0$, se $y_m = 1$ senza lavori,
    porre $y_m = 0$ resta ammissibile e **aumenta** il profitto di $c_m$ — in un
    problema di massimo il verso del miglioramento si inverte, la struttura
    dell'argomento no.

## Il modello in gurobipy

```python
m = gp.Model("selezione");  m.Params.OutputFlag = 0
x = m.addVars(n, k, vtype=GRB.BINARY, name="x")
y = m.addVars(k, vtype=GRB.BINARY, name="y")
m.setObjective(gp.quicksum(r[j] * x[j, mm] for j in range(n) for mm in range(k))
               - gp.quicksum(c[mm] * y[mm] for mm in range(k)), GRB.MAXIMIZE)
m.addConstrs((x.sum(j, "*") <= 1 for j in range(n)), name="al_piu_una")
m.addConstrs((gp.quicksum(t[j] * x[j, mm] for j in range(n)) - a[mm] * y[mm] <= 0
              for mm in range(k)), name="link")
m.optimize()
```

## L'istanza

| | $m=1$ | $m=2$ | $m=3$ |
|---|---:|---:|---:|
| $a_m$ | 105 | 110 | 100 |
| $c_m$ | 20 | 30 | 15 |

| | $j=1$ | $j=2$ | $j=3$ |
|---|---:|---:|---:|
| $t_j$ | 25 | 40 | 75 |
| $r_j$ | 10 | 15 | 30 |

## Euristica costruttiva: il bound primale

In un problema di massimo una soluzione ammissibile dà un *lower* bound. Un
lavoro che non sta su nessuna macchina viene **saltato**. Il best-fit sceglie la
macchina **più piena** fra quelle che bastano:

- **Passo 1.** Lavoro 1 ($t_1 = 25$): $ra = (105, 110, 100)$; la più piena è la
  macchina 3: $x[1][3] = 1$, $ra[3] = 75$.
- **Passo 2.** Lavoro 2 ($t_2 = 40$): la più piena è ancora la 3: $x[2][3] = 1$,
  $ra[3] = 35$.
- **Passo 3.** Lavoro 3 ($t_3 = 75$): la 3 non basta; fra 1 e 2 la più piena è
  la 1: $x[3][1] = 1$, $ra[1] = 30$.

Profitto $10 + 15 + 30 - 20 - 15 = 20$: $z(\mathrm{MILP}) \ge 20$. Next-fit e
first-fit riempiono prima la macchina 1 e arrivano a $5$.

## Rilassamento LP e duale: il bound duale

Con $\mu_j \ge 0$ (al più una) e $\pi_m \ge 0$ (link):

$$
\begin{aligned}
\min ~~ \sum_{j=1}^{n} \mu_j & & \\
\text{soggetto a} \quad \mu_j + t_j\, \pi_m &\ge r_j, & \forall j,\ \forall m, \\
-a_m\, \pi_m &\ge -c_m, & \forall m, \\
\mu_j \ge 0,\quad \pi_m &\ge 0. &
\end{aligned}
$$

**Una soluzione duale a mano.** $\bar\pi_m = c_m/a_m$: $\tfrac{4}{21}, \tfrac{3}{11}, \tfrac{3}{20}$;
poi $\bar\mu_j = \max\{0, \max_m (r_j - t_j \bar\pi_m)\}$:
$\bar\mu_1 = \tfrac{25}{4}$, $\bar\mu_2 = 9$, $\bar\mu_3 = \tfrac{75}{4}$; valore $34$:

$$20 ~\le~ z(\mathrm{MILP}) ~\le~ 34.$$

**Quello che dice il solver.** $z(\mathrm{LP}) = 34$: la soluzione a mano è
ottima per il duale; il rilassamento con i bound scende a $680/21 = 32{,}38$.
Ottimo intero $25$: i lavori 1 e 3 sulla macchina 3 ($25 + 75 = 100$,
esattamente la disponibilità), profitto $40 - 15$; il lavoro 2 non conviene
perché richiederebbe una seconda macchina ($c_1 = 20 > r_2 = 15$). Gap
dell'euristica: $20\%$.

| $LB$ (best-fit) | $UB$ (duale a mano) | $z(\mathrm{LP})$ | $z(\mathrm{LP}^+)$ | $z(\mathrm{MILP})$ | gap euristica |
|---:|---:|---:|---:|---:|---:|
| 20 | 34 | 34 | $680/21$ | 25 | $20{,}0\%$ |

## Considerazioni aggiuntive

- $y_m \le 1$ rafforza il rilassamento ($34 \to 32{,}38$); $x_{jm} \le 1$ è
  implicato.
- I link disaggregati $x_{jm} \le y_m$ sono validi e rafforzano il rilassamento.
- Se $r_j < \min_m c_m$ e il lavoro $j$ è l'unico su una macchina, eseguirlo
  non conviene mai (il lavoro 2 nell'istanza).

## Domande di modellazione aggiuntive

??? question "7.3.1 — Tutti i lavori obbligatori"
    Tutti i lavori vanno eseguiti. Come cambia il modello e quanto costa
    l'obbligo?

    !!! tip "Soluzione"
        La soluzione è nel documento delle soluzioni, riservato ai docenti.
??? question "7.3.2 — Un lavoro condizionato a un altro"
    Si può eseguire il lavoro 3 solo se si esegue anche il lavoro 2. Scrivere
    il vincolo e trovare il nuovo ottimo.

    !!! tip "Soluzione"
        La soluzione è nel documento delle soluzioni, riservato ai docenti.
## Codice

Script completo: [`python/fam07_3_selezione.py`](https://github.com/fabiofurini/modellazione-mip/blob/main/python/fam07_3_selezione.py);
notebook: [`notebooks/fam07_3_selezione.ipynb`](https://github.com/fabiofurini/modellazione-mip/blob/main/notebooks/fam07_3_selezione.ipynb).

<!-- script-incorporato: inizio (rigenerato da python/incorpora_codice.py) -->

??? example "Mostra lo script completo — `python/fam07_3_selezione.py` (110 righe)"

    ```python
    """Problema 7.3 -- Selezione di lavori con ricavo e macchine a costo fisso.

    Stesso legame di attivazione del problema 7.2, letto in un problema di
    massimo: l'euristica da' un lower bound, il duale un upper bound -- i ruoli
    si scambiano rispetto ai problemi di minimo.
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
    intestazione("3. Selezione di lavori: massimo profitto = ricavi - costi fissi")
    t3 = [25, 40, 75]
    r3 = [10, 15, 30]
    c3 = [20, 30, 15]
    a3 = [105, 110, 100]
    salva_dati(pd.DataFrame({"lavoro": R(1, 4), "t": t3, "r": r3}), "sched3_lavori")
    salva_dati(pd.DataFrame({"macchina": R(1, 4), "c": c3, "a": a3}), "sched3_macchine")


    def modello_3(t, r, c, a):
        n, k = len(t), len(a)
        m = nuovo_modello("selezione")
        x = m.addVars(n, k, vtype=GRB.BINARY, name="x")
        y = m.addVars(k, vtype=GRB.BINARY, name="y")
        m.setObjective(gp.quicksum(r[j] * x[j, mm] for j in R(n) for mm in R(k))
                       - gp.quicksum(c[mm] * y[mm] for mm in R(k)), GRB.MAXIMIZE)
        m.addConstrs((x.sum(j, "*") <= 1 for j in R(n)), name="al_piu_una")
        m.addConstrs((gp.quicksum(t[j] * x[j, mm] for j in R(n)) - a[mm] * y[mm] <= 0 for mm in R(k)),
                     name="link")
        return m, x, y


    def duale_3(t, r, c, a):
        """min sum mu_j;  mu_j + t_j pi_m >= r_j;  -a_m pi_m >= -c_m;  mu, pi >= 0."""
        n, k = len(t), len(a)
        d = nuovo_modello("duale_selezione")
        mu = d.addVars(n, name="mu")
        pi = d.addVars(k, name="pi")
        d.setObjective(mu.sum(), GRB.MINIMIZE)
        d.addConstrs((mu[j] + t[j] * pi[mm] >= r[j] for j in R(n) for mm in R(k)), name="rc_x")
        d.addConstrs((-a[mm] * pi[mm] >= -c[mm] for mm in R(k)), name="rc_y")
        return d


    def valore_3(e, r, c):
        return sum(r[j] for (j, mm) in e.x) - sum(c[mm] * y for mm, y in enumerate(e.y))


    m3, x3, y3 = modello_3(t3, r3, c3, a3)

    # ---------- 2. EURISTICA COSTRUTTIVA (LOWER BOUND) ----------
    T3 = matrice(t3, 3)
    eur3 = [("next-fit (salta se non ci sta)", next_fit(T3, a3, salta=True)),
            ("first-fit", first_fit(T3, a3, salta=True)),
            ("best-fit (macchina più piena)", best_fit(T3, a3, lambda j, mm, ra: ra[mm], "ra", salta=True))]
    print("Euristiche costruttive (qui danno un LOWER bound: il problema è di massimo):")
    for nome, e in eur3:
        print(f"  {nome:32s} lb = {valore_3(e, r3, c3):3d}")
    print("Esecuzione passo-passo del best-fit:")
    eur3[2][1].traccia.stampa()
    lb3 = max(valore_3(e, r3, c3) for _, e in eur3)

    # ---------- 3. RILASSAMENTO LP E DUALE (UPPER BOUND) ----------
    d3 = duale_3(t3, r3, c3, a3)
    mano = {f"pi[{mm}]": c3[mm] / a3[mm] for mm in R(3)}
    mano.update({f"mu[{j}]": max([0] + [r3[j] - t3[j] * c3[mm] / a3[mm] for mm in R(3)]) for j in R(3)})
    ub3, viol = valuta(d3, mano)
    assert viol <= 1e-9
    print("Soluzione duale a mano: pi_m = c_m/a_m; mu_j = max{0, r_j - t_j pi_m} = "
          + ", ".join(frazione(mano[f"mu[{j}]"]) for j in R(3)) + f"  ->  ub = {frazione(ub3)}")
    zlp3, zlp3r, _ = due_rilassamenti(m3, d3)

    # ---------- 4. SOLUZIONE OTTIMA DEL MILP ----------
    z3 = risolvi(m3)
    print("Soluzione ottima del MILP:")
    stampa_soluzione(m3, solo_non_nulle=True)
    riga = registra_bound("3 selezione", ub3, lb3, zlp3, zlp3r, z3, senso="max")
    salva_dati(pd.DataFrame([riga]), "sched3_bound")

    # ---------- 5. DOMANDE DI MODELLAZIONE AGGIUNTIVE ----------


    varianti = {}


    def variante(nome, m):
        z = risolvi(m)
        print(f"  {nome:70s} z = {frazione(z)}")
        return z

    # 3a: tutti i lavori devono essere eseguiti (torna il vincolo di assegnamento)
    m, x, y = modello_3(t3, r3, c3, a3)
    m.addConstrs((x.sum(j, "*") == 1 for j in R(3)), name="tutti")
    varianti["3a"] = variante("3a. Tutti i lavori eseguiti (sum_m x_jm = 1)", m)
    # 3b: il lavoro 3 solo se il lavoro 2
    m, x, y = modello_3(t3, r3, c3, a3)
    m.addConstr(x.sum(2, "*") <= x.sum(1, "*"), name="3_solo_se_2")
    varianti["3b"] = variante("3b. Il lavoro 3 si esegue solo se si esegue il lavoro 2", m)
    salva_dati(pd.DataFrame({"variante": list(varianti), "z": list(varianti.values())}), "sched3_varianti")

    print("Fine.")
    ```

<!-- script-incorporato: fine -->
