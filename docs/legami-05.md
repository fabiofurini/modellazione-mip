# 3.5 L'ausiliaria di massimo

**Tecnica:** continua con binarie · **Script:** `python/cap03_legami.py` · [Tutte le tecniche](legami.md)

## Il legame in parole

Una variabile $z$ deve valere il **massimo** di certe quantità: il tempo
dell'attività più lunga, il costo di connessione più alto, il carico della
macchina più carica.

## I vincoli

$$z ~\ge~ t_j\, x_j, \qquad \forall j \qquad (n \text{ vincoli}), \qquad z \ge 0.$$

## La dimostrazione, in tre passi

1. **Imposto dal vincolo.** Per ogni $j$ con $x_j = 1$ si ha $z \ge t_j$, quindi
   $z \ge \max_{j : x_j = 1} t_j$. Vale in ogni soluzione ammissibile.
2. **Dall'ottimalità.** Se $z$ compare nell'obiettivo con coefficiente
   strettamente positivo in un minimo (o strettamente negativo in un massimo) e
   in nessun altro vincolo, allora in ogni ottimo $z$ assume il valore più
   piccolo ammissibile: data una soluzione ottima con
   $z > \max_{j:x_j=1} t_j$, abbassare $z$ fino a quel massimo lascia tutti i
   vincoli soddisfatti e migliora strettamente l'obiettivo.
3. **Sintesi.** In ogni ottimo, $z = \max_{j : x_j = 1} t_j$ esattamente, con la
   convenzione che il massimo sull'insieme vuoto è $0$, garantita da $z \ge 0$.

!!! danger "Il passo 2 cade se $z$ è usata altrove"
    Se $z$ compare in un altro vincolo che la vuole *grande* — per esempio
    $z \ge$ qualcos'altro, come nella domanda 7.7.2 — l'argomento di scambio non
    funziona più: abbassare $z$ può violare quel vincolo. In quel caso
    $z \ge \max$ resta vero, ma $z = \max$ no.

## La forza del rilassamento

$\min z$ con $z \ge t_j x_j$, $t = (4, 7, 3)$ e $\sum_j x_j \ge 2$: l'ottimo
intero è $z(\mathrm{MILP}) = 4$ (si scelgono i lavori 1 e 3, e il massimo è 4).
Il rilassamento vale $168/61 \approx 2{,}75$: la soluzione frazionaria
$x_j = z/t_j$ spalma la scelta su tutti e tre i lavori e abbassa il massimo. Il
legame di massimo dà rilassamenti **deboli**: è una delle ragioni per cui i
problemi di makespan sono difficili.

## In gurobipy, e dove si rivede

```python
z = m.addVar(name="z")
m.addConstrs((z >= t[j] * x[j] for j in range(n)), name="massimo")
```

Si rivede nei problemi [7.4](scheduling-4.md), [7.7](scheduling-7.md),
[8.4](localizzazione-4.md) e 11.4 (libri sugli scaffali).
