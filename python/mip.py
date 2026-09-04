"""Utilità comuni del corso: solver, rilassamento LP, duale, bound e controlli.

Tutti gli script dei capitoli importano da qui. Un solo solver: Gurobi.
"""
from fractions import Fraction

import gurobipy as gp
from gurobipy import GRB

TOL = 1e-6


def nuovo_modello(nome: str = "modello") -> gp.Model:
    """Un modello Gurobi silenzioso."""
    m = gp.Model(nome)
    m.Params.OutputFlag = 0
    return m


def risolvi(m: gp.Model) -> float:
    """Risolve all'ottimo e restituisce il valore ottimo (errore se non ottimo)."""
    m.optimize()
    if m.Status != GRB.OPTIMAL:
        raise RuntimeError(f"{m.ModelName}: stato Gurobi {m.Status}, atteso OPTIMAL")
    return m.ObjVal


def rilassamento(m: gp.Model, rafforzato: bool = True):
    """Risolve il rilassamento LP di un MILP.

    Con `rafforzato=True` (quello che fa il solver con m.relax()) le variabili
    binarie restano in [0, 1]; con `rafforzato=False` si tolgono anche i limiti
    superiori, cioè si rilassa x in {0,1} con x >= 0 soltanto: è il rilassamento
    di cui la dispensa scrive il duale a mano, e il suo ottimo coincide con
    l'ottimo di quel duale (dualità forte).

    Restituisce (z_lp, soluzione, duali): la soluzione è {nome variabile: valore},
    i duali sono {nome vincolo: Pi}.
    """
    m.update()               # relax() copia il modello: le modifiche pendenti vanno prima applicate
    r = m.relax()
    r.Params.OutputFlag = 0
    if not rafforzato:
        for v, v0 in zip(r.getVars(), m.getVars()):
            if v0.VType in (GRB.BINARY, GRB.INTEGER) and v0.LB == 0 and v0.UB == 1:
                v.UB = GRB.INFINITY
    r.optimize()
    if r.Status != GRB.OPTIMAL:
        raise RuntimeError(f"rilassamento di {m.ModelName}: stato Gurobi {r.Status}")
    sol = {v.VarName: v.X for v in r.getVars()}
    pi = {c.ConstrName: c.Pi for c in r.getConstrs()}
    return r.ObjVal, sol, pi


def valuta(m: gp.Model, sol: dict):
    """Valore dell'obiettivo e massima violazione di una soluzione data.

    `sol` è {nome variabile: valore}; le variabili non nominate valgono 0.
    Serve per le soluzioni euristiche (primale) e per quelle duali costruite a
    mano: il modello duale si scrive come modello Gurobi e si valuta qui.
    """
    m.update()
    val = {v.VarName: float(sol.get(v.VarName, 0.0)) for v in m.getVars()}
    obj = m.getObjective()
    z = obj.getConstant() + sum(obj.getCoeff(i) * val[obj.getVar(i).VarName]
                                for i in range(obj.size()))
    viol = 0.0
    for v in m.getVars():
        viol = max(viol, v.LB - val[v.VarName], val[v.VarName] - v.UB)
    for c in m.getConstrs():
        riga = m.getRow(c)
        lhs = sum(riga.getCoeff(i) * val[riga.getVar(i).VarName] for i in range(riga.size()))
        if c.Sense == GRB.LESS_EQUAL:
            viol = max(viol, lhs - c.RHS)
        elif c.Sense == GRB.GREATER_EQUAL:
            viol = max(viol, c.RHS - lhs)
        else:
            viol = max(viol, abs(lhs - c.RHS))
    return z, viol


def ammissibile(m: gp.Model, sol: dict) -> bool:
    return valuta(m, sol)[1] <= TOL


def frazione(x: float) -> str:
    """Numero come frazione ridotta (o intero), come nella dispensa: 25/4, 7, 5/6."""
    f = Fraction(x).limit_denominator(10_000)
    return str(f.numerator) if f.denominator == 1 else f"{f.numerator}/{f.denominator}"


def tabella_bound(ub, lb, zlp, zmilp, senso: str = "min", zlp_r=None) -> str:
    """Riga riassuntiva dei bound: ub, lb, z(LP), [z(LP+)], z(MILP) e gap dell'euristica.

    Per un problema di minimo ub viene dall'euristica e lb dal duale; per un
    massimo i ruoli si scambiano (l'euristica dà un lower bound). `senso` serve
    solo per il gap, che è sempre |valore euristico - ottimo| / |ottimo|.
    z(LP) è il rilassamento «puro» (x >= 0), z(LP+) quello rafforzato (x <= 1).
    """
    eur = ub if senso == "min" else lb
    gap = abs(eur - zmilp) / abs(zmilp) if abs(zmilp) > TOL else 0.0
    extra = f"   z(LP+) = {frazione(zlp_r):>8}" if zlp_r is not None else ""
    return (f"  ub = {frazione(ub):>8}   lb = {frazione(lb):>8}   z(LP) = {frazione(zlp):>8}{extra}"
            f"   z(MILP) = {frazione(zmilp):>6}   gap euristica = {100 * gap:.1f}%")


def stampa_soluzione(m: gp.Model, solo_non_nulle: bool = False) -> None:
    """Stampa le variabili di un modello risolto (x~ = soluzione ottima)."""
    for v in m.getVars():
        if solo_non_nulle and abs(v.X) < TOL:
            continue
        print(f"    {v.VarName} = {frazione(v.X)}")


def stampa_lp(m: gp.Model) -> None:
    """Il modello dell'istanza in formato LP (per controllare i tabulari della dispensa)."""
    import os
    import tempfile
    m.update()
    with tempfile.TemporaryDirectory() as d:
        percorso = os.path.join(d, "modello.lp")
        m.write(percorso)
        print(open(percorso).read())


def due_rilassamenti(m, d):
    """z(LP) puro (= ottimo del duale scritto a mano) e z(LP+) rafforzato del solver.

    `m` è il modello primale, `d` il suo duale (scritto a mano, come modello
    Gurobi a sé): la funzione controlla che i due ottimi coincidano (dualità
    forte) e stampa entrambi i rilassamenti.
    """
    zlp, _, pi = rilassamento(m, rafforzato=False)
    zlp_r, _, _ = rilassamento(m, rafforzato=True)
    zd = risolvi(d)
    assert abs(zlp - zd) <= 1e-6, (zlp, zd)
    print(f"Ottimo del duale = z(LP) (dualità forte): {frazione(zd)};  rilassamento rafforzato "
          f"con x <= 1: z(LP+) = {frazione(zlp_r)}")
    return zlp, zlp_r, pi


def registra_bound(nome, ub, lb, zlp, zlp_r, zmilp, senso="min"):
    """Stampa la riga dei bound e restituisce il record da salvare in CSV."""
    print(tabella_bound(ub, lb, zlp, zmilp, senso, zlp_r))
    return {"problema": nome, "ub": ub, "lb": lb, "z_lp": zlp, "z_lp_rafforzato": zlp_r,
            "z_milp": zmilp}
