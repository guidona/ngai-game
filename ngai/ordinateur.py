"""L'adversaire ordinateur : une recherche minimax avec élagage alpha-bêta.

L'ordinateur explore les coups possibles sur plusieurs tours, en supposant que l'adversaire joue
au mieux, et garde le coup qui maximise l'écart entre les deux greniers.
"""

import random

NIVEAUX = {"facile": 1, "moyen": 4, "difficile": 10}


def evaluer(board, joueur):
    """L'écart de pions entre le joueur et son adversaire, en fin de séance si elle est finie."""
    if board.terminee():
        board = board.copie()
        board.ramasser()
    return board.grenier[joueur] - board.grenier[1 - joueur]


def minimax(board, profondeur, joueur, alpha, beta):
    if profondeur == 0 or board.terminee():
        return evaluer(board, joueur)

    maximiser = board.joueur == joueur
    meilleur = float("-inf") if maximiser else float("inf")
    for trou in board.coups_possibles():
        suite = board.copie()
        suite.jouer(trou)
        valeur = minimax(suite, profondeur - 1, joueur, alpha, beta)
        if maximiser:
            meilleur = max(meilleur, valeur)
            alpha = max(alpha, valeur)
        else:
            meilleur = min(meilleur, valeur)
            beta = min(beta, valeur)
        if alpha >= beta:
            break
    return meilleur


def choisir_coup(board, profondeur, hasard=None):
    """Le meilleur coup pour le joueur qui a la main ; entre deux coups égaux, au hasard."""
    hasard = hasard or random.Random()
    joueur = board.joueur
    coups = board.coups_possibles()
    hasard.shuffle(coups)

    meilleur_coup, meilleure_valeur = None, float("-inf")
    for trou in coups:
        suite = board.copie()
        suite.jouer(trou)
        valeur = minimax(suite, profondeur - 1, joueur, meilleure_valeur, float("inf"))
        if valeur > meilleure_valeur:
            meilleur_coup, meilleure_valeur = trou, valeur
    return meilleur_coup
