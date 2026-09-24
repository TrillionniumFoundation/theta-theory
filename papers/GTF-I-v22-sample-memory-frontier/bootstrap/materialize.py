#!/usr/bin/env python3
"""Restore the reviewed v22 sources without modifying any predecessor path."""
from __future__ import annotations
import base64, hashlib, json, lzma, shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEST = HERE.parent
BASE = DEST.parent / 'GTF-I-v21-multicut-resources'
EXPECTED = '66f1042929525eff6554801712e06caf3d1b0bb623bc4b1890ae859c1265849c'

def main() -> None:
    parts = sorted(HERE.glob('payload.part*.b64'))
    if [p.name for p in parts] != [f'payload.part{i:02d}.b64' for i in range(7)]:
        raise RuntimeError('Missing or unexpected payload segment')
    compressed = base64.b64decode(''.join(p.read_text().strip() for p in parts), validate=True)
    if hashlib.sha256(compressed).hexdigest() != EXPECTED:
        raise RuntimeError('Source payload checksum mismatch')
    payload = json.loads(lzma.decompress(compressed))
    if not isinstance(payload, dict) or len(payload) != 22:
        raise RuntimeError('Unexpected source manifest')
    for name, text in payload.items():
        p = Path(name)
        if p.name != name or p.suffix not in {'.tex', '.md', '.json', '.py'} or not isinstance(text, str):
            raise RuntimeError('Invalid source path or type')
    for p in BASE.glob('*.tex'):
        shutil.copyfile(p, DEST / p.name)
    shutil.copyfile(BASE / 'HISTORICAL_PIPELINE_V20.json', DEST / 'HISTORICAL_PIPELINE_V20.json')
    shutil.copyfile(BASE / 'verify.py', DEST / 'verify_v21.py')
    shutil.copyfile(BASE / 'verify_v20.py', DEST / 'verify_v20.py')
    history = DEST / 'history'
    history.mkdir(exist_ok=True)
    for name in ['frontmatter', 'introduction', 'main', 'references-main']:
        shutil.copyfile(BASE / (name + '.tex'), history / (name + '-v21.tex'))
    for name, text in payload.items():
        (DEST / name).write_text(text, encoding='utf-8')
    print(f'Materialized {len(payload)} revised files; predecessor paths untouched.')

if __name__ == '__main__':
    main()
