---
hide:
  - navigation
  - toc
---

<div class="hero" markdown>

# Modellazione MIP

<!-- collana-riga -->
<p class="collana-riga" markdown>Un corso della collana <b>Ricerca Operativa e Matematica</b> · [tutti i corsi](#la-collana)</p>
<!-- /collana-riga -->

Materiale didattico ideato e sviluppato da **[Fabio Furini](https://fabiofurini.github.io/)**, professore
associato al [DIAG](https://www.diag.uniroma1.it/), Sapienza Università di Roma.

Il corso presenta la modellazione con la programmazione lineare intera: che cos'è un modello MIP,
rilassamenti, dualità e bound, l'implementazione in Python/Gurobi, le euristiche costruttive, la logica
con le variabili binarie e i legami fra variabili, e i modelli di problemi di assegnamento, scheduling,
localizzazione, copertura e pianificazione della produzione.

Prerequisiti: [Programmazione lineare intera](https://fabiofurini.github.io/programmazione-lineare-intera/).

[Comincia :material-arrow-right:](modellazione.md){ .md-button .md-button--primary }
[:material-pencil: Esercizi](da-modellare.md){ .md-button }
[:material-gesture-tap: Laboratorio](laboratorio/index.md){ .md-button }
[:material-clipboard-check-outline: Quiz](autovalutazione.md){ .md-button }
[:material-download: Materiale](materiale.md){ .md-button }

</div>

<!-- collana-app -->
## Provalo subito

Il modello dei lotti con costo fisso di setup, risolto all'ottimo nel browser: cambia il costo di setup, il costo di giacenza e la domanda dell'ultimo giorno con i cursori e l'ottimo ricalcola i giorni con un setup, il costo e il rilassamento continuo.

<div class="gi" data-grafico="mip-lotti"></div>

[:material-gesture-tap: Altre app nel laboratorio](laboratorio/index.md){ .md-button }
<!-- /collana-app -->

## Le parti del corso

<div class="grid cards" markdown>

-   :material-vector-polygon: **Modellazione**

    ---

    Che cos'è un MIP, logica e variabili binarie, i legami fra variabili
    (attivazione, lotto minimo, big-M, massimi, se e solo se…), i bound dal
    basso e dall'alto, il solver, e quindici modelli numerici svolti.

    [:octicons-arrow-right-24: I sei capitoli](modellazione.md)

-   :material-timer-sand: **Assegnamento e scheduling**

    ---

    Lavori su macchine con disponibilità: costi fissi, selezione, lavori in
    parallelo, setup, premi «se e solo se», sequenziamento con big-M.

    [:octicons-arrow-right-24: I sette problemi](scheduling.md)

-   :material-map-marker-radius: **Localizzazione e copertura**

    ---

    Dove aprire sedi e hub: attivazione aggregata e disaggregata, «se e solo
    se», variabile di massimo.

    [:octicons-arrow-right-24: I quattro problemi](localizzazione.md)

-   :material-factory: **Pianificazione della produzione**

    ---

    Quanto produrre, non soltanto se: scorte, costo fisso di setup, organico e
    assunzioni, lotto minimo.

    [:octicons-arrow-right-24: I tre problemi](produzione.md)

-   :material-shape-outline: **Problemi misti**

    ---

    I problemi senza famiglia: modalità alternative, contenitori, divisione e
    bilanciamento, bound duali con argomenti combinatori.

    [:octicons-arrow-right-24: I nove problemi](misti.md)

-   :material-school: **Il corso**

    ---

    Organizzazione, il formato degli esercizi, le dispense in PDF, i notebook.

    [:octicons-arrow-right-24: Organizzazione](organizzazione.md)

</div>

<!-- collana-da-non-perdere -->
## Da non perdere

<div class="grid cards" markdown>

-   :material-pencil-box-multiple: **Esercizi**

    ---

    Esercizi di modellazione per ogni capitolo, di livello d'esame, sui casi del corso.

    [:octicons-arrow-right-24: Gli esercizi](da-modellare.md)

-   :material-clipboard-check-outline: **Quiz di autovalutazione**

    ---

    Un facsimile d'esame nuovo a ogni avvio: 13 domande, 33 punti, con la soluzione e il link alle dispense. In Materiale c'è anche la banca completa delle domande.

    [:octicons-arrow-right-24: Mettiti alla prova](autovalutazione.md)

-   :material-gesture-tap: **Laboratorio interattivo**

    ---

    App che girano nel browser: muovi i parametri e guarda le idee del corso lavorare, un passo alla volta.

    [:octicons-arrow-right-24: Il laboratorio](laboratorio/index.md)

-   :material-download: **Dispense in PDF**

    ---

    Dispense, eserciziari e slide in PDF, con la stessa numerazione del sito.

    [:octicons-arrow-right-24: Il materiale](materiale.md)

-   :material-language-python: **Notebook in Colab**

    ---

    Il codice del corso che gira nel browser, senza installare niente.

    [:octicons-arrow-right-24: I notebook](notebook.md)

-   :material-format-list-numbered: **Indice completo**

    ---

    Tutti i capitoli con le loro sezioni in una pagina, e come è fatto ogni capitolo.

    [:octicons-arrow-right-24: L'indice](programma.md)

</div>
<!-- /collana-da-non-perdere -->

---

<!-- collana -->
## La collana

Tutti i corsi della collana hanno la stessa impostazione: dispense online e in PDF, esercizi con le soluzioni, laboratorio interattivo e quiz di autovalutazione.

<div class="grid cards" markdown>

-   :material-function-variant: **[Analisi Matematica 1](https://fabiofurini.github.io/analisi-matematica-1/)**

    numeri reali, funzioni, limiti, derivate e serie, con i grafici interattivi

-   :material-matrix: **[Algebra lineare](https://fabiofurini.github.io/algebra-lineare/)**

    vettori, matrici, determinanti, sistemi lineari e autovalori, con il laboratorio di calcolo

-   :material-code-braces: **[Algoritmi](https://fabiofurini.github.io/algoritmi/)**

    rappresentazione dei numeri, pseudocodice, ordinamento e ricerca, analisi e algoritmi ricorsivi

-   :material-vector-triangle: **[Programmazione lineare](https://fabiofurini.github.io/programmazione-lineare/)**

    poliedri, algoritmo del simplesso, dualità e simplesso duale, con il laboratorio interattivo

-   :material-dots-grid: **[Programmazione lineare intera](https://fabiofurini.github.io/programmazione-lineare-intera/)**

    rilassamento continuo, disuguaglianze valide, piani di taglio, branch-and-bound e branch-and-cut

-   :material-vector-curve: **[Ottimizzazione convessa](https://fabiofurini.github.io/ottimizzazione-convessa/)**

    insiemi e funzioni convesse, problemi di ottimizzazione convessa, con grafici interattivi

-   :material-graph-outline: **[Ottimizzazione su reti](https://fabiofurini.github.io/ottimizzazione-su-reti/)**

    grafi, alberi ricoprenti, cammini minimi, flussi su reti, simplesso su reti e gestione dei progetti

-   :material-hexagon-multiple-outline: **[Problemi di ottimizzazione combinatoria](https://fabiofurini.github.io/ottimizzazione-combinatoria/)**

    zaino, bin packing, colorazione, TSP, scheduling e lot sizing: i problemi, le formulazioni e gli algoritmi ad hoc

-   :material-table-large: **[Programmazione dinamica](https://fabiofurini.github.io/programmazione-dinamica/)**

    principi e algoritmi di PD per zaino, lot sizing, cambio monete e taglio delle aste

-   :material-map-marker-path: **[Algoritmi euristici](https://fabiofurini.github.io/algoritmi-euristici/)**

    euristiche costruttive, ricerca locale, metaeuristiche ed euristiche MIP per i problemi di ottimizzazione combinatoria

-   :material-approximately-equal: **[Algoritmi di approssimazione](https://fabiofurini.github.io/algoritmi-di-approssimazione/)**

    garanzie di prestazione, schemi di approssimazione e limiti dell'approssimazione per i problemi combinatori

-   :material-chart-line: **[Modellazione PL](https://fabiofurini.github.io/modellazione-pl/)**

    modelli di programmazione lineare per problemi gestionali, risolti con Python e Gurobi

-   :material-chart-bell-curve-cumulative: **[Modellazione PNL](https://fabiofurini.github.io/modellazione-pnl/)**

    modelli di programmazione non lineare, dal portafoglio al machine learning, con Python e Gurobi

-   :material-vector-polygon: **Modellazione MIP** · *questo corso*

    modelli di programmazione lineare a variabili intere, dalla formulazione alla soluzione con i solver

</div>
<!-- /collana -->

---

Materiale didattico di **[Fabio Furini](https://fabiofurini.github.io/)** —
[DIAG](https://www.diag.uniroma1.it/), Sapienza Università di Roma.
