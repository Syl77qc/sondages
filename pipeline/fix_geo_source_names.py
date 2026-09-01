from pathlib import Path
import csv, io, json

root=Path(__file__).resolve().parents[1]

def names(path):
    raw=path.read_bytes()
    for enc in ("utf-8-sig","cp1252","latin1"):
        try: text=raw.decode(enc); break
        except UnicodeDecodeError: pass
    rows=csv.reader(io.StringIO(text),delimiter=";")
    next(rows)
    out={}
    for row in rows:
        try: out[int(row[0])]=row[1]
        except (ValueError,IndexError): pass
    return out

n18=names(root/"2018/circonscriptions.csv")
n22=names(root/"2022/circonscriptions.csv")
path=root/"pipeline/qc127_geo_data.json"
d=json.loads(path.read_text(encoding="utf-8"))
for district in d["districts"]:
    for x in district["sources2022"]: x["name"]=n22.get(x["code"],x["name"])
    for x in district["sources2018"]: x["name"]=n18.get(x["code"],x["name"])
path.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding="utf-8")
