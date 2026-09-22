#!/usr/bin/env python3
"""Rerun the pinned v116/v115 tests in a disposable copy, never the old tree."""
from pathlib import Path
import json, shutil, subprocess, sys, tempfile
HERE=Path(__file__).resolve().parent
with tempfile.TemporaryDirectory(prefix='a2-v117-inherited-') as tmp:
    dest=Path(tmp)/'v116'
    shutil.copytree(HERE.parent/'v116',dest,ignore=shutil.ignore_patterns('*.pdf','*.log','*.fls','*.aux','*.out','__pycache__'))
    for name in ['run_inherited.py','verify_revision.py']:
        subprocess.run([sys.executable,name],cwd=dest,check=True)
    result={}
    for name in ['DIAGNOSTICS.json','V115_RERUN_DIAGNOSTICS.json']:
        source=dest/'evidence'/name
        if source.exists():result[name]=json.loads(source.read_text())
    (HERE/'evidence/V116_RERUN_DIAGNOSTICS.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print('Pinned v116 and inherited v115 diagnostic reruns completed; not proof certification.')
