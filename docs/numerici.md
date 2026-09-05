# Quindici modelli numerici

**Classe:** BIP · ILP · MILP · **Script:** uno per modello,
`python/ex01_furgone.py` … `python/ex15_orario.py`

I quindici modelli numerici del corso, da EX 1 a EX 15. Sono gli esempi più
facili: dati espliciti, poche variabili, un solo passaggio per ciascuna tecnica.
Vengono prima delle famiglie di problemi proprio per questo — si leggono per
prendere le misure, e poi si affrontano i problemi generali.

Il formato è ridotto ma conserva sempre gli stessi cinque pezzi:

1. l'enunciato, con i dati dell'istanza;
2. il **modello simbolico**, con le sue variabili e i suoi vincoli;
3. il **modello dell'istanza**, primale e duale;
4. una soluzione ammissibile costruita a mano, che dà il bound primale;
5. una soluzione duale costruita a mano, che dà il bound duale, e il confronto
   con l'ottimo del solver.

Ogni modello ha il suo script e il suo notebook. Sei modelli hanno anche la
pagina online, linkata qui sotto; per gli altri il testo completo è nella
dispensa in PDF, e il codice gira in Colab.

| Modello | Che cosa mette in gioco | $z(\mathit{MILP})$ | Notebook |
|---|---|---:|---|
| EX 1 — Il furgone da otto posti | selezione con capacità e un'implicazione fra gruppi | 120 | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/ex01_furgone.ipynb) |
| [EX 2 — Linee di autobus](ex-02.md) | assegnamento con capacità in numero di linee | 9 | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/ex02_linee.ipynb) |
| [EX 3 — Staffetta](ex-03.md) | assegnamento con più risorse che compiti; matrice totalmente unimodulare | 95 | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/ex03_staffetta.ipynb) |
| EX 4 — Scarpe: produzione, scorte e assunzioni | bilancio delle scorte e organico su tre mesi | 774 180 | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/ex04_scarpe.ipynb) |
| EX 5 — Veicoli con quantità minima | lotto minimo: una quantità minima se il tipo si produce | 25 250 | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/ex05_veicoli.ipynb) |
| [EX 6 — Hub-and-spoke](ex-06.md) | copertura: il minimo numero di hub | 3 | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/ex06_hub.ipynb) |
| EX 7 — Aerei su commessa con costo fisso | costo fisso di attrezzaggio e quantità libera fino alla richiesta | 5 | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/ex07_aerei.ipynb) |
| [EX 8 — Seminari](ex-08.md) | cardinalità esatta, non-adiacenza, duale con variabile libera | 18 | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/ex08_seminari.ipynb) |
| EX 9 — Le otto regine | packing su scacchiera: righe, colonne e diagonali | 8 | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/ex09_regine.ipynb) |
| [EX 10 — Utensili di una macchina CNC](ex-10.md) | selezione con corredo di utensili: attivazione disaggregata | 2 500 | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/ex10_utensili.ipynb) |
| [EX 11 — Bilanciamento fra due operai](ex-11.md) | min-max contro differenza: stesse soluzioni, valori diversi | 9 | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/ex11_bilanciamento.ipynb) |
| EX 12 — Scarpe con soglia minima di produzione | lotto minimo con tre risorse condivise | 24 000 | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/ex12_scarpe_soglia.ipynb) |
| EX 13 — Fondi acquistabili a lotti | conteggi interi a lotti, con un vincolo di proporzione | 16 | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/ex13_fondi.ipynb) |
| EX 14 — I turni del pronto soccorso | copertura dei fabbisogni giornalieri con turni settimanali | 7 060 | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/ex14_turni.ipynb) |
| EX 15 — L'orario della scuola di musica | conflitti, non-adiacenza e preferenze da evitare | 0 | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/ex15_orario.ipynb) |
