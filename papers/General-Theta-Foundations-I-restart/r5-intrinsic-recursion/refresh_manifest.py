#!/usr/bin/env python3
"""Intentional authoring-time inventory refresh; not invoked by verification."""
from pathlib import Path
import hashlib, json
p=Path(__file__).resolve().parent
names=sorted(f for f in p.rglob('*') if f.is_file() and f.suffix in {'.tex','.py','.md'} and 'evidence' not in f.relative_to(p).parts)
files=[{'path':str(f.relative_to(p)),'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in names]
(p/'SOURCE_MANIFEST.json').write_text(json.dumps({'schema':1,'files':files},indent=2,sort_keys=True)+'\n')
