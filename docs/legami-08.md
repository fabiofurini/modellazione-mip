# 3.8 Big-M: vincoli condizionati e disgiunzioni

**Tecnica:** binaria con un vincolo · **Script:** `python/cap03_legami.py` · [Tutte le tecniche](legami.md)

## Il legame in parole

«Se $y = 1$ allora vale il vincolo $a' x \le b$; se $y = 0$ il vincolo non c'è».
Un vincolo che si accende e si spegne.

## Il vincolo

$$a' x ~\le~ b + M\,(1 - y) \qquad (1 \text{ vincolo}).$$

## La dimostrazione, e come si sceglie $M$

Con $y = 1$ il vincolo è $a' x \le b$: acceso. Con $y = 0$ diventa
$a' x \le b + M$: spento **purché** $M$ sia abbastanza grande da non tagliare
nulla, cioè

$$M ~\ge~ \max\{a' x : x \text{ ammissibile per gli altri vincoli}\} - b.$$

Si distinguono tre cose:

- un $M$ **valido**: soddisfa la disuguaglianza sopra, quindi il modello ha
  l'insieme intero giusto;
- un $M$ **migliorabile**: valido ma più grande del necessario; l'insieme intero
  è lo stesso, il rilassamento è più debole;
- il **minimo $M$ dimostrato**: il più piccolo valore per cui si è *dimostrata*
  la validità, tipicamente calcolando quel massimo sui soli bound delle
  variabili. Non è necessariamente il minimo assoluto, ed è onesto dirlo.

!!! danger "Un $M$ non valido non è «un po' diverso»"
    Con $a = (3,4,5)$, $b = 6$ e $x$ binarie, il massimo di $a'x$ è $12$, quindi
    $M = 12 - 6 = 6$ è valido. Su $\max\ x_1 + x_2 + x_3 + y$ l'ottimo è
    $z(\mathit{MILP}) = 3$ (con $y = 0$ e tutte le $x$ a 1). Con $M = 5$ il
    vincolo con $y = 0$ resta $3x_1 + 4x_2 + 5x_3 \le 11$, che esclude
    $x = (1,1,1)$: l'ottimo scende a $2$. Il modello non risponde più alla
    domanda posta.

## La forza del rilassamento

| $M$ | $z(\mathit{LP}^+)$ | |
|---|---:|---|
| $6$ (il minimo dimostrato) | $3$ | coincide con $z(\mathit{MILP})$ |
| $20$ | $37/10 = 3{,}7$ | |
| $1000$ | $1997/500 \approx 3{,}994$ | quasi il massimo possibile, $4$ |

Il degrado è monotono e rapido. La regola operativa: **calcolare $M$ dai dati,
sempre, e scriverlo nel testo subito dopo il modello**.

## In gurobipy, e dove si rivede

```python
M = sum(max(a[j], 0) for j in range(n)) - b       # calcolato dai dati, non scelto a occhio
m.addConstr(gp.quicksum(a[j] * x[j] for j in range(n)) <= b + M * (1 - y), name="cond")
```

Si rivede nel problema [7.7](scheduling-7.md) e nella
[tecnica 3.9](legami-09.md).
