# 3.2 Costo fisso, capacità e flusso continuo

**Tecnica:** binaria con continua · **Script:** `python/cap03_legami.py` · [Tutte le tecniche](legami.md)

## Il legame in parole

Come nell'[attivazione](legami-01.md), ma la quantità usata è **continua**:
$q_j \ge 0$ è quanto si produce nell'impianto $j$, e $y_j$ dice se l'impianto è
aperto. Un impianto chiuso non produce; uno aperto produce al più la sua
capacità $C_j$.

## I vincoli

$$q_j \le C_j\, y_j, \qquad \forall j \qquad (m \text{ vincoli}).$$

Un solo vincolo per impianto, con il coefficiente **giusto**: la capacità, non
un numero grande a caso.

## La dimostrazione

Se $y_j = 0$ il vincolo dà $q_j \le 0$ e, con $q_j \ge 0$, forza $q_j = 0$:
l'implicazione «chiuso $\Rightarrow$ non produce» è imposta dal vincolo, e con
essa la sua contronominale «produce $\Rightarrow$ aperto». Se $y_j = 1$ il
vincolo dà $q_j \le C_j$: la capacità.

Il verso «aperto $\Rightarrow$ produce» non è imposto e segue dall'ottimalità
solo se $f_j > 0$, come nella [tecnica 3.1](legami-01.md).

## La forza del rilassamento

Due impianti, costi fissi $f = (10, 14)$, costi unitari $c = (3, 2)$, capacità
$C = (6, 7)$, domanda $D = 9$. L'ottimo è $z(\mathit{MILP}) = 44$ (entrambi
aperti, $q = (2, 7)$).

| Coefficiente della binaria | $z(\mathit{LP}^+)$ |
|---|---:|
| la capacità $C_j$ | $112/3 \approx 37{,}33$ |
| un big-M $= 100$ (più $q_j \le C_j$ a parte) | $1059/50 = 21{,}18$ |

Stesso insieme intero, stesso ottimo, rilassamenti lontanissimi.

!!! tip "La regola"
    Il coefficiente di una binaria di attivazione è il **più piccolo valore che
    la variabile continua può assumere quando l'attivazione vale 1**, e va
    ricavato dai dati. Un big-M scelto «grande abbastanza» è sempre valido e
    quasi sempre pessimo.

## In gurobipy, e dove si rivede

```python
m.addConstrs((q[j] <= C[j] * y[j] for j in range(mm)), name="link")
```

Si rivede nel problema [8.1](localizzazione-1.md) e in tutta la famiglia della
produzione.
