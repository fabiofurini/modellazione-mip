"""Euristiche costruttive del corso: trascrizione riga per riga dei pseudocodici.

Le tre famiglie ispirate al bin packing — next-fit, first-fit, best-fit — per i
problemi «lavori su macchine con disponibilità»: ogni funzione restituisce un
`Esito` con la soluzione, le macchine usate e la traccia dell'esecuzione
passo-passo (lo stesso testo che compare nella dispensa).

Convenzioni: indici 0-based nel codice, 1-based nei messaggi; `t[j][m]` è il
tempo del lavoro j sulla macchina m (per tempi indipendenti dalla macchina si
passa la matrice con righe costanti), `a[m]` la disponibilità della macchina m.
"""
from dataclasses import dataclass, field

INF = float("inf")


class Traccia(list):
    """Elenco dei passi dell'euristica, uno per lavoro."""

    def passo(self, testo: str) -> None:
        self.append(testo)

    def stampa(self) -> None:
        for i, r in enumerate(self, 1):
            print(f"  Passo {i}. {r}")


@dataclass
class Esito:
    x: dict                      # {(j, m): 1} lavoro j assegnato alla macchina m
    y: list                      # y[m] = 1 se la macchina m è usata
    traccia: Traccia = field(default_factory=Traccia)
    ok: bool = True              # False = "nessuna soluzione ammissibile trovata"
    saltati: list = field(default_factory=list)   # lavori non eseguiti (se ammesso)

    def assegnazione(self, j: int):
        """Macchina (0-based) a cui è assegnato il lavoro j, oppure None."""
        for (jj, m), v in self.x.items():
            if jj == j and v == 1:
                return m
        return None


def _ra_testo(ra) -> str:
    return ", ".join(f"ra[{m + 1}] = {r:g}" for m, r in enumerate(ra))


def next_fit(t, a, salta: bool = False) -> Esito:
    """Next-fit: si carica una macchina alla volta.

    Il lavoro j va sulla macchina corrente se ci sta; altrimenti si passa alla
    macchina successiva (se il lavoro ci sta) oppure l'algoritmo fallisce — o,
    con `salta=True`, il lavoro viene saltato (problemi di selezione).
    """
    n, k = len(t), len(a)
    e = Esito(x={}, y=[0] * k)
    cm, ra = 0, a[0]
    for j in range(n):
        if t[j][cm] > ra:
            if cm < k - 1 and t[j][cm + 1] <= a[cm + 1]:
                e.traccia.passo(
                    f"Lavoro {j + 1}: t[{j + 1}][{cm + 1}] = {t[j][cm]:g} > ra = {ra:g}, la macchina "
                    f"{cm + 1} non basta; si passa alla macchina {cm + 2} (ra = {a[cm + 1]:g}), "
                    f"dove t[{j + 1}][{cm + 2}] = {t[j][cm + 1]:g} ci sta: x[{j + 1}][{cm + 2}] = 1, "
                    f"ra = {a[cm + 1]:g} - {t[j][cm + 1]:g} = {a[cm + 1] - t[j][cm + 1]:g}.")
                cm, ra = cm + 1, a[cm + 1]
            elif salta:
                e.traccia.passo(
                    f"Lavoro {j + 1}: t[{j + 1}][{cm + 1}] = {t[j][cm]:g} > ra = {ra:g} e non c'è "
                    f"un'altra macchina su cui passare: il lavoro viene saltato.")
                e.saltati.append(j)
                continue
            else:
                e.traccia.passo(
                    f"Lavoro {j + 1}: t[{j + 1}][{cm + 1}] = {t[j][cm]:g} > ra = {ra:g} e non c'è "
                    f"un'altra macchina su cui passare: nessuna soluzione ammissibile trovata.")
                e.ok = False
                return e
        else:
            e.traccia.passo(
                f"Lavoro {j + 1}: macchina corrente {cm + 1}, ra = {ra:g}; t[{j + 1}][{cm + 1}] = "
                f"{t[j][cm]:g} <= {ra:g}, quindi x[{j + 1}][{cm + 1}] = 1 e ra = {ra:g} - {t[j][cm]:g} "
                f"= {ra - t[j][cm]:g}.")
        e.x[(j, cm)] = 1
        e.y[cm] = 1
        ra -= t[j][cm]
    return e


def first_fit(t, a, salta: bool = False, solo_aperte: bool = False) -> Esito:
    """First-fit: il lavoro va sulla prima macchina con disponibilità residua sufficiente.

    Con `solo_aperte=True` si scandiscono prima le macchine già aperte (in ordine di
    indice) e, se nessuna basta, si apre la successiva.
    """
    n, k = len(t), len(a)
    e = Esito(x={}, y=[0] * k)
    ra = list(a)
    aperte = 0
    for j in range(n):
        sm = None
        limite = aperte if solo_aperte else k
        for m in range(limite):
            if t[j][m] <= ra[m]:
                sm = m
                break
        if sm is None and solo_aperte and aperte < k and t[j][aperte] <= a[aperte]:
            sm = aperte
            aperte += 1
            apre = f" (si apre la macchina {sm + 1})"
        else:
            apre = ""
        if sm is None:
            if salta:
                e.traccia.passo(f"Lavoro {j + 1}: nessuna macchina ha disponibilità sufficiente "
                                f"({_ra_testo(ra)}); il lavoro viene saltato.")
                e.saltati.append(j)
                continue
            e.traccia.passo(f"Lavoro {j + 1}: nessuna macchina ha disponibilità sufficiente "
                            f"({_ra_testo(ra)}): nessuna soluzione ammissibile trovata.")
            e.ok = False
            return e
        scartate = [f"t[{j + 1}][{m + 1}] = {t[j][m]:g} > ra[{m + 1}] = {ra[m]:g}"
                    for m in range(sm) if t[j][m] > ra[m]]
        motivo = ("; ".join(scartate) + "; " if scartate else "")
        e.traccia.passo(
            f"Lavoro {j + 1}: disponibilità residue {_ra_testo(ra)}. {motivo}la macchina {sm + 1} "
            f"è la prima con disponibilità sufficiente (t[{j + 1}][{sm + 1}] = {t[j][sm]:g} <= "
            f"{ra[sm]:g}){apre}: x[{j + 1}][{sm + 1}] = 1, ra[{sm + 1}] = {ra[sm]:g} - {t[j][sm]:g} "
            f"= {ra[sm] - t[j][sm]:g}.")
        e.x[(j, sm)] = 1
        e.y[sm] = 1
        ra[sm] -= t[j][sm]
        if not solo_aperte:
            aperte = max(aperte, sm + 1)
    return e


def best_fit(t, a, criterio, nome_criterio: str, salta: bool = False,
             solo_aperte: bool = False) -> Esito:
    """Best-fit: fra le macchine con disponibilità sufficiente si sceglie quella che
    minimizza `criterio(j, m, ra)`.

    Criteri usati nel corso: il costo c[j][m] (costo minimo), il tempo t[j][m]
    (tempo minimo), la disponibilità residua ra[m] (macchina più piena) e la
    disponibilità dopo l'assegnazione ra[m] - t[j][m] (incastro più stretto).
    """
    n, k = len(t), len(a)
    e = Esito(x={}, y=[0] * k)
    ra = list(a)
    aperte = 0
    for j in range(n):
        limite = aperte if solo_aperte else k
        candidate = [(criterio(j, m, ra), m) for m in range(limite) if t[j][m] <= ra[m]]
        apre = ""
        if candidate:
            val, sm = min(candidate)
            dettagli = "; ".join(f"macchina {m + 1}: {nome_criterio} = {v:g}" for v, m in
                                 sorted(candidate, key=lambda c: c[1]))
            motivo = f"macchine ammissibili — {dettagli}; il minimo è la macchina {sm + 1}"
        elif solo_aperte and aperte < k and t[j][aperte] <= a[aperte]:
            sm = aperte
            aperte += 1
            motivo = f"nessuna macchina aperta basta, si apre la macchina {sm + 1}"
        else:
            if salta:
                e.traccia.passo(f"Lavoro {j + 1}: nessuna macchina ha disponibilità sufficiente "
                                f"({_ra_testo(ra)}); il lavoro viene saltato.")
                e.saltati.append(j)
                continue
            e.traccia.passo(f"Lavoro {j + 1}: nessuna macchina ha disponibilità sufficiente "
                            f"({_ra_testo(ra)}): nessuna soluzione ammissibile trovata.")
            e.ok = False
            return e
        e.traccia.passo(
            f"Lavoro {j + 1}: disponibilità residue {_ra_testo(ra)}; {motivo}: "
            f"x[{j + 1}][{sm + 1}] = 1, ra[{sm + 1}] = {ra[sm]:g} - {t[j][sm]:g} = {ra[sm] - t[j][sm]:g}.")
        e.x[(j, sm)] = 1
        e.y[sm] = 1
        ra[sm] -= t[j][sm]
        if not solo_aperte:
            aperte = max(aperte, sm + 1)
    return e


def matrice(vettore, k: int):
    """Tempi indipendenti dalla macchina: il vettore t_j diventa una matrice n x k."""
    return [[v] * k for v in vettore]
