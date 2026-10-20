// Les règles du Ngai et l'adversaire ordinateur, pour la version web.
//
// C'est la traduction de ngai/plateau.py et ngai/ordinateur.py : les mêmes règles, les mêmes noms.
// tests/web.test.mjs vérifie que les deux versions donnent les mêmes résultats ; toute
// modification des règles se fait donc des deux côtés.
//
// Les trous sont numérotés de 0 à 9 dans le sens trigonométrique : 0 à 4 forment la rangée du Sud
// (A à E, de gauche à droite), 5 à 9 la rangée du Nord (5 à 1, de droite à gauche).

export const TROUS = 10;
export const PIONS_PAR_TROU = 5;
export const MINIMUM_POUR_JOUER = 2;
export const PRISES = [2, 4];

export const SUD = 0;
export const NORD = 1;
export const NOMS_TROUS = ["A", "B", "C", "D", "E", "5", "4", "3", "2", "1"];
export const NIVEAUX = { facile: 1, moyen: 4, difficile: 10 };

export function rangee(joueur) {
  return joueur === SUD ? [0, 1, 2, 3, 4] : [5, 6, 7, 8, 9];
}

export function nomTrou(trou) {
  return NOMS_TROUS[trou];
}

export class Board {
  constructor(cases = null, joueur = SUD, grenier = [0, 0]) {
    this.cases = cases ? [...cases] : Array(TROUS).fill(PIONS_PAR_TROU);
    this.joueur = joueur;
    this.grenier = [...grenier];
  }

  copie() {
    return new Board(this.cases, this.joueur, this.grenier);
  }

  coupsPossibles(joueur = this.joueur) {
    return rangee(joueur).filter((t) => this.cases[t] >= MINIMUM_POUR_JOUER);
  }

  // Joue un trou du joueur qui a la main. Renvoie { semis, prises } : les trous semés dans
  // l'ordre, et les prises sous forme de [trou, pions].
  jouer(trou) {
    if (!this.coupsPossibles().includes(trou)) {
      throw new Error("coup non permis : " + nomTrou(trou));
    }

    // Le semis : un pion par trou, dans le sens trigonométrique. Quand on fait le tour du
    // tableau, le trou de départ reçoit aussi son pion.
    let pions = this.cases[trou];
    this.cases[trou] = 0;
    let position = trou;
    const semis = [];
    while (pions) {
      position = (position + 1) % TROUS;
      this.cases[position] += 1;
      semis.push(position);
      pions -= 1;
    }

    // Les prises : le dernier trou semé s'il contient 2 ou 4 pions, puis les trous suivants tant
    // qu'ils remplissent la même condition, sans dépasser l'angle de la rangée.
    const prises = [];
    const rangeeFinale = Math.floor(position / 5);
    while (Math.floor(position / 5) === rangeeFinale && PRISES.includes(this.cases[position])) {
      prises.push([position, this.cases[position]]);
      this.grenier[this.joueur] += this.cases[position];
      this.cases[position] = 0;
      position += 1;
    }

    // La main passe à l'adversaire, sauf s'il ne peut pas jouer.
    const adversaire = 1 - this.joueur;
    if (this.coupsPossibles(adversaire).length) this.joueur = adversaire;
    return { semis, prises };
  }

  terminee() {
    return !this.coupsPossibles(SUD).length && !this.coupsPossibles(NORD).length;
  }

  ramasser() {
    for (const joueur of [SUD, NORD]) {
      for (const t of rangee(joueur)) {
        this.grenier[joueur] += this.cases[t];
        this.cases[t] = 0;
      }
    }
  }

  gagnant() {
    if (this.grenier[SUD] === this.grenier[NORD]) return null;
    return this.grenier[SUD] > this.grenier[NORD] ? SUD : NORD;
  }

  etat() {
    return this.cases.join(",") + "|" + this.joueur;
  }
}

// Une séance complète : le plateau, plus la détection des positions répétées.
export class Partie {
  constructor(board = null) {
    this.board = board || new Board();
    this.vues = new Set([this.board.etat()]);
    this.raisonFin = null;
  }

  get joueur() {
    return this.board.joueur;
  }

  // Joue un coup. Renvoie { semis, prises, passe } : passe est vrai si l'adversaire saute son tour.
  jouer(trou) {
    const joueur = this.board.joueur;
    const { semis, prises } = this.board.jouer(trou);
    const passe = this.board.joueur === joueur && !this.board.terminee();

    if (this.board.terminee()) this.raisonFin = "plus aucun coup n'est possible";
    else if (this.vues.has(this.board.etat())) this.raisonFin = "la même position est revenue";
    this.vues.add(this.board.etat());

    if (this.raisonFin) this.board.ramasser();
    return { semis, prises, passe };
  }

  terminee() {
    return this.raisonFin !== null;
  }
}

// L'ordinateur : minimax avec élagage alpha-bêta, comme ngai/ordinateur.py.

export function evaluer(board, joueur) {
  if (board.terminee()) {
    board = board.copie();
    board.ramasser();
  }
  return board.grenier[joueur] - board.grenier[1 - joueur];
}

export function minimax(board, profondeur, joueur, alpha, beta) {
  if (profondeur === 0 || board.terminee()) return evaluer(board, joueur);

  const maximiser = board.joueur === joueur;
  let meilleur = maximiser ? -Infinity : Infinity;
  for (const trou of board.coupsPossibles()) {
    const suite = board.copie();
    suite.jouer(trou);
    const valeur = minimax(suite, profondeur - 1, joueur, alpha, beta);
    if (maximiser) {
      meilleur = Math.max(meilleur, valeur);
      alpha = Math.max(alpha, valeur);
    } else {
      meilleur = Math.min(meilleur, valeur);
      beta = Math.min(beta, valeur);
    }
    if (alpha >= beta) break;
  }
  return meilleur;
}

// La valeur exacte de chaque coup possible, sans élagage à la racine (sert aux tests).
export function valeursDesCoups(board, profondeur) {
  const valeurs = {};
  for (const trou of board.coupsPossibles()) {
    const suite = board.copie();
    suite.jouer(trou);
    valeurs[trou] = minimax(suite, profondeur - 1, board.joueur, -Infinity, Infinity);
  }
  return valeurs;
}

// Le meilleur coup pour le joueur qui a la main ; entre deux coups égaux, au hasard.
export function choisirCoup(board, profondeur, hasard = Math.random) {
  const joueur = board.joueur;
  const coups = board.coupsPossibles();
  for (let i = coups.length - 1; i > 0; i--) {
    const j = Math.floor(hasard() * (i + 1));
    [coups[i], coups[j]] = [coups[j], coups[i]];
  }

  let meilleurCoup = null;
  let meilleureValeur = -Infinity;
  for (const trou of coups) {
    const suite = board.copie();
    suite.jouer(trou);
    const valeur = minimax(suite, profondeur - 1, joueur, meilleureValeur, Infinity);
    if (valeur > meilleureValeur) {
      meilleurCoup = trou;
      meilleureValeur = valeur;
    }
  }
  return meilleurCoup;
}
