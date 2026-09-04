# Organizzazione del corso

## Percorso in tre parti

| | Contenuto | Obiettivi di apprendimento |
|---|---|---|
| **Parte I** | Modellazione | riconoscere un legame fra variabili (attivazione, massimo, big-M, se e solo se…) e dimostrare che il modello lo impone davvero |
| **Parte II** | I problemi | applicare i legami a sei famiglie di problemi reali, dal modello al codice Gurobi |
| **Parte III** | Il corso | mettere alla prova quanto imparato con le domande di modellazione aggiuntive |

## Il formato di ogni esercizio (e dell'esame)

Ogni problema del corso — e ogni domanda d'esame — segue lo stesso schema in
quattro quesiti:

1. **Modello.** Scrivere il MILP: variabili (con il conteggio), obiettivo,
   vincoli con la loro descrizione, e — se ci sono due famiglie di variabili
   collegate — spiegare il legame: qual è l'implicazione, e come il vincolo
   (o l'ottimo) la impone, nei due versi.
2. **Istanza.** Scrivere il modello per un'istanza numerica piccola.
3. **Euristica.** Progettare un algoritmo costruttivo che trovi una soluzione
   ammissibile dell'istanza, ed eseguirlo passo per passo per ottenere un
   upper bound (lower bound se il problema è di massimo).
4. **Duale.** Scrivere il duale del rilassamento LP, per il modello generale e
   per l'istanza, e costruire a mano una soluzione duale ammissibile per
   ottenere il bound dal lato opposto.

Il `lb ≤ z(MILP) ≤ ub` che ne risulta è il filo conduttore del corso: un
modello non si limita a scriverlo, lo si stringe da entrambi i lati prima di
affidarlo al solver — ed è esattamente ciò a cui si ricorre quando un MILP
reale non si riesce a risolvere all'ottimo provato in tempo utile: l'euristica
e il bound duale sono il certificato di qualità che una run del solver
interrotta a metà non può fornire da sola.

## Criteri di valutazione

| Dimensione | Peso |
|---|---|
| Correttezza del modello (variabili, obiettivo, vincoli) | 35% |
| Dimostrazione del legame fra le variabili (nei due versi) | 25% |
| Euristica costruttiva ed esecuzione corretta | 20% |
| Duale del rilassamento e soluzione duale ammissibile | 20% |

## Domande tipiche di discussione

- Il vincolo di link è aggregato o disaggregato? Che differenza fa sul
  rilassamento LP?
- Il verso opposto dell'implicazione è imposto dal vincolo o segue
  dall'ottimo? Come lo si dimostra?
- Qual è il big-M più piccolo che si può giustificare dai dati?
- L'euristica trova l'ottimo? Come si fa a saperlo senza il solver?
- Il duale a mano è ottimo per il rilassamento, o solo ammissibile?

## Gli errori più comuni

1. Scrivere un'implicazione la cui tesi è vera comunque (controinversa
   vacua): prima di scriverla, verificare che antecedente e conseguente siano
   entrambi genuini.
2. Dimostrare un solo verso di un'implicazione «imposta dal vincolo» — servono
   sempre entrambi gli "if".
3. Confondere una relazione «imposta dal vincolo» con una che «segue
   dall'ottimo»: la seconda richiede l'argomento di scambio in sei passi, non
   basta dire «si vede che conviene».
4. Concludere «in ogni soluzione ottima» quando il coefficiente è solo
   $\ge 0$ (non $> 0$): la conclusione corretta è più debole, «esiste un
   ottimo in cui…».
5. Usare un big-M enorme «per sicurezza»: peggiora il rilassamento LP senza
   bisogno.
6. Dimenticare che un vincolo di mutua esclusione ($A + B \le 1$) non implica
   che almeno uno dei due valga 1.
7. Scrivere il duale del rilassamento sbagliando il verso o il segno di una
   variabile duale rispetto al verso del vincolo primale.
8. Costruire una soluzione duale ammissibile ma non verificarne
   l'ammissibilità su tutti i vincoli.

## Riproducibilità

```bash
python3 -m pip install gurobipy matplotlib pandas
python3 python/esegui_tutti.py       # rigenera dati, risultati, figure e notebook
python3 python/verifica_numeri.py    # verifica ogni numero citato nella dispensa
```
