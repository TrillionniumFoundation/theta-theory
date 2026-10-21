#!/usr/bin/env python3
"""Rebuild the frozen 390-file native historical assembly in an isolated copy."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json
import shutil
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
def digest(p):
    b=p.read_bytes()
    return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=ROOT/'build/current-history')
    args=parser.parse_args()
    out=args.output.resolve()
    out.mkdir(parents=True,exist_ok=True)
    source=ROOT/'history/predecessor/history/predecessor/history/historical-v108'
    copied=out/'isolated-source'
    if copied.exists():
        raise RuntimeError('Use a fresh historical output directory to retain all attempts')
    shutil.copytree(source,copied)
    command=[sys.executable,'-B',str(copied/'rebuild_history.py'),'--evidence-dir',str(out/'execution')]
    started=datetime.now(timezone.utc).isoformat()
    with (out/'rebuild.stdout.log').open('wb') as handle:
        run=subprocess.run(command,stdout=handle,stderr=subprocess.STDOUT,check=False)
    result={'started_utc':started,'finished_utc':datetime.now(timezone.utc).isoformat(),
            'command':command,'exit_code':run.returncode,
            'scope':'Actual original assembler and six pdflatex passes on isolated historical source copy',
            'historical_repository_wide_gate_executed':False,'continuum_proof_certificate':False,
            'log':digest(out/'rebuild.stdout.log')}
    if run.returncode==0:
        for name in ('main','supplement'):
            shutil.copy2(copied/'build'/(name+'.pdf'),out/('historical-'+name+'.pdf'))
        result['documents']=[digest(out/('historical-'+n+'.pdf')) for n in ('main','supplement')]
    (out/'REBUILD_SUMMARY.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'passed' if run.returncode==0 else 'failed','output':str(out)}))
    return run.returncode
if __name__=='__main__':
    raise SystemExit(main())
