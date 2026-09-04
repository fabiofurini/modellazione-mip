# Una macchina, classi di lavori con setup

**Classe:** BIP · **Legami:** attivazione disaggregata, CNF · **Script:** `python/fam07_5_classisetup.py`

[![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/fam07_5_classisetup.ipynb)

!!! abstract "Problema 7.5"
    Un'azienda ha $n$ lavori eseguibili su una macchina con disponibilità
    $a \in \mathbb{Q}_{>0}$ minuti. Per ogni lavoro $j$, $t_j$ è il tempo e $r_j$ il
    ricavo se eseguito. I lavori sono partizionati in $q \ge 2$ classi
    $\mathscr{J}_1, \dots, \mathscr{J}_q$. Se la macchina esegue lavori di una classe
    $c$, si paga un costo di setup $f_c \ge 0$ e si consuma un tempo di setup
    $s_c \ge 0$. La macchina non esegue lavori in parallelo. Massimizzare il
    profitto.

**Il problema a parole.** *Decidiamo* quali lavori eseguire e quali classi
attivare. *L'obiettivo*: ricavi meno costi di setup. *Il vincolo*: tempi dei
lavori più tempi di setup entro la disponibilità. Uno zaino con costi fissi per
gruppo: il legame di attivazione, stavolta **disaggregato** fin dall'inizio.

## Modello

| Simbolo | Tipo | Significato |
|---|---|---|
| $n$, $a$ | | numero di lavori, disponibilità |
| $t_j$, $r_j$ | $\in \mathbb{Q}_{>0}$ | tempo e ricavo del lavoro $j$ |
| $q$, $\mathscr{J}_c$ | | numero di classi e lavori della classe $c$ (partizione) |
| $f_c$, $s_c$ | $\in \mathbb{Q}_{\ge 0}$ | costo e tempo di setup della classe $c$ |

**Variabili.** $n + q$ binarie: $x_j = 1$ se il lavoro $j$ è eseguito;
$y_c = 1$ se almeno un lavoro della classe $c$ è eseguito.

$$
\begin{aligned}
\max ~~ \sum_{j=1}^{n} r_j\, x_j - \sum_{c=1}^{q} f_c\, y_c & & \\
\text{soggetto a} \quad \sum_{j=1}^{n} t_j\, x_j + \sum_{c=1}^{q} s_c\, y_c &\le a, & \\
x_j - y_c &\le 0, & \forall c,\ \forall j \in \mathscr{J}_c, \\
x_j \in \{0, 1\},\quad y_c &\in \{0, 1\}. &
\end{aligned}
$$

- l'obiettivo massimizza ricavi meno setup;
- il vincolo di **disponibilità** ($1$ vincolo lineare);
- i vincoli di **link**: se un lavoro di una classe è eseguito, la classe è
  attivata ($n$ vincoli lineari, uno per lavoro);
- i vincoli di dominio definiscono le variabili.

!!! note "Legame fra le variabili: la CNF diventa vincolo"
    **Dal vincolo.** «Se almeno un lavoro della classe $c$ è eseguito, la classe
    è attivata»: $(x_j \,\mathtt{OR}\, x_s \,\mathtt{OR}\, \dots) \Rightarrow y_c$,
    contronominale $\mathtt{NOT}\,y_c \Rightarrow (\mathtt{NOT}\,x_j \,\mathtt{AND}\, \dots)$.
    L'espressione $\mathtt{NOT}(x_j \,\mathtt{OR}\, \dots) \,\mathtt{OR}\, y_c$ diventa,
    con De Morgan e distributività, la CNF
    $(\mathtt{NOT}\,x_j \,\mathtt{OR}\, y_c) \,\mathtt{AND}\, (\mathtt{NOT}\,x_s \,\mathtt{OR}\, y_c) \,\mathtt{AND}\, \dots$,
    cioè $1 - x_j + y_c \ge 1$: **esattamente** i vincoli di link
    $x_j \le y_c$. Verifica nei due versi: $x_j = 1$ forza $y_c = 1$; $y_c = 0$
    forza tutti gli $x_j$ della classe a $0$.

    **Dall'ottimo.** «Se nessun lavoro della classe è eseguito, la classe non è
    attivata»: non imposta, segue **senza perdita di ottimalità**: porre
    $y_c = 0$ resta ammissibile, libera $s_c$ minuti e non diminuisce
    l'obiettivo perché $f_c \ge 0$. Poiché $f_c$ può essere nullo, la
    conclusione corretta è «esiste un ottimo in cui…», non «in ogni ottimo».

## Il modello in gurobipy

```python
m = gp.Model("classi_setup");  m.Params.OutputFlag = 0
x = m.addVars(n, vtype=GRB.BINARY, name="x")
y = m.addVars(q, vtype=GRB.BINARY, name="y")
m.setObjective(gp.quicksum(r[j] * x[j] for j in range(n))
               - gp.quicksum(f[c] * y[c] for c in range(q)), GRB.MAXIMIZE)
m.addConstr(gp.quicksum(t[j] * x[j] for j in range(n))
            + gp.quicksum(s[c] * y[c] for c in range(q)) <= a, name="disponibilita")
m.addConstrs((x[j] - y[c] <= 0 for c in range(q) for j in J[c]), name="link")
m.optimize()
```

## L'istanza

$n = 7$, $q = 3$: $\mathscr{J}_1 = \{1, 2\}$, $\mathscr{J}_2 = \{3, 4\}$,
$\mathscr{J}_3 = \{5, 6, 7\}$, $a = 50$.

| | $j=1$ | $j=2$ | $j=3$ | $j=4$ | $j=5$ | $j=6$ | $j=7$ |
|---|---:|---:|---:|---:|---:|---:|---:|
| $r_j$ | 10 | 6 | 8 | 6 | 7 | 9 | 5 |
| $t_j$ | 5 | 10 | 8 | 6 | 9 | 5 | 6 |

| | $c=1$ | $c=2$ | $c=3$ |
|---|---:|---:|---:|
| $f_c$ | 10 | 5 | 4 |
| $s_c$ | 10 | 12 | 6 |

## Euristica costruttiva: lower bound

Classe per classe: il primo lavoro paga anche il setup, se ci sta.

- **Passo 1.** Classe 1: $s_1 + t_1 = 15 \le 50$; $y[1] = x[1] = 1$, $ra = 35$.
- **Passo 2.** $t_2 = 10 \le 35$; $x[2] = 1$, $ra = 25$.
- **Passo 3.** Classe 2: $s_2 + t_3 = 20 \le 25$; $y[2] = x[3] = 1$, $ra = 5$.
- **Passo 4.** $t_4 = 6 > 5$: saltato. **Passi 5–7.** Classe 3: $s_3 + t_j > 5$:
  saltati.

Profitto $10 + 6 + 8 - 10 - 5 = 9$: $z(\mathrm{MILP}) \ge 9$.

## Rilassamento LP e duale: upper bound

Con $\pi \ge 0$ (disponibilità) e $\lambda_j \ge 0$ (link):

$$
\begin{aligned}
\min ~~ a\, \pi & & \\
\text{soggetto a} \quad t_j\, \pi + \lambda_j &\ge r_j, & \forall j, \\
s_c\, \pi - \sum_{j \in \mathscr{J}_c} \lambda_j &\ge -f_c, & \forall c, \\
\pi \ge 0,\quad \lambda_j &\ge 0. &
\end{aligned}
$$

**Una soluzione duale a mano.** $\bar\lambda = 0$ e
$\bar\pi = \max_j r_j/t_j = \tfrac{10}{5} = 2$: valore $100$. Quindi
$9 \le z(\mathrm{MILP}) \le 100$: un bound grossolano, come spesso i bound «di
zaino», che ignora setup e costi.

**Quello che dice il solver.** $z(\mathrm{LP}) = 425/13 = 32{,}7$ (con
$\pi = \tfrac{17}{26}$ e alcuni $\lambda_j > 0$); $z(\mathrm{LP}^+) = 329/13$.
Ottimo intero $21$: classi 2 e 3, lavori $3, 4, 5, 6$, profitto $30 - 9$.
L'euristica resta a $9$ (gap $57\%$): l'ordine di scansione conta.

| $\mathrm{lb}$ | $\mathrm{ub}$ (duale a mano) | $z(\mathrm{LP})$ | $z(\mathrm{LP}^+)$ | $z(\mathrm{MILP})$ | gap euristica |
|---:|---:|---:|---:|---:|---:|
| 9 | 100 | $425/13$ | $329/13$ | 21 | $57{,}1\%$ |

## Considerazioni aggiuntive

- $y_c \le 1$ rafforza il rilassamento; $x_j \le 1$ è implicato.
- $\sum_{j \in \mathscr{J}_c} x_j \ge y_c$ ($q$ vincoli) non è valido ma
  preserva l'ottimo.
- La forma aggregata $\sum_{j \in \mathscr{J}_c} x_j \le |\mathscr{J}_c|\, y_c$
  ha lo stesso insieme intero e un rilassamento più debole.

## Domande di modellazione aggiuntive

??? question "7.5.1 — Una sola classe"
    Si può attivare al più una classe.

    ??? success "Soluzione"
        Set packing sulle attivazioni: $\sum_c y_c \le 1$. Ottimo $17$: la
        classe 3 da sola, tutti i suoi lavori ($26 \le 50$), $21 - 4$.

??? question "7.5.2 — Una classe subordinata a un'altra"
    La classe 3 si può attivare solo se si attiva anche la classe 1.

    ??? success "Soluzione"
        $y_3 \Rightarrow y_1$, cioè $y_3 \le y_1$. Ottimo da $21$ a $18$.

## Codice

Script completo: [`python/fam07_5_classisetup.py`](https://github.com/fabiofurini/modellazione-mip/blob/main/python/fam07_5_classisetup.py);
notebook: [`notebooks/fam07_5_classisetup.ipynb`](https://github.com/fabiofurini/modellazione-mip/blob/main/notebooks/fam07_5_classisetup.ipynb).
