#!/usr/bin/env python3
"""Deterministic current-source manifest (not a certificate of correctness)."""
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parent
EXCLUDED_ROOT = {'SOURCE_MANIFEST.json', 'BUILD_REPORT.json', 'PRESERVATION_REPORT.json'}

def source_files(root=ROOT):
    for path in sorted(root.rglob('*')):
        rel = path.relative_to(root)
        if not path.is_file() or any(x in {'build', 'validation', '__pycache__', '.git'} for x in rel.parts):
            continue
        if len(rel.parts) == 1 and rel.name in EXCLUDED_ROOT:
            continue
        if path.suffix not in {'.tex', '.py', '.md', '.json'} and rel.name != '.gitignore':
            continue
        yield rel.as_posix(), path

def generate():
    return {'version': 16, 'submission_basis': 'e1d0ff2ef04a8641ac77923b664c4d3e8386f212',
            'controlling_review': 'd89bc35dc5d50240c8ae3c82aa251437dcc2165a',
            'scope': 'Current text, code and retained historical source records. Excludes this manifest, generated PDF, build and execution receipts.',
            'files': {name: hashlib.sha256(path.read_bytes()).hexdigest() for name,path in source_files()}}

def verify():
    stored = json.loads((ROOT / 'SOURCE_MANIFEST.json').read_text())
    current = generate()
    if stored != current:
        raise ValueError('Current source does not match SOURCE_MANIFEST.json')
    return len(current['files'])

if __name__ == '__main__':
    if '--write' in sys.argv:
        (ROOT / 'SOURCE_MANIFEST.json').write_text(json.dumps(generate(), indent=2)+'\n')
    print(json.dumps({'verified_source_files': verify()}))
