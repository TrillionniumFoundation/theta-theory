#!/usr/bin/env python3
"""Materialize exactly the locally checked A2 v63 revision; delete no source.

The patch is accepted only against every byte of the frozen reviewed v62
archive. Native Git-tree equality is checked by the publication workflow.
"""
from pathlib import Path
import base64,hashlib,json,lzma,zipfile
ROOT=Path(__file__).resolve().parents[2]
P=ROOT/'papers/A2-v17-boundary-information-coarsening'
BASE='037c80dc44d8191e6f808591ea0651e813234d06'
ARCHIVE_SHA='3d320058366746fb3b4d9d8dc5e71f01a710737ea8c3e686bfe6687ddcea138f'
PAYLOAD_SHA='124032d9ecde7b937c6177aeb6ae6a7185c83651ff24018b5868517b1c039970'
def require(ok,message):
    if not ok:raise RuntimeError(message)
def sha(b):return hashlib.sha256(b).hexdigest()
def safe(name):
    p=Path(name)
    require(not p.is_absolute() and '..' not in p.parts and '\\' not in name,'Unsafe path')
    return p
archive=ROOT/'deliveries/a2-v62'/BASE/'native-source.zip'
require(sha(archive.read_bytes())==ARCHIVE_SHA,'Reviewed source archive mismatch')
with zipfile.ZipFile(archive) as z:
    manifest=json.loads(z.read('SOURCE_MANIFEST.json'))
    require(manifest['source_commit']==BASE and len(manifest['files'])==767,'Wrong baseline')
    for name,m in manifest['files'].items():
        b=(P/safe(name)).read_bytes()
        require(sha(b)==m['sha256'] and len(b)==m['bytes'],'Baseline changed: '+name)
        require(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==m['git_blob'],'Git blob mismatch')
        require(bool((P/name).stat().st_mode&0o111)==(m['mode']=='100755'),'Mode mismatch')
parts=sorted(Path(__file__).parent.glob('a2-v63-payload-*.b64'))
require(len(parts)==3,'Missing payload piece')
raw=lzma.decompress(base64.b64decode(''.join(p.read_text().strip() for p in parts),validate=True))
require(sha(raw)==PAYLOAD_SHA,'Revision payload digest mismatch')
data=json.loads(raw)
require(len(data['patches'])==8 and len(data['new_files'])==8,'Unexpected patch inventory')
A=P/'history/v62-review-baseline'
require(not A.exists(),'Revision already materialized or archive path occupied')
for name,spec in data['patches'].items():
    path=P/safe(name);b=path.read_bytes()
    require(sha(b)==spec['before'],'Patch preimage mismatch: '+name)
    old=b.decode();new=old
    last=len(old)+1
    for e in reversed(spec['edits']):
        require(0<=e['start']<=e['end']<last,'Overlapping or invalid patch')
        new=new[:e['start']]+e['text']+new[e['end']:];last=e['start']+1
    require(sha(new.encode())==spec['after'],'Patch postimage mismatch: '+name)
    backup=A/safe(name);backup.parent.mkdir(parents=True,exist_ok=True);backup.write_bytes(b)
    path.write_text(new)
for name,text in data['new_files'].items():
    path=P/safe(name);require(not path.exists(),'New path already exists: '+name)
    path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text)
(A/'SOURCE_MANIFEST.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
oldreadme=ROOT/'README.md';saved=ROOT/'README_PRE_V63.md'
require(not saved.exists(),'Root README archive exists');saved.write_bytes(oldreadme.read_bytes())
(ROOT/'README.md').write_text("""# Theta-Theory — A2 revision 63\n\n**Boundary laws and rigidity of periodic dispersing billiards** — Qian Qi, September 16, 2026.\n\nThis source revision responds to the frozen v62 referee report. The complete principal article, full technical manuscript and two-collision companion are retained. The all-history pilot-grid time bound is corrected without changing the five finite-experiment statements or their confidence rates. A hypothesis-accurate comparison with Zelditch's published orbit-local inverse spectral theorem is integrated in both introductions.\n\n[Revision index](A2_REVISION_V63_INDEX.md) · [Point-by-point response](papers/A2-v17-boundary-information-coarsening/RESPONSE_TO_REFEREE_V63.md) · [Principal source](papers/A2-v17-boundary-information-coarsening/rigidity.tex) · [Complete source](papers/A2-v17-boundary-information-coarsening/main.tex).\n\nThe complete native PDFs and exact-source evidence are published by the v63 native workflow on a separate revision branch after successful compilation. This source-stage index does not assert a pending workflow has completed. The subsequent review-ready guide identifies the actual published source and products. Previous reviews, delivery branches, A1 and the default branch are unchanged.\n""")
(ROOT/'A2_REVISION_V63_INDEX.md').write_text("""# A2 revision 63 — source index\n\nBaseline review: `a568573d1d4a5d976f6db3c54122d97c769acd38`. Reviewed mathematical source: `037c80dc44d8191e6f808591ea0651e813234d06`.\n\nThe complete manuscript lives in `papers/A2-v17-boundary-information-coarsening/`. Entry points are `rigidity.tex`, `main.tex` and `two_collision.tex`. Source branch: `revision/a2-v63-referee-response-2026-09-16`.\n\nThe point-by-point response, cover letter, historical audit, literature check and dependency ledger carry the V63 suffix. Exact originals of the eight modified inherited paths and the full frozen baseline manifest are in `history/v62-review-baseline/`. The checker retains 767 baseline paths and all 126 inherited active inputs; a shared comparison adds one active input. Five finite-experiment statement bodies are unchanged.\n\nRun `python3 -B papers/A2-v17-boundary-information-coarsening/tools/check_revision_v63.py`, also under `python3 -O`, to reproduce source and exact arithmetic checks. The native build uses the retained immutable-source builder with shell escape disabled. A successful build is not proof certification or an editorial acceptance judgment. Final delivery identities are recorded after publication, not anticipated here.\n""")
print(json.dumps({'status':'materialized','baseline':BASE,'payload_sha256':PAYLOAD_SHA,
 'modified_inherited_paths':sorted(data['patches']),'new_manuscript_paths':sorted(data['new_files']),
 'archived_originals':8,'deleted_paths':[]},indent=2,sort_keys=True))
