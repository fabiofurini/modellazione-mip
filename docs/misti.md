# Modelli misti

**Classe:** BIP / MILP · **Script:** uno script e un notebook per problema
(`python/fam10_1_premi.py` … `fam10_9_scaffali.py`).

Le tre famiglie precedenti hanno una struttura riconoscibile: si assegna, si
localizza, si pianifica. I nove problemi di questo capitolo non ce l'hanno, e
non gliene va imposta una: ciascuno mette insieme pezzi diversi, e il lavoro di
modellazione consiste proprio nel riconoscere quali.

- **Selezione con modalità alternative** (10.1 e 10.2): si sceglie un
  sottoinsieme, ma ogni oggetto ha più di un modo di essere scelto, e i modi si
  escludono a vicenda.
- **Conteggi con lotto minimo** (10.3): le variabili non sono binarie ma
  quantità intere, e una quantità può stare a zero oppure sopra una soglia.
- **Copertura con contenitori** (10.4 e 10.5): un fabbisogno va coperto
  acquistando confezioni di composizione fissa, e la quantità in eccesso si
  paga o si spreca.
- **Divisione e bilanciamento** (10.6–10.9): un insieme va diviso fra più
  contenitori e la qualità si misura su quanto i contenitori si somigliano.

Quattro di questi problemi hanno in comune un tratto che nelle tre famiglie non
si era presentato: il **rilassamento lineare è debole**, e in due casi vale
esattamente zero. La ragione è sempre la stessa: una soluzione frazionaria può
spezzare a metà ogni oggetto e metterne una metà in ciascun contenitore,
pareggiando tutto.

!!! note "Dove cercare il bound duale quando il rilassamento non serve"
    **Parità:** un conteggio che non può che essere pari.
    **Numero di contenitori:** quanti ne servono al minimo, letto dalle
    capacità.
    **Dominanza di una classe:** una classe di oggetti che da sola impone il
    valore.
    Sono argomenti *combinatori*: nascono dall'interezza, e il duale del
    rilassamento non può vederli.

## I nove problemi

<div class="grid cards" markdown>

-   **10.1 Premi acquistabili con due modalità**

    ---

    Set packing su quattro variabili invece di due: la quantità
    $x_i + y_i$ è l'indicatore «premio $i$ preso».

    [:octicons-arrow-right-24: BIP · set packing](misti-1.md)

-   **10.2 Asta combinatoria**

    ---

    Un set packing sulle offerte: due offerte che condividono un lotto non
    possono essere accettate entrambe.

    [:octicons-arrow-right-24: BIP · set packing](misti-2.md)

-   **10.3 Dieta con lotto minimo**

    ---

    Quantità intere e variabili semicontinue: un alimento si compra a zero
    oppure sopra la sua soglia.

    [:octicons-arrow-right-24: MILP · lotto minimo](misti-3.md)

-   **10.4 Scatole di luci per gli alberi**

    ---

    Configurazioni di composizione fissa e un vincolo di varietà: quante
    scatole di ciascun tipo comprare.

    [:octicons-arrow-right-24: MILP · contenitori](misti-4.md)

-   **10.5 Spedizioni in scatole**

    ---

    Copertura di una domanda con contenitori di taglia diversa, uno per tipo
    di prodotto.

    [:octicons-arrow-right-24: MILP · capacità](misti-5.md)

-   **10.6 Bambini fra campi estivi**

    ---

    Conteggi interi e vincoli di composizione. Il rilassamento lineare non
    vede la parità: il bound utile è combinatorio.

    [:octicons-arrow-right-24: ILP · conteggi interi](misti-6.md)

-   **10.7 Filiali fra due società**

    ---

    Min-max sullo squilibrio peggiore. Il rilassamento vale zero: si spezza
    ogni filiale a metà.

    [:octicons-arrow-right-24: BIP · min-max](misti-7.md)

-   **10.8 Brani fra CD**

    ---

    Valore assoluto e pareggio delle durate. Anche qui il rilassamento vale
    zero.

    [:octicons-arrow-right-24: MILP · massimo e minimo](misti-8.md)

-   **10.9 Libri fra scaffali**

    ---

    Variabile di massimo: l'altezza di uno scaffale è quella del libro più
    alto, imposta con $y_s \ge h_b\, x_{bs}$.

    [:octicons-arrow-right-24: MILP · variabile di massimo](misti-9.md)

</div>

## Due problemi da modellare

Il capitolo si chiude con due problemi dati come arrivano davvero — un testo,
dei dati, una domanda — senza il modello già scritto: **la settimana del
deposito** (10.10) e **il presidio tecnico** (10.11). Le soluzioni delle loro
domande, come tutte le altre del corso, stanno nel documento riservato ai
docenti e non sono pubblicate.
