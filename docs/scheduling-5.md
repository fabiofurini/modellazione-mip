# Una macchina, classi di lavori con setup

**Classe:** BIP · **Legami:** attivazione disaggregata, CNF · **Script:** `python/fam07_5_classisetup.py`

[![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/fam07_5_classisetup.ipynb)

!!! abstract "Problema 7.5"
    Un'azienda ha $n$ lavori eseguibili su una macchina con disponibilità
    $a \in \mathbb{Q}_{>0}$ minuti. Per ogni lavoro $j$, $t_j$ è il tempo e $r_j$ il
    ricavo se eseguito. I lavori sono partizionati in $q \ge 2$ classi
    $\mathscr{J}_1, \dots, \mathscr{J}_q$. Se la macchina esegue lavori di una classe
    $c$, si paga un costo di setup $f_c \ge 0$ e si consuma un tempo di setup
    $s_c \ge 0$. La macchina non esegue lavori in parallelo. Massimizzare il
    profitto.

**Il problema a parole.** *Decidiamo* quali lavori eseguire e quali classi
attivare. *L'obiettivo*: ricavi meno costi di setup. *Il vincolo*: tempi dei
lavori più tempi di setup entro la disponibilità. Uno zaino con costi fissi per
gruppo: il legame di attivazione, stavolta **disaggregato** fin dall'inizio.

## Modello

| Simbolo | Tipo | Significato |
|---|---|---|
| $n$, $a$ | | numero di lavori, disponibilità |
| $t_j$, $r_j$ | $\in \mathbb{Q}_{>0}$ | tempo e ricavo del lavoro $j$ |
| $q$, $\mathscr{J}_c$ | | numero di classi e lavori della classe $c$ (partizione) |
| $f_c$, $s_c$ | $\in \mathbb{Q}_{\ge 0}$ | costo e tempo di setup della classe $c$ |

**Variabili.** $n + q$ binarie: $x_j = 1$ se il lavoro $j$ è eseguito;
$y_c = 1$ se almeno un lavoro della classe $c$ è eseguito.

$$
\begin{aligned}
\max ~~ \sum_{j=1}^{n} r_j\, x_j - \sum_{c=1}^{q} f_c\, y_c & & \\
\text{soggetto a} \quad \sum_{j=1}^{n} t_j\, x_j + \sum_{c=1}^{q} s_c\, y_c &\le a, & \\
x_j - y_c &\le 0, & \forall c,\ \forall j \in \mathscr{J}_c, \\
x_j \in \{0, 1\},\quad y_c &\in \{0, 1\}. &
\end{aligned}
$$

- l'obiettivo massimizza ricavi meno setup;
- il vincolo di **disponibilità** ($1$ vincolo lineare);
- i vincoli di **link**: se un lavoro di una classe è eseguito, la classe è
  attivata ($n$ vincoli lineari, uno per lavoro);
- i vincoli di dominio definiscono le variabili.

!!! note "Legame fra le variabili: la CNF diventa vincolo"
    **Dal vincolo.** «Se almeno un lavoro della classe $c$ è eseguito, la classe
    è attivata»: $(x_j \,\mathtt{OR}\, x_s \,\mathtt{OR}\, \dots) \Rightarrow y_c$,
    contronominale $\mathtt{NOT}\,y_c \Rightarrow (\mathtt{NOT}\,x_j \,\mathtt{AND}\, \dots)$.
    L'espressione $\mathtt{NOT}(x_j \,\mathtt{OR}\, \dots) \,\mathtt{OR}\, y_c$ diventa,
    con De Morgan e distributività, la CNF
    $(\mathtt{NOT}\,x_j \,\mathtt{OR}\, y_c) \,\mathtt{AND}\, (\mathtt{NOT}\,x_s \,\mathtt{OR}\, y_c) \,\mathtt{AND}\, \dots$,
    cioè $1 - x_j + y_c \ge 1$: **esattamente** i vincoli di link
    $x_j \le y_c$. Verifica nei due versi: $x_j = 1$ forza $y_c = 1$; $y_c = 0$
    forza tutti gli $x_j$ della classe a $0$.

    **Dall'ottimo.** «Se nessun lavoro della classe è eseguito, la classe non è
    attivata»: non imposta, segue **senza perdita di ottimalità**: porre
    $y_c = 0$ resta ammissibile, libera $s_c$ minuti e non diminuisce
    l'obiettivo perché $f_c \ge 0$. Poiché $f_c$ può essere nullo, la
    conclusione corretta è «esiste un ottimo in cui…», non «in ogni ottimo».

## Il modello in gurobipy

```python
m = gp.Model("classi_setup");  m.Params.OutputFlag = 0
x = m.addVars(n, vtype=GRB.BINARY, name="x")
y = m.addVars(q, vtype=GRB.BINARY, name="y")
m.setObjective(gp.quicksum(r[j] * x[j] for j in range(n))
               - gp.quicksum(f[c] * y[c] for c in range(q)), GRB.MAXIMIZE)
m.addConstr(gp.quicksum(t[j] * x[j] for j in range(n))
            + gp.quicksum(s[c] * y[c] for c in range(q)) <= a, name="disponibilita")
m.addConstrs((x[j] - y[c] <= 0 for c in range(q) for j in J[c]), name="link")
m.optimize()
```

## L'istanza

$n = 7$, $q = 3$: $\mathscr{J}_1 = \{1, 2\}$, $\mathscr{J}_2 = \{3, 4\}$,
$\mathscr{J}_3 = \{5, 6, 7\}$, $a = 50$.

| | $j=1$ | $j=2$ | $j=3$ | $j=4$ | $j=5$ | $j=6$ | $j=7$ |
|---|---:|---:|---:|---:|---:|---:|---:|
| $r_j$ | 10 | 6 | 8 | 6 | 7 | 9 | 5 |
| $t_j$ | 5 | 10 | 8 | 6 | 9 | 5 | 6 |

| | $c=1$ | $c=2$ | $c=3$ |
|---|---:|---:|---:|
| $f_c$ | 10 | 5 | 4 |
| $s_c$ | 10 | 12 | 6 |

## Euristica costruttiva: il bound primale

Classe per classe: il primo lavoro paga anche il setup, se ci sta.

- **Passo 1.** Classe 1: $s_1 + t_1 = 15 \le 50$; $y[1] = x[1] = 1$, $ra = 35$.
- **Passo 2.** $t_2 = 10 \le 35$; $x[2] = 1$, $ra = 25$.
- **Passo 3.** Classe 2: $s_2 + t_3 = 20 \le 25$; $y[2] = x[3] = 1$, $ra = 5$.
- **Passo 4.** $t_4 = 6 > 5$: saltato. **Passi 5–7.** Classe 3: $s_3 + t_j > 5$:
  saltati.

Profitto $10 + 6 + 8 - 10 - 5 = 9$: $z(\mathit{MILP}) \ge 9$.

## Rilassamento LP e duale: il bound duale

Con $\pi \ge 0$ (disponibilità) e $\lambda_j \ge 0$ (link):

$$
\begin{aligned}
\min ~~ a\, \pi & & \\
\text{soggetto a} \quad t_j\, \pi + \lambda_j &\ge r_j, & \forall j, \\
s_c\, \pi - \sum_{j \in \mathscr{J}_c} \lambda_j &\ge -f_c, & \forall c, \\
\pi \ge 0,\quad \lambda_j &\ge 0. &
\end{aligned}
$$

**Una soluzione duale a mano.** $\bar\lambda = 0$ e
$\bar\pi = \max_j r_j/t_j = \tfrac{10}{5} = 2$: valore $100$. Quindi
$9 \le z(\mathit{MILP}) \le 100$: un bound grossolano, come spesso i bound «di
zaino», che ignora setup e costi.

**Quello che dice il solver.** $z(\mathit{LP}) = 425/13 = 32{,}7$ (con
$\pi = \tfrac{17}{26}$ e alcuni $\lambda_j > 0$); $z(\mathit{LP}^+) = 329/13$.
Ottimo intero $21$: classi 2 e 3, lavori $3, 4, 5, 6$, profitto $30 - 9$.
L'euristica resta a $9$ (gap $57\%$): l'ordine di scansione conta.

| $LB$ | $UB$ (duale a mano) | $z(\mathit{LP})$ | $z(\mathit{LP}^+)$ | $z(\mathit{MILP})$ | gap euristica |
|---:|---:|---:|---:|---:|---:|
| 9 | 100 | $425/13$ | $329/13$ | 21 | $57{,}1\%$ |

## Considerazioni aggiuntive

- $y_c \le 1$ rafforza il rilassamento; $x_j \le 1$ è implicato.
- $\sum_{j \in \mathscr{J}_c} x_j \ge y_c$ ($q$ vincoli) non è valido ma
  preserva l'ottimo.
- La forma aggregata $\sum_{j \in \mathscr{J}_c} x_j \le |\mathscr{J}_c|\, y_c$
  ha lo stesso insieme intero e un rilassamento più debole.

## Domande di modellazione aggiuntive

??? question "7.5.1 — Una sola classe"
    Si può attivare al più una classe.

    !!! tip "Soluzione"
        La soluzione è nel documento delle soluzioni, riservato ai docenti.
??? question "7.5.2 — Una classe subordinata a un'altra"
    La classe 3 si può attivare solo se si attiva anche la classe 1.

    !!! tip "Soluzione"
        La soluzione è nel documento delle soluzioni, riservato ai docenti.
## Codice

Script completo: [`python/fam07_5_classisetup.py`](https://github.com/fabiofurini/modellazione-mip/blob/main/python/fam07_5_classisetup.py);
notebook: [`notebooks/fam07_5_classisetup.ipynb`](https://github.com/fabiofurini/modellazione-mip/blob/main/notebooks/fam07_5_classisetup.ipynb).

<!-- script-incorporato: inizio (rigenerato da python/incorpora_codice.py) -->

??? example "Mostra lo script completo — `python/fam07_5_classisetup.py` (127 righe)"

    ```python
    """Problema 7.5 -- Una macchina, classi di lavori con setup.

    Il legame di attivazione disaggregato dedotto passo passo dalla CNF di
    un'implicazione booleana: (OR di lavori) => classe attivata.
    """
    import gurobipy as gp
    import numpy as np
    import pandas as pd
    from gurobipy import GRB

    from euristiche import best_fit, first_fit, matrice, next_fit
    from mip import (ammissibile, due_rilassamenti, frazione, nuovo_modello,
                     registra_bound, risolvi, stampa_soluzione, valuta)
    from stile import CICLO, ROSSO, intestazione, plt, salva_dati, salva_figura

    R = range

    # ---------- 1. MODELLO E ISTANZA ----------
    intestazione("5. Classi di lavori con costo e tempo di setup: y_c attiva la classe")
    r5 = [10, 6, 8, 6, 7, 9, 5]
    t5 = [5, 10, 8, 6, 9, 5, 6]
    J5 = [[0, 1], [2, 3], [4, 5, 6]]       # classi (0-based)
    f5 = [10, 5, 4]
    s5 = [10, 12, 6]
    a5 = 50
    salva_dati(pd.DataFrame({"lavoro": R(1, 8), "r": r5, "t": t5,
                             "classe": [c + 1 for j in R(7) for c in R(3) if j in J5[c]]}), "sched5_lavori")
    salva_dati(pd.DataFrame({"classe": R(1, 4), "f": f5, "s": s5}), "sched5_classi")


    def modello_5(r, t, J, f, s, a):
        n, q = len(r), len(J)
        m = nuovo_modello("classi_setup")
        x = m.addVars(n, vtype=GRB.BINARY, name="x")
        y = m.addVars(q, vtype=GRB.BINARY, name="y")
        m.setObjective(gp.quicksum(r[j] * x[j] for j in R(n)) - gp.quicksum(f[c] * y[c] for c in R(q)),
                       GRB.MAXIMIZE)
        m.addConstr(gp.quicksum(t[j] * x[j] for j in R(n)) + gp.quicksum(s[c] * y[c] for c in R(q)) <= a,
                    name="disponibilita")
        m.addConstrs((x[j] - y[c] <= 0 for c in R(q) for j in J[c]), name="link")
        return m, x, y


    def duale_5(r, t, J, f, s, a):
        """min a pi;  t_j pi + lam_j >= r_j;  s_c pi - sum_{j in J_c} lam_j >= -f_c;  pi, lam >= 0."""
        n, q = len(r), len(J)
        d = nuovo_modello("duale_classi_setup")
        pi = d.addVar(name="pi")
        lam = d.addVars(n, name="lam")
        d.setObjective(a * pi, GRB.MINIMIZE)
        d.addConstrs((t[j] * pi + lam[j] >= r[j] for j in R(n)), name="rc_x")
        d.addConstrs((s[c] * pi - gp.quicksum(lam[j] for j in J[c]) >= -f[c] for c in R(q)), name="rc_y")
        return d


    def euristica_5(r, t, J, f, s, a):
        """Classe per classe: il primo lavoro paga anche il setup, se ci sta."""
        n, q = len(r), len(J)
        x, y, ra, passi = [0] * n, [0] * q, a, []
        for c in R(q):
            for j in J[c]:
                if y[c] == 0:
                    if s[c] + t[j] <= ra:
                        y[c], x[j] = 1, 1
                        passi.append(f"Classe {c + 1} non attiva: s[{c + 1}] + t[{j + 1}] = {s[c]} + {t[j]} = "
                                     f"{s[c] + t[j]} <= ra = {ra}; y[{c + 1}] = 1, x[{j + 1}] = 1, ra = {ra - s[c] - t[j]}.")
                        ra -= s[c] + t[j]
                    else:
                        passi.append(f"Classe {c + 1} non attiva: s[{c + 1}] + t[{j + 1}] = {s[c] + t[j]} > ra = {ra}; "
                                     f"il lavoro {j + 1} viene saltato.")
                else:
                    if t[j] <= ra:
                        x[j] = 1
                        passi.append(f"Classe {c + 1} attiva: t[{j + 1}] = {t[j]} <= ra = {ra}; x[{j + 1}] = 1, ra = {ra - t[j]}.")
                        ra -= t[j]
                    else:
                        passi.append(f"Classe {c + 1} attiva: t[{j + 1}] = {t[j]} > ra = {ra}; il lavoro {j + 1} viene saltato.")
        return x, y, passi


    m5, x5, y5 = modello_5(r5, t5, J5, f5, s5, a5)

    # ---------- 2. EURISTICA COSTRUTTIVA (LOWER BOUND) ----------
    xe, ye, passi = euristica_5(r5, t5, J5, f5, s5, a5)
    print("Euristica classe per classe:")
    for i, s in enumerate(passi, 1):
        print(f"  Passo {i}. {s}")
    lb5 = sum(r5[j] * xe[j] for j in R(7)) - sum(f5[c] * ye[c] for c in R(3))
    print(f"  lb = {lb5}  (x = {xe}, y = {ye})")

    # ---------- 3. RILASSAMENTO LP E DUALE (UPPER BOUND) ----------
    d5 = duale_5(r5, t5, J5, f5, s5, a5)
    pi_mano = max(r5[j] / t5[j] for j in R(7))
    ub5, viol = valuta(d5, {"pi": pi_mano})
    assert viol <= 1e-9
    print(f"Soluzione duale a mano: lam = 0, pi = max_j r_j/t_j = {frazione(pi_mano)}  ->  ub = {frazione(ub5)}")
    zlp5, zlp5r, _ = due_rilassamenti(m5, d5)

    # ---------- 4. SOLUZIONE OTTIMA DEL MILP ----------
    z5 = risolvi(m5)
    print("Soluzione ottima del MILP:")
    stampa_soluzione(m5, solo_non_nulle=True)
    riga = registra_bound("5 classi setup", ub5, lb5, zlp5, zlp5r, z5, senso="max")
    salva_dati(pd.DataFrame([riga]), "sched5_bound")

    # ---------- 5. DOMANDE DI MODELLAZIONE AGGIUNTIVE ----------


    varianti = {}


    def variante(nome, m):
        z = risolvi(m)
        print(f"  {nome:70s} z = {frazione(z)}")
        return z

    # 5a: una sola classe attiva
    m, x, y = modello_5(r5, t5, J5, f5, s5, a5)
    m.addConstr(y.sum() <= 1, name="una_classe")
    varianti["5a"] = variante("5a. Al più una classe attivata (sum y_c <= 1)", m)
    # 5b: la classe 3 solo se la classe 1
    m, x, y = modello_5(r5, t5, J5, f5, s5, a5)
    m.addConstr(y[2] <= y[0], name="3_solo_se_1")
    varianti["5b"] = variante("5b. La classe 3 si attiva solo se si attiva la classe 1 (y_3 <= y_1)", m)
    salva_dati(pd.DataFrame({"variante": list(varianti), "z": list(varianti.values())}), "sched5_varianti")

    print("Fine.")
    ```

<!-- script-incorporato: fine -->
