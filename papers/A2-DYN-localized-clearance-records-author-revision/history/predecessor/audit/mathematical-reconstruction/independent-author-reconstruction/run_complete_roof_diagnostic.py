#!/usr/bin/env python3
"""Record actual auxiliary-check execution, independently of deterministic math JSON."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parent
PYTHON=Path('/workspace/scratch/35c64a3513c5/a2dyn-roof-venv/bin/python')
SOURCE=Path('/workspace/scratch/35c64a3513c5/theta-theory-next/papers/A2-DYN-physical-roof-variation-author-revision/core/323_complete_physical_roof_variation.tex')
PROGRAM=ROOT/'check_complete_roof_variation.py'
OUT=ROOT/'execution'
OUT.mkdir(exist_ok=True)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

run_id=datetime.now(timezone.utc).strftime('323-%Y%m%dT%H%M%S%fZ')
source_before,program_before=sha(SOURCE),sha(PROGRAM)
receipts=[]
for mode in ['normal','optimized']:
    details=OUT/(mode+'.details.json')
    command=[str(PYTHON)]+(['-O'] if mode=='optimized' else [])+[str(PROGRAM),'--source',str(SOURCE),'--details',str(details)]
    started=datetime.now(timezone.utc).isoformat()
    timer=time.monotonic()
    result=subprocess.run(command,cwd=ROOT,capture_output=True,check=False)
    elapsed=time.monotonic()-timer
    finished=datetime.now(timezone.utc).isoformat()
    stdout=OUT/(mode+'.stdout.log');stderr=OUT/(mode+'.stderr.log')
    stdout.write_bytes(result.stdout);stderr.write_bytes(result.stderr)
    receipt={'command_id':run_id+'-'+mode,'mode':mode,'command':command,'cwd':str(ROOT),
             'started_utc':started,'finished_utc':finished,'elapsed_seconds':elapsed,
             'exit_code':result.returncode,'stdout':stdout.name,'stderr':stderr.name,
             'stdout_bytes':len(result.stdout),'stderr_bytes':len(result.stderr),
             'stdout_sha256':sha(stdout),'stderr_sha256':sha(stderr),
             'program_sha256':program_before,'source323_sha256':source_before,
             'scope':'Actual finite analytic diagnostic invocation; not a source/TeX/physical-model proof run.'}
    (OUT/(mode+'.command.json')).write_text(json.dumps(receipt,indent=2)+'\n')
    receipts.append(receipt)
    if result.returncode != 0:
        raise RuntimeError('Auxiliary diagnostic failed in '+mode+'; actual logs retained')
    if not details.is_file() or details.read_bytes()!=result.stdout:
        raise RuntimeError('Details/stdout mismatch in '+mode)
    payload=json.loads(result.stdout)
    if payload['source_sha256']!=source_before or payload['program_sha256']!=program_before:
        raise RuntimeError('Diagnostic did not identify the expected source/program')
if sha(SOURCE)!=source_before or sha(PROGRAM)!=program_before:
    raise RuntimeError('Source or program changed during execution; receipts must not be frozen')
if (OUT/'normal.stdout.log').read_bytes()!=(OUT/'optimized.stdout.log').read_bytes():
    raise RuntimeError('Normal and optimized deterministic mathematical outputs differ')
summary={'status':'passed','run_id':run_id,'source323_sha256':source_before,'program_sha256':program_before,
         'commands':receipts,'normal_optimized_stdout_byte_identical':True,
         'normal_optimized_details_byte_identical':True,'mathematical_output_sha256':sha(OUT/'normal.stdout.log'),
         'total_checks_each':payload['total_checks'],'counts':payload['counts'],
         'scope':payload['scope'],'continuum_proof_certificate':False,
         'source_and_program_unchanged_during_run':True}
(OUT/'EXECUTION_SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({key:value for key,value in summary.items() if key!='commands'},indent=2))
