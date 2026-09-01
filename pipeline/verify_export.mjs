import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";
const path=process.argv[2];
const wb=await SpreadsheetFile.importXlsx(await FileBlob.load(path));
console.log((await wb.inspect({kind:"table",sheetId:"Sièges",range:"A4:H14",include:"values,formulas",tableMaxRows:14,tableMaxCols:8,maxChars:8000})).ndjson);
console.log((await wb.inspect({kind:"match",searchTerm:"#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",options:{useRegex:true,maxResults:300},summary:"reopened export formula scan"})).ndjson);
