# 3. Dal modello a Python/Gurobi

**Classe:** implementazione · **Script:** `python/cap06_gurobi.py`
{ .scheda }

[![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/cap06_gurobi.ipynb)

Il corso usa **un solo solver**, Gurobi da Python. La pagina ha tre parti: come
si **scrive** un modello — una famiglia di vincoli per blocco, con i nomi del
modello matematico; come si **leggono** i risultati, incluso il caso in cui il
solver non ha finito; e tre **modelli completi** — bin packing, makespan e
commesso viaggiatore — scritti dall'enunciato fino all'istanza, che il
[capitolo delle euristiche](modellazione-4.md) riprende.

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

## Leggere i risultati

L'ordine di lettura non si cambia: `Status`, poi `SolCount`, poi `ObjVal` e
`ObjBound`, poi `MIPGap`, `NodeCount`, `Runtime`.

| `Status` | valore | `SolCount` | Che cosa si può dire |
|---|---:|---:|---|
| `OPTIMAL` | 2 | $\ge 1$ | $z(\mathit{MILP}) = $ `ObjVal`, dimostrato |
| `INFEASIBLE` | 3 | 0 | il modello non ha soluzioni ammissibili |
| `UNBOUNDED` | 5 | 0 | manca un vincolo, o un bound su una variabile |
| `TIME_LIMIT` | 9 | 0 | niente: né una soluzione né, in generale, un bound utile |
| `TIME_LIMIT` | 9 | $\ge 1$ | `ObjBound` $\le z(\mathit{MILP}) \le$ `ObjVal` |
| `SOLUTION_LIMIT` | 10 | $\ge 1$ | come sopra |

!!! example "I quattro casi sull'istanza di assegnamento"
    - **Risoluzione normale.** `Status = 2`, `SolCount = 2`,
      `ObjVal = ObjBound = 11`, `MIPGap = 0`, `NodeCount = 0`.
    - **Inammissibile.** Con disponibilità $(1,1,1)$: `Status = 3`,
      `SolCount = 0`.
    - **Fermato subito.** Con `TimeLimit = 0`: `Status = 9`, `SolCount = 0`,
      `ObjBound` $= -\infty$. Non c'è nulla da riportare.
    - **Fermato alla prima soluzione.** Con `SolutionLimit = 1`: `Status = 10`,
      `SolCount = 1`, `ObjVal = 12`, `ObjBound = 10`, `MIPGap = 0,1667`. Questo
      è il caso in cui si riporta un **intervallo**: l'ottimo sta fra $10$ e
      $12$. Dire «l'ottimo è $12$» sarebbe falso.

!!! danger "Che cosa *non* si riporta"
    Non si scrive «l'ottimo è `ObjVal`» se `Status` non è `OPTIMAL`. Non si
    scrive un gap se `SolCount` è $0$. Non si confronta il `Runtime` di due
    modelli risolti con impostazioni diverse. E non si legge `ObjBound` a fine
    risoluzione pensando di leggere il rilassamento della radice: per quello
    serve `relax()`.

## Le tolleranze

| Parametro | Default | Significato |
|---|---:|---|
| `IntFeasTol` | $10^{-5}$ | quanto una variabile intera può distare da un intero |
| `FeasibilityTol` | $10^{-6}$ | violazione ammessa su un vincolo lineare |
| `OptimalityTol` | $10^{-6}$ | tolleranza sui costi ridotti |
| `MIPGap` | $10^{-4}$ | gap relativo sotto il quale il solver si ferma |

!!! warning "«Intero» significa «intero entro una tolleranza»"
    Una binaria può tornare come $0{,}9999999997$. Nel testo si scrive $1$: i
    valori si arrotondano *quando si riportano*, e i confronti si fanno sempre
    con una tolleranza — nel corso $10^{-6}$, la costante `TOL` di
    `python/mip.py`. Scrivere `if x.X == 1` è un errore; si scrive
    `if x.X > 0.5`.

    Il default `MIPGap` $= 10^{-4}$ significa anche che il solver può fermarsi
    *prima* dell'ottimo esatto dichiarando `OPTIMAL`: su istanze con valori
    grandi vale la pena abbassarlo.

## Il rilassamento con `relax()`

```python
m.update()            # relax() copia il modello: le modifiche pendenti vanno applicate prima
r = m.relax()         # le binarie diventano 0 <= x <= 1, le intere x >= lb
r.Params.OutputFlag = 0
r.optimize()
zlp = r.ObjVal
duali = {c.ConstrName: c.Pi for c in r.getConstrs()}
```

Su quell'istanza, $z(\mathit{LP}^+) = z(\mathit{LP}) = 53/5$ — i
due rilassamenti coincidono perché i vincoli di assegnamento implicano già
$x_{jm} \le 1$ — e i duali non nulli sono $\tilde\mu = (2,\ 4{,}8,\ 5)$ e
$\tilde\pi_2 = -0{,}2$: la macchina 2 è la sola risorsa stretta.

## Tre problemi che il corso riusa

Fin qui il modello di esempio è sempre stato lo zaino. I tre problemi qui sotto
ritornano nel [capitolo delle euristiche](modellazione-4.md), dove si
costruiscono a mano le soluzioni di next-fit, first-fit, best-fit, LPT e vicino
più vicino: qui si scrivono i loro modelli, così quelle euristiche hanno un
ottimo con cui confrontarsi.

### Bin packing: quanti contenitori bastano

!!! abstract "Bin packing"
    Ci sono $n$ oggetti, l'oggetto $j$ pesa $w_j$. I contenitori sono tutti
    uguali, di capacità $c$. Si usi il minimo numero di contenitori.

#### Il modello

Servono due famiglie di variabili binarie: $x_{jb} = 1$ se l'oggetto $j$ va nel
contenitore $b$, e $y_b = 1$ se il contenitore $b$ viene usato.

$$
\begin{aligned}
\min ~~ \sum_{b=1}^{k} y_b & &\\
\text{soggetto a} \quad \sum_{b=1}^{k} x_{jb} &= 1, & \forall j \in \{1, 2, \dots, n\},\\
\sum_{j=1}^{n} w_j\, x_{jb} - c\, y_b &\le 0, & \forall b \in \{1, 2, \dots, k\},\\
x_{jb} &\in \{0, 1\}, & \forall j \in \{1, 2, \dots, n\},\ \forall b \in \{1, 2, \dots, k\},\\
y_b &\in \{0, 1\}, & \forall b \in \{1, 2, \dots, k\}.
\end{aligned}
$$

La prima famiglia dice che ogni oggetto finisce in esattamente un contenitore.
La seconda è la capacità scritta come **attivazione**: finché $y_b = 0$ il
contenitore $b$ non può ricevere niente, e appena $y_b = 1$ accoglie fino a $c$.
L'obiettivo conta i contenitori accesi.

#### La costruzione in gurobipy

```python
def modello_bpp(w, c, k):
    n = len(w)
    m = nuovo_modello("bin_packing")
    x = m.addVars(n, k, vtype=GRB.BINARY, name="x")
    y = m.addVars(k, vtype=GRB.BINARY, name="y")
    m.setObjective(y.sum(), GRB.MINIMIZE)
    m.addConstrs((x.sum(j, "*") == 1 for j in R(n)), name="oggetto")
    m.addConstrs((gp.quicksum(w[j] * x[j, b] for j in R(n)) <= c * y[b]
                  for b in R(k)), name="capacita")
    return m, x, y
```

#### L'istanza

Sull'istanza di quattro oggetti di peso $w = (5, 4, 3, 3)$ e capacità $c = 7$:

<!-- modello-esteso: cap06_bpp -->

<div class="modello-esteso largo" markdown>

$$
\begin{array}{rrrrrrrrrrrrrrrr c l}
\min &  &  &  &  &  &  &  &  &  &  &  &  & y_1 & +y_2 & +y_3 &  & \\
\text{soggetto a} & x_{11} & +x_{12} & +x_{13} &  &  &  &  &  &  &  &  &  &  &  &  & = & 1\\
 &  &  &  & x_{21} & +x_{22} & +x_{23} &  &  &  &  &  &  &  &  &  & = & 1\\
 &  &  &  &  &  &  & x_{31} & +x_{32} & +x_{33} &  &  &  &  &  &  & = & 1\\
 &  &  &  &  &  &  &  &  &  & x_{41} & +x_{42} & +x_{43} &  &  &  & = & 1\\
 & 5x_{11} &  &  & +4x_{21} &  &  & +3x_{31} &  &  & +3x_{41} &  &  & -7y_1 &  &  & \le & 0\\
 &  & 5x_{12} &  &  & +4x_{22} &  &  & +3x_{32} &  &  & +3x_{42} &  &  & -7y_2 &  & \le & 0\\
 &  &  & 5x_{13} &  &  & +4x_{23} &  &  & +3x_{33} &  &  & +3x_{43} &  &  & -7y_3 & \le & 0\\
 & x_{11}, & x_{12}, & x_{13}, & x_{21}, & x_{22}, & x_{23}, & x_{31}, & x_{32}, & x_{33}, & x_{41}, & x_{42}, & x_{43} &  &  &  & \in & \{0, 1\}\\
 &  &  &  &  &  &  &  &  &  &  &  &  & y_1, & y_2, & y_3 & \in & \{0, 1\}
\end{array}
$$

</div>

<!-- modello-esteso: fine -->

Il peso totale è $15$, quindi nessuna soluzione può usare meno di
$\lceil 15/7 \rceil = 3$ contenitori; l'ottimo ne usa esattamente $3$, e il
conteggio è quindi stretto.

!!! warning "Il rilassamento del bin packing è debolissimo"
    Rilassando $y_b$ a $y_b \ge 0$ il modello compra frazioni di contenitore, e
    l'ottimo dell'LP scende a $\sum_j w_j / c = 15/7 \approx 2{,}14$: il rilassamento
    non sa che un contenitore si apre tutto intero. È il motivo per cui su questo
    problema il bound duale è poco utile e le euristiche contano di più.

### Makespan: il carico della macchina più carica

!!! abstract "Makespan su macchine identiche"
    Ci sono $n$ lavori, di durata $d_j$, e $k$ macchine identiche. Ogni lavoro va
    su una macchina sola e non si interrompe. Si minimizzi l'istante in cui
    l'ultima macchina finisce.

#### Il modello

Con $x_{jm} = 1$ se il lavoro $j$ va sulla macchina $m$, e $z \ge 0$ il carico
della macchina più carica:

$$
\begin{aligned}
\min ~~ z & &\\
\text{soggetto a} \quad \sum_{m=1}^{k} x_{jm} &= 1, & \forall j \in \{1, 2, \dots, n\},\\
\sum_{j=1}^{n} d_j\, x_{jm} - z &\le 0, & \forall m \in \{1, 2, \dots, k\},\\
x_{jm} &\in \{0, 1\}, & \forall j \in \{1, 2, \dots, n\},\ \forall m \in \{1, 2, \dots, k\},\\
z &\ge 0. &
\end{aligned}
$$

L'obiettivo è la sola variabile $z$: nessun dato vi compare. Sono le $k$ righe di
carico a darle significato, dicendo che nessuna macchina lavora più a lungo di
$z$; il minimo la schiaccia allora sul carico della macchina più carica.
È la tecnica [min-max](legami-06.md).

#### La costruzione in gurobipy

```python
def modello_cmax(d, k):
    n = len(d)
    m = nuovo_modello("makespan")
    x = m.addVars(n, k, vtype=GRB.BINARY, name="x")
    z = m.addVar(name="z")
    m.setObjective(z, GRB.MINIMIZE)
    m.addConstrs((x.sum(j, "*") == 1 for j in R(n)), name="lavoro")
    m.addConstrs((gp.quicksum(d[j] * x[j, mm] for j in R(n)) <= z
                  for mm in R(k)), name="carico")
    return m, x, z
```

#### L'istanza

Sull'istanza di sette lavori di durata $d = (5, 5, 4, 4, 3, 3, 3)$ su $k = 3$
macchine:

<!-- modello-esteso: cap06_cmax -->

<div class="modello-esteso largo" markdown>

$$
\begin{array}{rrrrrrrrrrrrrrrrrrrrrrr c l}
\min &  &  &  &  &  &  &  &  &  &  &  &  &  &  &  &  &  &  &  &  &  & z &  & \\
\text{soggetto a} & x_{11} & +x_{12} & +x_{13} &  &  &  &  &  &  &  &  &  &  &  &  &  &  &  &  &  &  &  & = & 1\\
 &  &  &  & x_{21} & +x_{22} & +x_{23} &  &  &  &  &  &  &  &  &  &  &  &  &  &  &  &  & = & 1\\
 &  &  &  &  &  &  & x_{31} & +x_{32} & +x_{33} &  &  &  &  &  &  &  &  &  &  &  &  &  & = & 1\\
 &  &  &  &  &  &  &  &  &  & x_{41} & +x_{42} & +x_{43} &  &  &  &  &  &  &  &  &  &  & = & 1\\
 &  &  &  &  &  &  &  &  &  &  &  &  & x_{51} & +x_{52} & +x_{53} &  &  &  &  &  &  &  & = & 1\\
 &  &  &  &  &  &  &  &  &  &  &  &  &  &  &  & x_{61} & +x_{62} & +x_{63} &  &  &  &  & = & 1\\
 &  &  &  &  &  &  &  &  &  &  &  &  &  &  &  &  &  &  & x_{71} & +x_{72} & +x_{73} &  & = & 1\\
 & 5x_{11} &  &  & +5x_{21} &  &  & +4x_{31} &  &  & +4x_{41} &  &  & +3x_{51} &  &  & +3x_{61} &  &  & +3x_{71} &  &  & -z & \le & 0\\
 &  & 5x_{12} &  &  & +5x_{22} &  &  & +4x_{32} &  &  & +4x_{42} &  &  & +3x_{52} &  &  & +3x_{62} &  &  & +3x_{72} &  & -z & \le & 0\\
 &  &  & 5x_{13} &  &  & +5x_{23} &  &  & +4x_{33} &  &  & +4x_{43} &  &  & +3x_{53} &  &  & +3x_{63} &  &  & +3x_{73} & -z & \le & 0\\
 & x_{11}, & x_{12}, & x_{13}, & x_{21}, & x_{22}, & x_{23}, & x_{31}, & x_{32}, & x_{33}, & x_{41}, & x_{42}, & x_{43}, & x_{51}, & x_{52}, & x_{53}, & x_{61}, & x_{62}, & x_{63}, & x_{71}, & x_{72}, & x_{73} &  & \in & \{0, 1\}\\
 &  &  &  &  &  &  &  &  &  &  &  &  &  &  &  &  &  &  &  &  &  & z & \ge & 0
\end{array}
$$

</div>

<!-- modello-esteso: fine -->

Il carico totale è $27$ e le macchine sono tre: nessuna soluzione può scendere
sotto $27/3 = 9$, e l'ottimo vale esattamente $9$ — i lavori si dividono in tre
gruppi da $9$. Qui il conteggio chiude il problema da solo.

### Commesso viaggiatore: la formulazione MTZ

!!! abstract "Commesso viaggiatore"
    Ci sono $n$ città e una distanza $d_{ij}$ fra ogni coppia. Si trovi il giro
    di lunghezza minima che tocca ogni città esattamente una volta e torna al
    punto di partenza.

#### Il modello

Con $x_{ij} = 1$ se il giro va da $i$ a $j$, le due famiglie «si esce una volta»
e «si entra una volta» non bastano: ammettono anche soluzioni fatte di
**sottocicli** separati. La formulazione di Miller–Tucker–Zemlin aggiunge una
variabile $u_i$ per ogni città diversa dalla prima, che ne registra la posizione
lungo il giro.

$$
\begin{aligned}
\min ~~ \sum_{i=1}^{n} \sum_{j \ne i} d_{ij}\, x_{ij} & &\\
\text{soggetto a} \quad \sum_{j \ne i} x_{ij} &= 1, & \forall i \in \{1, 2, \dots, n\},\\
\sum_{i \ne j} x_{ij} &= 1, & \forall j \in \{1, 2, \dots, n\},\\
u_i - u_j + n\, x_{ij} &\le n - 1, & \forall i, j \in \{2, 3, \dots, n\},\ i \ne j,\\
x_{ij} &\in \{0, 1\}, & \forall i, j \in \{1, 2, \dots, n\},\ i \ne j,\\
u_i &\in [1,\, n-1], & \forall i \in \{2, 3, \dots, n\}.
\end{aligned}
$$

Il terzo gruppo è il cuore della formulazione. Se $x_{ij} = 0$ la riga diventa
$u_i - u_j \le n - 1$, sempre vera perché le $u$ stanno fra $1$ e $n-1$: non
vieta niente. Se invece $x_{ij} = 1$ diventa $u_j \ge u_i + 1$, cioè «se vado da
$i$ a $j$, la posizione di $j$ è la successiva». Un sottociclo che non tocca la
città $1$ richiederebbe una catena di posizioni sempre crescenti che si richiude
su se stessa, e questo è impossibile; la città $1$ non ha la sua $u$ proprio
perché è il punto in cui il giro si chiude.

#### La costruzione in gurobipy

```python
def modello_tsp(D):
    n = len(D)
    m = nuovo_modello("tsp")
    x = m.addVars(((i, j) for i in R(n) for j in R(n) if i != j),
                  vtype=GRB.BINARY, name="x")
    u = m.addVars(R(1, n), lb=1, ub=n - 1, name="u")
    m.setObjective(gp.quicksum(D[i][j] * x[i, j] for i, j in x), GRB.MINIMIZE)
    m.addConstrs((gp.quicksum(x[i, j] for j in R(n) if j != i) == 1
                  for i in R(n)), name="esce")
    m.addConstrs((gp.quicksum(x[i, j] for i in R(n) if i != j) == 1
                  for j in R(n)), name="entra")
    m.addConstrs((u[i] - u[j] + n * x[i, j] <= n - 1
                  for i in R(1, n) for j in R(1, n) if i != j), name="mtz")
    return m, x, u
```

#### L'istanza

Sull'istanza di quattro città del
[capitolo delle euristiche](modellazione-4.md) il giro ottimo è
$1 \to 2 \to 4 \to 3 \to 1$ e misura $22$. Il modello dell'istanza ha quindici
colonne — dodici archi e tre posizioni — e quattordici righe:

<!-- modello-esteso: cap06_tsp -->

<div class="modello-esteso largo" markdown>

$$
\begin{array}{rrrrrrrrrrrrrrrr c l}
\min & 4x_{12} & +5x_{13} & +9x_{14} & +4x_{21} & +9x_{23} & +9x_{24} & +5x_{31} & +9x_{32} & +4x_{34} & +9x_{41} & +9x_{42} & +4x_{43} &  &  &  &  & \\
\text{soggetto a} & x_{12} & +x_{13} & +x_{14} &  &  &  &  &  &  &  &  &  &  &  &  & = & 1\\
 &  &  &  & x_{21} & +x_{23} & +x_{24} &  &  &  &  &  &  &  &  &  & = & 1\\
 &  &  &  &  &  &  & x_{31} & +x_{32} & +x_{34} &  &  &  &  &  &  & = & 1\\
 &  &  &  &  &  &  &  &  &  & x_{41} & +x_{42} & +x_{43} &  &  &  & = & 1\\
 &  &  &  & x_{21} &  &  & +x_{31} &  &  & +x_{41} &  &  &  &  &  & = & 1\\
 & x_{12} &  &  &  &  &  &  & +x_{32} &  &  & +x_{42} &  &  &  &  & = & 1\\
 &  & x_{13} &  &  & +x_{23} &  &  &  &  &  &  & +x_{43} &  &  &  & = & 1\\
 &  &  & x_{14} &  &  & +x_{24} &  &  & +x_{34} &  &  &  &  &  &  & = & 1\\
 &  &  &  &  & 4x_{23} &  &  &  &  &  &  &  & +u_2 & -u_3 &  & \le & 3\\
 &  &  &  &  &  & 4x_{24} &  &  &  &  &  &  & +u_2 &  & -u_4 & \le & 3\\
 &  &  &  &  &  &  &  & 4x_{32} &  &  &  &  & -u_2 & +u_3 &  & \le & 3\\
 &  &  &  &  &  &  &  &  & 4x_{34} &  &  &  &  & +u_3 & -u_4 & \le & 3\\
 &  &  &  &  &  &  &  &  &  &  & 4x_{42} &  & -u_2 &  & +u_4 & \le & 3\\
 &  &  &  &  &  &  &  &  &  &  &  & 4x_{43} &  & -u_3 & +u_4 & \le & 3\\
 & x_{12}, & x_{13}, & x_{14}, & x_{21}, & x_{23}, & x_{24}, & x_{31}, & x_{32}, & x_{34}, & x_{41}, & x_{42}, & x_{43} &  &  &  & \in & \{0, 1\}\\
 &  &  &  &  &  &  &  &  &  &  &  &  & u_2, & u_3, & u_4 & \ge & 1
\end{array}
$$

</div>

<!-- modello-esteso: fine -->

!!! warning "MTZ è comoda, non è la più forte"
    I vincoli MTZ sono $O(n^2)$ e si scrivono in tre righe di `gurobipy`, ma il
    loro rilassamento lineare è debole: le $u$ continue assorbono quasi tutto e
    l'LP si avvicina poco all'ottimo intero. Le formulazioni che eliminano i
    sottocicli con i tagli di connessione danno bound molto migliori, al prezzo
    di un numero esponenziale di vincoli da generare a mano a mano. Per le
    dimensioni di questo corso MTZ basta.

## Il protocollo del corso, dall'inizio alla fine

$$\text{dati} \to \text{modello} \to \text{euristica e verifica} \to \text{LP e duale} \to \text{MIP} \to \text{tabella} \to \text{figure e notebook}$$

```python
m, x = modello(t, c, a)                                  # (1) dati, (2) modello

e = best_fit(t, a, lambda j, h, ra: c[j][h], "costo")    # (3) euristica
ub = sum(c[j][h] for (j, h) in e.x)
assert ammissibile(m, {f"x[{j},{h}]": 1 for (j, h) in e.x})   # vincoli, bound E interezza

d = duale(t, c, a)                                       # (4) duale scritto a mano
mano = {f"mu[{j}]": min(c[j]) for j in range(n)}
lb, viol = valuta(d, mano);  assert viol <= 1e-9
zlp, zlp_raff, pi = due_rilassamenti(m, d)               #     controlla la dualita' forte

z = risolvi(m)                                           # (5) il MIP
riga = registra_bound("7.1 assegnamento", ub, lb, zlp, zlp_raff, z)   # (6) la tabella
salva_dati(pd.DataFrame([riga]), "fam07_1_bound")         #     -> dati/fam07_1_bound.csv
```

Sull'istanza di assegnamento il protocollo produce $\mathit{LB} = 10$,
$z(\mathit{LP}) = 53/5$, $z(\mathit{MILP}) = 11$, $\mathit{UB} = 11$, e la riga
finisce in `dati/fam07_1_bound.csv`. Da lì la leggono la dispensa, la pagina del
sito e `verifica_numeri.py`: **un solo posto in cui il numero esiste**.

![I quattro numeri del protocollo](img/cap06_protocollo.png)

## Eseguire il codice

Dalla cartella `python/`:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install gurobipy pandas matplotlib
python3 fam07_1_assegnamento.py     # un capitolo
python3 esegui_tutti.py             # tutti, piu' i notebook
python3 verifica_numeri.py          # gli assert su ogni numero citato
```

Su Colab ogni capitolo ha un notebook che si apre dal badge in cima alla pagina:
la prima cella installa `gurobipy` e scarica i tre moduli comuni.

!!! tip "La licenza inclusa in `gurobipy` basta, e perché"
    La licenza *size-limited* del pacchetto pip permette modelli fino a **2000
    variabili e 2000 vincoli**. Le istanze di questo corso sono piccolissime — il
    modello più grande del corso ha poche decine di variabili — e ci stanno
    tutte con enorme margine. Per istanze più grandi si attiva gratuitamente la
    licenza accademica da [portal.gurobi.com](https://portal.gurobi.com). Se un
    modello supera il limite, Gurobi lo segnala con un errore esplicito
    all'atto di `optimize()`: non produce silenziosamente un risultato sbagliato.

## Codice

Lo script completo è
[`python/cap06_gurobi.py`](https://github.com/fabiofurini/modellazione-mip/blob/main/python/cap06_gurobi.py);
il notebook è
[`notebooks/cap06_gurobi.ipynb`](https://github.com/fabiofurini/modellazione-mip/blob/main/notebooks/cap06_gurobi.ipynb).

<!-- script-incorporato: inizio (rigenerato da python/incorpora_codice.py) -->

??? example "Mostra lo script completo — `python/cap06_gurobi.py` (309 righe)"

    ```python
    """Capitolo 3 -- Dal modello a Python/Gurobi: come si scrive e come si legge.

    Le quattro classi di variabili, una addConstrs per famiglia di vincoli, e
    soprattutto la lettura dei risultati: Status, SolCount, ObjVal, ObjBound,
    MIPGap, NodeCount, il limite di tempo, le tolleranze e relax(). Chiude con il
    protocollo completo del corso su un'istanza minima.
    """
    import gurobipy as gp
    import pandas as pd
    from gurobipy import GRB

    from euristiche import best_fit
    from mip import (ammissibile, due_rilassamenti, frazione, nuovo_modello, registra_bound,
                     rilassamento, risolvi, stampa_lp, stampa_soluzione, valuta, viola_interezza)
    from esteso import salva_modello
    from stile import (ARANCIO, BLU, CICLO, GRIGIO, ROSSO, TEAL, VERDE, intestazione,
                       plt, salva_dati, salva_figura)

    R = range

    # ---------- 1. LE QUATTRO CLASSI DI VARIABILI ----------
    intestazione("1. Le quattro classi di variabili e i loro domini")
    m = nuovo_modello("tipi_di_variabile")
    b = m.addVar(vtype=GRB.BINARY, name="binaria")
    i = m.addVar(vtype=GRB.INTEGER, lb=0, ub=10, name="intera")
    c = m.addVar(lb=0.0, ub=GRB.INFINITY, name="continua")
    l = m.addVar(lb=-GRB.INFINITY, ub=GRB.INFINITY, name="libera")
    m.update()
    for v in m.getVars():
        print(f"  {v.VarName:9s} VType = {v.VType}   lb = {v.LB:>6.1f}   ub = "
              f"{'+inf' if v.UB >= GRB.INFINITY else f'{v.UB:.1f}':>6s}")
    print("  GRB.BINARY implica gia' lb = 0 e ub = 1: non serve dichiararli.")
    print("  Una variabile continua ha lb = 0 per default: le variabili libere vanno")
    print("  dichiarate esplicitamente con lb = -GRB.INFINITY (i duali di un'uguaglianza).")

    # ---------- 2. UN MODELLO, UNA FAMIGLIA DI VINCOLI ALLA VOLTA ----------
    intestazione("2. Il modello si scrive una famiglia di vincoli per blocco")
    t = [[2, 1, 3], [3, 4, 2], [4, 5, 3]]
    co = [[5, 10, 2], [5, 4, 6], [5, 4, 6]]
    a = [5, 6, 7]
    n, k = 3, 3


    def modello(t, co, a):
        """Un assegnamento: una addConstrs per famiglia, con il nome dell'etichetta."""
        mm = nuovo_modello("assegnamento")
        x = mm.addVars(n, k, vtype=GRB.BINARY, name="x")          # dati -> variabili
        mm.setObjective(gp.quicksum(co[j][h] * x[j, h] for j in R(n) for h in R(k)), GRB.MINIMIZE)
        mm.addConstrs((x.sum(j, "*") == 1 for j in R(n)), name="assegna")
        mm.addConstrs((gp.quicksum(t[j][h] * x[j, h] for j in R(n)) <= a[h] for h in R(k)),
                      name="disponibilita")
        return mm, x


    m2, x2 = modello(t, co, a)
    m2.update()
    print(f"  Variabili: {m2.NumVars}   vincoli: {m2.NumConstrs}   non zeri: {m2.NumNZs}")
    print("  Nomi dei vincoli (le stesse etichette del modello matematico):")
    print("   " + ", ".join(cc.ConstrName for cc in m2.getConstrs()))
    print("  Il modello dell'istanza in formato LP, per controllare i tabulari della dispensa:")
    import io
    import os
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        percorso = os.path.join(d, "modello.lp")
        m2.write(percorso)
        testo_lp = open(percorso).read()
    for riga in [r for r in testo_lp.splitlines() if r.strip()][:8]:
        print("    " + riga)
    print("    ...")

    # ---------- 3. LEGGERE I RISULTATI: IL CASO NORMALE ----------
    intestazione("3. Leggere i risultati quando tutto va bene")
    m2.optimize()
    print(f"  Status   = {m2.Status}   (2 = OPTIMAL)")
    print(f"  SolCount = {m2.SolCount}   (quante soluzioni intere sono state trovate)")
    print(f"  ObjVal   = {frazione(m2.ObjVal)}   ObjBound = {frazione(m2.ObjBound)}   "
          f"MIPGap = {m2.MIPGap:.6f}")
    print(f"  NodeCount = {int(m2.NodeCount)}   Runtime = {m2.Runtime:.3f} s")
    print("  Soluzione ottima (solo le variabili non nulle):")
    stampa_soluzione(m2, solo_non_nulle=True)
    z_ott = m2.ObjVal

    # ---------- 4. LEGGERE I RISULTATI QUANDO NON VA BENE ----------
    intestazione("4. I tre casi in cui ObjVal non si puo' leggere")
    # (a) inammissibile
    m3, x3 = modello(t, co, [1, 1, 1])          # disponibilita' insufficienti
    m3.optimize()
    print(f"  (a) disponibilita' (1,1,1): Status = {m3.Status} (3 = INFEASIBLE), "
          f"SolCount = {m3.SolCount}")
    print("      ObjVal non esiste: leggerlo solleva un errore. Si legge Status, sempre prima.")
    assert m3.Status == GRB.INFEASIBLE
    # (b) limite di tempo con nessuna soluzione trovata
    m4, x4 = modello(t, co, a)
    m4.Params.TimeLimit = 0.0
    m4.optimize()
    print(f"  (b) TimeLimit = 0: Status = {m4.Status} (9 = TIME_LIMIT), SolCount = {m4.SolCount}")
    print(f"      ObjBound = {m4.ObjBound if m4.ObjBound > -GRB.INFINITY else '-inf'}: "
          f"nemmeno il bound e' stato calcolato.")
    # (c) limite di tempo con una soluzione trovata: il caso utile
    m5, x5 = modello(t, co, a)
    m5.Params.SolutionLimit = 1                 # si ferma alla prima soluzione intera
    m5.optimize()
    print(f"  (c) SolutionLimit = 1: Status = {m5.Status} (10 = SOLUTION_LIMIT), "
          f"SolCount = {m5.SolCount}")
    if m5.SolCount > 0:
        print(f"      ObjVal = {frazione(m5.ObjVal)}  ObjBound = {frazione(m5.ObjBound)}  "
              f"MIPGap = {m5.MIPGap:.4f}")
        print("      Questo e' l'unico caso in cui si riporta un intervallo: l'ottimo sta")
        print("      fra ObjBound e ObjVal, e il MIPGap ne misura l'ampiezza.")
    salva_dati(pd.DataFrame([
        {"caso": "ottimo", "status": m2.Status, "sol_count": m2.SolCount, "obj_val": m2.ObjVal,
         "obj_bound": m2.ObjBound, "mip_gap": m2.MIPGap},
        {"caso": "inammissibile", "status": m3.Status, "sol_count": m3.SolCount,
         "obj_val": None, "obj_bound": None, "mip_gap": None},
        {"caso": "limite di tempo, nessuna soluzione", "status": m4.Status,
         "sol_count": m4.SolCount, "obj_val": None, "obj_bound": None, "mip_gap": None},
        {"caso": "prima soluzione", "status": m5.Status, "sol_count": m5.SolCount,
         "obj_val": m5.ObjVal if m5.SolCount else None,
         "obj_bound": m5.ObjBound, "mip_gap": m5.MIPGap if m5.SolCount else None},
    ]), "cap06_stati")

    # ---------- 5. TOLLERANZE ----------
    intestazione("5. Le tolleranze: 'intero' vuol dire 'intero entro IntFeasTol'")
    m6, x6 = modello(t, co, a)
    print(f"  IntFeasTol  = {m6.Params.IntFeasTol:g}  (quanto una binaria puo' distare da 0 o 1)")
    print(f"  FeasibilityTol = {m6.Params.FeasibilityTol:g}  (violazione ammessa sui vincoli)")
    print(f"  OptimalityTol  = {m6.Params.OptimalityTol:g}  (tolleranza sui costi ridotti)")
    print(f"  MIPGap (obiettivo) = {m6.Params.MIPGap:g}  (si ferma quando il gap scende sotto)")
    m6.optimize()
    peggiore = max(min(abs(v.X - round(v.X)), 1) for v in m6.getVars())
    print(f"  Sulla soluzione restituita, la distanza massima da un intero e' {peggiore:.2e}")
    print("  Nel testo si scrive 1, non 0.9999999997: i valori si arrotondano quando si")
    print("  riportano, e i confronti si fanno con una tolleranza (nel corso, 1e-6).")

    # ---------- 6. IL RILASSAMENTO CON relax() ----------
    intestazione("6. relax(): il rilassamento del modello che abbiamo scritto")
    zlp_r, sol_r, pi_r = rilassamento(m6, rafforzato=True)
    zlp_p, _, _ = rilassamento(m6, rafforzato=False)
    print(f"  z(LP+) = {frazione(zlp_r)}   (relax(): le binarie diventano 0 <= x <= 1)")
    print(f"  z(LP)  = {frazione(zlp_p)}   (rilassamento senza i bound: si toglie anche x <= 1)")
    print("  Duali del rilassamento letti da Gurobi:")
    for nome, valore in pi_r.items():
        if abs(valore) > 1e-9:
            print(f"    {nome}: {valore:.4f}")
    print("  relax() copia il modello: le modifiche pendenti vanno applicate prima con")
    print("  m.update(), altrimenti si rilassa una versione vecchia.")

    # ---------- 7. IL PROTOCOLLO DEL CORSO, DALL'INIZIO ALLA FINE ----------
    intestazione("7. Il protocollo: dati -> modello -> euristica -> LP e duale -> MIP -> tabella")
    # (1) dati  ->  (2) modello
    m7, x7 = modello(t, co, a)
    # (3) euristica e sua verifica
    e = best_fit(t, a, lambda j, h, ra: co[j][h], "costo")
    ub = sum(co[j][h] for (j, h) in e.x)
    sol_eur = {f"x[{j},{h}]": 1 for (j, h) in e.x}
    assert ammissibile(m7, sol_eur), "la soluzione euristica deve essere ammissibile E intera"
    print(f"  (3) euristica best-fit: ub = {frazione(ub)}, ammissibilita' verificata "
          f"(vincoli, bound e interezza)")
    # (4) LP e duale scritto a mano
    d = nuovo_modello("duale")
    mu = d.addVars(n, lb=-GRB.INFINITY, name="mu")
    pi = d.addVars(k, lb=-GRB.INFINITY, ub=0.0, name="pi")
    d.setObjective(mu.sum() + gp.quicksum(a[h] * pi[h] for h in R(k)), GRB.MAXIMIZE)
    d.addConstrs((mu[j] + t[j][h] * pi[h] <= co[j][h] for j in R(n) for h in R(k)), name="rc")
    mano = {f"mu[{j}]": min(co[j]) for j in R(n)}
    lb, viol = valuta(d, mano)
    assert viol <= 1e-9
    print(f"  (4) soluzione duale a mano: lb = {frazione(lb)}, ammissibile per il duale")
    zlp, zlp_raff, _ = due_rilassamenti(m7, d)
    # (5) MIP
    z = risolvi(m7)
    # (6) tabella
    riga = registra_bound("7.1 assegnamento", ub, lb, zlp, zlp_raff, z)
    salva_dati(pd.DataFrame([riga]), "cap06_protocollo")
    assert lb <= zlp <= z <= ub + 1e-9
    print("  (7) la riga della tabella e' quella qui sopra, ed e' salvata in CSV: da li'")
    print("      la leggono la dispensa, il sito e verifica_numeri.py.")

    # ---------- 8. TRE PROBLEMI CHE IL CORSO RIUSA ----------
    # Bin packing, makespan su macchine identiche e commesso viaggiatore: sono i tre
    # problemi su cui il capitolo delle euristiche costruisce next-fit, first-fit,
    # best-fit, LPT e vicino piu' vicino. Qui si scrivono i modelli, cosi' quel
    # capitolo ha qualcosa con cui confrontare le sue soluzioni.
    intestazione("8. Bin packing, makespan e TSP: i modelli che le euristiche useranno")

    # --- bin packing: quanti contenitori bastano ---
    w_bpp = [5, 4, 3, 3]             # peso degli oggetti
    c_bpp = 7                        # capacita' di un contenitore
    n_bpp = len(w_bpp)
    k_bpp = n_bpp                    # al piu' un contenitore per oggetto


    def modello_bpp(w, c, k):
        n = len(w)
        m = nuovo_modello("bin_packing")
        x = m.addVars(n, k, vtype=GRB.BINARY, name="x")
        y = m.addVars(k, vtype=GRB.BINARY, name="y")
        m.setObjective(y.sum(), GRB.MINIMIZE)
        m.addConstrs((x.sum(j, "*") == 1 for j in R(n)), name="oggetto")
        m.addConstrs((gp.quicksum(w[j] * x[j, b] for j in R(n)) <= c * y[b] for b in R(k)),
                     name="capacita")
        return m, x, y


    # con sei contenitori possibili il modello dell'istanza avrebbe 42 colonne: per
    # scriverlo per esteso bastano i tre che servono davvero, e il conto sotto lo
    # dimostra
    m_bpp, x_bpp, y_bpp = modello_bpp(w_bpp, c_bpp, k_bpp)
    z_bpp = risolvi(m_bpp)
    minimo_teorico = -(-sum(w_bpp) // c_bpp)        # arrotondamento all'insu'
    print(f"  Bin packing: pesi {w_bpp}, capacita' {c_bpp}.")
    print(f"  Il peso totale e' {sum(w_bpp)}: nessuna soluzione usa meno di "
          f"{sum(w_bpp)}/{c_bpp} = {minimo_teorico} contenitori, e l'ottimo ne usa {int(z_bpp)}.")
    m_bpp3, x_bpp3, y_bpp3 = modello_bpp(w_bpp, c_bpp, int(z_bpp))
    risolvi(m_bpp3)
    salva_modello(m_bpp3, "cap06_bpp")
    assert z_bpp == minimo_teorico

    # --- P||Cmax: il makespan su macchine identiche ---
    d_cmax = [5, 5, 4, 4, 3, 3, 3]   # durate dei lavori
    k_cmax = 3                       # macchine identiche


    def modello_cmax(d, k):
        n = len(d)
        m = nuovo_modello("makespan")
        x = m.addVars(n, k, vtype=GRB.BINARY, name="x")
        z = m.addVar(name="z")
        m.setObjective(z, GRB.MINIMIZE)
        m.addConstrs((x.sum(j, "*") == 1 for j in R(n)), name="lavoro")
        m.addConstrs((gp.quicksum(d[j] * x[j, mm] for j in R(n)) <= z for mm in R(k)),
                     name="carico")
        return m, x, z


    m_cmax, x_cmax, z_cmax_var = modello_cmax(d_cmax, k_cmax)
    z_cmax = risolvi(m_cmax)
    salva_modello(m_cmax, "cap06_cmax")
    print(f"  Makespan: durate {d_cmax} su {k_cmax} macchine identiche.")
    print(f"  Il carico totale e' {sum(d_cmax)}: diviso per {k_cmax} da' "
          f"{frazione(sum(d_cmax) / k_cmax)}, e l'ottimo vale {frazione(z_cmax)}.")

    # --- TSP con la formulazione MTZ ---
    D_tsp = [[0, 4, 5, 9],
             [4, 0, 9, 9],
             [5, 9, 0, 4],
             [9, 9, 4, 0]]
    n_tsp = len(D_tsp)


    def modello_tsp(D):
        """TSP con i vincoli di Miller-Tucker-Zemlin.

        Le variabili u ordinano le citta' lungo il tour: il vincolo
        u_i - u_j + n x_ij <= n - 1 e' vero se x_ij = 0 e obbliga u_j >= u_i + 1 se
        x_ij = 1. I sottocicli che non toccano la citta' 1 sono cosi' esclusi, perche'
        richiederebbero una catena di u sempre crescenti che si richiude su se stessa.
        """
        n = len(D)
        m = nuovo_modello("tsp")
        x = m.addVars(((i, j) for i in R(n) for j in R(n) if i != j), vtype=GRB.BINARY, name="x")
        u = m.addVars(R(1, n), lb=1, ub=n - 1, name="u")
        m.setObjective(gp.quicksum(D[i][j] * x[i, j] for i, j in x), GRB.MINIMIZE)
        m.addConstrs((gp.quicksum(x[i, j] for j in R(n) if j != i) == 1 for i in R(n)), name="esce")
        m.addConstrs((gp.quicksum(x[i, j] for i in R(n) if i != j) == 1 for j in R(n)), name="entra")
        m.addConstrs((u[i] - u[j] + n * x[i, j] <= n - 1
                      for i in R(1, n) for j in R(1, n) if i != j), name="mtz")
        return m, x, u


    m_tsp, x_tsp, u_tsp = modello_tsp(D_tsp)
    salva_modello(m_tsp, "cap06_tsp")
    z_tsp = risolvi(m_tsp)
    seguente = {i: j for (i, j) in x_tsp if x_tsp[i, j].X > 0.5}
    giro, citta = [0], 0
    while seguente[citta] != 0:
        citta = seguente[citta]
        giro.append(citta)
    print(f"  TSP su {n_tsp} citta': tour ottimo "
          + " -> ".join(str(c + 1) for c in giro + [0])
          + f", lunghezza {frazione(z_tsp)}.")
    salva_dati(pd.DataFrame([{"problema": "bin packing", "z_milp": z_bpp},
                             {"problema": "makespan", "z_milp": z_cmax},
                             {"problema": "TSP", "z_milp": z_tsp}]), "cap06_tre_problemi")

    # ---------- 8. FIGURA: I QUATTRO NUMERI DEL PROTOCOLLO ----------
    fig, ax = plt.subplots(figsize=(7.6, 3.0))
    ax.plot([lb, ub], [0, 0], color=GRIGIO, lw=3, solid_capstyle="round")
    # z(MILP) e ub cadono sullo stesso punto quando l'euristica e' ottima: il pallino
    # piu' grande sta sotto, cosi' si vede che sono due numeri e non uno solo, e le
    # etichette si scostano a sinistra e a destra per non sovrapporsi
    for valore, colore, testo, dx, dy, ha, ms in [
            (lb, TEAL, "$\\mathrm{lb}$ (duale a mano)", 0, 16, "center", 10),
            (zlp, BLU, "$z(\\mathrm{LP})$", -8, -30, "right", 10),
            (ub, ARANCIO, "$\\mathrm{ub}$ (euristica)", 8, -30, "left", 15),
            (z, ROSSO, "$z(\\mathrm{MILP})$", 0, 16, "center", 9)]:
        ax.plot(valore, 0, "o", color=colore, ms=ms)
        ax.annotate(f"{testo}\n{frazione(valore)}", (valore, 0), textcoords="offset points",
                    xytext=(dx, dy), ha=ha, fontsize=9, color=colore)
    ax.set_yticks([])
    ax.set_ylim(-1.1, 1.0)
    ax.set_xlim(lb - 0.7, ub + 0.7)
    ax.set_xlabel("valore dell'obiettivo")
    ax.set_title("I quattro numeri che ogni esercizio produce")
    ax.spines["left"].set_visible(False)
    ax.grid(False)
    salva_figura(fig, "cap06_protocollo")
    print("Fine.")
    ```

<!-- script-incorporato: fine -->
