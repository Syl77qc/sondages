import fs from "node:fs/promises";
import { Workbook, SpreadsheetFile } from "@oai/artifact-tool";

const data = JSON.parse(await fs.readFile("pipeline/qc127_geo_data.json", "utf8"));
const outputDir = "outputs/qc127_geo_20260829";
await fs.mkdir(outputDir, { recursive: true });

const wb = Workbook.create();
const seats = wb.worksheets.add("Sièges");
const model = wb.worksheets.add("Modèle");
const regions = wb.worksheets.add("Régions");
const map = wb.worksheets.add("Carte 2026");
const crosswalk = wb.worksheets.add("Correspondance");
const method = wb.worksheets.add("Méthodologie");

const navy = "#1F4E78";
const lightBlue = "#D9EAF7";
const inputBlue = "#0000FF";
const white = "#FFFFFF";
const gray = "#F2F2F2";
const green = "#C6EFCE";
const yellow = "#FFD966";
const red = "#F4CCCC";
const parties = ["CAQ", "PLQ", "QS", "PQ", "PCQ", "Autre"];

function title(range, text) {
  range.merge();
  range.values = [[text]];
  range.format = { fill: navy, font: { bold: true, color: white, size: 15 }, horizontalAlignment: "center", verticalAlignment: "center" };
}
function header(range) {
  range.format = { fill: navy, font: { bold: true, color: white }, horizontalAlignment: "center", verticalAlignment: "center", wrapText: true };
}
function colLetter(n) {
  let s = "";
  while (n > 0) { n--; s = String.fromCharCode(65 + n % 26) + s; n = Math.floor(n / 26); }
  return s;
}
function winnerFormula(startCol, row) {
  const cells = parties.map((_, i) => `${colLetter(startCol + i)}${row}`);
  const mx = `MAX(${cells[0]}:${cells.at(-1)})`;
  let f = `"Autre"`;
  for (let i = parties.length - 2; i >= 0; i--) f = `IF(${mx}=${cells[i]},"${parties[i]}",${f})`;
  return `=${f}`;
}

// Sièges
seats.showGridLines = false;
title(seats.getRange("A1:H1"), "MODÈLE VIVANT QC127 – PROJECTIONS ÉLECTORALES v4.1 GÉOSPATIAL");
seats.getRange("A2:H2").merge();
seats.getRange("A2").values = [["Synopsis Recherche / La Presse, 24–26 août 2026 | Référence 2022 transposée par chevauchement géographique pondéré | Seuil majorité : 64 sièges"]];
seats.getRange("A2:H2").format = { font: { italic: true, color: "#666666" }, horizontalAlignment: "center" };
seats.getRange("A4:H4").values = [["Scénario", ...parties, "Majorité?"]];
header(seats.getRange("A4:H4"));
const scenarioLabels = [
  "Référence 2022 transposée",
  "Scén. A – Swing proportionnel",
  "Scén. B – A + inertie locale",
  "Scén. C – Fourchette haute (+3,3 pp)",
  "Scén. D – Fourchette basse (–3,3 pp)",
];
seats.getRange("A5:A9").values = scenarioLabels.map(x => [x]);
const countCols = ["C", "AO", "AP", "AQ", "AR"];
for (let r = 5; r <= 9; r++) {
  const formulas = parties.map(p => `=COUNTIF('Modèle'!$${countCols[r-5]}$2:$${countCols[r-5]}$128,"${p}")`);
  seats.getRange(`B${r}:G${r}`).formulas = [formulas];
  seats.getRange(`H${r}`).formulas = [[`=IF(MAX(B${r}:G${r})>=64,"OUI ✓","non")`]];
}
seats.getRange("A5:H5").format.fill = gray;
seats.getRange("A6:H6").format.fill = green;
seats.getRange("A7:H7").format.fill = yellow;
seats.getRange("A8:H8").format.fill = "#BDD7EE";
seats.getRange("A9:H9").format.fill = red;
seats.getRange("A11:A12").values = [["Fourchette min (C vs D)"], ["Fourchette max (C vs D)"]];
for (let c = 2; c <= 7; c++) {
  const L = colLetter(c);
  seats.getRange(`${L}11`).formulas = [[`=MIN(${L}8,${L}9)`]];
  seats.getRange(`${L}12`).formulas = [[`=MAX(${L}8,${L}9)`]];
}
seats.getRange("A11:G12").format.fill = "#9DC3E6";
seats.getRange("A14").values = [["Bascules potentielles (< 5 pp) :"]];
seats.getRange("B14").formulas = [["=COUNTIF('Modèle'!$AT$2:$AT$128,\"Oui\")"]];
seats.getRange("A16:H16").merge();
seats.getRange("A16").values = [["LÉGENDE | A : swing régional proportionnel | B : A + inertie locale recalculée sur la carte 2026 | C/D : sondage ± marge | Cellules bleues : intrants modifiables | Références transposées au moyen des sections de vote 2026 pondérées par leurs électeurs."]];
seats.getRange("A16:H16").format = { font: { italic: true, color: "#666666", size: 9 }, wrapText: true };
seats.getRange("A1:H16").format.font.name = "Arial";
seats.getRange("A1:H16").format.borders = { preset: "inside", style: "thin", color: "#D9D9D9" };
seats.getRange("A:A").format.columnWidth = 36;
seats.getRange("B:H").format.columnWidth = 14;
seats.getRange("1:1").format.rowHeight = 28;
seats.getRange("16:16").format.rowHeight = 34;
seats.freezePanes.freezeRows(4);

// Modèle
model.showGridLines = false;
const modelHeaders = ["Circonscription","Région","Vainqueur réf.","CAQ 2022","PLQ 2022","QS 2022","PQ 2022","PCQ 2022","Autre 2022","Total","% CAQ","% PLQ","% QS","% PQ","% PCQ","% Autre","A-CAQ","A-PLQ","A-QS","A-PQ","A-PCQ","A-Autre","B-CAQ","B-PLQ","B-QS","B-PQ","B-PCQ","B-Autre","C-CAQ","C-PLQ","C-QS","C-PQ","C-PCQ","C-Autre","D-CAQ","D-PLQ","D-QS","D-PQ","D-PCQ","D-Autre","Vainq. A","Vainq. B","Vainq. C","Vainq. D","Marge réf.","Bascule","Résidu CAQ","Résidu PLQ","Résidu QS","Résidu PQ"];
model.getRange("A1:AX1").values = [modelHeaders];
header(model.getRange("A1:AX1"));
const baseRows = data.districts.map(d => [d.name,d.region,null,d.votes.CAQ,d.votes.PLQ,d.votes.QS,d.votes.PQ,d.votes.PCQ,d.votes.Autre,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,d.residuals.CAQ,d.residuals.PLQ,d.residuals.QS,d.residuals.PQ]);
model.getRange("A2:AX128").values = baseRows;
for (let r = 2; r <= 128; r++) {
  model.getRange(`C${r}`).formulas = [[winnerFormula(4, r)]];
  model.getRange(`J${r}`).formulas = [[`=SUM(D${r}:I${r})`]];
  model.getRange(`K${r}:P${r}`).formulas = [[...Array.from({length:6},(_,i)=>`=IFERROR(${colLetter(4+i)}${r}/J${r},0)`)]];
  model.getRange(`Q${r}:V${r}`).formulas = [[...Array.from({length:6},(_,i)=>`=${colLetter(4+i)}${r}*INDEX('Régions'!$T$2:$Y$6,MATCH($B${r},'Régions'!$A$2:$A$6,0),${i+1})`)]];
  model.getRange(`W${r}:AB${r}`).formulas = [[
    `=MAX(0,Q${r}+(AU${r}/100)*J${r}*'Régions'!$O$2)`,
    `=MAX(0,R${r}+(AV${r}/100)*J${r}*'Régions'!$O$2)`,
    `=MAX(0,S${r}+(AW${r}/100)*J${r}*'Régions'!$O$2)`,
    `=MAX(0,T${r}+(AX${r}/100)*J${r}*'Régions'!$O$2)`,
    `=U${r}`, `=V${r}`,
  ]];
  model.getRange(`AC${r}:AH${r}`).formulas = [[...Array.from({length:6},(_,i)=>`=${colLetter(4+i)}${r}*INDEX('Régions'!$Z$2:$AE$6,MATCH($B${r},'Régions'!$A$2:$A$6,0),${i+1})`)]];
  model.getRange(`AI${r}:AN${r}`).formulas = [[...Array.from({length:6},(_,i)=>`=${colLetter(4+i)}${r}*INDEX('Régions'!$AF$2:$AK$6,MATCH($B${r},'Régions'!$A$2:$A$6,0),${i+1})`)]];
  model.getRange(`AO${r}`).formulas = [[winnerFormula(17, r)]];
  model.getRange(`AP${r}`).formulas = [[winnerFormula(23, r)]];
  model.getRange(`AQ${r}`).formulas = [[winnerFormula(29, r)]];
  model.getRange(`AR${r}`).formulas = [[winnerFormula(35, r)]];
  model.getRange(`AS${r}`).formulas = [[`=(MAX(K${r}:P${r})-LARGE(K${r}:P${r},2))*100`]];
  model.getRange(`AT${r}`).formulas = [[`=IF(AS${r}<5,"Oui","Non")`]];
}
model.getRange("D2:I128").format.font.color = inputBlue;
model.getRange("AU2:AX128").format.font.color = inputBlue;
model.getRange("K2:P128").format.numberFormat = "0.0%";
model.getRange("AS2:AS128").format.numberFormat = "0.0";
model.getRange("D2:J128").format.numberFormat = "#,##0";
model.getRange("Q2:AN128").format.numberFormat = "#,##0";
model.getRange("AU2:AX128").format.numberFormat = "0.000";
model.getRange("A1:AX128").format.font.name = "Arial";
model.getRange("A1:AX128").format.font.size = 9;
model.getRange("A1:AX128").format.borders = { preset: "inside", style: "thin", color: "#E7E6E6" };
model.getRange("A:A").format.columnWidth = 28;
model.getRange("B:B").format.columnWidth = 22;
model.getRange("C:C").format.columnWidth = 14;
model.getRange("D:AX").format.columnWidth = 11;
model.freezePanes.freezeRows(1);
model.freezePanes.freezeColumns(3);

// Régions
regions.showGridLines = false;
const regionHeaders=["Région","Réf. CAQ%","Réf. PLQ%","Réf. QS%","Réf. PQ%","Réf. PCQ%","Réf. Autre%","Sond. CAQ","Sond. PLQ","Sond. QS","Sond. PQ","Sond. PCQ","Sond. Autre","Marge (pp)","Facteur inertie",null,null,null,null,"SwA CAQ","SwA PLQ","SwA QS","SwA PQ","SwA PCQ","SwA Autre","SwC CAQ","SwC PLQ","SwC QS","SwC PQ","SwC PCQ","SwC Autre","SwD CAQ","SwD PLQ","SwD QS","SwD PQ","SwD PCQ","SwD Autre"];
regions.getRange("A1:AK1").values=[regionHeaders];
header(regions.getRange("A1:AK1"));
regions.getRange("A2:A6").values=[["Montréal RMR"],["Île de Montréal"],["Banlieue de Montréal"],["Québec RMR"],["Reste du Québec"]];
const survey=[[23,26,12,27,10,2],[15,34,17,24,8,2],[32,18,7,30,12,1],[36,7,6,28,22,1],[28,16,8,29,17,1]];
regions.getRange("H2:M6").values=survey;
regions.getRange("N2:O2").values=[[3.3,0.5]];
for (let r=2;r<=6;r++) {
  for (let i=0;i<6;i++) {
    const voteCol=colLetter(4+i);
    const refFormula = r===2
      ? `=(SUMIFS('Modèle'!$${voteCol}$2:$${voteCol}$128,'Modèle'!$B$2:$B$128,$A$3)+SUMIFS('Modèle'!$${voteCol}$2:$${voteCol}$128,'Modèle'!$B$2:$B$128,$A$4))/(SUMIFS('Modèle'!$J$2:$J$128,'Modèle'!$B$2:$B$128,$A$3)+SUMIFS('Modèle'!$J$2:$J$128,'Modèle'!$B$2:$B$128,$A$4))*100`
      : `=SUMIFS('Modèle'!$${voteCol}$2:$${voteCol}$128,'Modèle'!$B$2:$B$128,$A${r})/SUMIFS('Modèle'!$J$2:$J$128,'Modèle'!$B$2:$B$128,$A${r})*100`;
    regions.getRange(`${colLetter(2+i)}${r}`).formulas=[[refFormula]];
    regions.getRange(`${colLetter(20+i)}${r}`).formulas=[[`=IFERROR(${colLetter(8+i)}${r}/${colLetter(2+i)}${r},1)`]];
    regions.getRange(`${colLetter(26+i)}${r}`).formulas=[[`=IFERROR((${colLetter(8+i)}${r}+$N$2)/${colLetter(2+i)}${r},1)`]];
    regions.getRange(`${colLetter(32+i)}${r}`).formulas=[[`=IFERROR(MAX(${colLetter(8+i)}${r}-$N$2,0)/${colLetter(2+i)}${r},1)`]];
  }
}
regions.getRange("H2:O2").format.font.color=inputBlue;
regions.getRange("H3:M6").format.font.color=inputBlue;
regions.getRange("H2:O6").format.fill=lightBlue;
regions.getRange("B2:G6").format.numberFormat="0.00";
regions.getRange("H2:N6").format.numberFormat="0.0";
regions.getRange("O2:AK6").format.numberFormat="0.000";
regions.getRange("A1:AK6").format.font.name="Arial";
regions.getRange("A1:AK6").format.font.size=9;
regions.getRange("A1:AK6").format.borders={preset:"inside",style:"thin",color:"#D9D9D9"};
regions.getRange("A:A").format.columnWidth=24;
regions.getRange("B:AK").format.columnWidth=11;
regions.freezePanes.freezeRows(1);
regions.freezePanes.freezeColumns(1);

// Carte 2026
map.showGridLines=false;
title(map.getRange("A1:J1"), "CARTE ÉLECTORALE 2026 – 127 CIRCONSCRIPTIONS");
map.getRange("A3:J3").values=[["Code DGEQ","Circonscription 2026","Région du modèle","Électeurs 2026","Couverture 2022","Source 2022 principale","Poids 2022","Couverture 2017","Source 2017 principale","Poids 2017"]];
header(map.getRange("A3:J3"));
map.getRange("A4:J130").values=data.districts.map(d=>[d.code,d.name,d.region,d.electors2026,d.coverage2022,d.sources2022[0]?.name??"",d.sources2022[0]?.weight??0,d.coverage2018,d.sources2018[0]?.name??"",d.sources2018[0]?.weight??0]);
map.getRange("D4:D130").format.numberFormat="#,##0";
map.getRange("E4:E130").format.numberFormat="0.00%";
map.getRange("G4:H130").format.numberFormat="0.00%";
map.getRange("J4:J130").format.numberFormat="0.00%";
map.getRange("A1:J130").format.font.name="Arial";
map.getRange("A1:J130").format.borders={preset:"inside",style:"thin",color:"#E7E6E6"};
map.getRange("A:A").format.columnWidth=12;
map.getRange("B:B").format.columnWidth=34;
map.getRange("C:C").format.columnWidth=23;
map.getRange("D:D").format.columnWidth=15;
map.getRange("E:E").format.columnWidth=16;
map.getRange("F:F").format.columnWidth=31;
map.getRange("G:H").format.columnWidth=14;
map.getRange("I:I").format.columnWidth=31;
map.getRange("J:J").format.columnWidth=14;
map.freezePanes.freezeRows(3);

// Correspondance détaillée
crosswalk.showGridLines=false;
title(crosswalk.getRange("A1:G1"), "MATRICE DE CORRESPONDANCE GÉOGRAPHIQUE");
crosswalk.getRange("A3:G3").values=[["Circonscription 2026","Région","Carte source","Code source","Circonscription source","Poids électoral","Rang"]];
header(crosswalk.getRange("A3:G3"));
const crossRows=[];
for (const d of data.districts) {
  for (const [year,sources] of [["2022",d.sources2022],["2017",d.sources2018]]) {
    let rank=0;
    for (const s of sources.filter(x=>x.weight>=0.0001)) {
      rank++;
      crossRows.push([d.name,d.region,year,s.code,s.name,s.weight,rank]);
    }
  }
}
crosswalk.getRange(`A4:G${crossRows.length+3}`).values=crossRows;
crosswalk.getRange(`F4:F${crossRows.length+3}`).format.numberFormat="0.00%";
crosswalk.getRange(`A1:G${crossRows.length+3}`).format.font.name="Arial";
crosswalk.getRange(`A1:G${crossRows.length+3}`).format.borders={preset:"inside",style:"thin",color:"#E7E6E6"};
crosswalk.getRange("A:A").format.columnWidth=34;
crosswalk.getRange("B:B").format.columnWidth=23;
crosswalk.getRange("C:D").format.columnWidth=13;
crosswalk.getRange("E:E").format.columnWidth=34;
crosswalk.getRange("F:G").format.columnWidth=14;
crosswalk.freezePanes.freezeRows(3);

// Méthodologie
method.showGridLines=false;
method.getRange("A1:B1").values=[["Paramètre","Description"]];
header(method.getRange("A1:B1"));
const methods=[
  ["Modèle QC127 v4.1","Projection électorale québécoise – 127 circonscriptions, quatre scénarios; seuil majoritaire de 64 sièges."],
  ["Sondage","Synopsis Recherche / La Presse, 24–26 août 2026, après répartition (n=867). Intrants régionaux repris du modèle QC125 fourni."],
  ["Carte 2026","127 circonscriptions conformes aux fichiers géographiques d’Élections Québec fournis, avec électeurs inscrits au 15 juillet 2026."],
  ["Référence 2022 transposée","Chaque section de vote 2026 est intersectée avec les circonscriptions de 2022. Ses électeurs sont répartis selon les superficies d’intersection; les profils partisans 2022 sont ensuite pondérés par ces électeurs."],
  ["Référence 2018 transposée","La même méthode est appliquée avec la carte de 2017 utilisée lors de l’élection de 2018. Les inerties locales 2018→2022 sont ainsi recalculées sur la géographie commune de 2026."],
  ["Régions","Île de Montréal (28), Banlieue de Montréal (40), Québec RMR (13), Reste du Québec (46). Montréal RMR demeure un agrégat de sondage seulement."],
  ["Scénario A","Swing proportionnel régional : votes projetés = votes de référence × (sondage régional / référence régionale)."],
  ["Scénario B","Scénario A + inertie locale 2018→2022 × facteur d’inertie. Les votes négatifs sont ramenés à zéro."],
  ["Scénarios C/D","Fourchette déterministe : sondage régional ± marge inscrite dans Régions!N2."],
  ["Intrants","Les cellules à police bleue sont modifiables : votes de référence synthétiques, sondages régionaux, marge, facteur d’inertie et résidus."],
  ["Limite principale","Les votes historiques sont disponibles par circonscription, non sous forme de polygones de bureaux historiques. La méthode suppose donc que le profil partisan d’une ancienne circonscription est homogène à l’intérieur de ses limites; elle est néanmoins pondérée par la distribution fine des électeurs 2026."],
  ["Autres limites","Modèle déterministe, sans régression vers la moyenne, effets de candidature, simulation probabiliste ni correction des corrélations régionales."],
  ["Sources locales","Résultats par bureau de vote 2018 et 2022; cartes des circonscriptions 2017 et 2022; carte des 127 circonscriptions et sections de vote 2026; modèle QC125 fourni."],
  ["Source Web","https://www.electionsquebec.qc.ca/"],
  ["Pour actualiser","1) Modifier Régions!H2:M6; 2) ajuster Régions!N2 et O2; 3) consulter Sièges; 4) revoir les estimations des nouvelles limites lorsqu’une table de correspondance officielle devient disponible."],
];
method.getRange(`A2:B${methods.length+1}`).values=methods;
method.getRange(`A2:A${methods.length+1}`).format={font:{bold:true},fill:gray,verticalAlignment:"top"};
method.getRange(`B2:B${methods.length+1}`).format.wrapText=true;
method.getRange(`A1:B${methods.length+1}`).format.font.name="Arial";
method.getRange(`A1:B${methods.length+1}`).format.borders={preset:"inside",style:"thin",color:"#D9D9D9"};
method.getRange("A:A").format.columnWidth=29;
method.getRange("B:B").format.columnWidth=112;
method.getRange(`2:${methods.length+1}`).format.rowHeight=48;
method.freezePanes.freezeRows(1);

// Compact formula and visual checks before export.
const keyCheck = await wb.inspect({ kind:"table", sheetId:"Sièges", range:"A4:H14", include:"values,formulas", tableMaxRows:14, tableMaxCols:8, maxChars:9000 });
console.log(keyCheck.ndjson);
const regionCheck = await wb.inspect({ kind:"table", sheetId:"Régions", range:"A1:O6", include:"values,formulas", tableMaxRows:8, tableMaxCols:15, maxChars:9000 });
console.log(regionCheck.ndjson);
const errors = await wb.inspect({ kind:"match", searchTerm:"#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A", options:{useRegex:true,maxResults:300}, summary:"final formula error scan" });
console.log(errors.ndjson);

for (const [sheetName, range] of [["Sièges","A1:H16"],["Modèle","A1:AX35"],["Régions","A1:AK6"],["Carte 2026","A1:J35"],["Correspondance","A1:G40"],["Méthodologie",`A1:B${methods.length+1}`]]) {
  const img = await wb.render({ sheetName, range, scale:1, format:"png" });
  const safe=sheetName.normalize("NFD").replace(/[\u0300-\u036f]/g,"").replace(/[^A-Za-z0-9_-]/g,"_");
  await fs.writeFile(`${outputDir}/${safe}.png`,new Uint8Array(await img.arrayBuffer()));
}

const out = await SpreadsheetFile.exportXlsx(wb);
await out.save(`${outputDir}/ModeleVivantQC127_v4_1_geospatial_synopsis_24aout.xlsx`);
console.log(JSON.stringify({output:`${outputDir}/ModeleVivantQC127_v4_1_geospatial_synopsis_24aout.xlsx`,districts:data.districts.length,regionCounts:data.regionCounts,crosswalkRows:crossRows.length}));
