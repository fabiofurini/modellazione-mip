# Classi con premio di completamento e riduzione «se e solo se»

**Classe:** BIP · **Legami:** se e solo se (due), CNF · **Script:** `python/fam07_6_classipremio.py`

[![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/fam07_6_classipremio.ipynb)

!!! abstract "Problema 7.6"
    Un'azienda ha $n$ lavori eseguibili su una macchina con disponibilità $a$.
    Per ogni lavoro $j$, $t_j$ è il tempo e $r_j$ il ricavo. I lavori sono
    partizionati in $q \ge 2$ classi. La disponibilità si riduce di $u > 0$ minuti
    *se e solo se* la macchina esegue lavori di almeno due classi diverse. Per ogni
    classe $c$ si ottiene un ricavo extra $v_c > 0$ *se e solo se* tutti i lavori
    della classe sono eseguiti. Massimizzare il ricavo totale.

**Il problema a parole.** Due «se e solo se»: uno premia (il completamento),
uno penalizza (la mescolanza). Di ciascuno basta imporre un verso: l'altro lo
impone l'obiettivo.

## Modello

**Variabili.** $n + q + 1$ binarie: $x_j$ (lavoro eseguito), $y_c$ (classe
completa), $z$ (lavori di almeno due classi).

$$
\begin{aligned}
\max ~~ \sum_{j=1}^{n} r_j\, x_j + \sum_{c=1}^{q} v_c\, y_c & & \\
\text{soggetto a} \quad x_j - y_c &\ge 0, & \forall c,\ \forall j \in \mathscr{J}_c, \\
x_j + x_i - z &\le 1, & \forall c < g,\ \forall j \in \mathscr{J}_c,\ \forall i \in \mathscr{J}_g, \\
\sum_{j=1}^{n} t_j\, x_j + u\, z &\le a, & \\
x_j,\ y_c,\ z &\in \{0, 1\}. &
\end{aligned}
$$

- l'obiettivo massimizza ricavi dei lavori più premi delle classi complete;
- i vincoli **tutti**: se una classe è dichiarata completa, tutti i suoi lavori
  sono eseguiti ($n$ vincoli);
- i vincoli **miste**: se si eseguono due lavori di classi diverse, $z = 1$
  ($\sum_{c<g} |\mathscr{J}_c|\,|\mathscr{J}_g|$ vincoli);
- il vincolo di **disponibilità** con la riduzione $u z$ ($1$ vincolo);
- i vincoli di dominio.

!!! note "Legame fra le variabili: quattro implicazioni"
    **$y_c$, dal vincolo.** $y_c \Rightarrow (x_j \,\mathtt{AND}\, x_i \,\mathtt{AND}\, \dots)$:
    l'espressione $(x_j \,\mathtt{AND}\, \dots) \,\mathtt{OR}\, \mathtt{NOT}\,y_c$ diventa
    per distributività la CNF $(x_j \,\mathtt{OR}\, \mathtt{NOT}\,y_c) \,\mathtt{AND}\, \dots$,
    cioè $x_j \ge y_c$. **$y_c$, dall'ottimo.** Se tutti i lavori sono
    eseguiti allora $y_c = 1$: porre $y_c = 1$ resta ammissibile e aumenta
    l'obiettivo di $v_c > 0$.

    **$z$, dal vincolo.** $x_j \,\mathtt{AND}\, x_i \Rightarrow z$ per ogni coppia
    mista: De Morgan dà $\mathtt{NOT}\,x_j \,\mathtt{OR}\, \mathtt{NOT}\,x_i \,\mathtt{OR}\, z$,
    cioè $x_j + x_i - z \le 1$. **$z$, dall'ottimo.** Se i lavori eseguiti
    stanno in una sola classe, $z = 0$: porre $z = 0$ resta ammissibile, libera
    $u$ minuti e non cambia l'obiettivo (dove $z$ non compare) — «esiste un
    ottimo», non «in ogni ottimo».

## Il modello in gurobipy

```python
coppie = [(j, i) for c in range(q) for g in range(c + 1, q) for j in J[c] for i in J[g]]
m = gp.Model("classi_premio");  m.Params.OutputFlag = 0
x = m.addVars(n, vtype=GRB.BINARY, name="x")
y = m.addVars(q, vtype=GRB.BINARY, name="y")
z = m.addVar(vtype=GRB.BINARY, name="z")
m.setObjective(gp.quicksum(r[j] * x[j] for j in range(n))
               + gp.quicksum(v[c] * y[c] for c in range(q)), GRB.MAXIMIZE)
m.addConstrs((x[j] - y[c] >= 0 for c in range(q) for j in J[c]), name="tutti")
m.addConstrs((x[j] + x[i] - z <= 1 for (j, i) in coppie), name="miste")
m.addConstr(gp.quicksum(t[j] * x[j] for j in range(n)) + u * z <= a, name="disponibilita")
m.optimize()
```

## L'istanza

$n = 6$, $q = 3$: $\mathscr{J}_1 = \{1, 2\}$, $\mathscr{J}_2 = \{3, 4\}$,
$\mathscr{J}_3 = \{5, 6\}$, $a = 50$, $u = 10$.

| | $j=1$ | $j=2$ | $j=3$ | $j=4$ | $j=5$ | $j=6$ |
|---|---:|---:|---:|---:|---:|---:|
| $r_j$ | 10 | 5 | 20 | 12 | 10 | 22 |
| $t_j$ | 5 | 15 | 25 | 15 | 10 | 38 |

| | $c=1$ | $c=2$ | $c=3$ |
|---|---:|---:|---:|
| $v_c$ | 5 | 4 | 10 |

## Euristica costruttiva: lower bound

Classe per classe; dalla seconda classe il primo lavoro paga anche $u$.

- **Passi 1–2.** Classe 1: $x[1] = x[2] = 1$, $ra = 30$; classe completa, $y[1] = 1$.
- **Passo 3.** Classe 2: $t_3 + u = 35 > 30$, saltato. **Passo 4.**
  $t_4 + u = 25 \le 30$: $x[4] = 1$, $z = 1$, $ra = 5$.
- **Passi 5–6.** Classe 3: $t_5, t_6 > 5$, saltati.

Ricavo $10 + 5 + 12 + 5 = 32$: $z(\mathrm{MILP}) \ge 32$.

## Rilassamento LP e duale: upper bound

Con $\pi_j \le 0$ (tutti), $\lambda_{ji} \ge 0$ (miste), $\mu \ge 0$
(disponibilità):

$$
\begin{aligned}
\min ~~ \sum_{\text{coppie miste}} \lambda_{ji} + a\, \mu & & \\
\text{soggetto a} \quad \pi_j + \sum_{i \notin \mathscr{J}_c} \lambda_{ji} + t_j\, \mu &\ge r_j, & \forall c,\ \forall j \in \mathscr{J}_c, \\
-\sum_{j \in \mathscr{J}_c} \pi_j &\ge v_c, & \forall c, \\
-\sum_{\text{coppie miste}} \lambda_{ji} + u\, \mu &\ge 0. &
\end{aligned}
$$

**Una soluzione duale a mano.** Il premio di ogni classe caricato su un solo
lavoro: $\bar\pi_1 = -5$, $\bar\pi_3 = -4$, $\bar\pi_5 = -10$; $\bar\lambda = 0$;
$\bar\mu = \max_j (r_j - \bar\pi_j)/t_j = \max\{3, \tfrac{1}{3}, \tfrac{24}{25}, \tfrac{4}{5}, 2, \tfrac{11}{19}\} = 3$;
valore $150$: $32 \le z(\mathrm{MILP}) \le 150$.

**Quello che dice il solver.** $z(\mathrm{LP}) = 5280/113 = 46{,}7$. Ottimo
intero $42$: la sola classe 3 completa, lavori 5 e 6 ($48 \le 50$, $z = 0$),
ricavo $10 + 22 + 10$. Gap dell'euristica $24\%$.

| $\mathrm{lb}$ | $\mathrm{ub}$ (duale a mano) | $z(\mathrm{LP})$ | $z(\mathrm{MILP})$ | gap euristica |
|---:|---:|---:|---:|---:|
| 32 | 150 | $5280/113$ | 42 | $23{,}8\%$ |

## Considerazioni aggiuntive

- Il verso di ottimalità per $y_c$ si impone con
  $\sum_{j \in \mathscr{J}_c} x_j - y_c \le |\mathscr{J}_c| - 1$ ($q$ vincoli che
  preservano l'ottimo, non validi).
- Il verso di ottimalità per $z$: $z \le \sum_{j \notin \mathscr{J}_c} x_j$ per
  ogni $c$.
- Una forma aggregata con variabili di classe $w_c \ge x_j$ e
  $\sum_c w_c - 1 \le (q-1) z$ sostituisce le coppie: stesso insieme intero,
  rilassamento diverso.

## Domande di modellazione aggiuntive

??? question "7.6.1 — Almeno un lavoro per classe"
    Eseguire almeno un lavoro di ogni classe. Che succede a $z$?

    ??? success "Soluzione"
        Copertura per classe $\sum_{j \in \mathscr{J}_c} x_j \ge 1$. Con tutte
        le classi toccate, i vincoli «miste» forzano $z = 1$: la riduzione è
        certa e $z$ si può eliminare ($a - u$). Ottimo $40$.

??? question "7.6.2 — Penalità per classe iniziata e non finita"
    Iniziare una classe senza completarla costa $w = 3$.

    ??? success "Soluzione"
        Una variabile $s_c$ «classe iniziata» con $s_c \ge x_j$ per
        $j \in \mathscr{J}_c$; obiettivo $- w \sum_c (s_c - y_c)$. Il verso
        $s_c = 0$ a classe vuota segue dall'obiettivo ($-w < 0$ in un massimo);
        $y_c \le s_c$ vale in ogni soluzione ammissibile da $y_c \le x_j \le s_c$.
        L'ottimo resta $42$.

## Codice

Script completo: [`python/fam07_6_classipremio.py`](https://github.com/fabiofurini/modellazione-mip/blob/main/python/fam07_6_classipremio.py);
notebook: [`notebooks/fam07_6_classipremio.ipynb`](https://github.com/fabiofurini/modellazione-mip/blob/main/notebooks/fam07_6_classipremio.ipynb).
