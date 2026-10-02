"""EX 15 -- Orario della scuola di musica (famiglia 11).

Due pomeriggi da tre ore, sei ore di lezione da collocare: l'orario e' una
partizione delle sei caselle. Il modello usa il conteggio degli strumenti
per giorno (tecnica 3.11), le precedenze fra ore consecutive (3.9) e i vincoli
violabili con penalita' (3.13).

Il modello di partenza contiene un errore istruttivo: il legame fra la lezione e
l'indicatore di strumento e' scritto a senso unico, e il vincolo di varieta'
diventa vuoto. Lo si mette in evidenza risolvendo il modello sbagliato, poi lo si
corregge.

Sui dati dell'esercizio, con il modello corretto, esiste un orario che non viola
nessuna preferenza: l'ottimo vale zero e il certificato e' immediato, perche' i
costi sono tutti non negativi. Le due varianti mostrano che cosa succede appena
le preferenze si stringono: nella prima il conteggio delle caselle disponibili
da' un bound inferiore positivo, nella seconda il modello diventa inammissibile.
"""
import gurobipy as gp
import pandas as pd
from gurobipy import GRB

from mip import ammissibile, frazione, nuovo_modello, risolvi, rilassamento, valuta
from stile import ARANCIO, BLU, GRIGIO, TEAL, intestazione, plt, salva_dati, salva_figura
from esteso import salva_modello

R = range

# ---------- 1. MODELLO E ISTANZA ----------
intestazione("EX 15. Orario della scuola di musica: minimizzare le preferenze violate")
GIORNI = ["lunedi", "martedi"]
ORE = [1, 2, 3]
STRUM = ["chitarra", "violino", "pianoforte"]
h14 = [3, 2, 1]                 # ore da collocare per strumento
nd, nt, ni = len(GIORNI), len(ORE), len(STRUM)
CHITARRA, PIANO = 0, 2          # i due docenti che non vogliono ore consecutive
print(f"  Ore da collocare: {sum(h14)}; caselle disponibili: {nd} * {nt} = {nd * nt}.")
print("  Le due cifre coincidono: ogni casella dell'orario ospita esattamente una lezione.")


def costi(extra_chitarra=()):
    """c[d][t][i] = 1 se la casella viola una preferenza del docente di i."""
    c = [[[0] * ni for _ in R(nt)] for _ in R(nd)]
    for d in R(nd):
        for t in R(nt):
            if d == 1:
                c[d][t][0] = 1                      # chitarra: il docente non viene di martedi
            if t in extra_chitarra:
                c[d][t][0] = 1                      # preferenze aggiuntive della chitarra
            if t == 1 and d == 1:
                c[d][t][1] = 1                      # violino: non all'ora 2 di martedi
            if t == 2:
                c[d][t][2] = 1                      # pianoforte: mai all'ora 3
    return c


c14 = costi()
salva_dati(pd.DataFrame([{"giorno": GIORNI[d], "ora": ORE[t], "strumento": STRUM[i],
                          "costo": c14[d][t][i]}
                         for d in R(nd) for t in R(nt) for i in R(ni)]), "ex15_costi")


def modello(h, c, minimo_strumenti=2, legame_doppio=True):
    """Con `legame_doppio=False` si ottiene il modello della bozza di partenza."""
    mod = nuovo_modello("orario")
    x = mod.addVars(nd, nt, ni, vtype=GRB.BINARY, name="x")
    y = mod.addVars(nd, ni, vtype=GRB.BINARY, name="y")
    mod.setObjective(gp.quicksum(c[d][t][i] * x[d, t, i]
                                 for d in R(nd) for t in R(nt) for i in R(ni)), GRB.MINIMIZE)
    mod.addConstrs((x.sum("*", "*", i) == h[i] for i in R(ni)), name="ore")
    mod.addConstrs((x.sum(d, t, "*") <= 1 for d in R(nd) for t in R(nt)), name="casella")
    mod.addConstrs((y.sum(d, "*") >= minimo_strumenti for d in R(nd)), name="varieta")
    mod.addConstrs((x[d, t, i] - y[d, i] <= 0 for d in R(nd) for t in R(nt) for i in R(ni)),
                   name="attiva")
    if legame_doppio:
        # senza questo verso y_di puo' valere 1 anche se lo strumento i non compare
        mod.addConstrs((y[d, i] - x.sum(d, "*", i) <= 0 for d in R(nd) for i in R(ni)),
                       name="attiva_inversa")
    mod.addConstrs((x[d, t, CHITARRA] + x[d, t + 1, PIANO] <= 1
                    for d in R(nd) for t in R(nt - 1)), name="conflitto1")
    mod.addConstrs((x[d, t, PIANO] + x[d, t + 1, CHITARRA] <= 1
                    for d in R(nd) for t in R(nt - 1)), name="conflitto2")
    return mod, x, y


m14, x14, y14 = modello(h14, c14)
salva_modello(m14, "ex15_primale")


def stampa_orario(valore):
    for d in R(nd):
        riga = []
        for t in R(nt):
            chi = [STRUM[i] for i in R(ni) if valore(d, t, i) > 0.5]
            pen = [i for i in R(ni) if valore(d, t, i) > 0.5 and c14[d][t][i]]
            riga.append((chi[0] if chi else "-") + ("*" if pen else ""))
        print(f"    {GIORNI[d]:11s} " + " | ".join(f"{s:12s}" for s in riga))


# ---------- 2. IL VINCOLO DI VARIETA' SCRITTO A SENSO UNICO E' VUOTO ----------
intestazione("EX 15. Perche' il vincolo di varieta' va scritto nei due versi")
m_err, x_err, y_err = modello(h14, c14, legame_doppio=False)
z_err = risolvi(m_err)
print("  Con il solo legame x_dti <= y_di il solver restituisce questo orario:")
stampa_orario(lambda d, t, i: x_err[d, t, i].X)
strumenti_giorno = [sum(1 for i in R(ni) if any(x_err[d, t, i].X > 0.5 for t in R(nt)))
                    for d in R(nd)]
print("  Strumenti effettivamente presenti: "
      + ", ".join(f"{GIORNI[d]} {strumenti_giorno[d]}" for d in R(nd)))
poveri = [GIORNI[d] for d in R(nd) if strumenti_giorno[d] < 2]
print(f"  Ci sono giorni con un solo strumento ({', '.join(poveri)}), eppure il vincolo")
print("  sum_i y_di >= 2 e' soddisfatto: basta porre y_di = 1 senza fare lezione. Il legame")
print("  x_dti <= y_di dice «se c'e' lezione allora l'indicatore e' acceso», non il viceversa.")
print("  Serve anche y_di <= sum_t x_dti, cioe' la tecnica 3.10 (se e solo se).")
assert poveri, "il modello senza il secondo verso deve ammettere giorni a uno strumento"
salva_dati(pd.DataFrame({"giorno": GIORNI, "strumenti_modello_errato": strumenti_giorno}),
           "ex15_varieta")

# ---------- 3. UNA SOLUZIONE AMMISSIBILE COSTRUITA A MANO ----------
# Regola: il pianoforte va all'ora 1 di lunedi (mai all'ora 3); la chitarra
# riempie le ore restanti di lunedi, cosi' evita l'ora 1; il violino prende le ore
# 1 e 3 di martedi, cosi' evita l'ora 2 e non finisce accanto al pianoforte.
piano_orario = {
    (0, 0): 0, (0, 1): 0, (0, 2): 1,
    (1, 0): PIANO, (1, 1): 1, (1, 2): 0,
}
sol_eur = {f"x[{d},{t},{i}]": 1 for (d, t), i in piano_orario.items()}
for (d, t), i in piano_orario.items():
    sol_eur[f"y[{d},{i}]"] = 1
assert ammissibile(m14, sol_eur), sol_eur
ub14 = sum(c14[d][t][i] for (d, t), i in piano_orario.items())
print("  Orario costruito a mano (l'asterisco segnala una preferenza violata):")
stampa_orario(lambda d, t, i: 1 if piano_orario.get((d, t)) == i else 0)
for i in R(ni):
    assert sum(1 for v in piano_orario.values() if v == i) == h14[i]
print(f"  Preferenze violate: {ub14}  ->  ub = {frazione(ub14)}")

# ---------- 4. IL BOUND INFERIORE ----------
# Il bound che si legge dai dati: la chitarra ha tre ore e il suo docente non viene
# di martedi; lunedi pero' ne puo' ospitare al piu' due, perche' il giorno vuole
# almeno due strumenti diversi. Almeno un'ora di chitarra cade quindi di martedi,
# e vale una violazione.
lb14 = 0.0
conteggio = h14[0] - (nt - 1)
print("  Tutti i costi c_dti sono 0 oppure 1, quindi l'obiettivo e' una somma di termini non")
print("  negativi: lb = 0 senza bisogno di alcun duale.")
print(f"  Contando si dice di piu': la chitarra ha {h14[0]} ore e lunedi ne ospita al piu'")
print(f"  {nt - 1}, perche' il giorno vuole almeno due strumenti; almeno {conteggio} ora di")
print("  chitarra cade quindi di martedi, dove il docente non vorrebbe venire. Attenzione:")
print("  quel conteggio vale sul problema intero, non sul rilassamento --- infatti z(LP) = 0")
print("  --- quindi non si puo' mettere al posto di lb nella catena dei bound.")
zlp14, _, _ = rilassamento(m14, rafforzato=False)
zlp14r, _, _ = rilassamento(m14, rafforzato=True)
print(f"    lb = {frazione(lb14)}   z(LP) = {frazione(zlp14)}   z(LP+) = {frazione(zlp14r)}")
assert lb14 <= zlp14 + 1e-9 <= zlp14r + 1e-9

# ---------- 5. OTTIMO DEL MILP ----------
z14 = risolvi(m14)
print("  Orario ottimo trovato dal solver:")
stampa_orario(lambda d, t, i: x14[d, t, i].X)
print(f"  ub = {frazione(ub14)}   lb = {frazione(lb14)}   z(LP) = {frazione(zlp14)}   "
      f"z(LP+) = {frazione(zlp14r)}   z(MILP) = {frazione(z14)}")
salva_dati(pd.DataFrame([{"problema": "EX 15 orario", "ub": ub14, "lb": lb14,
                          "z_lp": zlp14, "z_lp_rafforzato": zlp14r, "z_milp": z14}]),
           "ex15_bound")
salva_dati(pd.DataFrame([{"giorno": GIORNI[d], "ora": ORE[t], "strumento": STRUM[i]}
                         for d in R(nd) for t in R(nt) for i in R(ni)
                         if x14[d, t, i].X > 0.5]), "ex15_ottimo")
assert lb14 <= z14 and abs(z14 - ub14) <= 1e-9, (lb14, z14, ub14)
print("  L'orario costruito a mano era gia' ottimo, ma nessuno dei due bound lo dimostra:")
print(f"  fra {frazione(lb14)} e {frazione(ub14)} resta un divario che solo il branch and bound chiude.")
assert conteggio <= z14

# ---------- 6. VARIANTI ----------
intestazione("EX 15. Che cosa succede se le preferenze si stringono")
# 14a: la chitarra preferisce non insegnare alle ore 1 e 2 di nessun giorno
c_a = costi(extra_chitarra=(1, 2))
libere = sum(1 for d in R(nd) for t in R(nt) if c_a[d][t][0] == 0)
print(f"  14a. Il docente di chitarra preferisce non insegnare alle ore 2 e 3 di nessun giorno.")
print(f"       Restano {libere} caselle senza penalita' per la chitarra, ma le ore da")
print(f"       collocare sono {h14[0]}: almeno {h14[0] - libere} lezioni violeranno la")
print("       preferenza. E' un bound inferiore che si legge dai soli dati.")
m, x, y = modello(h14, c_a)
z_a = risolvi(m)
minimo = h14[0] - libere
print(f"       z = {frazione(z_a)}: il conteggio da' {minimo}, e il modello non riesce a")
print("       fermarsi li' perche' le caselle libere della chitarra sono tutte nello stesso")
print("       giorno, e il vincolo di varieta' ne vieta l'uso completo.")
assert z_a >= h14[0] - libere - 1e-9
# 14b: ogni giorno deve avere almeno tre strumenti diversi
print("  14b. Ogni giorno deve avere almeno tre strumenti diversi.")
print(f"       Con tre ore al giorno e tre strumenti diversi la chitarra puo' occupare al piu'")
print(f"       una casella al giorno, cioe' {nd} in tutto, ma le ore di chitarra sono {h14[0]}.")
print("       Il modello e' inammissibile, e lo si dimostra contando.")
m, x, y = modello(h14, c14, minimo_strumenti=3)
m.optimize()
stato = {GRB.INFEASIBLE: "INFEASIBLE", GRB.OPTIMAL: "OPTIMAL"}.get(m.Status, str(m.Status))
print(f"       Gurobi restituisce lo stato {stato}, come previsto.")
assert m.Status == GRB.INFEASIBLE
salva_dati(pd.DataFrame([{"variante": "14a. chitarra libera solo all'ora 3", "z": z_a},
                         {"variante": "14b. tre strumenti al giorno", "z": float("nan")}]),
           "ex15_varianti")

# ---------- 7. FIGURA ----------
fig, ax = plt.subplots(figsize=(6.6, 3.0))
colori = {0: TEAL, 1: BLU, 2: ARANCIO, 3: GRIGIO}
for d in R(nd):
    for t in R(nt):
        for i in R(ni):
            if x14[d, t, i].X > 0.5:
                ax.add_patch(plt.Rectangle((t, nd - 1 - d), 1, 1, color=colori[i]))
                ax.annotate(STRUM[i], (t + 0.5, nd - 1 - d + 0.5), ha="center", va="center",
                            fontsize=8, color="white")
for i in R(ni):
    ax.plot([], [], color=colori[i], lw=6, label=f"{STRUM[i]} ({h14[i]} ore)")
ax.set_xlim(0, nt)
ax.set_ylim(0, nd)
ax.set_xticks([t + 0.5 for t in R(nt)])
ax.set_xticklabels([f"ora {o}" for o in ORE])
ax.set_yticks([nd - 1 - d + 0.5 for d in R(nd)])
ax.set_yticklabels(GIORNI)
ax.set_title(f"EX 15: orario ottimo, {frazione(z14)} preferenze violate")
ax.legend(fontsize=7, loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=4)
salva_figura(fig, "ex15_orario")
print("Fine.")
