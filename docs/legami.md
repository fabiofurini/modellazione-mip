# Legami fra variabili

**Classe:** tecniche di modellazione · **Script:** `python/cap03_legami.py`

[![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/cap03_legami.ipynb)

Il [capitolo 2](modellazione-2.md) collega variabili **tutte binarie**. Qui si
collegano famiglie **diverse**: binarie con continue, binarie con intere,
continue fra loro. Sono quattordici tecniche, e sono il vero contenuto della
modellazione MIP.

!!! note "Come si legge ogni tecnica"
    (a) il **legame in parole**; (b) i **vincoli lineari** che lo dicono, con il
    conteggio; (c) la **dimostrazione** — nei due versi se entrambi sono imposti
    dai vincoli, con un argomento di scambio se uno segue dall'ottimalità, con
    un *controesempio* quando una conversa è falsa; (d) la **forza del
    rilassamento** su un'istanza minima risolta dallo script; (e) la riga
    `gurobipy` e i rimandi ai problemi della Parte II.

!!! warning "Due proprietà che non vanno confuse"
    Una proprietà **imposta dai vincoli** vale per *ogni* soluzione ammissibile,
    ottima o no, e si dimostra guardando solo i vincoli. Una proprietà **di
    ottimalità** vale solo nelle soluzioni ottime, e si dimostra con un
    *argomento di scambio*: si prende una soluzione ammissibile che la viola, si
    costruisce una soluzione modificata, si verifica che resta ammissibile e si
    confrontano i valori. Se il valore migliora **strettamente** la conclusione
    è «in ogni ottimo»; se non peggiora è «esiste un ottimo», che è più debole.
    Scrivere «in ogni ottimo» quando il coefficiente è solo non negativo è
    l'errore più comune di questo capitolo.

<div class="grid cards" markdown>

-   **3.1 Attivazione**

    ---

    $x_{ij} \le y_j$ oppure $\sum_i x_{ij} \le k_j y_j$: più righe, rilassamento
    più stretto.

    [:octicons-arrow-right-24: aggregata o disaggregata](legami-01.md)

-   **3.2 Costo fisso**

    ---

    $q_j \le C_j y_j$ con il coefficiente **giusto**: la capacità, non un big-M.

    [:octicons-arrow-right-24: costo fisso e flusso](legami-02.md)

-   **3.3 Lotto minimo**

    ---

    $\ell y_j \le q_j \le C_j y_j$: la variabile semicontinua, e perché non si
    vede nel rilassamento.

    [:octicons-arrow-right-24: lotto minimo](legami-03.md)

-   **3.4 Conteggi interi**

    ---

    $\sum_i a_i x_i \le K w$ con $w$ intera: l'arrotondamento all'intero
    superiore, scritto senza scriverlo.

    [:octicons-arrow-right-24: quante scatole](legami-04.md)

-   **3.5 Variabile di massimo**

    ---

    $z \ge t_j x_j$: il vincolo dà $\ge$, l'obiettivo dà l'uguaglianza — se $z$
    non compare altrove.

    [:octicons-arrow-right-24: l'ausiliaria di massimo](legami-05.md)

-   **3.6 Min-max e max-min**

    ---

    Tre obiettivi di equità che descrivono la stessa soluzione con numeri
    diversi, e non si confrontano.

    [:octicons-arrow-right-24: min-max, max-min, differenza](legami-06.md)

-   **3.7 Valore assoluto**

    ---

    In obiettivo costa due vincoli e nessuna binaria; come vincolo $\ge$ è una
    disgiunzione, e la binaria serve.

    [:octicons-arrow-right-24: il valore assoluto](legami-07.md)

-   **3.8 Big-M**

    ---

    $a'x \le b + M(1-y)$: valido, migliorabile, minimo dimostrato. E che cosa
    succede se $M$ è troppo piccolo.

    [:octicons-arrow-right-24: vincoli condizionati](legami-08.md)

-   **3.9 Precedenze**

    ---

    «O prima l'uno o prima l'altro», con $M$ pari alla somma dei tempi e
    l'orizzonte dichiarato.

    [:octicons-arrow-right-24: sequenziamento](legami-09.md)

-   **3.10 Se e solo se**

    ---

    Un verso dal vincolo, l'altro dall'obiettivo — e che cosa succede quando il
    premio è nullo.

    [:octicons-arrow-right-24: se e solo se](legami-10.md)

-   **3.11 Contare i tipi**

    ---

    «Almeno due tipi diversi»: senza la soglia $\ell$ il conteggio non dice
    niente.

    [:octicons-arrow-right-24: conteggio dei tipi](legami-11.md)

-   **3.12 Alldiff ed espansione**

    ---

    Doppio partitioning (rilassamento esatto) ed espansione binaria (che non
    rafforza nulla).

    [:octicons-arrow-right-24: alldiff](legami-12.md)

-   **3.13 Vincoli violabili**

    ---

    $a'x + s^- - s^+ = \beta$ con penalità: da un modello inammissibile a uno
    utile.

    [:octicons-arrow-right-24: penalità](legami-13.md)

-   **3.14 Funzioni a tratti**

    ---

    Combinazione convessa più adiacenza: senza, si finisce sotto il grafico.

    [:octicons-arrow-right-24: scaglioni di costo](legami-14.md)

</div>

## La mappa delle tecniche

Si legge dalla prima colonna («che cosa voglio dire») alla seconda («come si
scrive»); le ultime due ricordano che cosa va dichiarato e dove la tecnica si
rivede all'opera.

| Tecnica | Formulazione | Da dichiarare | Si rivede in |
|---|---|---|---|
| [3.1 attivazione](legami-01.md) | $x_{ij} \le y_j$ (disagg.) oppure $\sum_i x_{ij} \le k_j y_j$ (agg.) | quale forma e perché; segno di $f_j$ per il verso di ottimalità | 7.2, 7.3, 7.5, 8.4 |
| [3.2 costo fisso](legami-02.md) | $q_j \le C_j y_j$ | che $C_j$ è la capacità, non un big-M | 8.1, cap. 9 |
| [3.3 lotto minimo](legami-03.md) | $\ell y_j \le q_j \le C_j y_j$ | che $\ell \le C_j$; che il rilassamento non ne risente | 7.2.2, 9.1, 9.3 |
| [3.4 conteggio intero](legami-04.md) | $\sum_i a_i x_i \le K w$, $w$ intera | che l'interezza realizza il tetto | 9.2, 12.1, 12.2 |
| [3.5 ausiliaria di massimo](legami-05.md) | $z \ge t_j x_j$, $z \ge 0$ | che $z$ non compare altrove; segno nell'obiettivo | 7.4, 7.7, 8.4, 11.4 |
| [3.6 min-max / max-min](legami-06.md) | $T \ge L_k$ e $\min T$; $U \le L_k$ e $\max U$ | quale dei tre obiettivi, e che non si confrontano | 7.4.1, 11.2, 11.3 |
| [3.7 valore assoluto](legami-07.md) | $d \ge \pm(u-v)$ in obiettivo; disgiunzione se $\ge k$ | se è obiettivo o vincolo, e in quale verso | 11.2, 11.3 |
| [3.8 big-M](legami-08.md) | $a'x \le b + M(1-y)$ | il valore di $M$ calcolato dai dati | 7.7, 3.9 |
| [3.9 precedenze](legami-09.md) | $s_{ij}+s_{ji}=1$, $\kappa_i \ge \kappa_j + t_i - M(1-s_{ij})$ | l'orizzonte e $M = \sum_h t_h$ | 7.7 |
| [3.10 se e solo se](legami-10.md) | $y \le x_j$ e $y \ge \sum_j x_j - (p-1)$ | se il secondo verso serve o segue dall'ottimalità | 7.6, 9.3 |
| [3.11 conteggio dei tipi](legami-11.md) | $\ell y_j \le q_j \le C_j y_j$, $\sum_j y_j \ge p$ | che senza la soglia $\ell$ il conteggio è vuoto | 9.3, 10.2, 12.1 |
| [3.12 alldiff / espansione](legami-12.md) | doppio partitioning; $v = \sum_k 2^k b_k$ | che l'alldiff ha rilassamento esatto | EX 9, EX 15 |
| [3.13 vincoli violabili](legami-13.md) | $a'x + s^- - s^+ = \beta$ con penalità | i due segni delle penalità | 9.1, EX 15 |
| [3.14 funzione a tratti](legami-14.md) | combinazione convessa $+$ adiacenza | se $g$ è convessa; altrimenti l'adiacenza è obbligatoria | 10.1 |

!!! tip "Le tre domande da farsi davanti a un legame nuovo"
    1. **Quale verso è imposto dai vincoli e quale no?** Si risponde guardando
       solo i vincoli, un caso per valore della binaria.
    2. **Il verso mancante segue dall'ottimalità?** Si risponde con l'argomento
       di scambio, e la risposta dipende dal *segno* del coefficiente
       nell'obiettivo: strettamente diverso da zero dà «in ogni ottimo», nullo
       dà al più «esiste un ottimo».
    3. **Quanto è forte il rilassamento?** Si risponde confrontando
       $z(\mathrm{LP}^+)$ con $z(\mathrm{MILP})$ su un'istanza piccola e, quando
       ci sono due formulazioni, confrontandole fra loro — dopo averle
       dimostrate equivalenti sui punti interi.

## Codice

Tutte le istanze minime di queste quattordici pagine sono risolte da
[`python/cap03_legami.py`](https://github.com/fabiofurini/modellazione-mip/blob/main/python/cap03_legami.py),
che salva la tavola riassuntiva in `dati/cap03_tecniche.csv`. Il notebook è
[`notebooks/cap03_legami.ipynb`](https://github.com/fabiofurini/modellazione-mip/blob/main/notebooks/cap03_legami.ipynb).

<!-- script-incorporato: inizio (rigenerato da python/incorpora_codice.py) -->

??? example "Mostra lo script completo — `python/cap03_legami.py` (496 righe)"

    ```python
    """Capitolo 3 -- Legami fra variabili: un esempio verificato per ogni tecnica.

    Quattordici tecniche di collegamento fra famiglie di variabili. Per ciascuna:
    un'istanza minima, il modello, l'ottimo intero, il rilassamento LP+ e --- dove
    esistono due formulazioni dello stesso insieme intero --- il confronto fra le
    loro forze. Ogni affermazione del capitolo sui numeri esce da qui, e ogni
    equivalenza fra formulazioni e' controllata per enumerazione.
    """
    from itertools import product

    import gurobipy as gp
    import pandas as pd
    from gurobipy import GRB

    from mip import (ammissibile, frazione, nuovo_modello, rilassamento, risolvi,
                     stampa_soluzione, valuta, viola_interezza)
    from stile import (ARANCIO, BLU, CICLO, GRIGIO, ROSSO, TEAL, VERDE, intestazione,
                       plt, salva_dati, salva_figura)

    R = range
    TAV = []          # riga per tecnica: (sezione, tecnica, z(MILP), z(LP+) forme a confronto)


    def registra(sezione, tecnica, zmilp, forme):
        """forme: {nome formulazione: z(LP+)}."""
        riga = {"sezione": sezione, "tecnica": tecnica, "z_milp": zmilp}
        for i, (nome, z) in enumerate(forme.items(), 1):
            riga[f"formulazione_{i}"] = nome
            riga[f"z_lp_{i}"] = z
        TAV.append(riga)
        testo = "   ".join(f"{n}: z(LP+) = {frazione(z)}" for n, z in forme.items())
        print(f"  z(MILP) = {frazione(zmilp)}      {testo}")


    # ---------- 1. ATTIVAZIONE: AGGREGATA O DISAGGREGATA ----------
    intestazione("3.1  Attivazione: il legame aggregato e quello disaggregato")
    f31 = [8, 6]                                   # costo di attivazione delle 2 sedi
    c31 = [[2, 5], [4, 1], [3, 3]]                 # costo di servire il cliente i dalla sede j
    n31, m31 = 3, 2


    def modello_attivazione(disaggregato):
        m = nuovo_modello("attivazione")
        x = m.addVars(n31, m31, vtype=GRB.BINARY, name="x")
        y = m.addVars(m31, vtype=GRB.BINARY, name="y")
        m.setObjective(gp.quicksum(f31[j] * y[j] for j in R(m31))
                       + gp.quicksum(c31[i][j] * x[i, j] for i in R(n31) for j in R(m31)),
                       GRB.MINIMIZE)
        m.addConstrs((x.sum(i, "*") == 1 for i in R(n31)), name="assegna")
        if disaggregato:
            m.addConstrs((x[i, j] <= y[j] for i in R(n31) for j in R(m31)), name="link")
        else:
            m.addConstrs((x.sum("*", j) <= n31 * y[j] for j in R(m31)), name="link")
        return m, x, y


    forme = {}
    for nome, dis in [("aggregata", False), ("disaggregata", True)]:
        m, x, y = modello_attivazione(dis)
        z31 = risolvi(m)
        forme[nome], _, _ = rilassamento(m, rafforzato=True)
    print("  Le due formulazioni hanno lo stesso insieme intero (verificato per enumerazione):")
    for valori in product((0, 1), repeat=n31 * m31 + m31):
        xv = {(i, j): valori[i * m31 + j] for i in R(n31) for j in R(m31)}
        yv = {j: valori[n31 * m31 + j] for j in R(m31)}
        agg = all(sum(xv[i, j] for i in R(n31)) <= n31 * yv[j] for j in R(m31))
        dis = all(xv[i, j] <= yv[j] for i in R(n31) for j in R(m31))
        assert agg == dis                        # sui punti binari le due forme coincidono
    registra("3.1", "attivazione aggregata / disaggregata", z31, forme)
    print("  Il numero di vincoli di link e' m = 2 nella forma aggregata e n m = 6 in quella")
    print("  disaggregata: piu' righe, rilassamento piu' stretto.")

    # ---------- 2. COSTO FISSO, CAPACITA' E FLUSSO CONTINUO ----------
    intestazione("3.2  Costo fisso, capacita' e flusso continuo")
    f32, c32, cap32, D32 = [10, 14], [3, 2], [6, 7], 9


    def modello_costofisso(M=None):
        m = nuovo_modello("costo_fisso")
        q = m.addVars(2, name="q")
        y = m.addVars(2, vtype=GRB.BINARY, name="y")
        m.setObjective(gp.quicksum(f32[j] * y[j] + c32[j] * q[j] for j in R(2)), GRB.MINIMIZE)
        m.addConstr(q.sum() >= D32, name="domanda")
        limite = cap32 if M is None else [M, M]
        m.addConstrs((q[j] <= limite[j] * y[j] for j in R(2)), name="link")
        if M is not None:
            m.addConstrs((q[j] <= cap32[j] for j in R(2)), name="capacita")
        return m, q, y


    forme = {}
    for nome, M in [("con la capacita' come coefficiente", None), ("con un big-M = 100", 100)]:
        m, q, y = modello_costofisso(M)
        z32 = risolvi(m)
        forme[nome], _, _ = rilassamento(m, rafforzato=True)
    registra("3.2", "costo fisso con capacita'", z32, forme)
    print("  Stesso insieme intero, stesso ottimo: ma il coefficiente piu' piccolo che")
    print("  funziona (la capacita') da' un rilassamento molto piu' stretto del big-M.")

    # ---------- 3. LOTTO MINIMO E VARIABILE SEMICONTINUA ----------
    intestazione("3.3  Lotto minimo: la variabile semicontinua")
    ell33 = 5


    def modello_lotto(con_soglia=True):
        m = nuovo_modello("lotto_minimo")
        q = m.addVars(2, name="q")
        y = m.addVars(2, vtype=GRB.BINARY, name="y")
        m.setObjective(gp.quicksum(f32[j] * y[j] + c32[j] * q[j] for j in R(2)), GRB.MINIMIZE)
        m.addConstr(q.sum() >= D32, name="domanda")
        m.addConstrs((q[j] <= cap32[j] * y[j] for j in R(2)), name="capacita")
        if con_soglia:
            m.addConstrs((q[j] >= ell33 * y[j] for j in R(2)), name="lotto")
        return m, q, y


    esiti33 = {}
    for nome, soglia in [("senza lotto minimo", False), ("con lotto minimo l = 5", True)]:
        m, q, y = modello_lotto(soglia)
        z = risolvi(m)
        zr, _, _ = rilassamento(m, rafforzato=True)
        esiti33[nome] = (z, zr)
        print(f"  {nome:26s} z(MILP) = {frazione(z):>5}   z(LP+) = {frazione(zr):>7}   "
              f"q = ({frazione(q[0].X)}, {frazione(q[1].X)})  y = ({int(y[0].X)}, {int(y[1].X)})")
    z33 = esiti33["con lotto minimo l = 5"][0]
    registra("3.3", "lotto minimo / semicontinua", z33,
             {"con lotto minimo": esiti33["con lotto minimo l = 5"][1]})
    print("  Sono due problemi diversi, non due formulazioni dello stesso: la soglia cambia")
    print("  l'insieme ammissibile e l'ottimo passa da 44 a 49. Il rilassamento LP+ pero'")
    print("  non cambia: con y frazionaria il vincolo q_j >= l y_j non morde, perche' y_j")
    print("  puo' scendere quanto serve. La soglia si paga tutta sull'interezza.")
    print(f"  Con la soglia, ogni q_j vale 0 oppure sta in [{ell33}, cap_j]: e' una variabile")
    print("  semicontinua, scritta con due vincoli e una binaria.")

    # ---------- 4. CONTEGGI INTERI, CAPACITA' MULTIPLA, ARROTONDAMENTO ----------
    intestazione("3.4  Conteggi interi: quante scatole servono")
    pezzi34, capienza34 = 17, 5
    m = nuovo_modello("scatole")
    w = m.addVar(vtype=GRB.INTEGER, name="w")
    m.setObjective(w, GRB.MINIMIZE)
    m.addConstr(capienza34 * w >= pezzi34, name="capienza")
    z34 = risolvi(m)
    zr34, _, _ = rilassamento(m, rafforzato=True)
    print(f"  {pezzi34} pezzi, capienza {capienza34}: w >= {pezzi34}/{capienza34} = "
          f"{frazione(pezzi34 / capienza34)}, e w intera da' w = {int(z34)}")
    assert z34 == -(-pezzi34 // capienza34)        # ceil
    registra("3.4", "conteggio intero (arrotondamento all'intero superiore)", z34,
             {"vincolo di capienza": zr34})
    print("  Il rilassamento vale 17/5: l'interezza, da sola, alza il bound di 3/5.")

    # ---------- 5. AUSILIARIA DI MASSIMO ----------
    intestazione("3.5  La variabile che vale il massimo")
    t35 = [4, 7, 3]                                # tempi dei tre lavori
    m = nuovo_modello("massimo")
    xm = m.addVars(3, vtype=GRB.BINARY, name="x")
    zmax = m.addVar(name="z")
    m.setObjective(zmax, GRB.MINIMIZE)
    m.addConstr(xm.sum() >= 2, name="almeno_due")
    m.addConstrs((zmax >= t35[j] * xm[j] for j in R(3)), name="massimo")
    z35 = risolvi(m)
    zr35, _, _ = rilassamento(m, rafforzato=True)
    scelti35 = [j + 1 for j in R(3) if xm[j].X > 0.5]
    print(f"  Lavori scelti {scelti35}; z = {frazione(zmax.X)} = max dei tempi scelti "
          f"= {max(t35[j] for j in R(3) if xm[j].X > 0.5)}")
    assert abs(zmax.X - max(t35[j] for j in R(3) if xm[j].X > 0.5)) < 1e-9
    registra("3.5", "ausiliaria di massimo", z35, {"z >= t_j x_j": zr35})
    print("  Il vincolo impone solo z >= max; e' l'obiettivo, che minimizza z, a")
    print("  renderlo un'uguaglianza in ogni ottimo.")

    # ---------- 6. MIN-MAX, MAX-MIN E DIFFERENZA ----------
    intestazione("3.6  Min-max, max-min e differenza fra il massimo e il minimo")
    p36 = [3, 5, 2, 4, 7]                          # pesi da ripartire su 2 operai (totale 21)


    def modello_bilanciamento(criterio):
        m = nuovo_modello("bilanciamento")
        a = m.addVars(len(p36), 2, vtype=GRB.BINARY, name="a")
        car = m.addVars(2, name="carico")
        m.addConstrs((a.sum(i, "*") == 1 for i in R(len(p36))), name="assegna")
        m.addConstrs((car[k] == gp.quicksum(p36[i] * a[i, k] for i in R(len(p36))) for k in R(2)),
                     name="carico_def")
        if criterio == "minmax":
            T = m.addVar(name="T")
            m.addConstrs((T >= car[k] for k in R(2)), name="max")
            m.setObjective(T, GRB.MINIMIZE)
        elif criterio == "maxmin":
            L = m.addVar(name="L")
            m.addConstrs((L <= car[k] for k in R(2)), name="min")
            m.setObjective(L, GRB.MAXIMIZE)
        else:                                       # differenza massimo - minimo
            T = m.addVar(name="T")
            L = m.addVar(name="L")
            m.addConstrs((T >= car[k] for k in R(2)), name="max")
            m.addConstrs((L <= car[k] for k in R(2)), name="min")
            m.setObjective(T - L, GRB.MINIMIZE)
        return m, car


    risultati36 = {}
    for criterio in ["minmax", "maxmin", "differenza"]:
        m, car = modello_bilanciamento(criterio)
        z = risolvi(m)
        risultati36[criterio] = (z, (car[0].X, car[1].X))
        print(f"  {criterio:11s} z = {frazione(z):>5}   carichi = "
              f"({frazione(car[0].X)}, {frazione(car[1].X)})   totale {sum(p36)}")
    zr36, _, _ = rilassamento(modello_bilanciamento("minmax")[0], rafforzato=True)
    registra("3.6", "min-max / max-min / differenza", risultati36["minmax"][0], {"min-max": zr36})
    assert risultati36["minmax"][0] == 11 and risultati36["maxmin"][0] == 10
    assert risultati36["differenza"][0] == 1
    print("  Il totale 21 e' dispari: la ripartizione perfetta non esiste e il meglio")
    print("  possibile e' (11, 10). Le tre versioni scelgono la stessa ripartizione, ma i")
    print("  loro obiettivi valgono 11, 10 e 1: sono tre numeri diversi che descrivono la")
    print("  stessa soluzione, e non si confrontano fra loro.")

    # ---------- 7. VALORE ASSOLUTO ----------
    intestazione("3.7  Il valore assoluto: in obiettivo e nei vincoli")
    obiettivo37 = list(p36)          # la stessa istanza della sezione precedente
    m = nuovo_modello("valore_assoluto")
    a = m.addVars(len(obiettivo37), 2, vtype=GRB.BINARY, name="a")
    car = m.addVars(2, name="carico")
    d = m.addVar(name="d")                          # d >= |carico_1 - carico_2|
    m.addConstrs((a.sum(i, "*") == 1 for i in R(len(obiettivo37))), name="assegna")
    m.addConstrs((car[k] == gp.quicksum(obiettivo37[i] * a[i, k] for i in R(len(obiettivo37)))
                  for k in R(2)), name="carico_def")
    m.addConstr(d >= car[0] - car[1], name="abs_piu")
    m.addConstr(d >= car[1] - car[0], name="abs_meno")
    m.setObjective(d, GRB.MINIMIZE)
    z37 = risolvi(m)
    zr37, _, _ = rilassamento(m, rafforzato=True)
    print(f"  min |carico_1 - carico_2| = {frazione(z37)}, con carichi "
          f"({frazione(car[0].X)}, {frazione(car[1].X)})")
    assert abs(z37 - abs(car[0].X - car[1].X)) < 1e-9
    registra("3.7", "valore assoluto in obiettivo", z37, {"due vincoli, d >= +/-(u-v)": zr37})
    # |u - v| >= k NON si scrive con due vincoli: serve una disgiunzione
    m2 = nuovo_modello("abs_vincolo")
    u = m2.addVar(ub=10, name="u")
    v = m2.addVar(ub=10, name="v")
    b = m2.addVar(vtype=GRB.BINARY, name="b")
    m2.setObjective(u + v, GRB.MINIMIZE)
    m2.addConstr(u + v >= 6, name="somma")
    m2.addConstr(u - v >= 4 - 20 * (1 - b), name="disg_piu")     # b = 1 -> u - v >= 4
    m2.addConstr(v - u >= 4 - 20 * b, name="disg_meno")          # b = 0 -> v - u >= 4
    z37b = risolvi(m2)
    print(f"  |u - v| >= 4 con u + v >= 6, min u + v: z = {frazione(z37b)}, "
          f"u = {frazione(u.X)}, v = {frazione(v.X)}, b = {int(b.X)}")
    print("  In obiettivo (minimo) il valore assoluto costa due vincoli e nessuna binaria;")
    print("  come vincolo >= diventa una disgiunzione, e la binaria serve.")

    # ---------- 8. BIG-M: VINCOLI CONDIZIONATI E DISGIUNZIONI ----------
    intestazione("3.8  Big-M: quanto grande, e che cosa cambia nel rilassamento")
    a38, b38 = [3, 4, 5], 6      # y = 1  =>  3x1 + 4x2 + 5x3 <= 6


    def modello_bigm(M):
        m = nuovo_modello("bigM")
        xb = m.addVars(3, vtype=GRB.BINARY, name="x")
        y = m.addVar(vtype=GRB.BINARY, name="y")
        m.setObjective(gp.quicksum(xb[j] for j in R(3)) + y, GRB.MAXIMIZE)
        m.addConstr(gp.quicksum(a38[j] * xb[j] for j in R(3)) <= b38 + M * (1 - y), name="cond")
        return m


    Mmin = sum(a38) - b38        # il piu' piccolo M valido: max del membro sinistro meno b
    forme = {}
    for etichetta, M in [(f"M minimo = {Mmin}", Mmin), ("M = 20", 20), ("M = 1000", 1000)]:
        m = modello_bigm(M)
        z38 = risolvi(m)
        forme[etichetta], _, _ = rilassamento(m, rafforzato=True)
        print(f"  {etichetta:16s} z(MILP) = {frazione(z38)}   z(LP+) = {frazione(forme[etichetta])}")
    m = modello_bigm(Mmin - 1)   # M troppo piccolo: taglia soluzioni ammissibili
    z_troppo = risolvi(m)
    print(f"  M = {Mmin - 1} (troppo piccolo) da' z(MILP) = {frazione(z_troppo)} invece di "
          f"{frazione(z38)}:")
    print("  con y = 0 il vincolo dovrebbe sparire e invece resta 3x1 + 4x2 + 5x3 <= 11,")
    print("  che esclude x = (1,1,1). Un M non valido non rende il modello 'un po' diverso':")
    print("  gli toglie soluzioni ammissibili.")
    assert z_troppo < z38
    registra("3.8", "big-M in un vincolo condizionato", z38, forme)

    # ---------- 9. PRECEDENZE E SEQUENZIAMENTO ----------
    intestazione("3.9  Precedenze: la disgiunzione 'o prima l'uno o prima l'altro'")
    t39 = [3, 2, 4]
    M39 = sum(t39)
    m = nuovo_modello("sequenziamento")
    kap = m.addVars(3, name="kappa")                # istante di completamento
    s = m.addVars(3, 3, vtype=GRB.BINARY, name="s")  # s[i,j] = 1 se j precede i
    Cmax = m.addVar(name="Cmax")
    m.setObjective(Cmax, GRB.MINIMIZE)
    m.addConstrs((kap[j] >= t39[j] for j in R(3)), name="minimo")
    m.addConstrs((Cmax >= kap[j] for j in R(3)), name="makespan")
    for i in R(3):
        for j in R(i):
            m.addConstr(s[i, j] + s[j, i] == 1, name=f"disg{i}{j}")
            m.addConstr(kap[i] >= kap[j] + t39[i] - M39 * (1 - s[i, j]), name=f"prec{i}{j}")
            m.addConstr(kap[j] >= kap[i] + t39[j] - M39 * (1 - s[j, i]), name=f"prec{j}{i}")
    z39 = risolvi(m)
    zr39, _, _ = rilassamento(m, rafforzato=True)
    print(f"  Tre lavori di durata {t39} su una macchina: makespan = {frazione(z39)} = "
          f"somma dei tempi = {sum(t39)}")
    print(f"  Completamenti: " + ", ".join(f"kappa_{j+1} = {frazione(kap[j].X)}" for j in R(3)))
    assert z39 == sum(t39)
    registra("3.9", "precedenze e sequenziamento (big-M)", z39, {f"M = sum t_j = {M39}": zr39})
    print(f"  Il piu' piccolo M che funziona e' la somma dei tempi, {M39}: un M piu' grande")
    print("  lascia lo stesso insieme intero e un rilassamento piu' debole.")

    # ---------- 10. SE E SOLO SE ----------
    intestazione("3.10  'Se e solo se': un verso dal vincolo, l'altro dall'obiettivo")
    classe = [0, 1, 2]           # i tre lavori della classe
    premio = 9
    ric = [2, 2, 2]


    def modello_iff(entrambi_i_versi, v):
        m = nuovo_modello("iff")
        xj = m.addVars(3, vtype=GRB.BINARY, name="x")
        yc = m.addVar(vtype=GRB.BINARY, name="y")
        m.setObjective(gp.quicksum(ric[j] * xj[j] for j in R(3)) + v * yc, GRB.MAXIMIZE)
        m.addConstr(gp.quicksum(xj[j] for j in R(3)) <= 3, name="capacita")
        m.addConstrs((yc <= xj[j] for j in R(3)), name="premio_su")     # y = 1 => tutti scelti
        if entrambi_i_versi:                                            # tutti scelti => y = 1
            m.addConstr(yc >= gp.quicksum(xj[j] for j in R(3)) - 2, name="premio_giu")
        return m, xj, yc


    for v in (premio, 0):
        for nome, versi in [("solo y <= x_j", False), ("anche y >= sum x_j - 2", True)]:
            m, xj, yc = modello_iff(versi, v)
            z310 = risolvi(m)
            zr310, _, _ = rilassamento(m, rafforzato=True)
            tutti = all(xj[j].X > 0.5 for j in R(3))
            fedele = (round(yc.X) == 1) == tutti
            print(f"  premio = {v}   {nome:24s} z(MILP) = {frazione(z310):>4}   "
                  f"y = {int(yc.X)}   x = {[int(xj[j].X) for j in R(3)]}   "
                  f"y coerente con 'classe completa': {'si' if fedele else 'NO'}")
    m, xj, yc = modello_iff(True, premio)
    z310 = risolvi(m)
    zr310, _, _ = rilassamento(m, rafforzato=True)
    registra("3.10", "se e solo se", z310, {"entrambi i versi imposti": zr310})
    print("  Con premio > 0 il verso mancante segue dall'ottimalita': in ogni ottimo y = 1")
    print("  quando i tre lavori sono eseguiti, perche' alzare y aumenta l'obiettivo.")
    print("  Con premio = 0 quell'argomento cade e il solo vincolo y <= x_j lascia y = 0")
    print("  con tutti i lavori eseguiti: se y deve *significare* 'classe completa' anche")
    print("  fuori dall'ottimo, il secondo vincolo va scritto.")

    # ---------- 11. CONTARE I TIPI DIVERSI ----------
    intestazione("3.11  Contare quanti tipi diversi si producono")
    q_max = [10, 10, 10]
    ric311 = [4, 3, 5]
    m = nuovo_modello("tipi")
    qq = m.addVars(3, name="q")
    yy = m.addVars(3, vtype=GRB.BINARY, name="y")
    m.setObjective(gp.quicksum(ric311[j] * qq[j] for j in R(3)), GRB.MAXIMIZE)
    m.addConstr(qq.sum() <= 12, name="risorsa")
    m.addConstrs((qq[j] <= q_max[j] * yy[j] for j in R(3)), name="attiva")
    m.addConstr(yy.sum() >= 2, name="almeno_due_tipi")
    m.addConstrs((qq[j] >= 3 * yy[j] for j in R(3)), name="lotto")
    z311 = risolvi(m)
    zr311, _, _ = rilassamento(m, rafforzato=True)
    print("  Almeno due tipi in produzione, lotto minimo 3: q = "
          + ", ".join(frazione(qq[j].X) for j in R(3))
          + f"   tipi attivi = {int(sum(yy[j].X for j in R(3)))}")
    registra("3.11", "conteggio dei tipi diversi", z311, {"attivazione + soglia": zr311})
    print("  Senza il lotto minimo, y_j = 1 con q_j = 0 sarebbe ammissibile e la soglia")
    print("  'almeno due tipi' non direbbe niente: le due tecniche vanno insieme.")

    # ---------- 12. ALLDIFF ED ESPANSIONE BINARIA ----------
    intestazione("3.12  Alldiff e espansione binaria di una variabile intera")
    val312 = [1, 2, 3]           # tre posizioni distinte da assegnare a tre oggetti
    costo312 = [[4, 2, 5], [3, 6, 1], [7, 3, 2]]
    m = nuovo_modello("alldiff")
    p = m.addVars(3, 3, vtype=GRB.BINARY, name="p")   # p[i,v] = 1 se l'oggetto i prende il valore v
    m.setObjective(gp.quicksum(costo312[i][v] * p[i, v] for i in R(3) for v in R(3)), GRB.MINIMIZE)
    m.addConstrs((p.sum(i, "*") == 1 for i in R(3)), name="un_valore")
    m.addConstrs((p.sum("*", v) == 1 for v in R(3)), name="alldiff")
    z312 = risolvi(m)
    zr312, _, _ = rilassamento(m, rafforzato=True)
    print("  Alldiff = un set partitioning per riga e uno per colonna; z = " + frazione(z312))
    # espansione binaria: v in {0,...,7} come somma di potenze di 2
    me = nuovo_modello("espansione")
    bb = me.addVars(3, vtype=GRB.BINARY, name="b")
    vv = me.addVar(vtype=GRB.INTEGER, ub=7, name="v")
    me.addConstr(vv == gp.quicksum(2 ** k * bb[k] for k in R(3)), name="espansione")
    me.addConstr(vv >= 5, name="soglia")
    me.setObjective(vv, GRB.MINIMIZE)
    z312b = risolvi(me)
    print(f"  Espansione binaria: v = {int(z312b)} = "
          + " + ".join(f"{2 ** k}" for k in R(3) if bb[k].X > 0.5)
          + f"   (b = {[int(bb[k].X) for k in R(3)]})")
    assert z312b == 5 and sum(2 ** k * round(bb[k].X) for k in R(3)) == 5
    registra("3.12", "alldiff / espansione binaria", z312, {"doppio partitioning": zr312})
    assert abs(zr312 - z312) < 1e-9
    print("  Qui z(LP+) = z(MILP): la matrice del doppio partitioning e' totalmente")
    print("  unimodulare, il rilassamento ha gia' vertici interi e l'interezza e' gratis.")

    # ---------- 13. VINCOLI VIOLABILI E PENALITA' ----------
    intestazione("3.13  Vincoli violabili: deviazioni positive e negative con penalita'")
    target = [6, 6, 6]
    disp = 15
    pen_su, pen_giu = 3, 2
    m = nuovo_modello("penalita")
    qv = m.addVars(3, name="q")
    su = m.addVars(3, name="s_piu")
    giu = m.addVars(3, name="s_meno")
    m.setObjective(gp.quicksum(pen_su * su[j] + pen_giu * giu[j] for j in R(3)), GRB.MINIMIZE)
    m.addConstr(qv.sum() <= disp, name="risorsa")
    m.addConstrs((qv[j] + giu[j] - su[j] == target[j] for j in R(3)), name="target")
    z313 = risolvi(m)
    zr313, _, _ = rilassamento(m, rafforzato=True)
    print("  Domanda 6 per periodo, disponibilita' 15: q = "
          + ", ".join(frazione(qv[j].X) for j in R(3))
          + "   sotto-copertura = " + ", ".join(frazione(giu[j].X) for j in R(3)))
    print(f"  penalita' totale = {frazione(z313)}")
    assert abs(sum(giu[j].X for j in R(3)) - 3) < 1e-9
    registra("3.13", "vincoli violabili con penalita'", z313, {"deviazioni +/-": zr313})
    print("  Le due deviazioni non sono mai entrambe positive in un ottimo: le penalita'")
    print("  sono positive, e ridurle entrambe della stessa quantita' resta ammissibile.")

    # ---------- 14. FUNZIONI LINEARI A TRATTI ----------
    intestazione("3.14  Funzione lineare a tratti: scaglioni di costo")
    nodi = [0, 4, 10, 16]                     # estremi degli scaglioni
    costi = [0, 12, 30, 36]                   # costo cumulato in ciascun nodo (sconto di quantita')
    domanda314 = 13


    def modello_tratti(adiacenza=True):
        """Combinazione convessa con binarie di tratto (adiacenza esplicita)."""
        m = nuovo_modello("tratti")
        lam = m.addVars(len(nodi), name="lambda")
        w = m.addVars(len(nodi) - 1, vtype=GRB.BINARY, name="w")
        qtot = m.addVar(name="q")
        m.addConstr(lam.sum() == 1, name="convessa")
        m.addConstr(qtot == gp.quicksum(nodi[k] * lam[k] for k in R(len(nodi))), name="ascissa")
        m.setObjective(gp.quicksum(costi[k] * lam[k] for k in R(len(nodi))), GRB.MINIMIZE)
        m.addConstr(qtot >= domanda314, name="domanda")
        if adiacenza:
            m.addConstr(w.sum() == 1, name="un_tratto")
            for k in R(len(nodi)):
                vicini = [t for t in R(len(nodi) - 1) if t == k or t == k - 1]
                m.addConstr(lam[k] <= gp.quicksum(w[t] for t in vicini), name=f"adiacenza{k}")
        return m, lam, w, qtot


    forme = {}
    for nome, adj in [("senza adiacenza (combinazione convessa libera)", False),
                      ("con adiacenza (SOS2 scritta a mano)", True)]:
        m, lam, w, qtot = modello_tratti(adj)
        z314 = risolvi(m)
        forme[nome], _, _ = rilassamento(m, rafforzato=True)
        attivi = [k for k in R(len(nodi)) if lam[k].X > 1e-9]
        print(f"  {nome:46s} z = {frazione(z314)}   lambda non nulle nei nodi {attivi}")
    registra("3.14", "funzione lineare a tratti", z314, forme)
    print("  Attenzione al rilassamento: con w frazionaria il vincolo di adiacenza non morde")
    print("  piu', e le due formulazioni hanno lo stesso z(LP+). L'adiacenza cambia")
    print("  l'insieme intero, non la forza del rilassamento.")
    esatto = costi[2] + (costi[3] - costi[2]) * (domanda314 - nodi[2]) / (nodi[3] - nodi[2])
    print(f"  Il valore esatto della funzione a tratti in q = {domanda314} e' {frazione(esatto)}.")
    print("  Senza l'adiacenza la combinazione convessa puo' mescolare i nodi 0 e 3, che non")
    print("  sono estremi di uno stesso tratto: si ottiene un punto sotto il grafico, cioe'")
    print("  l'inviluppo convesso inferiore, e un costo che la funzione non assume mai.")

    # ---------- 15. LA TAVOLA DELLE TECNICHE ----------
    intestazione("3.15  La tavola riassuntiva")
    tav = pd.DataFrame(TAV)
    salva_dati(tav, "cap03_tecniche")
    for riga in TAV:
        print(f"  {riga['sezione']:5s} {riga['tecnica'][:44]:46s} z(MILP) = {frazione(riga['z_milp'])}")

    # ---------- 16. FIGURE ----------
    fig, ax = plt.subplots(figsize=(6.6, 3.8))
    ax.plot(nodi, costi, "o-", color=TEAL, lw=2, label="funzione a tratti $g(q)$")
    for k in R(len(nodi) - 1):
        ax.annotate(f"tratto {k + 1}", ((nodi[k] + nodi[k + 1]) / 2, (costi[k] + costi[k + 1]) / 2),
                    textcoords="offset points", xytext=(-16, 10), fontsize=8, color=GRIGIO)
    ax.plot([domanda314], [esatto], "s", color=ROSSO, ms=9, label=f"$q = {domanda314}$, $g = {esatto:g}$")
    ax.plot([nodi[0], nodi[-1]], [costi[0], costi[-1]], "--", color=GRIGIO, lw=1,
            label="corda fra i nodi 0 e 3 (senza adiacenza)")
    ax.set_xlabel("quantita' $q$")
    ax.set_ylabel("costo $g(q)$")
    ax.set_title("Scaglioni di costo: una funzione lineare a tratti convessa")
    ax.legend(fontsize=8)
    salva_figura(fig, "cap03_tratti")

    fig, ax = plt.subplots(figsize=(6.6, 3.6))
    etichette = ["aggregata", "disaggregata"]
    valori = [TAV[0]["z_lp_1"], TAV[0]["z_lp_2"]]
    ax.bar(etichette, valori, color=[ARANCIO, TEAL], width=0.5)
    ax.axhline(TAV[0]["z_milp"], color=ROSSO, lw=1.6, ls="--")
    ax.annotate(f"$z(\\mathrm{{MILP}}) = {TAV[0]['z_milp']:g}$", (1.35, TAV[0]["z_milp"]),
                ha="right", va="bottom", fontsize=9, color=ROSSO)
    for i, v in enumerate(valori):
        ax.annotate(f"{v:.3f}", (i, v), ha="center", va="bottom", fontsize=9)
    ax.set_ylabel("$z(\\mathrm{LP}^+)$")
    ax.set_ylim(0, TAV[0]["z_milp"] * 1.25)
    ax.set_title("Attivazione: la forma disaggregata da' un rilassamento piu' stretto")
    salva_figura(fig, "cap03_attivazione")
    print("Fine.")
    ```

<!-- script-incorporato: fine -->
