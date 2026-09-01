import fs from "node:fs/promises";
import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";

const workbook = await SpreadsheetFile.importXlsx(await FileBlob.load(process.argv[2]));
const sheet = workbook.worksheets.getItem("Modèle");
const payload = {
  headers: sheet.getRange("A1:AX1").values[0],
  rows: sheet.getRange("A2:AX126").values,
  formulasFirst: sheet.getRange("J2:AX2").formulas[0],
};
await fs.writeFile("pipeline/model_qc125.json", JSON.stringify(payload, null, 2), "utf8");
