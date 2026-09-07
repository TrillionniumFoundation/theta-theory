#!/usr/bin/env python3
"""Deterministic v21 source manifest; not a certificate of correctness."""
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
    return {'version':21,'submission_basis':'6f103ad252d7c65f140720f4095585026f7bb1b9',
            'controlling_review':'078f34222b00797203cdf6dd421eab9f9f428c59',
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
