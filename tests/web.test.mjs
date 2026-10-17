// Vérifie que la version web (web/ngai.js) applique exactement les mêmes règles que la version
// Python. Lancer avec : node --test tests/
import { execFileSync } from "node:child_process";
import { strict as assert } from "node:assert";
import { test } from "node:test";
import { fileURLToPath } from "node:url";

import { Board, NIVEAUX, Partie, SUD, choisirCoup, valeursDesCoups } from "../web/ngai.js";

const reference = fileURLToPath(new URL("reference.py", import.meta.url));
const python = process.env.PYTHON || "python3";
const parties = JSON.parse(execFileSync(python, [reference], { maxBuffer: 64 * 1024 * 1024 }));

test("les parties de référence se rejouent à l'identique", () => {
  let total = 0;
  for (const coups of parties) {
    const premier = coups[0].avant;
    const partie = new Partie(new Board(premier.cases, premier.joueur, premier.grenier));
    for (const coup of coups) {
      assert.deepEqual(
        { cases: partie.board.cases, joueur: partie.joueur, grenier: partie.board.grenier },
        coup.avant,
      );
      const { prises, passe } = partie.jouer(coup.trou);
      assert.deepEqual(prises, coup.prises);
      assert.equal(passe, coup.passe);
      assert.deepEqual(
        { cases: partie.board.cases, joueur: partie.joueur, grenier: partie.board.grenier },
        coup.apres,
      );
      assert.equal(partie.raisonFin, coup.raison_fin);
      total += 1;
    }
  }
  assert.ok(total > 500, `seulement ${total} coups comparés`);
});

test("l'ordinateur évalue les coups comme la version Python", () => {
  for (const coups of parties.slice(0, 10)) {
    for (const coup of coups) {
      const { cases, joueur, grenier } = coup.avant;
      const valeurs = valeursDesCoups(new Board(cases, joueur, grenier), 4);
      assert.deepEqual(
        Object.fromEntries(Object.entries(valeurs).map(([t, v]) => [t, v])),
        coup.valeurs,
      );
    }
  }
});

test("le semis est renvoyé trou par trou, sans le trou de départ", () => {
  const board = new Board([12, 0, 0, 0, 0, 0, 0, 0, 0, 1]);
  const { semis } = board.jouer(0);
  assert.deepEqual(semis, [1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2, 3]);
});

test("l'ordinateur difficile choisit vite un coup permis", () => {
  const board = new Board();
  const debut = Date.now();
  const coup = choisirCoup(board, NIVEAUX.difficile);
  assert.ok(board.coupsPossibles(SUD).includes(coup));
  assert.ok(Date.now() - debut < 2000);
});
