# 3.4 Conteggi interi e arrotondamento all'intero superiore

**Tecnica:** intera con binarie · **Script:** `python/cap03_legami.py` · [Tutte le tecniche](legami.md)

## Il legame in parole

«Quanti contenitori servono?» La variabile non è binaria ma **intera**:
$w \in \mathbb{Z}_{\ge 0}$ conta oggetti indivisibili (scatole, camion, turni,
operai) e ciascuno porta una capacità $K$.

## I vincoli

$$\sum_{i} a_i\, x_i ~\le~ K\, w, \qquad w \in \mathbb{Z}_{\ge 0}
\qquad (1 \text{ vincolo}, 1 \text{ variabile intera}).$$

## La dimostrazione

Posto $A = \sum_i a_i x_i$, il vincolo impone $w \ge A/K$ e l'interezza impone
$w \ge \lceil A/K \rceil$. Insieme a un obiettivo che minimizza $w$ (o che paga
$w$), in ogni ottimo $w$ vale esattamente quel tetto: se valesse di più,
abbassarlo di 1 resterebbe ammissibile e ridurrebbe il costo. Con costo nullo
per $w$ la conclusione si indebolisce in «esiste un ottimo».

!!! warning "Il tetto non si scrive con $\lceil\cdot\rceil$"
    $\lceil t \rceil$ non è una funzione lineare: non si può scrivere dentro un
    vincolo. La coppia «disuguaglianza $\le K w$ + dichiarazione $w$ intera» la
    realizza *implicitamente*, e va letta così quando si spiega il modello.

## La forza del rilassamento

$17$ pezzi unitari, capienza $K = 5$: il rilassamento dà $w \ge 17/5 = 3{,}4$ e
l'ottimo intero è $z(\mathrm{MILP}) = 4$. Il gap $4 - 17/5 = 3/5$ viene tutto
dall'interezza: nessun taglio lineare sulle sole $x$ lo chiude, serve una
disuguaglianza che usi $w$ intera.

## In gurobipy, e dove si rivede

```python
w = m.addVar(vtype=GRB.INTEGER, name="w")
m.addConstr(gp.quicksum(a[i] * x[i] for i in range(n)) <= K * w, name="capienza")
```

Si rivede negli esercizi 12.1 (scatole di luci), 12.2 (spedizioni) e 9.2
(manodopera).
