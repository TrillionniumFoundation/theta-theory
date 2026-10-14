#!/usr/bin/env python3
"""Refresh the native source inventory BEFORE committing; builds never call this."""
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent
files=[]
for p in sorted(root.rglob('*')):
    rel=p.relative_to(root)
    if not p.is_file() or 'evidence' in rel.parts or '__pycache__' in rel.parts:
        continue
    if p.name in ('SOURCE_MANIFEST.json','paper.pdf'):
        continue
    data=p.read_bytes()
    files.append({'path':rel.as_posix(),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
(root/'SOURCE_MANIFEST.json').write_text(json.dumps({'schema':1,'files':files},indent=2,sort_keys=True)+'\n')
print(json.dumps({'source_files':len(files),'source_bytes':sum(x['bytes'] for x in files)},sort_keys=True))
