# Runbook — Modèle vivant QC127
**Procédure d'exploitation** · dernière mise à jour : 31 août 2026 (v7)

---

## 0. Carte du dossier

```
PROJET IA/sondages/
├── Data/                    rapports PDF des sondages + recensement 2021 par CEP 2026
├── 2018/                    résultats par bureau de vote 2018 + shapefile carte 2017
├── 2022/                    résultats par bureau de vote 2022 + shapefile carte 2022
├── 2026/                    shapefiles : 127 circonscriptions + sections de vote
├── pipeline/                   scripts du pipeline (+ dépendances Python vendorisées)
├── outputs/                 sorties horodatées : .xlsx, captures PNG, .inspect.ndjson
└── ModeleVivantQC127_*.xlsx versions du modèle
```

**Scripts clés dans `pipeline/`**

| Script | Rôle |
|---|---|
| `prepare_qc127_data.py` | Prépare `qc127_data.json` — circonscriptions, régions, références |
| `build_geospatial_reference.py` | Intersecte les sections de vote 2026 avec les cartes 2017/2022 → `qc127_geo_data.json` |
| `analyze_crosswalk.py` | Vérifie la matrice de correspondance (couvertures, poids, sommes à 1) |
| `build_qc127.mjs` | Construit le classeur Excel à partir des JSON |
| `verify_qc127.py` | Contrôles de cohérence après construction |
| `inspect_workbook.mjs` / `verify_export.mjs` | Inspection et vérification du .xlsx produit |
| `spreadsheet_cf/apply_conditional_formatting.mjs` | Mise en forme conditionnelle par parti |

---

## 1. Un nouveau sondage est publié

### 1.0 Voie automatique — `pipeline/pipeline.py`
```bash
python3 pipeline/pipeline.py --dossier . --simulation   # voir ce qui serait fait
python3 pipeline/pipeline.py --dossier .                # faire
```
Le script détecte les rapports non intégrés, les extrait, les saisit, étend les plages,
recalcule, passe les neuf contrôles, met à jour le CSV **et** la page. Il s'arrête au
moindre doute plutôt que de produire une projection fausse. Les sections 1.1 à 1.6
décrivent la même chose à la main : elles restent la référence quand le script s'arrête.

**Trois conventions qu'il applique, et qu'il faut connaître :**

| | Convention | Pourquoi |
|---|---|---|
| Date | **Milieu** de la période de terrain, lue **dans le PDF** | Le nom de fichier porte la date de publication : Léger publie le 1er sept. un sondage mené du 28 au 31 août. Un sondage mesure un intervalle, pas un instant. |
| `n` | La colonne d'effectifs du **tableau régional** du rapport, province et régions | Elle existe dans les trois formats. Aucun effectif n'est estimé ni divisé. |
| Doublon | Refusé si même firme, moins de six jours d'écart, et parts provinciales identiques à 0,6 pt près | Le même sondage arrive deux fois : rapport de terrain, puis rapport régional. |

> **Effectifs des lignes antérieures au 1er septembre 2026.** Toutes portent `n = 300`,
> une valeur de remplissage saisie à la main. La pondération par √n de l'agrégat est donc
> uniforme sur ces sondages-là, ce qui est un choix défendable mais n'est pas celui que la
> formule annonce. Les vrais effectifs sont lisibles dans les rapports ; leur reprise est
> au `TODO`.

### 1.1 Déposer le rapport
Enregistrer le PDF dans `Data/` sous le format **`AAAA-MM-JJ-firme.pdf`**. La date du nom sert d'index et de garde-fou (le script refuse un terrain à plus de 30 jours d'elle) ; c'est la date **lue dans le rapport** qui est saisie. Exemple : `2026-09-12-leger.pdf`. Le nommage est ce qui permet la détection automatique.

### 1.2 Extraire les ventilations régionales
```bash
pdftotext -layout "Data/2026-09-12-leger.pdf" - | less
```
Repérer le tableau d'intentions de vote **après répartition des indécis** (Léger : colonne « Total électeurs décidés » ; Synopsis : « après répartition » ; Pallas : bloc « électeurs favorables »).

Découpage régional par firme — à connaître par cœur :

| Firme | Régions publiées | Utilisable directement ? |
|---|---|---|
| **Pallas** | MTL RMR, Île, Banlieue, QC RMR, Reste | Oui, les 5 régions du modèle |
| **Synopsis** | Île, MTL RMR hors île, QC RMR, Ailleurs | Oui, 4 régions (MTL RMR se recalcule) |
| **Léger** | MTL RMR, QC RMR, Reste du Qc | **Non** — pas de ventilation Île/Banlieue |

**Si le sondage est un Léger ordinaire** (trois régions) : saisir UNIQUEMENT les lignes PROVINCE, `Montréal RMR`, `Québec RMR` et `Reste du Québec`. **Ne rien saisir pour l'Île ni pour la Banlieue, et surtout ne rien reconstruire à la main.** Depuis la v7, l'onglet `Agrégat` calcule les décalages Île/Banlieue à partir des sondages qui les ventilent (Pallas, Synopsis, et le Léger cumulatif du 25 août) ; une ligne Léger à trois régions y contribue correctement sans intervention. Saisir des valeurs reconstruites à la main fausserait l'agrégat en comptant deux fois la même information.

**Rapports cumulatifs** (comme le Léger « Grandes tendances régionales » du 25 août, qui agrège 11 sondages) : les saisir avec la firme exactement `leger-cumul`. La colonne `Nat.` de l'onglet `Sondages` les exclut alors automatiquement du niveau national, pour ne pas compter deux fois les sondages qu'ils agrègent. Ils servent uniquement aux décalages régionaux, où leur très grand n est précieux.

### 1.3 Contrôles avant saisie
- Chaque région somme à 100 ± 1 point.
- Le n du sous-échantillon régional est noté. **n < 100 : à lire avec prudence. n < 30 : indicatif seulement.**
- Le total provincial recalculé à partir des régions concorde avec le total publié.
- Comparer le sondage à la **vague précédente de la même firme**, jamais à un sondage d'une autre firme : la différence intra-firme annule l'effet de maison. Rappel : l'incertitude sur un écart est plus grande que sur un niveau (environ ×1,4).

### 1.4 Mettre à jour l'agrégat, pas le fichier
**Ne pas remplacer les intrants du modèle par le nouveau sondage.** Ajouter le sondage à la série et recalculer :
1. niveau national par ajustement local linéaire (niveau + pente), fenêtre ≈ 25 jours, pondération par √n ;
2. effets de maison estimés en résidus vs consensus lissé, rétrécis vers zéro selon le nombre de sondages de la firme (une firme avec un seul sondage doit avoir un effet de maison ≈ 0) ;
3. décalages régionaux (région − province) pondérés par récence, demi-vie ≈ 21 jours ;
4. estimation régionale = niveau national + décalage, plancher 0, renormalisation à 100.

Le résultat alimente `Régions!H2:M6`.

### 1.5 Recalculer et vérifier
```bash
python3 pipeline/verify_qc127.py
node pipeline/verify_export.mjs
```
Après toute écriture de formules avec openpyxl, **recalculer obligatoirement** — openpyxl n'évalue pas les formules. Utiliser le script de recalcul du projet, ou :
```bash
soffice --headless --convert-to xlsx --outdir recalc fichier.xlsx
```

### 1.6 Rafraîchir les livrables — ne pas sauter cette étape

Le classeur n'est pas le seul livrable. Deux autres vieillissent en silence si on les oublie, et rien dans le fichier Excel ne le signale.

**La page « Tendances Québec 2026 »** (artefact publié, et copie autonome `tendances-quebec-2026.html` à la racine du dossier) contient trois blocs à mettre à jour :

1. la série des sondages, dans l'objet `D` du script — ajouter le nouveau sondage et recalculer les courbes lissées ;
2. l'objet `SEATS`, avec les six scénarios issus du nouveau calcul ;
3. la date dans l'exergue en haut de page, et la ligne de source en bas.

Republier ensuite à la **même adresse** : l'artefact conserve son URL tant qu'on republie le même fichier. Une nouvelle adresse casserait les liens déjà partagés.

**`GUIDE-LECTURE.md`** contient des chiffres datés à trois endroits seulement — le reste du texte est stable :

- la section « L'état actuel, en trois phrases » ;
- la valeur de pente citée à l'étape 2 ;
- le nombre de sièges cité dans les pièges classiques.

**Règle simple :** si le nombre de sièges d'un parti a bougé, la page et le guide sont périmés. Un tableau de bord faux est pire qu'un tableau de bord absent, parce que personne ne le vérifie.

---

## 2. Contrôles de non-régression

À passer après chaque mise à jour. Un seul échec bloque la publication.

| # | Contrôle | Valeur attendue |
|---|---|---|
| 1 | Nombre de circonscriptions | 127 |
| 2 | Répartition régionale | Île 28 · Banlieue 40 · QC RMR 13 · Reste 46 |
| 3 | Somme des sièges, chaque scénario | 127 |
| 4 | Seuil de majorité dans les formules | **64**, jamais 63 |
| 5 | Base de référence, total | 4 112 822 (votes réels 2022) — **pas** 8,4 M, qui serait la base électeurs |
| 6 | Référence provinciale | CAQ 41,0 · PLQ 14,4 · QS 15,4 · **PQ 14,6** · PCQ 12,9 · Autre 1,7 |
| 7 | Somme des parts par région | 100,0 |
| 8 | Réplication indépendante en Python | écart nul sur au moins 3 circonscriptions tirées au hasard |

### Règle d'arrêt

**La session s'arrête et remonte le cas au lieu de publier si :**

1. un seul des huit contrôles ci-dessus échoue ;
2. un parti bouge de **plus de dix sièges** par rapport au calcul précédent — un mouvement de cette taille est possible, mais il doit être expliqué avant d'être diffusé, pas après ;
3. la somme des parts d'une région saisie s'écarte de 100 de plus d'un point ;
4. un sous-échantillon régional est sous n=100, ou sous n=30 pour une conclusion ;
5. les libellés des partis ne sont pas lisibles en texte dans le PDF — c'est le cas des rapports où les tableaux sont des graphiques : l'identité des partis se lit alors aux couleurs, et une erreur y est silencieuse. Recouper avec un tableau croisé étiqueté du même rapport avant de saisir quoi que ce soit.

Suivre une procédure fidèlement, c'est aussi suivre ses angles morts. Cette règle existe pour ça.

Le contrôle 6 est celui qui a détecté la fuite « Autre → PQ » de v4.1 : si le PQ dépasse 14,6 et « Autre » tombe sous 1,7 dans la même proportion, la transposition a reversé des voix de tiers partis au PQ.

---

## 3. Rédiger un livrable

**Toujours inclure :**
- la date de fin de terrain et le n, global et par sous-échantillon régional ;
- le mode de collecte, et le bon terme : **intervalle de crédibilité** pour un panel web (Léger, Synopsis), pas « marge d'erreur » ;
- l'avertissement de non-linéarité : la relation intentions-sièges de la CAQ est quasi plate sous 24 % et explosive entre 25 et 30 %. La CAQ est actuellement dans cette zone, donc un écart de deux points déplace des dizaines de sièges ;
- pour un sondage Léger, la mention que la ventilation Île/Banlieue est reconstruite et non mesurée ;
- pour chaque recommandation, **un contre-argument explicite ou une condition d'échec**.

**Ne jamais :**
- publier un décompte de sièges tiré d'un sondage unique ;
- présenter la fourchette C/D comme un intervalle de confiance — c'est un décalage uniforme déterministe, pas une distribution ;
- conclure à une tendance sur un mouvement inférieur à l'incertitude, sauf convergence de plusieurs indicateurs ou de plusieurs firmes.

---

## 4. Convention de versionnage

`ModeleVivantQC127_v<N>_<source>_<date>.xlsx`, où `<source>` est l'agrégat ou la firme si le fichier tourne sur un sondage unique. Aligner `Sièges!A1` et `Méthodologie!B2` sur le numéro du nom de fichier — trois versions portent actuellement un intitulé interne qui contredit leur nom.

Chaque construction dépose dans `outputs/<slug>_<AAAAMMJJ>/` : le .xlsx, les captures PNG des onglets, et le `.inspect.ndjson`. Ne jamais écraser le fichier maître du projet ; produire une nouvelle version.

---

## 5. Sources

| Donnée | Source |
|---|---|
| Résultats officiels et cartes | Élections Québec — `electionsquebec.qc.ca` |
| Délimitation 2026 (127 circonscriptions) | Loi visant à assurer la représentation effective des électeurs, 2026 c. 15, sanctionnée le 12 juin 2026 |
| Recensement par circonscription 2026 | `Data/statistiques-recensement-2021-CEP2026.xls` |
| Séries de sondages | `qc125.com/sondages.htm` (Philippe J. Fournier) |
| Participation par âge et sexe | Institut de la statistique du Québec |
| Référence méthodologique externe | `route127.ca/methodologie` — source grise, transparente, non validée par les pairs |
