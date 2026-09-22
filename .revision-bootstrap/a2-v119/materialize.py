#!/usr/bin/env python3
from pathlib import Path
import base64, io, shutil, tarfile

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'papers/A2-v17-boundary-information-coarsening/article/v118'
DEST=ROOT/'papers/A2-v17-boundary-information-coarsening/article/v119'
BOOT=Path(__file__).resolve().parent

if not BASE.is_dir():
    raise SystemExit('missing reviewed v118 sibling')

if not DEST.exists():
    DEST.mkdir(parents=True)
    for p in BASE.rglob('*'):
        rel=p.relative_to(BASE)
        if not p.is_file():
            continue
        if rel.parts and rel.parts[0] in ('evidence','crossrefs','__pycache__'):
            continue
        if p.suffix in ('.pdf','.log','.aux','.fls','.fdb_latexmk'):
            continue
        q=DEST/rel
        q.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(p,q)

# A seeded Git tree may contain v118 build products.  They are never
# inherited as v119 evidence; the v119 build regenerates them.
for rel in (
    'evidence','crossrefs',
    'geometry.pdf','paper.pdf','applications.pdf',
    'geometry.log','paper.log','applications.log',
    'geometry.aux','paper.aux','applications.aux',
    'geometry.fls','paper.fls','applications.fls',
    'geometry.fdb_latexmk','paper.fdb_latexmk','applications.fdb_latexmk',
):
    q=DEST/rel
    if q.is_dir():
        shutil.rmtree(q)
    elif q.exists():
        q.unlink()

encoded=''.join(p.read_text().strip() for p in sorted(BOOT.glob('payload-*.b64')))
payload=base64.b64decode(encoded)
with tarfile.open(fileobj=io.BytesIO(payload),mode='r:gz') as tf:
    tf.extractall(ROOT)
print('materialized A2 v119 overlay on reviewed v118 baseline')
