#!/usr/bin/env python3
"""Assemble v139 from the pinned native predecessor and a verified text overlay."""
from pathlib import Path
import gzip,json,hashlib,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
PIN='cf4925b91608b806580bc0cd4fd8ce2441870c08'
SRC=ROOT/'papers/A2-v17-boundary-information-coarsening/article/v138'
DST=SRC.parent/'v139'
EXPECTED='8e410c0d18678d341039e8f048bd6337b4e9eaa6b8ba870e5f66743c9974bd66'
PARTS=('0','1a','1b','1c','1d','2a','2b','2c','2d')
blob=b''.join((HERE/f'overlay.part{i}').read_bytes() for i in PARTS)
assert hashlib.sha256(blob).hexdigest()==EXPECTED, 'transport checksum mismatch'
subprocess.run(['git','merge-base','--is-ancestor',PIN,'HEAD'],cwd=ROOT,check=True)
subprocess.run(['git','diff','--exit-code',PIN,'--',str(SRC.relative_to(ROOT)),'reviews'],cwd=ROOT,check=True)
payload=json.loads(gzip.decompress(blob))
if DST.exists():shutil.rmtree(DST)
shutil.copytree(SRC,DST,ignore=shutil.ignore_patterns('*.pdf','*.aux','*.log','*.out','*.toc','__pycache__','evidence'))
(DST/'evidence').mkdir(exist_ok=True)
for name,text in payload['files'].items():
    p=Path(name)
    if p.is_absolute() or '..' in p.parts or not p.parts:raise RuntimeError(name)
    target=DST/p;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(text)
(HERE/'finalize.py').write_text(payload['finalize_source'])
subprocess.run([sys.executable,str(HERE/'finalize.py')],cwd=ROOT,check=True)
print('v139 native sources assembled')
