# Les règles du Ngay

Ce document rassemble ce que l'on sait des règles du Ngay, jeu traditionnel tupuri. Il reprend le
rapport de 2018 ([`Docs/ngay-ai.pdf`](Docs/ngay-ai.pdf)) et décrit ce que fait le programme actuel.

Les règles ne sont pas encore complètes. Les points manquants sont listés à la fin, dans
[Questions ouvertes](#questions-ouvertes) : si vous connaissez le jeu, c'est là que votre aide compte
le plus.

## Selon le rapport de 2018

### Le matériel

- Un tableau de **10 trous**, creusés dans le sol ou dans le sable, répartis en **deux rangées de 5**.
- **50 pions**.
- Les pions circulent dans le **sens trigonométrique** (inverse des aiguilles d'une montre).

![Le tableau de jeu du Ngay](Docs/images/ngay-platform.png)

Le Ngay ressemble à l'awalé d'Afrique de l'Ouest, mais il est plus élaboré.

### Les joueurs et les trous

- Le Ngay se joue à plusieurs : **2 joueurs** idéalement, **10 au maximum**.
- Au début, on **distribue les trous** entre les joueurs. Pendant une séance, les propriétaires ne
  changent pas de trous.
- À la fin d'une séance, on constate à qui appartient chaque trou, et on refait la répartition selon
  les pions gagnés par chacun.
- Pour être **propriétaire légitime** d'un trou, il faut y mettre **au moins 3 pions** ; sinon, le
  trou passe à un autre joueur.

### Le but du jeu

- Le but est de prendre le plus de pions possible à ses adversaires.
- Le jeu est une **suite de séances**. Il se termine quand un seul joueur a gagné tous les trous de
  ses adversaires.
- Un joueur a gagné lorsqu'il a pris tous les pions, ou **au moins 48**, et occupe ainsi tous les
  trous du tableau.

### Les prises

On ne prend jamais qu'un **nombre pair de pions inférieur à 5**, c'est-à-dire **2 ou 4**, et cela
peut se faire dans **n'importe quel trou**. Il y a deux sortes de prises :

| | Gain simple | Gain cumulatif |
|---|---|---|
| Pions pris | 2 ou 4 | 2 ou 4 dans chacun des trous consécutifs qui remplissent la même condition |

Un **gain cumulatif** est une suite de gains simples. La suite de trous pris **ne doit pas dépasser
les angles de la rangée opposée**.

## Ce que fait le programme

Le programme ([`Code/`](Code/)) est une version **à deux joueurs dans le terminal**. Il applique les
règles de prise du rapport, et fait en plus des choix que le rapport ne précise pas. Ces choix sont
marqués *(choix du programme)* : ils sont à confirmer.

- **Le tableau.** Le joueur 1 (Sud) a la rangée du bas, trous `A` à `E`. Le joueur 2 (Nord) a la
  rangée du haut, trous `1` à `5`. Chaque joueur ne joue que depuis sa rangée. *(choix du
  programme)*
- **Le départ.** Le tableau commence avec une position d'essai de **8 pions**, pas les 50 du jeu
  réel, parce que la répartition de départ n'est pas encore connue.
- **Jouer un coup.** Le joueur choisit un de ses trous. Il faut que ce trou contienne **au moins
  2 pions** *(choix du programme)*. Les pions sont semés un par un dans les trous suivants, dans le
  sens trigonométrique, y compris chez l'adversaire. Un coup non valable redonne la main au même
  joueur.
- **Les prises.** Si le dernier trou semé contient 2 ou 4 pions, le joueur les prend (gain simple).
  La prise continue sur les trous **suivants, dans le sens du jeu**, tant qu'ils contiennent 2 ou 4
  pions (gain cumulatif). Elle s'arrête au bout de la rangée où elle se trouve. Les pions pris vont
  dans le grenier du joueur, affiché à côté du tableau.

  **Erreur connue :** si le dernier trou semé ne donne rien, le programme regarde quand même le trou
  suivant et le prend s'il contient 2 ou 4 pions. Exemple : avec 2 pions en `A` et 2 en `D`, jouer
  `A` sème en `B` et `C` (1 pion chacun), et le joueur prend les 2 pions de `D`, qui n'a pas été
  semé.
- **Passer son tour.** Si un joueur n'a aucun trou avec au moins 2 pions, la main passe à l'autre.
- **La fin.** La partie s'arrête quand plus aucun trou ne contient au moins 2 pions.
- **Pas encore programmé :** les 50 pions, plus de deux joueurs, la propriété des trous (règle des
  3 pions), les séances et la redistribution des trous, la victoire à 48 pions.

## Questions ouvertes

Le rapport s'arrête avant d'expliquer ces points. Pour chacun, la réponse de quelqu'un qui joue au
Ngay permettra de compléter les règles puis le programme.

1. **La répartition de départ.** Comment les 50 pions sont-ils placés au début ? Combien par trou ?
2. **Le premier coup.** Qui commence, et comment le décide-t-on ?
3. **Les trous jouables.** Peut-on jouer un trou qui ne contient qu'un seul pion ? Peut-on jouer
   un trou qui n'est pas à soi ?
4. **Le semis.** Quand un trou contient beaucoup de pions et que l'on fait le tour du tableau,
   saute-t-on le trou de départ ?
5. **Le sens des prises cumulatives.** Après le dernier trou semé, la prise continue-t-elle vers
   les trous suivants (comme dans le programme) ou vers les trous précédents (comme à l'awalé) ?
6. **Les angles.** Que veut dire exactement « ne pas dépasser les angles de la rangée opposée » ?
   Peut-on prendre dans sa propre rangée ?
7. **Les trous des joueurs.** Comment les trous sont-ils répartis au début d'une partie à 2, à 3, à
   10 joueurs ? Comment s'applique la règle des 3 pions ?
8. **La fin d'une séance.** Quand une séance se termine-t-elle ? Que deviennent les pions restés sur
   le tableau ?
9. **La redistribution.** Comment refait-on la répartition des trous selon les pions gagnés ?
10. **Le nombre de joueurs.** Le rapport parle de 2 à 10 joueurs, mais aussi d'une version « pour
    cinq joueurs ». Quelle est la règle habituelle ?
