from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent / "geo_vendor"))
import shapefile

root=Path(__file__).resolve().parents[1]
paths=[
 next((root/"2018/circonscriptions_electorales_2017_shapefile").glob("*.shp")),
 next((root/"2022/circonscriptions_electorales_2022_shapefile").glob("*.shp")),
 next((root/"pipeline/geo").rglob("Circonscription*.shp")),
 next((root/"pipeline/geo").rglob("sections_de_vote*.shp")),
]
for p in paths:
    r=shapefile.Reader(str(p), encoding="utf-8", encodingErrors="replace")
    print(p)
    print([f[0] for f in r.fields[1:]], len(r))
    print(r.record(0).as_dict())
