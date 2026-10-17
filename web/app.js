// L'interface web : le plateau sur l'illustration, le semis animé, et le tour de l'ordinateur.
import { Board, NIVEAUX, NORD, Partie, SUD, choisirCoup, nomTrou } from "./ngai.js";

// La position des trous et des greniers sur l'illustration, en pourcentage de sa largeur (x, d)
// et de sa hauteur (y). d est le diamètre.
const TROU_D = 14.4;
const COLONNES = [15.3, 32.6, 50.1, 67.6, 84.9];
const GEOMETRIE = {
  trous: [
    ...COLONNES.map((x) => ({ x, y: 60.9 })), // A à E, en bas, de gauche à droite
    ...[...COLONNES].reverse().map((x) => ({ x, y: 39.2 })), // 5 à 1, en haut, de droite à gauche
  ],
  greniers: [
    { x: 50.3, y: 86.3, d: 19 }, // Sud, en bas
    { x: 50.4, y: 13.4, d: 19 }, // Nord, en haut
  ],
};

const DUREE_PION = 170;
const DUREE_PRISE = 650;
const REFLEXION = 500;

const plateau = document.getElementById("plateau");
const message = document.getElementById("message");
const choixMode = document.getElementById("mode");

let partie;
let niveau;
let occupe = false;
let generation = 0; // change à chaque nouvelle partie, pour arrêter une animation en cours

const attendre = (ms) => new Promise((ok) => setTimeout(ok, ms));
const pions = (n) => `${n} pion${n > 1 ? "s" : ""}`;

function nomJoueur(joueur) {
  if (niveau) return joueur === SUD ? "Vous" : "L'ordinateur";
  return joueur === SUD ? "Joueur 1 (Sud)" : "Joueur 2 (Nord)";
}

// --- Construction du plateau ---------------------------------------------------------------

function placer(element, { x, y, d }) {
  element.style.left = `${x}%`;
  element.style.top = `${y}%`;
  element.style.width = `${d}%`;
}

const boutons = GEOMETRIE.trous.map((position, trou) => {
  const bouton = document.createElement("button");
  bouton.className = trou < 5 ? "trou sud" : "trou nord";
  bouton.dataset.trou = trou;
  placer(bouton, { ...position, d: TROU_D });
  bouton.innerHTML = `<span class="pions"></span><span class="badge"><span class="nom">${nomTrou(trou)}</span><span class="compte"></span></span>`;
  bouton.addEventListener("click", () => jouerHumain(trou));
  plateau.append(bouton);
  return bouton;
});

const greniers = GEOMETRIE.greniers.map((position, joueur) => {
  const grenier = document.createElement("div");
  grenier.className = "grenier";
  placer(grenier, position);
  grenier.innerHTML = `<span class="pions"></span><span class="etiquette"><span class="qui"></span><strong class="total"></strong></span>`;
  grenier.querySelector(".qui").dataset.joueur = joueur;
  plateau.append(grenier);
  return grenier;
});

// Les pions d'un trou, disposés en spirale (comme les graines d'un tournesol) : chaque nouveau
// pion s'ajoute au bord sans déplacer les autres.
function dessinerPions(conteneur, n) {
  const existants = conteneur.children.length;
  for (let i = existants; i < n; i++) {
    const pion = document.createElement("span");
    pion.className = "pion";
    pion.style.setProperty("--teinte", `${(i * 47) % 30}`);
    conteneur.append(pion);
  }
  while (conteneur.children.length > n) conteneur.lastChild.remove();

  const taille = Math.max(9, Math.min(24, 62 / Math.sqrt(Math.max(n, 1))));
  const rayonMax = 40 - taille / 2;
  [...conteneur.children].forEach((pion, i) => {
    const r = n === 1 ? 0 : rayonMax * Math.sqrt((i + 0.5) / n);
    const angle = i * 2.39996; // l'angle d'or
    pion.style.width = `${taille}%`;
    pion.style.left = `${50 + r * Math.cos(angle)}%`;
    pion.style.top = `${50 + r * Math.sin(angle)}%`;
  });
}

// --- Affichage -----------------------------------------------------------------------------

function afficher(board, { jouables = [], surbrillance = [] } = {}) {
  boutons.forEach((bouton, trou) => {
    const n = board.cases[trou];
    dessinerPions(bouton.querySelector(".pions"), n);
    bouton.querySelector(".compte").textContent = n;
    const jouable = jouables.includes(trou);
    bouton.disabled = !jouable;
    bouton.classList.toggle("jouable", jouable);
    bouton.classList.toggle("surbrillance", surbrillance.includes(trou));
    bouton.setAttribute("aria-label", `Trou ${nomTrou(trou)}, ${pions(n)}${jouable ? ", jouable" : ""}`);
  });
  greniers.forEach((grenier, joueur) => {
    dessinerPions(grenier.querySelector(".pions"), board.grenier[joueur]);
    grenier.querySelector(".qui").textContent = nomJoueur(joueur);
    grenier.querySelector(".total").textContent = board.grenier[joueur];
    grenier.classList.toggle("actif", !partie.terminee() && partie.joueur === joueur);
  });
}

function jouablesPourHumain() {
  if (occupe || partie.terminee()) return [];
  if (niveau && partie.joueur === NORD) return [];
  return partie.board.coupsPossibles();
}

// Ajoute « à qui de jouer » aux lignes qui décrivent le dernier coup.
function direTour(lignes = []) {
  if (partie.terminee() || (niveau && partie.joueur === NORD)) return;
  const tour = niveau ? "À vous de jouer." : `Au j${nomJoueur(partie.joueur).slice(1)} de jouer.`;
  message.textContent = [...lignes, tour].join(" ");
}

// --- Un coup, animé ------------------------------------------------------------------------

async function jouerCoup(trou) {
  const ma = generation;
  occupe = true;
  const joueur = partie.joueur;
  const avant = partie.board.copie();
  const { semis, prises, passe } = partie.jouer(trou);

  // Le semis, pion par pion.
  const vue = avant.copie();
  vue.cases[trou] = 0;
  afficher(vue, { surbrillance: [trou] });
  for (const position of semis) {
    await attendre(DUREE_PION);
    if (ma !== generation) return;
    vue.cases[position] += 1;
    afficher(vue, { surbrillance: [position] });
  }

  // Les prises vont au grenier du joueur.
  const lignes = [`${nomJoueur(joueur)} ${niveau && joueur === SUD ? "jouez" : "joue"} ${nomTrou(trou)}.`];
  if (prises.length) {
    const total = prises.reduce((somme, [, n]) => somme + n, 0);
    const sorte = prises.length === 1 ? "Gain simple" : "Gain cumulatif";
    lignes.push(`${sorte} : ${pions(total)} pris (${prises.map(([t]) => nomTrou(t)).join(", ")}).`);
    afficher(vue, { surbrillance: prises.map(([t]) => t) });
    await attendre(DUREE_PRISE);
    if (ma !== generation) return;
    for (const [t, n] of prises) {
      vue.cases[t] = 0;
      vue.grenier[joueur] += n;
    }
    afficher(vue);
  }
  if (passe) lignes.push(`${nomJoueur(1 - joueur)} ne peut pas jouer et passe son tour.`);

  await attendre(DUREE_PION);
  if (ma !== generation) return;
  occupe = false;
  afficher(partie.board, { jouables: jouablesPourHumain() });
  message.textContent = lignes.join(" ");

  if (partie.terminee()) return finir();
  if (niveau && partie.joueur === NORD) return tourOrdinateur();
  direTour(lignes);
}

async function tourOrdinateur() {
  const ma = generation;
  occupe = true;
  afficher(partie.board);
  const avant = message.textContent;
  message.textContent = `${avant} L'ordinateur réfléchit…`.trim();
  await attendre(REFLEXION);
  if (ma !== generation) return;
  await jouerCoup(choisirCoup(partie.board, NIVEAUX[niveau]));
}

function jouerHumain(trou) {
  if (!jouablesPourHumain().includes(trou)) return;
  jouerCoup(trou);
}

function finir() {
  const board = partie.board;
  afficher(board);
  const gagnant = board.gagnant();
  let resultat;
  if (gagnant === null) resultat = `Égalité, ${pions(board.grenier[SUD])} partout.`;
  else if (niveau) {
    resultat = gagnant === SUD
      ? `Vous gagnez, ${board.grenier[SUD]} pions contre ${board.grenier[NORD]} !`
      : `L'ordinateur gagne, ${board.grenier[NORD]} pions contre ${board.grenier[SUD]}.`;
  } else {
    resultat = `${nomJoueur(gagnant)} gagne, ${board.grenier[gagnant]} pions contre ${board.grenier[1 - gagnant]}.`;
  }
  message.textContent = `Fin de la séance : ${partie.raisonFin}. Chacun prend les pions de sa rangée. ${resultat}`;
}

// --- Nouvelle partie -----------------------------------------------------------------------

function nouvellePartie() {
  generation += 1;
  occupe = false;
  niveau = choixMode.value || null;
  try {
    localStorage.setItem("ngai-mode", choixMode.value);
  } catch {}
  partie = new Partie(new Board());
  afficher(partie.board, { jouables: jouablesPourHumain() });
  message.textContent = niveau
    ? "Vous jouez la rangée du bas, l'ordinateur celle du haut. Vous commencez : choisissez un trou."
    : "Le joueur 1 (Sud) joue la rangée du bas, le joueur 2 (Nord) celle du haut. Le joueur 1 commence.";
}

try {
  const mode = localStorage.getItem("ngai-mode");
  if (mode !== null && [...choixMode.options].some((o) => o.value === mode)) choixMode.value = mode;
} catch {}

document.getElementById("nouvelle").addEventListener("click", nouvellePartie);
choixMode.addEventListener("change", nouvellePartie);
nouvellePartie();

// Pour les tests et le débogage depuis la console.
window.ngai = { get partie() { return partie; } };
