# TODO — Modèle vivant QC127

## JOURNAL — 31 août 2026, 23 h

**Fait dans `ModeleVivantQC127_v7_agregat.xlsx` :**

- **P0-1 Fusion des deux lignées** — le crosswalk de v4.1 est appliqué aux **votes réels 2022**. Total conservé exactement : 4 112 821. Référence provinciale CAQ 40,98 · PLQ 14,37 · QS 15,43 · **PQ 14,61**.
- **P0-2 Fuite « Autre → PQ »** — disparue. Autre remonte de 0,6 à 1,39.
- **P0-4 Marge `N2`** — portée de 2,9 à **6,0 pp** (l'intervalle de crédibilité publié ne couvre que l'échantillonnage).
- **P1-5 Agrégat** — onglets `Sondages` et `Agrégat` vivants : 11 rapports, niveau national ET pente par régression linéaire pondérée, décalages régionaux pondérés récence × √n. Alimente `Régions!H2:M6`.
- **P1-6 Ventilation Île/Banlieue** — intégrée, et confirmée par le Léger cumulatif (n=1 885 / 1 828) : CAQ −14 · PLQ +17 · QS +6 · PQ −12.
- **Léger du 25 août** (cumul 12 juin – 24 août, n=11 305) intégré, **exclu du niveau national** pour ne pas compter deux fois les 11 sondages qu'il agrège.

Les 8 contrôles de non-régression passent, réplication Python du scénario A incluse (0 écart sur 127 circonscriptions).

**Reste à faire, par ordre :** P0-3 (les 62 circonscriptions à confronter au décret), P2-8 (simulation Monte-Carlo), P2-9 (validation hors échantillon), et la correction PCQ/Autre dans la table de votes 2022 source (PCQ 13,22 contre 12,90 au DGEQ — écart hérité, non introduit par la transposition).

---

**État au 31 août 2026** · Élection le 5 octobre 2026 (J−35) · Seuil de majorité : 64 sièges sur 127

---

## Où en est le projet

Deux lignées de fichiers coexistent, et **chacune détient la moitié de la solution** :

| | `v4_1_geospatial` | `v6_pallas_29aout` |
|---|---|---|
| Transposition géographique réelle | **Oui** — onglet `Correspondance`, 371 lignes, poids électoraux issus des shapefiles | Non — 62 des 119 circonscriptions de même nom gardent les chiffres de la carte 125 |
| Base de référence | **Électeurs inscrits** (8 422 574 = 2,05× les votes réels) | **Votes réels 2022** (4 112 822) ✔ |
| Référence provinciale | CAQ 41,0 · PLQ 14,4 · QS 15,4 · **PQ 15,3** · PCQ 13,3 · **Autre 0,6** | CAQ 41,0 · PLQ 14,4 · QS 15,4 · **PQ 14,6** ✔ · PCQ 13,2 · Autre 1,4 |
| Réel 2022 (DGEQ) | — | CAQ 41,0 · PLQ 14,4 · QS 15,4 · PQ 14,6 · PCQ 12,9 · Autre 1,7 |
| Scénario base 2018 | Non | Oui (scén. E) ✔ |

**La cible : le crosswalk de v4.1 appliqué aux votes réels de v6.**

---

## P0 — Défauts de justesse (à régler avant toute publication)

### 1. Fusionner les deux lignées
Appliquer la matrice `Correspondance` de `v4_1_geospatial` (circonscription 2026 × carte source × circonscription source × poids électoral) aux **votes réels 2022** de `v6`, plutôt qu'aux électeurs inscrits.

*Pourquoi* : pondérer par les électeurs inscrits suppose un taux de participation uniforme entre circonscriptions. Il ne l'est pas — la participation est nettement plus basse sur l'Île de Montréal, particulièrement dans les circonscriptions non francophones. Le biais se transmet aux références régionales, donc aux ratios de swing.

*Effort* : moyen. Le crosswalk existe déjà, il ne manque que la substitution de la base.

### 2. Corriger la fuite « Autre → PQ » dans v4.1
Dans la référence transposée de v4.1, le PQ est surestimé et « Autre » sous-estimé, en échange exactement complémentaire, **dans les cinq régions** :

| Région | Δ PQ | Δ Autre |
|---|---|---|
| Île de Montréal | +1,7 | −1,8 |
| Montréal RMR | +1,2 | −1,1 |
| Banlieue | +0,8 | −0,8 |
| Québec RMR | +0,4 | −0,5 |
| Reste du Québec | +0,2 | −0,3 |

Un changement de frontières déplacerait les partis dans des sens différents selon les régions. Un transfert 1:1 partout est une signature de traitement de données, pas de géographie.

*Impact mesuré* : sur l'agrégat de 10 sondages, scénario A — PQ **48 → 54** sièges, CAQ **28 → 23**. Six sièges provenant d'un artefact.

### 3. Vérifier la transposition de v6
62 des 119 circonscriptions de même nom ont des totaux de votes **identiques** à la carte de 125, écart médian de 0. Soit ces circonscriptions sont réellement inchangées par la révision — la note d'Élections Québec dit que la carte « maintient certaines circonscriptions établies en 2017 » —, soit la transposition ne les a pas touchées. **À trancher en confrontant la liste au décret de délimitation définitive.** Tant que ce n'est pas fait, on ne sait pas si v6 est correct ou incomplet.

### 4. Corriger `Régions!N2` : ce n'est pas une marge d'erreur
Les sondages Léger et Synopsis sont des panels web : ils publient un **intervalle de crédibilité**, pas une marge d'erreur — la notion frequentiste suppose un échantillonnage probabiliste. Pallas est en IVR, ce qui est différent. Deux conséquences :
- ne pas écrire « marge d'erreur » dans les livrables pour les panels web ;
- la valeur publiée ne couvre que la composante d'échantillonnage. La littérature (Shirani-Mehr et al. 2018, 4 221 sondages) situe l'erreur totale à environ **deux fois** l'erreur implicite des marges publiées. Les scénarios C/D à ±2,9 ou ±3,3 pp sont donc trop serrés.

---

## P1 — Méthode

### 5. Remplacer le sondage unique par un agrégat — priorité absolue
Le modèle tourne sur un seul sondage. Voici ce que donne **le même fichier v4.1**, même carte, même méthode, en ne changeant que le sondage d'entrée :

| Sondage d'entrée | CAQ | PLQ | QS | PQ | PCQ | Majorité |
|---|---|---|---|---|---|---|
| Pallas 2 août | 3 | 37 | 7 | **66** | 14 | PQ |
| Synopsis 8 août | 5 | 39 | 6 | 63 | 14 | aucune |
| Pallas 29 août | 25 | 35 | 6 | 46 | 15 | aucune |
| **Synopsis 25 août** (intrant actuel de v4.1) | **47** | 35 | 6 | **35** | 4 | aucune |
| **Agrégat 10 sondages au 31 août** | **28** | 36 | 6 | **48** | 9 | aucune |

Synopsis du 25 août et Pallas du 29 août sont séparés de **quatre jours** et donnent CAQ 47 contre CAQ 25. Une partie est du mouvement réel — la CAQ monte —, mais l'essentiel est du bruit d'échantillonnage amplifié par la traduction en sièges. **Publier un décompte de sièges fondé sur un sondage unique n'a pas de sens dans le régime actuel.**

Méthode retenue : niveau national par **ajustement local linéaire** (niveau + pente) sur les 35 sondages depuis août 2025, effets de maison rétrécis, puis décalage régional (région − province) pondéré par récence. Une simple moyenne pondérée ne suffit pas : elle retarde sur une série en tendance et redonne presque exactement le sondage unique (CAQ 22,7 contre 25,5 pour le local linéaire, la valeur publiée par Qc125 étant 25).

### 6. Ventilation Île / Banlieue — acquis, à préserver
Les rapports Pallas ventilent les cinq régions du modèle ; Synopsis en ventile quatre ; **Léger n'en ventile que trois** (MTL RMR agrégé). L'écart Île − Banlieue est massif et de signe constant sur les six sondages qui le ventilent : CAQ **−12,8**, PLQ **+13,9**, QS **+8,8**, PQ **−11,1**. Quand l'intrant vient de Léger, il faut reconstruire la ventilation à partir des décalages Pallas/Synopsis, jamais appliquer l'agrégat MTL aux deux régions.

### 7. Correctif de biais PQ — le laisser hors du centre
La revue de littérature conclut que rien n'appuie un retrait déterministe de 2,3 points au PQ : la fourchette « +1,7 à +2,9 » ne décrit pas le dernier sondage de chaque cycle (en 2022, le dernier Léger donnait PQ 15 % contre 14,61 % au scrutin, soit +0,39), la série ne compte que trois élections, et le PQ est passé de troisième force à favori. À conserver comme scénario de sensibilité étiqueté, jamais comme espérance centrale.

---

## P2 — Robustesse

### 8. Remplacer C/D par une simulation
Les scénarios C/D sont une fourchette déterministe : on décale toutes les régions du même nombre de points, dans le même sens. C'est irréaliste. Une simulation Monte-Carlo tirerait : bruit local par circonscription, erreur de méthode par firme, et **choc commun d'élection corrélé entre partis** — cette dernière composante ne diminue pas quand on ajoute des sondages. Sortie : une distribution de sièges et une probabilité de majorité, pas quatre nombres.

### 9. Validation « élection entière laissée de côté »
Le facteur d'inertie (`O2` = 0,5), le poids du swing et la demi-vie de l'agrégat sont des hyperparamètres jamais validés. Les choisir par validation hors échantillon sur 2014, 2018, 2022. Limite honnête : trois points de validation, c'est peu, et si le classement des modèles change selon l'élection retirée, il faut publier un ensemble plutôt qu'un gagnant.

### 10. Non-linéarité CAQ — à documenter dans les livrables
`memoire.txt` note que la relation intentions-sièges de la CAQ est quasi plate sous 24 % et explosive entre 25 et 30 %. Le tableau du point 5 le confirme brutalement : de 3 à 47 sièges. **La CAQ est actuellement dans cette zone.** Tout livrable doit le dire, sinon le lecteur prendra un décompte pour une prévision.

---

## Corrections mineures

- `memoire.txt` attribue qc125.com à « William Croteau-Charest ». Qc125 est de **Philippe J. Fournier**. À corriger avant qu'un livrable ne reprenne l'erreur.
- v4.1 `Méthodologie!B14` cite « résultats par bureau de vote 2018 et 2022 » comme source, alors que `B12` dit que les votes historiques ne sont disponibles que par circonscription. Les deux énoncés sont réconciliables — on a les résultats par bureau mais pas les polygones historiques — mais la formulation devrait le dire.
- Trois versions portent le même intitulé v4.0/v6.0 dans la cellule `Sièges!A1` alors que les noms de fichiers disent v4.1, v5 et v6. Aligner.
