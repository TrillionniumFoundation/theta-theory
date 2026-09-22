#!/usr/bin/env python3
from pathlib import Path
import base64, io, shutil, tarfile
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'papers/A2-v17-boundary-information-coarsening/article/v118'
DEST=ROOT/'papers/A2-v17-boundary-information-coarsening/article/v119'
BOOT=Path(__file__).resolve().parent
if not BASE.is_dir(): raise SystemExit('missing reviewed v118 sibling')
if DEST.exists(): raise SystemExit('v119 already exists; refusing to overwrite')
DEST.mkdir(parents=True)
for p in BASE.rglob('*'):
    rel=p.relative_to(BASE)
    if not p.is_file(): continue
    if rel.parts and rel.parts[0] in ('evidence','crossrefs','__pycache__'): continue
    if p.suffix in ('.pdf','.log','.aux','.fls','.fdb_latexmk'): continue
    q=DEST/rel; q.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(p,q)
encoded=''.join(p.read_text().strip() for p in sorted(BOOT.glob('payload-*.b64')))
payload=base64.b64decode(encoded)
with tarfile.open(fileobj=io.BytesIO(payload),mode='r:gz') as tf:
    tf.extractall(ROOT)
print('materialized A2 v119 from reviewed v118 baseline')
