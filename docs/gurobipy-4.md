# 3.4 Tre modelli classici

[:material-file-pdf-box: Dispensa (PDF)](pdf/dispensa-1-modellazione.pdf) · [:material-presentation: Slide (PDF)](pdf/slide-03-gurobi.pdf)

**Classe:** implementazione · **Script:** `python/cap06_bpp.py`, `python/cap06_cmax.py`, `python/cap06_tsp.py`
{ .scheda }

Bin packing, makespan e commesso viaggiatore: enunciato, modello, costruzione in
`gurobipy` e modello dell'istanza. Sono i tre problemi su cui il
[capitolo delle euristiche](modellazione-4.md) costruisce next-fit, first-fit,
best-fit, LPT e vicino più vicino.

Fin qui il modello di esempio è sempre stato lo zaino. I tre problemi qui sotto
ritornano nel [capitolo delle euristiche](modellazione-4.md), dove si
costruiscono a mano le soluzioni di next-fit, first-fit, best-fit, LPT e vicino
più vicino: qui si scrivono i loro modelli, così quelle euristiche hanno un
ottimo con cui confrontarsi.

## Bin packing: quanti contenitori bastano

[![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/cap06_bpp.ipynb)

Lo script è `python/cap06_bpp.py`.

!!! abstract "Bin packing"
    Ci sono $n$ oggetti, l'oggetto $j$ pesa $w_j$. I contenitori sono tutti
    uguali, di capacità $c$. Si usi il minimo numero di contenitori.

### Il modello

Servono due famiglie di variabili binarie: $x_{jb} = 1$ se l'oggetto $j$ va nel
contenitore $b$, e $y_b = 1$ se il contenitore $b$ viene usato.

$$
\begin{aligned}
\min ~~ \sum_{b=1}^{k} y_b & &\\
\text{soggetto a} \quad \sum_{b=1}^{k} x_{jb} &= 1, & \forall j \in \{1, 2, \dots, n\},\\
\sum_{j=1}^{n} w_j\, x_{jb} - c\, y_b &\le 0, & \forall b \in \{1, 2, \dots, k\},\\
x_{jb} &\in \{0, 1\}, & \forall j \in \{1, 2, \dots, n\},\ \forall b \in \{1, 2, \dots, k\},\\
y_b &\in \{0, 1\}, & \forall b \in \{1, 2, \dots, k\}.
\end{aligned}
$$

La prima famiglia dice che ogni oggetto finisce in esattamente un contenitore.
La seconda è la capacità scritta come **attivazione**: finché $y_b = 0$ il
contenitore $b$ non può ricevere niente, e appena $y_b = 1$ accoglie fino a $c$.
L'obiettivo conta i contenitori accesi.

### La costruzione in gurobipy

```python
def modello_bpp(w, c, k):
    n = len(w)
    m = nuovo_modello("bin_packing")
    x = m.addVars(n, k, vtype=GRB.BINARY, name="x")
    y = m.addVars(k, vtype=GRB.BINARY, name="y")
    m.setObjective(y.sum(), GRB.MINIMIZE)
    m.addConstrs((x.sum(j, "*") == 1 for j in R(n)), name="oggetto")
    m.addConstrs((gp.quicksum(w[j] * x[j, b] for j in R(n)) <= c * y[b]
                  for b in R(k)), name="capacita")
    return m, x, y
```

### L'istanza

Sull'istanza di quattro oggetti di peso $w = (5, 4, 3, 3)$ e capacità $c = 7$:

<!-- modello-esteso: cap06_bpp -->

<div class="modello-esteso largo" markdown>

$$
\begin{array}{rrrrrrrrrrrrrrrr c l}
\min &  &  &  &  &  &  &  &  &  &  &  &  & y_1 & +y_2 & +y_3 &  & \\
\text{soggetto a} & x_{11} & +x_{12} & +x_{13} &  &  &  &  &  &  &  &  &  &  &  &  & = & 1\\
 &  &  &  & x_{21} & +x_{22} & +x_{23} &  &  &  &  &  &  &  &  &  & = & 1\\
 &  &  &  &  &  &  & x_{31} & +x_{32} & +x_{33} &  &  &  &  &  &  & = & 1\\
 &  &  &  &  &  &  &  &  &  & x_{41} & +x_{42} & +x_{43} &  &  &  & = & 1\\
 & 5x_{11} &  &  & +4x_{21} &  &  & +3x_{31} &  &  & +3x_{41} &  &  & -7y_1 &  &  & \le & 0\\
 &  & 5x_{12} &  &  & +4x_{22} &  &  & +3x_{32} &  &  & +3x_{42} &  &  & -7y_2 &  & \le & 0\\
 &  &  & 5x_{13} &  &  & +4x_{23} &  &  & +3x_{33} &  &  & +3x_{43} &  &  & -7y_3 & \le & 0\\
 & x_{11}, & x_{12}, & x_{13}, & x_{21}, & x_{22}, & x_{23}, & x_{31}, & x_{32}, & x_{33}, & x_{41}, & x_{42}, & x_{43} &  &  &  & \in & \{0, 1\}\\
 &  &  &  &  &  &  &  &  &  &  &  &  & y_1, & y_2, & y_3 & \in & \{0, 1\}
\end{array}
$$

</div>

<!-- modello-esteso: fine -->

Il peso totale è $15$, quindi nessuna soluzione può usare meno di
$\lceil 15/7 \rceil = 3$ contenitori; l'ottimo ne usa esattamente $3$, e il
conteggio è quindi stretto.

!!! warning "Il rilassamento del bin packing è debolissimo"
    Rilassando $y_b$ a $y_b \ge 0$ il modello compra frazioni di contenitore, e
    l'ottimo dell'LP scende a $\sum_j w_j / c = 15/7 \approx 2{,}14$: il rilassamento
    non sa che un contenitore si apre tutto intero. È il motivo per cui su questo
    problema il bound duale è poco utile e le euristiche contano di più.

## Makespan: il carico della macchina più carica

[![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/cap06_cmax.ipynb)

Lo script è `python/cap06_cmax.py`.

!!! abstract "Makespan su macchine identiche"
    Ci sono $n$ lavori, di durata $d_j$, e $k$ macchine identiche. Ogni lavoro va
    su una macchina sola e non si interrompe. Si minimizzi l'istante in cui
    l'ultima macchina finisce.

### Il modello

Con $x_{jm} = 1$ se il lavoro $j$ va sulla macchina $m$, e $z \ge 0$ il carico
della macchina più carica:

$$
\begin{aligned}
\min ~~ z & &\\
\text{soggetto a} \quad \sum_{m=1}^{k} x_{jm} &= 1, & \forall j \in \{1, 2, \dots, n\},\\
\sum_{j=1}^{n} d_j\, x_{jm} - z &\le 0, & \forall m \in \{1, 2, \dots, k\},\\
x_{jm} &\in \{0, 1\}, & \forall j \in \{1, 2, \dots, n\},\ \forall m \in \{1, 2, \dots, k\},\\
z &\ge 0. &
\end{aligned}
$$

L'obiettivo è la sola variabile $z$: nessun dato vi compare. Sono le $k$ righe di
carico a darle significato, dicendo che nessuna macchina lavora più a lungo di
$z$; il minimo la schiaccia allora sul carico della macchina più carica.
È la tecnica [min-max](legami-06.md).

### La costruzione in gurobipy

```python
def modello_cmax(d, k):
    n = len(d)
    m = nuovo_modello("makespan")
    x = m.addVars(n, k, vtype=GRB.BINARY, name="x")
    z = m.addVar(name="z")
    m.setObjective(z, GRB.MINIMIZE)
    m.addConstrs((x.sum(j, "*") == 1 for j in R(n)), name="lavoro")
    m.addConstrs((gp.quicksum(d[j] * x[j, mm] for j in R(n)) <= z
                  for mm in R(k)), name="carico")
    return m, x, z
```

### L'istanza

Sull'istanza di quattro lavori di durata $d = (3, 4, 5, 6)$ su $k = 2$
macchine --- la stessa su cui il capitolo delle euristiche fa correre LPT:

<!-- modello-esteso: cap06_cmax -->

<div class="modello-esteso largo" markdown>

$$
\begin{array}{rrrrrrrrrr c l}
\min &  &  &  &  &  &  &  &  & z &  & \\
\text{soggetto a} & x_{11} & +x_{12} &  &  &  &  &  &  &  & = & 1\\
 &  &  & x_{21} & +x_{22} &  &  &  &  &  & = & 1\\
 &  &  &  &  & x_{31} & +x_{32} &  &  &  & = & 1\\
 &  &  &  &  &  &  & x_{41} & +x_{42} &  & = & 1\\
 & 3x_{11} &  & +4x_{21} &  & +5x_{31} &  & +6x_{41} &  & -z & \le & 0\\
 &  & 3x_{12} &  & +4x_{22} &  & +5x_{32} &  & +6x_{42} & -z & \le & 0\\
 & x_{11}, & x_{12}, & x_{21}, & x_{22}, & x_{31}, & x_{32}, & x_{41}, & x_{42} &  & \in & \{0, 1\}\\
 &  &  &  &  &  &  &  &  & z & \ge & 0
\end{array}
$$

</div>

<!-- modello-esteso: fine -->

Il carico totale è $18$ e le macchine sono due: nessuna soluzione può scendere
sotto $18/2 = 9$, e l'ottimo vale esattamente $9$ — i lavori si dividono in
$6+3$ e $5+4$. Qui il conteggio chiude il problema da solo.

## Commesso viaggiatore: la formulazione MTZ

[![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/cap06_tsp.ipynb)

Lo script è `python/cap06_tsp.py`.

!!! abstract "Commesso viaggiatore"
    Ci sono $n$ città e una distanza $d_{ij}$ fra ogni coppia. Si trovi il giro
    di lunghezza minima che tocca ogni città esattamente una volta e torna al
    punto di partenza.

### Il modello

Con $x_{ij} = 1$ se il giro va da $i$ a $j$, le due famiglie «si esce una volta»
e «si entra una volta» non bastano: ammettono anche soluzioni fatte di
**sottocicli** separati. La formulazione di Miller–Tucker–Zemlin aggiunge una
variabile $u_i$ per ogni città diversa dalla prima, che ne registra la posizione
lungo il giro.

$$
\begin{aligned}
\min ~~ \sum_{i=1}^{n} \sum_{j \ne i} d_{ij}\, x_{ij} & &\\
\text{soggetto a} \quad \sum_{j \ne i} x_{ij} &= 1, & \forall i \in \{1, 2, \dots, n\},\\
\sum_{i \ne j} x_{ij} &= 1, & \forall j \in \{1, 2, \dots, n\},\\
u_i - u_j + n\, x_{ij} &\le n - 1, & \forall i, j \in \{2, 3, \dots, n\},\ i \ne j,\\
x_{ij} &\in \{0, 1\}, & \forall i, j \in \{1, 2, \dots, n\},\ i \ne j,\\
u_i &\in [1,\, n-1], & \forall i \in \{2, 3, \dots, n\}.
\end{aligned}
$$

Il terzo gruppo è il cuore della formulazione. Se $x_{ij} = 0$ la riga diventa
$u_i - u_j \le n - 1$, sempre vera perché le $u$ stanno fra $1$ e $n-1$: non
vieta niente. Se invece $x_{ij} = 1$ diventa $u_j \ge u_i + 1$, cioè «se vado da
$i$ a $j$, la posizione di $j$ è la successiva». Un sottociclo che non tocca la
città $1$ richiederebbe una catena di posizioni sempre crescenti che si richiude
su se stessa, e questo è impossibile; la città $1$ non ha la sua $u$ proprio
perché è il punto in cui il giro si chiude.

### La costruzione in gurobipy

```python
def modello_tsp(D):
    n = len(D)
    m = nuovo_modello("tsp")
    x = m.addVars(((i, j) for i in R(n) for j in R(n) if i != j),
                  vtype=GRB.BINARY, name="x")
    u = m.addVars(R(1, n), lb=1, ub=n - 1, name="u")
    m.setObjective(gp.quicksum(D[i][j] * x[i, j] for i, j in x), GRB.MINIMIZE)
    m.addConstrs((gp.quicksum(x[i, j] for j in R(n) if j != i) == 1
                  for i in R(n)), name="esce")
    m.addConstrs((gp.quicksum(x[i, j] for i in R(n) if i != j) == 1
                  for j in R(n)), name="entra")
    m.addConstrs((u[i] - u[j] + n * x[i, j] <= n - 1
                  for i in R(1, n) for j in R(1, n) if i != j), name="mtz")
    return m, x, u
```

### L'istanza

Sull'istanza di quattro città del
[capitolo delle euristiche](modellazione-4.md) il giro ottimo è
$1 \to 2 \to 4 \to 3 \to 1$ e misura $22$. Il modello dell'istanza ha quindici
colonne — dodici archi e tre posizioni — e quattordici righe:

<!-- modello-esteso: cap06_tsp -->

<div class="modello-esteso largo" markdown>

$$
\begin{array}{rrrrrrrrrrrrrrrr c l}
\min & 4x_{12} & +5x_{13} & +9x_{14} & +4x_{21} & +9x_{23} & +9x_{24} & +5x_{31} & +9x_{32} & +4x_{34} & +9x_{41} & +9x_{42} & +4x_{43} &  &  &  &  & \\
\text{soggetto a} & x_{12} & +x_{13} & +x_{14} &  &  &  &  &  &  &  &  &  &  &  &  & = & 1\\
 &  &  &  & x_{21} & +x_{23} & +x_{24} &  &  &  &  &  &  &  &  &  & = & 1\\
 &  &  &  &  &  &  & x_{31} & +x_{32} & +x_{34} &  &  &  &  &  &  & = & 1\\
 &  &  &  &  &  &  &  &  &  & x_{41} & +x_{42} & +x_{43} &  &  &  & = & 1\\
 &  &  &  & x_{21} &  &  & +x_{31} &  &  & +x_{41} &  &  &  &  &  & = & 1\\
 & x_{12} &  &  &  &  &  &  & +x_{32} &  &  & +x_{42} &  &  &  &  & = & 1\\
 &  & x_{13} &  &  & +x_{23} &  &  &  &  &  &  & +x_{43} &  &  &  & = & 1\\
 &  &  & x_{14} &  &  & +x_{24} &  &  & +x_{34} &  &  &  &  &  &  & = & 1\\
 &  &  &  &  & 4x_{23} &  &  &  &  &  &  &  & +u_2 & -u_3 &  & \le & 3\\
 &  &  &  &  &  & 4x_{24} &  &  &  &  &  &  & +u_2 &  & -u_4 & \le & 3\\
 &  &  &  &  &  &  &  & 4x_{32} &  &  &  &  & -u_2 & +u_3 &  & \le & 3\\
 &  &  &  &  &  &  &  &  & 4x_{34} &  &  &  &  & +u_3 & -u_4 & \le & 3\\
 &  &  &  &  &  &  &  &  &  &  & 4x_{42} &  & -u_2 &  & +u_4 & \le & 3\\
 &  &  &  &  &  &  &  &  &  &  &  & 4x_{43} &  & -u_3 & +u_4 & \le & 3\\
 & x_{12}, & x_{13}, & x_{14}, & x_{21}, & x_{23}, & x_{24}, & x_{31}, & x_{32}, & x_{34}, & x_{41}, & x_{42}, & x_{43} &  &  &  & \in & \{0, 1\}\\
 &  &  &  &  &  &  &  &  &  &  &  &  & u_2, & u_3, & u_4 & \ge & 1
\end{array}
$$

</div>

<!-- modello-esteso: fine -->

!!! warning "MTZ è comoda, non è la più forte"
    I vincoli MTZ sono $O(n^2)$ e si scrivono in tre righe di `gurobipy`, ma il
    loro rilassamento lineare è debole: le $u$ continue assorbono quasi tutto e
    l'LP si avvicina poco all'ottimo intero. Le formulazioni che eliminano i
    sottocicli con i tagli di connessione danno bound molto migliori, al prezzo
    di un numero esponenziale di vincoli da generare a mano a mano. Per le
    dimensioni di questo corso MTZ basta.

<!-- script-incorporato: inizio (rigenerato da python/incorpora_codice.py) -->

??? example "Mostra lo script completo — `python/cap06_bpp.py` (51 righe)"

    ```python
    """Bin packing: quanti contenitori bastano (capitolo 3).

    Il primo dei tre problemi che il capitolo delle euristiche riprende: li' si
    costruiscono a mano next-fit, first-fit e best-fit, qui si scrive il modello che
    dice qual e' l'ottimo. La capacita' e' scritta come attivazione: finche' il
    contenitore non si apre non puo' ricevere niente.
    """
    import gurobipy as gp
    import pandas as pd
    from gurobipy import GRB

    from esteso import salva_modello
    from mip import frazione, nuovo_modello, risolvi
    from stile import intestazione, salva_dati

    R = range

    intestazione("Bin packing: il minimo numero di contenitori")
    w_bpp = [5, 4, 3, 3]             # peso degli oggetti
    c_bpp = 7                        # capacita' di un contenitore
    n_bpp = len(w_bpp)


    def modello_bpp(w, c, k):
        n = len(w)
        m = nuovo_modello("bin_packing")
        x = m.addVars(n, k, vtype=GRB.BINARY, name="x")
        y = m.addVars(k, vtype=GRB.BINARY, name="y")
        m.setObjective(y.sum(), GRB.MINIMIZE)
        m.addConstrs((x.sum(j, "*") == 1 for j in R(n)), name="oggetto")
        m.addConstrs((gp.quicksum(w[j] * x[j, b] for j in R(n)) <= c * y[b] for b in R(k)),
                     name="capacita")
        return m, x, y


    # con un contenitore per oggetto si trova quanti ne servono davvero; il modello
    # che si stampa usa poi solo quelli, perche' gli altri resterebbero vuoti
    m_largo, _, _ = modello_bpp(w_bpp, c_bpp, n_bpp)
    z_bpp = risolvi(m_largo)
    minimo_teorico = -(-sum(w_bpp) // c_bpp)        # arrotondamento all'insu'
    print(f"  Pesi {w_bpp}, capacita' {c_bpp}.")
    print(f"  Il peso totale e' {sum(w_bpp)}: nessuna soluzione usa meno di "
          f"{sum(w_bpp)}/{c_bpp} = {minimo_teorico} contenitori, e l'ottimo ne usa {int(z_bpp)}.")
    assert z_bpp == minimo_teorico
    m_bpp, x_bpp, y_bpp = modello_bpp(w_bpp, c_bpp, int(z_bpp))
    risolvi(m_bpp)
    salva_modello(m_bpp, "cap06_bpp")
    print("  Il rilassamento compra frazioni di contenitore e scende a "
          f"{frazione(sum(w_bpp) / c_bpp)}: non sa che un contenitore si apre tutto intero.")
    salva_dati(pd.DataFrame([{"problema": "bin packing", "z_milp": z_bpp}]), "cap06_bpp")
    print("Fine.")
    ```

??? example "Mostra lo script completo — `python/cap06_cmax.py` (47 righe)"

    ```python
    """Makespan su macchine identiche (capitolo 3).

    Il secondo dei tre problemi che il capitolo delle euristiche riprende: li' si
    confronta l'ordine naturale con LPT sugli stessi quattro lavori. L'obiettivo e'
    una sola variabile, z, e sono i vincoli di carico a darle significato: e' la
    tecnica min-max.
    """
    import gurobipy as gp
    import pandas as pd
    from gurobipy import GRB

    from esteso import salva_modello
    from mip import frazione, nuovo_modello, risolvi
    from stile import intestazione, salva_dati

    R = range

    intestazione("Makespan: il carico della macchina piu' carica")
    d_cmax = [3, 4, 5, 6]            # durate dei lavori
    k_cmax = 2                       # macchine identiche


    def modello_cmax(d, k):
        n = len(d)
        m = nuovo_modello("makespan")
        x = m.addVars(n, k, vtype=GRB.BINARY, name="x")
        z = m.addVar(name="z")
        m.setObjective(z, GRB.MINIMIZE)
        m.addConstrs((x.sum(j, "*") == 1 for j in R(n)), name="lavoro")
        m.addConstrs((gp.quicksum(d[j] * x[j, mm] for j in R(n)) <= z for mm in R(k)),
                     name="carico")
        return m, x, z


    m_cmax, x_cmax, z_var = modello_cmax(d_cmax, k_cmax)
    z_cmax = risolvi(m_cmax)
    salva_modello(m_cmax, "cap06_cmax")
    print(f"  Durate {d_cmax} su {k_cmax} macchine identiche.")
    print(f"  Il carico totale e' {sum(d_cmax)}: diviso per {k_cmax} da' "
          f"{frazione(sum(d_cmax) / k_cmax)}, e l'ottimo vale {frazione(z_cmax)}.")
    for mm in R(k_cmax):
        lavori = [j + 1 for j in R(len(d_cmax)) if x_cmax[j, mm].X > 0.5]
        print(f"    macchina {mm + 1}: lavori {lavori}, carico "
              f"{sum(d_cmax[j - 1] for j in lavori)}")
    assert z_cmax == sum(d_cmax) / k_cmax
    salva_dati(pd.DataFrame([{"problema": "makespan", "z_milp": z_cmax}]), "cap06_cmax")
    print("Fine.")
    ```

??? example "Mostra lo script completo — `python/cap06_tsp.py` (54 righe)"

    ```python
    """Commesso viaggiatore con la formulazione MTZ (capitolo 3).

    Il terzo dei tre problemi che il capitolo delle euristiche riprende: li' si
    costruisce il tour con il vicino piu' vicino, qui si trova l'ottimo.

    Le variabili u ordinano le citta' lungo il giro: il vincolo
    u_i - u_j + n x_ij <= n - 1 e' vero se x_ij = 0 e obbliga u_j >= u_i + 1 se
    x_ij = 1. I sottocicli che non toccano la citta' 1 sono cosi' esclusi, perche'
    richiederebbero una catena di u sempre crescenti che si richiude su se stessa.
    """
    import gurobipy as gp
    import pandas as pd
    from gurobipy import GRB

    from esteso import salva_modello
    from mip import frazione, nuovo_modello, risolvi
    from stile import intestazione, salva_dati

    R = range

    intestazione("Commesso viaggiatore: il giro piu' corto")
    D_tsp = [[0, 4, 5, 9],
             [4, 0, 9, 9],
             [5, 9, 0, 4],
             [9, 9, 4, 0]]
    n_tsp = len(D_tsp)


    def modello_tsp(D):
        n = len(D)
        m = nuovo_modello("tsp")
        x = m.addVars(((i, j) for i in R(n) for j in R(n) if i != j), vtype=GRB.BINARY, name="x")
        u = m.addVars(R(1, n), lb=1, ub=n - 1, name="u")
        m.setObjective(gp.quicksum(D[i][j] * x[i, j] for i, j in x), GRB.MINIMIZE)
        m.addConstrs((gp.quicksum(x[i, j] for j in R(n) if j != i) == 1 for i in R(n)), name="esce")
        m.addConstrs((gp.quicksum(x[i, j] for i in R(n) if i != j) == 1 for j in R(n)), name="entra")
        m.addConstrs((u[i] - u[j] + n * x[i, j] <= n - 1
                      for i in R(1, n) for j in R(1, n) if i != j), name="mtz")
        return m, x, u


    m_tsp, x_tsp, u_tsp = modello_tsp(D_tsp)
    salva_modello(m_tsp, "cap06_tsp")
    z_tsp = risolvi(m_tsp)
    seguente = {i: j for (i, j) in x_tsp if x_tsp[i, j].X > 0.5}
    giro, citta = [0], 0
    while seguente[citta] != 0:
        citta = seguente[citta]
        giro.append(citta)
    print(f"  {n_tsp} citta', distanze simmetriche e metriche.")
    print("  Giro ottimo: " + " -> ".join(str(c + 1) for c in giro + [0])
          + f", lunghezza {frazione(z_tsp)}.")
    salva_dati(pd.DataFrame([{"problema": "TSP", "z_milp": z_tsp}]), "cap06_tsp")
    print("Fine.")
    ```

<!-- script-incorporato: fine -->
