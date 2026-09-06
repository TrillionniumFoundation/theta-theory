#!/usr/bin/env python3
"""Build and test the v10 principal; keep inherited inputs unchanged."""
from __future__ import annotations
from pathlib import Path
from datetime import datetime, timezone
import argparse, hashlib, json, os, platform, re, shutil, subprocess, sys, tempfile, time
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[1]

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(command,cwd,log,timeout=180):
    start=time.monotonic()
    p=subprocess.run(command,cwd=cwd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=timeout)
    log.write_text(p.stdout)
    if p.returncode: raise RuntimeError(f'{command!r} failed: see {log}')
    return {'command':list(map(str,command)),'exit_code':p.returncode,'seconds':round(time.monotonic()-start,3),'log':str(log.relative_to(ROOT))}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--context',choices=['local','ci','standalone'],default='standalone');args=ap.parse_args()
    out=ROOT/'validation'/args.context;out.mkdir(parents=True,exist_ok=True)
    before={str(p.relative_to(REPO)):sha(p) for path in ['papers/A1-english-v9','papers/A1-english-v7','reviews/a1-english-v9-2026-09-06'] for p in (REPO/path).rglob('*') if p.is_file()}
    operations=[]
    operations.append(run([sys.executable,str(REPO/'scripts/materialize_a1_v10.py')],REPO,out/'materialize.log'))
    inherited=[]
    with tempfile.TemporaryDirectory(prefix='a1-v10-inherited-') as tmp:
        t=Path(tmp)/'papers';t.mkdir()
        shutil.copytree(REPO/'papers/A1-english-v9',t/'A1-english-v9')
        shutil.copytree(REPO/'papers/A1-english-v7',t/'A1-english-v7')
        old=t/'A1-english-v9'
        for tag,receipt,key,expected in [('v7','DIAGNOSTICS.json','checks_passed',97),('v8','V8_DIAGNOSTICS.json','passed',256),('v9','V9_DIAGNOSTICS.json','passed',642)]:
            op=run([sys.executable,'tests/test_'+tag+'.py'],old,out/(tag+'-inherited.log'))
            data=json.loads((old/receipt).read_text())
            if data[key]!=expected:raise RuntimeError('Unexpected inherited execution count: '+tag)
            dest=out/(tag.upper()+'_INHERITED_RERUN.json');shutil.copy2(old/receipt,dest)
            op.update({'suite':tag,'passed':data[key],'script_sha256':sha(old/'tests'/('test_'+tag+'.py'))})
            inherited.append(op);operations.append(op)
    operations.append(run([sys.executable,'tests/test_v10.py'],ROOT,out/'v10.log'))
    shutil.copy2(ROOT/'validation/V10_DIAGNOSTICS.json',out/'V10_DIAGNOSTICS.json')
    new=json.loads((out/'V10_DIAGNOSTICS.json').read_text())
    reviewer=REPO/'reviews/a1-english-v9-2026-09-06/referee_checks.py'
    operations.append(run([sys.executable,str(reviewer),'--output',str(out/'V9_REFEREE_CODE_RERUN.json')],ROOT,out/'referee-code-rerun.log'))
    ref=json.loads((out/'V9_REFEREE_CODE_RERUN.json').read_text())
    for i in range(1,4):
        operations.append(run(['pdflatex','-no-shell-escape','-interaction=nonstopmode','-halt-on-error','main.tex'],ROOT,out/f'latex-pass-{i}.log'))
    text=(ROOT/'main.log').read_text(errors='replace')
    bad=[line for line in text.splitlines() if re.search(r'undefined|multiply defined|Overfull|Fatal error',line,re.I)]
    if bad:raise RuntimeError('TeX validation warnings: '+repr(bad))
    page_match=re.search(r'Output written on main.pdf \((\d+) pages?',text)
    if page_match is None:raise RuntimeError('No PDF completion receipt')
    after={p:sha(REPO/p) for p in before}
    if before!=after:raise RuntimeError('Inherited input changed during build')
    preservation=json.loads((ROOT/'validation/PRESERVATION.json').read_text())
    report={'context':args.context,'generated_utc':datetime.now(timezone.utc).isoformat(),
        'python':platform.python_version(),'platform':platform.platform(),
        'input_commit':os.environ.get('GITHUB_SHA'),'workflow_run_id':os.environ.get('GITHUB_RUN_ID'),
        'inherited_suites':[{'suite':o['suite'],'passed':o['passed']} for o in inherited],
        'new_assertions_passed':new['passed_assertions'],'new_assertions_failed':new['failed_assertions'],
        'referee_script_rerun_passed':ref['passed'],'referee_script_rerun_failed':ref['failed'],
        'referee_script_sha256':sha(reviewer),
        'referee_rerun_status':'Author-side rerun of unchanged reviewer code; not a new independent review.',
        'new_index_only_fixtures':new['index_only_fixtures'],'new_exact_raw_update_comparisons':new['exact_raw_update_comparisons'],
        'inherited_labels':preservation['inherited_labels'],'inherited_proofs':preservation['inherited_proofs'],
        'printed_labels':preservation['printed_labels'],'printed_proofs':preservation['printed_proofs'],
        'unchanged_inherited_files_checked':len(before),'inherited_inputs_unchanged':True,
        'pdf_pages':int(page_match.group(1)),'pdf_sha256':sha(ROOT/'main.pdf'),
        'tex_log_sha256':sha(ROOT/'main.log'),'undefined_or_overfull_warnings':bad,
        'operations':operations,
        'scope':'Source integrity, finite program execution and PDF compilation only. No proof-assistant, originality or editorial certification.'}
    (out/'BUILD_REPORT.json').write_text(json.dumps(report,indent=2)+'\n')
    manifest={str(p.relative_to(ROOT)):sha(p) for p in ROOT.rglob('*') if p.is_file() and p.suffix in {'.tex','.in','.py','.md'} and '__pycache__' not in p.parts}
    (out/'SOURCE_MANIFEST.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ['operations']},indent=2))
if __name__=='__main__':main()
