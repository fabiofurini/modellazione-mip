# Copertura del segnale con interferenza

**Classe:** BIP · **Legami:** se e solo se (soglia + interferenza) · **Script:** `python/fam08_3_copertura.py`

[![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/fam08_3_copertura.ipynb)

!!! abstract "Problema 8.3"
    Un operatore sceglie al più $k \in \mathbb{Z}_{\ge 1}$ sedi, fra
    $m \in \mathbb{Z}_{\ge 1}$ candidate, per servire $n \in \mathbb{Z}_{\ge
    1}$ clienti. $s_{lc} \in \mathbb{Q}_{\ge 0}$ è il segnale ricevuto dal
    cliente $c$ se $l$ è installata. Un cliente è **coperto** se e solo se
    il segnale totale è almeno $t \in \mathbb{Q}_{>0}$ *e* al più una sede
    genera per lui un segnale $\ge b \in \mathbb{Q}_{>0}$. $p_c \in
    \mathbb{Q}_{>0}$ è il profitto se coperto. Si vuole massimizzare il
    profitto totale.

**Il problema a parole.** *Decidiamo* quali sedi installare (al più $k$).
*L'obiettivo*: profitto totale massimo. *I vincoli*: un cliente è coperto se
e solo se riceve segnale sufficiente e non troppa interferenza; al più $k$
sedi installate.

## Modello

**Dati.** $m$, $n$, $s_{lc} \in \mathbb{Q}_{\ge 0}$, $p_c \in
\mathbb{Q}_{>0}$, soglia $t$, limite di interferenza $b$, budget $k$. Per
ogni cliente $c$: $\mathscr{L}_c = \{l : s_{lc} \ge b\}$.

**Variabili decisionali.** $m$ binarie $x_l$ (sede installata), $n$ binarie
$y_c$ (cliente coperto).

$$
\begin{aligned}
\max ~~ \sum_{c=1}^{n} p_c\, y_c & & \\
\text{soggetto a} \quad -\sum_{l=1}^{m} s_{lc}\, x_l + t\, y_c &\le 0, & \forall c, \\
\sum_{l \in \mathscr{L}_c} x_l + (m-1)\, y_c &\le m, & \forall c, \\
\sum_{l=1}^{m} x_l &\le k, & \\
x_l, y_c &\in \{0, 1\}. & &
\end{aligned}
$$

- l'obiettivo massimizza il profitto totale;
- il primo vincolo lega copertura e segnale ricevuto ($n$ vincoli);
- il secondo lega copertura e interferenza ($n$ vincoli);
- il terzo limita a $k$ le sedi installate (un vincolo).

**Il legame: un se e solo se.** Un verso — $y_c=1 \Rightarrow$ segnale
$\ge t$ **e** al più una sede forte — è imposto direttamente dai due
vincoli. L'altro verso — se entrambe le condizioni valgono, il cliente è
coperto — non è imposto dai vincoli (che ammettono anche $y_c=0$), ma segue
dall'ottimalità: poiché $p_c>0$ e $y_c$ compare solo in questi due vincoli,
alzarla a $1$ resta ammissibile e aumenta l'obiettivo. Lo stesso schema del
problema 7.6.

## Il modello in gurobipy

```python
mod = gp.Model("copertura_interferenza")
x = mod.addVars(m, vtype=GRB.BINARY, name="x")
y = mod.addVars(n, vtype=GRB.BINARY, name="y")
mod.setObjective(gp.quicksum(p[c] * y[c] for c in range(n)), GRB.MAXIMIZE)
mod.addConstrs((-gp.quicksum(s[l][c] * x[l] for l in range(m)) + t * y[c] <= 0
                for c in range(n)), name="soglia")
mod.addConstrs((gp.quicksum(x[l] for l in L[c]) + (m - 1) * y[c] <= m
                for c in range(n)), name="interferenza")
mod.addConstr(x.sum() <= k, name="budget")
```

## L'istanza

$m=3$, $n=5$, $t=5$, $b=4$, $k=2$:

| $s_{lc}$ | $c=1$ | $c=2$ | $c=3$ | $c=4$ | $c=5$ |
|---|---:|---:|---:|---:|---:|
| $l=1$ | 6 | 0 | 5 | 3 | 1 |
| $l=2$ | 4 | 5 | 2 | 0 | 0 |
| $l=3$ | 0 | 7 | 5 | 4 | 2 |

| | $c=1$ | $c=2$ | $c=3$ | $c=4$ | $c=5$ |
|---|---:|---:|---:|---:|---:|
| $p_c$ | 10 | 20 | 5 | 15 | 25 |

Con $b=4$: $\mathscr{L}_1=\{1,2\}$, $\mathscr{L}_2=\{3\}$,
$\mathscr{L}_3=\{1,3\}$, $\mathscr{L}_4=\{3\}$, $\mathscr{L}_5=\emptyset$.

## Euristica costruttiva: lower bound

Si aprono le prime $k$ sedi. Cliente 1: segnale $10\ge5$ ma 2 sedi forti
($>1$): **non coperto**. Cliente 2: segnale $5\ge5$, 0 sedi forti:
**coperto**. Cliente 3: segnale $7\ge5$, 1 sede forte: **coperto**. Clienti
4 e 5: segnale insufficiente: **non coperti**. Valore $20+5=25$:
$z(\mathrm{MILP}) \ge \mathrm{lb} = 25$.

## Rilassamento LP e duale: upper bound

Con $\bar\pi_c=0$, $\bar\mu=0$ e $\bar\lambda_c = p_c/(m-1) = p_c/2$:

$$
\bar\lambda_1=5,\ \bar\lambda_2=10,\ \bar\lambda_3=5/2,\ \bar\lambda_4=15/2,\ \bar\lambda_5=25/2,
$$

di valore $m\sum_c\bar\lambda_c = 3\cdot75/2=225/2$. Per la dualità debole
(problema di massimo: l'euristica dà il lower bound, il duale l'upper
bound), $\mathrm{lb}=25 \le z(\mathrm{MILP}) \le z(\mathrm{LP}) \le
\mathrm{ub}=225/2$.

**Quello che dice il solver.** $z(\mathrm{LP}) = 41925/646 \approx 64{,}9$,
$z(\mathrm{LP}^+) = 125/2 = 62{,}5$. $z(\mathrm{MILP}) = 45$, con le sedi 1
e 3 installate e i clienti 1, 2, 4 coperti (non 3 né 5): diverso da quanto
trovato dall'euristica. Gap euristica $44{,}4\%$.

| $\mathrm{lb}$ | $\mathrm{ub}$ (duale) | $z(\mathrm{LP})$ | $z(\mathrm{LP}^+)$ | $z(\mathrm{MILP})$ | gap |
|---:|---:|---:|---:|---:|---:|
| 25 | $225/2$ | $41925/646$ | $125/2$ | 45 | $44{,}4\%$ |

![Soluzione ottima](img/cap08_copertura_ottimo.png)

## Considerazioni aggiuntive

- Il cliente 5 non può mai essere coperto: segnale massimo $1+0+2=3<5$
  anche aprendo tutte le sedi.
- Per i clienti con $|\mathscr{L}_c|\le1$ (2, 4, 5) il vincolo di
  interferenza è ridondante.

## Domande di modellazione aggiuntive

??? question "8.3.1 — Copertura minima garantita"
    Almeno 3 clienti devono essere coperti. Come cambia il modello? Qual è
    il nuovo ottimo?

    ??? success "Soluzione"
        $\sum_c y_c \ge 3$. L'ottimo copre già 3 clienti: resta $45$.

??? question "8.3.2 — Installazione condizionata"
    La sede 1 può essere installata solo se lo è anche la sede 3. Come si
    modella? Qual è il nuovo ottimo?

    ??? success "Soluzione"
        $x_1 \le x_3$. L'ottimo installa già entrambe: resta $45$.

## Codice

Script completo —
[`python/fam08_3_copertura.py`](https://github.com/fabiofurini/modellazione-mip/blob/main/python/fam08_3_copertura.py)
(riproducibile con `python3 python/fam08_3_copertura.py` dalla cartella
`python/`). Notebook —
[`notebooks/fam08_3_copertura.ipynb`](https://github.com/fabiofurini/modellazione-mip/blob/main/notebooks/fam08_3_copertura.ipynb)
— che si apre in Colab dal badge in cima alla pagina.
