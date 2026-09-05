# 3.9 Precedenze e sequenziamento

**Tecnica:** binarie con continue, big-M · **Script:** `python/cap03_legami.py` · [Tutte le tecniche](legami.md)

## Il legame in parole

Su una macchina che esegue un lavoro alla volta, per ogni coppia di lavori uno
dei due precede l'altro. È una **disgiunzione per coppia**, non una precedenza
fissata dai dati.

## I vincoli

Con $\kappa_j \ge 0$ l'istante di completamento del lavoro $j$, $t_j$ la sua
durata e $s_{ij} \in \{0,1\}$ che vale 1 se $j$ precede $i$:

$$
\begin{aligned}
s_{ij} + s_{ji} &= 1, & \forall i < j &\qquad \big(\tbinom{n}{2} \text{ vincoli}\big),\\
\kappa_i &\ge \kappa_j + t_i - M\,(1 - s_{ij}), & \forall i \ne j &\qquad (n(n-1) \text{ vincoli}),\\
\kappa_j &\ge t_j, & \forall j &\qquad (n \text{ vincoli}).
\end{aligned}
$$

## La dimostrazione, e il minimo $M$

Il primo vincolo impone che esattamente uno dei due ordini sia scelto. Se
$s_{ij} = 1$, il secondo diventa $\kappa_i \ge \kappa_j + t_i$: il lavoro $i$
finisce almeno $t_i$ dopo la fine di $j$, cioè non si sovrappongono. Se
$s_{ij} = 0$ diventa $\kappa_i \ge \kappa_j + t_i - M$, che deve essere sempre
soddisfatto. Poiché $\kappa_i \ge t_i$ e $\kappa_j \le \sum_h t_h$ in ogni
soluzione sensata, basta

$$M = \sum_{h=1}^{n} t_h,$$

perché allora $\kappa_j + t_i - M \le \sum_h t_h + t_i - \sum_h t_h = t_i \le \kappa_i$.

!!! warning "L'orizzonte va dichiarato"
    Senza un limite superiore sui $\kappa_j$, **nessun $M$ finito è valido**.
    L'orizzonte $\sum_h t_h$ è parte del modello, non un dettaglio implementativo.

## La forza del rilassamento

Tre lavori di durata $(3, 2, 4)$ su una macchina, obiettivo makespan:
$z(\mathit{MILP}) = 9 = \sum_h t_h$ (ovvio: una sola macchina), con
completamenti $(3, 5, 9)$. Il rilassamento vale $4$: con $s_{ij} = 1/2$ tutti i
vincoli di precedenza si spengono a metà e i lavori possono sovrapporsi. È il
rilassamento più debole di tutto il capitolo, e spiega perché i modelli di
sequenziamento big-M scalano male.

## In gurobipy, e dove si rivede

```python
M = sum(t)                                    # l'orizzonte, dichiarato
for i in range(n):
    for j in range(i):
        m.addConstr(s[i, j] + s[j, i] == 1, name=f"disg{i}{j}")
        m.addConstr(kappa[i] >= kappa[j] + t[i] - M * (1 - s[i, j]), name=f"prec{i}{j}")
        m.addConstr(kappa[j] >= kappa[i] + t[j] - M * (1 - s[j, i]), name=f"prec{j}{i}")
```

Si rivede nel problema [7.7](scheduling-7.md), dove le date di rilascio
permettono di ridurre $M$.
