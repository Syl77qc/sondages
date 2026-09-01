# Correction d’un biais systémique du PQ dans une projection électorale québécoise

**État de la recherche au 31 août 2026**  
**Question examinée :** la littérature justifie-t-elle de retrancher systématiquement 2,3 points au Parti québécois (PQ) dans une projection de 2026 parce que les derniers sondages de 2014, 2018 et 2022 l’auraient surestimé?

## Réponse courte — synthèse (environ 550 mots)

La littérature justifie de traiter l’erreur totale des sondages comme nettement plus grande que la seule erreur d’échantillonnage, mais **elle ne justifie pas, en l’état des preuves, une correction déterministe de −2,3 points propre au PQ**. Shirani-Mehr et ses coauteurs analysent 4 221 sondages américains et obtiennent une erreur quadratique moyenne d’environ 3,5 points, soit près du double de celle qu’impliqueraient les marges d’erreur publiées. Leur résultat important est l’existence d’une composante commune à plusieurs sondages d’une même élection : additionner des sondages réduit le bruit indépendant, mais non un biais partagé. Ce résultat appuie une variance systémique dans une simulation Monte-Carlo; il n’établit ni la direction ni la permanence d’un biais péquiste. Les rapports de l’AAPOR constatent justement que la direction partisane des erreurs peut être corrélée à l’intérieur d’une élection sans être stable d’une élection à l’autre.

Le dossier québécois rend plausible l’existence de biais contextuels. En 1998, les derniers sondages donnaient en moyenne cinq points d’avance au PQ, alors que le PLQ a gagné le vote populaire d’environ un point; l’étude publiée dans *Public Opinion Quarterly* privilégie des problèmes communs de couverture et de non-réponse plutôt qu’un simple mouvement tardif. Le chapitre de Claire Durand sur 2012 documente aussi une sous-estimation historique fréquente du PLQ et l’usage de répartitions non proportionnelles des « discrets ». Mais cette histoire n’est pas celle d’un coefficient immuable : l’ADQ a été sous-estimée en 2007 et le PQ en 2008; en 2018, Durand et Blais attribuent l’essentiel de l’écart à des changements de dernière minute et au vote des non-déclarants, variables selon les régions.

La série 2014-2018-2022 est trop petite et trop dépendante des choix de mesure pour identifier une constante de −2,3. En 2014, le dernier Léger donnait 29 % au PQ contre 25,38 % au scrutin (+3,62). En 2018, les derniers Léger, Mainstreet et Forum donnaient 19 à 20 %, contre 17,06 % (+1,94 à +2,94). En 2022, le dernier Léger donnait 15 % contre 14,61 % (+0,39), tandis que Forum donnait 17,2 % (+2,59). Une « moyenne des derniers sondages » peut donc reproduire la fourchette avancée par Route 127, mais le résultat change selon la firme, la date, l’arrondi et la pondération. Surtout, la différence sondage-résultat confond erreur de mesure et évolution réelle entre le terrain et le vote.

Cette confusion est décisive cinq ou six semaines avant l’élection. Un sondage mesure une intention présente; il ne prédit pas automatiquement le vote final. La recherche comparative montre que les erreurs diminuent généralement à l’approche du scrutin, tandis que les électeurs tardifs sont plus volatils. Importer dans une mesure faite aujourd’hui un « biais » calculé sur des sondages finaux revient à transformer des mouvements futurs possibles en défaut actuel du sondage.

La solution défendable est donc **probabiliste et fortement régularisée** : conserver une erreur commune par élection et des effets de maison; si l’historique PQ est utilisé, en faire un prior centré près de zéro, partiellement mutualisé avec les autres partis et élections, dont l’incertitude est grande. Une correction non nulle ne devrait survivre que si elle améliore des validations hors échantillon, notamment en laissant une élection entière de côté. À défaut, −2,3 points doit être présenté comme un scénario de sensibilité, non comme l’espérance centrale du modèle.

## Q1 — Erreur totale ou seule erreur d’échantillonnage?

**Établi.** La marge d’erreur publiée décrit principalement la variabilité d’échantillonnage sous des hypothèses idéales. Elle omet ou décrit mal la couverture, la non-réponse, le mode, la pondération, le modèle de participation, la formulation des questions et le changement d’opinion après le terrain. Dans 4 221 sondages menés durant les trois dernières semaines de 608 courses américaines (1998-2014), [Shirani-Mehr et al. (2018)](https://ideas.repec.org/a/taf/jnlasa/v113y2018i522p607-614.html) trouvent une RMSE d’environ **3,5 points par part de vote**, « environ deux fois » l’erreur impliquée par la plupart des marges publiées, ainsi qu’un biais absolu commun à l’élection d’environ 2 points.

**Précision indispensable.** Le facteur deux porte sur l’échelle d’erreur implicite, pas sur l’énoncé simpliste « l’erreur absolue sera toujours deux fois la marge ±3 ». RMSE, erreur absolue, erreur sur une part de vote et erreur sur l’écart entre deux partis sont des quantités différentes. Le rapport de deux est un ordre de grandeur empirique, dépendant du pays, de la période et du type de course, et non une constante universelle. La base comparative de [Jennings et Wlezien (2018)](https://www.nature.com/articles/s41562-018-0315-6), plus de 30 000 sondages dans 351 élections et 45 pays, situe l’erreur absolue d’un parti dans la dernière semaine autour de 2,1 points depuis 2001.

**Implication.** La simulation doit ajouter une erreur non échantillonnale corrélée entre sondages et entre partis. Faire la moyenne de dix sondages ne divise pas par \(\sqrt{10}\) un biais commun de participation ou de pondération.

## Q2 — Un biais partisan récurrent peut-il être corrigé?

**Établi.** Des biais directionnels existent dans une élection donnée, et des « effets de maison » peuvent persister parce que les firmes ont des modes, filtres d’électeurs probables et pondérations propres. Les modèles de [Jackman (2005)](https://www.tandfonline.com/doi/abs/10.1080/10361140500302472) et [Linzer (2013)](https://ideas.repec.org/a/taf/jnlasa/v108y2013i501p124-134.html) estiment ces effets dans des structures dynamiques et hiérarchiques. Cela autorise une correction **de firme ou de méthode**, avec incertitude et mutualisation.

**Établi contre la permanence du signe.** Le [rapport AAPOR sur 2016](https://aapor.org/wp-content/uploads/2023/01/AAPOR-2016-Election-Polling-Report.pdf) conclut que les erreurs sont souvent corrélées à l’intérieur d’une élection, mais qu’il n’existe pas de direction partisane constante d’une élection à l’autre. Le rapport [AAPOR 2024](https://aapor.org/wp-content/uploads/2025/10/Task-Force-on-2024-Pre-Election-Polling_Report.pdf) rappelle que démocrates et républicains ont été sous-estimés à des fréquences comparables sur la longue période. Les causes changent lorsque changent l’électorat, le mode de collecte, les cibles de pondération et la mobilisation.

**Interprétation pour le PQ.** Trois élections consécutives constituent au mieux un signal exploratoire. Elles ne suffisent pas à séparer :

- un effet réellement propre au PQ;
- un effet de taille ou de position dans la course;
- une sous-estimation du PLQ ou d’un autre parti, nécessairement reflétée ailleurs puisque les parts totalisent 100 %;
- un effet de firme;
- un mouvement entre la fin du terrain et le scrutin.

Une soustraction fixe estimée et évaluée sur les mêmes trois élections est exposée au surajustement. Le risque de non-stationnarité est particulièrement fort : le PQ était parti gouvernemental sortant en 2014, troisième ou quatrième force en 2018-2022 et favori potentiel en 2026, dans un système partisan transformé par la CAQ, QS et le PCQ. La correction raisonnable est un coefficient hiérarchique rétréci vers zéro, non une constante imposée.

## Q3 — Ce que montrent les élections québécoises

| Élection | Observation vérifiable | Lecture causale prudente |
|---|---|---|
| 1998 | Les six derniers sondages donnaient en moyenne environ **PQ +5**; le vote fut environ **PLQ 44 / PQ 43**. | [Durand, Blais et Vachon](http://www.jstor.org/stable/3078789) écartent comme explications suffisantes le mouvement tardif, la participation différentielle et la répartition des non-déclarants; ils privilégient des déficiences communes de couverture/non-réponse. C’est une preuve d’un biais contextuel compatible avec une surestimation du PQ, pas d’une constante contemporaine. |
| 2012 | Résultat PQ : **31,95 %**. Les dernières estimations secondaires recensées varient : Léger **33 %** (+1,05), Forum **36 %** (+4,05). | [Durand (2013)](https://www.degruyterbrill.com/document/doi/10.1515/9782760632264-012/html?lang=en) décrit des biais historiques et les « discrets », mais aussi des changements de signe et de parti. Le choix du « dernier sondage » change déjà beaucoup l’estimation. |
| 2014 | Dernier Léger : **29 %**; résultat officiel : **25,38 %**, soit +3,62. | Écart net dans le sens allégué. Une seule firme finale ne permet toutefois pas d’identifier un paramètre PQ distinct d’un mouvement de campagne ou d’un effet de méthode. [Résultat officiel](https://www.electionsquebec.qc.ca/resultats-et-statistiques/resultats-generales/2014-04-07/); [archive Qc125](https://qc125.com/canada/bulletin-qc2014.htm). |
| 2018 | Derniers Léger/Mainstreet/Forum : **19-20 %**; résultat : **17,06 %**, soit environ +1,94 à +2,94. | L’écart PQ est réel, mais le grand raté de l’élection concernait surtout CAQ/PLQ. L’analyse publiée de [Durand et Blais (2020)](https://www.cambridge.org/core/journals/canadian-journal-of-political-science-revue-canadienne-de-science-politique/article/abs/quebec-2018-a-failure-of-the-polls/97380BA7567B11B95E88FAA2149BDC51) attribue l’essentiel de l’écart total aux mouvements de dernière minute et aux non-déclarants, avec hétérogénéité régionale. |
| 2022 | Résultat PQ : **14,61 %**. Dernier Léger : **15 %** (+0,39); dernier Forum : **17,2 %** (+2,59). | Le biais dépend directement de la firme et de la règle d’agrégation. Le dernier [Léger](https://leger360.com/fr/la-politique-au-quebec-2-octobre-2022/) est presque exact pour le PQ; [Élections Québec](https://www.electionsquebec.qc.ca/en/results-and-statistics/general-election-results/2022-10-03/) fournit le résultat officiel. |

**Conclusion spécifique.** La fourchette « +1,7 à +2,9 » peut résulter d’une moyenne finale définie par Route 127; elle ne décrit pas chaque dernier sondage. La [méthodologie de Route 127](https://route127.ca/methodologie) est une source grise transparente : elle calibre une erreur systémique sur les écarts des trois dernières élections. Il s’agit d’un choix de modélisation praticien, non d’une validation scientifique indépendante d’un coefficient PQ de 2,3.

**Francophones, souverainistes et hors Montréal.** Les travaux de 1998 examinent notamment l’électorat francophone et trouvent que les sondages sous-estimaient le PLQ chez les francophones. Le chapitre de 2012 documente l’ancienne question des « discrets ». Je n’ai toutefois trouvé aucune étude évaluée par les pairs qui établisse, pour la période récente, un biais stable propre aux souverainistes, aux francophones hors Montréal ou aux répondants péquistes et qui en estime un coefficient transportable à 2026.

## Q4 — Cinq ou six semaines avant le vote n’est pas la veille du vote

**Établi.** Les sondages deviennent en moyenne plus proches du résultat en approchant du scrutin. [Jennings et Wlezien](https://www.nature.com/articles/s41562-018-0315-6) montrent une convergence structurée au cours de la chronologie électorale. [Fournier et al. (2004)](https://www.sciencedirect.com/science/article/pii/S0261379403000751), à partir de l’Étude électorale canadienne, montrent que les électeurs qui décident pendant la campagne sont réellement plus sensibles aux événements et à la couverture. [Box-Steffensmeier et al. (2015)](https://www.sciencedirect.com/science/article/pii/S026137941500058X) concluent que les décideurs tardifs sont systématiquement moins prévisibles.

**Nuance.** La proximité ne garantit pas une disparition monotone de l’erreur : en 2020 aux États-Unis, le rapport AAPOR ne trouve pratiquement pas d’amélioration entre les deux dernières semaines, la dernière semaine et les trois derniers jours. Les mouvements tardifs peuvent être faibles ou importants selon l’élection et n’ont pas de direction partisane universelle.

**Conséquence conceptuelle.** Pour un sondage à J−35 ou J−42, il faut séparer deux variables :

1. l’erreur de mesure de l’intention au jour du terrain;
2. l’innovation de campagne entre ce jour et le vote.

Calibrer la première avec l’écart entre un sondage final et le résultat, puis appliquer la correction à J−42, mélange les deux. Un modèle dynamique devrait faire croître la variance prospective avec l’horizon, sans supposer que le PQ perdra en moyenne 2,3 points.

## Q5 — Favori, deuxième ou troisième : l’erreur change-t-elle de signe?

**Établi.** Les grands partis présentent en moyenne une erreur absolue plus élevée en points : Jennings et Wlezien trouvent environ 2,3 points pour les partis dépassant 20 %. C’est largement mécanique et statistique : une part près de zéro ne peut pas être surestimée de 10 points aussi facilement qu’une part de 35 %. Ce résultat justifie une variance dépendante du niveau de soutien.

**Non établi.** Je n’ai pas trouvé de résultat comparatif robuste selon lequel le favori serait systématiquement surestimé, le deuxième correctement mesuré et le troisième sous-estimé, ou l’inverse. La position ordinale est endogène à la part de vote, à la compétitivité et au système partisan. En faire une correction directionnelle risquerait de confondre niveau, volatilité et statut médiatique.

**Pour 2026.** Le passage du PQ d’une force de troisième rang à un favori potentiel fragilise précisément l’extrapolation de 2018-2022. On peut faire dépendre la variance de sa part prévue; on ne devrait pas conserver automatiquement le même signe de biais.

## Q6 — Swing uniforme, proportionnel et mélange 80/20

**Établi.** Un swing additif uniforme applique le même changement en points à toutes les circonscriptions; un swing proportionnel multiplie les anciennes parts par un facteur national. Le premier peut produire des valeurs impossibles aux extrêmes; le second peut mal représenter les basculements lorsque les partis partent de niveaux très différents. Les modèles modernes utilisent aussi l’échelle logit, des effets régionaux, des transitions individuelles ou une distribution hiérarchique des swings.

[Erfort et al. (2026)](https://www.sciencedirect.com/science/article/pii/S0261379426000624) comparent plusieurs variantes sur huit élections fédérales allemandes et en simulation. Les différences moyennes sont souvent modestes, mais elles affectent la précision; le swing uniforme fonctionne mieux lorsque le swing national est grand, la volatilité locale faible et le nombre de partis élevé. C’est la meilleure comparaison évaluée par les pairs trouvée, mais elle n’est ni britannique ni québécoise.

Au Royaume-Uni, [Hanretty, Lauderdale et Vivyan (2016)](https://ueaeprints.uea.ac.uk/id/eprint/57496/) proposent un « generalized normal swing » combinant sondages nationaux et de circonscription. Les exit polls britanniques utilisent des régressions sur les caractéristiques de circonscription plutôt qu’un simple swing uniforme; [Curtice et al. (2017)](https://ora.ox.ac.uk/objects/uuid%3Abbb61aff-a024-4d1a-a4ce-3f13e1ce8b17) montrent leur grande précision en 2017. Mais un exit poll observé le jour même n’est pas une validation directe d’un modèle préélectoral québécois.

**Non établi.** Je n’ai trouvé aucune validation évaluée par les pairs d’un poids universel **80 % uniforme / 20 % proportionnel**. Des praticiens canadiens mélangent ces familles, mais le poids est un hyperparamètre. Il doit être choisi par validation hors échantillon, idéalement en laissant une élection entière de côté, et comparé à un swing régional/logit. Un 80/20 peut être raisonnable comme point de départ; il ne bénéficie pas d’un statut scientifique particulier.

## Q7 — Agrégation, récence, effets de maison et herding

**Récence.** Une demi-vie fixe de 14 jours, comme celle décrite dans le [lexique de Route 127](https://route127.ca/en/lexique), est une règle praticienne intelligible, mais je n’ai trouvé aucune étude qui valide 14 jours comme constante optimale pour le Québec. Les modèles de Jackman et Linzer utilisent plutôt un état latent évoluant dans le temps : les données apprennent la vitesse du mouvement et l’incertitude augmente lorsqu’il y a peu de sondages.

**Effets de maison.** Ils doivent être estimés par firme, mode et population cible, avec rétrécissement pour les firmes nouvelles. Jackman souligne aussi un problème d’identification : avant l’élection, on ne peut pas savoir sans hypothèse si la moyenne de l’industrie est elle-même biaisée. Centrer mécaniquement les maisons autour de zéro ne supprime pas le biais partagé.

**Herding.** Le rapport britannique dirigé par [Sturgis et al. (2016)](https://eprints.soton.ac.uk/390588) conclut que l’erreur de 2015 provenait principalement d’échantillons non représentatifs; la faible dispersion tardive était compatible avec du herding, sans preuve suffisante qu’il expliquait le raté. L’[AAPOR 2024](https://aapor.org/wp-content/uploads/2025/10/Task-Force-on-2024-Pre-Election-Polling-Report-Executive-Summary.pdf) ne trouve pas de preuve de herding malgré une dispersion faible, qu’il relie plutôt à des variables politiques communes de sélection et pondération.

**Implication.** Une moyenne poll-by-poll devrait comprendre : erreur d’échantillonnage, effet de maison partiellement mutualisé, état latent temporel, biais commun d’élection et covariance entre partis. Elle ne doit pas traiter les sondages comme indépendants ni interpréter une faible dispersion comme preuve que l’incertitude réelle est faible.

## Q8 — Avantage du député sortant et du chef dans sa circonscription

**Député sortant.** Dans les élections fédérales canadiennes de 1867 à 2008, [Kendall et Rekkas (2012)](https://ideas.repec.org/a/wly/canjec/v45y2012i4p1560-1585.html) estiment par discontinuité de régression une hausse de 9,4 à 11,2 points de probabilité de gagner et environ 2,4 à 2,8 points de part de vote; l’effet semble surtout individuel. Mais [Sevi (2025)](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/A604D0F1FAD60EEF0FD0159762BE1933/S0008423925000058a.pdf/the-incumbency-advantage-in-canadian-elections.pdf), avec les élections fédérales de 1867 à 2021, estime qu’après 1972 l’effet moyen n’est plus qu’environ 2 points de probabilité et n’est pas statistiquement significatif. La magnitude est donc sensible à la période et au modèle.

**Candidat local.** [Blais et al. (2003)](https://www.cambridge.org/core/journals/canadian-journal-of-political-science-revue-canadienne-de-science-politique/article/abs/does-the-local-candidate-matter-candidate-effects-in-the-canadian-election-of-2000/9E0027D9ABC436C4357C37F570DEF903) estiment que le candidat local fut décisif pour 5 % des électeurs canadiens, 6 % hors Québec mais seulement 2 % au Québec en 2000. Ce n’est pas un bonus uniforme de part de vote.

**Chef dans sa propre circonscription.** Je n’ai trouvé aucune estimation évaluée par les pairs, propre au Canada ou au Québec, qui permette d’ajouter un nombre fixe de points au chef. Les chefs choisissent souvent une circonscription favorable; comparer leur résultat à celui du parti sans corriger cette sélection surestime l’« effet chef ». Un bonus devrait être estimé sur des résidus de circonscription, avec contrôles pour la force historique, le sortant, la région, la redistribution et la qualité des adversaires, puis fortement rétréci.

## Lacunes de la littérature et des données

1. **Aucun post-mortem universitaire repéré pour Québec 2022** qui décompose mouvement tardif, non-réponse, participation, firme et parti.
2. **Aucune validation propre au Québec** d’un coefficient PQ stable, d’une demi-vie de 14 jours ou d’un mélange swing 80/20.
3. **Très peu d’élections comparables.** Les frontières partisanes et les méthodes de sondage ont changé; les observations ne sont pas échangeables sans modèle.
4. **Définition instable du “dernier sondage”.** Firme, date de fin de terrain, suivi chevauchant, arrondi, population (adultes, inscrits, probables) et moyenne choisie modifient l’erreur.
5. **Données régionales insuffisantes.** Les hypothèses sur francophones, souverainistes et hors Montréal manquent d’échantillons harmonisés et de microdonnées de non-réponse.
6. **Effet chef non identifié.** Les cas sont rares et sélectionnés; les élections partielles et changements de circonscription compliquent les comparaisons.
7. **Validation de sièges rarement probabiliste.** Une bonne moyenne de sièges peut masquer une mauvaise calibration des probabilités circonscription par circonscription.

## Implications de modélisation recommandées

### 1. Remplacer −2,3 fixe par un biais PQ hiérarchique, centré près de zéro

Modéliser \(b_{PQ,e}\) comme un effet d’élection tiré d’une distribution à queues épaisses, avec moyenne PQ fortement rétrécie vers la moyenne de tous les partis et variance estimée. La correction de 2,3 peut rester un scénario pessimiste, pas le centre.

**Contre-argument :** trois erreurs de même signe sont informatives.  
**Condition d’échec :** si une validation prospective ou leave-one-election-out montre qu’un biais non nul et stable améliore nettement le log score et la calibration, le rétrécissement vers zéro serait trop fort.

### 2. Séparer maintenantcast et forecast de jour d’élection

Un état latent mesure l’intention au jour du terrain; un processus de campagne propage cette intention jusqu’au vote, avec variance croissante selon l’horizon et corrélations régionales/partisanes. Ne pas appliquer un résidu de sondage final comme correction actuelle à J−42.

**Contre-argument :** le public veut un résultat électoral, pas une intention présente.  
**Condition d’échec :** si l’historique montre des trajectoires quasi nulles et une variance identique quel que soit l’horizon, la couche dynamique ajoute de la complexité sans gain.

### 3. Modéliser les parts conjointement et les erreurs communes

Utiliser une transformation log-ratio ou un multinomial logit pour que les parts restent positives et totalisent 100 %. Ajouter un choc commun d’élection, des effets de maison/mode et une covariance entre partis. Toute baisse du PQ doit être redistribuée probabilistiquement, non ajoutée arbitrairement au principal adversaire.

**Contre-argument :** le modèle devient moins transparent.  
**Condition d’échec :** avec trop peu de données, une matrice de covariance libre sera instable; employer alors une structure parcimonieuse ou factorielle.

### 4. Choisir la récence et le swing par validation “élection entière laissée de côté”

Comparer demi-vies, random walk, swing additif, proportionnel, logit, régional et mélanges; retenir le modèle sur des scores de probabilité, l’erreur de part par circonscription, l’erreur de sièges et la couverture des intervalles. L’hyperparamètre 80/20 ne doit pas être choisi sur les mêmes élections servant à publier sa performance.

**Contre-argument :** le Québec offre peu de scrutins modernes.  
**Condition d’échec :** si le classement varie énormément selon l’élection laissée de côté, publier un ensemble de modèles et intégrer l’incertitude de structure plutôt que choisir un gagnant.

### 5. Traiter sortant et chef comme effets locaux régularisés

Inclure un effet sortant contemporain faible, avec interaction parti/période, et estimer l’effet chef sur le résidu local après contrôles. Ne jamais transposer directement le +2,4 à +2,8 fédéral historique de Kendall-Rekkas au Québec provincial de 2026.

**Contre-argument :** certains chefs ont manifestement une prime personnelle.  
**Condition d’échec :** si les chefs changent stratégiquement de circonscription ou affrontent des candidats atypiques, même un effet contrôlé demeure endogène; le présenter alors comme scénario.

## Bibliographie annotée

### Articles et ouvrages évalués par les pairs

- **Shirani-Mehr, H., Rothschild, D., Goel, S. et Gelman, A. (2018).** “Disentangling Bias and Variance in Election Polls.” *Journal of the American Statistical Association*, 113(522), 607-614. [doi:10.1080/01621459.2018.1448823](https://doi.org/10.1080/01621459.2018.1448823). — Quantifie l’écart entre marge d’échantillonnage et erreur totale, ainsi que le biais commun à une élection.
- **Jennings, W. et Wlezien, C. (2018).** “Election polling errors across time and space.” *Nature Human Behaviour*, 2, 276-283. [doi:10.1038/s41562-018-0315-6](https://doi.org/10.1038/s41562-018-0315-6). — Offre la plus vaste comparaison temporelle et internationale utilisée ici.
- **Tierney, G. et Volfovsky, A. (2025).** “Bias and excess variance in election polling: a not-so-hidden Markov model.” *Journal of the Royal Statistical Society Series A*, 188(2), 566-582. [doi:10.1093/jrsssa/qnae066](https://doi.org/10.1093/jrsssa/qnae066). — Montre que les post-mortems statiques confondent mouvement des préférences et erreur de sondage et surestiment le biais.
- **Jackman, S. (2005).** “Pooling the polls over an election campaign.” *Australian Journal of Political Science*, 40(4), 499-517. [doi:10.1080/10361140500302472](https://doi.org/10.1080/10361140500302472). — Modèle dynamique d’agrégation et d’effets de maison.
- **Linzer, D. A. (2013).** “Dynamic Bayesian Forecasting of Presidential Elections in the States.” *Journal of the American Statistical Association*, 108(501), 124-134. [doi:10.1080/01621459.2012.737735](https://doi.org/10.1080/01621459.2012.737735). — Exemple canonique de mutualisation hiérarchique entre temps et territoires.
- **Durand, C., Blais, A. et Vachon, S. (2001).** “A Late Campaign Swing or a Failure of the Polls? The Case of the 1998 Quebec Election.” *Public Opinion Quarterly*, 65(1), 108-123. [JSTOR](http://www.jstor.org/stable/3078789). — Post-mortem québécois clé concluant surtout à des problèmes communs de couverture et de non-réponse.
- **Durand, C. et Blais, A. (2020).** “Quebec 2018: A Failure of the Polls?” *Canadian Journal of Political Science*, 53(1), 133-150. [doi:10.1017/S000842392000013X](https://doi.org/10.1017/S000842392000013X). — Attribue la majeure partie du raté de 2018 à des mouvements tardifs et aux non-déclarants, variables régionalement.
- **Durand, C. (2013).** “Les sondages et l’élection québécoise de 2012.” Dans *Les Québécois aux urnes*, Presses de l’Université de Montréal, 163-176. [doi:10.1515/9782760632264-012](https://doi.org/10.1515/9782760632264-012). — Retrace les biais québécois et la répartition non proportionnelle des électeurs « discrets ».
- **Fournier, P., Nadeau, R., Blais, A., Gidengil, E. et Nevitte, N. (2004).** “Time-of-voting decision and susceptibility to campaign effects.” *Electoral Studies*, 23(4), 661-681. [doi:10.1016/j.electstud.2003.09.001](https://doi.org/10.1016/j.electstud.2003.09.001). — Établit avec des données canadiennes que les décideurs de campagne répondent davantage aux événements.
- **Box-Steffensmeier, J. M., Dillard, M., Kimball, D. et Massengill, W. (2015).** “The long and short of it: The unpredictability of late deciding voters.” *Electoral Studies*, 39, 181-194. [doi:10.1016/j.electstud.2015.03.013](https://doi.org/10.1016/j.electstud.2015.03.013). — Documente l’incertitude supérieure des électeurs tardifs.
- **Erfort, C., Gschwend, T., Stoetzer, L. F. et Munzert, S. (2026).** “How swing model assumptions shape vote-to-seat predictions.” *Electoral Studies*, 102, article 103104. [doi:10.1016/j.electstud.2026.103104](https://doi.org/10.1016/j.electstud.2026.103104). — Compare directement swings uniforme et proportionnel; aucune pondération 80/20 universelle n’en découle.
- **Hanretty, C., Lauderdale, B. et Vivyan, N. (2016).** “Combining national and constituency polling for forecasting.” *Electoral Studies*, 41, 239-243. [doi:10.1016/j.electstud.2015.11.019](https://doi.org/10.1016/j.electstud.2015.11.019). — Propose un swing généralisé conciliant données nationales et locales britanniques.
- **Curtice, J., Fisher, S., Kuha, J. et Mellon, J. (2017).** “Surprise, surprise! (again): The 2017 British general election exit poll.” *Significance*, 14(4), 26-29. [doi:10.1111/j.1740-9713.2017.01054.x](https://doi.org/10.1111/j.1740-9713.2017.01054.x). — Illustre le gain des modèles de circonscription calibrés, tout en portant sur un exit poll.
- **Kendall, C. et Rekkas, M. (2012).** “Incumbency advantages in the Canadian Parliament.” *Canadian Journal of Economics*, 45(4), 1560-1585. [doi:10.1111/j.1540-5982.2012.01739.x](https://doi.org/10.1111/j.1540-5982.2012.01739.x). — Estime un avantage fédéral historique important, surtout individuel.
- **Sevi, S. (2025).** “The Incumbency Advantage in Canadian Elections.” *Canadian Journal of Political Science*, 58(2), 397-407. [doi:10.1017/S0008423925000058](https://doi.org/10.1017/S0008423925000058). — Montre que l’avantage devient faible et non significatif après 1972 dans l’ensemble.
- **Blais, A., Gidengil, E., Dobrzynska, A., Nevitte, N. et Nadeau, R. (2003).** “Does the Local Candidate Matter? Candidate Effects in the Canadian Election of 2000.” *Canadian Journal of Political Science*, 36(3), 657-664. [doi:10.1017/S0008423903778810](https://doi.org/10.1017/S0008423903778810). — Estime que le candidat local fut décisif pour seulement 2 % des électeurs québécois étudiés.

### Rapports méthodologiques, sources officielles et sources grises

- **Kennedy, C. et al. (2017).** *An Evaluation of 2016 Election Polls in the U.S.* American Association for Public Opinion Research. [Rapport](https://aapor.org/wp-content/uploads/2023/01/AAPOR-2016-Election-Polling-Report.pdf). — Rapport professionnel majeur établissant l’absence de direction partisane stable entre élections.
- **Task Force on 2020 Pre-Election Polling (2021).** *An Evaluation of the 2020 General Election Polls.* AAPOR. [Rapport](https://aapor.org/wp-content/uploads/2022/11/AAPOR-Task-Force-on-2020-Pre-Election-Polling_Report-FNL.pdf). — Montre un important biais partagé et l’absence d’amélioration dans les tout derniers jours.
- **AAPOR Task Force (2025).** *2024 Pre-Election Polling: An Evaluation of the 2024 General Election Polls.* [Rapport](https://aapor.org/wp-content/uploads/2025/10/Task-Force-on-2024-Pre-Election-Polling_Report.pdf). — Ne trouve pas de preuve de herding et rappelle l’alternance historique de la direction des erreurs.
- **Sturgis, P. et al. (2016).** *Report of the Inquiry into the 2015 British General Election Opinion Polls.* Market Research Society/British Polling Council. [Dépôt institutionnel](https://eprints.soton.ac.uk/390588). — Identifie les échantillons non représentatifs comme cause principale du raté britannique de 2015.
- **Élections Québec.** Résultats officiels de [2014](https://www.electionsquebec.qc.ca/resultats-et-statistiques/resultats-generales/2014-04-07/), [2018](https://www.electionsquebec.qc.ca/resultats-et-statistiques/resultats-generales/2018-10-01/736/) et [2022](https://www.electionsquebec.qc.ca/en/results-and-statistics/general-election-results/2022-10-03/). — Dénominateur officiel pour mesurer les écarts sondage-résultat.
- **Route 127.** “Méthodologie” et “Lexique”. [Méthodologie](https://route127.ca/methodologie); [lexique](https://route127.ca/en/lexique). — Source grise utile pour comprendre la calibration à trois élections et la demi-vie de 14 jours, sans validation indépendante publiée.

## Verdict final

**Appui scientifique :** fort pour élargir l’incertitude au-delà de la marge d’échantillonnage; modéré pour des effets de maison et un choc commun d’élection; faible pour une moyenne historique propre au PQ avec seulement trois scrutins; **insuffisant pour soustraire automatiquement 2,3 points au PQ en 2026**. Le coefficient peut être conservé comme test de robustesse clairement étiqueté. Il ne devrait devenir le centre de la distribution qu’après une validation hors échantillon démontrant un gain prédictif stable malgré le changement de position du PQ et l’horizon de cinq à six semaines.
