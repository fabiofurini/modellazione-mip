# 3.10 «Se e solo se»

**Tecnica:** binaria con binarie · **Script:** `python/cap03_legami.py` · [Tutte le tecniche](legami.md)

## Il legame in parole

Una binaria $y$ deve valere 1 **esattamente quando** una condizione è vera — per
esempio «tutti i lavori della classe sono eseguiti». Non basta
un'implicazione: ne servono due.

## I vincoli

Con $x_1, \dots, x_p$ binarie e la condizione «tutte valgono 1»:

$$
\begin{aligned}
y &\le x_j, & \forall j &\qquad (p \text{ vincoli}),\\
y &\ge \sum_{j=1}^{p} x_j - (p - 1) & &\qquad (1 \text{ vincolo}).
\end{aligned}
$$

## La dimostrazione, nei due versi

- Il primo gruppo dà $y = 1 \Rightarrow x_j = 1$ per ogni $j$; equivalentemente,
  se anche uno solo degli $x_j$ è zero allora $y = 0$.
- Il secondo dà il verso opposto: se tutti gli $x_j = 1$, il membro destro vale
  $p - (p-1) = 1$, quindi $y \ge 1$ e dunque $y = 1$. Se almeno uno è zero, il
  membro destro è $\le 0$ e il vincolo non dice nulla.

Insieme, impongono $y = 1 \iff \sum_j x_j = p$ in **ogni** soluzione ammissibile.

## Quando basta un verso solo

Se $y$ compare nell'obiettivo di un massimo con un premio $v > 0$ e in nessun
altro vincolo, il secondo vincolo si può omettere: in ogni ottimo, se tutti gli
$x_j = 1$ e $y = 0$, alzare $y$ a 1 resta ammissibile e aumenta l'obiettivo di
$v > 0$. È un argomento di ottimalità, e vale **solo all'ottimo**.

!!! danger "Con $v = 0$ l'argomento cade, e $y$ smette di significare"
    Istanza a tre lavori, ricavi $(2,2,2)$, capacità 3:

    | premio $v$ | vincoli | $z(\mathrm{MILP})$ | $y$, $x$ all'ottimo | $y$ dice «classe completa»? |
    |---:|---|---:|---|---|
    | $9$ | solo $y \le x_j$ | $15$ | $y=1$, $x=(1,1,1)$ | sì |
    | $9$ | entrambi | $15$ | $y=1$, $x=(1,1,1)$ | sì |
    | $0$ | solo $y \le x_j$ | $6$ | $y=0$, $x=(1,1,1)$ | **no** |
    | $0$ | entrambi | $6$ | $y=1$, $x=(1,1,1)$ | sì |

    Con $v = 0$ il valore ottimo è lo stesso nei due modelli, ma nel terzo caso
    $y$ non è più un indicatore fedele. Se $y$ serve solo a pagare un premio, il
    verso mancante è inutile; se $y$ compare in *altri* vincoli — e questo
    succede appena si aggiunge una condizione sul numero di classi complete — va
    scritto.

## La forza del rilassamento

$z(\mathrm{LP}^+) = 15 = z(\mathrm{MILP})$ su questa istanza: entrambi i versi
imposti danno un rilassamento esatto. Il secondo vincolo è debole nel
rilassamento (con $x_j = 1/2$ il membro destro è negativo), ma qui non serve.

## In gurobipy, e dove si rivede

```python
m.addConstrs((y <= x[j] for j in range(p)), name="iff_su")
m.addConstr(y >= gp.quicksum(x[j] for j in range(p)) - (p - 1), name="iff_giu")
```

Si rivede nel problema [7.6](scheduling-6.md) e nell'esercizio 9.3.
