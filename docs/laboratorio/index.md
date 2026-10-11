---
hide:
  - navigation
---

# Laboratorio interattivo

Le idee del corso da toccare con mano: rilassamenti, bound, euristiche e formulazioni.
Scegli un'app: si apre a tutta pagina. Tutto gira nel browser, senza Gurobi;
i problemi sono piccoli, così ogni passo si vede.

## 2. Rilassamenti, dualità e bound

<div class="grid cards" markdown>

-   :material-dots-grid: **Punti interi e rilassamento**

    ---

    I punti interi dentro il poliedro, l'ottimo del rilassamento continuo e l'ottimo intero: muovi i vincoli e la funzione obiettivo e guarda quanto è largo il divario fra i due.

    [Apri l'app →](punti-interi.md)

</div>

## 4. Euristiche costruttive

<div class="grid cards" markdown>

-   :material-bag-personal: **Zaino: euristica per rapporto contro ottimo**

    ---

    L'euristica costruttiva per rapporto riempie lo zaino in ordine di valore/peso: seguila oggetto per oggetto e confronta il suo valore con l'ottimo e con il bound del rilassamento continuo.

    [Apri l'app →](zaino-greedy.md)

-   :material-map-marker-path: **TSP: nearest neighbour contro giro ottimo**

    ---

    Il giro del nearest neighbour si costruisce passo passo, poi il 2-opt lo migliora: si confronta con il giro ottimo, con la lunghezza di entrambi.

    [Apri l'app →](tsp-euristiche.md)

-   :material-package-variant-closed: **Bin packing e scheduling**

    ---

    Next Fit, First Fit, Best Fit e First Fit Decreasing riempiono i contenitori, List scheduling e LPT assegnano i lavori alle macchine: passo passo, con il bound inferiore accanto alla soluzione e l'ottimo alla fine.

    [Apri l'app →](bin-packing-scheduling.md)

</div>

## 5. Logica e variabili binarie

<div class="grid cards" markdown>

-   :material-alpha-m-box: **Big-M e rilassamento**

    ---

    Un vincolo condizionato scritto con il big-M: sposta \(M\) con il cursore e guarda il rilassamento continuo allargarsi quando \(M\) supera il minimo, e l'insieme del MILP perdere pezzi quando è troppo piccolo.

    [Apri l'app →](big-m.md)

</div>

## 6. Legami fra variabili

<div class="grid cards" markdown>

-   :material-vector-polygon-variant: **Formulazioni deboli e forti**

    ---

    Due formulazioni con gli stessi punti interi, sovrapposte: quanto si avvicina ciascuna all'involucro convesso, e che cosa cambia nel bound del rilassamento.

    [Apri l'app →](formulazioni.md)

</div>
