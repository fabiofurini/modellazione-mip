# Come si lavora con il corso

Il percorso è in due parti: prima si imparano gli strumenti di modellazione,
poi li si applica a problemi completi. Il filo che le tiene insieme è uno solo —
un modello non si limita a scriverlo: se ne racchiude l'ottimo fra due numeri,
$\mathit{LB} \le z(\mathit{MILP}) \le \mathit{UB}$, prima ancora di affidarlo
al solver.

## Percorso in due parti

| | Contenuto | Obiettivi di apprendimento |
|---|---|---|
| **Parte I** | Modellazione | riconoscere un legame fra variabili (attivazione, massimo, big-M, se e solo se…) e dimostrare che il modello lo impone davvero |
| **Parte II** | I problemi | applicare i legami a tre famiglie di problemi reali e ai problemi misti, dal modello al codice Gurobi |

## Il formato di ogni esercizio

Ogni problema del corso segue lo stesso schema in
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

Il `lb ≤ z(\mathit{MILP}) ≤ ub` che ne risulta è il filo conduttore del corso: un
modello non si limita a scriverlo: se ne racchiude l'ottimo fra due numeri prima di
affidarlo al solver. Un solver interrotto a metà, del resto, un certificato lo
fornisce eccome — l'incumbent `ObjVal` e il bound `ObjBound` racchiudono
l'ottimo in un intervallo, e il `MIPGap` ne misura l'ampiezza. Il punto
didattico è un altro: **saper costruire quei due numeri a mano** serve a capire
da dove vengono, a giudicare se l'intervallo che il solver riporta è stretto
perché il modello è buono o largo perché è formulato male, e a produrre un bound
anche quando il solver non arriva a nulla di utile.

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

Nessun numero di queste pagine è scritto a mano: escono tutti da uno script che
si può rilanciare, e un controllo automatico verifica che testo e codice dicano
la stessa cosa. I comandi stanno nella pagina del
[materiale scaricabile](materiale.md#rigenerare-tutto).
