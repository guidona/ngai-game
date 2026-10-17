"""Produit des parties de référence avec la version Python, pour tests/web.test.mjs.

Écrit sur la sortie standard, en JSON, des parties jouées au hasard (avec une graine fixe) : pour
chaque coup, la position avant, le coup, le résultat, et la valeur de chaque coup selon
l'ordinateur.
"""

import json
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from ngai.ordinateur import valeurs_des_coups  # noqa: E402
from ngai.plateau import Partie  # noqa: E402


def position(board):
    return {"cases": list(board.cases), "joueur": board.joueur, "grenier": list(board.grenier)}


def main():
    parties = []
    for graine in range(40):
        hasard = random.Random(graine)
        partie = Partie()
        coups = []
        while not partie.terminee():
            avant = position(partie.board)
            valeurs = valeurs_des_coups(partie.board, 4)
            trou = hasard.choice(partie.board.coups_possibles())
            prises, passe = partie.jouer(trou)
            coups.append({
                "avant": avant,
                "trou": trou,
                "valeurs": {str(t): v for t, v in valeurs.items()},
                "prises": prises,
                "passe": passe,
                "apres": position(partie.board),
                "raison_fin": partie.raison_fin,
            })
        parties.append(coups)
    json.dump(parties, sys.stdout)


if __name__ == "__main__":
    main()
