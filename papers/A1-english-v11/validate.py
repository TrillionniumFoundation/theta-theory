#!/usr/bin/env python3
"""Reproduce source, numerical and TeX checks without fetching network content."""
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
OUT = ROOT/'validation'
REVIEW = REPO/'reviews/a1-english-v10-effective-finite-memory-2026-09-06'
OLD = ROOT.parent/'A1-english-v10'


def run(args):
    result = subprocess.run([str(a) for a in args],cwd=ROOT,text=True,capture_output=True)
    if result.returncode:
        sys.stderr.write(result.stdout+result.stderr)
        raise RuntimeError('validation command failed: '+str(args))
    return result.stdout


def main():
    OUT.mkdir(exist_ok=True)
    manifest=json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())
    for name,expected in manifest['sha256'].items():
        actual=hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
        if actual!=expected:raise RuntimeError('source identity mismatch: '+name)
    commands=[
        [sys.executable,OLD/'tests/test_v10.py',OUT/'V10_AUTHOR_RERUN.json'],
        [sys.executable,REVIEW/'referee_checks.py',OUT/'V10_REFEREE_RERUN.json'],
        [sys.executable,REVIEW/'mutation_checks.py',OLD,OUT/'v10_mutation'],
        [sys.executable,ROOT/'tests/test_v11.py',OUT/'V11_DIAGNOSTICS.json'],
        [sys.executable,ROOT/'build.py'],
    ]
    for i,args in enumerate(commands):
        (OUT/f'command-{i+1}.txt').write_text(run(args))
    info=run(['pdfinfo',ROOT/'main.pdf'])
    match=re.search(r'^Pages:\s+(\d+)',info,re.M)
    if not match:raise RuntimeError('PDF page count unavailable')
    receipts={n:json.loads((OUT/n).read_text()) for n in
              ('V10_AUTHOR_RERUN.json','V10_REFEREE_RERUN.json','V11_DIAGNOSTICS.json')}
    report={'status':'passed','source_commit':os.environ.get('GITHUB_SHA','local source manifest'),
            'python':platform.python_version(),'pdflatex':run(['pdflatex','--version']).splitlines()[0],
            'source_files_verified':len(manifest['sha256']),
            'diagnostic_counts':{n:r['assertions'] for n,r in receipts.items()},
            'preservation':json.loads((ROOT/'PRESERVATION_REPORT.json').read_text()),
            'pages':int(match.group(1)),
            'pdf_sha256':hashlib.sha256((ROOT/'main.pdf').read_bytes()).hexdigest(),
            'old_mutation':json.loads((OUT/'v10_mutation/MUTATION_DIAGNOSTICS.json').read_text()),
            'scope':'Executed source/numerical/build checks, not formal proof checking or editorial approval.'}
    (OUT/'REVISION_VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
