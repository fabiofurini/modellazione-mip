# 3. Dal modello a Python/Gurobi

[:material-file-pdf-box: Dispensa (PDF)](pdf/dispensa-1-modellazione.pdf) · [:material-presentation: Slide (PDF)](pdf/slide-03-gurobi.pdf)

**Classe:** implementazione · **Script:** `python/cap06_gurobi.py`
{ .scheda }

[![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/cap06_gurobi.ipynb)

Il corso usa **un solo solver**, Gurobi da Python. Il capitolo mostra come si
**scrive** un modello — una famiglia di vincoli per blocco, con i nomi del
modello matematico — come si **leggono** i risultati, incluso il caso in cui il
solver non ha finito, e tre **modelli completi** che il
[capitolo delle euristiche](modellazione-4.md) riprende.

Ogni numero di queste pagine esce da un unico script,
`python/cap06_gurobi.py`, e il capitolo è diviso in cinque sezioni.

<div class="grid cards" markdown>

-   :material-pencil-ruler: **3.1 Scrivere un modello in gurobipy**

    ---

    Le istruzioni di base di gurobipy, le quattro classi di variabili e la regola del
    corso: una famiglia di vincoli per blocco.

    [:octicons-arrow-right-24: La sezione](gurobipy-1.md)

-   :material-magnify: **3.2 Leggere i risultati**

    ---

    `Status`, `SolCount`, `ObjVal`, `ObjBound`, `MIPGap`, `NodeCount`, e i tre casi
    in cui `ObjVal` non si può leggere.

    [:octicons-arrow-right-24: La sezione](gurobipy-2.md)

-   :material-tune: **3.3 Tolleranze e rilassamenti**

    ---

    «Intero» entro `IntFeasTol`, e `relax()` per ottenere il rilassamento del
    modello appena scritto.

    [:octicons-arrow-right-24: La sezione](gurobipy-3.md)

-   :material-cube-outline: **3.4 Tre modelli classici**

    ---

    Bin packing, makespan e commesso viaggiatore, dall'enunciato all'istanza: i tre
    problemi che le euristiche riprendono.

    [:octicons-arrow-right-24: La sezione](gurobipy-4.md)

-   :material-play-circle: **3.5 Il protocollo, e come si esegue**

    ---

    La sequenza che ogni problema ripete, dai dati alla tabella dei bound, e come si
    fa girare lo script.

    [:octicons-arrow-right-24: La sezione](gurobipy-5.md)

</div>
