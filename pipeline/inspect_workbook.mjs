import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";
import fs from "node:fs/promises";

const inputPath = process.argv[2];
const input = await FileBlob.load(inputPath);
const workbook = await SpreadsheetFile.importXlsx(input);

const overview = await workbook.inspect({
  kind: "workbook,sheet,definedName,drawing,table",
  maxChars: 14000,
  tableMaxRows: 8,
  tableMaxCols: 14,
  tableMaxCellChars: 100,
});
console.log(overview.ndjson);

for (const sheet of workbook.worksheets.items) {
  const used = sheet.getUsedRange();
  console.log(JSON.stringify({
    type: "sheet_used_range",
    name: sheet.name,
    address: used?.address ?? null,
    rowCount: used?.rowCount ?? null,
    columnCount: used?.columnCount ?? null,
  }));
  if (used) {
    const preview = await workbook.inspect({
      kind: "table",
      sheetId: sheet.name,
      range: used.address,
      maxChars: 10000,
      tableMaxRows: 16,
      tableMaxCols: 24,
      tableMaxCellChars: 100,
    });
    console.log(preview.ndjson);
    const formulas = await workbook.inspect({
      kind: "formula",
      sheetId: sheet.name,
      range: used.address,
      maxChars: 16000,
      options: { maxResults: 180 },
    });
    console.log(formulas.ndjson);
    const rendered = await workbook.render({ sheetName: sheet.name, autoCrop: "all", scale: 1, format: "png" });
    const safe = sheet.name.normalize("NFD").replace(/[\u0300-\u036f]/g, "").replace(/[^A-Za-z0-9_-]/g, "_");
    await fs.mkdir("pipeline/previews", { recursive: true });
    await fs.writeFile(`pipeline/previews/${safe}.png`, new Uint8Array(await rendered.arrayBuffer()));
  }
}
