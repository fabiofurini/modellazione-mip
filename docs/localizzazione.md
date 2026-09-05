# Localizzazione e copertura

**Classe:** BIP / MILP · **Script:** uno script e un notebook per problema
(`python/fam08_1_capacitata.py` … `fam08_4_hub.py`).

Quattro problemi in cui si decide **dove** aprire una struttura — una sede,
un hub — e come questo vincola le variabili che dipendono da quella
decisione: dove spedire la merce, quali clienti servire, quali clienti
coprire, a quale hub connettere ciascun terminale. Cambia, di problema in
problema, la natura del legame fra la variabile di apertura e le variabili
che ne dipendono e il modo in cui il budget sulle aperture entra nel modello.

!!! note "I legami fra variabili che si rivedono qui"
    **Attivazione aggregata** (8.1): un'unica famiglia di vincoli fa da
    legame e da vincolo di capacità insieme, $\sum_c y_{lc} \le u_l x_l$.
    **Attivazione disaggregata** (8.2): $x_l \ge y_{lc}$, dedotta dalla CNF
    di un'implicazione booleana come nel problema 7.5, con un budget $k$ sul
    numero di sedi. **Se e solo se** (8.3): un verso imposto da due famiglie
    di vincoli (soglia di segnale e interferenza), l'altro che segue
    dall'obiettivo. **Attivazione aggregata e variabile di massimo** (8.4):
    la stessa attivazione dell'8.1 insieme al legame di massimo
    $z_j \ge c_{ij} x_{ij}$ già visto nel problema 7.7.

## Notazione della famiglia

| Simbolo | Tipo | Significato |
|---|---|---|
| $m$ | $\in \mathbb{Z}_{\ge 1}$ | numero di sedi/hub candidati, $l \in \{1, 2, \dots, m\}$ |
| $n$ | $\in \mathbb{Z}_{\ge 1}$ | numero di clienti/terminali, $c \in \{1, 2, \dots, n\}$ |
| $t_{lc}$ | $\in \mathbb{Q}_{>0}$ | costo di trasporto/connessione dalla sede/hub $l$ al cliente/terminale $c$ |
| $i_l,\ f_l$ | $\in \mathbb{Q}_{\ge 0}$ | costo di apertura/attivazione della sede/hub $l$ |
| $u_l$ | $\in \mathbb{Q}_{>0}$ | capacità della sede $l$ |
| $d_c$ | $\in \mathbb{Q}_{>0}$ | domanda del cliente $c$ |
| $k$ | $\in \mathbb{Z}_{\ge 1}$ | numero massimo di sedi aperte / capacità di ciascun hub |
| $s_{lc}$ | $\in \mathbb{Q}_{\ge 0}$ | intensità del segnale dalla sede $l$ al cliente $c$ |
| $p_c$ | $\in \mathbb{Q}_{>0}$ | profitto se il cliente $c$ è coperto |
| $t,\ b$ | $\in \mathbb{Q}_{>0}$ | soglia di segnale e limite di interferenza |

## I quattro problemi

<div class="grid cards" markdown>

-   **8.1 Localizzazione capacitata**

    ---

    Dove aprire le sedi e quanto spedire da ciascuna: il vincolo di capacità
    è anche il legame di attivazione. Costo minimo.

    [:octicons-arrow-right-24: MILP · attivazione](localizzazione-1.md)

-   **8.2 p-mediana**

    ---

    Al più $k$ sedi aperte, ogni cliente al più vicino aperto: attivazione
    disaggregata, dedotta dalla CNF.

    [:octicons-arrow-right-24: BIP · attivazione](localizzazione-2.md)

-   **8.3 Copertura con interferenza**

    ---

    Un cliente è coperto se e solo se riceve segnale sufficiente e non
    troppa interferenza: un problema di massimo con due vincoli di link.

    [:octicons-arrow-right-24: BIP · se e solo se](localizzazione-3.md)

-   **8.4 Hub con costo massimo**

    ---

    Attivazione degli hub più il costo di connessione più alto per hub: la
    stessa variabile di massimo del problema 7.7, euristica riusata dal
    bin packing.

    [:octicons-arrow-right-24: MILP · attivazione, massimo](localizzazione-4.md)

</div>

## Modelli numerici della famiglia

Due modelli brevi con dati espliciti sulle tecniche di copertura e attivazione.

| Modello | Che cosa mette in gioco | $z(\mathrm{MILP})$ |
|---|---|---:|
| [EX 6 — Hub-and-spoke](ex-06.md) | set covering puro; il duale a mano chiude il problema | 3 |
| [EX 10 — Utensili CNC](ex-10.md) | attivazione disaggregata al rovescio; una ricetta duale non ammissibile, corretta | 2500 |
