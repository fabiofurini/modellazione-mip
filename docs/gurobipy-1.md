# 3.1 Scrivere un modello in gurobipy

**Classe:** implementazione · **Script:** `python/cap06_gurobi.py`
{ .scheda }

Le otto istruzioni che bastano per scrivere un modello, le quattro classi di
variabili e la regola del corso: una famiglia di vincoli per blocco, con i nomi
del modello matematico.

## Le otto istruzioni che bastano

Un modello si scrive in gurobipy con otto istruzioni, sempre le stesse, e da qui
in poi accanto a ogni modello comparirà la riga di codice che lo scrive. Conviene
vederle una volta su un modello piccolo e completo: lo **zaino binario**, dove di
$n$ oggetti di valore $p_j$ e peso $w_j$ si sceglie un sottoinsieme di peso al
più $c$ che valga il più possibile.

$$
\begin{aligned}
\max ~~ \sum_{j=1}^{n} p_j\, x_j & &\\
\text{soggetto a} \quad \sum_{j=1}^{n} w_j\, x_j &\le c, &\\
x_j &\in \{0, 1\}, & \forall j \in \{1, 2, \dots, n\}.
\end{aligned}
$$

```python
import gurobipy as gp                       # il modulo, sempre abbreviato gp
from gurobipy import GRB                    # le costanti: GRB.BINARY, GRB.MAXIMIZE...

p = [10, 7, 6, 4]                           # valori
w = [5, 4, 3, 3]                            # pesi
c = 9                                       # capacita'
n = len(p)

m = gp.Model("zaino")                                        # un modello vuoto
x = m.addVars(n, vtype=GRB.BINARY, name="x")                 # n variabili binarie
m.setObjective(gp.quicksum(p[j] * x[j] for j in range(n)), GRB.MAXIMIZE)
m.addConstr(gp.quicksum(w[j] * x[j] for j in range(n)) <= c, name="capacita")
m.optimize()
```

Otto istruzioni, una per riga del modello:

- `Model` crea il modello; tutto il resto si appende a lui.
- `addVars` aggiunge un'intera famiglia indicizzata: `addVars(n)` dà
  $x_0, \dots, x_{n-1}$, `addVars(n, k)` la matrice $x_{ij}$, e si indicizzano
  con `x[j]` e `x[i, j]`. Per una variabile sola c'è `addVar`. Gli indici di
  Python partono da zero, nei modelli scritti partono da uno: è la sola
  differenza da tenere a mente.
- `vtype` dichiara il dominio: `GRB.BINARY`, `GRB.INTEGER`, e senza `vtype` la
  variabile è continua e non negativa. Il dominio è un vincolo: dichiararlo male
  è dichiarare un altro modello.
- `quicksum` costruisce una somma $\sum_j c_j x_j$ senza espressioni intermedie.
- `setObjective` prende l'espressione e il verso, `GRB.MINIMIZE` o
  `GRB.MAXIMIZE`.
- `addConstr` aggiunge *un* vincolo, `addConstrs` una famiglia, e vuole un
  generatore fra parentesi tonde: una riga di codice per una famiglia, com'è una
  riga sola nel modello scritto.
- `optimize` risolve.

Con le stesse otto istruzioni si scrivono gli altri problemi classici che tornano
in queste pagine. Il **bin packing** — $n$ oggetti di dimensione $w_j$ in
contenitori di capacità $c$, usandone il meno possibile — vuole due famiglie di
binarie, $x_{ji}$ e $y_i$, e due famiglie di vincoli:

```python
x = m.addVars(n, k, vtype=GRB.BINARY, name="x")
y = m.addVars(k, vtype=GRB.BINARY, name="y")
m.setObjective(y.sum(), GRB.MINIMIZE)
m.addConstrs((x.sum(j, "*") == 1 for j in range(n)), name="assegna")
m.addConstrs((gp.quicksum(w[j] * x[j, i] for j in range(n)) <= c * y[i]
              for i in range(k)), name="capacita")
```

Lo **scheduling su macchine identiche** ($P||z$) cambia solo l'obiettivo e
un vincolo: una continua $T$ per il makespan, $\min T$, e
$\sum_j t_j x_{ji} \le T$ per ogni macchina. Il **commesso viaggiatore** ha una
binaria per arco, $x_{ij}$, e due famiglie di uguaglianze — da ogni città si
parte una volta e in ogni città si arriva una volta — più i vincoli che
impediscono i sottogiri.

## Le quattro classi di variabili

| Che cosa | `vtype` | Dominio | Uso tipico |
|---|---|---|---|
| decisione sì/no | `GRB.BINARY` | $\{0,1\}$ | selezione, attivazione, assegnamento |
| conteggio | `GRB.INTEGER` | $\mathbb{Z}$ fra `lb` e `ub` | scatole, turni, operai |
| quantità misurabile | (default) | $[\mathit{LB}, \mathit{UB}] \subseteq \mathbb{R}$ | tempo, denaro, flusso |
| variabile libera | (default) con `lb=-GRB.INFINITY` | $\mathbb{R}$ | duali di uguaglianze |

!!! warning "I due default che si dimenticano"
    `GRB.BINARY` implica già `lb = 0` e `ub = 1`: non serve ripeterli. Una
    variabile continua ha `lb = 0` per default: una variabile che deve poter
    essere negativa — tipicamente un duale di uguaglianza, o una deviazione con
    segno — va dichiarata con `lb=-GRB.INFINITY`, altrimenti il modello è
    silenziosamente sbagliato.

## Il modello, una famiglia per blocco

```python
def modello(t, c, a):
    """Un assegnamento: una addConstrs per famiglia, con il nome dell'etichetta."""
    m = gp.Model("assegnamento");  m.Params.OutputFlag = 0
    x = m.addVars(n, k, vtype=GRB.BINARY, name="x")           # dati -> variabili
    m.setObjective(gp.quicksum(c[j][h] * x[j, h] for j in range(n)
                               for h in range(k)), GRB.MINIMIZE)
    m.addConstrs((x.sum(j, "*") == 1 for j in range(n)), name="assegna")
    m.addConstrs((gp.quicksum(t[j][h] * x[j, h] for j in range(n)) <= a[h]
                  for h in range(k)), name="disponibilita")
    return m, x
```

Le tre regole di scrittura del corso: **una `addConstrs` per famiglia**,
nell'ordine del modello matematico, con il `name` uguale all'etichetta; **le
variabili si dichiarano tutte insieme** con `addVars` e gli indici del modello
(`x.sum(j, "*")` è la scrittura dell'indice muto); **i dati arrivano come
argomenti**, non come variabili globali, così la stessa funzione serve per
l'istanza base e per tutte le varianti.

Il modello ha $9$ variabili, $6$ vincoli e $18$ coefficienti non nulli. Per
controllare che sia quello scritto sulla carta, `m.write("modello.lp")`:

```text
Minimize
  5 x[0,0] + 10 x[0,1] + 2 x[0,2] + 5 x[1,0] + 4 x[1,1] + 6 x[1,2]
   + 5 x[2,0] + 4 x[2,1] + 6 x[2,2]
Subject To
 assegna[0]: x[0,0] + x[0,1] + x[0,2] = 1
 ...
```

È il modo più rapido per accorgersi di un coefficiente sbagliato: il tabulare
dell'istanza e questo output devono coincidere riga per riga.
