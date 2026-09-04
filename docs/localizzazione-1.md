# Localizzazione capacitata

**Classe:** MILP · **Legami:** attivazione aggregata (anche vincolo di capacità) · **Script:** `python/fam08_1_capacitata.py`

[![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/fam08_1_capacitata.ipynb)

!!! abstract "Problema 8.1"
    Un'azienda deve servire $n \in \mathbb{Z}_{\ge 1}$ clienti e ha
    individuato $m \in \mathbb{Z}_{\ge 1}$ sedi candidate. Per ogni cliente
    $c$, $d_c \in \mathbb{Q}_{>0}$ è la domanda in litri. Per ogni sede $l$ e
    cliente $c$, $t_{lc} \in \mathbb{Q}_{>0}$ è il costo di trasporto per
    litro. Per ogni sede $l$, $u_l \in \mathbb{Q}_{>0}$ è la capacità e
    $i_l \in \mathbb{Q}_{>0}$ il costo di installazione. Si vuole decidere
    dove installare e come servire i clienti, a costo minimo.

**Il problema a parole.** *Decidiamo* dove installare le strutture e quanto
spedire da ciascuna sede a ciascun cliente. *L'obiettivo*: costo totale
(installazione più trasporto) minimo. *I vincoli*: da una sede non
installata non parte nulla, e una installata non supera la capacità; la
domanda va soddisfatta esattamente. È la **localizzazione capacitata**.

## Modello

**Dati.**

| Simbolo | Tipo | Significato |
|---|---|---|
| $m$ | $\in \mathbb{Z}_{\ge 1}$ | numero di sedi, $l \in \{1, 2, \dots, m\}$ |
| $n$ | $\in \mathbb{Z}_{\ge 1}$ | numero di clienti, $c \in \{1, 2, \dots, n\}$ |
| $t_{lc}$ | $\in \mathbb{Q}_{>0}$ | costo di trasporto dalla sede $l$ al cliente $c$ |
| $u_l$ | $\in \mathbb{Q}_{>0}$ | capacità della sede $l$ |
| $i_l$ | $\in \mathbb{Q}_{>0}$ | costo di installazione della sede $l$ |
| $d_c$ | $\in \mathbb{Q}_{>0}$ | domanda del cliente $c$ |

**Variabili decisionali.** $m$ binarie $x_l$ (sede $l$ installata) e $m\,n$
continue non negative $y_{lc}$ (litri spediti da $l$ a $c$):

$$
x_l = \begin{cases} 1 & \text{se si installa la sede } l,\\ 0 & \text{altrimenti,}\end{cases}
\qquad y_{lc} = \text{litri spediti da } l \text{ a } c.
$$

Modello MILP:

$$
\begin{aligned}
\min ~~ \sum_{l=1}^{m} i_l\, x_l + \sum_{l=1}^{m}\sum_{c=1}^{n} t_{lc}\, y_{lc} & & \\
\text{soggetto a} \quad u_l\, x_l - \sum_{c=1}^{n} y_{lc} &\ge 0, & \forall l \in \{1, 2, \dots, m\}, \\
\sum_{l=1}^{m} y_{lc} &= d_c, & \forall c \in \{1, 2, \dots, n\}, \\
x_l &\in \{0, 1\}, & \forall l \in \{1, 2, \dots, m\}, \\
y_{lc} &\ge 0, & \forall l, c.
\end{aligned}
$$

- l'obiettivo minimizza il costo totale (installazione più trasporto);
- il primo vincolo lega trasporto e installazione **e** impone la capacità
  ($m$ vincoli lineari);
- il secondo soddisfa la domanda di ogni cliente ($n$ vincoli lineari);
- i vincoli restanti definiscono le variabili.

**Il legame.** Se una quantità positiva parte dalla sede $l$, la sede deve
essere installata; dalla contronominale, una sede chiusa non spedisce nulla.
Entrambi i versi sono imposti direttamente dal primo vincolo. Il verso
opposto — una sede installata spedisce qualcosa — non è imposto ma segue
dall'obiettivo: poiché $i_l > 0$, un ottimo non lascia mai una sede aperta
inutilizzata. Una sola famiglia di vincoli fa dunque sia da legame di
attivazione sia da vincolo di capacità.

## Il modello in gurobipy

```python
mod = gp.Model("localizzazione_capacitata")
x = mod.addVars(m, vtype=GRB.BINARY, name="x")
y = mod.addVars(m, n, name="y")
mod.setObjective(gp.quicksum(i[l] * x[l] for l in range(m))
                 + gp.quicksum(t[l][c] * y[l, c] for l in range(m) for c in range(n)), GRB.MINIMIZE)
mod.addConstrs((u[l] * x[l] - gp.quicksum(y[l, c] for c in range(n)) >= 0
                for l in range(m)), name="capacita")
mod.addConstrs((gp.quicksum(y[l, c] for l in range(m)) == d[c] for c in range(n)), name="domanda")
```

## L'istanza

$m = 2$ sedi, $n = 3$ clienti:

| $t_{lc}$ | $c=1$ | $c=2$ | $c=3$ |
|---|---:|---:|---:|
| $l=1$ | 4 | 5 | 6 |
| $l=2$ | 6 | 4 | 3 |

| | $l=1$ | $l=2$ |
|---|---:|---:|
| $u_l$ | 50 | 50 |
| $i_l$ | 60 | 90 |

| | $c=1$ | $c=2$ | $c=3$ |
|---|---:|---:|---:|
| $d_c$ | 8 | 25 | 27 |

## Euristica costruttiva: upper bound

Si scandiscono le sedi in ordine; per ciascuna, i clienti, spedendo il
minimo fra capacità residua e domanda residua.

Esecuzione: la sede 1 spedisce $8$ al cliente 1, $25$ al cliente 2, $17$ al
cliente 3 (capacità esaurita); la sede 2 spedisce i restanti $10$ al
cliente 3. Valore: $60+90 + (4{\cdot}8+5{\cdot}25+6{\cdot}17+3{\cdot}10) =
150+289 = 439$. Quindi $z(\mathrm{MILP}) \le \mathrm{ub} = 439$.

## Rilassamento LP e duale: lower bound

Con $\bar\mu_l = i_l/u_l$ (spalma il costo fisso sulla capacità) e
$\bar\pi_c = \min_l(t_{lc}+\bar\mu_l)$:

$$
\bar\mu_1 = 6/5,\quad \bar\mu_2 = 9/5,\qquad
\bar\pi_1 = 26/5,\quad \bar\pi_2 = 29/5,\quad \bar\pi_3 = 24/5,
$$

di valore $8{\cdot}26/5 + 25{\cdot}29/5 + 27{\cdot}24/5 = 1581/5$. Per la
dualità debole, $\mathrm{lb} = 1581/5 \le z(\mathrm{LP}) \le z(\mathrm{MILP})
\le \mathrm{ub} = 439$.

**Quello che dice il solver.** $z(\mathrm{LP}) = 1581/5$ esattamente: la
soluzione duale a mano è già ottima. Rafforzando con $x_l \le 1$,
$z(\mathrm{LP}^+) = 317$. $z(\mathrm{MILP}) = 365$, con entrambe le sedi
aperte: la sede 1 serve il cliente 1 e parte del cliente 2, la sede 2 il
resto del cliente 2 e tutto il cliente 3. Gap euristica $20{,}3\%$.

| $\mathrm{ub}$ | $\mathrm{lb}$ (duale) | $z(\mathrm{LP})$ | $z(\mathrm{LP}^+)$ | $z(\mathrm{MILP})$ | gap |
|---:|---:|---:|---:|---:|---:|
| 439 | $1581/5$ | $1581/5$ | 317 | 365 | $20{,}3\%$ |

![Soluzione ottima](img/cap08_capacitata_ottimo.png)

## Considerazioni aggiuntive

- Se $u_l < d_c$ nessuna sede da sola può soddisfare il cliente $c$: non il
  caso qui, ma va verificato.
- $y_{lc} \le d_c\, x_l$ è valida ma implicata dai due vincoli insieme.

## Domande di modellazione aggiuntive

??? question "8.1.1 — Lotto minimo per ogni sede aperta"
    Ogni sede aperta deve spedire almeno $5$ litri. Come cambia il modello?
    Qual è il nuovo ottimo?

    ??? success "Soluzione"
        $\sum_c y_{lc} \ge 5\, x_l$ per ogni $l$ ($m$ vincoli). Sull'istanza
        non è mai stretto: l'ottimo resta $365$.

??? question "8.1.2 — Apertura condizionata"
    La sede 2 può essere installata solo se lo è anche la sede 1. Come si
    modella? Qual è il nuovo ottimo?

    ??? success "Soluzione"
        $x_2 \le x_1$ (un vincolo). L'ottimo apre già entrambe le sedi:
        resta $365$.

## Codice

Script completo —
[`python/fam08_1_capacitata.py`](https://github.com/fabiofurini/modellazione-mip/blob/main/python/fam08_1_capacitata.py)
(riproducibile con `python3 python/fam08_1_capacitata.py` dalla cartella
`python/`). Notebook —
[`notebooks/fam08_1_capacitata.ipynb`](https://github.com/fabiofurini/modellazione-mip/blob/main/notebooks/fam08_1_capacitata.ipynb)
— che si apre in Colab dal badge in cima alla pagina.
