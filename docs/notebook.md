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
| [Assegnamento a costo minimo con disponibilità](scheduling-1.md) | BIP | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/fam07_1_assegnamento.ipynb) |
| [Macchine con costo fisso di utilizzo](scheduling-2.md) | BIP | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/fam07_2_costofisso.ipynb) |
| [Selezione di lavori con ricavo e macchine a costo fisso](scheduling-3.md) | BIP | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/fam07_3_selezione.ipynb) |
| [Lavori in parallelo: il tempo di lavorazione come massimo](scheduling-4.md) | MILP | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/fam07_4_parallelo.ipynb) |
| [Una macchina, classi di lavori con setup](scheduling-5.md) | BIP | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/fam07_5_classisetup.ipynb) |
| [Classi con premio di completamento e riduzione «se e solo se»](scheduling-6.md) | BIP | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/fam07_6_classipremio.ipynb) |
| [Ritardo totale su una macchina: sequenziamento con big-M](scheduling-7.md) | MILP | [![Apri in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fabiofurini/modellazione-mip/blob/main/notebooks/fam07_7_ritardo.ipynb) |

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
