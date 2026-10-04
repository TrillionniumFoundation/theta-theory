#!/usr/bin/env python3
"""One-article qualification; preserves history without repackaging it for a journal."""
from __future__ import annotations
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys
import zipfile

ROOT=Path(__file__).resolve().parents[1]
ARCHIVE_TREE='213cecf77265c5ebea98791a99126b9def5d25f0'
SCHEMA='a2-v34-validation-1'


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_tree(path: Path) -> str:
    entries=[]
    for p in path.iterdir():
        name=p.name.encode()
        if p.is_symlink():
            raise ValueError('symlink in preserved source: '+str(p))
        if p.is_dir():
            mode=b'40000'; sha=git_tree(p); key=name+b'/'
        elif p.is_file():
            data=p.read_bytes(); mode=b'100755' if p.stat().st_mode&0o111 else b'100644'
            sha=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest(); key=name
        else:
            raise ValueError('non-regular source: '+str(p))
        entries.append((key,mode+b' '+name+b'\0'+bytes.fromhex(sha)))
    data=b''.join(value for _,value in sorted(entries))
    return hashlib.sha1(b'tree '+str(len(data)).encode()+b'\0'+data).hexdigest()


def git(*args: str) -> str | None:
    p=subprocess.run(['git','-C',str(ROOT),*args],text=True,stdout=subprocess.PIPE,
                     stderr=subprocess.DEVNULL)
    return p.stdout.strip() if p.returncode==0 else None


def manifest() -> dict[str,str]:
    paths=[ROOT/'main.tex',ROOT/'references.tex']
    paths+=sorted((ROOT/'core').glob('*.tex'))+sorted((ROOT/'tools').glob('*.py'))
    return {str(p.relative_to(ROOT)):digest(p) for p in paths}


def validate_contract(pins: dict, actual: dict[str,str], archive: str,
                      expected_commit: str | None, actual_commit: str | None,
                      require_checkout: bool) -> None:
    if pins.get('schema')!='a2-v34-source-pins-1':
        raise ValueError('incorrect pin schema')
    if pins.get('journal_documents')!=['main.tex']:
        raise ValueError('journal package must declare exactly the primary')
    if pins.get('source_sha256')!=actual:
        raise ValueError('source hashes or complete input set differ')
    if archive!=ARCHIVE_TREE or pins.get('archive_v33_tree')!=ARCHIVE_TREE:
        raise ValueError('reviewed full archive differs')
    if require_checkout and (not expected_commit or actual_commit!=expected_commit):
        raise ValueError('exact expected checkout required')
    if expected_commit and actual_commit!=expected_commit:
        raise ValueError('expected and actual source commits differ')


def make_journal_zip(destination: Path, expected: dict[str,str]) -> list[str]:
    names=['main.tex','references.tex']+sorted(str(p.relative_to(ROOT)) for p in (ROOT/'core').glob('*.tex'))
    if any(not n.endswith('.tex') or n.startswith('archive/') for n in names):
        raise ValueError('non-primary journal member')
    with zipfile.ZipFile(destination,'w',zipfile.ZIP_DEFLATED) as z:
        for name in names:
            if digest(ROOT/name)!=expected[name]:
                raise ValueError('source changed before packaging')
            z.write(ROOT/name,name)
    return names


def main() -> int:
    parser=argparse.ArgumentParser()
    parser.add_argument('--require-checkout',action='store_true')
    parser.add_argument('--expected-commit')
    args=parser.parse_args()
    out=ROOT/'verification/current'; out.mkdir(parents=True,exist_ok=True)
    record={'schema':SCHEMA,'status':'running',
            'started_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
            'scope':'primary_and_archive_integrity_not_historical_volume_rebuilds',
            'source_commit':git('rev-parse','HEAD'),
            'github_sha':os.getenv('GITHUB_SHA'),'github_run_id':os.getenv('GITHUB_RUN_ID'),
            'platform':platform.platform(),'python':sys.version,'commands':[],
            'documents':[],'formal_proof_certificate':False,'physical_sensor_executed':False}
    def run(argv: list[str], label: str, cwd: Path=ROOT) -> str:
        p=subprocess.run(argv,cwd=cwd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,
                         env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','TERM':'dumb'})
        log=out/(label+'.log'); log.write_text(p.stdout)
        record['commands'].append({'argv':argv,'cwd':str(cwd.relative_to(ROOT)),
                                   'exit_code':p.returncode,'log':log.name,'sha256':digest(log)})
        if p.returncode:
            raise RuntimeError(label+': exit '+str(p.returncode))
        return p.stdout
    try:
        pins=json.loads((ROOT/'SOURCE_PINS.json').read_text())
        before=manifest(); archived=git_tree(ROOT/'archive/v33')
        validate_contract(pins,before,archived,args.expected_commit,record['source_commit'],args.require_checkout)
        if record['github_sha'] and record['github_sha']!=record['source_commit']:
            raise ValueError('trigger differs from checkout')
        if args.require_checkout and git('status','--porcelain','--untracked-files=no','--','.')!='':
            raise ValueError('tracked checkout not clean')
        record['source_manifest']=before; record['archive_tree']=archived
        record['execution_kind']='exact_expected_checkout' if args.require_checkout else 'source_content'
        record['diagnostics']=[]
        suites=[(ROOT,'tools/verify_v34.py','v34'),(ROOT,'tools/test_contract_v34.py','contract-v34'),
                (ROOT/'archive/v33','tools/verify_v33.py','retained-v33'),
                (ROOT/'archive/v33','tools/test_contract_v33.py','contract-v33'),
                (ROOT/'archive/v33/retained/v32','tools/verify_v32.py','retained-v32'),
                (ROOT/'archive/v33/retained/v32','tools/test_contract.py','contract-v32')]
        for cwd,script,label in suites:
            normal=run([sys.executable,script],label+'-normal',cwd)
            optimized=run([sys.executable,'-O',script],label+'-optimized',cwd)
            if normal!=optimized:
                raise RuntimeError('normal and optimized outputs differ: '+label)
            record['diagnostics'].append({'label':label,'normal_optimized_identical':True,
                                           'result':json.loads(normal)})
        run(['pdflatex','--version'],'tex-version')
        run(['latexmk','-v'],'latexmk-version')
        run(['latexmk','-g','-pdf','-interaction=nonstopmode','-halt-on-error',
             '-outdir=build','main.tex'],'primary-build')
        log=ROOT/'build/main.log'; pdf=ROOT/'build/main.pdf'
        warnings=re.findall(r'^.*(?:Warning|Overfull|Underfull|undefined).*$',log.read_text(errors='replace'),re.M)
        info=run(['pdfinfo',str(pdf)],'primary-pdfinfo')
        pages=re.search(r'^Pages:\s+(\d+)',info,re.M)
        record['documents']=[{'source':'main.tex','pages':int(pages.group(1)) if pages else None,
                              'pdf_sha256':digest(pdf),'final_tex_log_sha256':digest(log),
                              'final_tex_diagnostics':warnings}]
        if warnings:
            raise RuntimeError('final TeX diagnostics')
        record['journal_members']=make_journal_zip(out/'A2-v34-journal-source.zip',before)
        record['journal_zip_sha256']=digest(out/'A2-v34-journal-source.zip')
        if before!=manifest() or git_tree(ROOT/'archive/v33')!=archived:
            raise RuntimeError('qualification modified mathematics, tools or archive')
        if args.require_checkout and git('status','--porcelain','--untracked-files=no','--','.')!='':
            raise RuntimeError('tracked checkout changed')
        record['source_unchanged']=True; record['status']='passed'
    except Exception as exc:
        record['status']='failed'; record['error']=str(exc)
    finally:
        record['finished_utc']=dt.datetime.now(dt.timezone.utc).isoformat()
        (out/'receipt.json').write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
        print(json.dumps(record,indent=2,sort_keys=True))
    return 0 if record['status']=='passed' else 1

if __name__=='__main__':
    raise SystemExit(main())
