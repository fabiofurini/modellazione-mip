# Selezione di lavori con ricavo e macchine a costo fisso

**Classe:** BIP · **Legami:** attivazione (aggregata), problema di massimo · **Script:** `python/fam07_scheduling.py`

[![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/fam07_scheduling.ipynb)

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

## Euristica costruttiva: lower bound

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

## Rilassamento LP e duale: upper bound

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
ottima per il duale; il rilassamento rafforzato scende a $680/21 = 32{,}38$.
Ottimo intero $25$: i lavori 1 e 3 sulla macchina 3 ($25 + 75 = 100$,
esattamente la disponibilità), profitto $40 - 15$; il lavoro 2 non conviene
perché richiederebbe una seconda macchina ($c_1 = 20 > r_2 = 15$). Gap
dell'euristica: $20\%$.

| $\mathrm{lb}$ (best-fit) | $\mathrm{ub}$ (duale a mano) | $z(\mathrm{LP})$ | $z(\mathrm{LP}^+)$ | $z(\mathrm{MILP})$ | gap euristica |
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

    ??? success "Soluzione"
        I vincoli «al più una» diventano uguaglianze $\sum_m x_{jm} = 1$: il
        modello torna quello del problema 7.2 con la costante $\sum_j r_j$
        nell'obiettivo. L'ottimo scende da $25$ a $20$ (servono due macchine:
        il lavoro 3 sulla 3, i lavori 1 e 2 sulla 1). L'obbligo costa $5$ euro.

??? question "7.3.2 — Un lavoro condizionato a un altro"
    Si può eseguire il lavoro 3 solo se si esegue anche il lavoro 2. Scrivere
    il vincolo e trovare il nuovo ottimo.

    ??? success "Soluzione"
        «3 $\Rightarrow$ 2» con le proposizioni $\sum_m x_{3m} = 1$ e
        $\sum_m x_{2m} = 1$:

        $$\sum_{m=1}^{k} x_{3m} \le \sum_{m=1}^{k} x_{2m}.$$

        Se il lavoro 3 è eseguito il vincolo forza il 2; se il 2 non è eseguito
        forza fuori il 3; non impone la converse. Nuovo ottimo $20$.

## Codice

Script completo: [`python/fam07_scheduling.py`](https://github.com/fabiofurini/modellazione-mip/blob/main/python/fam07_scheduling.py);
notebook: [`notebooks/fam07_scheduling.ipynb`](https://github.com/fabiofurini/modellazione-mip/blob/main/notebooks/fam07_scheduling.ipynb).
