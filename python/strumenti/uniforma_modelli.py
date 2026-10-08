"""Uniforma la scrittura dei modelli dell'istanza allo stile dei sorgenti di Fabio.

Due regole, applicate solo dentro i modelli numerici (box `istanza` della
dispensa e array corrispondenti sul sito), mai nei modelli simbolici in
`align`, che la virgola dopo il termine noto la tengono:

R1  nessuna punteggiatura dopo il termine noto: ogni riga finisce con il
    valore, l'ultima compresa (niente virgola, niente punto finale);
R2  nella riga delle variabili la virgola sta attaccata alla variabile
    (`x_{11}, &`), non in una colonna sua incolonnata con i segni
    (`x_{11} & , &`).

Uso:
    python3 it/python/strumenti/uniforma_modelli.py            # applica
    python3 it/python/strumenti/uniforma_modelli.py --verifica # esce 1 se c'e' da fare
"""

import re
import sys
from pathlib import Path

RADICE = Path(__file__).resolve().parents[3]   # radice del modulo

# dispensa: i box `istanza`; sito: gli array dentro i blocchi $$...$$ delle
# pagine che riportano il modello dell'istanza
SORGENTI_TEX = ([RADICE / f"it/dispensa_{i}/capitoli" for i in (1, 2, 3)]
                + [RADICE / f"en/notes_{i}/capitoli" for i in (1, 2, 3)])
SORGENTI_MD = [RADICE / "it/docs", RADICE / "en/docs"]

APRE_ARRAY = "\\begin{array}"
CHIUDE_ARRAY = "\\end{array}"


def _spezza(riga):
    """Separa il corpo della riga dal terminatore `\\\\` e dal ritorno a capo."""
    corpo = riga.rstrip("\n")
    fine = riga[len(corpo):]
    if corpo.rstrip().endswith("\\\\"):
        tagliato = corpo.rstrip()
        return tagliato[:-2], "\\\\", fine
    return corpo, "", fine


def _senza_punteggiatura(corpo):
    """R1: via la virgola o il punto subito dopo il termine noto."""
    return re.sub(r"[,.]\s*$", "", corpo)


def _virgole_attaccate(corpo):
    """R2: la virgola passa dalla sua colonna alla fine della cella precedente."""
    if " & , " not in corpo + " " and not re.search(r"&\s*,\s*&", corpo):
        return corpo
    celle = corpo.split("&")
    for k, cella in enumerate(celle):
        if cella.strip() != ",":
            continue
        precedente = next((j for j in range(k - 1, -1, -1) if celle[j].strip()), None)
        if precedente is None:
            continue
        celle[precedente] = celle[precedente].rstrip() + ","
        celle[k] = " "
    return "&".join(celle)


def _blocchi(righe, apre, chiude):
    """Indici delle righe interne a ogni blocco apre...chiude."""
    dentro = False
    for i, riga in enumerate(righe):
        if apre in riga:
            dentro = True
            continue
        if chiude in riga:
            dentro = False
            continue
        if dentro:
            yield i


def _normalizza(righe, apre, chiude):
    cambiate = list(righe)
    for i in _blocchi(righe, apre, chiude):
        corpo, terminatore, fine = _spezza(cambiate[i])
        if not corpo.strip() or corpo.lstrip().startswith("%"):
            continue
        nuovo = _virgole_attaccate(_senza_punteggiatura(corpo))
        cambiate[i] = nuovo + terminatore + fine
    return cambiate


def _file_da_trattare():
    for cartella in SORGENTI_TEX:
        for f in sorted(cartella.rglob("*.tex")):
            yield f, APRE_ARRAY, CHIUDE_ARRAY
    for cartella in SORGENTI_MD:
        for f in sorted(cartella.glob("*.md")):
            yield f, APRE_ARRAY, CHIUDE_ARRAY


def main(verifica=False):
    toccati = []
    for percorso, apre, chiude in _file_da_trattare():
        righe = percorso.read_text(encoding="utf-8").splitlines(keepends=True)
        if apre not in "".join(righe):
            continue
        nuove = _normalizza(righe, apre, chiude)
        if nuove == righe:
            continue
        toccati.append(percorso.relative_to(RADICE))
        if not verifica:
            percorso.write_text("".join(nuove), encoding="utf-8")

    if verifica:
        if toccati:
            print("Modelli non uniformi in:")
            for f in toccati:
                print(f"  {f}")
            return 1
        print("Modelli dell'istanza uniformi.")
        return 0

    print(f"File uniformati: {len(toccati)}")
    for f in toccati:
        print(f"  {f}")
    return 0


if __name__ == "__main__":
    sys.exit(main(verifica="--verifica" in sys.argv))
