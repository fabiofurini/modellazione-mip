# 3.3 Tolleranze e rilassamenti

[:material-file-pdf-box: Dispensa (PDF)](pdf/dispensa-1-modellazione.pdf) · [:material-presentation: Slide (PDF)](pdf/slide-03-gurobi.pdf)

**Classe:** implementazione · **Script:** `python/cap06_gurobi.py`
{ .scheda }

[![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/cap06_gurobi.ipynb)

«Intero» vuol dire «intero entro una tolleranza», e `relax()` costruisce il
rilassamento del modello che si è appena scritto.

## Le tolleranze

| Parametro | Default | Significato |
|---|---:|---|
| `IntFeasTol` | $10^{-5}$ | quanto una variabile intera può distare da un intero |
| `FeasibilityTol` | $10^{-6}$ | violazione ammessa su un vincolo lineare |
| `OptimalityTol` | $10^{-6}$ | tolleranza sui costi ridotti |
| `MIPGap` | $10^{-4}$ | gap relativo sotto il quale il solver si ferma |

!!! warning "«Intero» significa «intero entro una tolleranza»"
    Una binaria può tornare come $0{,}9999999997$. Nel testo si scrive $1$: i
    valori si arrotondano *quando si riportano*, e i confronti si fanno sempre
    con una tolleranza — nel corso $10^{-6}$, la costante `TOL` di
    `python/mip.py`. Scrivere `if x.X == 1` è un errore; si scrive
    `if x.X > 0.5`.

    Il default `MIPGap` $= 10^{-4}$ significa anche che il solver può fermarsi
    *prima* dell'ottimo esatto dichiarando `OPTIMAL`: su istanze con valori
    grandi vale la pena abbassarlo.

## Il rilassamento con `relax()`

```python
m.update()            # relax() copia il modello: le modifiche pendenti vanno applicate prima
r = m.relax()         # le binarie diventano 0 <= x <= 1, le intere x >= lb
r.Params.OutputFlag = 0
r.optimize()
zlp = r.ObjVal
duali = {c.ConstrName: c.Pi for c in r.getConstrs()}
```

Su quell'istanza, $z(\mathit{LP}^+) = z(\mathit{LP}) = 53/5$ — i
due rilassamenti coincidono perché i vincoli di assegnamento implicano già
$x_{jm} \le 1$ — e i duali non nulli sono $\tilde\mu = (2,\ 4{,}8,\ 5)$ e
$\tilde\pi_2 = -0{,}2$: la macchina 2 è la sola risorsa stretta.
