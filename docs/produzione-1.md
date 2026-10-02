# Lotti con costo fisso di lancio

**Classe:** MILP · **Legami:** costo fisso (big-M letto dai dati) · **Script:** `python/fam09_1_lotti.py`<br>
**Difficoltà:** ★★★★☆ · **Tempo:** 45–60 min
{ .scheda }

[![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/fam09_1_lotti.ipynb)

!!! abstract "Problema 9.1"
    Un'azienda deve pianificare la produzione di un unico prodotto su
    $n \in \mathbb{Z}_{\ge 1}$ periodi. Per ogni periodo $t$, $d_t$ è la domanda,
    $p_t$ il costo di produrre una unità e $q_t$ il costo fisso da sostenere se
    in quel periodo la produzione viene lanciata. Per ogni $t \le n-1$, $h_t$ è
    il costo di tenere una unità in magazzino a fine periodo. La scorta iniziale
    è $r_0$, quella finale richiesta è $r_n$. Si vuole soddisfare tutta la
    domanda al costo totale minimo.

**Il problema a parole.** *Decidiamo* quanto produrre in ogni periodo, e di
conseguenza quanto resta in magazzino. *L'obiettivo*: costo totale (produzione,
lanci e magazzino) minimo. *I vincoli*: la domanda di ogni periodo va
soddisfatta esattamente, e non si può produrre senza pagare il costo fisso. È il
problema di **lot sizing** con setup.

## Modello

**Variabili.** $x_t \ge 0$ unità prodotte, $s_t \ge 0$ scorta a fine periodo
($t \le n-1$), $y_t \in \{0,1\}$ lancio della produzione.

<!-- modello: 9.1 -->

$$
\begin{aligned}
\min ~~ \sum_{t=1}^{n} p_t\, x_t + \sum_{t=1}^{n} q_t\, y_t + \sum_{t=1}^{n-1} h_t\, s_t & & \\
\text{soggetto a} \quad x_1 - s_1 &= d_1 - r_0, & \\
x_t + s_{t-1} - s_t &= d_t, & \forall t \in \{2, 3, \dots, n-1\}, \\
x_n + s_{n-1} &= d_n + r_n, & \\
-x_t + M_t\, y_t &\ge 0, & \forall t \in \{1, 2, \dots, n\}, \\
x_t &\ge 0, & \forall t \in \{1, 2, \dots, n\}, \\
s_t &\ge 0, & \forall t \in \{1, 2, \dots, n-1\}, \\
y_t &\in \{0, 1\}, & \forall t \in \{1, 2, \dots, n\}.
\end{aligned}
$$

<!-- modello: fine -->

**Il legame.** Il vincolo $x_t \le M_t\, y_t$ dice: se $y_t = 0$ allora
$x_t = 0$ (senza lancio non si produce); se $y_t = 1$ il vincolo non è
restrittivo. Il verso opposto — se $x_t = 0$ allora $y_t = 0$ — non è imposto da
alcun vincolo ma segue dall'**ottimalità**, perché porre $y_t = 0$ resta
ammissibile e fa risparmiare $q_t$. Se $q_t > 0$ ogni soluzione ottima ha
$y_t = 0$; se $q_t = 0$ il risparmio è nullo e si può dire soltanto che
*esiste* una soluzione ottima con $y_t = 0$.

!!! warning "Il big-M si legge dai dati"
    Un $M_t$ valido deve essere almeno la massima quantità che conviene produrre
    nel periodo $t$. In una soluzione ottima non si produce mai più della domanda
    che resta da coprire:

    $$M_t = \sum_{\tau = t}^{n} d_\tau + r_n .$$

    Nel primo periodo si può togliere la scorta iniziale, che è un dato:
    $M_1 = \sum_{\tau = 1}^{n} d_\tau + r_n - r_0$. Dal secondo in poi la
    scorta che entra non è nota a priori, e il bound resta quello scritto
    sopra. Sull'istanza $r_0 = 0$, quindi i due valori coincidono.

    Ogni valore più grande è ancora valido ma **indebolisce** il rilassamento LP;
    ogni valore più piccolo può tagliare soluzioni ottime. Sull'istanza
    $M = (110, 90, 80, 50, 10)$: il big-M dell'ultimo periodo vale $10$, non $110$.

## Il modello in gurobipy

```python
m = gp.Model("lotti")
x = m.addVars(n, name="x")
s = m.addVars(n - 1, name="s")
y = m.addVars(n, vtype=GRB.BINARY, name="y")
m.setObjective(gp.quicksum(p[t] * x[t] for t in range(n))
               + gp.quicksum(q[t] * y[t] for t in range(n))
               + gp.quicksum(h[t] * s[t] for t in range(n - 1)), GRB.MINIMIZE)
m.addConstr(x[0] - s[0] == d[0] - r0, name="bilancio[0]")
m.addConstrs((x[t] + s[t - 1] - s[t] == d[t] for t in range(1, n - 1)), name="bilancio")
m.addConstr(x[n - 1] + s[n - 2] == d[n - 1] + rn, name=f"bilancio[{n - 1}]")
m.addConstrs((-x[t] + M[t] * y[t] >= 0 for t in range(n)), name="lancio")
```

## L'istanza

$n = 5$ giorni, $r_0 = r_n = 0$, domanda totale $110$ unità.

| | $t=1$ | $t=2$ | $t=3$ | $t=4$ | $t=5$ |
|---|---:|---:|---:|---:|---:|
| $d_t$ | 20 | 10 | 30 | 40 | 10 |
| $p_t$ | 2 | 3 | 2 | 3 | 2 |
| $q_t$ | 50 | 50 | 50 | 50 | 50 |
| $M_t$ | 110 | 90 | 80 | 50 | 10 |
| $h_t$ | 1 | 1 | 1 | 1 | — |

Il modello scritto sui dati dell'istanza:

<!-- modello-esteso: fam09_1_primale -->

<div class="modello-esteso largo" markdown>

$$
\begin{array}{rrrrrrrrrrrrrrr c l}
\min & 2x_1 & +3x_2 & +2x_3 & +3x_4 & +2x_5 & +s_1 & +s_2 & +s_3 & +s_4 & +50y_1 & +50y_2 & +50y_3 & +50y_4 & +50y_5 &  & \\
\text{soggetto a} & x_1 &  &  &  &  & -s_1 &  &  &  &  &  &  &  &  & = & 20\\
 &  & x_2 &  &  &  & +s_1 & -s_2 &  &  &  &  &  &  &  & = & 10\\
 &  &  & x_3 &  &  &  & +s_2 & -s_3 &  &  &  &  &  &  & = & 30\\
 &  &  &  & x_4 &  &  &  & +s_3 & -s_4 &  &  &  &  &  & = & 40\\
 &  &  &  &  & x_5 &  &  &  & +s_4 &  &  &  &  &  & = & 10\\
 & -x_1 &  &  &  &  &  &  &  &  & +110y_1 &  &  &  &  & \ge & 0\\
 &  & -x_2 &  &  &  &  &  &  &  &  & +90y_2 &  &  &  & \ge & 0\\
 &  &  & -x_3 &  &  &  &  &  &  &  &  & +80y_3 &  &  & \ge & 0\\
 &  &  &  & -x_4 &  &  &  &  &  &  &  &  & +50y_4 &  & \ge & 0\\
 &  &  &  &  & -x_5 &  &  &  &  &  &  &  &  & +10y_5 & \ge & 0\\
 & x_1, & x_2, & x_3, & x_4, & x_5 &  &  &  &  &  &  &  &  &  & \ge & 0\\
 &  &  &  &  &  & s_1, & s_2, & s_3, & s_4 &  &  &  &  &  & \ge & 0\\
 &  &  &  &  &  &  &  &  &  & y_1, & y_2, & y_3, & y_4, & y_5 & \in & \{0, 1\}
\end{array}
$$

</div>

<!-- modello-esteso: fine -->

## Euristiche costruttive: il bound primale

**(a) Lot-for-lot.** Si produce ogni giorno esattamente la domanda: nessuna
scorta, ma un lancio ogni giorno. Costo $270 + 250 = 520$.

**(b) Least unit cost.** Si parte dal primo periodo scoperto e si copre con un
solo lancio il numero di periodi che minimizza il costo medio per unità,

$$\frac{q + \sum_{i=1}^{k-1} h \cdot (\text{unità tenute } i \text{ periodi})}
       {\sum_{i=0}^{k-1} d_{t+i}} ,$$

poi si ricomincia. Costo $O(n^2)$. Al numeratore ci sono solo il lancio e il
magazzino: il costo di produzione $p$ non compare perché le alternative che si
confrontano partono tutte dallo stesso periodo e coprono comunque le stesse
domande, quindi pagano lo stesso $p$ per unità e non cambiano il confronto. I
numeri qui sotto sono dunque costi *incrementali* di lancio più magazzino, non
il costo pieno di un'unità.

- periodo 1: copre fino al 2, quantità $30$, costo medio $2$;
- periodo 3: copre fino al 4, quantità $70$, costo medio $\approx 1{,}286$;
- periodo 5: copre solo sé stesso, quantità $10$, costo medio $5$.

Si lancia nei giorni $1, 3, 5$, per un costo di $420$. Tenendo la migliore delle
due, $z(\mathit{MILP}) \le \mathit{UB} = 420$.

## Rilassamento LP e duale: il bound duale

Con $\mu_t$ **libera** su ogni bilancio e $\pi_t \ge 0$ su ogni vincolo di
lancio:

<!-- modello: 9.1-duale -->

$$
\begin{aligned}
\max ~~ \sum_{t=1}^{n} b_t\, \mu_t & & \\
\text{soggetto a} \quad \mu_t - \pi_t &\le p_t, & \forall t \in \{1, 2, \dots, n\}, \\
M_t\, \pi_t &\le q_t, & \forall t \in \{1, 2, \dots, n\}, \\
-\mu_t + \mu_{t+1} &\le h_t, & \forall t \in \{1, 2, \dots, n-1\}, \\
\mu_t &\gtreqless 0, & \forall t \in \{1, 2, \dots, n\}, \\
\pi_t &\ge 0, & \forall t \in \{1, 2, \dots, n\}.
\end{aligned}
$$

<!-- modello: fine -->

Lo stesso duale, scritto sui dati dell'istanza:

<!-- modello-esteso: fam09_1_duale -->

<div class="modello-esteso largo" markdown>

$$
\begin{array}{rrrrrrrrrrr c l}
\max & 20\mu_1 & +10\mu_2 & +30\mu_3 & +40\mu_4 & +10\mu_5 &  &  &  &  &  &  & \\
\text{soggetto a} & \mu_1 &  &  &  &  & -\pi_1 &  &  &  &  & \le & 2\\
 &  & \mu_2 &  &  &  &  & -\pi_2 &  &  &  & \le & 3\\
 &  &  & \mu_3 &  &  &  &  & -\pi_3 &  &  & \le & 2\\
 &  &  &  & \mu_4 &  &  &  &  & -\pi_4 &  & \le & 3\\
 &  &  &  &  & \mu_5 &  &  &  &  & -\pi_5 & \le & 2\\
 &  &  &  &  &  & 110\pi_1 &  &  &  &  & \le & 50\\
 &  &  &  &  &  &  & 90\pi_2 &  &  &  & \le & 50\\
 &  &  &  &  &  &  &  & 80\pi_3 &  &  & \le & 50\\
 &  &  &  &  &  &  &  &  & 50\pi_4 &  & \le & 50\\
 &  &  &  &  &  &  &  &  &  & 10\pi_5 & \le & 50\\
 & -\mu_1 & +\mu_2 &  &  &  &  &  &  &  &  & \le & 1\\
 &  & -\mu_2 & +\mu_3 &  &  &  &  &  &  &  & \le & 1\\
 &  &  & -\mu_3 & +\mu_4 &  &  &  &  &  &  & \le & 1\\
 &  &  &  & -\mu_4 & +\mu_5 &  &  &  &  &  & \le & 1\\
 & \mu_1, & \mu_2, & \mu_3, & \mu_4, & \mu_5 &  &  &  &  &  & \gtreqless & 0\\
 &  &  &  &  &  & \pi_1, & \pi_2, & \pi_3, & \pi_4, & \pi_5 & \ge & 0
\end{array}
$$

</div>

<!-- modello-esteso: fine -->

**Ricetta.** $\bar\pi_t = 0$: i lanci si regalano. Restano $\mu_t \le p_t$ e
$\mu_{t+1} \le \mu_t + h_t$, e il valore più grande ammissibile si costruisce in
avanti,

$$\bar\mu_1 = p_1, \qquad \bar\mu_t = \min(\bar\mu_{t-1} + h_{t-1},\ p_t).$$

La lettura è diretta: $\bar\mu_t$ è il costo unitario più basso per avere una
unità disponibile nel periodo $t$, o producendola allora, o producendola prima e
tenendola in magazzino. Sull'istanza $\bar\mu = (2, 3, 2, 3, 2)$ e

$$\mathit{LB} = 2{\cdot}20 + 3{\cdot}10 + 2{\cdot}30 + 3{\cdot}40 + 2{\cdot}10 = 270 .$$

È il costo di produzione se i lanci fossero gratuiti: valido, e volutamente
ottimista.

**Quello che dice il solver.** $z(\mathit{LP}) = z(\mathit{LP}^+) = 3890/11
\approx 353{,}6$: il rilassamento i lanci li paga in frazione
($\pi_t = q_t/M_t$ è ammissibile). L'ottimo intero lancia nei giorni 1 e 3.

| | $t=1$ | $t=2$ | $t=3$ | $t=4$ | $t=5$ |
|---|---:|---:|---:|---:|---:|
| lancio $y_t$ | 1 | 0 | 1 | 0 | 0 |
| produzione $x_t$ | 30 | 0 | 80 | 0 | 0 |
| scorta $s_t$ | 10 | 0 | 50 | 10 | — |

| $UB$ | $LB$ (duale) | $z(\mathit{LP})$ | $z(\mathit{LP}^+)$ | $z(\mathit{MILP})$ | gap dell'euristica |
|---:|---:|---:|---:|---:|---:|
| 420 | 270 | $3890/11$ | $3890/11$ | 390 | $7{,}7\%$ |

![Piano ottimo](img/cap09_lotti_ottimo.png)

## Considerazioni aggiuntive

- Il problema si risolve in tempo $O(n^2)$ con la programmazione dinamica di
  **Wagner–Whitin**. La least unit cost *non* è quell'algoritmo: è una regola
  miope che guarda un lancio per volta, e infatti si ferma a $420$ contro $390$.
- La disuguaglianza valida $x_t \le M_t$ non aggiunge nulla: $M_t$ è già la
  massima produzione utile, e infatti $z(\mathit{LP}) = z(\mathit{LP}^+)$.
- Una formulazione alternativa con variabili $x_{t\tau}$ («prodotte in $t$,
  vendute in $\tau$») ha rilassamento **intero** ma $O(n^2)$ variabili: il tipico
  scambio fra dimensione del modello e qualità del rilassamento.

## Domande di modellazione aggiuntive

??? question "9.1.1 — Lotto minimo"
    Se in un giorno si produce, si devono produrre almeno $25$ unità. Come cambia
    il modello? Qual è il nuovo ottimo?

## Una variante svolta: capacità giornaliera

L'impianto non può produrre più di $35$ unità al giorno.

Si aggiungono gli $n$ vincoli lineari

$$
x_t \le 35, \qquad \forall t \in \{1, 2, \dots, n\} .
$$

In alternativa si può sostituire il big-M con $M_t' = \min(M_t, 35)$: il
vincolo diventa allora sia il legame di attivazione sia il
vincolo di capacità, esattamente come nella localizzazione capacitata del
capitolo «Localizzazione e copertura». Sull'istanza il piano ottimo con due soli
lanci non è più ammissibile ($80 > 35$) e l'ottimo sale a $470$.

Il tetto $x_t \le 35$ aggiunge al duale una famiglia $\nu_t \ge 0$ con termine
noto $-35$: entra nell'obiettivo con il segno negativo e allenta la colonna di
$x_t$. Alzare $\nu_t$ di una unità alza il tetto su $\mu_t$ e incassa $d_t$, ma
costa $35$, quindi conviene solo dove la domanda supera la capacità; e
sull'istanza nemmeno il giorno più carico lo giustifica, perché la catena delle
scorte tiene già $\mu_t$ sotto il tetto. Il certificato resta allora quello del
problema base, $\lb = 270$. Cambia invece l'euristica: il quarto giorno il
lot-for-lot sforerebbe, e le $5$ unità in eccesso si anticipano al terzo, che le
tiene in magazzino.

<!-- tabella-variante: fam09_1a_bound -->

|  | valore | che cos'è |
|---|---:|---|
| $\mathit{UB}$ | $520$ | soluzione euristica |
| $\mathit{LB}$ | $270$ | certificato duale costruito a mano |
| $z(\mathit{LP})$ | $\frac{305365}{792}$ | rilassamento senza i bound |
| $z(\mathit{LP}^+)$ | $\frac{305365}{792}$ | rilassamento con i bound |
| $z(\mathit{MILP})$ | $470$ | ottimo del MILP |

<!-- tabella-variante: fine -->

## Codice

Script completo —
[`python/fam09_1_lotti.py`](https://github.com/fabiofurini/modellazione-mip/blob/main/python/fam09_1_lotti.py)
(riproducibile con `python3 python/fam09_1_lotti.py` dalla cartella `python/`).
Notebook —
[`notebooks/fam09_1_lotti.ipynb`](https://github.com/fabiofurini/modellazione-mip/blob/main/notebooks/fam09_1_lotti.ipynb)
— che si apre in Colab dal badge in cima alla pagina.

<!-- script-incorporato: inizio (rigenerato da python/incorpora_codice.py) -->

??? example "Mostra lo script completo — `python/fam09_1_lotti.py` (259 righe)"

    ```python
    """Problema 9.1 -- Produzione e lotti con costo fisso di lancio.

    Bilancio delle scorte, attivazione della produzione con big-M e magazzino. Il
    legame e' quello del costo fisso (sezione 3.2) con il coefficiente ricavato dai
    dati: M_t e' la domanda residua, non un numero grande a caso.
    """
    import gurobipy as gp
    import pandas as pd
    from gurobipy import GRB

    from euristiche import euristica_lotti
    from mip import (ammissibile, dualita_forte, due_rilassamenti, frazione,
                     nuovo_modello, registra_bound, rilassamenti, risolvi, valuta)
    from stile import ARANCIO, BLU, ROSSO, TEAL, VERDE, intestazione, plt, salva_dati, salva_figura
    from esteso import salva_modello

    R = range

    # ---------- 1. MODELLO E ISTANZA ----------
    intestazione("9.1 Produzione e lotti: bilancio delle scorte, lancio con costo fisso")
    d1 = [20, 10, 30, 40, 10]          # domanda dei cinque giorni
    p1 = [2, 3, 2, 3, 2]               # costo unitario di produzione
    q1 = [50, 50, 50, 50, 50]          # costo fisso di lancio
    h1 = [1, 1, 1, 1]                  # costo di magazzino a fine giorno (t = 1..n-1)
    r0, rn = 0, 0                      # scorta iniziale e finale richiesta
    n1 = len(d1)
    # il piu' piccolo big-M valido: in un ottimo non si produce mai piu' della domanda residua
    M1 = [sum(d1[t:]) + rn for t in R(n1)]
    salva_dati(pd.DataFrame({"giorno": R(1, n1 + 1), "domanda": d1, "costo_unitario": p1,
                             "costo_lancio": q1, "M": M1}), "fam09_1_dati")


    def modello_1(d, p, q, h, r0, rn):
        n = len(d)
        M = [sum(d[t:]) + rn for t in R(n)]
        m = nuovo_modello("lotti")
        x = m.addVars(n, name="x")                       # quantita' prodotta
        s = m.addVars(n - 1, name="s")                   # scorta a fine giorno t
        y = m.addVars(n, vtype=GRB.BINARY, name="y")     # lancio della produzione
        m.setObjective(gp.quicksum(p[t] * x[t] for t in R(n))
                       + gp.quicksum(q[t] * y[t] for t in R(n))
                       + gp.quicksum(h[t] * s[t] for t in R(n - 1)), GRB.MINIMIZE)
        m.addConstr(x[0] - s[0] == d[0] - r0, name="bilancio[0]")
        m.addConstrs((x[t] + s[t - 1] - s[t] == d[t] for t in R(1, n - 1)), name="bilancio")
        m.addConstr(x[n - 1] + s[n - 2] == d[n - 1] + rn, name=f"bilancio[{n - 1}]")
        m.addConstrs((-x[t] + M[t] * y[t] >= 0 for t in R(n)), name="lancio")
        return m, x, s, y


    def duale_1(d, p, q, h, r0, rn):
        """max sum_t b_t mu_t;  mu_t - pi_t <= p_t;  M_t pi_t <= q_t;  -mu_t + mu_{t+1} <= h_t;
        mu libere, pi >= 0."""
        n = len(d)
        M = [sum(d[t:]) + rn for t in R(n)]
        b = [d[0] - r0] + d[1:n - 1] + [d[n - 1] + rn]
        dl = nuovo_modello("duale_lotti")
        mu = dl.addVars(n, lb=-GRB.INFINITY, name="mu")
        pi = dl.addVars(n, name="pi")
        dl.setObjective(gp.quicksum(b[t] * mu[t] for t in R(n)), GRB.MAXIMIZE)
        dl.addConstrs((mu[t] - pi[t] <= p[t] for t in R(n)), name="rc_x")
        dl.addConstrs((M[t] * pi[t] <= q[t] for t in R(n)), name="rc_y")
        dl.addConstrs((-mu[t] + mu[t + 1] <= h[t] for t in R(n - 1)), name="rc_s")
        return dl


    m1, x1, s1, y1 = modello_1(d1, p1, q1, h1, r0, rn)
    salva_modello(m1, "fam09_1_primale")
    print(f"  Domanda totale {sum(d1)}; big-M per giorno (domanda residua): {M1}")

    # ---------- 2. IL RILASSAMENTO LP ----------
    zlp1, zlp1r, pi1 = rilassamenti(m1)

    # ---------- 3. IL DUALE DEL RILASSAMENTO (LOWER BOUND) ----------
    dl1 = duale_1(d1, p1, q1, h1, r0, rn)
    salva_modello(dl1, "fam09_1_duale")
    # ricetta: pi = 0 (i lanci si regalano) e mu_t = costo minimo per avere una unita' al giorno t
    mu = []
    for t in R(n1):
        mu.append(p1[t] if t == 0 else min(mu[t - 1] + h1[t - 1], p1[t]))
    mano = {f"mu[{t}]": mu[t] for t in R(n1)}
    lb1, viol = valuta(dl1, mano)
    assert viol <= 1e-9, viol
    print("  Duale a mano: pi = 0 (i lanci non si pagano) e mu_t = il costo unitario piu' basso")
    print("  per avere una unita' disponibile il giorno t, cioe' min(mu_{t-1} + h_{t-1}, p_t):")
    print("    mu = " + ", ".join(frazione(v) for v in mu))
    print(f"  ->  lb = {frazione(lb1)}: e' il costo di produzione se i lanci fossero gratis.")
    dualita_forte(dl1, zlp1)

    # ---------- 4. EURISTICA COSTRUTTIVA (UPPER BOUND) ----------
    # (a) lot-for-lot: si produce ogni giorno esattamente la domanda, niente scorte
    lot_per_lot = sum(p1[t] * d1[t] for t in R(n1)) + sum(q1)
    sol_llf = {f"x[{t}]": d1[t] for t in R(n1)} | {f"y[{t}]": 1 for t in R(n1)} \
        | {f"s[{t}]": 0 for t in R(n1 - 1)}
    assert ammissibile(m1, sol_llf)
    print(f"  (a) lot-for-lot: si lancia ogni giorno, costo "
          f"{sum(p1[t] * d1[t] for t in R(n1))} di produzione + {sum(q1)} di lanci = {lot_per_lot}")
    # (b) least unit cost: si copre il numero di giorni che minimizza il costo medio per unita'
    e = euristica_lotti(d1, q1[0], h1[0])
    e.traccia.stampa()
    sol_luc = {f"x[{t}]": e.lanci.get(t, 0) for t in R(n1)} \
        | {f"y[{t}]": 1 if t in e.lanci else 0 for t in R(n1)}
    scorta = 0
    for t in R(n1 - 1):
        scorta += sol_luc[f"x[{t}]"] - d1[t]
        sol_luc[f"s[{t}]"] = scorta
    assert ammissibile(m1, sol_luc)
    luc = sum(p1[t] * sol_luc[f"x[{t}]"] for t in R(n1)) + sum(q1[t] for t in e.lanci) \
        + sum(h1[t] * sol_luc[f"s[{t}]"] for t in R(n1 - 1))
    print(f"  (b) least unit cost: lanci nei giorni {[t + 1 for t in sorted(e.lanci)]}, costo {luc}")
    ub1 = min(lot_per_lot, luc)
    print(f"  La migliore delle due: ub = {frazione(ub1)}")

    # ---------- 5. OTTIMO DEL MILP ----------
    z1 = risolvi(m1)
    lanci_ott = [t + 1 for t in R(n1) if y1[t].X > 0.5]
    print(f"  Soluzione ottima: lanci nei giorni {lanci_ott}; quantita' "
          + ", ".join(frazione(x1[t].X) for t in R(n1))
          + "; scorte " + ", ".join(frazione(s1[t].X) for t in R(n1 - 1)))
    riga = registra_bound("1 lotti con setup", ub1, lb1, zlp1, zlp1r, z1)
    salva_dati(pd.DataFrame([riga]), "fam09_1_bound")
    assert lb1 <= zlp1 <= z1 <= ub1 + 1e-9

    # ---------- 6. DOMANDE DI MODELLAZIONE AGGIUNTIVE ----------
    varianti = {}


    def variante(nome, m):
        z = risolvi(m)
        print(f"  {nome:70s} z = {frazione(z)}")
        return z


    # 1a: capacita' giornaliera di 35 litri
    m, x, s, y = modello_1(d1, p1, q1, h1, r0, rn)
    m.addConstrs((x[t] <= 35 for t in R(n1)), name="capacita")
    varianti["1a"] = variante("1a. Capacita' giornaliera di 35 litri (x_t <= 35)", m)
    # 1b: lotto minimo di 25 litri quando si produce (variabile semicontinua)
    m, x, s, y = modello_1(d1, p1, q1, h1, r0, rn)
    m.addConstrs((x[t] >= 25 * y[t] for t in R(n1)), name="lotto_minimo")
    varianti["1b"] = variante("1b. Lotto minimo di 25 litri se si produce (x_t >= 25 y_t)", m)
    salva_dati(pd.DataFrame({"variante": list(varianti), "z": list(varianti.values())}),
               "fam09_1_varianti")

    # ---------- 7. IL SANDWICH SULLA VARIANTE 1a ----------
    intestazione("9.1a Il sandwich sulla variante: capacita' giornaliera di 35 litri")
    CAP = 35


    def modello_1a(d, p, q, h, r0, rn, cap=CAP):
        mm, xx, ss, yy = modello_1(d, p, q, h, r0, rn)
        mm.addConstrs((xx[t] <= cap for t in R(len(d))), name="capacita")
        return mm, xx, ss, yy


    def duale_1a(d, p, q, h, r0, rn, cap=CAP):
        """Al duale di 9.1 si aggiunge nu_t >= 0 per ogni vincolo di capacita'
        x_t <= cap, scritto come -x_t >= -cap: entra nell'obiettivo con il suo
        termine noto, negativo, e allenta la colonna di x_t."""
        nn = len(d)
        MM = [sum(d[tt:]) + rn for tt in R(nn)]
        b = [d[0] - r0] + d[1:nn - 1] + [d[nn - 1] + rn]
        dl = nuovo_modello("duale_lotti_1a")
        mu = dl.addVars(nn, lb=-GRB.INFINITY, name="mu")
        pi = dl.addVars(nn, name="pi")
        nu = dl.addVars(nn, name="nu")
        dl.setObjective(gp.quicksum(b[tt] * mu[tt] for tt in R(nn))
                        - cap * nu.sum(), GRB.MAXIMIZE)
        dl.addConstrs((mu[tt] - pi[tt] - nu[tt] <= p[tt] for tt in R(nn)), name="rc_x")
        dl.addConstrs((MM[tt] * pi[tt] <= q[tt] for tt in R(nn)), name="rc_y")
        dl.addConstrs((-mu[tt] + mu[tt + 1] <= h[tt] for tt in R(nn - 1)), name="rc_s")
        return dl


    m1a, x1a, s1a, y1a = modello_1a(d1, p1, q1, h1, r0, rn)
    salva_modello(m1a, "fam09_1a_primale")

    # -- euristica ammissibile: lot-for-lot non sfora mai la capacita' se la domanda non la supera --
    print("Euristica costruttiva: si produce ogni giorno la domanda del giorno (lot-for-lot). Se")
    print("un giorno la domanda supera la capacita', l'eccedenza si anticipa al giorno prima, che")
    print("la tiene in magazzino: e' l'unico modo di coprirla rispettando il vincolo.")
    prod = list(d1)
    for tt in R(n1 - 1, 0, -1):
        if prod[tt] > CAP:
            ecc = prod[tt] - CAP
            prod[tt] -= ecc
            prod[tt - 1] += ecc
            print(f"  giorno {tt + 1}: domanda {d1[tt]} oltre la capacita'; {ecc} unita' anticipate "
                  f"al giorno {tt}")
    assert max(prod) <= CAP, "l'anticipo non basta: servirebbe spalmare su piu' giorni"
    scorte = []
    acc = 0
    for tt in R(n1 - 1):
        acc += prod[tt] - d1[tt]
        scorte.append(acc)
    ub1a = (sum(p1[tt] * prod[tt] for tt in R(n1)) + sum(q1[tt] for tt in R(n1) if prod[tt] > 0)
            + sum(h1[tt] * scorte[tt] for tt in R(n1 - 1)))
    sol_1a = ({f"x[{tt}]": prod[tt] for tt in R(n1)}
              | {f"y[{tt}]": (1 if prod[tt] > 0 else 0) for tt in R(n1)}
              | {f"s[{tt}]": scorte[tt] for tt in R(n1 - 1)})
    assert ammissibile(m1a, sol_1a), "la soluzione euristica della variante deve essere ammissibile"
    print(f"  produzione {prod}, scorte {scorte}  ->  ub = {frazione(ub1a)}")

    # -- certificato duale: nu paga cap e incassa la domanda del giorno --
    dl1a = duale_1a(d1, p1, q1, h1, r0, rn)
    salva_modello(dl1a, "fam09_1a_duale")
    b1 = [d1[0] - r0] + d1[1:n1 - 1] + [d1[n1 - 1] + rn]


    def valore_duale_1a(nu_val, giorno):
        """Alzando nu_giorno il tetto su mu_giorno sale, ma si paga cap per unita'."""
        nu_v = [nu_val if tt == giorno else 0.0 for tt in R(n1)]
        mu_v = []
        for tt in R(n1):
            tetto = p1[tt] + nu_v[tt]
            mu_v.append(tetto if tt == 0 else min(mu_v[tt - 1] + h1[tt - 1], tetto))
        return sum(b1[tt] * mu_v[tt] for tt in R(n1)) - CAP * sum(nu_v), mu_v, nu_v


    giorno_1a = max(R(n1), key=lambda tt: b1[tt])
    candidati_1a = [0.0] + [abs(p1[tt] - p1[giorno_1a]) + k for tt in R(n1) for k in (0, 1, 2)]
    migliore_1a = max(sorted(set(candidati_1a)), key=lambda v: valore_duale_1a(v, giorno_1a)[0])
    lb1a, mu_1a, nu_1a = valore_duale_1a(migliore_1a, giorno_1a)
    mano_1a = ({f"mu[{tt}]": mu_1a[tt] for tt in R(n1)}
               | {f"nu[{tt}]": nu_1a[tt] for tt in R(n1)})
    lb1a_val, viol_1a = valuta(dl1a, mano_1a)
    assert viol_1a <= 1e-9, viol_1a
    print("Soluzione duale a mano: pi = 0 come nel problema base. Alzare nu_t di una unita' alza")
    print(f"  il tetto su mu_t e incassa b_t, ma costa cap = {CAP}: conviene solo dove la domanda")
    print("  supera la capacita'. Si prova sul giorno di domanda massima, il "
          f"{giorno_1a + 1} (b = {b1[giorno_1a]}).")
    if migliore_1a > 0:
        print(f"  Il migliore e' nu = {frazione(migliore_1a)}.")
    else:
        print("  Qui nu resta a zero: anche sul giorno piu' carico la catena delle scorte tiene")
        print("  mu sotto il tetto, quindi alzare nu costerebbe senza alzare nulla.")
    print(f"  ->  lb = {frazione(lb1a_val)}")
    zlp1a, zlp1ar, _ = due_rilassamenti(m1a, dl1a)
    z1a = risolvi(m1a)
    riga_1a = registra_bound("1a capacita' giornaliera", ub1a, lb1a_val, zlp1a, zlp1ar, z1a)
    salva_dati(pd.DataFrame([riga_1a]), "fam09_1a_bound")
    assert lb1a_val <= zlp1a <= z1a <= ub1a + 1e-9

    # ---------- 8. FIGURA ----------
    fig, ax = plt.subplots(figsize=(7.0, 3.4))
    giorni = list(R(1, n1 + 1))
    ax.bar(giorni, [x1[t].X for t in R(n1)], color=TEAL, label="produzione $x_t$", width=0.55)
    ax.plot(giorni, d1, "o--", color=ROSSO, label="domanda $d_t$")
    ax.plot(giorni[:-1], [s1[t].X for t in R(n1 - 1)], "s-", color=ARANCIO,
            label="scorta a fine giorno $s_t$")
    for t in lanci_ott:
        ax.annotate("lancio", (t, x1[t - 1].X), textcoords="offset points", xytext=(0, 6),
                    ha="center", fontsize=8, color=BLU)
    ax.set_xticks(giorni)
    ax.set_xlabel("giorno")
    ax.set_ylabel("litri")
    ax.set_title(f"9.1: piano ottimo (z = {frazione(z1)})")
    ax.legend(fontsize=8, ncols=3, loc="upper left")
    salva_figura(fig, "cap09_lotti_ottimo")
    print("Fine.")
    ```

<!-- script-incorporato: fine -->
