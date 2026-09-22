#!/usr/bin/env python3
"""Run inherited author suites, v20 exact diagnostics, and the complete build."""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time
from manifest import verify
from build import verify_history
ROOT=Path(__file__).resolve().parent
EXPECTED={10:7904,11:8207,12:26158,13:12944,14:7400,15:5868}

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def run(command,log):
    start=time.monotonic()
    with log.open('w') as out:
        result=subprocess.run(command,cwd=ROOT,stdout=out,stderr=subprocess.STDOUT,timeout=900)
    if result.returncode:
        raise RuntimeError(f'Execution failed ({result.returncode}): {command}; see {log}')
    return round(time.monotonic()-start,3)

def main():
    out=ROOT/'validation';out.mkdir(exist_ok=True)
    receipt=out/'EXECUTION_REPORT.json';receipt.unlink(missing_ok=True)
    report={'version':20,'python':platform.python_version(),
            'submission_basis':'01abeb689b203ea871b88495d16a826bb4942e16',
            'controlling_review':'59018a3231abb551d93947929f7e9bf0e3ddcd9e',
            'workflow_run_id':os.environ.get('GITHUB_RUN_ID'),
            'workflow_input_commit':os.environ.get('GITHUB_SHA'),
            'verified_source_files_before':verify(),
            'suites':[],
            'scope':'Actual finite author diagnostics and full source/build checks; not an independent referee report or a formal proof certificate.'}
    report['historical_source_checks']=verify_history()
    for version in (*range(10,16),17,18,19,20):
        script=f'tests/test_v{version}.py' if version<18 else f'tests/verify_v{version}.py'
        target=out/f'V{version}_AUTHOR_RERUN.json'
        elapsed=run([sys.executable,script,str(target)],out/f'v{version}-stdout.txt')
        data=json.loads(target.read_text())
        passed=data.get('passed') is True or data.get('status')=='passed'
        count=data.get('assertions',0)
        if not passed or count<=0 or (version in EXPECTED and count!=EXPECTED[version]):
            raise ValueError('Unexpected diagnostic receipt: '+str(version))
        report['suites'].append({'version':version,'passed':True,'assertions':count,
            'seconds':elapsed,'source_sha256':digest(ROOT/script),'receipt_sha256':digest(target)})
        (out/'EXECUTION_PROGRESS.json').write_text(json.dumps(report,indent=2)+'\n')
    report['assertions_total']=sum(x['assertions'] for x in report['suites'])
    # Actual corruption of the inherited inverse must fail even in standalone
    # preparation mode; current source manifests cannot stand in for this test.
    inverse=ROOT/'sections/operational_reconstruction.tex'
    original=inverse.read_bytes()
    try:
        changed=original.replace(b'\\begin{proof}',b'\\begin{proof}\nMUTATION TEST. ',1)
        if changed==original:
            raise RuntimeError('Mutation target proof missing')
        inverse.write_bytes(changed)
        bad=subprocess.run([sys.executable,'build.py','--prepare-only'],cwd=ROOT,
                           capture_output=True,text=True,timeout=180)
        (out/'standalone-mutation.txt').write_text(bad.stdout+bad.stderr)
        if bad.returncode==0 or 'Inherited source changed' not in bad.stderr:
            raise RuntimeError('Standalone preparation did not reject inherited inverse mutation')
        report['standalone_inverse_mutation_rejected']=True
    finally:
        inverse.write_bytes(original)
    report['restored_sources_after_mutation']=verify()
    report['build_seconds']=run([sys.executable,'build.py'],out/'build-stdout.txt')
    report['build']=json.loads((ROOT/'BUILD_REPORT.json').read_text())
    info=subprocess.run(['pdfinfo',str(ROOT/'main.pdf')],check=True,capture_output=True,text=True)
    report['pdf_pages']=int(next(line.split(':',1)[1] for line in info.stdout.splitlines() if line.startswith('Pages:')))
    report['pdf_sha256']=digest(ROOT/'main.pdf')
    report['verified_source_files_after']=verify()
    report['passed']=True
    receipt.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__':
    main()
