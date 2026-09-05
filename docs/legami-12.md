# 3.12 Alldiff ed espansione binaria

**Tecnica:** binarie fra loro; intera con binarie · **Script:** `python/cap03_legami.py` · [Tutte le tecniche](legami.md)

## Il legame in parole

Due esigenze diverse ma imparentate: dare a $n$ oggetti $n$ valori **tutti
distinti** (*alldiff*), e rappresentare una variabile intera limitata con
variabili binarie (*espansione binaria*).

## I vincoli

**Alldiff**, con $p_{iv} = 1$ se l'oggetto $i$ riceve il valore $v$:

$$
\sum_{v} p_{iv} = 1 \quad \forall i \qquad (n \text{ vincoli}), \qquad
\sum_{i} p_{iv} = 1 \quad \forall v \qquad (n \text{ vincoli}).
$$

**Espansione binaria** di $v \in \{0, 1, \dots, 2^K - 1\}$:

$$v = \sum_{k=0}^{K-1} 2^k\, b_k, \qquad b_k \in \{0,1\}
\qquad (1 \text{ vincolo}, K \text{ binarie}).$$

## La dimostrazione

L'alldiff è un **doppio set partitioning**: il primo gruppo dà «ogni oggetto un
valore», il secondo «ogni valore a un solo oggetto». Insieme impongono una
biiezione, cioè valori tutti distinti. L'espansione binaria è la
rappresentazione in base 2, unica per ogni intero in quell'intervallo: la
corrispondenza fra $v$ e $(b_0, \dots, b_{K-1})$ è biunivoca.

!!! note "L'alldiff ha rilassamento esatto, l'espansione no"
    La matrice del doppio partitioning è quella del problema di assegnamento: è
    **totalmente unimodulare**, quindi tutti i vertici del rilassamento sono
    interi e $z(\mathit{LP}^+) = z(\mathit{MILP})$. Sull'istanza $3 \times 3$
    dello script entrambi valgono $7$: l'interezza è gratis.

    L'espansione binaria, al contrario, non aggiunge forza: $\sum_k 2^k b_k$ con
    $b_k \in [0,1]$ copre tutto $[0, 2^K - 1]$ in modo continuo, esattamente
    come $v \ge 0$, $v \le 2^K - 1$. Serve a *riformulare*, non a rafforzare —
    per esempio quando un'altra parte del modello ha bisogno di indicatori
    binari e non di una variabile intera.

## L'esempio

$v \in \{0,\dots,7\}$ con $v \ge 5$, $\min v$: il modello dà $v = 5 = 1 + 4$,
cioè $(b_0, b_1, b_2) = (1, 0, 1)$.

## In gurobipy, e dove si rivede

```python
m.addConstrs((p.sum(i, "*") == 1 for i in range(n)), name="un_valore")
m.addConstrs((p.sum("*", v) == 1 for v in range(n)), name="alldiff")
m.addConstr(v == gp.quicksum(2 ** k * b[k] for k in range(K)), name="espansione")
```

L'alldiff si rivede nel modello numerico delle regine (EX 9) e nell'orario
della scuola di musica (EX 15).
