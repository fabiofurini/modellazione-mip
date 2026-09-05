# Pianificazione della produzione

**Classe:** MILP · **Script:** uno script e un notebook per problema
(`python/fam09_1_lotti.py` … `fam09_3_veicoli.py`).

Tre problemi in cui si decide **quanto** produrre, non soltanto *se* fare
qualcosa. Le variabili di quantità sono continue o intere, e sopra di esse si
appoggiano delle binarie che accendono, limitano o premiano: il lancio della
produzione con il suo costo fisso (9.1), l'organico con le assunzioni (9.2), il
lotto minimo per tipo con un premio per la varietà (9.3).

Il tratto comune è il **bilancio**: una quantità che entra, una che esce e una
che resta. Nel 9.1 e nel 9.2 è il bilancio delle scorte,
$x_t + s_{t-1} - s_t = d_t$; nel 9.2 c'è in più il bilancio dell'organico,
$y_t - y_{t-1} - z_t = 0$. Sono vincoli di uguaglianza, e i loro duali sono
variabili **libere**: è la prima famiglia del corso in cui questo succede in
modo sistematico.

!!! note "I legami fra variabili che si rivedono qui"
    **Costo fisso** (9.1): $x_t \le M_t\, y_t$, con $M_t$ letto dai dati (la
    domanda residua) e non scelto a caso.
    **Conteggi interi** (9.2): l'organico $y_t$ e le assunzioni $z_t$ sono
    numeri di persone, e le ore disponibili sono $r\, y_t$.
    **Lotto minimo** (9.3): la variabile semicontinua
    $q_j\, y_j \le x_j \le M_j\, y_j$, che vale zero oppure almeno $q_j$.
    **Contare i tipi** e **se e solo se** (9.3): il premio per la varietà si
    incassa solo se il conteggio dei tipi attivi arriva a due, e il verso
    mancante lo impone l'ottimalità perché il premio è positivo.

## Notazione della famiglia

| Simbolo | Tipo | Significato |
|---|---|---|
| $n$ | $\in \mathbb{Z}_{\ge 1}$ | numero di periodi, $t \in \{1, 2, \dots, n\}$ |
| $d_t$ | $\in \mathbb{Q}_{\ge 0}$ | domanda del periodo $t$ |
| $p_t$ | $\in \mathbb{Q}_{>0}$ | costo unitario di produzione nel periodo $t$ |
| $q_t$ | $\in \mathbb{Q}_{\ge 0}$ | costo fisso di lancio nel periodo $t$ |
| $h_t$ | $\in \mathbb{Q}_{\ge 0}$ | costo di magazzino a fine periodo $t$ |
| $M_t$ | $\in \mathbb{Q}_{>0}$ | massima produzione utile: $\sum_{\tau \ge t} d_\tau + r_n$ |
| $m_0$ | $\in \mathbb{Z}_{\ge 0}$ | operai in servizio all'inizio |
| $w,\ u$ | $\in \mathbb{Q}_{>0}$ | salario per periodo e costo di assunzione |
| $r,\ g$ | $\in \mathbb{Q}_{>0}$ | ore per operaio e ore per unità di prodotto |
| $a_{ij}$ | $\in \mathbb{Q}_{\ge 0}$ | risorsa $i$ per una unità del tipo $j$ |
| $b_i$ | $\in \mathbb{Q}_{>0}$ | disponibilità della risorsa $i$ |
| $\bar q_j$ | $\in \mathbb{Z}_{\ge 1}$ | lotto minimo del tipo $j$, se lo si produce |
| $\bar r$ | $\in \mathbb{Q}_{>0}$ | premio se si producono almeno due tipi |

## I tre problemi

<div class="grid cards" markdown>

-   **9.1 Lotti con costo fisso di lancio**

    ---

    Bilancio delle scorte e lancio della produzione con big-M letto dai dati.
    Due euristiche a confronto: lot-for-lot e least unit cost.

    [:octicons-arrow-right-24: MILP · costo fisso](produzione-1.md)

-   **9.2 Produzione e manodopera**

    ---

    La stessa decisione scritta due volte, con le assunzioni o con l'organico:
    si dimostra che i due modelli sono equivalenti, ottimo e rilassamento
    compresi.

    [:octicons-arrow-right-24: MILP · conteggi interi](produzione-2.md)

-   **9.3 Veicoli con lotto minimo e premio**

    ---

    Variabili semicontinue, conteggio dei tipi attivi e un premio «se e solo
    se». Qui il rilassamento con i bound batte il duale a mano.

    [:octicons-arrow-right-24: MILP · lotto minimo](produzione-3.md)

</div>

