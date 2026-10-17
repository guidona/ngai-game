"""Tests des règles et de l'ordinateur. Lancer avec : python3 -m unittest discover tests"""

import os
import random
import subprocess
import sys
import unittest

RACINE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, RACINE)

from ngai.ordinateur import choisir_coup  # noqa: E402
from ngai.plateau import NORD, SUD, Board, Partie, trou_depuis_nom  # noqa: E402

A, B, C, D, E = range(5)
N5, N4, N3, N2, N1 = range(5, 10)


class TestDepart(unittest.TestCase):
    def test_cinquante_pions_cinq_par_trou(self):
        board = Board()
        self.assertEqual(board.cases, [5] * 10)
        self.assertEqual(sum(board.cases), 50)

    def test_le_sud_commence_et_peut_jouer(self):
        board = Board()
        self.assertEqual(board.joueur, SUD)
        self.assertEqual(board.coups_possibles(), [A, B, C, D, E])


class TestNoms(unittest.TestCase):
    def test_lettres_et_chiffres(self):
        self.assertEqual(trou_depuis_nom("a"), A)
        self.assertEqual(trou_depuis_nom(" E "), E)
        self.assertEqual(trou_depuis_nom("1"), N1)
        self.assertEqual(trou_depuis_nom("5"), N5)
        self.assertIsNone(trou_depuis_nom("x"))
        self.assertIsNone(trou_depuis_nom(""))


class TestCoups(unittest.TestCase):
    def test_il_faut_au_moins_deux_pions(self):
        board = Board([1, 2, 0, 0, 0, 3, 0, 0, 0, 0])
        self.assertEqual(board.coups_possibles(), [B])
        with self.assertRaises(ValueError):
            board.jouer(A)

    def test_on_ne_joue_que_ses_trous(self):
        board = Board()
        with self.assertRaises(ValueError):
            board.jouer(N1)

    def test_semis_dans_le_sens_trigonometrique(self):
        # D sème E, puis passe dans la rangée du Nord (5, puis 4).
        board = Board([0, 0, 0, 3, 0, 0, 0, 0, 0, 3])
        self.assertEqual(board.jouer(D), [])
        self.assertEqual(board.cases, [0, 0, 0, 0, 1, 1, 1, 0, 0, 3])

    def test_le_trou_de_depart_est_saute(self):
        # 12 pions : un tour complet sans A, puis B, C et D reçoivent un deuxième pion.
        board = Board([12, 0, 0, 0, 0, 0, 0, 0, 0, 1])
        prises = board.jouer(A)
        self.assertEqual(prises, [(D, 2)])
        self.assertEqual(board.cases, [0, 2, 2, 0, 1, 1, 1, 1, 1, 2])

    def test_la_main_passe(self):
        board = Board([3, 0, 0, 0, 0, 3, 0, 0, 0, 0])
        board.jouer(A)
        self.assertEqual(board.joueur, NORD)


class TestPrises(unittest.TestCase):
    def test_gain_simple(self):
        board = Board([2, 0, 1, 0, 0, 3, 0, 0, 0, 0])
        prises = board.jouer(A)
        self.assertEqual(prises, [(C, 2)])
        self.assertEqual(board.grenier, [2, 0])
        self.assertEqual(board.cases[C], 0)

    def test_quatre_pions_se_prennent_aussi(self):
        board = Board([2, 0, 3, 0, 0, 3, 0, 0, 0, 0])
        self.assertEqual(board.jouer(A), [(C, 4)])

    def test_trois_pions_ne_se_prennent_pas(self):
        board = Board([2, 0, 2, 0, 0, 3, 0, 0, 0, 0])
        self.assertEqual(board.jouer(A), [])
        self.assertEqual(board.cases[C], 3)

    def test_gain_cumulatif_vers_les_trous_suivants(self):
        # D sème E, 5 et 4. 4 a 2 pions : pris, puis 3 (2 pions) et 2 (4 pions). 5, derrière le
        # dernier trou semé, n'est pas pris.
        board = Board([0, 0, 0, 3, 0, 1, 1, 2, 4, 0])
        self.assertEqual(board.jouer(D), [(N4, 2), (N3, 2), (N2, 4)])
        self.assertEqual(board.cases, [0, 0, 0, 0, 1, 2, 0, 0, 0, 0])
        self.assertEqual(board.grenier, [8, 0])

    def test_la_prise_s_arrete_au_premier_trou_qui_ne_convient_pas(self):
        # 4 est pris ; 3 a 3 pions, donc la prise s'arrête, et 2 n'est pas pris.
        board = Board([0, 0, 0, 3, 0, 1, 1, 3, 2, 0])
        self.assertEqual(board.jouer(D), [(N4, 2)])
        self.assertEqual(board.cases[N3], 3)
        self.assertEqual(board.cases[N2], 2)

    def test_la_prise_ne_depasse_pas_l_angle(self):
        # C sème D et E. E a 2 pions et est pris (dans sa propre rangée) ; 5 en a 2 aussi, mais
        # il est de l'autre côté de l'angle.
        board = Board([0, 0, 2, 0, 1, 2, 0, 0, 0, 0])
        self.assertEqual(board.jouer(C), [(E, 2)])
        self.assertEqual(board.cases[N5], 2)

    def test_pas_de_prise_sur_un_trou_non_seme(self):
        # L'erreur de 2018 : D était pris alors qu'il n'avait pas été semé.
        board = Board([2, 0, 0, 2, 0, 3, 0, 0, 0, 0])
        self.assertEqual(board.jouer(A), [])
        self.assertEqual(board.cases[D], 2)
        self.assertEqual(board.grenier, [0, 0])


class TestFin(unittest.TestCase):
    def test_un_joueur_bloque_passe_son_tour(self):
        # Après D, le Nord n'a que des trous à 1 pion : le Sud rejoue.
        partie = Partie(Board([0, 0, 0, 3, 3, 0, 0, 0, 0, 0]))
        prises, passe = partie.jouer(D)
        self.assertTrue(passe)
        self.assertEqual(partie.joueur, SUD)

    def test_fin_et_ramassage(self):
        partie = Partie(Board([0, 0, 0, 0, 2, 0, 0, 0, 0, 0], grenier=(10, 20)))
        partie.jouer(E)
        # Personne ne peut plus jouer : le Nord ramasse les 2 pions de sa rangée.
        self.assertTrue(partie.terminee())
        self.assertEqual(partie.board.cases, [0] * 10)
        self.assertEqual(partie.board.grenier, [10, 22])

    def test_les_pions_sont_conserves(self):
        hasard = random.Random(0)
        partie = Partie()
        while not partie.terminee():
            partie.jouer(hasard.choice(partie.board.coups_possibles()))
            self.assertEqual(sum(partie.board.cases) + sum(partie.board.grenier), 50)
        self.assertEqual(sum(partie.board.grenier), 50)


class TestOrdinateur(unittest.TestCase):
    def test_prend_quand_il_peut(self):
        # Jouer B prend 4 pions en D ; les autres coups ne prennent rien.
        board = Board([0, 2, 0, 3, 0, 1, 0, 0, 0, 0])
        self.assertEqual(choisir_coup(board, 1, random.Random(0)), B)

    def test_joue_un_coup_permis(self):
        board = Board()
        for profondeur in (1, 4, 10):
            self.assertIn(choisir_coup(board, profondeur, random.Random(0)), board.coups_possibles())

    def test_le_niveau_difficile_bat_le_niveau_facile(self):
        victoires = 0
        for graine in range(10):
            hasard = random.Random(graine)
            partie = Partie()
            while not partie.terminee():
                profondeur = 10 if partie.joueur == NORD else 1
                partie.jouer(choisir_coup(partie.board, profondeur, hasard))
            victoires += partie.board.gagnant() == NORD
        self.assertGreaterEqual(victoires, 8)


class TestTerminal(unittest.TestCase):
    def jouer(self, saisie):
        return subprocess.run(
            [sys.executable, "ngai.py"], input=saisie, cwd=RACINE,
            capture_output=True, text=True, timeout=60,
        ).stdout

    def test_partie_contre_l_ordinateur_jusqu_au_bout(self):
        sortie = self.jouer("2\n" + "a\nb\nc\nd\ne\n" * 40)
        self.assertIn("Fin de la séance", sortie)
        self.assertNotIn("Traceback", sortie)

    def test_messages_d_erreur(self):
        sortie = self.jouer("1\nx\n1\nq\n")
        self.assertIn("« x » n'est pas un trou", sortie)
        self.assertIn("Le trou 1 n'est pas à vous", sortie)
        self.assertIn("Partie abandonnée", sortie)

    def test_fin_de_saisie(self):
        sortie = self.jouer("1\n")
        self.assertIn("Au revoir", sortie)


if __name__ == "__main__":
    unittest.main()
