#!/usr/bin/env python3
"""Read-only A2 v25 validation; inherited exact sources are never rewritten.

Full-package mode invokes the preserved v24 validator with its own schema.
Historical raw diagnostics and disclosed staged layout wrappers remain visible.
"""
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

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOTS = {'retained/v24':'3d729a1fe93e2250cd68494d149fbb6e90b4096e',
             'complete':'14b2e5379e5b223bc0bdc823c97fd77c2dca2cda'}


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def git(*args: str) -> str | None:
    p=subprocess.run(['git','-C',str(ROOT),*args],text=True,
                     stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
    return p.stdout.strip() if p.returncode==0 else None


def manifest() -> dict[str,str]:
    files=[ROOT/'main.tex',ROOT/'references.tex']
    files+=sorted((ROOT/'core').glob('*.tex'))
    files+=sorted((ROOT/'tools').glob('*.py'))
    files+=sorted((ROOT/'examples').glob('*.json'))
    return {str(p.relative_to(ROOT)):sha(p) for p in files}


def main() -> int:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--all-volumes',action='store_true')
    ap.add_argument('--require-checkout',action='store_true')
    ap.add_argument('--output-dir',default='verification/current')
    args=ap.parse_args()
    out=(ROOT/args.output_dir).resolve()
    if not out.is_relative_to(ROOT/'verification'):
        raise ValueError('output must be below verification/')
    out.mkdir(parents=True,exist_ok=True)
    before=manifest()
    record={'schema':'a2-v25-source-validation-1','status':'running',
        'started_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
        'scope':'all_declared_volumes' if args.all_volumes else 'primary_only',
        'source_commit':git('rev-parse','HEAD'),'source_tree':git('rev-parse','HEAD^{tree}'),
        'github_sha':os.getenv('GITHUB_SHA'),'github_run_id':os.getenv('GITHUB_RUN_ID'),
        'runner_image':os.getenv('ImageOS'),'runner_image_version':os.getenv('ImageVersion'),
        'platform':platform.platform(),'python':sys.version,'source_manifest':before,
        'commands':[],'documents':[],'physical_sensor_executed':False,
        'formal_proof_certificate':False}
    record['execution_kind']='git_checkout' if record['source_commit'] else 'source_content_not_git_checkout'

    def run(argv: list[str],cwd: Path,label: str) -> str:
        p=subprocess.run(argv,cwd=cwd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,
                         env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','TERM':'dumb'})
        path=out/(label+'.log');path.write_text(p.stdout)
        record['commands'].append({'argv':argv,'cwd':str(cwd.relative_to(ROOT)),
            'exit_code':p.returncode,'log':path.name,'log_sha256':sha(path)})
        if p.returncode:
            raise RuntimeError(f'{label}: exit {p.returncode}')
        return p.stdout

    try:
        pins=json.loads((ROOT/'SOURCE_PINS.json').read_text())
        if pins['source_sha256']!=before:
            raise RuntimeError('source pins do not exactly cover the current manifest')
        record['source_pins_sha256']=sha(ROOT/'SOURCE_PINS.json')
        if args.all_volumes and not args.require_checkout:
            raise RuntimeError('all-volume validation requires --require-checkout')
        if args.require_checkout:
            if not record['source_commit'] or git('diff','--name-only','HEAD','--','.')!='':
                raise RuntimeError('no clean tracked Git checkout')
            if record['github_sha'] and record['github_sha']!=record['source_commit']:
                raise RuntimeError('trigger and checkout SHA differ')
            prefix=git('rev-parse','--show-prefix') or ''
            for path,want in SNAPSHOTS.items():
                if git('rev-parse','HEAD:'+prefix+path)!=want:
                    raise RuntimeError('retained tree differs: '+path)
            record['verified_retained_trees']=SNAPSHOTS
        normal=run([sys.executable,'tools/verify_v25.py'],ROOT,'v25-normal')
        optimized=run([sys.executable,'-O','tools/verify_v25.py'],ROOT,'v25-optimized')
        if normal!=optimized:
            raise RuntimeError('normal and optimized output differ')
        record['diagnostics']=json.loads(normal)
        record['normal_optimized_identical']=True
        example=run([sys.executable,'tools/calibrate_fingerprint.py',
                     'examples/numerical_bounds.json'],ROOT,'symbolic-calibration')
        record['calibration_example']=json.loads(example)
        run(['pdflatex','--version'],ROOT,'tex-version')
        run(['latexmk','-v'],ROOT,'latexmk-version')
        run(['latexmk','-g','-pdf','-interaction=nonstopmode','-halt-on-error',
             '-outdir=build','main.tex'],ROOT,'primary-build')
        pdf=ROOT/'build/main.pdf';log=ROOT/'build/main.log'
        problems=re.findall(r'^.*(?:Warning|Overfull|Underfull|undefined).*$',
                            log.read_text(errors='replace'),re.M)
        info=run(['pdfinfo',str(pdf)],ROOT,'primary-pdfinfo')
        pages=re.search(r'^Pages:\s+(\d+)',info,re.M)
        record['documents'].append({'source':'main.tex','pages':int(pages.group(1)) if pages else None,
            'pdf':'build/main.pdf','pdf_sha256':sha(pdf),'tex_log_sha256':sha(log),
            'final_tex_diagnostics':problems,'layout_wrapper_applied':False})
        if problems:
            raise RuntimeError('primary final TeX diagnostics remain')
        if args.all_volumes:
            inherited=ROOT/'retained/v24'
            output='verification/v25-requalification'
            run([sys.executable,'tools/validate_v24.py','--all-volumes','--require-checkout',
                 '--output-dir',output],inherited,'inherited-v24-driver')
            receipt_path=inherited/output/'receipt.json'
            nested=json.loads(receipt_path.read_text())
            if nested['status']!='passed' or nested['source_commit']!=record['source_commit']:
                raise RuntimeError('inherited receipt does not bind current success')
            record['inherited_receipt']={'path':str(receipt_path.relative_to(ROOT)),
                'sha256':sha(receipt_path),'schema':nested['schema'],
                'source_commit':nested['source_commit'],'documents':nested['documents'],
                'raw_historical_documents':nested.get('raw_historical_documents',[])}
            record['inherited_layout_policy']='unchanged v24 driver; raw diagnostics and reversible staged wrappers retained'
        if manifest()!=before:
            raise RuntimeError('mathematical or tool sources changed')
        if args.require_checkout and git('diff','--name-only','HEAD','--','.')!='':
            raise RuntimeError('tracked source changed during validation')
        record['source_unchanged']=True
        record['status']='passed'
    except Exception as exc:
        record['status']='failed';record['error']=str(exc)
    finally:
        record['source_manifest_sha256']=hashlib.sha256(
            json.dumps(before,sort_keys=True,separators=(',',':')).encode()).hexdigest()
        record['finished_utc']=dt.datetime.now(dt.timezone.utc).isoformat()
        (out/'receipt.json').write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
        print(json.dumps(record,indent=2,sort_keys=True))
    return 0 if record['status']=='passed' else 1


if __name__=='__main__':
    raise SystemExit(main())
