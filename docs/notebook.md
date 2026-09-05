# I notebook del corso

Ogni capitolo con dei modelli ha il suo **notebook**: si apre in Google Colab con
un clic sul badge, installa il solver da sé e gira nel browser — sul computer non
serve installare niente. È lo stesso codice degli script di `python/`, cella per
cella, con le figure che compaiono sotto le celle invece di finire in un file.

!!! tip "La licenza del pacchetto pip basta"
    La licenza inclusa in `gurobipy` è limitata a 2000 variabili e 2000 vincoli:
    le istanze del corso sono piccole e ci stanno tutte con ampio margine. Per
    istanze più grandi si attiva la licenza accademica gratuita da
    [portal.gurobi.com](https://portal.gurobi.com).

| Capitolo | Classe | Notebook |
|---|---|---|
| [Che cos'è un modello MIP](modellazione-1.md) | LP | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/cap01_modelli.ipynb) |
| [Logica e variabili binarie](modellazione-2.md) | BIP | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/cap02_logica.ipynb) |
| [Legami fra variabili](legami.md) | tecniche di modellazione | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/cap03_legami.ipynb) |
| [Rilassamenti, dualità e bound](modellazione-4.md) | LP | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/cap04_bound.ipynb) |
| [Euristiche costruttive](modellazione-5.md) | algoritmi | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/cap05_euristiche.ipynb) |
| [Dal modello a Python/Gurobi](modellazione-6.md) | implementazione | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/cap06_gurobi.ipynb) |
| [Assegnamento a costo minimo con disponibilità](scheduling-1.md) | BIP | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/fam07_1_assegnamento.ipynb) |
| [Macchine con costo fisso di utilizzo](scheduling-2.md) | BIP | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/fam07_2_costofisso.ipynb) |
| [Selezione di lavori con ricavo e macchine a costo fisso](scheduling-3.md) | BIP | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/fam07_3_selezione.ipynb) |
| [Lavori in parallelo: il tempo di lavorazione come massimo](scheduling-4.md) | MILP | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/fam07_4_parallelo.ipynb) |
| [Una macchina, classi di lavori con setup](scheduling-5.md) | BIP | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/fam07_5_classisetup.ipynb) |
| [Classi con premio di completamento e riduzione «se e solo se»](scheduling-6.md) | BIP | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/fam07_6_classipremio.ipynb) |
| [Ritardo totale su una macchina: sequenziamento con big-M](scheduling-7.md) | MILP | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/fam07_7_ritardo.ipynb) |
| [Localizzazione capacitata](localizzazione-1.md) | MILP | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/fam08_1_capacitata.ipynb) |
| [p-mediana: al più $k$ sedi](localizzazione-2.md) | BIP | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/fam08_2_pmediana.ipynb) |
| [Copertura del segnale con interferenza](localizzazione-3.md) | BIP | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/fam08_3_copertura.ipynb) |
| [Localizzazione di hub con costo massimo](localizzazione-4.md) | MILP | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/fam08_4_hub.ipynb) |
| [Lotti con costo fisso di lancio](produzione-1.md) | MILP | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/fam09_1_lotti.ipynb) |
| [Produzione e manodopera: due formulazioni equivalenti](produzione-2.md) | MILP | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/fam09_2_manodopera.ipynb) |
| [Veicoli: lotto minimo e premio per la varietà](produzione-3.md) | MILP | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/fam09_3_veicoli.ipynb) |
| [Premi acquistabili con due modalità](misti-1.md) | BIP | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/fam10_1_premi.ipynb) |
| [Asta combinatoria](misti-2.md) | BIP | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/fam10_2_asta.ipynb) |
| [Dieta con conteggio dei cibi e lotto minimo](misti-3.md) | MILP | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/fam10_3_dieta.ipynb) |
| [Alberi di Natale e scatole di luci](misti-4.md) | MILP | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/fam10_4_luci.ipynb) |
| [Spedizioni in scatole](misti-5.md) | MILP | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/fam10_5_spedizioni.ipynb) |
| [Bambini fra campi estivi](misti-6.md) | ILP | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/fam10_6_campi.ipynb) |
| [Filiali fra due società](misti-7.md) | BIP | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/fam10_7_antitrust.ipynb) |
| [Brani fra CD](misti-8.md) | MILP | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/fam10_8_cd.ipynb) |
| [Libri fra scaffali](misti-9.md) | MILP | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/fam10_9_scaffali.ipynb) |

## I quindici modelli numerici

Uno per modello, da EX 1 a EX 15 — l'elenco completo è nella pagina
[Quindici modelli numerici](numerici.md).

| Modello | Classe | Notebook |
|---|---|---|
| EX 1 — Il furgone da otto posti | BIP | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/ex01_furgone.ipynb) |
| [EX 2 — Linee di autobus](ex-02.md) | BIP | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/ex02_linee.ipynb) |
| [EX 3 — Staffetta](ex-03.md) | BIP | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/ex03_staffetta.ipynb) |
| EX 4 — Scarpe: produzione, scorte e assunzioni | MILP | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/ex04_scarpe.ipynb) |
| EX 5 — Veicoli con quantità minima | ILP | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/ex05_veicoli.ipynb) |
| [EX 6 — Hub-and-spoke](ex-06.md) | BIP | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/ex06_hub.ipynb) |
| EX 7 — Aerei su commessa con costo fisso | ILP | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/ex07_aerei.ipynb) |
| [EX 8 — Seminari](ex-08.md) | BIP | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/ex08_seminari.ipynb) |
| EX 9 — Le otto regine | BIP | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/ex09_regine.ipynb) |
| [EX 10 — Utensili di una macchina CNC](ex-10.md) | BIP | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/ex10_utensili.ipynb) |
| [EX 11 — Bilanciamento fra due operai](ex-11.md) | MILP | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/ex11_bilanciamento.ipynb) |
| EX 12 — Scarpe con soglia minima di produzione | ILP | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/ex12_scarpe_soglia.ipynb) |
| EX 13 — Fondi acquistabili a lotti | ILP | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/ex13_fondi.ipynb) |
| EX 14 — I turni del pronto soccorso | ILP | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/ex14_turni.ipynb) |
| EX 15 — L'orario della scuola di musica | BIP | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/ex15_orario.ipynb) |

## Come sono fatti

I notebook non si scrivono a mano: si generano dagli script con

```bash
python3 python/genera_notebook.py
```

Lo script del capitolo resta l'unica sorgente del codice — il notebook ne riprende
docstring, sezioni e commenti — e chi preferisce la riga di comando continua a
lanciare, dalla cartella `python/`:

```bash
python3 fam07_1_assegnamento.py
```
