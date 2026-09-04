<h3 align="center">Materiale didattico di
<a href="https://sites.google.com/view/fabiofurini/home-page">Fabio Furini</a></h3>
<p align="center">
  Professore associato di Ricerca Operativa ·
  <a href="https://www.diag.uniroma1.it/">DIAG</a>, Sapienza Università di Roma ·
  <a href="https://sites.google.com/view/fabiofurini/home-page">sito personale</a>
</p>

# Modellazione MIP

> **L'autore.** Fabio Furini è professore associato al DIAG della Sapienza dal
> settembre 2021. Dottorato in Automatica e Ricerca Operativa all'Università di
> Bologna (2011) e assegno di ricerca fino al 2012; postdoc all'Université
> Paris-13 (2012–2013); dal 2013 al 2019 *Maître de Conférences* all'Université
> Paris-Dauphine. *Habilitation à Diriger des Recherches* in Francia nel 2017 e
> Abilitazione Scientifica Nazionale a professore ordinario in Ricerca Operativa
> nel 2019. Nel 2020 ricercatore CNR presso l'IASI-CNR di Roma.
> Sito personale: <https://sites.google.com/view/fabiofurini/home-page>

Modelli di programmazione lineare intera per l'Ingegneria Gestionale — come si
costruisce un modello con variabili binarie e intere, come si *dimostra* che fa
quello che deve, come lo si stringe fra un'euristica e un bound duale (gli
stessi bound a cui ricorre un solver reale quando non riesce a raggiungere
l'ottimo provato), come lo si risolve con Gurobi. Secondo corso della serie iniziata con il
[Laboratorio di Ricerca Operativa](https://fabiofurini.github.io/laboratorio-ricerca-operativa/).

**📖 Dispensa online: [fabiofurini.github.io/modellazione-mip](https://fabiofurini.github.io/modellazione-mip/)**

**▶️ Notebook eseguibili in Colab: [l'elenco dei capitoli](https://fabiofurini.github.io/modellazione-mip/notebook/)** — girano nel browser, senza installare niente.

## Eseguire i modelli

Ogni capitolo ha il suo script in [`python/`](python/), con i dati in [`dati/`](dati/):

```bash
python3 -m pip install gurobipy matplotlib pandas
python3 python/esegui_tutti.py     # tutti i modelli: dati, risultati, figure e notebook
```

La licenza `gurobipy` inclusa nel pacchetto pip basta per tutte le istanze del corso;
la licenza accademica gratuita si attiva da [portal.gurobi.com](https://portal.gurobi.com).

## Licenza

- **Testi, figure e dati** (`docs/`, `dati/`): [CC BY 4.0](LICENSE).
- **Codice Python** (`python/`): [MIT](LICENSE-CODE).

Per citare il materiale c'è [`CITATION.cff`](CITATION.cff).

## English version

The whole course is also available in English:
**[fabiofurini.github.io/mip-modelling](https://fabiofurini.github.io/mip-modelling/)**
([repository](https://github.com/fabiofurini/mip-modelling)).

---

Materiale didattico di **[Fabio Furini](https://sites.google.com/view/fabiofurini/home-page)** — [DIAG](https://www.diag.uniroma1.it/), Sapienza Università di Roma.
