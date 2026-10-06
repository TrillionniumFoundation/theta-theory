#!/usr/bin/env python3
"""Materialize the inspected v94 source bundle, then stage from pinned v93 bytes."""
from pathlib import Path
import base64
import gzip
import hashlib
import json
import runpy

HERE = Path(__file__).resolve().parent
DIGEST = '06933cc28a5f52b4ab9f8f6d1278db35a3f4cfe0dd22d0c2160a8e9c15f4bab9'
EXPECTED = {
    'stage-impl.py',
    'patch/sections/87-exact-initial-spectral-values.tex',
    'patch/spectral_value.py',
    'patch/spectral_value_check.py',
}
encoded = ''.join((HERE / f'payload-{i}.b64').read_text().strip() for i in range(4))
packed = base64.b64decode(encoded, validate=True)
if hashlib.sha256(packed).hexdigest() != DIGEST:
    raise RuntimeError('Revision bundle differs from the inspected source')
files = json.loads(gzip.decompress(packed))
if not isinstance(files, dict) or set(files) != EXPECTED:
    raise RuntimeError('Unexpected revision bundle inventory')
root = HERE / '_expanded'
if root.exists():
    raise RuntimeError('Refusing to overwrite an existing staging expansion')
for name, text in files.items():
    rel = Path(name)
    if rel.is_absolute() or '..' in rel.parts or not isinstance(text, str):
        raise RuntimeError('Unsafe revision bundle entry')
    target = root / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding='utf-8')
runpy.run_path(str(root / 'stage-impl.py'), run_name='__main__')
