#!/usr/bin/env python3
"""Run inherited author suites, v23 exact diagnostics, and the complete build."""
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
    report={'version':23,'python':platform.python_version(),
            'submission_basis':'5f745a863dac637496bd5eb20341f12cecb71ab1',
            'controlling_review':'325e89b9c012830cbd219fec0cff7c52b8e8d321',
            'workflow_run_id':os.environ.get('GITHUB_RUN_ID'),
            'workflow_input_commit':os.environ.get('GITHUB_SHA'),
            'verified_source_files_before':verify(),
            'suites':[],
            'scope':'Actual finite author diagnostics and full source/build checks; not an independent referee report or a formal proof certificate.'}
    report['historical_source_checks']=verify_history()
    for version in (*range(10,16),17,18,19,20,21,22,23):
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
    report['inherited_assertions_total']=sum(x['assertions'] for x in report['suites'] if x['version']<23)
    for v in (22,23):
        optimized=out/f'V{v}_OPTIMIZED_RERUN.json'
        run([sys.executable,'-O',f'tests/verify_v{v}.py',str(optimized)],out/f'v{v}-optimized-stdout.txt')
        if optimized.read_bytes()!=(out/f'V{v}_AUTHOR_RERUN.json').read_bytes():
            raise ValueError(f'Optimized v{v} receipt differs')
        report[f'v{v}_optimized_identical_receipt']=True
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
    referee=ROOT.parents[1]/'reviews/a1-english-v21-independent-2026-09-07/independent_diagnostics.py'
    if referee.exists():
        data=referee.read_bytes()
        blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        if blob!='6ff619c9ade544810576c9fa1b74707ba3b5f57a':
            raise ValueError('Referee diagnostic source is not the pinned v21 script')
        regular=out/'REFEREE_V21_RERUN.json';opt=out/'REFEREE_V21_OPTIMIZED.json'
        run([sys.executable,str(referee),'--output',str(regular)],out/'referee-v21-stdout.txt')
        run([sys.executable,'-O',str(referee),'--output',str(opt)],out/'referee-v21-optimized-stdout.txt')
        if regular.read_bytes()!=opt.read_bytes():
            raise ValueError('Referee optimized diagnostic output differs')
        rr=json.loads(regular.read_text())
        if (rr.get('status'),rr.get('total_cases'),rr.get('total_checks'))!=('PASS',140,657):
            raise ValueError('Unexpected referee diagnostic receipt')
        report['referee_v21_rerun']={'executed':True,'status':'PASS','cases':140,'checks':657,
            'source_git_blob':blob,'optimized_identical':True,
            'scope':'Rerun of the pinned referee script; not a new independent referee review.'}
    else:
        report['referee_v21_rerun']={'executed':False,
            'reason':'Pinned review script absent from this local downloaded v21 artifact; repository workflow can rerun it.'}
    referee22=ROOT.parents[1]/'reviews/a1-english-v22-harsh-independent-2026-09-07/independent_diagnostics.py'
    if referee22.exists():
        data=referee22.read_bytes()
        blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        if blob!='8b4fc8f5e957f9b298f9dbb54165b15e92a5f986':
            raise ValueError('Referee diagnostic source is not the pinned v22 script')
        regular=out/'REFEREE_V22_RERUN.json';opt=out/'REFEREE_V22_OPTIMIZED.json'
        run([sys.executable,str(referee22),str(regular)],out/'referee-v22-stdout.txt')
        run([sys.executable,'-O',str(referee22),str(opt)],out/'referee-v22-optimized-stdout.txt')
        if regular.read_bytes()!=opt.read_bytes():
            raise ValueError('Referee v22 optimized diagnostic output differs')
        rr=json.loads(regular.read_text())
        if (rr.get('status'),rr.get('checks'),rr.get('models'))!=('PASS',13884,50):
            raise ValueError('Unexpected v22 referee diagnostic receipt')
        report['referee_v22_rerun']={'executed':True,'status':'PASS','checks':13884,
            'models':50,'histories':400,'prefixes':1200,'source_git_blob':blob,
            'optimized_identical':True,'scope':'Rerun of the pinned referee script, not a new independent review.'}
    else:
        report['referee_v22_rerun']={'executed':False,'reason':'Pinned v22 review script absent.'}
    report['verified_source_files_after']=verify()
    report['passed']=True
    receipt.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__':
    main()
