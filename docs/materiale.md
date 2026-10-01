# Materiale scaricabile

Tutto il materiale del corso, in PDF, aggiornato a ogni pubblicazione del sito.
Testi, figure e dati sono sotto licenza
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.it); gli script
Python sotto licenza
[MIT](https://github.com/fabiofurini/modellazione-mip/blob/main/LICENSE-CODE).

<div class="grid cards" markdown>

-   :material-book-open-variant: **La dispensa**

    ---

    Il corso per intero: i sei capitoli di modellazione, i quindici modelli
    numerici, le quattro famiglie di problemi con euristiche, duali e domande
    aggiuntive, e l'organizzazione del corso.

    [:octicons-download-24: dispensa-mip.pdf](pdf/dispensa-mip.pdf)

-   :material-file-document-edit: **La raccolta degli enunciati**

    ---

    Gli stessi problemi, nello stesso ordine, con i soli testi: per esercitarsi
    prima di leggere la soluzione. Quarantasette enunciati.

    [:octicons-download-24: raccolta-enunciati.pdf](pdf/raccolta-enunciati.pdf)

-   :material-presentation: **Le slide del corso**

    ---

    Il percorso in quarantatré slide: il metodo, i quattordici legami, il
    sandwich dei bound, le quattro famiglie, il formato dell'esame.

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
