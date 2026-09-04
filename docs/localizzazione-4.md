# Localizzazione di hub con costo massimo

**Classe:** MILP · **Legami:** attivazione aggregata, variabile di massimo · **Script:** `python/fam08_4_hub.py`

[![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/fam08_4_hub.ipynb)

!!! abstract "Problema 8.4"
    $n \in \mathbb{Z}_{\ge 1}$ terminali, ciascuno da connettere a
    esattamente un hub; $m \in \mathbb{Z}_{\ge 1}$ hub, ciascuno con
    capacità $k \in \mathbb{Z}_{\ge 1}$ terminali e costo di attivazione
    $f_j \in \mathbb{Q}_{\ge 0}$. $c_{ij} \in \mathbb{Q}_{\ge 0}$ è il costo
    di connettere il terminale $i$ all'hub $j$. Si minimizza la somma dei
    costi di attivazione e del costo di connessione massimo di ciascun hub.

**Il problema a parole.** *Decidiamo* quali hub attivare e a quale hub
connettere ciascun terminale. *L'obiettivo*: attivazione più, per ciascun
hub, il costo di connessione più alto (non la somma). *I vincoli*: ogni
terminale a esattamente un hub; un hub non attivato non serve nessuno, uno
attivato serve al più $k$.

## Modello

**Variabili decisionali.** $n\,m$ binarie $x_{ij}$, $m$ binarie $y_j$
(hub attivato), $m$ continue non negative $z_j$ (costo massimo dell'hub $j$).

$$
\begin{aligned}
\min ~~ \sum_{j=1}^{m} f_j\, y_j + \sum_{j=1}^{m} z_j & & \\
\text{soggetto a} \quad \sum_{j=1}^{m} x_{ij} &= 1, & \forall i, \\
-\sum_{i=1}^{n} x_{ij} + k\, y_j &\ge 0, & \forall j, \\
-c_{ij}\, x_{ij} + z_j &\ge 0, & \forall i, j, \\
x_{ij}, y_j &\in \{0, 1\},\ z_j \ge 0. & &
\end{aligned}
$$

- l'obiettivo minimizza costi di attivazione più costo massimo per hub;
- il primo vincolo assegna ogni terminale a un hub ($n$ vincoli);
- il secondo lega assegnamento e attivazione, in forma **aggregata**, e
  impone la capacità ($m$ vincoli);
- il terzo lega assegnamento e variabile di massimo ($n\,m$ vincoli).

**Primo legame: attivazione aggregata.** Se un terminale è connesso
all'hub $j$, $j$ deve essere attivato; dalla contronominale, un hub non
attivato non serve nessuno. Entrambi imposti direttamente dal secondo
vincolo. Il verso opposto — un hub attivato serve almeno un terminale —
segue dall'obiettivo (poiché $f_j>0$). Come nel problema 7.2.

**Secondo legame: variabile di massimo.** Se il terminale $i$ è connesso
a $j$, $z_j \ge c_{ij}$: imposto direttamente. All'ottimo,
$z_j = \max_{i:x_{ij}=1} c_{ij}$ esattamente, perché l'obiettivo minimizza
$z_j$ e nessun altro vincolo la coinvolge. Come nel problema 7.7.

## Il modello in gurobipy

```python
mod = gp.Model("hub_max")
x = mod.addVars(n, m, vtype=GRB.BINARY, name="x")
y = mod.addVars(m, vtype=GRB.BINARY, name="y")
z = mod.addVars(m, name="z")
mod.setObjective(gp.quicksum(f[j] * y[j] for j in range(m)) + z.sum(), GRB.MINIMIZE)
mod.addConstrs((gp.quicksum(x[i, j] for j in range(m)) == 1 for i in range(n)), name="assegnamento")
mod.addConstrs((-gp.quicksum(x[i, j] for i in range(n)) + k * y[j] >= 0 for j in range(m)), name="attivazione")
mod.addConstrs((-c[i][j] * x[i, j] + z[j] >= 0 for i in range(n) for j in range(m)), name="massimo")
```

## L'istanza

$n=3$ terminali, $m=3$ hub, $k=2$:

| $c_{ij}$ | $j=1$ | $j=2$ | $j=3$ |
|---|---:|---:|---:|
| $i=1$ | 5 | 10 | 2 |
| $i=2$ | 5 | 4 | 6 |
| $i=3$ | 5 | 4 | 6 |

| | $j=1$ | $j=2$ | $j=3$ |
|---|---:|---:|---:|
| $f_j$ | 5 | 6 | 7 |

## Euristica costruttiva: upper bound

Un **next-fit** (bin packing): un hub alla volta, fino a $k$ terminali —
la stessa euristica generica dello scheduling, riusata da
`euristiche.py`. Terminale 1 e 2 sull'hub 1 (pieno), terminale 3 sull'hub
2. Costi massimi: $z_1=\max(5,5)=5$, $z_2=4$. Valore $5+6+5+4=20$:
$z(\mathrm{MILP}) \le \mathrm{ub} = 20$.

## Rilassamento LP e duale: lower bound

Con $\bar\gamma_{ij}=0$ e $\bar\beta_j = f_j/k$ (il massimo ammesso), il
vincolo su $\alpha_i$ vale per **ogni** hub $j$, non solo il più
conveniente: $\bar\alpha_i = \min_j \bar\beta_j$.

$$
\bar\beta = (5/2,\ 3,\ 7/2),\qquad \bar\alpha_i = 5/2\ \ \forall i,
$$

di valore $3\cdot5/2=15/2$. Per la dualità debole, $\mathrm{lb}=15/2 \le
z(\mathrm{LP}) \le z(\mathrm{MILP}) \le \mathrm{ub}=20$.

!!! warning "Un tranello frequente"
    Il vincolo su $\alpha_i$ vale per ogni hub $j$: fissare
    $\bar\gamma_{ij}=0$ solo per gli hub «non convenienti» non basta a
    liberare $\alpha_i$ da quel vincolo. $\alpha_i$ resta limitato dal
    minimo su tutti gli hub, non da uno solo.

**Quello che dice il solver.** $z(\mathrm{LP})=25/2$,
$z(\mathrm{LP}^+)=1015/78\approx13{,}0$. $z(\mathrm{MILP})=19$, con gli hub
1 e 3 attivati (non 1 e 2): il terminale 1 da solo sull'hub 3 (il più
economico per lui), i terminali 2 e 3 sull'hub 1. Gap euristica $5{,}3\%$.

| $\mathrm{ub}$ | $\mathrm{lb}$ (duale) | $z(\mathrm{LP})$ | $z(\mathrm{LP}^+)$ | $z(\mathrm{MILP})$ | gap |
|---:|---:|---:|---:|---:|---:|
| 20 | $15/2$ | $25/2$ | $1015/78$ | 19 | $5{,}3\%$ |

![Soluzione ottima](img/cap08_hub_ottimo.png)

## Considerazioni aggiuntive

- $x_{ij} \le y_j$ (disaggregato) è implicato dal vincolo aggregato di
  attivazione.
- Con $M_j=\max_i c_{ij}$, $z_j \le M_j y_j$ non è una disuguaglianza
  valida (il modello ammette $z_j>0$ con $y_j=0$), ma è un **vincolo che
  preserva l'ottimalità**: minimizzando $z_j$, l'ottimo la annulla comunque
  quando $y_j=0$.

## Domande di modellazione aggiuntive

??? question "8.4.1 — Link di attivazione disaggregato"
    Si sostituisca il vincolo aggregato con $x_{ij} \le y_j$. Cambia
    l'ottimo?

    ??? success "Soluzione"
        $x_{ij} \le y_j$ per ogni $i,j$ ($n\,m$ vincoli in più). L'ottimo
        resta $19$: la soluzione ottima già lo soddisfa.

??? question "8.4.2 — Connessione vietata"
    Il terminale 1 non può connettersi all'hub 2. Come si modella? Qual è
    il nuovo ottimo?

    ??? success "Soluzione"
        $x_{12}=0$. L'ottimo non la usa già (terminale 1 sull'hub 3):
        resta $19$.

## Codice

Script completo —
[`python/fam08_4_hub.py`](https://github.com/fabiofurini/modellazione-mip/blob/main/python/fam08_4_hub.py)
(riproducibile con `python3 python/fam08_4_hub.py` dalla cartella
`python/`, richiama `next_fit` da `euristiche.py`). Notebook —
[`notebooks/fam08_4_hub.ipynb`](https://github.com/fabiofurini/modellazione-mip/blob/main/notebooks/fam08_4_hub.ipynb)
— che si apre in Colab dal badge in cima alla pagina.
