# Modellazione MIP

Materiale didattico ideato e sviluppato da **[Fabio Furini](https://sites.google.com/view/fabiofurini/home-page)**, professore
associato al [DIAG](https://www.diag.uniroma1.it/), Sapienza Università di Roma.

**Modelli di programmazione lineare intera per l'Ingegneria Gestionale** — la
dispensa del corso in versione online, con codice Python/Gurobi, notebook e
istanze riproducibili. È il secondo corso della serie iniziata con il
[Laboratorio di Ricerca Operativa](https://fabiofurini.github.io/laboratorio-ricerca-operativa/).

Un modello con variabili binarie e intere non si *scrive* soltanto: si
*dimostra*. Ogni vincolo che lega due famiglie di variabili impone
un'implicazione logica, e lo studente deve saper provare che la impone davvero
— in entrambi i versi, oppure spiegando perché un verso segue dall'ottimalità.
Poi il modello si *stringe*: un'euristica costruttiva fornisce un upper bound
e una soluzione duale del rilassamento lineare fornisce un lower bound, che
intrappolano il valore ottimo fra i due — la stessa tecnica usata in pratica
quando un'istanza reale è troppo grande per essere risolta all'ottimo provato.
Infine il modello si *risolve*, con Gurobi da Python.

Tutti i modelli si possono eseguire **subito nel browser**: ogni capitolo ha il
suo [notebook che si apre in Colab](notebook.md), senza installare niente.

!!! tip "Il metodo del corso"
    Per ogni problema: modello → dimostrazione dei legami → istanza →
    euristica (upper bound) → duale del rilassamento LP (lower bound) →
    soluzione con il solver → **domande di modellazione aggiuntive**, perché
    il modello base lo si legge, la variante la si scrive.

## Le tre parti del corso

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
    pianificazione della produzione — più un capitolo di modelli misti, per i
    problemi che una famiglia non ce l'hanno. Esercizi risolti e domande
    aggiuntive.

    [:octicons-arrow-right-24: I problemi](problemi.md)

-   :material-school: **Il corso**

    ---

    Organizzazione, il formato dell'esame, la raccolta degli enunciati per
    esercitarsi, i notebook.

    [:octicons-arrow-right-24: Organizzazione](organizzazione.md)

</div>

## Installazione e licenza

```bash
python3 -m pip install gurobipy
```

Il pacchetto pip include una **licenza dimostrativa** (fino a 2000 variabili e 2000 vincoli):
sufficiente per tutte le istanze di questo corso. All'avvio compare la riga
`Restricted license - for non-production use only`: è normale.

**Licenza accademica completa (gratuita):**
1. registrarsi su <https://portal.gurobi.com> con l'email istituzionale (`@uniroma1.it`);
2. richiedere una *Named-User Academic License*;
3. eseguire il comando `grbgetkey XXXXXXXX-...` mostrato dal portale (serve la rete di ateneo o VPN);
4. la licenza viene salvata in `~/gurobi.lic` e da quel momento non ci sono limiti di dimensione.

---

## Avvio rapido

```bash
python3 -m pip install gurobipy matplotlib pandas
python3 python/esegui_tutti.py        # rigenera dati, risultati, figure e notebook
```

Oppure **senza installare niente**: ogni capitolo ha un
[notebook che si apre in Colab](notebook.md) e gira nel browser.

Nel [repository](https://github.com/fabiofurini/modellazione-mip)
trovi tutti gli **script Python** e le **istanze** in CSV.

---

Materiale didattico di **[Fabio Furini](https://sites.google.com/view/fabiofurini/home-page)** —
[DIAG](https://www.diag.uniroma1.it/), Sapienza Università di Roma.
