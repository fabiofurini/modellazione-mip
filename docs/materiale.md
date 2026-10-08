# Materiale scaricabile

Tutto il materiale del corso, in PDF, aggiornato a ogni pubblicazione del sito.
Testi, figure e dati sono sotto licenza
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.it); gli script
Python sotto licenza
[MIT](https://github.com/fabiofurini/modellazione-mip/blob/main/LICENSE-CODE).

## Le tre dispense

Se vuoi il corso intero da leggere offline, parti da questi tre PDF: sono il
cuore del materiale. Quello che viene dopo e' di contorno.

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

<!-- slide:inizio -->
## Le slide

Le slide delle lezioni, una per capitolo delle dispense (PDF).

<div class="grid cards" markdown>

-   :material-presentation: **Modellazione**

    ---

    - [Che cos'è un modello MIP](pdf/slide-01-modelli-mip.pdf)
    - [Rilassamenti, dualità e bound](pdf/slide-02-bound-duali.pdf)
    - [Dal modello a Python/Gurobi](pdf/slide-03-gurobi.pdf)
    - [Logica e variabili binarie](pdf/slide-05-logica-binarie.pdf)
    - [Legami fra variabili](pdf/slide-06-legami.pdf)

-   :material-presentation: **Problemi numerici**

    ---

    - [Modelli numerici: EX 1–5](pdf/slide-07-modelli-numerici-1.pdf)
    - [Modelli numerici: EX 6–10](pdf/slide-07-modelli-numerici-2.pdf)
    - [Modelli numerici: EX 11–15](pdf/slide-07-modelli-numerici-3.pdf)

-   :material-presentation: **Problemi con modello simbolico**

    ---

    - [Le famiglie di problemi](pdf/slide-08-famiglie.pdf)
    - [Localizzazione e copertura](pdf/slide-10-localizzazione.pdf)
    - [Pianificazione della produzione](pdf/slide-11-produzione.pdf)

</div>

<!-- slide:fine -->

## Gli altri documenti

<div class="grid cards" markdown>

-   :material-school-outline: **Come si lavora con il corso**

    ---

    Come è fatto il corso, come è fatto ogni esercizio e come è fatto l'esame:
    il percorso, i criteri di valutazione, le domande tipiche di discussione,
    gli errori più comuni e la riproducibilità dei numeri.

    [:octicons-download-24: organizzazione-del-corso.pdf](pdf/organizzazione-del-corso.pdf)

-   :material-help-circle-outline: **Problemi da modellare**

    ---

    *Per esercitarsi — soluzioni riservate ai docenti.*

    Quaranta problemi dati come arrivano davvero, senza il modello già scritto:
    venti con i dati numerici espliciti e venti in forma simbolica.

    [:octicons-download-24: esercizi.pdf](pdf/esercizi.pdf)


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

## La licenza di Gurobi

```bash
python3 -m pip install gurobipy
```

Il pacchetto pip include una **licenza dimostrativa** (fino a 2000 variabili e
2000 vincoli): basta per tutte le istanze di questo corso. All'avvio compare la
riga `Restricted license - for non-production use only`: è normale.

**Licenza accademica completa, gratuita:**

1. registrarsi su <https://portal.gurobi.com> con l'email istituzionale;
2. richiedere una *Named-User Academic License*;
3. eseguire il comando `grbgetkey XXXXXXXX-...` mostrato dal portale (serve la
   rete di ateneo o la VPN);
4. la licenza finisce in `~/gurobi.lic` e da quel momento non ci sono limiti di
   dimensione.
