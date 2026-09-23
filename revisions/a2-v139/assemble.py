#!/usr/bin/env python3
"""Assemble v139 from pinned Git objects; never depend on checkout filters."""
from pathlib import Path
import gzip,json,hashlib,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
PIN='cf4925b91608b806580bc0cd4fd8ce2441870c08'
SRC=ROOT/'papers/A2-v17-boundary-information-coarsening/article/v138'
DST=SRC.parent/'v139'
EXPECTED='8e410c0d18678d341039e8f048bd6337b4e9eaa6b8ba870e5f66743c9974bd66'
PARTS=(
 ('0','01606695cccb26a47364a44ae0a411a47fca599d'),
 ('1a','e843e77681d3c0fa38ef565edc5a80a072cee821'),
 ('1b','f0bc42fa08228bc052d5d32df12fe2c1c7467d20'),
 ('1c','02451c3b66f695badcb8d2beed85e9f078d55c68'),
 ('1d','d75631178dafc2380f38b3131fc43a54551bb42c'),
 ('2a','5beea3d4c761f1b6452462004a2611e9765caf03'),
 ('2b','349638a17a9f8b8ec78b6eb7928e5dbc3846ace7'),
 ('2c','cfc56e3ffaa5ce540df6423c010fb1854a3f280e'),
 ('2d','59deeb596b363c1dd88ed3313b8adc2fc501222e'),
)
chunks=[]
for name,expected_sha in PARTS:
    spec='HEAD:revisions/a2-v139/overlay.part'+name
    actual_sha=subprocess.check_output(['git','rev-parse',spec],cwd=ROOT,text=True).strip()
    if actual_sha!=expected_sha:
        raise RuntimeError(f'part {name}: expected Git blob {expected_sha}, found {actual_sha}')
    data=subprocess.check_output(['git','cat-file','blob',actual_sha],cwd=ROOT)
    object_sha=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    if object_sha!=expected_sha:
        raise RuntimeError(f'part {name}: invalid Git object bytes')
    print(f'part {name}: {len(data)} bytes, Git blob {object_sha}',flush=True)
    chunks.append(data)
blob=b''.join(chunks)
digest=hashlib.sha256(blob).hexdigest()
print(f'overlay: {len(blob)} bytes, SHA256 {digest}',flush=True)
if digest!=EXPECTED:
    raise RuntimeError(f'transport checksum mismatch: expected {EXPECTED}, found {digest}')
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
