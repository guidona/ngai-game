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

Le programme est une version **à deux joueurs dans le terminal**. Il gère le semis et les prises
(gain simple et gain cumulatif). Il commence avec une position d'essai de 8 pions, et ne gère pas
encore les 50 pions, plus de deux joueurs, la propriété des trous ni les séances : ces règles ne
sont pas encore entièrement connues. Le détail est dans [`REGLES.md`](REGLES.md).

Le carnet [`Code/ngay-ai-engine.ipynb`](Code/ngay-ai-engine.ipynb) contient un début de moteur
d'intelligence artificielle (un perceptron), qui n'est pas encore relié au jeu.

## Jouer

Il faut Python 3.

```sh
cd Code
python3 ngayMain.py
```

Le joueur 1 joue avec les lettres `A` à `E` (rangée du bas), le joueur 2 avec les chiffres `1` à
`5` (rangée du haut). Le nombre au-dessus et au-dessous du tableau est le grenier de chaque
joueur : les pions qu'il a pris.

```
      1   2   3   4   5
    +---+---+---+---+---+
    | 1 | 3 | 0 | 0 | 2 |
    +---+---+---+---+---+
    | 0 | 1 | 0 | 1 | 0 |
    +---+---+---+---+---+
      A   B   C   D   E
```

## Contribuer

Vous connaissez le Ngai ? L'aide la plus utile est de **répondre aux
[questions ouvertes](REGLES.md#questions-ouvertes)** sur les règles : ouvrez une *issue* sur GitHub,
ou écrivez-moi. Pas besoin de savoir programmer.

Pour le code : [`Code/ngayBoard.py`](Code/ngayBoard.py) contient le tableau et les règles,
[`Code/ngayMain.py`](Code/ngayMain.py) la boucle de jeu.

## Auteurs

Guy Mberebe Guidona et Oumar Djime Ratou.

---

*In English:* Ngai is a traditional Tupuri sowing game related to awalé. This project documents its
rules and implements them in Python; it is written in French because the people who know the game
and help with it are francophone.
