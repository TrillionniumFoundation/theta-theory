#!/usr/bin/env python3
"""Materialize checksum-bound native text from a pinned predecessor, then audit it."""
import base64, hashlib, json, lzma, shutil, subprocess, sys
from pathlib import Path, PurePosixPath
HERE=Path(__file__).resolve().parent
REPO=Path(subprocess.check_output(['git','rev-parse','--show-toplevel'],text=True).strip())
OLD=REPO/'papers/General-Theta-Foundations-I-restart/r3'
DEST=REPO/'papers/General-Theta-Foundations-I-restart/r4-causal-resolvent'
EXPECTED='203cd166f01778b3862339128f95617d22c09716dd12871cf7a2879b5984b561'
def require(ok,message):
    if not ok: raise RuntimeError(message)
require(subprocess.check_output(['git','rev-parse','HEAD:papers/General-Theta-Foundations-I-restart/r3'],text=True).strip()=='5d4e7327e3b616064df8062008808b3e97a7b303','Immutable r3 subtree mismatch')
require(not DEST.exists(),'Refusing to overwrite an existing revision')
chunks=sorted(HERE.glob('chunk-*.b64'))
require(len(chunks)==6,'Missing delivery chunks')
packed=base64.b64decode(''.join(p.read_text() for p in chunks),validate=True)
require(hashlib.sha256(packed).hexdigest()==EXPECTED,'Delivery checksum mismatch')
data=json.loads(lzma.decompress(packed))
for name in data['complete_paths']:
    p=PurePosixPath(name)
    require(not p.is_absolute() and '..' not in p.parts,'Unsafe source path')
    out=DEST/name;out.parent.mkdir(parents=True,exist_ok=True)
    old=(OLD/name).read_text() if (OLD/name).is_file() else ''
    change=data['changes'].get(name)
    if change:
        require(hashlib.sha256(old.encode()).hexdigest()==change['base_sha256'],'Predecessor file mismatch: '+name)
        lines=old.splitlines(keepends=True)
        text=''.join(''.join(lines[op[0]:op[1]]) if isinstance(op,list) else op for op in change['ops'])
    else:
        require((OLD/name).is_file(),'Missing inherited source: '+name)
        text=old
    out.write_text(text)
sys.path.insert(0,str(DEST));import verify
print(json.dumps({'status':'success','payload_sha256':EXPECTED,'source_audit':verify.source_audit()},indent=2,sort_keys=True))
