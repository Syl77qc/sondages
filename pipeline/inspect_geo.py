from pathlib import Path
import zipfile

root = Path(__file__).resolve().parents[1]
out = root / "pipeline" / "geo"
out.mkdir(parents=True, exist_ok=True)

for name in ["circonscriptions_electorales_2026_shapefile.zip", "sections_vote_2026_shapefile.zip"]:
    target = out / Path(name).stem
    target.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(root / "2026" / name) as zf:
        zf.extractall(target)

import struct

def read_dbf(path):
    raw = path.read_bytes()
    _, yy, mm, dd, nrec, hlen, rlen = struct.unpack_from("<BBBBIHH20x", raw, 0)
    fields = []
    pos = 32
    while raw[pos] != 0x0D:
        desc = raw[pos:pos+32]
        name = desc[:11].split(b"\0", 1)[0].decode("ascii", "replace")
        ftype = chr(desc[11])
        flen = desc[16]
        dec = desc[17]
        fields.append((name, ftype, flen, dec))
        pos += 32
    rows = []
    pos = hlen
    for _ in range(min(nrec, 12)):
        rec = raw[pos:pos+rlen]
        pos += rlen
        if rec[:1] == b"*":
            continue
        off = 1
        row = {}
        for name, ftype, flen, dec in fields:
            val = rec[off:off+flen].decode("utf-8", "replace").strip()
            row[name] = val
            off += flen
        rows.append(row)
    return nrec, fields, rows

for dbf in out.rglob("*.dbf"):
    nrec, fields, rows = read_dbf(dbf)
    print(f"FILE={dbf}")
    print(f"ROWS={nrec} FIELDS={fields}")
    for row in rows:
        print(row)
