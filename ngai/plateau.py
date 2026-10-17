"""Le plateau et les règles du Ngai, pour deux joueurs.

Les règles que le rapport de 2018 ne précise pas sont des choix provisoires du programme ; ils
sont décrits dans docs/regles.md (section « Ce que fait le programme »).

Les trous sont numérotés de 0 à 9 dans le sens trigonométrique : 0 à 4 forment la rangée du Sud
(A à E, de gauche à droite), 5 à 9 la rangée du Nord (5 à 1, de droite à gauche).
"""

TROUS = 10
PIONS_PAR_TROU = 5
MINIMUM_POUR_JOUER = 2
PRISES = (2, 4)

SUD, NORD = 0, 1
NOMS_JOUEURS = ("Joueur 1 (Sud)", "Joueur 2 (Nord)")
NOMS_TROUS = ("A", "B", "C", "D", "E", "5", "4", "3", "2", "1")


def rangee(joueur):
    """Les trous d'un joueur."""
    return range(0, 5) if joueur == SUD else range(5, 10)


def nom_trou(trou):
    return NOMS_TROUS[trou]


def trou_depuis_nom(nom):
    """Le trou correspondant à un nom (« a », « C », « 3 »…), ou None."""
    nom = nom.strip().upper()
    return NOMS_TROUS.index(nom) if nom in NOMS_TROUS else None


class Board:
    """Une position : les pions dans chaque trou, les greniers, et le joueur qui a la main."""

    def __init__(self, cases=None, joueur=SUD, grenier=(0, 0)):
        self.cases = list(cases) if cases is not None else [PIONS_PAR_TROU] * TROUS
        self.joueur = joueur
        self.grenier = list(grenier)

    def copie(self):
        return Board(self.cases, self.joueur, self.grenier)

    def coups_possibles(self, joueur=None):
        """Les trous que le joueur peut jouer : les siens, avec au moins 2 pions."""
        joueur = self.joueur if joueur is None else joueur
        return [t for t in rangee(joueur) if self.cases[t] >= MINIMUM_POUR_JOUER]

    def jouer(self, trou):
        """Joue un trou du joueur qui a la main.

        Renvoie la liste des prises, sous forme de (trou, pions), dans l'ordre où elles sont
        faites. Lève ValueError si le coup n'est pas permis.
        """
        if trou not in self.coups_possibles():
            raise ValueError("coup non permis : " + nom_trou(trou))

        # Le semis : un pion par trou, dans le sens trigonométrique, en sautant le trou de départ.
        pions, self.cases[trou] = self.cases[trou], 0
        position = trou
        while pions:
            position = (position + 1) % TROUS
            if position == trou:
                continue
            self.cases[position] += 1
            pions -= 1

        # Les prises : le dernier trou semé s'il contient 2 ou 4 pions, puis les trous
        # suivants tant qu'ils remplissent la même condition, sans dépasser l'angle de la rangée.
        prises = []
        rangee_finale = position // 5
        while position // 5 == rangee_finale and self.cases[position] in PRISES:
            prises.append((position, self.cases[position]))
            self.grenier[self.joueur] += self.cases[position]
            self.cases[position] = 0
            position += 1

        # La main passe à l'adversaire, sauf s'il ne peut pas jouer.
        adversaire = 1 - self.joueur
        if self.coups_possibles(adversaire):
            self.joueur = adversaire
        return prises

    def terminee(self):
        """La séance est finie quand aucun des deux joueurs ne peut jouer."""
        return not self.coups_possibles(SUD) and not self.coups_possibles(NORD)

    def ramasser(self):
        """En fin de séance, chaque joueur prend les pions restés dans sa rangée."""
        for joueur in (SUD, NORD):
            for t in rangee(joueur):
                self.grenier[joueur] += self.cases[t]
                self.cases[t] = 0

    def gagnant(self):
        """Le joueur qui a le plus de pions dans son grenier, ou None en cas d'égalité."""
        if self.grenier[SUD] == self.grenier[NORD]:
            return None
        return SUD if self.grenier[SUD] > self.grenier[NORD] else NORD

    def etat(self):
        return (tuple(self.cases), self.joueur)


class Partie:
    """Une séance complète : le plateau, plus la détection des positions répétées.

    Sans prise, les pions peuvent tourner indéfiniment ; la séance s'arrête donc aussi quand une
    position se répète.
    """

    def __init__(self, board=None):
        self.board = board or Board()
        self.vues = {self.board.etat()}
        self.raison_fin = None

    @property
    def joueur(self):
        return self.board.joueur

    def jouer(self, trou):
        """Joue un coup. Renvoie (prises, passe) : passe est vrai si l'adversaire saute son tour."""
        joueur = self.board.joueur
        prises = self.board.jouer(trou)
        passe = self.board.joueur == joueur and not self.board.terminee()

        if self.board.terminee():
            self.raison_fin = "plus aucun coup n'est possible"
        elif self.board.etat() in self.vues:
            self.raison_fin = "la même position est revenue"
        self.vues.add(self.board.etat())

        if self.raison_fin:
            self.board.ramasser()
        return prises, passe

    def terminee(self):
        return self.raison_fin is not None
