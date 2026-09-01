from pathlib import Path
from collections import defaultdict
import csv, json, re, struct, unicodedata

root = Path(__file__).resolve().parents[1]

def norm(s):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().upper()
    return re.sub(r"[^A-Z]", "", s).replace("SAINTE", "SAINT")

def read_dbf(path):
    raw = path.read_bytes()
    _, _, _, _, nrec, hlen, rlen = struct.unpack_from("<BBBBIHH20x", raw, 0)
    fields=[]; pos=32
    while raw[pos] != 0x0D:
        desc=raw[pos:pos+32]
        fields.append((desc[:11].split(b"\0",1)[0].decode("ascii"), desc[16]))
        pos += 32
    rows=[]; pos=hlen
    for _ in range(nrec):
        rec=raw[pos:pos+rlen]; pos += rlen
        if rec[:1] == b"*": continue
        off=1; row={}
        for name, flen in fields:
            cell=rec[off:off+flen].rstrip(b" \0"); off += flen
            try: val=cell.decode("utf-8")
            except UnicodeDecodeError: val=cell.decode("cp1252", "replace")
            row[name]=val.strip()
        rows.append(row)
    return rows

model=json.loads((root/"pipeline/model_qc125.json").read_text(encoding="utf-8"))
old_rows=model["rows"]
old_by_norm={norm(r[0]):r for r in old_rows}

rename = {
    "ARTHABASKALERABLE": ("Arthabaska-L'Érable", "ARTHABASKA"),
    "DANIELJOHNSON": ("Daniel-Johnson", "JOHNSON"),
    "PIERRELAPORTE": ("Pierre-Laporte", "LAPORTE"),
    "MATANEMATAPEDIAMITIS": ("Matane-Matapédia-Mitis", "MATANEMATAPEDIA"),
    "RIVIEREDULOUPTEMISCOUATALESBASQUES": ("Rivière-du-Loup–Témiscouata–Les Basques", "RIVIEREDULOUPTEMISCOUATA"),
    "VIMONTAUTEUIL": ("Vimont-Auteuil", "VIMONT"),
    "BELLEFEUILLE": ("Bellefeuille", None),
    "MARIELACOSTEGERINLAJOIE": ("Marie-Lacoste-Gérin-Lajoie", None),
}

circ_dbf=next((root/"pipeline/geo").rglob("Circonscription*.dbf"))
circs=read_dbf(circ_dbf)
sv_dbf=next((root/"pipeline/geo").rglob("sections_de_vote*.dbf"))
sections=read_dbf(sv_dbf)

electors_by_code=defaultdict(int)
municipal_electors=defaultdict(lambda: defaultdict(int))
for s in sections:
    code=int(s["CO_CEP"]); e=int(s["ELEC_2026"] or 0)
    electors_by_code[code]+=e
    municipal_electors[code][norm(s["NM_MUNCP"])]+=e

parties=["CAQ","PLQ","QS","PQ","PCQ","Autre"]
municipal_votes=defaultdict(lambda: defaultdict(int))
for path in sorted((root/"2022/resultats-bureau-vote").glob("*.csv")):
    text=None
    for enc in ("utf-8-sig","cp1252","latin1"):
        try: text=path.read_text(encoding=enc); break
        except UnicodeDecodeError: pass
    rows=csv.reader(text.splitlines(), delimiter=";")
    headers=next(rows)
    mun_i=headers.index("Nom des Municipalités")
    ei_i=next(i for i,h in enumerate(headers) if h in ("É.I.","�.I."))
    bv_i=headers.index("B.V.")
    pmap={}
    for i in range(ei_i+1,bv_i):
        u=headers[i].upper()
        if "C.A.Q" in u: p="CAQ"
        elif "P.L.Q" in u or "Q.L.P" in u: p="PLQ"
        elif "Q.S" in u: p="QS"
        elif "P.C.Q" in u: p="PCQ"
        elif "P.Q" in u: p="PQ"
        else: p="Autre"
        pmap[i]=p
    for row in rows:
        if not row: continue
        m=norm(re.sub(r",\s*[^,]+$", "", row[mun_i]))
        for i,p in pmap.items():
            try: municipal_votes[m][p]+=int(row[i] or 0)
            except (ValueError, IndexError): pass

def synthetic_new(code):
    weighted={p:0.0 for p in parties}; covered=0
    for mun,e in municipal_electors[code].items():
        votes=municipal_votes.get(mun)
        total=sum(votes.values()) if votes else 0
        if total:
            covered += e
            for p in parties: weighted[p] += e*votes[p]/total
    if covered == 0: raise RuntimeError(f"No municipal vote coverage for {code}")
    shares={p:weighted[p]/covered for p in parties}
    scale=round(electors_by_code[code]*0.66)
    counts={p:round(shares[p]*scale) for p in parties}
    diff=scale-sum(counts.values()); counts["Autre"]+=diff
    return counts, covered/electors_by_code[code]

out=[]
for c in circs:
    code=int(c["CO_CEP"]); key=c["NMTRI_CEP"].upper()
    if key in rename:
        official, source_key=rename[key]
    else:
        source_key=key
        if source_key not in old_by_norm:
            # DGEQ's sort key normalizes Saint/Sainte; compare after the same normalization.
            matches=[k for k in old_by_norm if norm(k)==norm(source_key)]
            if len(matches)!=1: raise RuntimeError(f"Unmapped district {key}")
            source_key=matches[0]
        official=old_by_norm[source_key][0]
    if source_key:
        src=old_by_norm[source_key]
        votes=dict(zip(parties, src[3:9]))
        residuals=dict(zip(["CAQ","PLQ","QS","PQ"], src[46:50]))
        region=src[1]
        method="Profil 2022 de la circonscription correspondante" if official==src[0] else f"Profil 2022 hérité de {src[0]}"
        coverage=1.0
    else:
        votes, coverage=synthetic_new(code)
        residuals={p:0 for p in ["CAQ","PLQ","QS","PQ"]}
        region="Banlieue de Montréal" if official=="Bellefeuille" else "Reste du Québec"
        method="Estimation municipale 2022 pondérée par les électeurs 2026; inertie locale fixée à 0"
    out.append({"code":code,"name":official,"region":region,"electors2026":electors_by_code[code],"votes":votes,"residuals":residuals,"method":method,"coverage":coverage})

out.sort(key=lambda x: norm(x["name"]))
assert len(out)==127
assert len({x["code"] for x in out})==127
counts=defaultdict(int)
for x in out: counts[x["region"]]+=1
payload={"districts":out,"regionCounts":dict(counts),"sourceWorkbook":"ModeleVivantQC125_v3_synopsis_24aout.xlsx"}
(root/"pipeline/qc127_data.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps({"districts":len(out),"regions":dict(counts),"new":[x for x in out if "Estimation municipale" in x["method"]]},ensure_ascii=False,indent=2))
