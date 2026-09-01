from pathlib import Path
from collections import defaultdict
import csv, re, unicodedata, json

root = Path(__file__).resolve().parents[1]

def norm(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii","ignore").decode().upper()
    s = re.sub(r",\s*(V|P|CT|M|VL|CANTON|PAROISSE|VILLE)$", "", s)
    return re.sub(r"[^A-Z0-9]", "", s)

def party(h):
    u = h.upper()
    if "C.A.Q" in u: return "CAQ"
    if "P.L.Q" in u or "Q.L.P" in u: return "PLQ"
    if "Q.S" in u: return "QS"
    if "P.C.Q" in u: return "PCQ"
    if "P.Q" in u: return "PQ"
    return None

municipal = defaultdict(lambda: defaultdict(int))
district = defaultdict(lambda: defaultdict(int))
files = sorted((root/"2022/resultats-bureau-vote").glob("*.csv"))
for path in files:
    text = None
    for enc in ("utf-8-sig", "cp1252", "latin1"):
        try:
            text = path.read_text(encoding=enc)
            break
        except UnicodeDecodeError:
            pass
    rows = csv.DictReader(text.splitlines(), delimiter=";")
    pcols = {h:party(h) for h in rows.fieldnames if party(h)}
    for r in rows:
        mun = norm(r.get("Nom des Municipalités", ""))
        dist = r.get("Circonscription", "")
        for h,p in pcols.items():
            try: v=int(r[h] or 0)
            except ValueError: v=0
            municipal[mun][p] += v
            district[dist][p] += v

targets = ["Saint-Jérôme", "Saint-Colomban", "Mirabel", "Drummondville", "Saint-Germain-de-Grantham", "Wickham", "L'Avenir", "Saint-Guillaume"]
for t in targets:
    print(t, municipal.get(norm(t)))
print("FILES",len(files),"MUNICIPALITIES",len(municipal),"DISTRICTS",len(district))
(root/"pipeline/municipal_votes.json").write_text(json.dumps(municipal, ensure_ascii=False), encoding="utf-8")
