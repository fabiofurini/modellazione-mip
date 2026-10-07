# Modellazione MIP

Materiale didattico ideato e sviluppato da **[Fabio Furini](https://sites.google.com/view/fabiofurini/home-page)**, professore
associato al [DIAG](https://www.diag.uniroma1.it/), Sapienza Università di Roma.

**Modelli di programmazione lineare intera per prendere decisioni ottime.**

<div class="grid cards" markdown>

-   :material-book-open-page-variant:{ .lg .middle } **Sto studiando la teoria**

    ---

    Che cos'è un modello MIP, logica e variabili binarie, i quattordici legami,
    rilassamenti e bound, euristiche, Gurobi.

    [:octicons-arrow-right-24: I sei capitoli](modellazione.md)

-   :material-pencil-ruler:{ .lg .middle } **Voglio fare esercizi**

    ---

    Trentotto problemi svolti per intero e quaranta da modellare, con enunciato,
    modello, istanza, euristica, duale e ottimo.

    [:octicons-arrow-right-24: I problemi](problemi.md)

-   :material-language-python:{ .lg .middle } **Voglio usare Gurobi**

    ---

    Quarantacinque notebook che girano nel browser, senza installare niente:
    lo stesso codice delle pagine, cella per cella.

    [:octicons-arrow-right-24: I notebook](notebook.md)

</div>

[:octicons-download-24: Scarica il materiale del corso](materiale.md){ .md-button .md-button--primary }

## Che cosa si impara a fare

- **Leggere un problema e scriverne il modello.** Quali sono le decisioni, quali
  variabili servono e con che dominio, e come ogni frase dell'enunciato diventa
  un vincolo.
- **Far vedere che il modello fa quello che deve.** Un vincolo che lega due
  variabili impone un'implicazione: si dimostra che la impone davvero, nei due
  versi.
- **Trovare una buona soluzione a mano**, con un'euristica che si costruisce in
  pochi passi e si sa giustificare.
- **Costruire il duale del rilassamento** e ricavarne quanto, al massimo, si
  potrebbe ancora guadagnare.
- **Dire quanto vale la soluzione che si ha in mano.** Su un'istanza grande il
  solver si ferma prima dell'ottimo: restano una soluzione e due numeri che la
  racchiudono. Se distano poco, quella soluzione si usa — e lo si può
  dimostrare.
- **Scrivere e risolvere il modello con Gurobi**, e capire che cosa risponde il
  solver.

## Come il corso ci arriva

- **Il metodo, in sei capitoli**: logica e variabili binarie, i quattordici
  legami fra variabili con le loro dimostrazioni, rilassamenti e bound,
  euristiche costruttive, Gurobi.
- **Trentotto problemi svolti per intero**: quindici modelli numerici, uno per
  tecnica, con i dati scritti per esteso; e ventitré problemi delle tre famiglie
  — assegnamento e scheduling, localizzazione e copertura, pianificazione della
  produzione — più i problemi misti. Ciascuno con enunciato, modello, istanza,
  euristica, duale, ottimo e confronto.
- **Due o tre domande aggiuntive su ogni problema**: si cambia un dato o si
  aggiunge un vincolo, e si rifanno modello e bound. Per ciascuno degli esercizi
  una variante è svolta per intero, come modello di risposta.
- **Quaranta problemi da modellare**, dati come arrivano davvero e senza il
  modello già scritto: venti con i dati numerici espliciti e venti in forma
  simbolica.
- **Quarantacinque [notebook](notebook.md)** che girano in Colab, senza
  installare niente: lo stesso codice delle pagine, cella per cella.
- **Nessun risultato trascritto a mano**: ogni numero viene da uno script che si
  può rilanciare, e un controllo automatico verifica che il testo e il codice
  dicano la stessa cosa.

!!! tip "Il formato di ogni esercizio (e dell'esame)"
    Modello → legami fra le variabili → istanza → euristica (upper bound) →
    duale del rilassamento LP (lower bound) → soluzione con il solver →
    domande di modellazione aggiuntive.

## Le due parti del corso

<div class="grid cards" markdown>

-   :material-vector-polygon: **Modellazione**

    ---

    Che cos'è un MIP, logica e variabili binarie, i legami fra variabili
    (attivazione, lotto minimo, big-M, massimi, se e solo se…), i bound dal
    basso e dall'alto, il solver.

    [:octicons-arrow-right-24: I sei capitoli](modellazione.md)

-   :material-puzzle: **I problemi**

    ---

    Tre famiglie — assegnamento e scheduling, localizzazione e copertura,
    pianificazione della produzione — più un capitolo di problemi misti, per i
    problemi che una famiglia non ce l'hanno. Esercizi risolti e domande
    aggiuntive.

    [:octicons-arrow-right-24: I problemi](problemi.md)

-   :material-school: **Il corso**

    ---

    Organizzazione, il formato dell'esame, le dispense in PDF, i notebook.

    [:octicons-arrow-right-24: Organizzazione](organizzazione.md)

</div>

## Il corso in breve

**6 capitoli di modellazione · 38 problemi svolti per intero · 40 problemi da
modellare · 45 notebook in Colab.** L'elenco completo, capitolo per capitolo, sta
nel [programma](programma.md).

## Per cominciare

Non serve installare niente: ogni script del corso ha il suo
[notebook che si apre in Colab](notebook.md) e gira nel browser.

Chi preferisce lavorare in locale trova i comandi e le note sulla licenza Gurobi
nella pagina del [materiale scaricabile](materiale.md#rigenerare-tutto).

---

Dello stesso autore: **[Laboratorio di Ricerca Operativa](https://fabiofurini.github.io/laboratorio-ricerca-operativa/)** —
il modulo di laboratorio, con gli stessi strumenti e lo stesso stile — e
**[Analisi Matematica 1](https://fabiofurini.github.io/analisi-matematica-1/)** — le dispense di analisi,
con i grafici interattivi.

Materiale didattico di **[Fabio Furini](https://sites.google.com/view/fabiofurini/home-page)** —
[DIAG](https://www.diag.uniroma1.it/), Sapienza Università di Roma.
