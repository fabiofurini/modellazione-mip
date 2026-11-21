# Assegnamento e scheduling

[:material-file-pdf-box: Dispensa (PDF)](pdf/dispensa-3-simbolici.pdf) · [:material-presentation: Slide (PDF)](pdf/slide-09-scheduling-1.pdf)

**Classe:** BIP / MILP · **Script:** uno script e un notebook per problema
(`python/fam07_1_assegnamento.py` … `fam07_7_ritardo.py`).
{ .scheda }

!!! nota "Prerequisiti"

    - Da questo modulo, [Capitolo 6 «Legami fra variabili»](https://fabiofurini.github.io/modellazione-mip/legami/): attivazione, variabile di massimo, *se e solo se*, big-M e precedenze.

    - Da questo modulo, [Capitolo 2 «Rilassamenti, dualità e bound»](https://fabiofurini.github.io/modellazione-mip/modellazione-2/): il protocollo dei bound e il duale del rilassamento LP.

    - Dal modulo *Problemi di ottimizzazione combinatoria*, la pagina [«Scheduling su macchine parallele identiche ($P\|C_{\max}$)»](https://fabiofurini.github.io/ottimizzazione-combinatoria/catalogo/scheduling-on-identical-parallel-machines/): il problema di scheduling $P\|C_{\max}$ e la regola LPT.

!!! chiave "Obiettivi"

    Alla fine di questo capitolo sarai in grado di:

    - scrivere dal suo enunciato il modello simbolico di un problema di assegnamento o di scheduling;

    - dimostrare i legami fra variabili di macchina, di classe e di assegnamento;

    - modellare il sequenziamento su una macchina con precedenze binarie e un big-M calcolato dai dati;

    - chiudere il sandwich dei bound con un'euristica costruttiva e una soluzione duale costruita a mano.

Sette problemi con lo stesso scheletro: dei **lavori** vanno assegnati a delle
**macchine** con disponibilità limitata. Cambia, di problema in problema, che
cosa si paga e che cosa si decide: il costo dell'assegnamento, il costo fisso di
ogni macchina accesa, il ricavo dei lavori che si scelgono di eseguire, il tempo
di lavorazione quando i lavori vanno in parallelo, il setup di una classe di
lavori, un premio che si incassa *se e solo se* una classe è completa, il
ritardo rispetto alle scadenze quando i lavori si susseguono su una sola macchina.

!!! note "I legami fra variabili che si rivedono qui"
    **Attivazione** (7.2, 7.3, 7.5): la binaria «macchina usata» o «classe
    attivata» che comanda le assegnazioni, con il vincolo aggregato
    $\sum_j t_{jm} x_{jm} \le a_m y_m$ o disaggregato $x_j \le y_c$.
    **Variabile di massimo** (7.4): $y_m \ge t_{jm} x_{jm}$ per ogni lavoro,
    che all'ottimo vale esattamente il massimo. **Se e solo se** (7.6): un
    verso lo impone il vincolo, l'altro l'obiettivo. **Big-M e disgiunzioni**
    (7.7): «o $j$ prima di $i$ o $i$ prima di $j$», con $M$ pari alla somma dei
    tempi.

## Notazione della famiglia

| Simbolo | Tipo | Significato |
|---|---|---|
| $n$ | $\in \mathbb{Z}_{\ge 1}$ | numero di lavori, $j \in \{1, 2, \dots, n\}$ |
| $k$ | $\in \mathbb{Z}_{\ge 1}$ | numero di macchine, $m \in \{1, 2, \dots, k\}$ |
| $t_{jm}$ | $\in \mathbb{Q}_{>0}$ | tempo di lavorazione (minuti) del lavoro $j$ sulla macchina $m$; $t_j$ se non dipende dalla macchina |
| $c_{jm}$ | $\in \mathbb{Q}_{>0}$ | costo (euro) di eseguire il lavoro $j$ sulla macchina $m$ |
| $c_m$ | $\in \mathbb{Q}_{>0}$ | costo fisso (euro) se la macchina $m$ viene usata |
| $a_m$ | $\in \mathbb{Q}_{>0}$ | disponibilità (minuti) della macchina $m$; $a$ se la macchina è una sola |
| $p_m$ | $\in \mathbb{Z}_{\ge 1}$ | numero massimo di lavori che la macchina $m$ può eseguire |
| $r_j$ | $\in \mathbb{Q}_{>0}$ | ricavo (euro) se il lavoro $j$ viene eseguito |
| $d_j$ | $\in \mathbb{Q}_{>0}$ | scadenza (minuti) del lavoro $j$ |
| $q$ | $\in \mathbb{Z}_{\ge 2}$ | numero di classi di lavori, $c \in \{1, 2, \dots, q\}$ |
| $\mathscr{J}_c$ | $\subseteq \{1, 2, \dots, n\}$ | lavori della classe $c$; le classi partizionano i lavori |
| $f_c,\ s_c$ | $\in \mathbb{Q}_{\ge 0}$ | costo (euro) e tempo (minuti) di setup della classe $c$ |
| $v_c$ | $\in \mathbb{Q}_{>0}$ | premio (euro) se tutti i lavori della classe $c$ sono eseguiti |
| $u$ | $\in \mathbb{Q}_{>0}$ | riduzione (minuti) della disponibilità se si eseguono lavori di almeno due classi |

## I sette problemi

<div class="grid cards" markdown>

-   **7.1 Assegnamento a costo minimo**

    ---

    Ogni lavoro su una macchina, disponibilità rispettata, costo minimo: il
    problema di assegnamento generalizzato. Una sola famiglia di variabili.

    [:octicons-arrow-right-24: BIP](scheduling-1.md)

-   **7.2 Macchine con costo fisso**

    ---

    Si paga la macchina accesa, non l'assegnamento: nascono le variabili di
    attivazione e il primo legame da dimostrare.

    [:octicons-arrow-right-24: BIP · attivazione](scheduling-2.md)

-   **7.3 Selezione di lavori**

    ---

    I lavori hanno un ricavo e non sono obbligatori: un problema di massimo, in
    cui euristica e duale si scambiano i ruoli.

    [:octicons-arrow-right-24: BIP · attivazione](scheduling-3.md)

-   **7.4 Lavori in parallelo**

    ---

    Il tempo di una macchina è il massimo dei tempi dei suoi lavori: la
    variabile «massimo» e la sua caratterizzazione in tre passi.

    [:octicons-arrow-right-24: MILP · massimo](scheduling-4.md)

-   **7.5 Classi con setup**

    ---

    Uno zaino con costi e tempi fissi per gruppo: l'attivazione disaggregata,
    dedotta dalla CNF di un'implicazione booleana.

    [:octicons-arrow-right-24: BIP · attivazione, CNF](scheduling-5.md)

-   **7.6 Classi con premio**

    ---

    Un premio se la classe è completa, una penalità se si mescolano classi: due
    «se e solo se», ognuno imposto per metà dai vincoli e per metà dall'ottimo.

    [:octicons-arrow-right-24: BIP · se e solo se](scheduling-6.md)

-   **7.7 Ritardo totale**

    ---

    Una sola macchina, una sequenza: precedenze binarie, completamenti, ritardi
    e il big-M che «spegne» un vincolo.

    [:octicons-arrow-right-24: MILP · big-M](scheduling-7.md)

</div>

## In sintesi

!!! chiave "In sintesi"

    - I sette problemi hanno lo stesso scheletro: lavori assegnati a macchine con disponibilità limitata.

    - Cambia che cosa si paga e che cosa si decide: costo di assegnamento, costo fisso, ricavo, tempo in parallelo, setup, premio, ritardo.

    - I legami che tornano: attivazione, variabile di massimo, *se e solo se* e big-M con le disgiunzioni.

    - Per ogni problema: modello, dimostrazione dei legami, istanza, euristica, soluzione duale a mano e confronto con il solver.
