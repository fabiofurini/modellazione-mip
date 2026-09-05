# 3.6 Min-max, max-min e differenza

**Tecnica:** continua con continue · **Script:** `python/cap03_legami.py` · [Tutte le tecniche](legami.md)

## Il legame in parole

Tre obiettivi di equità, spesso confusi: **min-max** (minimizzare il carico più
alto), **max-min** (massimizzare il carico più basso) e **differenza**
(minimizzare lo scarto fra il più alto e il più basso).

## I vincoli

Con $L_k$ il carico della risorsa $k$, $k = 1, \dots, K$:

$$
\begin{aligned}
\text{min-max:}&\quad \min T \quad\text{con}\quad T \ge L_k,\ \forall k &&(K \text{ vincoli}),\\
\text{max-min:}&\quad \max U \quad\text{con}\quad U \le L_k,\ \forall k &&(K \text{ vincoli}),\\
\text{differenza:}&\quad \min\,(T - U) \quad\text{con entrambi} &&(2K \text{ vincoli}).
\end{aligned}
$$

## La dimostrazione

Ciascuna è l'[ausiliaria di massimo](legami-05.md) (o di minimo) con l'argomento
di scambio nel verso giusto: in un $\min T$ la $T$ scende al massimo dei
carichi; in un $\max U$ la $U$ sale al minimo. Nella differenza entrambe le
spinte sono presenti e le due conclusioni valgono insieme.

!!! danger "I tre obiettivi non si confrontano"
    Sull'istanza a cinque pesi $p = (3, 5, 2, 4, 7)$ da ripartire su due operai
    (totale $21$), le tre versioni scelgono la **stessa** ripartizione
    $(11, 10)$ — la migliore possibile, perché il totale è dispari — ma i loro
    valori ottimi sono $11$, $10$ e $1$. Sono tre numeri diversi che descrivono
    la stessa soluzione. Confrontare «$z = 11$» di un min-max con «$z = 1$» di
    una differenza non significa niente. E le soluzioni ottime possono anche non
    coincidere: con più di due risorse, min-max e max-min in generale scelgono
    ripartizioni diverse.

## La forza del rilassamento

Il min-max su quell'istanza dà $z(\mathit{LP}^+) = 21/2 = 10{,}5$ contro
$z(\mathit{MILP}) = 11$: il rilassamento distribuisce i pesi a metà esatta, cosa
che l'interezza non permette.

## In gurobipy, e dove si rivede

```python
T = m.addVar(name="T")
m.addConstrs((T >= carico[k] for k in range(K)), name="max")
m.setObjective(T, GRB.MINIMIZE)
```

Si rivede nella domanda 7.4.1 (makespan), nell'esercizio 11.2 (suddivisione
antitrust) e nell'11.3 (distribuzione dei brani sui CD).
