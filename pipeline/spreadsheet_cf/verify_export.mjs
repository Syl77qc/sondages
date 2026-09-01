import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";

const sourcePath = "../../ModeleVivantQC127_v6_pallas_29aout.xlsx";
const outputPath = "../../outputs/01a05aae-1162-7d43-aa88-bfed01398bca/ModeleVivantQC127_v6_mise_en_forme_partis.xlsx";

const source = await SpreadsheetFile.importXlsx(await FileBlob.load(sourcePath));
const output = await SpreadsheetFile.importXlsx(await FileBlob.load(outputPath));

for (const sheetName of ["Sièges", "Modèle", "Régions", "Méthodologie"]) {
  const sourceSheet = source.worksheets.getItem(sheetName);
  const outputSheet = output.worksheets.getItem(sheetName);
  const sourceRange = sourceSheet.getUsedRange();
  const outputRange = outputSheet.getUsedRange();
  const sameFormulas = JSON.stringify(sourceRange.formulas) === JSON.stringify(outputRange.formulas);
  const sameValues = JSON.stringify(sourceRange.values) === JSON.stringify(outputRange.values);
  console.log(sheetName, JSON.stringify({
    sourceRange: sourceRange.address,
    outputRange: outputRange.address,
    sameFormulas,
    sameValues,
  }));
  if (!sameFormulas) process.exitCode = 1;
}

const styleCheck = await output.inspect({
  kind: "computedStyle",
  sheetId: "Modèle",
  range: "AO2:AR2",
  maxChars: 5000,
});
console.log("EXPORTED_STYLE_CHECK");
console.log(styleCheck.ndjson);
