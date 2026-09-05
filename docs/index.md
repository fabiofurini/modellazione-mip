# Modellazione MIP

Materiale didattico ideato e sviluppato da **[Fabio Furini](https://sites.google.com/view/fabiofurini/home-page)**, professore
associato al [DIAG](https://www.diag.uniroma1.it/), Sapienza Università di Roma.

**Modelli di programmazione lineare intera per l'Ingegneria Gestionale** — la
dispensa del corso in versione online, con codice Python/Gurobi, notebook e
istanze riproducibili.

Un modello con variabili binarie e intere non si *scrive* soltanto: si
*dimostra*. Ogni vincolo che lega due famiglie di variabili impone
un'implicazione logica, e lo studente deve saper provare che la impone davvero
— in entrambi i versi, oppure spiegando perché un verso segue dall'ottimalità.
Poi il modello si *stringe*: un'euristica costruttiva fornisce un upper bound
e una soluzione duale del rilassamento LP fornisce un lower bound, che
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

## Indice completo

**[Modellazione](modellazione.md)**

1. [Che cos'è un modello MIP](modellazione-1.md) — dati, variabili, obiettivo,
   vincoli; rilassamenti, bound e gap
2. [Logica e variabili binarie](modellazione-2.md) — CNF, le tre regole di
   traduzione, cinque esercizi
3. [Legami fra variabili](legami.md) — le quattordici tecniche, una per
   sottopagina, con la [mappa](legami.md)
4. [Rilassamenti, dualità e bound](modellazione-4.md) — la tabella di
   conversione, tre ricette per una soluzione duale a mano
5. [Euristiche costruttive](modellazione-5.md) — le sei regole, quando
   falliscono
6. [Dal modello a Python/Gurobi](modellazione-6.md) — le quattro classi di
   variabili, le tolleranze, il protocollo del corso

**[I problemi](problemi.md)**

*[Quindici modelli numerici](numerici.md)* — da EX 1 a EX 15, con la pagina online per

EX 2 [Linee di autobus](ex-02.md) ·
EX 3 [Staffetta](ex-03.md) ·
EX 6 [Hub-and-spoke](ex-06.md) ·
EX 8 [Seminari](ex-08.md) ·
EX 10 [Utensili CNC](ex-10.md) ·
EX 11 [Bilanciamento](ex-11.md)

*[Assegnamento e scheduling](scheduling.md)*

7.1 [Assegnamento a costo minimo](scheduling-1.md) ·
7.2 [Macchine con costo fisso](scheduling-2.md) ·
7.3 [Selezione di lavori](scheduling-3.md) ·
7.4 [Lavori in parallelo](scheduling-4.md) ·
7.5 [Classi con setup](scheduling-5.md) ·
7.6 [Classi con premio](scheduling-6.md) ·
7.7 [Ritardo totale](scheduling-7.md)

*[Localizzazione e copertura](localizzazione.md)*

8.1 [Localizzazione capacitata](localizzazione-1.md) ·
8.2 [p-mediana](localizzazione-2.md) ·
8.3 [Copertura con interferenza](localizzazione-3.md) ·
8.4 [Hub con costo massimo](localizzazione-4.md)

*[Pianificazione della produzione](produzione.md)*

9.1 [Lotti con costo fisso](produzione-1.md) ·
9.2 [Produzione e manodopera](produzione-2.md) ·
9.3 [Veicoli con lotto minimo](produzione-3.md)

*[Modelli misti](misti.md)*

10.1 [Premi con due modalità](misti-1.md) ·
10.2 [Asta combinatoria](misti-2.md) ·
10.3 [Dieta con lotto minimo](misti-3.md) ·
10.4 [Alberi e scatole di luci](misti-4.md) ·
10.5 [Spedizioni in scatole](misti-5.md) ·
10.6 [Bambini fra campi estivi](misti-6.md) ·
10.7 [Filiali fra due società](misti-7.md) ·
10.8 [Brani fra CD](misti-8.md) ·
10.9 [Libri fra scaffali](misti-9.md)



**Il corso**

- [Organizzazione del corso](organizzazione.md) — il percorso, l'esame, gli
  errori da evitare
- [Notebook in Colab](notebook.md) — uno per problema, si aprono nel browser

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
