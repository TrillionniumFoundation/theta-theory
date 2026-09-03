#!/usr/bin/env python3
"""Read-only source validation, finite examples, and clean LaTeX builds.
This is not a mathematical proof verifier. It never patches source files.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
REVIEW='e037717914a34fe7c0636743b3f5c645969bcb20'
CODES=('A1','A2','A3','A4','B1','B2','B3','B4','C1','C2','D1')

def digest(p: Path)->str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def run(cmd:list[str],cwd:Path=ROOT,timeout:int=120)->str:
    result=subprocess.run(cmd,cwd=cwd,text=True,stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,timeout=timeout,env={**os.environ,'TERM':'xterm'})
    if result.returncode:
        raise RuntimeError(f'Command failed: {cmd}\n{result.stdout[-15000:]}')
    return result.stdout

def check_manifest()->dict:
    path=ROOT/'ROUND33_SOURCE_MANIFEST.json'
    manifest=json.loads(path.read_text())
    if manifest['review_commit']!=REVIEW: raise AssertionError('Wrong review baseline')
    for entry in manifest['files']:
        p=ROOT/entry['path']
        if not p.is_file() or digest(p)!=entry['sha256']:
            raise AssertionError(f'Source digest mismatch: {entry["path"]}')
        if p.stat().st_size!=entry['bytes']: raise AssertionError('Source size mismatch')
    return manifest

def check_sources()->dict:
    labels={};refs=[];statements=0
    for code in CODES:
        path=ROOT/f'round33/chapters/{code}.tex'
        raw=path.read_bytes()
        if any(c<32 and c != 10 for c in raw):
            raise AssertionError(f'Control byte: {path}')
        text=raw.decode('utf-8')
        if re.search(r'\\(?:input|include)\{',text):
            raise AssertionError('Chapter must not import historical sources')
        if text.count(r'\begin{proof}')!=text.count(r'\end{proof}'):
            raise AssertionError(f'Unbalanced proof environment: {code}')
        for env in ('theorem','lemma','proposition','corollary','definition'):
            if text.count('\\begin{'+env+'}')!=text.count('\\end{'+env+'}'):
                raise AssertionError(f'Unbalanced {env}: {code}')
        statements+=len(re.findall(r'\\begin\{(?:theorem|lemma|proposition|corollary)\}',text))
        local=set(re.findall(r'\\label\{([^}]+)\}',text))
        all_local=re.findall(r'\\label\{([^}]+)\}',text)
        if len(local)!=len(all_local): raise AssertionError(f'Duplicate local labels: {code}')
        for label in local:
            if label in labels: raise AssertionError(f'Duplicate global label: {label}')
            if ':r33-' not in label: raise AssertionError(f'Unversioned label: {label}')
            labels[label]=code
        for ref in re.findall(r'\\(?:eqref|ref)\{([^}]+)\}',text):
            if ref not in local: raise AssertionError(f'Nonlocal or absent reference: {code}:{ref}')
            refs.append(ref)
        directories=list((ROOT/'papers').glob(code+'-*'))
        if len(directories)!=1: raise AssertionError(f'Ambiguous paper directory: {code}')
        folder=directories[0]
        main=(folder/'main.tex').read_text()
        wrapper=(folder/'ROUND33_REVISION.tex').read_text()
        if re.findall(r'\\input\{([^}]+)\}',main)!=['ROUND33_REVISION.tex']:
            raise AssertionError(f'Wrong canonical entry: {code}')
        imports=re.findall(r'\\input\{([^}]+)\}',wrapper)
        if imports!=['../../ROUND33_PREAMBLE.tex',f'../../round33/chapters/{code}.tex']:
            raise AssertionError(f'Wrong standalone imports: {code}')
    expected=['ROUND33_PREAMBLE.tex']+[f'round33/chapters/{c}.tex' for c in CODES]
    actual=re.findall(r'\\input\{([^}]+)\}',(ROOT/'ROUND33_REVISION_DOSSIER.tex').read_text())
    if actual!=expected: raise AssertionError('Wrong dossier import graph')
    ledger=json.loads((ROOT/'round33/ISSUE_LEDGER.json').read_text())
    if len(ledger['issues'])!=76 or ledger['all_original_gaps_closed'] is not False:
        raise AssertionError('Issue ledger must preserve unresolved application status')
    return {'chapters':11,'canonical_entries':11,'local_references':len(refs),
            'unique_labels':len(labels),'theorem_level_statements':statements,
            'mapped_referee_objections':76,'source_checks':'pass'}

def clean_build(tex:Path,out:Path)->dict:
    if out.exists(): shutil.rmtree(out)
    out.mkdir(parents=True)
    command=['latexmk','-pdf','-interaction=nonstopmode','-halt-on-error',
             '-file-line-error','-outdir='+str(out),tex.name]
    output=run(command,cwd=tex.parent,timeout=240)
    (out/'latexmk-output.txt').write_text(output)
    log=(out/(tex.stem+'.log')).read_text(errors='replace')
    forbidden=['Undefined control sequence','LaTeX Warning: There were undefined references',
               'multiply defined','LaTeX Error:']
    if any(word in log for word in forbidden): raise AssertionError(f'TeX diagnostic: {tex}')
    if 'Overfull \\hbox' in log or 'Overfull \\vbox' in log:
        raise AssertionError(f'Overfull layout requires inspection: {tex}')
    pdf=out/(tex.stem+'.pdf')
    if not pdf.is_file() or not pdf.read_bytes().startswith(b'%PDF-'):
        raise AssertionError('Invalid PDF')
    info=run(['pdfinfo',str(pdf)])
    pages=int(re.search(r'^Pages:\s+(\d+)',info,re.M).group(1))
    render=out/'first-page'
    run(['pdftoppm','-f','1','-singlefile','-scale-to','1200','-png',str(pdf),str(render)])
    if not render.with_suffix('.png').is_file(): raise AssertionError('PDF render missing')
    return {'file':str(pdf.relative_to(ROOT)),'pages':pages,'bytes':pdf.stat().st_size,'sha256':digest(pdf)}

def main()->int:
    parser=argparse.ArgumentParser()
    parser.add_argument('--build',action='store_true')
    args=parser.parse_args()
    manifest=check_manifest();source_info=check_sources()
    build=ROOT/'build';build.mkdir(exist_ok=True)
    examples=build/'ROUND33_REGRESSION_RESULTS.json'
    print(run([sys.executable,str(ROOT/'tests/test_round33.py'),str(examples)]))
    tests=json.loads(examples.read_text())
    result={**source_info,'scope':'source integrity, finite examples, and optional PDF builds; not a certificate of original mechanical application proofs',
        'source_manifest_sha256':digest(ROOT/'ROUND33_SOURCE_MANIFEST.json'),
        'review_commit':REVIEW,'regressions_passed':tests['passed'],
        'regressions_failed':tests['failed'],'pdfs':[],'remote_ci_verified':False}
    if args.build:
        for cmd in ('latexmk','pdflatex','pdfinfo','pdftoppm'):
            if shutil.which(cmd) is None: raise RuntimeError(f'Missing build tool: {cmd}')
        for code in CODES:
            folder=next((ROOT/'papers').glob(code+'-*'))
            result['pdfs'].append(clean_build(folder/'ROUND33_REVISION.tex',build/code))
        result['pdfs'].append(clean_build(ROOT/'ROUND33_REVISION_DOSSIER.tex',build/'dossier'))
        result['tex_engine']=run(['pdflatex','--version']).splitlines()[0]
    check_manifest() # Detect any unintended source mutation by build/test steps.
    result['status']='pass'
    (build/'ROUND33_BUILD_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    return 0

if __name__=='__main__':
    try: raise SystemExit(main())
    except (AssertionError,RuntimeError,OSError,ValueError,subprocess.SubprocessError) as exc:
        print(f'ROUND33 validation failed: {exc}',file=sys.stderr)
        raise SystemExit(1)
