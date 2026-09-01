from pathlib import Path
from collections import defaultdict
import csv, io, json, re, sys, unicodedata, zipfile

root=Path(__file__).resolve().parents[1]
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0,str(root/"pipeline/geo_vendor"))
import shapefile
from shapely.geometry import shape
from shapely import make_valid
from shapely.strtree import STRtree

parties=["CAQ","PLQ","QS","PQ","PCQ","Autre"]

def norm(s):
    s=unicodedata.normalize("NFKD",str(s)).encode("ascii","ignore").decode().upper()
    return re.sub(r"[^A-Z]","",s).replace("SAINTE","SAINT")

def clean_geom(g):
    if not g.is_valid: g=make_valid(g)
    return g

def load_districts(path):
    r=shapefile.Reader(str(path),encoding="utf-8",encodingErrors="replace")
    out=[]
    for sr in r.iterShapeRecords():
        rec=sr.record.as_dict()
        out.append({"code":int(rec["CO_CEP"]),"name":rec["NM_CEP"],"geom":clean_geom(shape(sr.shape.__geo_interface__))})
    return out

def party_for_header(h):
    u=h.upper()
    if "C.A.Q" in u: return "CAQ"
    if "P.L.Q" in u or "Q.L.P" in u: return "PLQ"
    if "Q.S" in u: return "QS"
    if "P.C.Q" in u: return "PCQ"
    if "P.Q" in u: return "PQ"
    return "Autre"

def read_election_zip(path):
    totals=defaultdict(lambda:defaultdict(int))
    with zipfile.ZipFile(path) as z:
        for name in z.namelist():
            if not name.lower().endswith(".csv"): continue
            raw=z.read(name)
            text=None
            for enc in ("utf-8-sig","cp1252","latin1"):
                try: text=raw.decode(enc); break
                except UnicodeDecodeError: pass
            rows=csv.reader(io.StringIO(text),delimiter=";")
            headers=next(rows)
            code_i=0
            ei_i=next(i for i,h in enumerate(headers) if h in ("É.I.","�.I."))
            bv_i=headers.index("B.V.")
            pmap={i:party_for_header(headers[i]) for i in range(ei_i+1,bv_i)}
            for row in rows:
                if not row: continue
                try: code=int(row[code_i])
                except (ValueError,IndexError): continue
                for i,p in pmap.items():
                    try: totals[code][p]+=int(row[i] or 0)
                    except (ValueError,IndexError): pass
    return totals

def read_electors(path):
    text=None
    raw=path.read_bytes()
    for enc in ("utf-8-sig","cp1252","latin1"):
        try: text=raw.decode(enc); break
        except UnicodeDecodeError: pass
    rows=csv.reader(io.StringIO(text),delimiter=";")
    headers=next(rows)
    out={}
    for row in rows:
        try: out[int(row[0])]=int(row[9])
        except (ValueError,IndexError): pass
    return out

def make_crosswalk(old_districts, section_reader, label):
    geoms=[d["geom"] for d in old_districts]
    codes=[d["code"] for d in old_districts]
    tree=STRtree(geoms)
    weights=defaultdict(lambda:defaultdict(float))
    assigned=defaultdict(float); total=defaultdict(float)
    for n,sr in enumerate(section_reader.iterShapeRecords(),1):
        rec=sr.record.as_dict(); e=float(rec["ELEC_2026"] or 0); new=int(rec["CO_CEP"])
        total[new]+=e
        if e<=0: continue
        g=clean_geom(shape(sr.shape.__geo_interface__))
        idxs=tree.query(g,predicate="intersects")
        pieces=[]; area_sum=0.0
        for idx in idxs:
            inter=g.intersection(geoms[int(idx)])
            a=inter.area
            if a>0: pieces.append((int(idx),a)); area_sum+=a
        if area_sum<=0:
            idx=int(tree.nearest(g)); pieces=[(idx,1.0)]; area_sum=1.0
        for idx,a in pieces:
            w=e*a/area_sum
            weights[new][codes[idx]]+=w; assigned[new]+=w
        if n%2000==0: print(f"{label}: {n}/16951",flush=True)
    return weights,assigned,total

old17_path=next((root/"2018/circonscriptions_electorales_2017_shapefile").glob("*.shp"))
old22_path=next((root/"2022/circonscriptions_electorales_2022_shapefile").glob("*.shp"))
sv_path=next((root/"pipeline/geo").rglob("sections_de_vote*.shp"))
old17=load_districts(old17_path); old22=load_districts(old22_path)
print("Loaded district maps",flush=True)
sv1=shapefile.Reader(str(sv_path),encoding="utf-8",encodingErrors="replace")
cw22,a22,t22=make_crosswalk(old22,sv1,"2022-2026")
sv2=shapefile.Reader(str(sv_path),encoding="utf-8",encodingErrors="replace")
cw18,a18,t18=make_crosswalk(old17,sv2,"2017-2026")
print("Crosswalks complete",flush=True)

votes22=read_election_zip(root/"2022/resultats-bureau-vote.zip")
votes18=read_election_zip(root/"2018/resultats-bureau-vote.zip")
elect22=read_electors(root/"2022/circonscriptions.csv")
elect18=read_electors(root/"2018/circonscriptions.csv")
proto=json.loads((root/"pipeline/qc127_data.json").read_text(encoding="utf-8"))
meta={int(d["code"]):d for d in proto["districts"]}

def transpose(cw,votes,elect,new_code):
    total_w=sum(cw[new_code].values())
    shares={p:0.0 for p in parties}; valid_rate=0.0
    for old_code,w in cw[new_code].items():
        vt=votes.get(old_code,{})
        tot=sum(vt.values())
        if tot<=0: continue
        frac=w/total_w
        for p in parties: shares[p]+=frac*vt.get(p,0)/tot
        valid_rate+=frac*tot/max(elect.get(old_code,tot),1)
    s=sum(shares.values())
    shares={p:(shares[p]/s if s else 0) for p in parties}
    synthetic_total=round(meta[new_code]["electors2026"]*valid_rate)
    counts={p:round(shares[p]*synthetic_total) for p in parties}
    counts["Autre"]+=synthetic_total-sum(counts.values())
    return counts,shares,valid_rate

districts=[]
for code in sorted(meta,key=lambda c:norm(meta[c]["name"])):
    c22,s22,tr22=transpose(cw22,votes22,elect22,code)
    c18,s18,tr18=transpose(cw18,votes18,elect18,code)
    top22=sorted(cw22[code].items(),key=lambda x:-x[1])
    top18=sorted(cw18[code].items(),key=lambda x:-x[1])
    districts.append({**meta[code],"votes":c22,"shares2018":s18,"counts2018":c18,"turnoutValid2022":tr22,"turnoutValid2018":tr18,
      "coverage2022":a22[code]/t22[code] if t22[code] else 0,"coverage2018":a18[code]/t18[code] if t18[code] else 0,
      "sources2022":[{"code":k,"weight":v/sum(cw22[code].values())} for k,v in top22],
      "sources2018":[{"code":k,"weight":v/sum(cw18[code].values())} for k,v in top18]})

# Recalculate local inertia residuals on the common 2026 geography.
region_counts22=defaultdict(lambda:defaultdict(int)); region_counts18=defaultdict(lambda:defaultdict(int))
for d in districts:
    for p in parties:
        region_counts22[d["region"]][p]+=d["votes"][p]
        region_counts18[d["region"]][p]+=d["counts2018"][p]
for d in districts:
    reg=d["region"]
    reg22={p:region_counts22[reg][p]/sum(region_counts22[reg].values()) for p in parties}
    reg18={p:region_counts18[reg][p]/sum(region_counts18[reg].values()) for p in parties}
    d["residuals"]={p:((d["votes"][p]/sum(d["votes"].values())-d["shares2018"][p])-(reg22[p]-reg18[p]))*100 for p in parties[:4]}
    d["method"]="Transposition géospatiale pondérée par les électeurs 2026"

names22={d["code"]:d["name"] for d in old22}; names18={d["code"]:d["name"] for d in old17}
for d in districts:
    for x in d["sources2022"]: x["name"]=names22.get(x["code"],str(x["code"]))
    for x in d["sources2018"]: x["name"]=names18.get(x["code"],str(x["code"]))

payload={"districts":districts,"regionCounts":proto["regionCounts"],"method":"Sections de vote 2026 pondérées par électeurs; intersections avec cartes 2017 et 2022"}
(root/"pipeline/qc127_geo_data.json").write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding="utf-8")
summary={"districts":len(districts),"minCoverage2022":min(d["coverage2022"] for d in districts),"minCoverage2018":min(d["coverage2018"] for d in districts),
"maxSources2022":max(len(d["sources2022"]) for d in districts),"maxSources2018":max(len(d["sources2018"]) for d in districts)}
print(json.dumps(summary,ensure_ascii=False),flush=True)
