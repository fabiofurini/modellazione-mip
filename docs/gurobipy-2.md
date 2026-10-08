# 3.2 Leggere i risultati

[:material-file-pdf-box: Dispensa (PDF)](pdf/dispensa-1-modellazione.pdf) · [:material-presentation: Slide (PDF)](pdf/slide-03-gurobi.pdf)

**Classe:** implementazione · **Script:** `python/cap06_gurobi.py`
{ .scheda }

[![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/cap06_gurobi.ipynb)

`Status`, `SolCount`, `ObjVal`, `ObjBound`, `MIPGap`, `NodeCount`: che cosa
significano e quali si possono leggere, compreso il caso in cui il solver non ha
finito.

## Leggere i risultati

L'ordine di lettura non si cambia: `Status`, poi `SolCount`, poi `ObjVal` e
`ObjBound`, poi `MIPGap`, `NodeCount`, `Runtime`.

| `Status` | valore | `SolCount` | Che cosa si può dire |
|---|---:|---:|---|
| `OPTIMAL` | 2 | $\ge 1$ | $z(\mathit{MILP}) = $ `ObjVal`, dimostrato |
| `INFEASIBLE` | 3 | 0 | il modello non ha soluzioni ammissibili |
| `UNBOUNDED` | 5 | 0 | manca un vincolo, o un bound su una variabile |
| `TIME_LIMIT` | 9 | 0 | niente: né una soluzione né, in generale, un bound utile |
| `TIME_LIMIT` | 9 | $\ge 1$ | `ObjBound` $\le z(\mathit{MILP}) \le$ `ObjVal` |
| `SOLUTION_LIMIT` | 10 | $\ge 1$ | come sopra |

!!! example "I quattro casi sull'istanza di assegnamento"
    - **Risoluzione normale.** `Status = 2`, `SolCount = 2`,
      `ObjVal = ObjBound = 11`, `MIPGap = 0`, `NodeCount = 0`.
    - **Inammissibile.** Con disponibilità $(1,1,1)$: `Status = 3`,
      `SolCount = 0`.
    - **Fermato subito.** Con `TimeLimit = 0`: `Status = 9`, `SolCount = 0`,
      `ObjBound` $= -\infty$. Non c'è nulla da riportare.
    - **Fermato alla prima soluzione.** Con `SolutionLimit = 1`: `Status = 10`,
      `SolCount = 1`, `ObjVal = 12`, `ObjBound = 10`, `MIPGap = 0,1667`. Questo
      è il caso in cui si riporta un **intervallo**: l'ottimo sta fra $10$ e
      $12$. Dire «l'ottimo è $12$» sarebbe falso.

!!! danger "Che cosa *non* si riporta"
    Non si scrive «l'ottimo è `ObjVal`» se `Status` non è `OPTIMAL`. Non si
    scrive un gap se `SolCount` è $0$. Non si confronta il `Runtime` di due
    modelli risolti con impostazioni diverse. E non si legge `ObjBound` a fine
    risoluzione pensando di leggere il rilassamento della radice: per quello
    serve `relax()`.
