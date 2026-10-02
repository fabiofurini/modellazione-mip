# Selezione di lavori con ricavo e macchine a costo fisso

**Classe:** BIP · **Legami:** attivazione (aggregata), problema di massimo · **Script:** `python/fam07_3_selezione.py`<br>
**Difficoltà:** ★★☆☆☆ · **Tempo:** 30–45 min
{ .scheda }

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

<!-- modello: 7.3 -->

$$
\begin{aligned}
\max ~~ \sum_{j=1}^{n} \sum_{m=1}^{k} r_j\, x_{jm} - \sum_{m=1}^{k} c_m\, y_m & & \\
\text{soggetto a} \quad \sum_{m=1}^{k} x_{jm} &\le 1, & \forall j \in \{1, 2, \dots, n\}, \\
\sum_{j=1}^{n} t_j\, x_{jm} - a_m\, y_m &\le 0, & \forall m \in \{1, 2, \dots, k\}, \\
x_{jm} &\in \{0, 1\}, & \forall j \in \{1, 2, \dots, n\},\ \forall m \in \{1, 2, \dots, k\}, \\
y_m &\in \{0, 1\}, & \forall m \in \{1, 2, \dots, k\}.
\end{aligned}
$$

<!-- modello: fine -->

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

Il modello scritto sui dati dell'istanza:

<!-- modello-esteso: fam07_3_primale -->

<div class="modello-esteso largo" markdown>

$$
\begin{array}{rrrrrrrrrrrrr c l}
\max & 10x_{11} & +10x_{12} & +10x_{13} & +15x_{21} & +15x_{22} & +15x_{23} & +30x_{31} & +30x_{32} & +30x_{33} & -20y_1 & -30y_2 & -15y_3 &  & \\
\text{soggetto a} & x_{11} & +x_{12} & +x_{13} &  &  &  &  &  &  &  &  &  & \le & 1\\
 &  &  &  & x_{21} & +x_{22} & +x_{23} &  &  &  &  &  &  & \le & 1\\
 &  &  &  &  &  &  & x_{31} & +x_{32} & +x_{33} &  &  &  & \le & 1\\
 & 25x_{11} &  &  & +40x_{21} &  &  & +75x_{31} &  &  & -105y_1 &  &  & \le & 0\\
 &  & 25x_{12} &  &  & +40x_{22} &  &  & +75x_{32} &  &  & -110y_2 &  & \le & 0\\
 &  &  & 25x_{13} &  &  & +40x_{23} &  &  & +75x_{33} &  &  & -100y_3 & \le & 0\\
 & x_{11}, & x_{12}, & x_{13}, & x_{21}, & x_{22}, & x_{23}, & x_{31}, & x_{32}, & x_{33} &  &  &  & \in & \{0, 1\}\\
 &  &  &  &  &  &  &  &  &  & y_1, & y_2, & y_3 & \in & \{0, 1\}
\end{array}
$$

</div>

<!-- modello-esteso: fine -->

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

Profitto $10 + 15 + 30 - 20 - 15 = 20$: $z(\mathit{MILP}) \ge 20$. Next-fit e
first-fit riempiono prima la macchina 1 e arrivano a $5$.

## Rilassamento LP e duale: il bound duale

Con $\mu_j \ge 0$ (al più una) e $\pi_m \ge 0$ (link):

<!-- modello: 7.3-duale -->

$$
\begin{aligned}
\min ~~ \sum_{j=1}^{n} \mu_j & & \\
\text{soggetto a} \quad \mu_j + t_j\, \pi_m &\ge r_j, & \forall j \in \{1, 2, \dots, n\},\ \forall m \in \{1, 2, \dots, k\}, \\
-a_m\, \pi_m &\ge -c_m, & \forall m \in \{1, 2, \dots, k\}, \\
\mu_j &\ge 0, & \forall j \in \{1, 2, \dots, n\}, \\
\pi_m &\ge 0, & \forall m \in \{1, 2, \dots, k\}.
\end{aligned}
$$

<!-- modello: fine -->

Lo stesso duale, scritto sui dati dell'istanza:

<!-- modello-esteso: fam07_3_duale -->

<div class="modello-esteso" markdown>

$$
\begin{array}{rrrrrrr c l}
\min & \mu_1 & +\mu_2 & +\mu_3 &  &  &  &  & \\
\text{soggetto a} & \mu_1 &  &  & +25\pi_1 &  &  & \ge & 10\\
 & \mu_1 &  &  &  & +25\pi_2 &  & \ge & 10\\
 & \mu_1 &  &  &  &  & +25\pi_3 & \ge & 10\\
 &  & \mu_2 &  & +40\pi_1 &  &  & \ge & 15\\
 &  & \mu_2 &  &  & +40\pi_2 &  & \ge & 15\\
 &  & \mu_2 &  &  &  & +40\pi_3 & \ge & 15\\
 &  &  & \mu_3 & +75\pi_1 &  &  & \ge & 30\\
 &  &  & \mu_3 &  & +75\pi_2 &  & \ge & 30\\
 &  &  & \mu_3 &  &  & +75\pi_3 & \ge & 30\\
 &  &  &  & -105\pi_1 &  &  & \ge & -20\\
 &  &  &  &  & -110\pi_2 &  & \ge & -30\\
 &  &  &  &  &  & -100\pi_3 & \ge & -15\\
 & \mu_1, & \mu_2, & \mu_3 &  &  &  & \ge & 0\\
 &  &  &  & \pi_1, & \pi_2, & \pi_3 & \ge & 0
\end{array}
$$

</div>

<!-- modello-esteso: fine -->

**Una soluzione duale a mano.** $\bar\pi_m = c_m/a_m$: $\tfrac{4}{21}, \tfrac{3}{11}, \tfrac{3}{20}$;
poi $\bar\mu_j = \max\{0, \max_m (r_j - t_j \bar\pi_m)\}$:
$\bar\mu_1 = \tfrac{25}{4}$, $\bar\mu_2 = 9$, $\bar\mu_3 = \tfrac{75}{4}$; valore $34$:

$$20 ~\le~ z(\mathit{MILP}) ~\le~ 34.$$

**Quello che dice il solver.** $z(\mathit{LP}) = 34$: la soluzione a mano è
ottima per il duale; il rilassamento con i bound scende a $680/21 = 32{,}38$.
Ottimo intero $25$: i lavori 1 e 3 sulla macchina 3 ($25 + 75 = 100$,
esattamente la disponibilità), profitto $40 - 15$; il lavoro 2 non conviene
perché richiederebbe una seconda macchina ($c_1 = 20 > r_2 = 15$). Gap
dell'euristica: $20\%$.

| $LB$ (best-fit) | $UB$ (duale a mano) | $z(\mathit{LP})$ | $z(\mathit{LP}^+)$ | $z(\mathit{MILP})$ | gap euristica |
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

## Una variante svolta: un lavoro condizionato a un altro

Il lavoro 3 richiede un semilavorato prodotto dal lavoro 2: si può eseguire il
lavoro 3 solo se si esegue anche il lavoro 2 (su qualunque macchina).

«Eseguo il lavoro 3» è la proposizione $\sum_m x_{3m} = 1$, «eseguo il lavoro 2»
è $\sum_m x_{2m} = 1$; l'implicazione «3 $\Rightarrow$ 2» si scrive

$$
\sum_{m=1}^{k} x_{3m} \le \sum_{m=1}^{k} x_{2m}
$$

(un vincolo lineare). Se il lavoro 3 è eseguito il membro sinistro vale $1$ e
il vincolo forza il membro destro a $1$: il lavoro 2 è eseguito; viceversa, se
il lavoro 2 non è eseguito il membro destro vale $0$ e il vincolo forza
$\sum_m x_{3m} = 0$. Il vincolo non impone la converse: il lavoro 2 può essere
eseguito senza il 3. Sull'istanza l'ottimo diventa $20$: la soluzione da $25$
(lavori 1 e 3 senza il 2) non è più ammissibile, e la migliore è di nuovo
$\{1, 2\}$ sulla macchina 1 e $\{3\}$ sulla macchina 3.

«Il lavoro 3 solo se anche il lavoro 2» aggiunge al duale un moltiplicatore
$\lambda \ge 0$, che sconta le colonne del lavoro 3 e carica quelle del lavoro 2.
Si alza $\lambda$ fin dove il lavoro 2 lo regge a costo zero: su questa istanza
quel margine non c'è, $\lambda$ resta a zero e il certificato coincide con quello
del problema base.

<!-- tabella-variante: fam07_3b_bound -->

|  | valore | che cos'è |
|---|---:|---|
| $\mathit{UB}$ | $34$ | certificato duale costruito a mano |
| $\mathit{LB}$ | $20$ | soluzione euristica |
| $z(\mathit{LP})$ | $34$ | rilassamento senza i bound |
| $z(\mathit{LP}^+)$ | $\frac{680}{21}$ | rilassamento con i bound |
| $z(\mathit{MILP})$ | $20$ | ottimo del MILP |

<!-- tabella-variante: fine -->

## Codice

Script completo: [`python/fam07_3_selezione.py`](https://github.com/fabiofurini/modellazione-mip/blob/main/python/fam07_3_selezione.py);
notebook: [`notebooks/fam07_3_selezione.ipynb`](https://github.com/fabiofurini/modellazione-mip/blob/main/notebooks/fam07_3_selezione.ipynb).

<!-- script-incorporato: inizio (rigenerato da python/incorpora_codice.py) -->

??? example "Mostra lo script completo — `python/fam07_3_selezione.py` (195 righe)"

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
    from mip import (ammissibile, dualita_forte, due_rilassamenti, frazione,
                     nuovo_modello, registra_bound, rilassamenti, risolvi,
                     stampa_soluzione, valuta)
    from stile import CICLO, ROSSO, intestazione, plt, salva_dati, salva_figura
    from esteso import salva_modello

    R = range

    # ---------- 1. MODELLO E ISTANZA ----------
    intestazione("3. Selezione di lavori: massimo profitto = ricavi - costi fissi")
    t3 = [25, 40, 75]
    r3 = [10, 15, 30]
    c3 = [20, 30, 15]
    a3 = [105, 110, 100]
    salva_dati(pd.DataFrame({"lavoro": R(1, 4), "t": t3, "r": r3}), "fam07_3_lavori")
    salva_dati(pd.DataFrame({"macchina": R(1, 4), "c": c3, "a": a3}), "fam07_3_macchine")


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
    salva_modello(m3, "fam07_3_primale")

    # ---------- 2. IL RILASSAMENTO LP ----------
    zlp3, zlp3r, _ = rilassamenti(m3)

    # ---------- 3. IL DUALE DEL RILASSAMENTO (UPPER BOUND: E' UN MASSIMO) ----------
    d3 = duale_3(t3, r3, c3, a3)
    salva_modello(d3, "fam07_3_duale")
    mano = {f"pi[{mm}]": c3[mm] / a3[mm] for mm in R(3)}
    mano.update({f"mu[{j}]": max([0] + [r3[j] - t3[j] * c3[mm] / a3[mm] for mm in R(3)]) for j in R(3)})
    ub3, viol = valuta(d3, mano)
    assert viol <= 1e-9
    print("Soluzione duale a mano: pi_m = c_m/a_m; mu_j = max{0, r_j - t_j pi_m} = "
          + ", ".join(frazione(mano[f"mu[{j}]"]) for j in R(3)) + f"  ->  ub = {frazione(ub3)}")
    dualita_forte(d3, zlp3)

    # ---------- 4. EURISTICA COSTRUTTIVA (LOWER BOUND: E' UN MASSIMO) ----------
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

    # ---------- 5. SOLUZIONE OTTIMA DEL MILP ----------
    z3 = risolvi(m3)
    print("Soluzione ottima del MILP:")
    stampa_soluzione(m3, solo_non_nulle=True)
    riga = registra_bound("3 selezione", ub3, lb3, zlp3, zlp3r, z3, senso="max")
    salva_dati(pd.DataFrame([riga]), "fam07_3_bound")

    # ---------- 6. DOMANDE DI MODELLAZIONE AGGIUNTIVE ----------


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
    salva_dati(pd.DataFrame({"variante": list(varianti), "z": list(varianti.values())}), "fam07_3_varianti")

    # ---------- 7. IL SANDWICH SULLA VARIANTE 3b ----------
    intestazione("3b. Il sandwich sulla variante: il lavoro 3 solo se anche il lavoro 2")


    def modello_3b(t, r, c, a):
        mm_, xx, yy = modello_3(t, r, c, a)
        mm_.addConstr(xx.sum(2, "*") - xx.sum(1, "*") <= 0, name="3_solo_se_2")
        return mm_, xx, yy


    def duale_3b(t, r, c, a):
        """Al duale di 7.3 si aggiunge lambda >= 0 per il vincolo
        sum_m x_3m - sum_m x_2m <= 0: compare con segno piu' nelle colonne del
        lavoro 3 e con segno meno in quelle del lavoro 2. Il termine noto e' zero,
        quindi l'obiettivo resta min sum_j mu_j."""
        nn, kk = len(t), len(a)
        d = nuovo_modello("duale_selezione_3b")
        mu = d.addVars(nn, name="mu")
        pi = d.addVars(kk, name="pi")
        lam = d.addVar(name="lambda")
        d.setObjective(mu.sum(), GRB.MINIMIZE)
        for mz in R(kk):
            d.addConstr(mu[0] + t[0] * pi[mz] >= r[0], name=f"rc_x0{mz}")
            d.addConstr(mu[1] + t[1] * pi[mz] - lam >= r[1], name=f"rc_x1{mz}")
            d.addConstr(mu[2] + t[2] * pi[mz] + lam >= r[2], name=f"rc_x2{mz}")
        d.addConstrs((-a[mz] * pi[mz] >= -c[mz] for mz in R(kk)), name="rc_y")
        return d


    m3b, x3b, y3b = modello_3b(t3, r3, c3, a3)
    salva_modello(m3b, "fam07_3b_primale")

    # -- euristica ammissibile: la base, riparata togliendo il lavoro 3 se il 2 manca --
    print("Euristica costruttiva: si parte dalla soluzione del problema base e, se esegue il")
    print("lavoro 3 senza il 2, si toglie il lavoro 3 (la riparazione e' sempre ammissibile).")
    e_base3 = max((e for _, e in eur3), key=lambda e: valore_3(e, r3, c3))
    scelti = {j for (j, _) in e_base3.x}
    print(f"  soluzione base: lavori {sorted(j + 1 for j in scelti)}, valore "
          f"{frazione(valore_3(e_base3, r3, c3))}")
    tenuti = [(j, mz) for (j, mz) in e_base3.x if not (j == 2 and 1 not in scelti)]
    macchine = sorted({mz for (_, mz) in tenuti})
    lb3b = sum(r3[j] for (j, _) in tenuti) - sum(c3[mz] for mz in macchine)
    sol_3b = {f"x[{j},{mz}]": 1 for (j, mz) in tenuti} | {f"y[{mz}]": 1 for mz in macchine}
    assert ammissibile(m3b, sol_3b), "la soluzione euristica della variante deve essere ammissibile"
    print(f"  dopo la riparazione: lavori {sorted(j + 1 for (j, _) in tenuti)}  ->  "
          f"lb = {frazione(lb3b)}")

    # -- certificato duale: lambda sposta valore dal lavoro 3 al lavoro 2 --
    d3b = duale_3b(t3, r3, c3, a3)
    salva_modello(d3b, "fam07_3b_duale")
    pi_b = {mz: c3[mz] / a3[mz] for mz in R(3)}
    # il lambda piu' grande che non costringe mu_2 a crescere: mu_2 resta a zero
    # finche' lambda <= min_m (t_2 pi_m - r_2); oltre, quello che si guadagna su mu_3
    # si ripaga su mu_2, quindi ci si ferma li'.
    lam_b = max(0.0, min(t3[1] * pi_b[mz] - r3[1] for mz in R(3)))
    mano_3b = {f"pi[{mz}]": pi_b[mz] for mz in R(3)} | {"lambda": lam_b}
    mano_3b["mu[0]"] = max([0] + [r3[0] - t3[0] * pi_b[mz] for mz in R(3)])
    mano_3b["mu[1]"] = max([0] + [r3[1] + lam_b - t3[1] * pi_b[mz] for mz in R(3)])
    mano_3b["mu[2]"] = max([0] + [r3[2] - lam_b - t3[2] * pi_b[mz] for mz in R(3)])
    ub3b, viol_3b = valuta(d3b, mano_3b)
    assert viol_3b <= 1e-9, viol_3b
    print("Soluzione duale a mano: pi_m = c_m/a_m come nel problema base; poi si alza lambda")
    print("  fin dove il lavoro 2 lo regge a costo zero, cioe' lambda = min_m (t_2 pi_m - r_2).")
    if lam_b > 0:
        print(f"  Qui lambda = {frazione(lam_b)}: sconta il lavoro 3 senza far crescere mu_2.")
    else:
        print("  Qui quel minimo e' negativo, quindi lambda resta a zero: sul lavoro 2 non c'e'")
        print("  margine da spendere, e il certificato della variante coincide con quello del")
        print("  problema base. L'implicazione alza l'ottimo intero ma non tocca il rilassamento.")
    print(f"  ->  ub = {frazione(ub3b)}")
    zlp3b, zlp3br, _ = due_rilassamenti(m3b, d3b)
    z3b = risolvi(m3b)
    riga_3b = registra_bound("3b lavoro 3 solo con il lavoro 2", ub3b, lb3b, zlp3b, zlp3br, z3b,
                             senso="max")
    salva_dati(pd.DataFrame([riga_3b]), "fam07_3b_bound")
    assert lb3b <= z3b <= zlp3b + 1e-9 <= ub3b + 1e-9


    print("Fine.")
    ```

<!-- script-incorporato: fine -->
