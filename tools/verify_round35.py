#!/usr/bin/env python3
"""Read-only manifest check, exact certificate, regressions and isolated builds.

Outputs live under build/. This verifier never modifies manuscript sources or
publishes Git refs. Reproducibility is tested with two fresh directories using
one locally installed toolchain; it is not a cross-toolchain guarantee.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ENTRIES=[('dossier','ROUND35_REVISION.tex'),
 ('C1','papers/C1-information-risk-sensitive-saddles/main.tex'),
 ('B1','papers/B1-microcanonical-preparation/main.tex'),
 ('B3','papers/B3-hamilton-boltzmann-cotangents/main.tex'),
 ('C2','papers/C2-cotangent-rigidity-tangent-representations/main.tex')]
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def check_manifest():
    manifest=json.loads((ROOT/'round35/SOURCE_MANIFEST.json').read_text())
    for name,expected in manifest['files'].items():
        p=ROOT/name
        if not p.is_file() or digest(p)!=expected:raise RuntimeError('hash mismatch: '+name)
    return manifest

def build_copy(directory,manifest):
    for name in manifest['files']:
        target=directory/name;target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(ROOT/name,target)
    env=os.environ.copy();env.update(SOURCE_DATE_EPOCH='1788397200',FORCE_SOURCE_DATE='1',TZ='UTC')
    results={}
    for code,name in ENTRIES:
        source=directory/name;dest=directory/'build'/code;dest.mkdir(parents=True)
        command=['pdflatex','-no-shell-escape','-halt-on-error','-interaction=nonstopmode','-recorder','-output-directory='+str(dest),source.name]
        for repeat in range(3):
            cp=subprocess.run(command,cwd=source.parent,env=env,text=True,capture_output=True,timeout=90)
            (dest/('pass%d.stdout'%repeat)).write_text(cp.stdout+cp.stderr)
            if cp.returncode:raise RuntimeError('LaTeX failed: '+code+'\n'+cp.stdout[-3000:])
        pdf=dest/(source.stem+'.pdf');log=(dest/(source.stem+'.log')).read_text(errors='replace')
        for bad in ('There were undefined references','There were multiply-defined labels','Undefined control sequence','LaTeX Warning: Citation'):
            if bad in log:raise RuntimeError(code+': '+bad)
        info=subprocess.run(['pdfinfo',str(pdf)],text=True,capture_output=True,check=True).stdout
        pages=int(re.search(r'^Pages:\s+(\d+)',info,re.M).group(1))
        overfull=[float(x) for x in re.findall(r'Overfull \\hbox \(([0-9.]+)pt too wide\)',log)]
        if max(overfull,default=0.0)>1.0:raise RuntimeError(code+': overfull box exceeds one point')
        results[code]=dict(sha256=digest(pdf),pages=pages,bytes=pdf.stat().st_size,
                           overfull_hbox_max_pt=max(overfull,default=0.0),source=name)
        out=ROOT/'build/round35'/code;out.mkdir(parents=True,exist_ok=True)
        shutil.copy2(pdf,out/'manuscript.pdf');shutil.copy2(dest/(source.stem+'.log'),out/'build.log')
    return results

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--skip-build',action='store_true')
    args=parser.parse_args();out=ROOT/'build/round35';out.mkdir(parents=True,exist_ok=True)
    manifest=check_manifest();started=time.monotonic()
    env=os.environ.copy();env['OPENBLAS_NUM_THREADS']='1';env['PYTHONDONTWRITEBYTECODE']='1'
    tests=subprocess.run([sys.executable,'-m','unittest','discover','-s','tests','-p','test_round35.py','-v'],cwd=ROOT,env=env,text=True,capture_output=True,timeout=120)
    testtext=tests.stdout+tests.stderr;(out/'tests.log').write_text(testtext)
    if tests.returncode:raise RuntimeError(testtext)
    count=int(re.search(r'Ran (\d+) tests',testtext).group(1))
    cp=subprocess.run([sys.executable,'tools/certify_round35.py','--output','build/round35/embedding-certificate.json'],cwd=ROOT,env=env,text=True,capture_output=True,check=True,timeout=60)
    certificate=json.loads(cp.stdout)
    if certificate != json.loads((ROOT/'round35/EMBEDDING_CERTIFICATE.json').read_text()):
        raise RuntimeError('committed rational certificate differs from recomputation')
    builds=[]
    if not args.skip_build:
        for _ in range(2):
            with tempfile.TemporaryDirectory(prefix='theta-r35-build-') as d:
                builds.append(build_copy(Path(d),manifest))
        if builds[0]!=builds[1]:raise RuntimeError('isolated build mismatch')
    check_manifest()
    record=dict(base_commit='9f5276233b63218a0d89df6611381975dc873232',
      source_manifest_sha256=digest(ROOT/'round35/SOURCE_MANIFEST.json'),
      source_files_verified=len(manifest['files']),tests_run=count,test_failures=0,
      exact_embedding_certified=certificate['embedding_certified'],
      isolated_builds_identical=(len(builds)==2),builds=(builds[0] if builds else {}),
      python=sys.version.split()[0],verification_seconds=round(time.monotonic()-started,3),
      remote_ci_verified=False,all_original_gaps_closed=False,formal_proof_assistant_used=False,
      scope='Local source, finite regressions, exact rational embedding certificate and repeated same-toolchain LaTeX builds.')
    (out/'verification.json').write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
    print(json.dumps(record,indent=2,sort_keys=True))
    return 0
if __name__=='__main__':raise SystemExit(main())
