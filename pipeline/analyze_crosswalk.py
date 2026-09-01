from pathlib import Path
import json, struct, unicodedata, re

root = Path(__file__).resolve().parents[1]

def read_dbf(path):
    raw = path.read_bytes()
    _, _, _, _, nrec, hlen, rlen = struct.unpack_from("<BBBBIHH20x", raw, 0)
    fields=[]; pos=32
    while raw[pos] != 0x0D:
        desc=raw[pos:pos+32]
        fields.append((desc[:11].split(b"\0",1)[0].decode("ascii"), chr(desc[11]), desc[16], desc[17]))
        pos += 32
    rows=[]; pos=hlen
    for _ in range(nrec):
        rec=raw[pos:pos+rlen]; pos += rlen
        if rec[:1] == b"*": continue
        off=1; row={}
        for name, typ, flen, dec in fields:
            cell=rec[off:off+flen].rstrip(b" \0"); off += flen
            try: val=cell.decode("utf-8")
            except UnicodeDecodeError: val=cell.decode("cp1252", "replace")
            row[name]=val.strip()
        rows.append(row)
    return rows

def norm(s):
    s=unicodedata.normalize("NFKD", s).encode("ascii","ignore").decode().upper()
    return re.sub(r"[^A-Z]", "", s)

model=json.loads((root/"pipeline/model_qc125.json").read_text(encoding="utf-8"))
old=[r[0] for r in model["rows"]]
new_dbf=next((root/"pipeline/geo").rglob("Circonscription*.dbf"))
new_rows=read_dbf(new_dbf)
new=sorted([r["NM_CEP"] for r in new_rows], key=norm)
old_norm={norm(x):x for x in old}; new_norm={norm(x):x for x in new}
print("OLD",len(old),"NEW",len(new),"MATCH",len(set(old_norm)&set(new_norm)))
print("NEW_ONLY")
for k in sorted(set(new_norm)-set(old_norm)):
    print(new_norm[k])
print("OLD_ONLY")
for k in sorted(set(old_norm)-set(new_norm)):
    print(old_norm[k])

sv_dbf=next((root/"pipeline/geo").rglob("sections_de_vote*.dbf"))
sv=read_dbf(sv_dbf)
by_dist={}
for r in sv:
    by_dist.setdefault(r["NM_CEP"], {"electors":0,"municipalities":{}})
    e=int(r["ELEC_2026"] or 0)
    by_dist[r["NM_CEP"]]["electors"] += e
    by_dist[r["NM_CEP"]]["municipalities"][r["NM_MUNCP"]]=by_dist[r["NM_CEP"]]["municipalities"].get(r["NM_MUNCP"],0)+e
for name in [new_norm[k] for k in sorted(set(new_norm)-set(old_norm))]:
    d=by_dist[name]
    top=sorted(d["municipalities"].items(), key=lambda x:-x[1])[:12]
    print("DIST",name,d["electors"],top)
