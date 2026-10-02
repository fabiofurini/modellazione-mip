# Problemi da modellare

**Quaranta problemi** dati come arrivano davvero — un testo, dei dati, una
domanda — senza il modello già scritto: venti con i dati numerici espliciti e
venti in forma simbolica. Si scaricano anche
[in PDF](pdf/esercizi.pdf).

Le soluzioni sono riservate ai docenti. Il metodo per rispondere è quello di
ogni problema del corso: decisioni e variabili, un vincolo per ogni frase
dell'enunciato, i legami fra le variabili, una soluzione ammissibile e una
duale per i due bound, poi il solver.

## Venti problemi numerici

Dati scritti per esteso, come nei quindici modelli numerici: si legge l'enunciato, si riconoscono le decisioni, si scrive il MILP e lo si risolve.

!!! abstract "N1 — Sei progetti e un budget"

    **Difficoltà:** ★☆☆☆☆

    Un dipartimento sceglie quali progetti finanziare fra sei. I costi sono $40$,
    $25$, $30$, $15$, $50$ e $20$ migliaia di euro; i benefici attesi sono $9$, $5$,
    $7$, $3$, $11$ e $4$. Il budget è $100$. I progetti $2$ e $5$ usano lo stesso
    laboratorio e non possono essere finanziati insieme; il progetto $6$ ha senso
    solo se si finanzia anche il $1$. Si vuole il beneficio massimo.

!!! abstract "N2 — Tre corrieri, quattro consegne"

    **Difficoltà:** ★★☆☆☆

    Quattro consegne vanno affidate a tre corrieri. La tabella riporta, per ogni
    corriere e ogni consegna, il tempo necessario in minuti:

    |  | consegna 1 | consegna 2 | consegna 3 | consegna 4 |
    |---|---|---|---|---|
    | corriere 1 | 20 | 35 | 25 | 40 |
    | corriere 2 | 25 | 20 | 30 | 35 |
    | corriere 3 | 30 | 25 | 20 | 30 |

    Ogni consegna va a un corriere solo; ogni corriere lavora al più $60$ minuti. Si
    vuole il tempo totale minimo.

!!! abstract "N3 — Antenne su cinque quartieri"

    **Difficoltà:** ★☆☆☆☆

    Una città ha cinque quartieri e quattro possibili siti per le antenne. Il
    sito 1 copre i quartieri $\{1,2\}$, il sito 2 copre $\{2,3,4\}$, il sito 3 copre
    $\{1,4,5\}$ e il sito 4 copre $\{3,5\}$. Ogni antenna costa lo stesso. Si vuole
    coprire tutti i quartieri con il minimo numero di antenne.

!!! abstract "N4 — Quattro pacchi in scatole da dieci chili"

    **Difficoltà:** ★☆☆☆☆

    Quattro pacchi pesano $6$, $5$, $4$ e $3$ chili. Ogni scatola porta al più $10$
    chili e un pacco non si divide. Sono disponibili tre scatole. Si vuole il minimo
    numero di scatole.

!!! abstract "N5 — Due prodotti, tre reparti"

    **Difficoltà:** ★☆☆☆☆

    Un'officina produce due articoli. Un pezzo del primo richiede $2$ ore nel
    reparto A, $1$ nel B e $3$ nel C; un pezzo del secondo richiede $1$, $3$ e $2$.
    I reparti hanno $20$, $24$ e $30$ ore disponibili. I margini unitari sono $7$ e
    $6$ euro, e i pezzi si vendono solo interi. Si vuole il margine massimo.

!!! abstract "N6 — I turni della settimana"

    **Difficoltà:** ★★★☆☆

    Uno sportello è aperto sette giorni. Gli addetti necessari sono, da lunedì a
    domenica, $4$, $3$, $4$, $5$, $6$, $5$ e $3$. Ogni addetto assunto lavora cinque
    giorni consecutivi e poi ne riposa due; il ciclo può cominciare in un giorno
    qualsiasi della settimana. Si vuole il minimo numero di addetti.

!!! abstract "N7 — Tre fornitori con costo di attivazione"

    **Difficoltà:** ★★☆☆☆

    Servono $100$ unità di un componente. Tre fornitori lo vendono a $9$, $7$ e $8$
    euro l'unità, ma chi riceve un ordine chiede anche una cifra fissa di $50$, $120$
    e $90$ euro. Il primo fornitore non può superare $40$ unità, il secondo $70$, il
    terzo $60$. Si vuole la spesa minima.

!!! abstract "N8 — Quattro lavori su una macchina"

    **Difficoltà:** ★★★★☆

    Quattro lavori vanno eseguiti uno dopo l'altro su una sola macchina. Le durate
    sono $4$, $2$, $6$ e $3$ ore; le scadenze sono $8$, $5$, $14$ e $10$ ore
    dall'inizio. La macchina parte all'istante $0$ e non si ferma. Si vuole
    minimizzare il ritardo peggiore, cioè il massimo fra zero e la differenza fra il
    completamento e la scadenza.

!!! abstract "N9 — Tre magazzini e tre clienti"

    **Difficoltà:** ★★★☆☆

    Tre clienti chiedono $12$, $8$ e $15$ pallet. Tre magazzini possono essere
    aperti, con capacità $20$, $25$ e $18$ pallet e costo fisso di apertura $100$,
    $90$ e $80$. La tabella riporta il costo di trasporto per pallet da ciascun
    magazzino a ciascun cliente:

    |  | cliente 1 | cliente 2 | cliente 3 |
    |---|---|---|---|
    | magazzino 1 | 2 | 4 | 5 |
    | magazzino 2 | 3 | 2 | 4 |
    | magazzino 3 | 5 | 3 | 2 |

    Si vuole il costo totale minimo.

!!! abstract "N10 — Quattro studenti in due gruppi"

    **Difficoltà:** ★★★☆☆

    Quattro studenti hanno voti medi $28$, $24$, $30$ e $23$. Vanno divisi in due
    gruppi da due. Si vuole che il gruppo con la media più alta e quello con la media
    più bassa siano il più vicini possibile.

!!! abstract "N11 — Cinque film in due sale"

    **Difficoltà:** ★★★☆☆

    Cinque film durano $90$, $120$, $100$, $140$ e $110$ minuti. Due sale sono
    libere per $240$ minuti ciascuna. Ogni film si proietta al più una volta, e in
    una sola sala. Gli incassi attesi sono $500$, $700$, $450$, $800$ e $600$ euro.
    I film $2$ e $4$ hanno lo stesso pubblico e non vanno programmati nella stessa
    sala. Si vuole l'incasso massimo.

!!! abstract "N12 — Dieta con quattro alimenti"

    **Difficoltà:** ★★★☆☆

    Quattro alimenti costano $2$, $3$, $1$ e $4$ euro al chilo. Un chilo di ciascuno
    fornisce

    |  | alimento 1 | alimento 2 | alimento 3 | alimento 4 |
    |---|---|---|---|---|
    | proteine (g) | 20 | 35 | 10 | 40 |
    | ferro (mg) | 3 | 2 | 5 | 4 |

    Servono almeno $120$ grammi di proteine e $25$ milligrammi di ferro. Un alimento,
    se entra nella razione, ci entra per almeno tre chili, e comunque mai per più
    di dieci. Si vuole la spesa minima.

!!! abstract "N13 — Acquisti a scaglioni"

    **Difficoltà:** ★★★★☆

    Un'azienda compra fino a $200$ unità di un materiale. Il prezzo è $10$ euro
    l'unità per le prime $50$, $8$ per quelle fra $51$ e $120$, $7$ oltre $120$. Lo
    sconto vale solo sulle unità dello scaglione, non su tutte. Servono almeno $90$
    unità, e il magazzino ne contiene al più $180$. Si vuole la spesa minima.

!!! abstract "N14 — Sei incroci da sorvegliare"

    **Difficoltà:** ★☆☆☆☆

    Una rete di strade collega sei incroci con i tratti
    $\{1,2\}$, $\{1,3\}$, $\{2,3\}$, $\{2,4\}$, $\{3,5\}$, $\{4,5\}$, $\{4,6\}$ e
    $\{5,6\}$. Una telecamera posta su un incrocio sorveglia tutti i tratti che vi
    arrivano. Si vogliono sorvegliare tutti i tratti con il minimo numero di
    telecamere.

!!! abstract "N15 — Tre mesi di produzione"

    **Difficoltà:** ★★★★☆

    Una linea produce un articolo per tre mesi. Le domande sono $100$, $140$ e $80$
    pezzi. Produrre un pezzo costa $5$ euro; lanciare la produzione in un mese costa
    $300$ euro, indipendentemente dalla quantità; tenere un pezzo in magazzino a
    fine mese costa $1$ euro. La linea produce al più $200$ pezzi al mese. Si parte e
    si finisce con magazzino vuoto. Si vuole il costo minimo.

!!! abstract "N16 — Tre container da scegliere"

    **Difficoltà:** ★★★☆☆

    Tre container sono disponibili: il primo porta $20$ tonnellate e costa $100$
    euro, il secondo $25$ tonnellate e costa $120$ euro, il terzo $15$ tonnellate e
    costa $80$ euro; si paga solo per quelli che si usano. Quattro carichi pesano
    $10$, $8$, $12$ e $6$ tonnellate, e ciascuno va imbarcato per intero in un
    container solo. I carichi $1$ e $3$ sono incompatibili e non viaggiano insieme;
    il carico $4$ richiede un container refrigerato, e lo è soltanto il secondo. Si
    vuole il costo minimo.

!!! abstract "N17 — Sei attività e due squadre"

    **Difficoltà:** ★★★☆☆

    Sei attività durano $3$, $2$, $4$, $1$, $5$ e $2$ giorni. Due squadre lavorano in
    parallelo, e un'attività occupa una sola squadra per tutta la sua durata, senza
    interruzioni. Ogni squadra svolge le sue attività una dopo l'altra. Si vuole
    finire il prima possibile.

!!! abstract "N18 — Due squadre di pronto intervento"

    **Difficoltà:** ★★★☆☆

    Due squadre vanno formate da quattro tecnici. Ogni tecnico ha una fra tre
    competenze: i tecnici $1$ e $2$ hanno la prima, il $3$ la seconda, il $4$ la
    terza. Ogni squadra ha due tecnici e deve avere due competenze diverse. Ogni
    tecnico sta in una squadra sola. I tecnici $1$ e $3$ non lavorano insieme. Si
    vuole sapere se una formazione esiste.

!!! abstract "N19 — Tre periodi con arretrati"

    **Difficoltà:** ★★★★★

    Le domande di tre periodi sono $50$, $70$ e $40$ unità. La produzione costa $4$
    euro l'unità e non supera $60$ unità per periodo. Tenere un'unità in magazzino a
    fine periodo costa $1$ euro; consegnare un'unità in ritardo costa $3$ euro per
    periodo di ritardo. Tutto va consegnato entro la fine del terzo periodo. Si
    vuole il costo minimo.

!!! abstract "N20 — Cinque quadri su due pareti"

    **Difficoltà:** ★★★☆☆

    Cinque quadri sono larghi $60$, $45$, $80$, $50$ e $70$ centimetri. Due pareti
    sono lunghe $180$ centimetri ciascuna. Ogni quadro va appeso, e su una parete
    sola. Si vuole che lo spazio libero sulle due pareti sia il più possibile uguale.

## Venti problemi simbolici

Dati dichiarati con il tipo e l'unità, come nei problemi delle famiglie. Ogni problema mette in gioco due o tre legami fra variabili, e il modello va scritto in generale, con i quantificatori.

!!! abstract "S1 — Progetti con budget, esclusioni e premio di portafoglio"

    **Difficoltà:** ★★★☆☆

    Un ente deve scegliere quali progetti finanziare fra $n \in \mathbb{Z}_{\ge 1}$
    candidati. Per ogni progetto $j \in \{1, 2, \dots, n\}$, il valore
    $c_j \in \mathbb{Q}_{>0}$ è il costo, in euro, e $p_j \in \mathbb{Q}_{>0}$ è il rendimento
    atteso, in euro. Il budget è $b \in \mathbb{Q}_{>0}$ euro. L'insieme $E$ contiene le
    coppie $\{i, j\}$ di progetti che usano lo stesso laboratorio e non possono
    essere finanziati insieme; l'insieme $D$ contiene le coppie ordinate $(i, j)$
    tali che finanziare $i$ obbliga a finanziare anche $j$. Un sottoinsieme
    $S \subseteq \{1, 2, \dots, n\}$ raccoglie i progetti strategici: se se ne
    finanziano almeno $\ell \in \mathbb{Z}_{\ge 1}$, l'ente riceve un contributo aggiuntivo
    di $\bar r \in \mathbb{Q}_{>0}$ euro, una volta sola. L'ente vuole decidere quali
    progetti finanziare, a rendimento totale massimo.

!!! abstract "S2 — Compiti e risorse da attivare"

    **Difficoltà:** ★★★★☆

    Un reparto deve affidare $n \in \mathbb{Z}_{\ge 1}$ compiti a $m \in \mathbb{Z}_{\ge 1}$ risorse.
    Per ogni risorsa $i \in \{1, 2, \dots, m\}$ e ogni compito
    $j \in \{1, 2, \dots, n\}$, il valore $c_{ij} \in \mathbb{Q}_{>0}$ è il costo, in euro,
    di affidare il compito $j$ alla risorsa $i$, e $t_{ij} \in \mathbb{Q}_{>0}$ è il tempo
    che quel compito occupa su quella risorsa, in ore. Per ogni risorsa $i$, il
    valore $b_i \in \mathbb{Q}_{>0}$ è il tempo disponibile, in ore; $f_i \in \mathbb{Q}_{>0}$ è il
    costo fisso di attivazione, in euro, da pagare se la risorsa riceve almeno un
    compito; $\ell_i \in \mathbb{Q}_{>0}$ è il carico minimo, in ore, che una risorsa
    attivata deve raggiungere, con $\ell_i \le b_i$. Ogni compito va affidato a una
    sola risorsa. Il reparto vuole decidere quali risorse attivare e come
    distribuire i compiti, a costo totale minimo.

!!! abstract "S3 — Presidi con raggio di servizio e riserva"

    **Difficoltà:** ★★★★☆

    Un'amministrazione deve coprire $m \in \mathbb{Z}_{\ge 1}$ utenti aprendo presidi in
    alcune di $n \in \mathbb{Z}_{\ge 1}$ sedi candidate. Per ogni sede
    $j \in \{1, 2, \dots, n\}$, il valore $f_j \in \mathbb{Q}_{>0}$ è il costo di apertura,
    in euro, e $u_j \in \mathbb{Z}_{\ge 1}$ è il numero massimo di utenti che il presidio
    può prendere in carico. Per ogni sede $j$ e ogni utente
    $i \in \{1, 2, \dots, m\}$, il valore $d_{ij} \in \mathbb{Q}_{\ge 0}$ è la distanza, in
    chilometri; la sede può servire l'utente soltanto se $d_{ij} \le r$, dove
    $r \in \mathbb{Q}_{>0}$ è il raggio di servizio. Ogni utente va preso in carico da
    esattamente un presidio aperto. Gli utenti di un sottoinsieme critico $K$ devono
    inoltre avere un secondo presidio aperto entro il raggio, anche se non li prende
    in carico. L'amministrazione vuole decidere dove aprire e chi prende in carico
    chi, a costo totale minimo.

!!! abstract "S4 — Contenitori di più tipi con merci incompatibili"

    **Difficoltà:** ★★★★☆

    Un magazzino deve riporre $n \in \mathbb{Z}_{\ge 1}$ oggetti in contenitori di
    $k \in \mathbb{Z}_{\ge 1}$ tipi. Per ogni oggetto $j \in \{1, 2, \dots, n\}$, il valore
    $w_j \in \mathbb{Q}_{>0}$ è il peso, in chili, e $g_j \in \{1, 2, \dots, q\}$ è la
    classe merceologica, fra $q \in \mathbb{Z}_{\ge 1}$ classi. Per ogni tipo di contenitore
    $h \in \{1, 2, \dots, k\}$, il valore $c_h \in \mathbb{Q}_{>0}$ è la capacità, in chili,
    $e_h \in \mathbb{Q}_{>0}$ è il costo di un contenitore di quel tipo, in euro, e
    $N_h \in \mathbb{Z}_{\ge 1}$ è il numero di contenitori disponibili. L'insieme $F$
    contiene le coppie $\{a, b\}$ di classi che non possono stare nello stesso
    contenitore. Un oggetto non si divide. Il magazzino vuole decidere quanti
    contenitori di ciascun tipo usare e come riempirli, a costo totale minimo.

!!! abstract "S5 — Lotti con attrezzaggio, capacità e magazzino limitato"

    **Difficoltà:** ★★★★☆

    Un'azienda pianifica la produzione di un articolo su $n \in \mathbb{Z}_{\ge 1}$ periodi.
    Per ogni periodo $t \in \{1, 2, \dots, n\}$, il valore $d_t \in \mathbb{Q}_{\ge 0}$ è la
    domanda, in pezzi; $p_t \in \mathbb{Q}_{>0}$ è il costo di produzione di un pezzo, in
    euro; $q_t \in \mathbb{Q}_{>0}$ è il costo fisso di attrezzaggio della linea, in euro,
    da pagare se nel periodo si produce; $c_t \in \mathbb{Q}_{>0}$ è la quantità massima
    producibile nel periodo, in pezzi; $v_t \in \mathbb{Q}_{>0}$ è la quantità minima che si
    produce se si produce, in pezzi, con $v_t \le c_t$. Per ogni periodo
    $t \in \{1, 2, \dots, n-1\}$, il valore $h_t \in \mathbb{Q}_{>0}$ è il costo di tenere un
    pezzo in magazzino a fine periodo, in euro; il magazzino tiene al più
    $M \in \mathbb{Q}_{>0}$ pezzi, in ogni periodo. I valori $r_0 \in \mathbb{Q}_{\ge 0}$ e
    $r_n \in \mathbb{Q}_{\ge 0}$ sono la scorta iniziale e quella richiesta alla fine, in
    pezzi. L'azienda vuole decidere quanto produrre in ogni periodo, a costo totale
    minimo.

!!! abstract "S6 — $p$ sedi, capacità e distanza peggiore"

    **Difficoltà:** ★★★★☆

    Un'azienda deve servire $m \in \mathbb{Z}_{\ge 1}$ clienti aprendo esattamente
    $p \in \mathbb{Z}_{\ge 1}$ sedi fra $n \in \mathbb{Z}_{\ge 1}$ candidate, con $p \le n$. Per ogni
    cliente $c \in \{1, 2, \dots, m\}$, il valore $d_c \in \mathbb{Q}_{>0}$ è la domanda, in
    pallet. Per ogni sede $l \in \{1, 2, \dots, n\}$, il valore $u_l \in \mathbb{Q}_{>0}$ è
    la capacità, in pallet; per ogni sede $l$ e cliente $c$, il valore
    $t_{lc} \in \mathbb{Q}_{\ge 0}$ è la distanza, in chilometri. Ogni cliente è servito
    interamente da una sola sede fra quelle aperte, e una sede aperta non supera la
    propria capacità. Un sottoinsieme $A$ di sedi è già di proprietà dell'azienda;
    fra quelle non di proprietà se ne possono aprire al più $\bar p \in \mathbb{Z}_{\ge 1}$.
    L'azienda vuole decidere dove aprire e chi serve chi, minimizzando la distanza
    più grande fra un cliente e la sede che lo serve.

!!! abstract "S7 — Macchine qualificate e date di rilascio"

    **Difficoltà:** ★★★★★

    Un'officina deve eseguire $n \in \mathbb{Z}_{\ge 1}$ lavori su $k \in \mathbb{Z}_{\ge 1}$
    macchine. Per ogni lavoro $j \in \{1, 2, \dots, n\}$, il valore
    $t_j \in \mathbb{Q}_{>0}$ è il tempo di lavorazione, in ore, uguale su tutte le
    macchine; $r_j \in \mathbb{Q}_{\ge 0}$ è la data di rilascio, cioè l'istante prima del
    quale il lavoro non può cominciare; $Q_j \subseteq \{1, 2, \dots, k\}$ è
    l'insieme delle macchine qualificate a eseguirlo. Per ogni macchina
    $i \in \{1, 2, \dots, k\}$, il valore $a_i \in \mathbb{Q}_{\ge 0}$ è l'istante da cui la
    macchina è libera. Ogni macchina esegue un lavoro alla volta e una lavorazione,
    una volta cominciata, non si interrompe. L'officina vuole decidere su quale
    macchina e in quale ordine eseguire i lavori, minimizzando l'istante in cui
    finisce l'ultimo.

!!! abstract "S8 — Scaffali con classi e peso massimo"

    **Difficoltà:** ★★★★☆

    Un deposito deve distribuire $n \in \mathbb{Z}_{\ge 1}$ oggetti su $m \in \mathbb{Z}_{\ge 1}$
    scaffali. Gli oggetti appartengono a $q \in \mathbb{Z}_{\ge 1}$ classi merceologiche:
    per ogni oggetto $j \in \{1, 2, \dots, n\}$, il valore
    $g_j \in \{1, 2, \dots, q\}$ è la classe e $w_j \in \mathbb{Q}_{>0}$ è il peso, in
    chili. Ogni scaffale può ospitare oggetti di al più $s \in \mathbb{Z}_{\ge 1}$ classi
    diverse, con $s \le q$, e porta al più $c \in \mathbb{Q}_{>0}$ chili. Gli oggetti di un
    sottoinsieme $P$ sono fragili e vanno messi su scaffali tutti diversi. Il
    deposito vuole decidere la distribuzione, minimizzando il peso dello scaffale
    più carico.

!!! abstract "S9 — Taglio con più formati di barra"

    **Difficoltà:** ★★★★★

    Un'officina deve ricavare spezzoni di $k \in \mathbb{Z}_{\ge 1}$ lunghezze diverse da
    barre di $h \in \mathbb{Z}_{\ge 1}$ formati. Per ogni formato $f \in \{1, 2, \dots, h\}$,
    il valore $L_f \in \mathbb{Q}_{>0}$ è la lunghezza della barra, in metri,
    $g_f \in \mathbb{Q}_{>0}$ è il costo di una barra, in euro, e $N_f \in \mathbb{Z}_{\ge 1}$ è il
    numero di barre disponibili. Per ogni lunghezza $i \in \{1, 2, \dots, k\}$, il
    valore $\ell_i \in \mathbb{Q}_{>0}$ è la lunghezza dello spezzone, in metri, e
    $b_i \in \mathbb{Z}_{\ge 1}$ è il numero di spezzoni richiesti. Lo sfrido complessivo
    non può superare una frazione $e \in \mathbb{Q}_{>0}$, con $e < 1$, della lunghezza
    totale delle barre usate. L'officina vuole decidere quante barre di ciascun
    formato usare e come tagliarle, a costo totale minimo.

!!! abstract "S10 — Rete con costo fisso d'arco e archi limitati"

    **Difficoltà:** ★★★★☆

    Un operatore logistico deve spedire $Q \in \mathbb{Q}_{>0}$ unità di merce da un nodo
    origine $s$ a un nodo destinazione $u$ su una rete orientata di nodi $V$ e archi
    $A \subseteq V \times V$; i nodi diversi da $s$ e $u$ sono di transito. Per ogni
    arco $(i, j) \in A$, il valore $c_{ij} \in \mathbb{Q}_{>0}$ è il costo di far passare
    un'unità, in euro; $f_{ij} \in \mathbb{Q}_{>0}$ è il costo fisso di attivazione, in
    euro; $k_{ij} \in \mathbb{Q}_{>0}$ è la capacità, in unità. Gli archi attivati non
    possono essere più di $\bar a \in \mathbb{Z}_{\ge 1}$, e da ogni nodo di transito non ne
    può uscire più di uno attivato. L'operatore vuole decidere quali archi attivare
    e quanto farvi passare, a costo totale minimo.

!!! abstract "S11 — Turni ciclici con riposo e competenze"

    **Difficoltà:** ★★★★★

    Un servizio è attivo su $n \in \mathbb{Z}_{\ge 1}$ giorni, in ciclo settimanale. Il
    personale è diviso in $q \in \mathbb{Z}_{\ge 1}$ competenze. Per ogni giorno
    $t \in \{1, 2, \dots, n\}$ e ogni competenza $c \in \{1, 2, \dots, q\}$, il
    valore $b_{tc} \in \mathbb{Z}_{\ge 0}$ è il numero di persone di quella competenza che
    devono essere in servizio quel giorno. Per ogni competenza $c$, il valore
    $w_c \in \mathbb{Q}_{>0}$ è il costo settimanale di una persona, in euro, e
    $m_c \in \mathbb{Z}_{\ge 0}$ è il numero di persone di quella competenza già assunte.
    Chi lavora sta in servizio $\ell \in \mathbb{Z}_{\ge 1}$ giorni consecutivi e poi ne
    riposa $g \in \mathbb{Z}_{\ge 1}$, e il ciclo può cominciare in un giorno qualsiasi. Il
    servizio vuole decidere quante persone assumere per competenza e con quale
    giorno di inizio ciclo, a costo totale minimo.

!!! abstract "S12 — Portafoglio a lotti con settori"

    **Difficoltà:** ★★★☆☆

    Un investitore dispone di un capitale $K \in \mathbb{Q}_{>0}$ euro e sceglie fra
    $n \in \mathbb{Z}_{\ge 1}$ fondi, divisi in $k \in \mathbb{Z}_{\ge 1}$ settori. Per ogni fondo
    $j \in \{1, 2, \dots, n\}$, il valore $s_j \in \{1, 2, \dots, k\}$ è il settore,
    $q_j \in \mathbb{Q}_{>0}$ è la taglia del lotto, in euro — il fondo si compra solo a
    lotti interi — e $r_j \in \mathbb{Q}_{>0}$ è il rendimento atteso per euro investito. In
    nessun settore si può investire più di una frazione $a \in \mathbb{Q}_{>0}$, con
    $a \le 1$, del capitale. Vanno scelti almeno $p \in \mathbb{Z}_{\ge 1}$ fondi diversi, e
    un fondo scelto riceve almeno $v_j \in \mathbb{Z}_{\ge 1}$ lotti. L'investitore vuole
    decidere quanti lotti comprare di ciascun fondo, a rendimento totale massimo.

!!! abstract "S13 — Razione su più giorni"

    **Difficoltà:** ★★★★★

    Una mensa prepara la razione di $n \in \mathbb{Z}_{\ge 1}$ giorni usando
    $s \in \mathbb{Z}_{\ge 1}$ alimenti e rispettando $r \in \mathbb{Z}_{\ge 1}$ vincoli
    nutrizionali. Per ogni alimento $i \in \{1, 2, \dots, s\}$, il valore
    $w_i \in \mathbb{Q}_{>0}$ è il costo di un chilo, in euro; $c_i \in \mathbb{Q}_{>0}$ è la
    quantità minima, in chili, che se ne usa in un giorno in cui compare;
    $u_i \in \mathbb{Q}_{>0}$ è la quantità massima giornaliera, con $c_i \le u_i$; e
    $h_i \in \mathbb{Q}_{>0}$ è il costo di tenere un chilo in dispensa da un giorno al
    successivo, in euro. Per ogni alimento $i$ e nutriente
    $j \in \{1, 2, \dots, r\}$, il valore $g_{ij} \in \mathbb{Q}_{\ge 0}$ è la quantità di
    nutriente $j$ in un chilo di alimento $i$; per ogni nutriente $j$, ogni giorno
    ne servono almeno $a_j \in \mathbb{Q}_{>0}$ e al più $b_j \in \mathbb{Q}_{>0}$. Ogni giorno
    devono comparire almeno $t \in \mathbb{Z}_{\ge 1}$ alimenti diversi. La mensa vuole
    decidere quanto comprare e quanto usare ogni giorno, a costo totale minimo.

!!! abstract "S14 — Sequenze con attrezzaggi dipendenti e finestre"

    **Difficoltà:** ★★★★★

    Su una sola macchina vanno eseguiti $n \in \mathbb{Z}_{\ge 1}$ lavori. Per ogni lavoro
    $j \in \{1, 2, \dots, n\}$, il valore $t_j \in \mathbb{Q}_{>0}$ è il tempo di
    lavorazione, in ore, e $d_j \in \mathbb{Q}_{>0}$ è la scadenza, cioè l'istante entro il
    quale il lavoro dovrebbe essere completato; consegnare in ritardo costa
    $w_j \in \mathbb{Q}_{>0}$ euro per ora di ritardo. Per ogni coppia di lavori distinti
    $i$ e $j$, il valore $s_{ij} \in \mathbb{Q}_{\ge 0}$ è il tempo di attrezzaggio, in ore,
    necessario per passare dal lavoro $i$ al lavoro $j$. La macchina parte
    all'istante $0$, esegue un lavoro alla volta e non si ferma durante una
    lavorazione. L'officina vuole decidere l'ordine dei lavori, minimizzando il
    costo totale dei ritardi.

!!! abstract "S15 — Squadre su più periodi"

    **Difficoltà:** ★★★★☆

    Un'azienda di servizi deve coprire $m \in \mathbb{Z}_{\ge 1}$ zone per
    $n \in \mathbb{Z}_{\ge 1}$ periodi, con $k \in \mathbb{Z}_{\ge 1}$ squadre. Per ogni squadra
    $j \in \{1, 2, \dots, k\}$, il valore $c_j \in \mathbb{Q}_{>0}$ è il costo di impiegarla
    per un periodo, in euro, e $S_j \subseteq \{1, 2, \dots, m\}$ è l'insieme delle
    zone che può coprire. In ogni periodo ogni zona va coperta da almeno una squadra
    impiegata, e una squadra impiegata in un periodo copre tutte e sole le zone di
    $S_j$. Una squadra non può essere impiegata per più di $\ell \in \mathbb{Z}_{\ge 1}$
    periodi su $n$, e se viene impiegata lo è per almeno $v \in \mathbb{Z}_{\ge 1}$ periodi,
    con $v \le \ell$. L'azienda vuole decidere quali squadre impiegare e in quali
    periodi, a costo totale minimo.

!!! abstract "S16 — Studenti e relatori con carichi equilibrati"

    **Difficoltà:** ★★★★☆

    Un corso di laurea deve assegnare $n \in \mathbb{Z}_{\ge 1}$ studenti a
    $m \in \mathbb{Z}_{\ge 1}$ relatori. Per ogni studente $i \in \{1, 2, \dots, n\}$ e ogni
    relatore $j \in \{1, 2, \dots, m\}$, il valore $v_{ij} \in \mathbb{Z}_{\ge 0}$ è il
    punteggio di preferenza che lo studente dà a quel relatore. Per ogni relatore
    $j$, il valore $u_j \in \mathbb{Z}_{\ge 1}$ è il numero massimo di studenti che può
    seguire. Ogni studente va assegnato a un solo relatore, e nessuno può ricevere
    un relatore a cui ha dato un punteggio minore di $\bar v \in \mathbb{Z}_{\ge 0}$. Il
    corso di laurea vuole decidere l'assegnazione massimizzando la somma delle
    preferenze, con il vincolo che la differenza fra il numero di studenti del
    relatore più carico e quello del meno carico fra i relatori con almeno uno
    studente non superi $g \in \mathbb{Z}_{\ge 0}$.

!!! abstract "S17 — Manutenzioni con finestre e perdita di produzione"

    **Difficoltà:** ★★★★★

    Uno stabilimento ha $n \in \mathbb{Z}_{\ge 1}$ macchine e pianifica le manutenzioni su
    $T \in \mathbb{Z}_{\ge 1}$ periodi. Per ogni macchina $j \in \{1, 2, \dots, n\}$, il
    valore $a_j \in \{1, 2, \dots, T\}$ e il valore $b_j \in \{1, 2, \dots, T\}$,
    con $a_j \le b_j$, delimitano la finestra entro cui la manutenzione va fatta,
    una volta sola; $p_j \in \mathbb{Q}_{>0}$ è la produzione oraria della macchina, in
    pezzi; $\ell_j \in \mathbb{Z}_{\ge 1}$ è la durata della manutenzione, in periodi
    consecutivi. Per ogni macchina $j$ e periodo $t$, il valore
    $c_{jt} \in \mathbb{Q}_{>0}$ è il costo della squadra di manutenzione, in euro, se la
    manutenzione comincia in quel periodo. In nessun periodo si possono fermare più
    di $k \in \mathbb{Z}_{\ge 1}$ macchine, e la produzione complessiva persa non può
    superare $M \in \mathbb{Q}_{>0}$ pezzi. Lo stabilimento vuole decidere quando fermare
    ciascuna macchina, a costo totale minimo.

!!! abstract "S18 — Partizione bilanciata di un grafo"

    **Difficoltà:** ★★★★☆

    Un'organizzazione deve dividere in due squadre i $n \in \mathbb{Z}_{\ge 1}$ nodi di un
    grafo non orientato di archi $E$. Per ogni nodo $i \in \{1, 2, \dots, n\}$, il
    valore $w_i \in \mathbb{Q}_{>0}$ è il carico di lavoro che porta; per ogni arco
    $\{i, j\} \in E$, il valore $u_{ij} \in \mathbb{Q}_{>0}$ è l'intensità dello scambio fra
    i due nodi. Il carico totale di ciascuna squadra deve stare fra
    $L \in \mathbb{Q}_{>0}$ e $U \in \mathbb{Q}_{>0}$, con $L \le U$. Alcune coppie di nodi,
    raccolte nell'insieme $P$, devono finire nella stessa squadra; altre, raccolte
    in $F$, in squadre diverse. L'organizzazione vuole decidere la divisione,
    minimizzando l'intensità totale degli scambi fra le due squadre.

!!! abstract "S19 — Caricamento con veicoli eterogenei"

    **Difficoltà:** ★★★★☆

    Un corriere deve spedire $n \in \mathbb{Z}_{\ge 1}$ carichi con $m \in \mathbb{Z}_{\ge 1}$
    veicoli. Per ogni carico $j \in \{1, 2, \dots, n\}$, il valore
    $w_j \in \mathbb{Q}_{>0}$ è il peso, in chili, $o_j \in \mathbb{Q}_{>0}$ è il volume, in metri
    cubi, e $V_j \subseteq \{1, 2, \dots, m\}$ è l'insieme dei veicoli su cui può
    salire. Per ogni veicolo $i \in \{1, 2, \dots, m\}$, il valore
    $c_i \in \mathbb{Q}_{>0}$ è la portata, in chili, $s_i \in \mathbb{Q}_{>0}$ è il volume
    disponibile, in metri cubi, e $f_i \in \mathbb{Q}_{>0}$ è il costo di usarlo, in euro.
    L'insieme $E$ contiene le coppie $\{a, b\}$ di carichi che non possono viaggiare
    sullo stesso veicolo. Ogni carico va imbarcato su un solo veicolo. Il corriere
    vuole decidere quali veicoli usare e come ripartire i carichi, a costo totale
    minimo.

!!! abstract "S20 — Capacità da installare con costi a scaglioni"

    **Difficoltà:** ★★★★★

    Un gestore deve installare una capacità complessiva di almeno
    $Q \in \mathbb{Q}_{>0}$ megawatt scegliendo fra $n \in \mathbb{Z}_{\ge 1}$ tecnologie. Per ogni
    tecnologia $j \in \{1, 2, \dots, n\}$, il valore $k_j \in \mathbb{Q}_{>0}$ è la capacità
    di una unità installata, in megawatt, e le unità si installano in numero intero;
    il costo unitario scende a scaglioni: per ogni scaglione
    $h \in \{1, 2, \dots, m_j\}$, con $m_j \in \mathbb{Z}_{\ge 1}$, il valore
    $u_{jh} \in \mathbb{Z}_{\ge 1}$ è il numero di unità dello scaglione e
    $c_{jh} \in \mathbb{Q}_{>0}$ è il costo di una unità in quello scaglione, con
    $c_{j1} > c_{j2} > \cdots > c_{jm_j}$; uno scaglione si usa solo se i precedenti
    sono stati riempiti. Si possono usare al più $p \in \mathbb{Z}_{\ge 1}$ tecnologie
    diverse, e una tecnologia usata va installata per almeno $v_j \in \mathbb{Z}_{\ge 1}$
    unità. Il gestore vuole decidere quanto installare di ciascuna tecnologia, a
    costo totale minimo.
