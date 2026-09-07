#!/usr/bin/env python3
"""Deterministic v23 source manifest; not a certificate of correctness."""
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
    return {'version':23,'submission_basis':'5f745a863dac637496bd5eb20341f12cecb71ab1',
            'controlling_review':'325e89b9c012830cbd219fec0cff7c52b8e8d321',
            'scope':'Current and archived source; excludes generated PDF, build files and current execution receipts.',
            'files':files}
def expand_stored(stored):
    if stored.get('format')!='v23-delta':
        return stored
    data=(ROOT.parent/'A1-english-v22/SOURCE_MANIFEST.json').read_bytes()
    blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    if blob!=stored['base_git_blob'] or blob!='a2fea657ca31b1e824cff9393f02c4aa78c2ad54':
        raise ValueError('Compact manifest baseline mismatch')
    files=json.loads(data)['files']
    for name in stored['removed']:
        del files[name]
    files.update(stored['files'])
    return dict(stored['metadata'],files=files)
def compact(current):
    data=(ROOT.parent/'A1-english-v22/SOURCE_MANIFEST.json').read_bytes()
    blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    if blob!='a2fea657ca31b1e824cff9393f02c4aa78c2ad54':
        raise ValueError('Compact manifest baseline mismatch')
    old=json.loads(data)['files']
    return {'format':'v23-delta','base_git_blob':blob,
        'metadata':{k:v for k,v in current.items() if k!='files'},
        'files':{p:h for p,h in current['files'].items() if old.get(p)!=h},
        'removed':sorted(set(old)-set(current['files']))}
def verify():
    stored=expand_stored(json.loads((ROOT/'SOURCE_MANIFEST.json').read_text()))
    current=generate()
    if stored!=current:
        raise ValueError('Source manifest mismatch')
    return len(current['files'])
if __name__=='__main__':
    if '--write' in sys.argv:
        data=generate()
        if '--compact' in sys.argv: data=compact(data)
        (ROOT/'SOURCE_MANIFEST.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({'verified_source_files':verify()}))
