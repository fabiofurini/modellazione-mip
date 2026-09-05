# Che cos'è un modello MIP

**Classe:** LP · ILP · BIP · MILP · **Script:** `python/cap01_modelli.py`

[![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/cap01_modelli.ipynb)

## Dati, variabili, obiettivo, vincoli

Un modello di *programmazione matematica* traduce una decisione in quattro
ingredienti, sempre nello stesso ordine: i **dati** (i numeri noti prima di
decidere), le **variabili** (quello che il decisore controlla), l'**obiettivo**
(una funzione delle variabili da minimizzare o massimizzare) e i **vincoli** (le
equazioni e disequazioni che rendono realizzabile una soluzione).

!!! note "Notazione dei valori ottimi"
    $X$ è l'**insieme ammissibile** (i punti che soddisfano tutti i vincoli,
    domini compresi); $z(\mathrm{MILP})$, $z(\mathrm{LP})$, $z(\mathrm{D})$ sono
    i valori ottimi del MILP, del suo rilassamento e del duale del rilassamento.
    Le soluzioni **costruite a mano** si segnano con la barra ($\bar x$), quelle
    **ottime** con la tilde ($\tilde x$). I bound si chiamano $LB$ e
    $UB$, qualunque sia il verso dell'obiettivo. Si usa sempre
    $z(\mathrm{MILP})$ e mai $z^\star$: quale modello si ottimizza deve essere
    esplicito.

**Classi di modelli.** **LP** se obiettivo e vincoli sono lineari e le variabili
continue; **ILP** se tutte le variabili sono intere; **BIP** se tutte sono
$0/1$; **MILP** se alcune sono intere o binarie e altre continue. Questo corso
lavora quasi solo con MILP.

## Perché l'interezza conta

$$
\begin{aligned}
\max ~~ x_1 + x_2 & & \\
\text{soggetto a} \quad 2x_1 + 2x_2 &\le 3, & \\
x_1,\ x_2 &\in \{0,1\}. &
\end{aligned}
$$

Il rilassamento LP sostituisce $x_1, x_2 \in \{0,1\}$ con $0 \le x_1, x_2 \le 1$
e vale $z(\mathrm{LP}^+) = 3/2$. Quel valore è raggiunto da **infinite**
soluzioni ottime — tutti i punti del segmento $x_1 + x_2 = 3/2$ dentro il
quadrato — fra cui $(3/4, 3/4)$, $(1, 1/2)$ e $(1/2, 1)$. Quale il solver
restituisca dipende dall'algoritmo: sulla nostra installazione Gurobi dà
$(1/2, 1)$.

Arrotondando $(3/4, 3/4)$ all'intero più vicino si ottiene $(1,1)$, che viola il
vincolo ($2+2 = 4 > 3$): **non è nemmeno ammissibile**. Arrotondando $(1, 1/2)$
si ottiene $(1, 0)$, ammissibile di valore $1$ — che è proprio l'ottimo intero,
$z(\mathrm{MILP}) = 1$.

![Il rilassamento e i punti interi](img/cap01_rilassamento.png)

Due lezioni distinte: l'arrotondamento può produrre punti **non ammissibili**, e
quando ne produce di ammissibili non c'è garanzia sul loro valore; e il divario
$3/2 - 1 = 1/2$ non è colpa dell'arrotondamento — nessun punto intero
ammissibile vale più di $1$.

## I due rilassamenti, e da che parte stanno

!!! note "Due versioni da non confondere"
    - **rilassamento senza i bound** $z(\mathrm{LP})$: $x \in \{0,1\}$ diventa il solo
      $x \ge 0$. È quello di cui negli esercizi si scrive il duale a mano.
    - **rilassamento con i bound** $z(\mathrm{LP}^+)$:
      $x \in \{0,1\}$ diventa $0 \le x \le 1$. È `relax()` di Gurobi e il
      rilassamento della radice del branch-and-bound.

    In un massimo $z(\mathrm{LP}) \ge z(\mathrm{LP}^+) \ge z(\mathrm{MILP})$; in
    un minimo i versi si rovesciano. I due coincidono quando gli altri vincoli
    implicano già $x \le 1$ — per esempio con un vincolo di assegnamento
    $\sum_m x_{jm} = 1$.

Il rilassamento **toglie** vincoli, quindi

$$X_{\mathrm{MILP}} \subseteq X_{\mathrm{LP}^+} \subseteq X_{\mathrm{LP}},$$

e ottimizzare su un insieme più grande non può dare un valore peggiore. In un
massimo il rilassamento è un *upper* bound, in un minimo un *lower* bound: in
entrambi i casi è un bound **ottimistico**.

!!! warning "Da quale lato arriva ciascun bound"
    Il duale del rilassamento **non** dà un bound «dall'altro lato». Per dualità
    debole, in un minimo ogni soluzione duale ammissibile vale al più
    $z(\mathrm{LP})$, quindi al più $z(\mathrm{MILP})$: sta dalla *stessa* parte
    del rilassamento. Il bound dall'altro lato — quello *pessimistico* — viene
    solo da una soluzione ammissibile del MILP, cioè da un'euristica o dal
    solver. In un problema di **minimo**:

    $$z(\mathrm{D}) \le z(\mathrm{LP}) \le z(\mathrm{LP}^+) \le z(\mathrm{MILP}) \le c'\bar x$$

    per ogni $\bar x$ ammissibile intero; in un **massimo** tutti i versi si
    rovesciano.

## Tre «gap» da non confondere

1. **Gap dell'euristica**, quando l'ottimo è noto:
   $|z_{\text{eur}} - z(\mathrm{MILP})| / |z(\mathrm{MILP})|$. È quello riportato
   nelle tabelle degli esercizi.
2. **Divario certificato** fra due bound noti, senza conoscere l'ottimo:
   $(\mathit{UB} - \mathit{LB})/|\mathit{UB}|$ per un minimo con
   $\mathit{UB} > 0$. Garantisce che l'ottimo stia nell'intervallo, non che sia
   vicino a un estremo.
3. **`MIPGap` del solver**: la stessa idea, calcolata da Gurobi con i suoi
   `ObjVal` e `ObjBound` e le sue tolleranze.

Il numeratore è sempre in valore assoluto; se il denominatore è nullo il gap
relativo non si scrive e si riporta la differenza assoluta.

## Tre pattern che tornano ovunque

| Nome | Vincolo | Significato |
|---|---|---|
| **set partitioning** | $\sum_{i \in I} x_i = 1$ | esattamente un elemento di $I$ |
| **set packing** | $\sum_{i \in I} x_i \le 1$ | al più un elemento di $I$ |
| **set covering** | $\sum_{i \in I} x_i \ge 1$ | almeno un elemento di $I$ |

Il problema [7.1](scheduling-1.md) usa un *partitioning* per ogni lavoro, il
[7.3](scheduling-3.md) un *packing*, e il [capitolo 2](modellazione-2.md) mostra
il *covering* come traduzione diretta di una clausola OR.

## Branch-and-bound in una pagina

Per un problema di **minimo**:

1. si risolve il rilassamento LP del sottoproblema: se è inammissibile si
   scarta; se la soluzione è intera diventa un candidato **incumbent**;
2. altrimenti si sceglie una variabile frazionaria $x_j = v$ e si **ramifica**
   in $x_j \le \lfloor v \rfloor$ e $x_j \ge \lceil v \rceil$: ogni soluzione
   intera soddisfa una delle due, e nessuna entrambe;
3. si **pota** un sottoproblema il cui rilassamento vale più dell'incumbent;
4. si termina quando non restano sottoproblemi aperti.

Con variabili binarie l'albero ha al più $2^n$ foglie e l'algoritmo termina
certamente; con variabili intere illimitate la terminazione non è garantita.

!!! example "La traccia sull'esempio (è un massimo: si pota chi vale *meno*)"
    - **Radice.** $z(\mathrm{LP}^+) = 3/2$ con $(1/2, 1)$: $x_1$ è frazionaria.
    - **Ramo $x_1 \le 0$.** Ottimo $x_2 = 1$, valore $1$, intero: incumbent.
    - **Ramo $x_1 \ge 1$.** Ottimo $x_2 = 1/2$, valore $3/2$: ancora
      frazionaria. Il sottoramo $x_2 \le 0$ dà $(1,0)$ di valore $1$, che non
      migliora; il sottoramo $x_2 \ge 1$ è inammissibile.
    - **Fine.** $z(\mathrm{MILP}) = 1$, dimostrato. I cinque rilassamenti sono
      risolti dallo script e salvati in `dati/cap01_branch.csv`.

## Quello che questo capitolo lascia aperto

| Domanda | Dove si risponde |
|---|---|
| Come si traducono le condizioni logiche in vincoli lineari? | [Capitolo 2](modellazione-2.md) |
| Come si legano fra loro famiglie di variabili diverse? | [Capitolo 3](legami.md) |
| Come si costruisce a mano un bound ottimistico? | [Capitolo 4](modellazione-4.md) |
| Come si costruisce in fretta una soluzione ammissibile? | [Capitolo 5](modellazione-5.md) |
| Come si scrive tutto in Python/Gurobi e come si leggono i risultati? | [Capitolo 6](modellazione-6.md) |

## Codice

Lo script completo — i due rilassamenti, l'arrotondamento, la traccia del
branch-and-bound e la figura — è
[`python/cap01_modelli.py`](https://github.com/fabiofurini/modellazione-mip/blob/main/python/cap01_modelli.py)
(riproducibile con `python3 python/cap01_modelli.py` dalla cartella `python/`).
Lo stesso codice è disponibile come notebook —
[`notebooks/cap01_modelli.ipynb`](https://github.com/fabiofurini/modellazione-mip/blob/main/notebooks/cap01_modelli.ipynb)
— che si apre in Colab dal badge in cima alla pagina.

<!-- script-incorporato: inizio (rigenerato da python/incorpora_codice.py) -->

??? example "Mostra lo script completo — `python/cap01_modelli.py` (157 righe)"

    ```python
    """Capitolo 1 -- Che cos'e' un modello MIP: rilassamento, arrotondamento, bound.

    Verifica numerica degli esempi del capitolo: il controesempio
    dell'arrotondamento, i due rilassamenti (puro e con i bound conservati),
    l'ottimo intero e la traccia del branch-and-bound svolto a mano nel testo.
    Tutti i numeri citati nella dispensa e sul sito escono da qui.
    """
    import gurobipy as gp
    import numpy as np
    import pandas as pd
    from gurobipy import GRB

    from mip import (ammissibile, frazione, nuovo_modello, rilassamento, risolvi,
                     stampa_soluzione, valuta, viola_interezza)
    from stile import BLU, CICLO, GRIGIO, ROSSO, TEAL, VERDE, intestazione, plt, salva_dati, salva_figura

    R = range

    # ---------- 1. IL MODELLO DELL'ESEMPIO ----------
    intestazione("1. max x1 + x2  s.t.  2x1 + 2x2 <= 3,  x1, x2 binarie")


    def modello_esempio(binarie=True, superiore=True):
        """Il modello (1.1) del capitolo.

        binarie=True   -> MILP;  binarie=False -> rilassamento continuo
        superiore=True -> si conserva x <= 1 (rilassamento LP+); False -> solo x >= 0
        """
        m = nuovo_modello("arrotondamento")
        tipo = GRB.BINARY if binarie else GRB.CONTINUOUS
        ub = 1.0 if superiore else GRB.INFINITY
        x = m.addVars(2, vtype=tipo, lb=0.0, ub=ub, name="x")
        m.setObjective(x[0] + x[1], GRB.MAXIMIZE)
        m.addConstr(2 * x[0] + 2 * x[1] <= 3, name="risorsa")
        return m, x


    # ---------- 2. I DUE RILASSAMENTI ----------
    intestazione("2. I due rilassamenti: puro (x >= 0) e con i bound conservati (x <= 1)")
    m_lp, x_lp = modello_esempio(binarie=False, superiore=False)
    zlp = risolvi(m_lp)
    print(f"Rilassamento senza i bound   z(LP)  = {frazione(zlp)}   soluzione restituita dal solver:")
    stampa_soluzione(m_lp)
    m_lpp, x_lpp = modello_esempio(binarie=False, superiore=True)
    zlpp = risolvi(m_lpp)
    vertice = (x_lpp[0].X, x_lpp[1].X)
    print(f"Rilassamento LP+    z(LP+) = {frazione(zlpp)}   soluzione restituita dal solver: "
          f"({frazione(vertice[0])}, {frazione(vertice[1])})")
    print("Entrambi valgono 3/2: il vincolo di risorsa da' gia' x1 + x2 <= 3/2, e il")
    print("limite x <= 1 non taglia nessun punto di quel segmento.")

    # tutte le soluzioni ottime del rilassamento LP+ sono il segmento x1 + x2 = 3/2 in [0,1]^2
    for punto in [(0.75, 0.75), (1.0, 0.5), (0.5, 1.0)]:
        z, viol = valuta(m_lpp, {"x[0]": punto[0], "x[1]": punto[1]})
        assert viol <= 1e-9 and abs(z - 1.5) <= 1e-9
        print(f"  ({frazione(punto[0])}, {frazione(punto[1])}) e' ammissibile per LP+ e vale "
              f"{frazione(z)}: e' una delle infinite soluzioni ottime.")

    # ---------- 3. PERCHE' L'ARROTONDAMENTO FALLISCE ----------
    intestazione("3. Arrotondamento delle soluzioni frazionarie")
    m_mip, x_mip = modello_esempio(binarie=True)
    for base in [(0.75, 0.75), (1.0, 0.5)]:
        for verso, arr in [("piu' vicino", lambda v: round(v)), ("verso il basso", int)]:
            cand = {"x[0]": float(arr(base[0])), "x[1]": float(arr(base[1]))}
            z, viol = valuta(m_mip, cand)
            ok = ammissibile(m_mip, cand)
            print(f"  da ({frazione(base[0])}, {frazione(base[1])}) arrotondando {verso:14s} -> "
                  f"({frazione(cand['x[0]'])}, {frazione(cand['x[1]'])})  "
                  f"{'ammissibile, valore ' + frazione(z) if ok else f'NON ammissibile (violazione {viol:g})'}")
    assert not ammissibile(m_mip, {"x[0]": 1.0, "x[1]": 1.0})
    assert ammissibile(m_mip, {"x[0]": 1.0, "x[1]": 0.0})
    # il controllo di interezza serve davvero: (1, 1/2) soddisfa i vincoli lineari ma non e' intera
    assert valuta(m_mip, {"x[0]": 1.0, "x[1]": 0.5})[1] <= 1e-9
    assert viola_interezza(m_mip, {"x[0]": 1.0, "x[1]": 0.5}) == 0.5
    assert not ammissibile(m_mip, {"x[0]": 1.0, "x[1]": 0.5})
    print("  (1, 1/2) soddisfa i vincoli lineari ma viola l'interezza di 1/2:")
    print("  la sola ammissibilita' continua non certifica un bound primale intero.")

    # ---------- 4. L'OTTIMO INTERO ----------
    intestazione("4. L'ottimo intero")
    zmilp = risolvi(m_mip)
    print(f"z(MILP) = {frazione(zmilp)}   soluzione ottima:")
    stampa_soluzione(m_mip)
    print(f"Divario fra rilassamento e ottimo intero: {frazione(zlpp)} - {frazione(zmilp)} = "
          f"{frazione(zlpp - zmilp)}")
    salva_dati(pd.DataFrame([{"modello": "esempio 1.1", "z_lp": zlp, "z_lp_rafforzato": zlpp,
                              "z_milp": zmilp}]), "cap01_bound")


    # ---------- 5. IL BRANCH-AND-BOUND SVOLTO A MANO ----------
    intestazione("5. Branch-and-bound: la traccia riportata nel capitolo")


    def nodo(fissa: dict):
        """Rilassamento LP+ del sottoproblema con le variabili limitate da `fissa`.

        `fissa` e' {indice: (lb, ub)}: sono i rami x_j <= floor(v) e x_j >= ceil(v).
        """
        m, x = modello_esempio(binarie=False, superiore=True)
        for j, (lo, hi) in fissa.items():
            x[j].LB, x[j].UB = lo, hi
        m.optimize()
        if m.Status != GRB.OPTIMAL:
            return None, None
        return m.ObjVal, (x[0].X, x[1].X)


    passi = []
    for etichetta, fissa in [("radice", {}),
                             ("x1 <= 0", {0: (0.0, 0.0)}),
                             ("x1 >= 1", {0: (1.0, 1.0)}),
                             ("x1 >= 1, x2 <= 0", {0: (1.0, 1.0), 1: (0.0, 0.0)}),
                             ("x1 >= 1, x2 >= 1", {0: (1.0, 1.0), 1: (1.0, 1.0)})]:
        z, sol = nodo(fissa)
        if z is None:
            print(f"  {etichetta:20s} inammissibile: il ramo si scarta")
            passi.append({"nodo": etichetta, "z_lp": None, "x1": None, "x2": None, "intera": False})
            continue
        intera = all(abs(v - round(v)) <= 1e-9 for v in sol)
        print(f"  {etichetta:20s} z(LP+) = {frazione(z):>4}   x = ({frazione(sol[0])}, "
              f"{frazione(sol[1])}){'   soluzione intera: candidato incumbent' if intera else '   frazionaria: si ramifica'}")
        passi.append({"nodo": etichetta, "z_lp": z, "x1": sol[0], "x2": sol[1], "intera": intera})
    salva_dati(pd.DataFrame(passi), "cap01_branch")
    assert passi[0]["z_lp"] == 1.5 and passi[1]["z_lp"] == 1.0 and passi[2]["z_lp"] == 1.5
    assert passi[3]["z_lp"] == 1.0 and passi[4]["z_lp"] is None
    print("  L'incumbent finale vale 1: e' l'ottimo, e nessun sottoproblema resta aperto.")

    # ---------- 6. FIGURA: LA REGIONE AMMISSIBILE E I PUNTI INTERI ----------
    fig, ax = plt.subplots(figsize=(5.4, 5.0))
    # poligono ammissibile del rilassamento LP+: {0<=x<=1, 2x1+2x2<=3}
    poligono = [(0, 0), (1, 0), (1, 0.5), (0.5, 1), (0, 1)]
    ax.fill(*zip(*poligono), color=TEAL, alpha=0.16, zorder=1,
            label="rilassamento LP$^+$")
    ax.plot([0.25, 1.5], [1.25, 0.0], color=TEAL, lw=1.6, zorder=2,
            label="$2x_1 + 2x_2 = 3$")
    for (p, q) in [(0, 0), (1, 0), (0, 1)]:
        ax.plot(p, q, "o", color=VERDE, ms=11, zorder=4)
        ax.annotate(f"({p},{q})", (p, q), textcoords="offset points", xytext=(9, 9),
                    fontsize=9, color=VERDE)
    ax.plot(1, 1, "X", color=ROSSO, ms=12, zorder=4)
    ax.annotate("(1,1): $2+2 > 3$", (1, 1), textcoords="offset points", xytext=(-92, 10),
                fontsize=9, color=ROSSO)
    for (p, q), testo in [((0.75, 0.75), "$(3/4,3/4)$"), ((1.0, 0.5), "$(1,1/2)$")]:
        ax.plot(p, q, "s", color=BLU, ms=7, zorder=4)
        ax.annotate(testo, (p, q), textcoords="offset points", xytext=(8, -14), fontsize=9, color=BLU)
    ax.plot([], [], "o", color=VERDE, ms=9, label="punti interi ammissibili")
    ax.plot([], [], "X", color=ROSSO, ms=9, label="punto intero non ammissibile")
    ax.plot([], [], "s", color=BLU, ms=6, label="soluzioni ottime del rilassamento")
    ax.set_xlim(-0.15, 1.45)
    ax.set_ylim(-0.15, 1.45)
    ax.set_xlabel("$x_1$")
    ax.set_ylabel("$x_2$")
    ax.set_title("Rilassamento LP$^+$ e punti interi\n$z(\\mathrm{LP}^+) = 3/2$, $z(\\mathrm{MILP}) = 1$")
    ax.legend(loc="upper right", fontsize=8)
    ax.set_aspect("equal")
    salva_figura(fig, "cap01_rilassamento")
    print("Fine.")
    ```

<!-- script-incorporato: fine -->
