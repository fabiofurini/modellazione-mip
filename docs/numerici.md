# Quindici modelli numerici

**Classe:** BIP · ILP · MILP · **Script:** uno per modello,
`python/ex01_furgone.py` … `python/ex15_orario.py`
{ .scheda }

I quindici modelli numerici del corso, da EX 1 a EX 15. Dati espliciti, poche
variabili, una tecnica per modello: sono i più facili, e vengono prima delle
famiglie di problemi e dei problemi misti.

Ogni modello numerico ha sempre le stesse cinque parti:

1. l'enunciato, con i dati dell'istanza;
2. le **variabili**, con il loro dominio e il loro conteggio;
3. il **modello dell'istanza**, primale e duale;
4. una soluzione ammissibile costruita a mano, che dà il bound primale;
5. una soluzione duale costruita a mano, che dà il bound duale, e il confronto
   con l'ottimo del solver.

Ogni modello ha la sua pagina, il suo script e il suo notebook.

| Modello | Che cosa mette in gioco | Notebook |
|---|---|---|
| [EX 1 — Il furgone da otto posti](ex-01.md) | selezione con capacità e un'implicazione fra gruppi | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/ex01_furgone.ipynb) |
| [EX 2 — Linee di autobus](ex-02.md) | assegnamento con capacità in numero di linee | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/ex02_linee.ipynb) |
| [EX 3 — Staffetta](ex-03.md) | assegnamento con più risorse che compiti; matrice totalmente unimodulare | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/ex03_staffetta.ipynb) |
| [EX 4 — Hub-and-spoke](ex-04.md) | copertura: il minimo numero di hub | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/ex04_hub.ipynb) |
| [EX 5 — Fondi acquistabili a lotti](ex-05.md) | conteggi interi a lotti, con un vincolo di proporzione | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/ex05_fondi.ipynb) |
| [EX 6 — Veicoli con quantità minima](ex-06.md) | lotto minimo: una quantità minima se il tipo si produce | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/ex06_veicoli.ipynb) |
| [EX 7 — Aerei su commessa con costo fisso](ex-07.md) | costo fisso di attrezzaggio e quantità libera fino alla richiesta | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/ex07_aerei.ipynb) |
| [EX 8 — Seminari](ex-08.md) | cardinalità esatta, non-adiacenza, duale con variabile libera | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/ex08_seminari.ipynb) |
| [EX 9 — Le regine sulla scacchiera](ex-09.md) | packing su scacchiera: righe, colonne e diagonali | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/ex09_regine.ipynb) |
| [EX 10 — Utensili di una macchina CNC](ex-10.md) | selezione con corredo di utensili: attivazione disaggregata | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/ex10_utensili.ipynb) |
| [EX 11 — Scarpe con soglia minima di produzione](ex-11.md) | lotto minimo con tre risorse condivise | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/ex11_scarpe_soglia.ipynb) |
| [EX 12 — Bilanciamento fra due operai](ex-12.md) | min-max contro differenza: stesse soluzioni, valori diversi | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/ex12_bilanciamento.ipynb) |
| [EX 13 — I turni del pronto soccorso](ex-13.md) | copertura dei fabbisogni giornalieri con turni settimanali | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/ex13_turni.ipynb) |
| [EX 14 — Scarpe: produzione, scorte e assunzioni](ex-14.md) | bilancio delle scorte e organico su tre mesi | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/ex14_scarpe.ipynb) |
| [EX 15 — L'orario della scuola di musica](ex-15.md) | conflitti, non-adiacenza e preferenze da evitare | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/ex15_orario.ipynb) |
