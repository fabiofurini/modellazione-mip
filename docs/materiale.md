# Materiale scaricabile

Tutto il materiale del corso, in PDF, aggiornato a ogni pubblicazione del sito.
Testi, figure e dati sono sotto licenza
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.it); gli script
Python sotto licenza
[MIT](https://github.com/fabiofurini/modellazione-mip/blob/main/LICENSE-CODE).

## Le tre dispense

<div class="grid cards" markdown>

-   :material-book-open-variant: **Modellazione**

    ---

    La parte metodologica: che cos'è un modello MIP, logica e variabili binarie,
    i quattordici legami fra variabili con le loro dimostrazioni, rilassamenti,
    dualità e bound, euristiche costruttive, e il passaggio a Python/Gurobi.

    [:octicons-download-24: dispensa-1-modellazione.pdf](pdf/dispensa-1-modellazione.pdf)

-   :material-numeric: **Problemi numerici**

    ---

    I quindici modelli numerici, dall'EX 1 all'EX 15: dati espliciti, poche
    variabili, un solo passaggio per tecnica. Si leggono per prendere le misure
    prima dei problemi generali.

    [:octicons-download-24: dispensa-2-numerici.pdf](pdf/dispensa-2-numerici.pdf)

-   :material-function-variant: **Problemi con modello simbolico**

    ---

    I ventitré problemi delle tre famiglie e dei problemi misti: enunciato, modello simbolico,
    istanza, euristica, duale del rilassamento, ottimo, domande aggiuntive e una
    variante svolta per intero.

    [:octicons-download-24: dispensa-3-simbolici.pdf](pdf/dispensa-3-simbolici.pdf)

</div>

## Gli altri documenti

<div class="grid cards" markdown>

-   :material-school-outline: **Organizzazione del corso**

    ---

    Come è fatto il corso, come è fatto ogni esercizio e come è fatto l'esame:
    il percorso, i criteri di valutazione, le domande tipiche di discussione,
    gli errori più comuni e la riproducibilità dei numeri.

    [:octicons-download-24: organizzazione-del-corso.pdf](pdf/organizzazione-del-corso.pdf)

-   :material-help-circle-outline: **Problemi da modellare**

    ---

    Quaranta problemi dati come arrivano davvero, senza il modello già scritto:
    venti con i dati numerici espliciti e venti in forma simbolica. Le soluzioni
    sono riservate ai docenti.

    [:octicons-download-24: esercizi.pdf](pdf/esercizi.pdf)

-   :material-presentation: **Le slide del corso**

    ---

    Il percorso in quarantatré slide: il metodo, i quattordici legami, il
    sandwich dei bound, le tre famiglie e i problemi misti, il formato dell'esame.

    [:octicons-download-24: slide-mip.pdf](pdf/slide-mip.pdf)

-   :material-language-python: **Il codice**

    ---

    Uno script per modello, i notebook generati, i dati in CSV. Tutto si rigenera
    con un comando e ogni numero è verificato da un `assert`.

    [:octicons-mark-github-16: modellazione-mip](https://github.com/fabiofurini/modellazione-mip)

</div>

## Rigenerare tutto

```bash
python3 -m pip install gurobipy pandas matplotlib mkdocs-material
python3 python/esegui_tutti.py       # dati, figure, modelli e notebook
python3 python/verifica_numeri.py    # ogni numero citato nei testi
python3 -m mkdocs build --strict     # il sito
```

La licenza inclusa nel pacchetto pip di `gurobipy` (2000 variabili, 2000
vincoli) basta per tutte le istanze del corso.
