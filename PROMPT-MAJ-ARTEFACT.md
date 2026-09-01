# Prompt — mise à jour de la page « Tendances Québec 2026 »

À coller dans une nouvelle conversation, une fois le dossier `PROJET IA/sondages` connecté
et le PDF du nouveau sondage déposé dans `Data/`.

**Adresse de l'artefact :** `https://claude.ai/code/artifact/bf929925-fad6-450d-8555-5fbc9b66199c`

---

```
Tu mets à jour le modèle de projection électorale QC127 et sa page publiée.
La méthode est fixée : tu l'appliques, tu ne la réinventes pas.

À LIRE D'ABORD, dans cet ordre
1. RUNBOOK.md  — procédure, huit contrôles, règle d'arrêt
2. memoire.txt — état du projet et principes acquis
3. TODO.md     — section JOURNAL seulement

Fichier de travail : le ModeleVivantQC127 le plus récent du dossier.
Page à mettre à jour : livrables/tendances.html (source) et
tendances-quebec-2026.html (copie autonome, à la racine).

ÉTAPE 1 — LE SONDAGE
Extrais du PDF les intentions de vote APRÈS répartition des indécis, au national et
par région, avec le n de chaque sous-échantillon. Ajoute les lignes dans l'onglet
Sondages du classeur, en respectant à la lettre les noms de région de la colonne C.
Ajoute aussi la ligne nationale dans data/sondages_national.csv, au format
  date|firme|n|CAQ|PLQ|QS|PQ|PCQ
Si la firme ne ventile pas l'Île et la banlieue — c'est le cas de Léger —, ne saisis
rien pour ces deux régions : l'agrégat s'en charge. Ne reconstruis jamais à la main.

ÉTAPE 2 — LE CLASSEUR
Recalcule, puis passe les huit contrôles de non-régression du runbook, réplication
Python du scénario A comprise. Un seul échec arrête tout.

ÉTAPE 3 — LA PAGE
Lance depuis le dossier :
  python3 pipeline/maj_artefact.py --classeur <le classeur> --recalculer

Le script recalcule le lissage, remplace les blocs de données de la page, met à jour
la date et le nombre de sondages, régénère la copie autonome, et affiche un rapport.
Ne modifie JAMAIS les blocs `const D` et `const SEATS` à la main : c'est le travail
du script, et une erreur de virgule y casse la page en silence.

ÉTAPE 4 — LE TEXTE
Le script ne touche pas au texte, volontairement. Il imprime la liste des passages
qui contiennent des chiffres écrits en toutes lettres. Relis-les et corrige CE QUI
EST DEVENU FAUX, sans réécrire ce qui reste vrai :
  · le chapeau
  · les quatre paragraphes de « Ce que la courbe dit »
  · le paragraphe PCQ de « D'ici le 5 octobre »
  · l'encadré « quatorze circonscriptions sur soixante-huit »
  · la ligne de mise à jour du pied de page
Le reste du texte est stable et ne doit pas bouger d'une vague à l'autre.

ÉTAPE 5 — PUBLIER
L'artefact existe déjà. Pour le mettre à jour SANS en créer un second :
  a) Artifact avec action:"read" et url:"https://claude.ai/code/artifact/bf929925-fad6-450d-8555-5fbc9b66199c"
  b) puis Artifact avec file_path:"livrables/tendances.html" ET la même url.
Publier sans le paramètre url crée un artefact séparé et casse les liens partagés.
Ne change ni le titre, ni le favicon.

Écris ensuite la copie autonome dans le dossier, à la racine, sous son nom actuel.

Si l'outil Artifact n'est pas disponible dans ta session : produis quand même la copie
autonome mise à jour, dis-le clairement, et n'invente pas d'autre méthode de publication.

RÈGLE D'ARRÊT
Tu t'arrêtes et tu expliques, sans publier, si :
 · un des huit contrôles échoue ;
 · un parti bouge de plus de dix sièges par rapport au calcul précédent ;
 · un parti atteint 64 sièges — la page affirme partout qu'aucun scénario n'y arrive,
   et il faudrait la réécrire, pas la rafraîchir ;
 · une pente change de signe — le récit de la page devient faux ;
 · une région saisie ne somme pas à 100 ± 1, ou un sous-échantillon est sous n=100 ;
 · les partis ne sont pas identifiables en texte dans le PDF (tableaux sous forme de
   graphiques : l'identité se lit aux couleurs et l'erreur y est silencieuse).

CONVENTIONS
Français québécois. Un panel web publie un intervalle de crédibilité, pas une marge
d'erreur. Ne jamais publier un décompte de sièges tiré d'un seul sondage : la sortie
du modèle est l'agrégat. Toute recommandation s'accompagne d'un contre-argument.

RENDS COMPTE À LA FIN
Le tableau des sièges, le niveau et la pente, l'écart avec le calcul précédent, les
phrases que tu as corrigées, et la confirmation que l'artefact a été republié à la
même adresse.
```

---

## Notes pour toi, Sylvain

**Ce que le script fait tout seul** : le lissage, les six scénarios, la date, le nombre
de sondages en toutes lettres, la copie autonome, et un rapport d'alertes qui compare à
l'état précédent.

**Ce qu'il ne fait pas, exprès** : réécrire le texte. Une phrase comme « la remontée
caquiste ralentit » peut devenir fausse sans qu'aucun chiffre du script ne le signale.
C'est le seul endroit où un jugement humain reste nécessaire, et c'est pour ça que
l'étape 4 est séparée.

**Le piège de la republication** : depuis une nouvelle conversation, il faut d'abord
lire l'artefact puis republier en passant son adresse. Sans ça, un second artefact est
créé et tous les liens déjà partagés continuent de pointer vers la vieille version —
sans erreur visible. C'est la seule manœuvre du processus qui échoue silencieusement.
