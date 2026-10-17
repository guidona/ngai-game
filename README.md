# Ngai

Le Ngai est un jeu traditionnel tupuri, un jeu de semis proche de l'awalé : des pions circulent dans
deux rangées de cinq trous, et l'on gagne en prenant ceux de ses adversaires.

Ce projet a deux buts : **écrire les règles complètes du Ngai** et **en faire un programme jouable**.
Il a commencé en 2018 dans le cadre d'un cours d'intelligence artificielle à l'École Nationale
Supérieure Polytechnique de Maroua.

Le rapport, le code et les fichiers de 2018 écrivent le nom du jeu « Ngay » ; ils sont gardés tels
quels.

- **Les règles :** [`REGLES.md`](REGLES.md), avec ce que l'on sait, ce que fait le programme, et les
  questions encore ouvertes.
- **Le rapport de 2018 :** [`Docs/ngay-ai.pdf`](Docs/ngay-ai.pdf) (source LaTeX :
  [`Docs/ngay-ai.tex`](Docs/ngay-ai.tex)).

## Où en est le projet

Le programme joue **une séance complète à deux joueurs**, dans le terminal : à deux, ou contre
l'ordinateur (trois niveaux). Il gère les 50 pions, le semis, les prises (gain simple et gain
cumulatif) et la fin de la séance.

Le rapport ne dit pas tout. Quand une règle manque, le programme fait un **choix provisoire**, noté
dans [`REGLES.md`](REGLES.md) avec la question qui permettra de le confirmer. Pas encore programmé :
plus de deux joueurs, la propriété des trous et la suite des séances.

## Jouer

Il faut Python 3.9 ou plus récent, sans rien d'autre à installer.

```sh
cd Code
python3 ngayMain.py
```

Choisissez de jouer à deux ou contre l'ordinateur. Le joueur 1 (Sud) joue avec les lettres `A` à
`E`, le joueur 2 (Nord) avec les chiffres `1` à `5`. Tapez `?` pour l'aide, `q` pour quitter.

```
    Joueur 2 (Nord) : 0 pion

      1    2    3    4    5
    +----+----+----+----+----+
    |  8 |  2 |  7 |  0 |  7 |
    +----+----+----+----+----+
    |  8 |  2 |  8 |  1 |  7 |
    +----+----+----+----+----+
      A    B    C    D    E

    Joueur 1 (Sud) : 0 pion

Joueur 2 (Nord) joue 4.

Joueur 1 (Sud), quel trou jouez-vous ? (? aide, q quitter)
```

## Contribuer

Vous connaissez le Ngai ? L'aide la plus utile est de **répondre aux
[questions ouvertes](REGLES.md#questions-ouvertes)** sur les règles : ouvrez une *issue* sur GitHub,
ou écrivez-moi. Pas besoin de savoir programmer.

Pour le code :

- [`Code/ngayBoard.py`](Code/ngayBoard.py) : le tableau et les règles ;
- [`Code/ordinateur.py`](Code/ordinateur.py) : l'adversaire ordinateur (minimax avec élagage
  alpha-bêta) ;
- [`Code/ngayMain.py`](Code/ngayMain.py) : le jeu dans le terminal ;
- [`tests/`](tests/) : les tests, à lancer avec `python3 -m unittest discover tests`. Ils tournent
  aussi sur GitHub à chaque envoi.

Le carnet [`Code/ngay-ai-engine.ipynb`](Code/ngay-ai-engine.ipynb) est le début de 2018 d'un
moteur à base de perceptron ; il n'est pas utilisé par le jeu.

## Auteurs

Guy Mberebe Guidona et Oumar Djime Ratou.

---

*In English:* Ngai is a traditional Tupuri sowing game related to awalé. This project documents its
rules and implements them in Python, with a computer opponent. It is written in French because the
people who know the game and help with it are francophone.
