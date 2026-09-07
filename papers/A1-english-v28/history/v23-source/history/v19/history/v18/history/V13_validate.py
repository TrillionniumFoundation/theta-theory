#!/usr/bin/env python3
"""Reproduce pinned-source, legacy, mutation, new diagnostics and TeX checks.

No network is used. The adjacent v11 source must be present for the historical
mutation reproduction; the repository contains it unchanged. Numerical tests
and source-preservation checks are not formal proof verification.
"""
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'validation'
OLD=ROOT.parent/'A1-english-v11'
V12=ROOT.parent/'A1-english-v12'
REFEREE=ROOT.parents[1]/'reviews/a1-english-v12-certified-memory-2026-09-06/reproduce_review.py'


def run(args):
    p=subprocess.run([str(a) for a in args],cwd=ROOT,capture_output=True,text=True)
    if p.returncode:
        sys.stderr.write(p.stdout+p.stderr)
        raise RuntimeError('validation failed: '+repr(args))
    return p.stdout


def main():
    OUT.mkdir(exist_ok=True)
    manifest=json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())
    for name,expected in manifest['sha256'].items():
        if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=expected:
            raise RuntimeError('source hash mismatch: '+name)
    commands=[
      [sys.executable,ROOT/'tests/test_v10.py',OUT/'V10_AUTHOR_RERUN.json'],
      [sys.executable,ROOT/'tests/test_v11.py',OUT/'V11_AUTHOR_RERUN.json'],
      [sys.executable,ROOT/'tests/reproduce_v11_transition.py',OLD,OUT/'V11_OLD_MUTATION_REPRODUCED.json'],
      [sys.executable,ROOT/'tests/test_v12.py',OUT/'V12_DIAGNOSTICS.json'],
      [sys.executable,ROOT/'tests/reject_v11_transition_on_v12.py',OUT/'V12_REJECTS_OLD_MUTATION.json'],
      [sys.executable,ROOT/'tests/reproduce_v12_contracts.py',V12,OUT/'V12_CONTRACT_FAULTS_REPRODUCED.json'],
      [sys.executable,ROOT/'tests/test_v13.py',OUT/'V13_DIAGNOSTICS.json'],
      [sys.executable,ROOT/'build.py']]
    if REFEREE.is_file():
        commands.insert(-1,[sys.executable,REFEREE,'--source-root',V12,
                            '--output',OUT/'V12_ORIGINAL_REFEREE_RERUN.json'])
    for i,args in enumerate(commands):
        (OUT/f'command-{i+1}.txt').write_text(run(args))
    info=run(['pdfinfo',ROOT/'main.pdf'])
    (OUT/'pdfinfo.txt').write_text(info)
    pages=int(re.search(r'^Pages:\s+(\d+)',info,re.M).group(1))
    diagnostics={n:json.loads((OUT/n).read_text()) for n in
                 ('V10_AUTHOR_RERUN.json','V11_AUTHOR_RERUN.json','V12_DIAGNOSTICS.json','V13_DIAGNOSTICS.json')}
    report={'status':'passed','source_commit':os.environ.get('GITHUB_SHA','local source manifest'),
        'controlling_review':'f2638b4910ee6245e9df4f641a2ed861bc4960b7',
        'python':platform.python_version(),'pdflatex':run(['pdflatex','--version']).splitlines()[0],
        'source_files_verified':len(manifest['sha256']),
        'diagnostic_counts':{k:v['assertions'] for k,v in diagnostics.items()},
        'historical_transition_mutation':json.loads((OUT/'V11_OLD_MUTATION_REPRODUCED.json').read_text()),
        'new_gate_rejects_historical_mutation':json.loads((OUT/'V12_REJECTS_OLD_MUTATION.json').read_text()),
        'preservation':json.loads((ROOT/'PRESERVATION_REPORT.json').read_text()),
        'v12_contract_faults_reproduced':json.loads((OUT/'V12_CONTRACT_FAULTS_REPRODUCED.json').read_text()),
        'original_v12_referee_script': ('executed unchanged' if REFEREE.is_file() else
             'not present in this source-only workspace; pinned author reproduction executed'),
        'pages':pages,'pdf_sha256':hashlib.sha256((ROOT/'main.pdf').read_bytes()).hexdigest(),
        'scope':'Executed finite diagnostics, source preservation and three-pass TeX build; not formal proof certification or editorial approval.',
        'not_run':'The separate legacy v10 referee/mutation suites are not claimed as rerun in this revision. Their historical files are retained.'}
    (OUT/'REVISION_VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='historical_transition_mutation'},indent=2))
if __name__=='__main__':main()
