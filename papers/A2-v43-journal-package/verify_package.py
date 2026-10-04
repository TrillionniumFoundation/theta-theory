#!/usr/bin/env python3
"""Verify the extracted journal package against its exact-source manifest."""
import hashlib,json,sys
from pathlib import Path
root=Path(__file__).resolve().parent
try:
    manifest=json.loads((root/'JOURNAL_PACKAGE.json').read_text())
    for name,sha in manifest['files'].items():
        path=Path(name)
        if path.is_absolute() or '..' in path.parts:raise ValueError('unsafe member')
        target=root/path
        if target.is_symlink() or hashlib.sha256(target.read_bytes()).hexdigest()!=sha:raise ValueError('changed or missing member: '+name)
    for name in manifest['pdf_pair']:
        if name not in manifest['files']:raise ValueError('incomplete PDF pair')
    print(json.dumps({'status':'passed','source_commit':manifest['source_commit'],'files':len(manifest['files']),'scope':'Package content integrity, not proof certification.'},sort_keys=True))
except Exception as exc:
    print(str(exc),file=sys.stderr);sys.exit(1)
