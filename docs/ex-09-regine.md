# EX 9 — Le regine sulla scacchiera

**Classe:** BIP · **Legami:** set packing, [alldiff](legami-12.md) · **Script:** `python/ex09_regine.py`<br><br>
**Difficoltà:** ★★☆☆☆ · **Tempo:** 30–45 min
{ .scheda }

[![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/ex09_regine.ipynb)

Uno dei [quindici modelli numerici](numerici.md): quello in cui il bound duale si
scrive in una riga sola, e vale esattamente quanto l'ottimo.

!!! abstract "EX 9"
    Su una scacchiera $4 \times 4$ si vuole collocare il **massimo numero di
    regine** in modo che nessuna possa catturarne un'altra in una sola mossa.
    Negli scacchi la regina si muove di un numero qualsiasi di caselle lungo la
    stessa riga, la stessa colonna o una delle due diagonali.

## Modello

Con $x_{ij} = 1$ se sulla casella $(i,j)$ c'è una regina: sedici variabili
binarie, una per casella.

Il modello dell'istanza, per esteso:

<!-- modello-esteso: ex09_primale -->

<div class="modello-esteso largo" markdown>

$$
\begin{array}{rrrrrrrrrrrrrrrrr c l}
\max & x_{11} & +x_{12} & +x_{13} & +x_{14} & +x_{21} & +x_{22} & +x_{23} & +x_{24} & +x_{31} & +x_{32} & +x_{33} & +x_{34} & +x_{41} & +x_{42} & +x_{43} & +x_{44} &  & \\
\text{soggetto a} & x_{11} & +x_{12} & +x_{13} & +x_{14} &  &  &  &  &  &  &  &  &  &  &  &  & \le & 1\\
 &  &  &  &  & x_{21} & +x_{22} & +x_{23} & +x_{24} &  &  &  &  &  &  &  &  & \le & 1\\
 &  &  &  &  &  &  &  &  & x_{31} & +x_{32} & +x_{33} & +x_{34} &  &  &  &  & \le & 1\\
 &  &  &  &  &  &  &  &  &  &  &  &  & x_{41} & +x_{42} & +x_{43} & +x_{44} & \le & 1\\
 & x_{11} &  &  &  & +x_{21} &  &  &  & +x_{31} &  &  &  & +x_{41} &  &  &  & \le & 1\\
 &  & x_{12} &  &  &  & +x_{22} &  &  &  & +x_{32} &  &  &  & +x_{42} &  &  & \le & 1\\
 &  &  & x_{13} &  &  &  & +x_{23} &  &  &  & +x_{33} &  &  &  & +x_{43} &  & \le & 1\\
 &  &  &  & x_{14} &  &  &  & +x_{24} &  &  &  & +x_{34} &  &  &  & +x_{44} & \le & 1\\
 &  &  & x_{13} &  &  &  &  & +x_{24} &  &  &  &  &  &  &  &  & \le & 1\\
 &  & x_{12} &  &  &  &  & +x_{23} &  &  &  &  & +x_{34} &  &  &  &  & \le & 1\\
 & x_{11} &  &  &  &  & +x_{22} &  &  &  &  & +x_{33} &  &  &  &  & +x_{44} & \le & 1\\
 &  &  &  &  & x_{21} &  &  &  &  & +x_{32} &  &  &  &  & +x_{43} &  & \le & 1\\
 &  &  &  &  &  &  &  &  & x_{31} &  &  &  &  & +x_{42} &  &  & \le & 1\\
 &  & x_{12} &  &  & +x_{21} &  &  &  &  &  &  &  &  &  &  &  & \le & 1\\
 &  &  & x_{13} &  &  & +x_{22} &  &  & +x_{31} &  &  &  &  &  &  &  & \le & 1\\
 &  &  &  & x_{14} &  &  & +x_{23} &  &  & +x_{32} &  &  & +x_{41} &  &  &  & \le & 1\\
 &  &  &  &  &  &  &  & x_{24} &  &  & +x_{33} &  &  & +x_{42} &  &  & \le & 1\\
 &  &  &  &  &  &  &  &  &  &  &  & x_{34} &  &  & +x_{43} &  & \le & 1\\
 & x_{11}, & x_{12}, & x_{13}, & x_{14}, & x_{21}, & x_{22}, & x_{23}, & x_{24}, & x_{31}, & x_{32}, & x_{33}, & x_{34}, & x_{41}, & x_{42}, & x_{43}, & x_{44} & \in & \{0, 1\}
\end{array}
$$

</div>

<!-- modello-esteso: fine -->

È un **set packing** su quattro famiglie di rette — le $4$ righe, le $4$ colonne
e le diagonali nei due versi — in tutto $18$ vincoli. Il trucco di indicizzazione
è tutto qui: le diagonali «discendenti» sono gli insiemi a $i - j$ costante,
quelle «ascendenti» gli insiemi a $i + j$ costante.

!!! tip "Le diagonali di una casella sola non diventano vincoli"
    I quattro angoli stanno ciascuno su una diagonale che non tocca nient'altro.
    Scriverne il vincolo darebbe $x_{ij} \le 1$ su una variabile già binaria: una
    riga che non vieta niente. Restano $5 + 5$ diagonali con almeno due caselle,
    e il modello perde dieci righe senza perdere una soluzione.

## Euristica costruttiva: il bound primale

È un **massimo**. Euristica riga per riga: nella riga $i$ si sceglie la prima
colonna libera che non sia attaccata dalle regine già piazzate; se non ce n'è, la
riga resta vuota. Non si torna mai indietro.

Sull'istanza l'euristica piazza le regine in $(1,1)$ e $(2,3)$; per la riga $3$
non resta nessuna casella libera e la riga salta; nella riga $4$ prende $(4,2)$.

$$\mathit{LB} = 3.$$

## Rilassamento LP e duale: il bound duale

Il duale è un **set covering**: una variabile per ogni retta, e ogni casella va
coperta da almeno una delle quattro rette che la attraversano.

<!-- modello-esteso: ex09_duale -->

<div class="modello-esteso largo" markdown>

$$
\begin{array}{rrrrrrrrrrrrrrrrrrr c l}
\min & \alpha_1 & +\alpha_2 & +\alpha_3 & +\alpha_4 & +\beta_1 & +\beta_2 & +\beta_3 & +\beta_4 & +\gamma_{-1} & +\gamma_0 & +\gamma_1 & +\gamma_2 & +\gamma_3 & +\delta_2 & +\delta_3 & +\delta_4 & +\delta_5 & +\delta_6 &  & \\
\text{soggetto a} & \alpha_1 &  &  &  & +\beta_1 &  &  &  &  &  & +\gamma_1 &  &  &  &  &  &  &  & \ge & 1\\
 & \alpha_1 &  &  &  &  & +\beta_2 &  &  &  & +\gamma_0 &  &  &  & +\delta_2 &  &  &  &  & \ge & 1\\
 & \alpha_1 &  &  &  &  &  & +\beta_3 &  & +\gamma_{-1} &  &  &  &  &  & +\delta_3 &  &  &  & \ge & 1\\
 & \alpha_1 &  &  &  &  &  &  & +\beta_4 &  &  &  &  &  &  &  & +\delta_4 &  &  & \ge & 1\\
 &  & \alpha_2 &  &  & +\beta_1 &  &  &  &  &  &  & +\gamma_2 &  & +\delta_2 &  &  &  &  & \ge & 1\\
 &  & \alpha_2 &  &  &  & +\beta_2 &  &  &  &  & +\gamma_1 &  &  &  & +\delta_3 &  &  &  & \ge & 1\\
 &  & \alpha_2 &  &  &  &  & +\beta_3 &  &  & +\gamma_0 &  &  &  &  &  & +\delta_4 &  &  & \ge & 1\\
 &  & \alpha_2 &  &  &  &  &  & +\beta_4 & +\gamma_{-1} &  &  &  &  &  &  &  & +\delta_5 &  & \ge & 1\\
 &  &  & \alpha_3 &  & +\beta_1 &  &  &  &  &  &  &  & +\gamma_3 &  & +\delta_3 &  &  &  & \ge & 1\\
 &  &  & \alpha_3 &  &  & +\beta_2 &  &  &  &  &  & +\gamma_2 &  &  &  & +\delta_4 &  &  & \ge & 1\\
 &  &  & \alpha_3 &  &  &  & +\beta_3 &  &  &  & +\gamma_1 &  &  &  &  &  & +\delta_5 &  & \ge & 1\\
 &  &  & \alpha_3 &  &  &  &  & +\beta_4 &  & +\gamma_0 &  &  &  &  &  &  &  & +\delta_6 & \ge & 1\\
 &  &  &  & \alpha_4 & +\beta_1 &  &  &  &  &  &  &  &  &  &  & +\delta_4 &  &  & \ge & 1\\
 &  &  &  & \alpha_4 &  & +\beta_2 &  &  &  &  &  &  & +\gamma_3 &  &  &  & +\delta_5 &  & \ge & 1\\
 &  &  &  & \alpha_4 &  &  & +\beta_3 &  &  &  &  & +\gamma_2 &  &  &  &  &  & +\delta_6 & \ge & 1\\
 &  &  &  & \alpha_4 &  &  &  & +\beta_4 &  &  & +\gamma_1 &  &  &  &  &  &  &  & \ge & 1\\
 & \alpha_1, & \alpha_2, & \alpha_3, & \alpha_4 &  &  &  &  &  &  &  &  &  &  &  &  &  &  & \ge & 0\\
 &  &  &  &  & \beta_1, & \beta_2, & \beta_3, & \beta_4 &  &  &  &  &  &  &  &  &  &  & \ge & 0\\
 &  &  &  &  &  &  &  &  & \gamma_{-1}, & \gamma_0, & \gamma_1, & \gamma_2, & \gamma_3 &  &  &  &  &  & \ge & 0\\
 &  &  &  &  &  &  &  &  &  &  &  &  &  & \delta_2, & \delta_3, & \delta_4, & \delta_5, & \delta_6 & \ge & 0
\end{array}
$$

</div>

<!-- modello-esteso: fine -->

**La ricetta:** si usa una famiglia sola. Con $\bar\alpha_i = 1$ per ogni riga e
tutto il resto a zero, ogni casella $(i,j)$ ha $\alpha_i = 1 \ge 1$: la soluzione
è ammissibile e vale $n$. È la traduzione duale della frase «in ogni riga sta al
più una regina».

$$\mathit{UB} = 4.$$

## Ottimo e confronto

| $\mathit{LB}$ | $\mathit{UB}$ | $z(\mathit{LP})$ | $z(\mathit{LP}^+)$ | $z(\mathit{MILP})$ |
|---:|---:|---:|---:|---:|
| 3 | 4 | 4 | 4 | 4 |

Il bound duale è raggiunto: la soluzione trovata è ottima, e lo si sa **senza
fidarsi del solver**. L'euristica invece si ferma a $3$: è l'euristica, non il
bound, a lasciare il divario del $25\%$.

!!! tip "Due varianti"
    Su scacchiere $n \times n$ con $n = 5$ e $n = 6$ l'ottimo vale sempre $n$, e
    il certificato $\bar\alpha_i = 1$ lo dimostra. Per $n = 2$ e $n = 3$ invece
    l'ottimo vale $1$ e $2$: il bound $n$ resta valido ma non è raggiungibile, ed
    è il primo caso in cui questa ricetta duale non chiude il problema. La
    scacchiera $4 \times 4$ dell'esercizio è la più piccola su cui le $n$ regine
    ci stanno davvero, e quindi la più piccola su cui il certificato chiude.

    Togliendo i vincoli sulle diagonali si ottengono le **torri** invece delle
    regine: il modello diventa un assegnamento, la matrice è totalmente
    unimodulare e il rilassamento LP dà già un valore intero.

![La scacchiera ottima](img/ex09_scacchiera.png)

## Codice

Lo script completo è
[`python/ex09_regine.py`](https://github.com/fabiofurini/modellazione-mip/blob/main/python/ex09_regine.py);
il notebook è
[`notebooks/ex09_regine.ipynb`](https://github.com/fabiofurini/modellazione-mip/blob/main/notebooks/ex09_regine.ipynb).

<!-- script-incorporato: inizio (rigenerato da python/incorpora_codice.py) -->

??? example "Mostra lo script completo — `python/ex09_regine.py` (183 righe)"

    ```python
    """EX 9 -- Regine sulla scacchiera (famiglia 11).

    Set packing su quattro famiglie di rette: righe, colonne e le due diagonali. Il
    duale del rilassamento si costruisce a mano in una riga sola (si paga 1 ogni
    riga) e vale esattamente quanto l'ottimo: e' un caso in cui il certificato chiude
    il problema. L'euristica costruttiva invece si blocca sotto le n regine.

    L'istanza e' 4x4, la piu' piccola su cui si collocano n regine: sedici binarie e
    diciotto vincoli, cosi' il modello si scrive per esteso come tutti gli altri del
    capitolo. Il caso classico 8x8 resta fra le varianti.

    Le diagonali di una sola casella non diventano vincoli: `x <= 1` su una binaria
    e' gia' vero per definizione, e scriverlo riempirebbe il modello di righe vuote.
    """
    import gurobipy as gp
    import pandas as pd
    from gurobipy import GRB

    from mip import (ammissibile, due_rilassamenti, frazione, nuovo_modello, registra_bound,
                     risolvi, valuta)
    from stile import ARANCIO, BLU, GRIGIO, TEAL, intestazione, plt, salva_dati, salva_figura
    from esteso import salva_modello

    R = range

    # ---------- 1. MODELLO E ISTANZA ----------
    intestazione("EX 9. Regine: il massimo numero di regine che non si attaccano")
    N = 4


    def diagonali(n):
        """Le diagonali con almeno due caselle, nei due versi.

        Su `i - j = k` le caselle sono `n - |k|`, su `i + j = k` sono
        `min(k, 2n-2-k) + 1`: quelle con una sola casella si scartano.
        """
        prima = [k for k in R(-(n - 1), n) if n - abs(k) >= 2]
        seconda = [k for k in R(0, 2 * n - 1) if min(k, 2 * n - 2 - k) + 1 >= 2]
        return prima, seconda


    def modello(n):
        m = nuovo_modello("regine")
        x = m.addVars(n, n, vtype=GRB.BINARY, name="x")
        m.setObjective(x.sum(), GRB.MAXIMIZE)
        m.addConstrs((x.sum(i, "*") <= 1 for i in R(n)), name="riga")
        m.addConstrs((x.sum("*", j) <= 1 for j in R(n)), name="colonna")
        prima, seconda = diagonali(n)
        m.addConstrs((gp.quicksum(x[i, j] for i in R(n) for j in R(n) if i - j == k) <= 1
                      for k in prima), name="diag1")
        m.addConstrs((gp.quicksum(x[i, j] for i in R(n) for j in R(n) if i + j == k) <= 1
                      for k in seconda), name="diag2")
        return m, x


    def duale(n):
        """min sum_i alpha_i + sum_j beta_j + sum_k gamma_k + sum_k delta_k
           s.t. alpha_i + beta_j + gamma_{i-j} + delta_{i+j} >= 1 per ogni casella."""
        d = nuovo_modello("duale_regine")
        prima, seconda = diagonali(n)
        alpha = d.addVars(n, name="alpha")
        beta = d.addVars(n, name="beta")
        gamma = d.addVars(prima, name="gamma")
        delta = d.addVars(seconda, name="delta")
        d.setObjective(alpha.sum() + beta.sum() + gamma.sum() + delta.sum(), GRB.MINIMIZE)
        d.addConstrs((alpha[i] + beta[j]
                      + (gamma[i - j] if i - j in prima else 0)
                      + (delta[i + j] if i + j in seconda else 0) >= 1
                      for i in R(n) for j in R(n)), name="rc")
        return d


    m8, x8 = modello(N)
    salva_modello(m8, "ex09_primale")
    _p, _s = diagonali(N)
    print(f"  Scacchiera {N}x{N}: {N * N} variabili binarie e {2 * N + len(_p) + len(_s)} vincoli")
    print(f"  ({N} righe, {N} colonne e {len(_p)} + {len(_s)} diagonali con almeno due caselle).")

    # ---------- 2. EURISTICA COSTRUTTIVA (LOWER BOUND) ----------
    # euristica costruttiva riga per riga: la prima colonna libera che non e' attaccata dalle regine
    # gia' piazzate. Non torna mai indietro: se una riga non ha caselle libere, la salta.
    def euristica(n):
        pos = []
        passi = []
        for i in R(n):
            scelta = None
            for j in R(n):
                if all(j != jj and abs(i - ii) != abs(j - jj) for ii, jj in pos):
                    scelta = j
                    break
            if scelta is None:
                passi.append(f"riga {i + 1}: nessuna casella libera, la riga resta vuota")
            else:
                pos.append((i, scelta))
                passi.append(f"riga {i + 1}: prima casella libera in colonna {scelta + 1}")
        return pos, passi


    pos, passi = euristica(N)
    for k, riga in enumerate(passi, 1):
        print(f"  Passo {k}. {riga}")
    lb8 = len(pos)
    sol_eur = {f"x[{i},{j}]": 1 for i, j in pos}
    assert ammissibile(m8, sol_eur), sol_eur
    print(f"  Regine piazzate dall'euristica costruttiva: {lb8}  ->  lb = {frazione(lb8)}")

    # ---------- 3. RILASSAMENTO LP E DUALE (UPPER BOUND) ----------
    d8 = duale(N)
    salva_modello(d8, "ex09_duale")
    mano = {f"alpha[{i}]": 1.0 for i in R(N)}       # beta = gamma = delta = 0
    ub8, viol = valuta(d8, mano)
    assert viol <= 1e-9, viol
    print(f"  Duale a mano: alpha_i = 1 su ogni riga, tutto il resto zero. Ogni casella (i, j) ha")
    print(f"  alpha_i = 1 >= 1: la soluzione e' ammissibile e vale {frazione(ub8)}.")
    print("  E' la traduzione duale della frase «in ogni riga sta al piu' una regina».")
    zlp8, zlp8r, _ = due_rilassamenti(m8, d8)

    # ---------- 4. OTTIMO DEL MILP ----------
    z8 = risolvi(m8)
    ott = [(i, j) for i in R(N) for j in R(N) if x8[i, j].X > 0.5]
    print("  Soluzione ottima (una regina per riga): "
          + ", ".join(f"riga {i + 1} colonna {j + 1}" for i, j in sorted(ott)))
    riga = registra_bound("EX 9 regine", ub8, lb8, zlp8, zlp8r, z8, senso="max")
    salva_dati(pd.DataFrame([riga]), "ex09_bound")
    salva_dati(pd.DataFrame([{"riga": i + 1, "colonna": j + 1} for i, j in sorted(ott)]),
               "ex09_ottimo")
    assert lb8 <= z8 <= zlp8 <= ub8 + 1e-9
    print(f"  Il bound duale {frazione(ub8)} e' raggiunto: la soluzione trovata e' ottima, e lo")
    print("  sappiamo senza fidarci del solver. L'euristica costruttiva invece si ferma prima: e' l'euristica,")
    print("  non il bound, a lasciare il divario.")

    # ---------- 5. DUE VARIANTI ----------
    intestazione("EX 9. Varianti")
    varianti = {}
    # 8a: scacchiere piu' piccole; per n = 2 e n = 3 non si arriva a n regine
    for n in (5, 6):
        m, x = modello(n)
        z = risolvi(m)
        varianti[f"n = {n}"] = z
        print(f"  Scacchiera {n}x{n}: z = {frazione(z)} (= n)")
        assert abs(z - n) <= 1e-9
    for n in (2, 3):
        m, x = modello(n)
        z = risolvi(m)
        varianti[f"n = {n}"] = z
        print(f"  Scacchiera {n}x{n}: z = {frazione(z)} < {n}: il bound duale n non e' raggiungibile")
        assert z < n - 0.5
    salva_dati(pd.DataFrame({"scacchiera": list(varianti), "z": list(varianti.values())}),
               "ex09_varianti")
    # 8b: le diagonali non contano (torri invece di regine)
    m, x = modello(N)
    m.update()
    for c in [c for c in m.getConstrs() if c.ConstrName.startswith("diag")]:
        m.remove(c)
    m.update()
    z_torri = risolvi(m)
    print(f"  Senza i vincoli sulle diagonali (torri invece di regine): z = {frazione(z_torri)},")
    print("  e il modello diventa un assegnamento: la matrice e' totalmente unimodulare e il")
    print("  rilassamento lineare da' gia' un valore intero.")

    # ---------- 6. FIGURA ----------
    fig, ax = plt.subplots(figsize=(4.4, 4.4))
    for i in R(N):
        for j in R(N):
            ax.add_patch(plt.Rectangle((j, N - 1 - i), 1, 1,
                                       color="#EFEFEF" if (i + j) % 2 else "#CFD8DC"))
    for i, j in pos:
        ax.plot(j + 0.5, N - 1 - i + 0.5, marker="s", color=ARANCIO, ms=13)
    for i, j in ott:
        ax.plot(j + 0.5, N - 1 - i + 0.5, marker="*", color=TEAL, ms=17)
    ax.plot([], [], marker="s", ls="", color=ARANCIO, label=f"euristica costruttiva ({lb8})")
    ax.plot([], [], marker="*", ls="", color=TEAL, label=f"ottimo ({int(z8)})")
    ax.set_xlim(0, N)
    ax.set_ylim(0, N)
    ax.set_xticks([j + 0.5 for j in R(N)])
    ax.set_xticklabels([str(j + 1) for j in R(N)])
    ax.set_yticks([i + 0.5 for i in R(N)])
    ax.set_yticklabels([str(N - i) for i in R(N)])
    ax.set_aspect("equal")
    ax.set_title("EX 9: euristica costruttiva contro ottimo")
    ax.legend(fontsize=8, loc="upper center", bbox_to_anchor=(0.5, -0.06), ncol=2)
    salva_figura(fig, "ex09_scacchiera")
    print("Fine.")
    ```

<!-- script-incorporato: fine -->
