# 3.3 Lotto minimo e variabile semicontinua

**Tecnica:** binaria con continua · **Script:** `python/cap03_legami.py` · [Tutte le tecniche](legami.md)

## Il legame in parole

«Se si produce, si produce almeno $\ell$»: la quantità $q_j$ vale zero oppure
sta fra una soglia $\ell$ e la capacità $c_j$. Non è un intervallo: è l'unione
di un punto e di un intervallo. Una variabile con questo dominio si chiama
**semicontinua**.

## I vincoli

$$\ell\, y_j ~\le~ q_j ~\le~ c_j\, y_j, \qquad \forall j \qquad (2m \text{ vincoli}).$$

## La dimostrazione

Entrambi i versi sono imposti dai vincoli. Se $y_j = 0$: $0 \le q_j \le 0$, cioè
$q_j = 0$. Se $y_j = 1$: $\ell \le q_j \le c_j$. Quindi

$$q_j \in \{0\} \cup [\ell,\ c_j],$$

esattamente il dominio voluto. Serve $\ell \le c_j$, altrimenti $y_j = 1$ è
inammissibile e la variabile è costretta a zero: un errore di dati che il solver
segnala come inammissibilità solo se $y_j$ è forzata a 1 da altri vincoli.

## La forza del rilassamento

Sulla stessa istanza della [tecnica 3.2](legami-02.md) con $\ell = 5$: l'ottimo
passa da $44$ a $z(\mathit{MILP}) = 49$, con $q = (5, 5)$ invece di $(2, 7)$ —
la soglia costringe a produrre 5 nel secondo impianto anche se il primo è più
caro. Ma $z(\mathit{LP}^+)$ resta $112/3$, **identico** al caso senza soglia.

!!! warning "Perché il lotto minimo non si vede nel rilassamento"
    Nel rilassamento $y_j$ è libera in $[0,1]$, e il vincolo
    $q_j \ge \ell y_j$ si soddisfa abbassando $y_j$: basta $y_j \le q_j/\ell$. Il
    vincolo di soglia **non morde mai** sul continuo. Tutto il suo effetto si
    scarica sull'interezza — ed è per questo che i modelli con lotto minimo sono
    tipicamente più difficili di quelli senza, a parità di dimensione.

## In gurobipy, e dove si rivede

```python
m.addConstrs((q[j] >= ell * y[j] for j in range(mm)), name="lotto")
m.addConstrs((q[j] <= C[j] * y[j] for j in range(mm)), name="capacita")
```

Gurobi ha anche il tipo `GRB.SEMICONT`, che dichiara direttamente il dominio; in
questo corso si scrive la formulazione a mano, perché è quella che si deve saper
dimostrare. Si rivede nella domanda 7.2.2 e negli esercizi 9.1 e 9.3.
