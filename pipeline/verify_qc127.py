from collections import Counter, defaultdict
from pathlib import Path
import json

root=Path(__file__).resolve().parents[1]
data=json.loads((root/"pipeline/qc127_geo_data.json").read_text(encoding="utf-8"))["districts"]
parties=["CAQ","PLQ","QS","PQ","PCQ","Autre"]
survey={
"Île de Montréal":[15,34,17,24,8,2],
"Banlieue de Montréal":[32,18,7,30,12,1],
"Québec RMR":[36,7,6,28,22,1],
"Reste du Québec":[28,16,8,29,17,1],
}
margin=3.3; inertia=0.5
region_votes=defaultdict(lambda:Counter())
for d in data:
    region_votes[d["region"]].update(d["votes"])
refs={r:[100*region_votes[r][p]/sum(region_votes[r].values()) for p in parties] for r in survey}

def winner(vals): return parties[max(range(6),key=lambda i:vals[i])]
base=Counter(); a=Counter(); b=Counter(); c=Counter(); lo=Counter()
for d in data:
    vals=[d["votes"][p] for p in parties]; base[winner(vals)]+=1
    sw=[survey[d["region"]][i]/refs[d["region"]][i] for i in range(6)]
    high=[(survey[d["region"]][i]+margin)/refs[d["region"]][i] for i in range(6)]
    low=[max(survey[d["region"]][i]-margin,0)/refs[d["region"]][i] for i in range(6)]
    va=[vals[i]*sw[i] for i in range(6)]; a[winner(va)]+=1
    vb=va[:]
    for i,p in enumerate(parties[:4]): vb[i]=max(0,vb[i]+d["residuals"][p]/100*sum(vals)*inertia)
    b[winner(vb)]+=1
    c[winner([vals[i]*high[i] for i in range(6)])]+=1
    lo[winner([vals[i]*low[i] for i in range(6)])]+=1
print(json.dumps({"base":base,"A":a,"B":b,"C":c,"D":lo},ensure_ascii=False))
assert all(sum(x[p] for p in parties)==127 for x in [base,a,b,c,lo])
