# Récolte des séries qc125

`recolte_qc125.js` sort un CSV (séparateur `|`) prêt pour l'onglet `Sondages`.

## Marche à suivre

1. Ouvrir `https://qc125.com/sondages.htm`, exécuter le script, coller le résultat dans `data/qc125-regions.csv`.
2. Ouvrir `https://qc125.com/sondages-demo.htm`, exécuter le même script, coller dans `data/qc125-demo.csv`.

Le paramètre `?demo=` de l'URL ne change rien : les onglets sont basculés côté client et **toutes** les tables sont déjà chargées dans `window.demopoll_TABLE_DATA.demos`.

## Ce que chaque table contient

| Clé | Contenu | Utilisé par le modèle |
|---|---|---|
| `National` | Intentions provinciales | oui — niveau et pente |
| `MTL` | Montréal RMR | oui — décalage régional |
| `QC` | Québec RMR | oui — décalage régional |
| `REG` | Ailleurs au Québec | oui — décalage régional |
| `FR` | Francophones | oui — couche linguistique |
| `NF` | Non-francophones | oui — couche linguistique |
| `m` `f` `age1` `age2` `age3` | Genre et âge | non |

## Pièges

- **Ordre des colonnes : CAQ, PLQ, QS, PQ, PCQ.** Ce n'est pas l'ordre affiché dans la légende du graphique de la page, qui est PLQ, PQ, CAQ, QS, PCQ. Toujours vérifier sur un sondage connu avant de charger.
- **qc125 ne ventile pas l'Île et la banlieue de Montréal.** Ces décalages continuent de venir des rapports PDF de Pallas, Synopsis et du Léger cumulatif.
- Les astérisques dans les tables `age2` et `age3` marquent des tranches d'âge recodées (Pallas utilise 35-49 / 50-64 / 65+, Léger 35-54 / 55+). Le script les retire; ne pas traiter ces valeurs comme des mesures brutes.
- Les lignes de résultats d'élection sont exclues par `r.generalelx`.
