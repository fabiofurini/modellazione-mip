# 3.13 Vincoli violabili, deviazioni e penalità

**Tecnica:** continue con continue · **Script:** `python/cap03_legami.py` · [Tutte le tecniche](legami.md)

## Il legame in parole

Un vincolo che si *preferirebbe* rispettare, ma che può essere violato pagando:
la domanda di un periodo, una preferenza di orario, un obiettivo di servizio.
Trasformare un vincolo rigido in uno morbido è spesso la differenza fra un
modello inammissibile e uno utile.

## I vincoli

Al posto di $a' x = \beta$ si scrive

$$a' x + s^- - s^+ = \beta, \qquad s^-,\ s^+ \ge 0
\qquad (1 \text{ vincolo}, 2 \text{ variabili continue}),$$

e nell'obiettivo si aggiunge $\pi^- s^- + \pi^+ s^+$ con penalità
$\pi^-, \pi^+ > 0$. La variabile $s^-$ misura di quanto si sta **sotto** il
target, $s^+$ di quanto si sta **sopra**.

## La dimostrazione

Il vincolo, da solo, è sempre soddisfacibile: qualunque $a'x$ si può compensare
con una delle due deviazioni. La proprietà interessante è che **in ogni ottimo
almeno una delle due deviazioni è nulla**: se $s^- = \sigma > 0$ e
$s^+ = \tau > 0$, sottrarre $\min(\sigma, \tau)$ da entrambe lascia il vincolo
soddisfatto (la differenza $s^- - s^+$ non cambia) e riduce l'obiettivo di
$(\pi^- + \pi^+)\min(\sigma,\tau) > 0$.

Quindi $s^-$ e $s^+$ sono davvero le parti positiva e negativa dello scarto, e
$s^- + s^+ = |a'x - \beta|$ in ogni ottimo: la stessa cosa della
[tecnica 3.7](legami-07.md), scritta con un'uguaglianza invece che con due
disuguaglianze.

!!! warning "Con penalità nulla le deviazioni perdono significato"
    Se $\pi^- = 0$, l'argomento di scambio non è più stretto e una soluzione
    ottima può avere entrambe le deviazioni positive: la lettura «$s^-$ è la
    sotto-copertura» non è più garantita. Vale la stessa regola di tutto il
    capitolo: la forza della conclusione dipende dal segno del coefficiente
    nell'obiettivo.

## L'esempio

Domanda $6$ in ciascuno di tre periodi, disponibilità totale $15 < 18$,
penalità $\pi^+ = 3$ e $\pi^- = 2$. Il modello rigido sarebbe **inammissibile**;
quello morbido dà $z(\mathit{MILP}) = 6$, con $q = (3, 6, 6)$ e una
sotto-copertura di $3$ concentrata sul primo periodo. Nulla, nei dati, dice che
vada concentrata: qualunque ripartizione della sotto-copertura totale $3$ ha lo
stesso costo, e il solver ne restituisce una.

## In gurobipy, e dove si rivede

```python
sm = m.addVars(T, name="s_meno");  sp = m.addVars(T, name="s_piu")
m.addConstrs((q[t] + sm[t] - sp[t] == domanda[t] for t in range(T)), name="target")
m.setObjective(costo + gp.quicksum(pen_giu * sm[t] + pen_su * sp[t] for t in range(T)),
               GRB.MINIMIZE)
```

Si rivede nel modello numerico dell'orario della scuola di musica (EX 15) e
nell'esercizio 9.1.
