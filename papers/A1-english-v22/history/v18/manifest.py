#!/usr/bin/env python3
"""Deterministic v18 source manifest; not a certificate of correctness."""
from pathlib import Path
import hashlib
import json
import sys
ROOT=Path(__file__).resolve().parent
EXCLUDED={'SOURCE_MANIFEST.json','BUILD_REPORT.json','PRESERVATION_REPORT.json',
          'ARTIFACT_INSPECTION.json','EXECUTION_REPORT.json'}
def generate():
    files={}
    for path in sorted(ROOT.rglob('*')):
        rel=path.relative_to(ROOT)
        if not path.is_file() or any(x in {'build','validation','__pycache__','.git'} for x in rel.parts):
            continue
        if len(rel.parts)==1 and rel.name in EXCLUDED:
            continue
        if path.suffix not in {'.tex','.py','.md','.json'} and rel.name!='.gitignore':
            continue
        files[rel.as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
    return {'version':18,'submission_basis':'1f3838d89a5820b853d1e4b78194293b23e70bd2',
            'controlling_review':'a2adb648c08b3c9e803e916f533605203963ee35',
            'scope':'Current and archived source; excludes generated PDF, build files and current execution receipts.',
            'files':files}
def verify():
    stored=json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())
    current=generate()
    if stored!=current:
        raise ValueError('Source manifest mismatch')
    return len(current['files'])
if __name__=='__main__':
    if '--write' in sys.argv:
        (ROOT/'SOURCE_MANIFEST.json').write_text(json.dumps(generate(),indent=2)+'\n')
    print(json.dumps({'verified_source_files':verify()}))
