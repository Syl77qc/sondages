import fs from "node:fs/promises";
import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";

const inputPath = "../../ModeleVivantQC127_v6_pallas_29aout.xlsx";
const input = await FileBlob.load(inputPath);
const workbook = await SpreadsheetFile.importXlsx(input);

const sheets = await workbook.inspect({
  kind: "sheet",
  include: "id,name",
  maxChars: 12000,
});
console.log("SHEETS");
console.log(sheets.ndjson);

const model = workbook.worksheets.getItem("Modèle");
const used = model.getUsedRange();
console.log("USED_RANGE", used?.address ?? "unknown");

const data = await workbook.inspect({
  kind: "table",
  sheetId: "Modèle",
  range: "AN1:AS140",
  include: "values,formulas",
  tableMaxRows: 140,
  tableMaxCols: 6,
  tableMaxCellChars: 120,
  maxChars: 30000,
});
console.log("TARGET_DATA");
console.log(data.ndjson);

const styles = await workbook.inspect({
  kind: "computedStyle",
  sheetId: "Modèle",
  range: "AO1:AR12",
  maxChars: 12000,
});
console.log("TARGET_STYLES");
console.log(styles.ndjson);

await fs.mkdir("preview_before", { recursive: true });
const preview = await workbook.render({
  sheetName: "Modèle",
  range: "AN1:AS140",
  scale: 1,
  format: "png",
});
await fs.writeFile("preview_before/modele_target.png", new Uint8Array(await preview.arrayBuffer()));

