import fs from "node:fs/promises";
import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";

const inputPath = "../../ModeleVivantQC127_v6_pallas_29aout.xlsx";
const outputDir = "../../outputs/01a05aae-1162-7d43-aa88-bfed01398bca";
const outputPath = `${outputDir}/ModeleVivantQC127_v6_mise_en_forme_partis.xlsx`;

const input = await FileBlob.load(inputPath);
const workbook = await SpreadsheetFile.importXlsx(input);
const model = workbook.worksheets.getItem("Modèle");
const target = model.getRange("AO2:AR128");

const formulasBefore = JSON.stringify(target.formulas);

const rules = [
  { value: "PQ", fill: "#0070C0", font: "#FFFFFF" },
  { value: "CAQ", fill: "#00B0F0", font: "#000000" },
  { value: "PCQ", fill: "#17365D", font: "#FFFFFF" },
  { value: "PLQ", fill: "#FF0000", font: "#FFFFFF" },
  { value: "QS", fill: "#ED7D31", font: "#000000" },
];

for (const rule of rules) {
  target.conditionalFormats.addCustom(`=AO2="${rule.value}"`, {
    fill: rule.fill,
    font: { color: rule.font },
  });
}

if (JSON.stringify(target.formulas) !== formulasBefore) {
  throw new Error("Les formules de AO2:AR128 ont changé pendant l'ajout de la mise en forme.");
}

await fs.mkdir(`${outputDir}/verification`, { recursive: true });

const targetPreview = await workbook.render({
  sheetName: "Modèle",
  range: "AN1:AS128",
  scale: 1,
  format: "png",
});
await fs.writeFile(
  `${outputDir}/verification/modele_apres.png`,
  new Uint8Array(await targetPreview.arrayBuffer()),
);

for (const sheetName of ["Sièges", "Modèle", "Régions", "Méthodologie"]) {
  const preview = await workbook.render({
    sheetName,
    autoCrop: "all",
    scale: 0.75,
    format: "png",
  });
  const safeName = sheetName.normalize("NFD").replace(/[\u0300-\u036f]/g, "").replace(/[^A-Za-z0-9_-]/g, "_");
  await fs.writeFile(
    `${outputDir}/verification/${safeName}.png`,
    new Uint8Array(await preview.arrayBuffer()),
  );
}

const targetCheck = await workbook.inspect({
  kind: "table",
  sheetId: "Modèle",
  range: "AO1:AR8",
  include: "values,formulas",
  tableMaxRows: 8,
  tableMaxCols: 4,
  maxChars: 6000,
});
console.log("TARGET_CHECK");
console.log(targetCheck.ndjson);

const formulaErrors = await workbook.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#N/A",
  options: { useRegex: true, maxResults: 100 },
  summary: "final formula error scan excluding unsupported-name errors",
});
console.log("FORMULA_ERROR_SCAN");
console.log(formulaErrors.ndjson);

await fs.mkdir(outputDir, { recursive: true });
const output = await SpreadsheetFile.exportXlsx(workbook);
await output.save(outputPath);
console.log("OUTPUT", outputPath);

