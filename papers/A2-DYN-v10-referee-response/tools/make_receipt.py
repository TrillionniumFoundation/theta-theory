#!/usr/bin/env python3
"""Record the source actually consumed by TeX and the available checkout identity."""
from pathlib import Path
import hashlib
import json
import os
import subprocess

root=Path(__file__).resolve().parents[1]
audit=json.loads((root/'evidence/source-audit.json').read_text())
used=set()
for line in (root/'build/main.fls').read_text().splitlines():
    if line.startswith('INPUT '):
        path=Path(line[6:])
        if not path.is_absolute():
            path=root/path
        path=path.resolve()
        if path.is_relative_to(root) and path.suffix=='.tex':
            used.add(path.relative_to(root).as_posix())
if used != set(audit['active_inputs']):
    raise RuntimeError('TeX recorder differs from audited input graph')
sha=None
clean=None
try:
    top=subprocess.check_output(['git','rev-parse','--show-toplevel'],cwd=root,stderr=subprocess.DEVNULL,text=True).strip()
    rel=root.relative_to(Path(top)).as_posix()
    tracked=subprocess.check_output(['git','ls-files',rel+'/main.tex'],cwd=top,text=True).strip()
    if tracked:
        sha=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
        clean=not subprocess.check_output(['git','status','--porcelain','--',rel],cwd=top,text=True).strip()
except (subprocess.CalledProcessError,ValueError):
    pass
expected=os.environ.get('GITHUB_SHA')
if expected and (sha != expected or not clean):
    raise RuntimeError('CI source is not the exact clean event commit')
print(json.dumps({'source_build':'passed','source_audit':'passed',
    'checkout_commit':sha,'clean_paper_checkout':clean,'github_event_sha':expected,
    'exact_event_commit_qualified':bool(expected and sha==expected and clean),
    'pdf_sha256':hashlib.sha256((root/'build/main.pdf').read_bytes()).hexdigest(),
    'source_sha256':audit['sha256'],'actual_TeX_inputs':sorted(used),
    'full_raw_LLT_verified':False,'independent_human_review':False},indent=2))
