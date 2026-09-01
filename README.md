# Modèle vivant QC127 — projection électorale québécoise

Projection de sièges pour l'élection générale du **5 octobre 2026**, sur la carte
de **127 circonscriptions** établie par la Loi visant à assurer la représentation
effective des électeurs (2026, chapitre 15).

Dépôt privé. Travail personnel, sans affiliation à aucun parti ni à aucune firme.

## Ce que le modèle fait

Il traduit des intentions de vote en sièges. Ce n'est pas une prévision du scrutin,
c'est une lecture du présent : *si le vote avait lieu aujourd'hui*.

La chaîne comporte cinq maillons :

1. **Agrégation.** Le niveau national et sa pente sont estimés par régression
   linéaire locale pondérée sur l'ensemble des sondages publiés, et non sur le
   dernier paru. Une moyenne simple retarde sur une série en tendance.
2. **Effets de maison.** Estimés par firme et rétrécis vers zéro selon le nombre
   de sondages de cette firme.
3. **Décalages régionaux.** Mesurés comme l'écart région − province *à l'intérieur
   de chaque sondage*, ce qui annule l'effet de maison de la firme.
4. **Transposition.** Les 4 112 821 votes réels de 2022 sont réaffectés sur la carte
   de 2026 au prorata des électeurs transférés, calculés par intersection des
   sections de vote 2026 avec les circonscriptions 2022.
5. **Scénarios.** Six lectures, dont une couche linguistique pondérée parti par
   parti selon ce que la langue explique réellement du vote de 2022.

## Ce qu'il ne fait pas

- Aucune simulation probabiliste : il donne des chiffres, pas des probabilités.
- Aucun effet de candidature ni de notoriété locale.
- Aucune modélisation de la participation : elle est supposée semblable à 2022.
- La transposition suppose l'homogénéité partisane à l'intérieur des anciennes
  circonscriptions — les résultats par bureau de vote existent, mais pas les
  polygones des bureaux historiques.

## Structure

```
├── ModeleVivantQC127_v*.xlsx   modèle, formules vivantes, intrants en bleu
├── RUNBOOK.md                  procédure d'exploitation et contrôles
├── GUIDE-LECTURE.md            explication pour non-spécialistes
├── TODO.md                     backlog priorisé
├── PROMPT-*.md                 prompts de délégation
├── data/                       séries de sondages (CSV)
├── livrables/                  page « Tendances Québec 2026 »
└── .work/                      scripts du pipeline
```

## Mettre à jour

Voir `RUNBOOK.md`. En résumé : déposer le PDF dans `Data/`, saisir les intentions
par région dans l'onglet `Sondages`, ajouter la ligne nationale dans
`data/sondages_national.csv`, recalculer, passer les huit contrôles, puis

```bash
python3 .work/maj_artefact.py --classeur <le classeur> --recalculer
```

## Données non versionnées

Volontairement absents du dépôt :

| Quoi | Pourquoi | Où les reprendre |
|---|---|---|
| `2018/` `2022/` `2026/` | 76 Mo de shapefiles et de résultats par bureau | Élections Québec, données ouvertes |
| `Data/*.pdf` | Rapports des firmes, sous droit d'auteur | Sites des firmes |
| `Data/*.xls` | Recensement 2021 par circonscription 2026 | Élections Québec |
| `outputs/` | Sorties de construction, régénérables | — |

Les **chiffres** extraits de ces documents sont des faits et vivent dans
`data/*.csv`, qui est versionné.

## Avertissement

La relation intentions-sièges n'a rien de proportionnel. Dans le régime actuel, la
CAQ se trouve dans la zone où deux points de pourcentage déplacent des dizaines de
circonscriptions. Un décompte de sièges se cite avec cet avertissement, ou ne se
cite pas.

## Sources

Élections Québec (résultats, cartes, recensement par circonscription) ·
rapports de Léger, Synopsis Recherche, Pallas Data, Mainstreet, Angus Reid,
Innovative Research, Liaison Strategies · série compilée sur qc125.com
(Philippe J. Fournier) · Institut de la statistique du Québec.
