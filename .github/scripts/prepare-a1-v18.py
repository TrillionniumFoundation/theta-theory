#!/usr/bin/env python3
"""Materialize the anchored, complete v18 revision from its checked source payload.

Only papers/A1-english-v18 is created. The preceding manuscript and reviews
are never changed. The final branch contains readable TeX, Python and Markdown;
this transport follows the preceding repository publication workflow.
"""
from __future__ import annotations
import base64
import hashlib
import json
import lzma
from pathlib import Path
import shutil
import subprocess

REPO=Path(__file__).resolve().parents[2]
SOURCE=REPO/'papers/A1-english-v17'
TARGET=REPO/'papers/A1-english-v18'
TREE='b583f5c8fca86b57451eaf1ca58dec912ff7c938'
PAYLOAD_SHA='619690510b2ad6b8b4accb0925f12320b7f3fa8bf3a29d8141f4c5eb4504260a'

def main():
    if TARGET.exists():
        raise RuntimeError('Refusing to overwrite an existing v18 directory')
    actual=subprocess.check_output(['git','rev-parse','HEAD:papers/A1-english-v17'],cwd=REPO,text=True).strip()
    if actual!=TREE:
        raise RuntimeError('Pinned v17 tree does not match')
    paths=sorted((REPO/'.github/scripts').glob('a1-v18-inputs-*.b64'))
    if len(paths)!=4:
        raise RuntimeError('Expected four checked payload fragments')
    data=base64.b64decode(''.join(p.read_text().strip() for p in paths),validate=True)
    if hashlib.sha256(data).hexdigest()!=PAYLOAD_SHA:
        raise RuntimeError('Payload checksum mismatch')
    files=json.loads(lzma.decompress(data))
    if len(files)!=16:
        raise RuntimeError('Unexpected source file count')
    for name,text in files.items():
        rel=Path(name)
        if rel.is_absolute() or '..' in rel.parts or not isinstance(text,str):
            raise RuntimeError('Unsafe source path or content')
    shutil.copytree(SOURCE,TARGET,ignore=shutil.ignore_patterns('build','__pycache__','*.aux','*.log','*.out'))
    history=TARGET/'history'
    archives={
        'main.tex':'V17_main.tex','main.pdf':'V17_main.pdf',
        'sections/introduction.tex':'V17_introduction.tex',
        'build.py':'build_v17.py','validate.py':'validate_v17.py',
        'manifest.py':'manifest_v17.py','SOURCE_MANIFEST.json':'V17_SOURCE_MANIFEST.json',
        'README.md':'V17_README.md','RESPONSE_TO_REFEREE.md':'V17_RESPONSE_TO_REFEREE.md',
        'PROOF_LEDGER.md':'V17_PROOF_LEDGER.md',
        'HISTORICAL_DERIVATION_MAP.md':'V17_HISTORICAL_DERIVATION_MAP.md',
        'NUMERICAL_EVIDENCE.md':'V17_NUMERICAL_EVIDENCE.md',
        'PRESERVATION_REPORT.json':'V17_PRESERVATION_REPORT.json',
        'BUILD_REPORT.json':'V17_BUILD_REPORT.json',
        'ARTIFACT_INSPECTION.json':'V17_ARTIFACT_INSPECTION.json',
        'MATERIALIZATION.json':'V17_MATERIALIZATION.json'}
    for old,new in archives.items():
        path=TARGET/old
        if path.exists():
            shutil.copy2(path,history/new)
    if (TARGET/'validation').exists():
        shutil.move(str(TARGET/'validation'),str(history/'v17_validation'))
    (TARGET/'validation').mkdir()
    # Never expose an old PDF or execution receipt as a new completed artifact.
    for name in ('main.pdf','SOURCE_MANIFEST.json','PRESERVATION_REPORT.json',
                 'BUILD_REPORT.json','ARTIFACT_INSPECTION.json','MATERIALIZATION.json'):
        (TARGET/name).unlink(missing_ok=True)
    for name,text in files.items():
        destination=TARGET/name
        destination.parent.mkdir(parents=True,exist_ok=True)
        destination.write_text(text,encoding='utf-8')
    print(json.dumps({'version':18,'source_tree':TREE,'new_files':len(files),
                      'payload_sha256':PAYLOAD_SHA,
                      'scope':'Source materialization only; validation and typesetting are separate steps.'},indent=2))
if __name__=='__main__':
    main()
