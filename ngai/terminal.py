"""Jouer au Ngai dans le terminal, à deux ou contre l'ordinateur."""

import sys

from .ordinateur import NIVEAUX, choisir_coup
from .plateau import NOMS_JOUEURS, NORD, SUD, Partie, nom_trou, rangee, trou_depuis_nom

AIDE = """
Règles en bref (le détail est dans docs/regles.md) :
  - Chaque joueur a une rangée de 5 trous : A à E pour le Sud, 1 à 5 pour le Nord.
  - On joue un de ses trous qui contient au moins 2 pions. Les pions sont semés un par un dans
    les trous suivants, dans le sens inverse des aiguilles d'une montre.
  - Si le dernier trou semé contient 2 ou 4 pions, on les prend. On prend aussi les trous
    suivants de la même rangée tant qu'ils contiennent 2 ou 4 pions.
  - Un joueur qui ne peut pas jouer passe son tour. La séance finit quand personne ne peut
    jouer ; chacun prend alors les pions de sa rangée. Le plus gros grenier gagne.
"""


def pions(n):
    """« 1 pion », « 0 pion », « 3 pions »."""
    return "{} pion{}".format(n, "s" if n > 1 else "")


def afficher(partie, messages):
    board = partie.board
    if sys.stdout.isatty():
        print("\033[2J\033[H", end="")
    ligne = "    +" + "----+" * 5
    nord = [board.cases[t] for t in range(9, 4, -1)]
    sud = [board.cases[t] for t in range(0, 5)]
    print()
    print("    {} : {}".format(NOMS_JOUEURS[NORD], pions(board.grenier[NORD])))
    print()
    print("      1    2    3    4    5")
    print(ligne)
    print("    |" + "|".join("{:>3} ".format(n) for n in nord) + "|")
    print(ligne)
    print("    |" + "|".join("{:>3} ".format(n) for n in sud) + "|")
    print(ligne)
    print("      A    B    C    D    E")
    print()
    print("    {} : {}".format(NOMS_JOUEURS[SUD], pions(board.grenier[SUD])))
    print()
    for message in messages:
        print(message)
    if messages:
        print()


def decrire_coup(nom, trou, prises, passe, adversaire):
    messages = ["{} joue {}.".format(nom, nom_trou(trou))]
    if prises:
        total = sum(pions for _, pions in prises)
        trous = ", ".join(nom_trou(t) for t, _ in prises)
        sorte = "Gain simple" if len(prises) == 1 else "Gain cumulatif"
        messages.append("{} : {} pris ({}).".format(sorte, pions(total), trous))
    if passe:
        messages.append("{} ne peut pas jouer et passe son tour.".format(adversaire))
    return messages


def demander_coup(partie, nom):
    """Demande un trou au joueur jusqu'à ce qu'il soit valable. Renvoie None pour quitter."""
    possibles = partie.board.coups_possibles()
    while True:
        reponse = input("{}, quel trou jouez-vous ? (? aide, q quitter) ".format(nom)).strip()
        if reponse.lower() in ("q", "quitter"):
            return None
        if reponse == "?":
            print(AIDE)
            continue
        trou = trou_depuis_nom(reponse)
        if trou in possibles:
            return trou
        jouables = ", ".join(sorted(nom_trou(t) for t in possibles))
        if trou is None:
            print("« {} » n'est pas un trou. Trous jouables : {}.".format(reponse, jouables))
        elif trou not in rangee(partie.joueur):
            print("Le trou {} n'est pas à vous. Trous jouables : {}.".format(nom_trou(trou), jouables))
        else:
            print("Le trou {} a {} : il en faut au moins 2. Trous jouables : {}.".format(
                nom_trou(trou), pions(partie.board.cases[trou]), jouables))


def choisir_mode():
    print("Ngai, jeu traditionnel tupuri")
    print()
    print("  1. Deux joueurs")
    print("  2. Contre l'ordinateur, facile")
    print("  3. Contre l'ordinateur, moyen")
    print("  4. Contre l'ordinateur, difficile")
    print()
    modes = {"1": None, "2": "facile", "3": "moyen", "4": "difficile"}
    while True:
        reponse = input("Votre choix (1 à 4) : ").strip()
        if reponse in modes:
            return modes[reponse]
        print("Tapez 1, 2, 3 ou 4.")


def jouer(niveau):
    partie = Partie()
    noms = list(NOMS_JOUEURS)
    if niveau:
        noms[NORD] = "L'ordinateur"
    messages = ["{} commence.".format(noms[SUD])]

    while not partie.terminee():
        afficher(partie, messages)
        joueur = partie.joueur
        if niveau and joueur == NORD:
            trou = choisir_coup(partie.board, NIVEAUX[niveau])
        else:
            trou = demander_coup(partie, noms[joueur])
            if trou is None:
                print("Partie abandonnée.")
                return
        prises, passe = partie.jouer(trou)
        messages = decrire_coup(noms[joueur], trou, prises, passe, noms[1 - joueur])

    board = partie.board
    messages.append("Fin de la séance : {}. Chacun prend les pions de sa rangée.".format(
        partie.raison_fin))
    gagnant = board.gagnant()
    if gagnant is None:
        messages.append("Égalité, {} partout.".format(pions(board.grenier[SUD])))
    else:
        messages.append("{} gagne, {} contre {}.".format(
            noms[gagnant], pions(board.grenier[gagnant]), board.grenier[1 - gagnant]))
    afficher(partie, messages)


def main():
    try:
        jouer(choisir_mode())
    except (EOFError, KeyboardInterrupt):
        print()
        print("Au revoir.")

