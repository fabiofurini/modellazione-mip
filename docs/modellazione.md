# Modellazione

Sei capitoli di tecniche: che cos'è un modello MIP, la logica delle variabili
binarie, i legami fra variabili, i bound dal lato del rilassamento (duale) e dal
lato delle soluzioni ammissibili (euristiche costruttive), il solver.

Ogni capitolo ha uno **script** che produce tutti i numeri citati e un
**notebook** che si apre in Colab. Nessun valore compare in queste pagine se non
esce da un'esecuzione riproducibile.

<div class="grid cards" markdown>

-   :material-shape-outline: **1. Che cos'è un modello MIP**

    ---

    Dati, variabili, obiettivo, vincoli. Perché l'arrotondamento fallisce. I due
    rilassamenti LP e da che parte stanno i bound. Tre gap da non confondere.
    Branch-and-bound in una pagina.

    [:octicons-arrow-right-24: Il capitolo](modellazione-1.md)

-   :material-gate-and: **2. Logica e variabili binarie**

    ---

    AND, OR, NOT; clausole e forma normale congiuntiva; le tre regole che
    traducono una CNF in vincoli lineari; implicazioni, contronominali e
    scissioni; cinque esercizi risolti e verificati per enumerazione.

    [:octicons-arrow-right-24: Il capitolo](modellazione-2.md)

-   :material-link-variant: **3. Legami fra variabili**

    ---

    Quattordici tecniche per collegare famiglie diverse di variabili:
    attivazione, costo fisso, lotto minimo, conteggi, massimo, min-max, valore
    assoluto, big-M, precedenze, «se e solo se», tipi, alldiff, penalità,
    funzioni a tratti. Più la mappa consultabile.

    [:octicons-arrow-right-24: Le quattordici tecniche](legami.md)

-   :material-arrow-collapse-vertical: **4. Rilassamenti, dualità e bound**

    ---

    La tabella di conversione primale/duale, tre ricette per costruire a mano
    una soluzione duale, disuguaglianze valide e tagli di copertura, e perché i
    duali dell'LP non sono i prezzi marginali del MILP.

    [:octicons-arrow-right-24: Il capitolo](modellazione-4.md)

-   :material-run-fast: **5. Euristiche costruttive**

    ---

    Next-fit, first-fit, best-fit, LPT, euristica costruttiva di copertura, euristica costruttiva per lo zaino
    e lot sizing: pseudocodice, traccia, verifica di ammissibilità e bound. Un
    fallimento della euristica costruttiva non dimostra l'inammissibilità.

    [:octicons-arrow-right-24: Il capitolo](modellazione-5.md)

-   :material-language-python: **6. Dal modello a Python/Gurobi**

    ---

    Le quattro classi di variabili, una `addConstrs` per famiglia, e come si
    leggono `Status`, `SolCount`, `ObjVal`, `ObjBound`, `MIPGap`,
    `NodeCount` e le tolleranze. Il protocollo del corso, dall'inizio alla fine.

    [:octicons-arrow-right-24: Il capitolo](modellazione-6.md)

</div>
