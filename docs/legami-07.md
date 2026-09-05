# 3.7 Il valore assoluto

**Tecnica:** continua con continue (e una binaria, quando serve) · **Script:** `python/cap03_legami.py` · [Tutte le tecniche](legami.md)

## Il legame in parole

Si vuole $|u - v|$: uno scarto, un errore, uno sbilanciamento. Il caso in
obiettivo e il caso in vincolo si comportano in modo **radicalmente diverso**.

## I vincoli

- **In obiettivo, minimizzando**: una variabile $d \ge 0$ e due vincoli,

    $$d \ge u - v, \qquad d \ge v - u \qquad (2 \text{ vincoli}),$$

    con $d$ nell'obiettivo da minimizzare. Nessuna binaria.

- **Come vincolo $\le$**: $|u - v| \le k$ è semplicemente $u - v \le k$ e
  $v - u \le k$ ($2$ vincoli, nessuna binaria).

- **Come vincolo $\ge$**: $|u - v| \ge k$ **non** si scrive senza binarie. È la
  disgiunzione «$u - v \ge k$ *oppure* $v - u \ge k$», e richiede una binaria
  $b$ e un big-M:

    $$u - v \ge k - M(1 - b), \qquad v - u \ge k - M b \qquad (2 \text{ vincoli}, 1 \text{ binaria}).$$

## La dimostrazione

Nel primo caso i due vincoli impongono $d \ge |u - v|$ (uno dei due membri
destri *è* $|u-v|$); l'obiettivo, che minimizza $d$ e in cui $d$ non compare
altrove, la porta all'uguaglianza con l'argomento di scambio della
[tecnica 3.5](legami-05.md). Nel terzo caso, $b = 1$ disattiva il secondo
vincolo (se $M \ge k + \max(v-u)$) e lascia il primo, e viceversa: è una
disgiunzione, non una congiunzione, e senza binaria si imporrebbero entrambi —
cioè $0 \ge 2k$, inammissibile per $k > 0$.

!!! danger "Il caso $\ge$ non è simmetrico al caso $\le$"
    $|u-v| \le k$ è l'intersezione di due semipiani: un insieme **convesso**,
    che si scrive con due vincoli lineari. $|u-v| \ge k$ è il complemento di una
    striscia: **non** è convesso, e nessun sistema di vincoli lineari senza
    variabili intere può descriverlo. La binaria non è un trucco: è necessaria.

## La forza del rilassamento

Sull'istanza dei cinque pesi, $\min |L_1 - L_2|$ ha ottimo
$z(\mathrm{MILP}) = 1$ e rilassamento $z(\mathrm{LP}^+) = 0$: il continuo divide
$21$ in due metà uguali e azzera lo scarto. Il rilassamento di un obiettivo di
valore assoluto è tipicamente $0$, cioè inutile.

## In gurobipy, e dove si rivede

```python
d = m.addVar(name="d")
m.addConstr(d >= u - v, name="abs_piu")
m.addConstr(d >= v - u, name="abs_meno")
```

Si rivede negli esercizi 11.3 (CD) e 11.2 (antitrust), e nella
[tecnica 3.13](legami-13.md) in una forma equivalente con due deviazioni.
