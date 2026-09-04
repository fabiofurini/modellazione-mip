# Lavori in parallelo: il tempo di lavorazione come massimo

**Classe:** MILP · **Legami:** variabile di massimo · **Script:** `python/fam07_scheduling.py`

[![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/fam07_scheduling.ipynb)

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

## Euristica costruttiva: upper bound

Next-fit sulle cardinalità: si riempie la macchina 1 fino a $p_1$ lavori, poi la
2, e così via.

- **Passo 1.** Lavoro 1 sulla macchina 1: $y[1] = 6$.
- **Passo 2.** La macchina 1 è piena ($p_1 = 1$): lavoro 2 sulla macchina 2,
  $y[2] = 10$.
- **Passo 3.** Lavoro 3 sulla macchina 2: $y[2] = \max(10, 13) = 13$.

$\bar y = (6, 13, 0)$, valore $19$: $z(\mathrm{MILP}) \le 19$.

## Rilassamento LP e duale: lower bound

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

| $\mathrm{ub}$ | $\mathrm{lb}$ (duale a mano) | $z(\mathrm{LP})$ | $z(\mathrm{MILP})$ | gap euristica |
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

    ??? success "Soluzione"
        Una variabile $w \ge 0$ con $w \ge y_m$ per ogni $m$ e obiettivo
        $\min\ w$: il pattern min-max. Le $y_m$ escono dall'obiettivo, quindi
        «$y_m$ = massimo in ogni ottimo» cade; resta vero che *esiste* un ottimo
        in cui lo è. Makespan ottimo $10$: il lavoro 3 richiede almeno $10$
        minuti ovunque.

??? question "7.4.2 — Costo fisso se la macchina lavora"
    Accendere una macchina costa $g_m = 4$ euro, un minuto costa $1$ euro.
    Quale legame serve e qual è il big-M più piccolo?

    ??? success "Soluzione"
        Un'attivazione $v_m \in \{0,1\}$ e il legame $y_m > 0 \Rightarrow v_m = 1$
        imposto con $y_m \le M_m v_m$; il più piccolo $M_m$ valido è
        $\bar t_m = \max_j t_{jm}$. Il verso opposto segue dall'obiettivo perché
        $g_m > 0$. Ottimo $23 = 15 + 2 \cdot 4$.

## Codice

Script completo: [`python/fam07_scheduling.py`](https://github.com/fabiofurini/modellazione-mip/blob/main/python/fam07_scheduling.py);
notebook: [`notebooks/fam07_scheduling.ipynb`](https://github.com/fabiofurini/modellazione-mip/blob/main/notebooks/fam07_scheduling.ipynb).
