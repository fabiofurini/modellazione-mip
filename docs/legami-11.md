# 3.11 Contare i tipi diversi

**Tecnica:** binarie con continue e un conteggio · **Script:** `python/cap03_legami.py` · [Tutte le tecniche](legami.md)

## Il legame in parole

«Si devono produrre almeno due tipi diversi», «al più tre alimenti in dieta»,
«non più di quattro configurazioni». Si conta **quanti** elementi sono attivi,
non quanto se ne produce.

## I vincoli

Con $q_j \ge 0$ la quantità e $y_j$ l'indicatore:

$$
\begin{aligned}
q_j &\le C_j\, y_j, & \forall j &\qquad (n \text{ vincoli}),\\
q_j &\ge \ell\, y_j, & \forall j &\qquad (n \text{ vincoli}),\\
\sum_{j=1}^{n} y_j &\ge p & &\qquad (1 \text{ vincolo}).
\end{aligned}
$$

## La dimostrazione, e perché servono entrambe le soglie

Il primo gruppo dà «$y_j = 0 \Rightarrow q_j = 0$»; il secondo dà il verso
mancante «$y_j = 1 \Rightarrow q_j \ge \ell$».

!!! danger "Senza la soglia $\ell$ il conteggio è vuoto"
    Senza $q_j \ge \ell y_j$, una soluzione con $y_j = 1$ e $q_j = 0$ è
    ammissibile: il vincolo di conteggio si soddisfa **accendendo indicatori
    vuoti**, e la condizione «almeno $p$ tipi diversi» non dice più niente.
    Contare i tipi funziona solo se ogni tipo acceso produce davvero qualcosa, e
    la soglia $\ell$ è ciò che lo garantisce. Le due tecniche —
    [attivazione](legami-02.md) e [lotto minimo](legami-03.md) — vanno insieme.

## La forza del rilassamento

Tre tipi, ricavi unitari $(4, 3, 5)$, risorsa $12$, capacità $10$ ciascuno,
soglia $\ell = 3$, almeno due tipi: $z(\mathrm{MILP}) = 57$, con
$q = (3, 0, 9)$. Il rilassamento vale anch'esso $57$: qui il conteggio non
introduce alcun gap.

## In gurobipy, e dove si rivede

```python
m.addConstrs((q[j] <= C[j] * y[j] for j in range(n)), name="attiva")
m.addConstrs((q[j] >= ell * y[j] for j in range(n)), name="lotto")
m.addConstr(y.sum() >= p, name="almeno_p_tipi")
```

Si rivede negli esercizi 9.3 (veicoli), 10.2 (dieta) e 12.1 (alberi).
