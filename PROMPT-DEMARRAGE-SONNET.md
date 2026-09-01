# Prompt de démarrage — session d'exécution (Sonnet)

À coller tel quel dans une nouvelle conversation, une fois le dossier
`PROJET IA/sondages` connecté et le PDF du sondage déposé dans `Data/`.

---

```
Tu intègres un nouveau sondage au modèle de projection électorale QC127.
C'est une tâche d'exécution : la méthode est déjà fixée, ne la réinvente pas.

AVANT DE COMMENCER, lis dans cet ordre :
1. RUNBOOK.md  — la procédure, les huit contrôles et la règle d'arrêt
2. memoire.txt — l'état du projet et les principes acquis
3. TODO.md     — section JOURNAL seulement, pour savoir ce qui est déjà fait

Le fichier de travail est ModeleVivantQC127_v7_agregat.xlsx.
Les versions v3 à v6 sont historiques : ne pas les rouvrir, ne pas les modifier.

CE QUE TU FAIS
1. Le PDF du nouveau sondage est dans Data/, nommé AAAA-MM-JJ-firme.pdf
   (date de FIN DE TERRAIN).
2. Extrais les intentions de vote APRÈS répartition des indécis, au national et
   par région, avec le n de chaque sous-échantillon.
3. Ajoute les lignes correspondantes dans l'onglet Sondages : une ligne PROVINCE
   plus une ligne par région publiée. Respecte scrupuleusement les noms de région
   déjà utilisés dans la colonne C — l'agrégat fonctionne par correspondance exacte.
4. Recalcule le classeur (openpyxl n'évalue pas les formules).
5. Passe les huit contrôles de non-régression du RUNBOOK, réplication Python du
   scénario A comprise.
6. Rends compte : le tableau des sièges, le niveau national et la pente, et
   l'écart avec le calcul précédent.

CE QUE TU NE FAIS PAS
- Tu ne modifies aucune formule des onglets Agrégat, Régions, Modèle ou Sièges.
- Tu ne saisis pas de valeurs pour l'Île de Montréal ni la Banlieue si la firme
  ne les publie pas. L'agrégat s'en charge. Ne reconstruis rien à la main.
- Tu n'entres aucun chiffre tiré d'un article de presse, d'un résumé ou d'une
  déduction. Uniquement le rapport de la firme.
- Tu ne publies pas de décompte de sièges fondé sur ce seul sondage : la sortie
  du modèle est l'agrégat, jamais la dernière vague.
- Tu n'écrases pas le fichier : tu produis une nouvelle version datée.

RÈGLE D'ARRÊT
Si un contrôle échoue, si un parti bouge de plus de dix sièges par rapport au
calcul précédent, si une région ne somme pas à 100 ± 1, si un sous-échantillon
est sous n=100, ou si les libellés de partis ne sont pas lisibles en texte dans
le PDF (tableaux sous forme de graphiques — l'identité des partis se lit alors
aux couleurs et l'erreur est silencieuse) : tu t'arrêtes, tu expliques, et tu
attends. Tu ne devines pas.

CONVENTIONS
Français québécois. Faits et interprétation clairement distingués. Toute
recommandation s'accompagne d'un contre-argument ou d'une condition d'échec.
Un panel web publie un intervalle de crédibilité, pas une marge d'erreur.

AVERTISSEMENT À REPRENDRE DANS TOUT LIVRABLE
La relation intentions-sièges est fortement non linéaire dans le régime actuel :
la CAQ est dans la zone où deux points de pourcentage déplacent des dizaines de
sièges. Un décompte n'est pas une prévision.
```

---

## Note

Ce prompt couvre la **boucle** d'intégration d'un sondage. Il ne couvre pas les
imprévus. Tout ce qui touche la transposition géographique, les formules de
l'`Agrégat`, un changement de méthode, ou une source qui paraît anormale doit
remonter à la conversation principale plutôt qu'être tranché en séance
d'exécution.
