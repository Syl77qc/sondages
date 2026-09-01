# Comment lire le modèle de projection QC127

*Guide à l'intention des non-spécialistes · 1er septembre 2026*

---

## Ce que le modèle fait, et ce qu'il ne fait pas

Le modèle répond à une seule question : **si l'élection avait lieu aujourd'hui, combien de sièges chaque parti obtiendrait-il ?**

Ce n'est pas une prédiction du 5 octobre. C'est une photo du présent, traduite en sièges. La distinction n'est pas une coquetterie : entre aujourd'hui et le vote, il reste cinq semaines de campagne, et la campagne change les choses. Le modèle ne sait rien de ce qui n'est pas encore arrivé.

Il faut aussi comprendre ce qu'il mesure. Un sondage recueille des **intentions déclarées**, pas des votes. Les gens changent d'avis, et surtout, tout le monde ne va pas voter. Le modèle suppose que ceux qui voteront ressemblent à ceux qui ont répondu. C'est une hypothèse raisonnable, pas une certitude.

---

## Étape 1 — On ne suit jamais un seul sondage

C'est la règle la plus importante, et la moins intuitive.

Voici ce que donne le **même modèle**, sur la **même carte**, avec la **même méthode**, en changeant uniquement le sondage qu'on lui donne à manger :

| Sondage utilisé | Sièges du PQ |
|---|---|
| Pallas, 2 août | 66 |
| Synopsis, 8 août | 63 |
| Pallas, 29 août | 46 |
| Synopsis, 25 août | 35 |

Synopsis et Pallas sont séparés de **quatre jours** et donnent un écart de onze sièges pour le PQ. Une partie de cet écart est un mouvement réel — les appuis bougeaient vite en août. Mais l'essentiel est du bruit : chaque sondage interroge environ mille personnes, et deux échantillons de mille personnes tirés le même jour ne donnent jamais exactement le même résultat.

Le modèle utilise donc **l'ensemble des sondages publiés** — trente-six depuis août 2025 — et non le dernier paru. C'est la différence entre suivre une trajectoire et réagir à chaque soubresaut.

---

## Étape 2 — La courbe, pas les points

Sur le graphique, chaque petit point est un sondage; chaque ligne est la tendance calculée à partir de tous les sondages voisins dans le temps.

**Il faut lire les lignes.** Un point qui s'écarte de sa courbe n'annonce pas un retournement : c'est très probablement la marge d'incertitude de ce sondage-là. Un vrai mouvement se reconnaît à ce que **plusieurs firmes bougent dans le même sens en même temps**.

La courbe fait deux choses. Elle donne le **niveau** — où en est chaque parti aujourd'hui — et la **pente** — à quelle vitesse ça bouge. La pente compte autant que le niveau. En ce moment, la CAQ est à 25,2 % avec une pente de **+5,7 points par tranche de trente jours**. Le niveau dit où elle est; la pente dit où elle s'en va si rien ne change.

C'est aussi pourquoi une simple moyenne des derniers sondages ne suffirait pas : dans une série qui monte, faire la moyenne des dernières semaines revient à mélanger des chiffres anciens plus bas avec des chiffres récents plus hauts, et donc à sous-estimer le présent. La courbe corrige ce retard.

---

## Étape 3 — Chaque maison de sondage a son décalage

Deux firmes qui sondent la même semaine ne donnent pas les mêmes chiffres. Ce n'est pas que l'une se trompe : elles n'utilisent pas les mêmes méthodes de recrutement, ne répartissent pas les indécis de la même façon, ne pondèrent pas identiquement. Chaque firme a un **décalage qui lui est propre et qui reste assez stable**.

D'où une règle simple et puissante : **pour mesurer un mouvement, on compare une firme à elle-même**. Le décalage s'annule dans la soustraction.

Exemple concret, en août : Pallas a mesuré la CAQ à +5 entre ses deux vagues, Léger à +3 entre les siennes, Synopsis à +7 entre les siennes. Aucune de ces trois mesures n'est concluante à elle seule. Mais trois firmes indépendantes qui pointent toutes dans le même sens, ça l'est. **La CAQ a bel et bien gagné environ cinq points en août.**

---

## Étape 4 — Descendre au niveau des régions

Un pourcentage national ne dit pas qui gagne où. Le modèle découpe donc le Québec en quatre territoires :

| Région | Circonscriptions |
|---|---|
| Île de Montréal | 28 |
| Banlieue de Montréal (le « 450 ») | 40 |
| Région de Québec | 13 |
| Reste du Québec | 46 |

Ce découpage n'est pas cosmétique. **L'Île de Montréal et sa banlieue votent de façon radicalement différente** — au point que les confondre fausse tout. En moyenne, par rapport à la banlieue, l'Île donne 13 points de plus au PLQ, 9 de plus à QS, 13 de moins à la CAQ et 11 de moins au PQ. Ces deux territoires représentent ensemble 68 des 127 circonscriptions : les traiter comme un bloc unique, c'est se tromper sur plus de la moitié de l'Assemblée nationale.

À côté de la géographie, il y a une seconde ligne de partage, plus forte encore : **la langue**. Chez les francophones, le PQ devance largement ; chez les non-francophones, le PLQ récolte près de la moitié des voix. Vingt-six points séparent le PLQ d'un groupe à l'autre. C'est le clivage le plus marqué du paysage québécois, et le scénario F en tient compte circonscription par circonscription.

Une complication pratique : les firmes ne publient pas toutes le même découpage. Pallas fournit les cinq régions du modèle, Synopsis quatre, **Léger seulement trois** — sans séparer l'Île de la banlieue. Le modèle comble le trou en appliquant les écarts Île/banlieue mesurés par les firmes qui, elles, les publient.

---

## Étape 5 — Traduire des pourcentages en sièges

C'est ici que le modèle fait son vrai travail, et c'est l'étape la moins intuitive.

**Le point de départ, c'est 2022.** On connaît le résultat réel de chaque circonscription à la dernière élection. Le modèle part de là et applique le mouvement mesuré depuis : si un parti a gagné 40 % dans une région depuis 2022, ses votes de 2022 sont augmentés de 40 % dans chaque circonscription de cette région. Ensuite, le parti qui arrive premier remporte le siège.

**Mais la carte a changé.** L'élection du 5 octobre se tiendra sur une carte de **127 circonscriptions**, adoptée en juin 2026, alors que celle de 2022 en comptait 125. Les frontières ont bougé. Il a donc fallu **transposer** les résultats de 2022 sur les nouvelles limites : pour chaque nouvelle circonscription, on identifie de quelles anciennes circonscriptions viennent ses électeurs, et on reconstitue le vote de 2022 en conséquence. Les 4 112 821 votes exprimés en 2022 sont intégralement redistribués sur la nouvelle carte.

Conséquence concrète à retenir : **le seuil de la majorité est de 64 sièges, plus de 63.**

---

## Étape 6 — Pourquoi il y a plusieurs scénarios

Le modèle ne produit pas un chiffre mais six lectures, parce que la traduction votes-sièges dépend d'hypothèses qu'on ne peut pas trancher avec certitude.

- **Scénario A** — chaque parti progresse ou recule proportionnellement à ce qu'il valait dans chaque circonscription. C'est la lecture de base.
- **Scénario B** — comme A, mais on tient compte du fait que certaines circonscriptions ont leur tempérament propre, mesuré par leur comportement entre 2018 et 2022.
- **Scénarios C et D** — les bornes haute et basse, si les sondages se trompaient tous dans le même sens.
- **Scénario E** — un mélange de deux façons de répartir le mouvement entre les circonscriptions.
- **Scénario F** — celui-ci tient compte de la **composition linguistique** de chaque circonscription. C'est le plus récent, et il repose sur un constat fort : en 2022, la proportion de francophones expliquait à elle seule 91 % de l'écart du vote libéral d'une circonscription à l'autre, et 67 % de celui de la CAQ. Le modèle régional attribue à une circonscription la moyenne de sa région, ce qui gonfle le vote libéral dans les banlieues francophones où il y a peu d'anglophones. Le scénario F corrige ça.

**Si les six scénarios racontent la même histoire, le résultat est robuste. S'ils divergent, c'est le signal qu'il faut être prudent.** En ce moment, ils convergent sur un point essentiel : *aucun* ne donne de majorité à qui que ce soit.

---

## Les cinq règles de lecture

**1. Un décompte de sièges n'est pas une prévision.** C'est ce que donnerait le vote aujourd'hui.

**2. Deux points de pourcentage peuvent valoir des dizaines de sièges.** La relation n'a rien de proportionnel. Dans les tests, la CAQ passe de 3 à 47 sièges selon le sondage utilisé, pour des écarts d'intentions de quelques points. Quand plusieurs partis sont serrés dans les mêmes régions, un déplacement minime fait basculer des dizaines de circonscriptions du même coup. **La CAQ se trouve précisément dans cette zone.**

**3. « Marge d'erreur » est un terme à manier avec soin.** La plupart des sondages sont faits par panel web : les répondants ne sont pas tirés au hasard dans la population, ils sont recrutés. On ne peut donc pas parler de marge d'erreur au sens statistique — les firmes publient un **intervalle de crédibilité**, qui est une estimation modélisée. Et ce chiffre ne couvre que l'incertitude d'échantillonnage, pas les autres sources d'erreur. La recherche montre que l'erreur totale est d'environ **le double** de ce que suggèrent les marges publiées. Le modèle utilise donc une fourchette élargie.

**4. Attention aux petits sous-échantillons.** Quand un sondage de mille personnes est découpé en régions, chaque région ne compte plus que 250 à 350 répondants. En dessous de 100, un chiffre régional est indicatif. En dessous de 30, il ne veut rien dire.

**5. Un mouvement inférieur à l'incertitude n'est pas une tendance.** Sauf si plusieurs indicateurs ou plusieurs firmes convergent.

---

## Les pièges classiques

**« Le dernier sondage montre que… »** — Un sondage isolé ne montre rien à lui seul. Il faut le situer dans la série.

**« Le PQ a perdu deux points, il s'effondre. »** — Deux points, c'est à l'intérieur du bruit d'un sondage. Regardez la courbe : elle descend lentement depuis décembre, ce qui est une information très différente d'un effondrement.

**« Le modèle dit 51, l'autre scénario dit 52, donc c'est solide. »** — Pas nécessairement. Deux scénarios peuvent converger par coïncidence. Ce qui compte, c'est l'étendue complète : le PQ va de 44 à 57 sièges selon le scénario, et c'est cette fourchette qui décrit honnêtement ce que le modèle sait.

**« Le modèle donne 51 sièges au PQ, donc le PQ aura 51 sièges. »** — Le modèle donne 51 sièges *si le vote avait lieu aujourd'hui et si la traduction votes-sièges se comporte comme prévu*. Les deux conditions sont fortes.

**« Cette firme est biaisée. »** — Toutes les firmes ont un décalage propre. Cela ne les disqualifie pas; cela veut dire qu'on les compare à elles-mêmes plutôt qu'entre elles.

**« Il y a 125 sièges à l'Assemblée. »** — Plus depuis juin 2026. Il y en a 127, et la majorité est à 64.

---

## Ce que le modèle ne sait pas faire

Il faut être franc sur les limites, parce qu'elles sont réelles.

- Il **ne modélise pas les candidats**. Un candidat vedette ou une controverse locale sont invisibles pour lui.
- Il **ne prévoit pas la participation**. Il suppose qu'elle sera semblable à celle de 2022, partout.
- Il est **déterministe** : il donne un chiffre, pas une probabilité. Il ne dit pas « le PQ a 30 % de chances d'être majoritaire ».
- Dans le scénario linguistique, la catégorie « non-francophone » des sondages désigne l'électorat anglophone et allophone. **Dans Ungava, elle recouvre une population majoritairement inuite et crie**, dont le comportement n'a rien à voir. Le résultat y est à lire avec prudence.
- La **transposition sur la nouvelle carte suppose une homogénéité** : quand une nouvelle circonscription est faite de morceaux de deux anciennes, on suppose que chaque morceau votait comme l'ensemble dont il provenait. C'est une approximation.
- Il ne dit **rien sur les raisons**. Il mesure que la CAQ monte; il n'explique pas pourquoi.

---

## L'état actuel, en trois phrases

Au 1er septembre 2026, la CAQ est remontée d'une quinzaine de points depuis son creux de mars et vient de dépasser le PLQ, mais sa progression ralentit. Le PQ demeure en tête, autour de 29 %, en érosion lente et régulière depuis décembre. **Aucun scénario ne donne de majorité à quiconque** — et compte tenu du nombre de circonscriptions serrées, c'est le constat le plus solide que le modèle produise en ce moment.

---

## Petit lexique

| Terme | Ce que ça veut dire |
|---|---|
| **Agrégat** | La moyenne intelligente de tous les sondages, pondérée par leur âge et leur taille |
| **Lissage** | Le calcul qui transforme un nuage de points en courbe |
| **Pente** | La vitesse à laquelle un parti monte ou descend, en points par mois |
| **Effet de maison** | Le décalage systématique propre à une firme de sondage |
| **Décidés** | Les répondants ayant exprimé une intention, après répartition des indécis |
| **Intervalle de crédibilité** | L'équivalent de la marge d'erreur pour un panel web, mais modélisé plutôt que déduit |
| **Transposition** | Le recalcul des résultats de 2022 sur les frontières de 2026 |
| **Bascule** | Une circonscription où l'écart entre les deux premiers est inférieur à 5 points |
| **Seuil de majorité** | 64 sièges sur 127 |

---

*Le modèle et ses données sont dans le dossier `PROJET IA\sondages`. La procédure de mise à jour est décrite dans `RUNBOOK.md`, les travaux en cours dans `TODO.md`.*
