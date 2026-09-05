# p-mediana: al più $k$ sedi

**Classe:** BIP · **Legami:** attivazione disaggregata · **Script:** `python/fam08_2_pmediana.py`

[![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/fam08_2_pmediana.ipynb)

!!! abstract "Problema 8.2"
    Un'azienda deve scegliere al più $k \in \mathbb{Z}_{\ge 1}$ sedi, fra
    $m \in \mathbb{Z}_{\ge 1}$ candidate, e assegnare ciascuno degli
    $n \in \mathbb{Z}_{\ge 1}$ clienti alla sede aperta più conveniente. Per
    ogni sede $l$ e cliente $c$, $d_{lc} \in \mathbb{Q}_{>0}$ è la distanza.
    Si vuole minimizzare la somma delle distanze cliente-sede.

**Il problema a parole.** *Decidiamo* quali sedi aprire (al più $k$) e a
quale sede assegnare ciascun cliente. *L'obiettivo*: somma delle distanze
minima. *I vincoli*: ogni cliente a esattamente una sede aperta; al più $k$
sedi aperte. Il classico problema della **p-mediana**.

## Modello

**Dati.**

| Simbolo | Tipo | Significato |
|---|---|---|
| $m$ | $\in \mathbb{Z}_{\ge 1}$ | numero di sedi, $l \in \{1, 2, \dots, m\}$ |
| $n$ | $\in \mathbb{Z}_{\ge 1}$ | numero di clienti, $c \in \{1, 2, \dots, n\}$ |
| $d_{lc}$ | $\in \mathbb{Q}_{>0}$ | distanza fra la sede $l$ e il cliente $c$ |
| $k$ | $\in \mathbb{Z}_{\ge 1}$ | numero massimo di sedi aperte |

**Variabili decisionali.** $m$ binarie $x_l$ (sede aperta) e $m\,n$ binarie
$y_{lc}$ (cliente $c$ servito da $l$).

$$
\begin{aligned}
\min ~~ \sum_{l=1}^{m}\sum_{c=1}^{n} d_{lc}\, y_{lc} & & \\
\text{soggetto a} \quad \sum_{l=1}^{m} y_{lc} &= 1, & \forall c, \\
\sum_{l=1}^{m} x_l &\le k, & \\
x_l - y_{lc} &\ge 0, & \forall l, c, \\
x_l, y_{lc} &\in \{0, 1\}. & &
\end{aligned}
$$

- l'obiettivo minimizza la somma delle distanze cliente-sede;
- il primo vincolo assegna ogni cliente a una sede ($n$ vincoli);
- il secondo limita a $k$ le sedi aperte (un vincolo);
- il terzo lega assegnamento e apertura, in forma **disaggregata**
  ($m\,n$ vincoli).

**Il legame.** Se $y_{lc}=1$ allora $x_l=1$: dalla CNF di
$y_{lc} \Rightarrow x_l$, cioè $\neg y_{lc} \lor x_l$, si ottiene
$x_l \ge y_{lc}$, imposto direttamente. A differenza del problema 8.1, qui
non c'è un costo di apertura che scoraggi sedi aperte inutilizzate: il
verso opposto non è né imposto né garantito dall'ottimo.

## Il modello in gurobipy

```python
mod = gp.Model("p_mediana")
x = mod.addVars(m, vtype=GRB.BINARY, name="x")
y = mod.addVars(m, n, vtype=GRB.BINARY, name="y")
mod.setObjective(gp.quicksum(dist[l][c] * y[l, c] for l in range(m) for c in range(n)), GRB.MINIMIZE)
mod.addConstrs((y.sum("*", c) == 1 for c in range(n)), name="assegna")
mod.addConstr(x.sum() <= k, name="numero_sedi")
mod.addConstrs((x[l] - y[l, c] >= 0 for l in range(m) for c in range(n)), name="link")
```

## L'istanza

$m = 3$ sedi, $n = 3$ clienti, $k = 2$:

| $d_{lc}$ | $c=1$ | $c=2$ | $c=3$ |
|---|---:|---:|---:|
| $l=1$ | 5 | 6 | 10 |
| $l=2$ | 3 | 12 | 9 |
| $l=3$ | 10 | 9 | 4 |

## Euristica costruttiva: il bound primale

Si aprono le prime $k$ sedi; ogni cliente va alla sede aperta più vicina.
Aperte le sedi 1 e 2: cliente 1 → sede 2 (dist. 3), cliente 2 → sede 1
(dist. 6), cliente 3 → sede 2 (dist. 9). Valore $3+6+9=18$: $z(\mathrm{MILP})
\le \mathit{UB} = 18$.

## Rilassamento LP e duale: il bound duale

Con $\bar\varrho=0$, $\bar\pi_{lc}=0$ e $\bar\mu_c = \min_l d_{lc}$ (la
distanza dalla sede più vicina in assoluto):

$$
\bar\mu_1 = 3,\quad \bar\mu_2 = 6,\quad \bar\mu_3 = 4,
$$

di valore $13$. Per la dualità debole, $\mathit{LB}=13 \le z(\mathrm{LP})
\le z(\mathrm{MILP}) \le \mathit{UB}=18$.

**Quello che dice il solver.** $z(\mathrm{LP}) = z(\mathrm{LP}^+) = 15$: il
rilassamento è già intero su questa istanza. $z(\mathrm{MILP}) = 15$, con le
sedi 1 e 3 aperte (non 1 e 2 come nell'euristica): gap euristica $20{,}0\%$.

| $UB$ | $LB$ (duale) | $z(\mathrm{LP})$ | $z(\mathrm{LP}^+)$ | $z(\mathrm{MILP})$ | gap |
|---:|---:|---:|---:|---:|---:|
| 18 | 13 | 15 | 15 | 15 | $20{,}0\%$ |

![Soluzione ottima](img/cap08_pmediana_ottimo.png)

## Considerazioni aggiuntive

- Il vincolo è «al più $k$», non «esattamente $k$»: si verifica con la
  domanda 8.2.1 che l'ottimo non cambia imponendo l'uguaglianza.
- $\sum_c y_{lc} \le n\, x_l$ è una disuguaglianza valida aggregata, più
  debole di quella disaggregata usata nel modello.

## Domande di modellazione aggiuntive

??? question "8.2.1 — Esattamente $k$ sedi aperte"
    Si devono aprire esattamente $k$ sedi. Come cambia il modello? Qual è il
    nuovo ottimo?

    !!! tip "Soluzione"
        La soluzione è nel documento delle soluzioni, riservato ai docenti.
??? question "8.2.2 — Copertura di prossimità per un cliente"
    Il cliente 1 deve essere servito entro distanza $4$. Come si modella?
    Qual è il nuovo ottimo?

    !!! tip "Soluzione"
        La soluzione è nel documento delle soluzioni, riservato ai docenti.
## Codice

Script completo —
[`python/fam08_2_pmediana.py`](https://github.com/fabiofurini/modellazione-mip/blob/main/python/fam08_2_pmediana.py)
(riproducibile con `python3 python/fam08_2_pmediana.py` dalla cartella
`python/`). Notebook —
[`notebooks/fam08_2_pmediana.ipynb`](https://github.com/fabiofurini/modellazione-mip/blob/main/notebooks/fam08_2_pmediana.ipynb)
— che si apre in Colab dal badge in cima alla pagina.

<!-- script-incorporato: inizio (rigenerato da python/incorpora_codice.py) -->

??? example "Mostra lo script completo — `python/fam08_2_pmediana.py` (141 righe)"

    ```python
    """Problema 8.2 -- Localizzazione con numero massimo di sedi (p-mediana).

    Attivazione disaggregata fra x_l (sede aperta) e y_lc (cliente c servito da
    l), dedotta dalla CNF di un'implicazione booleana come nel problema 7.5, ma
    qui il numero di sedi è limitato da k invece che dal budget di tempo.
    """
    import gurobipy as gp
    import pandas as pd
    from gurobipy import GRB

    from mip import (due_rilassamenti, frazione, nuovo_modello, registra_bound,
                     risolvi, stampa_soluzione, valuta)
    from stile import CICLO, intestazione, plt, salva_dati, salva_figura

    R = range

    # ---------- 1. MODELLO E ISTANZA ----------

    intestazione("2. p-mediana: al più k sedi, ogni cliente al più vicino aperto")
    dist2 = [[5, 6, 10], [3, 12, 9], [10, 9, 4]]   # distanza sede l -> cliente c
    k2 = 2
    m, n = 3, 3
    salva_dati(pd.DataFrame([{"sede": l + 1, "cliente": c + 1, "d": dist2[l][c]}
                             for l in R(m) for c in R(n)]), "loc2_distanze")


    def modello_2(dist, k):
        m, n = len(dist), len(dist[0])
        mod = nuovo_modello("p_mediana")
        x = mod.addVars(m, vtype=GRB.BINARY, name="x")
        y = mod.addVars(m, n, vtype=GRB.BINARY, name="y")
        mod.setObjective(gp.quicksum(dist[l][c] * y[l, c] for l in R(m) for c in R(n)), GRB.MINIMIZE)
        mod.addConstrs((y.sum("*", c) == 1 for c in R(n)), name="assegna")
        mod.addConstr(x.sum() <= k, name="numero_sedi")
        mod.addConstrs((x[l] - y[l, c] >= 0 for l in R(m) for c in R(n)), name="link")
        return mod, x, y


    def duale_2(dist, k):
        """max sum mu_c + k varrho;  varrho + sum_c pi_lc <= 0;  mu_c - pi_lc <= d_lc;
        mu libere, varrho <= 0, pi >= 0."""
        m, n = len(dist), len(dist[0])
        dl = nuovo_modello("duale_p_mediana")
        mu = dl.addVars(n, lb=-GRB.INFINITY, name="mu")
        varrho = dl.addVar(lb=-GRB.INFINITY, ub=0.0, name="varrho")
        pi = dl.addVars(m, n, name="pi")
        dl.setObjective(mu.sum() + k * varrho, GRB.MAXIMIZE)
        dl.addConstrs((varrho + gp.quicksum(pi[l, c] for c in R(n)) <= 0 for l in R(m)), name="rc_x")
        dl.addConstrs((mu[c] - pi[l, c] <= dist[l][c] for l in R(m) for c in R(n)), name="rc_y")
        return dl


    m2, x2, y2 = modello_2(dist2, k2)

    # ---------- 2. EURISTICA COSTRUTTIVA (UPPER BOUND) ----------

    print("Euristica: si aprono le prime k sedi nell'ordine naturale, poi ogni cliente")
    print("va servito dalla sede aperta più vicina.")


    def euristica_2(dist, k):
        m, n = len(dist), len(dist[0])
        x = [1 if l < k else 0 for l in R(m)]
        y, passi = {}, []
        for c in R(n):
            md, sl = float("inf"), None
            for l in R(k):
                if dist[l][c] < md:
                    md, sl = dist[l][c], l
            y[(sl, c)] = 1
            passi.append(f"Cliente {c + 1}: la sede aperta più vicina è la {sl + 1} (distanza {md}); "
                         f"y[{sl + 1}][{c + 1}] = 1.")
        return x, y, passi


    xe, ye, passi = euristica_2(dist2, k2)
    print(f"  Si aprono le prime k = {k2} sedi: x = {xe}.")
    for i, s in enumerate(passi, 1):
        print(f"  Passo {i}. {s}")
    ub2 = sum(dist2[l][c] for (l, c) in ye)
    print(f"  ub = {ub2}")

    # ---------- 3. RILASSAMENTO LP E DUALE (LOWER BOUND) ----------

    d2 = duale_2(dist2, k2)
    mano = {"varrho": 0.0}
    mano.update({f"mu[{c}]": min(dist2[l][c] for l in R(m)) for c in R(n)})
    lb2, viol = valuta(d2, mano)
    assert viol <= 1e-9, viol
    print("Soluzione duale a mano: pi = 0, varrho = 0, mu_c = min_l d_lc = "
          + ", ".join(frazione(mano[f"mu[{c}]"]) for c in R(n)) + f"  ->  lb = {frazione(lb2)}")
    zlp2, zlp2r, _ = due_rilassamenti(m2, d2)

    # ---------- 4. SOLUZIONE OTTIMA DEL MILP ----------

    z2 = risolvi(m2)
    print("Soluzione ottima del MILP:")
    stampa_soluzione(m2, solo_non_nulle=True)
    riga = registra_bound("2 p-mediana", ub2, lb2, zlp2, zlp2r, z2)
    salva_dati(pd.DataFrame([riga]), "loc2_bound")

    # ---------- 5. DOMANDE DI MODELLAZIONE AGGIUNTIVE ----------

    varianti = {}


    def variante(nome, mod):
        z = risolvi(mod)
        print(f"  {nome:70s} z = {frazione(z)}")
        return z


    # 2a: esattamente k sedi devono essere aperte (non al più k)
    mod, x, y = modello_2(dist2, k2)
    mod.addConstr(x.sum() >= k2, name="numero_sedi_esatto")   # con "<= k" già nel modello, insieme impongono "= k"
    varianti["2a"] = variante("2a. Esattamente k sedi aperte (sum x_l = k)", mod)
    # 2b: il cliente 1 va servito entro distanza 4 (copertura aggiuntiva)
    mod, x, y = modello_2(dist2, k2)
    mod.addConstrs((y[l, 0] == 0 for l in R(3) if dist2[l][0] > 4), name="distanza_max_cliente1")
    varianti["2b"] = variante("2b. Il cliente 1 servito entro distanza 4 (y_l1 = 0 se d_l1 > 4)", mod)
    salva_dati(pd.DataFrame({"variante": list(varianti), "z": list(varianti.values())}), "loc2_varianti")

    # ---------- 6. FIGURE ----------

    fig, ax = plt.subplots(figsize=(5.5, 5))
    xs = {"sede": [0, 1.4, 2.8], "cliente": [0.3, 1.1, 2.4]}
    for c in R(3):
        l = next(l for l in R(3) if y2[l, c].X > 0.5)
        ax.plot([xs["sede"][l], xs["cliente"][c]], [1, 0], color=CICLO[c], lw=2, marker="o")
    for l in R(3):
        marker = "s" if x2[l].X > 0.5 else "x"
        ax.plot(xs["sede"][l], 1, marker=marker, ms=16, color="black" if x2[l].X > 0.5 else "gray")
        ax.annotate(f"sede {l + 1}", (xs["sede"][l], 1), textcoords="offset points", xytext=(0, 12), ha="center")
    for c in R(3):
        ax.plot(xs["cliente"][c], 0, marker="o", ms=10, color=CICLO[c])
        ax.annotate(f"cliente {c + 1}", (xs["cliente"][c], 0), textcoords="offset points", xytext=(0, -18), ha="center")
    ax.set_ylim(-0.4, 1.4)
    ax.axis("off")
    ax.set_title(f"p-mediana: soluzione ottima (z = {frazione(z2)}); quadrato = sede aperta")
    salva_figura(fig, "cap08_pmediana_ottimo")
    print("Fine.")
    ```

<!-- script-incorporato: fine -->
