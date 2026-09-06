#!/usr/bin/env python3
"""Audit the complete checked-in V5 source and optionally compile its full PDF.

Never writes to retained-v4 or to the repository's review directories.
A receipt is emitted only after the corresponding audit/build actually runs.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone

ROOT=Path(__file__).resolve().parent

def git_blob(path: Path) -> str:
    data=path.read_bytes()
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()

def expand(path: Path, active: tuple[Path,...]=()) -> tuple[str,list[str]]:
    path=path.resolve()
    if ROOT not in path.parents or not path.is_file():
        raise RuntimeError(f'Missing or outside source: {path}')
    if path in active:
        raise RuntimeError(f'Cyclic TeX input: {path}')
    text=path.read_text(encoding='utf-8')
    used=[str(path.relative_to(ROOT))]
    def include(m: re.Match[str]) -> str:
        child=ROOT/m.group(1)
        if not child.suffix:child=child.with_suffix('.tex')
        body,files=expand(child,active+(path,))
        used.extend(files)
        return body
    return re.sub(r'\\input\{([^}]+)\}',include,text),used

def audit() -> dict:
    manifest=json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())
    text,files=expand(ROOT/'main.tex')
    # Ignore TeX comments for the reference/label scan.
    text=re.sub(r'(?<!\\)%[^\n]*','',text)
    labels=re.findall(r'\\label\{([^}]+)\}',text)
    duplicated=sorted({x for x in labels if labels.count(x)>1})
    if duplicated:raise RuntimeError(f'Duplicate labels: {duplicated}')
    refs=set(re.findall(r'\\(?:eqref|ref|pageref)\{([^}]+)\}',text))
    missing=sorted(refs-set(labels))
    if missing:raise RuntimeError(f'Unresolved source references: {missing}')
    cites={x.strip() for group in re.findall(r'\\cite(?:\[[^]]*\])?\{([^}]+)\}',text) for x in group.split(',')}
    bib=set(re.findall(r'\\bibitem(?:\[[^]]*\])?\{([^}]+)\}',text))
    if cites-bib:raise RuntimeError(f'Missing bibliography keys: {sorted(cites-bib)}')
    expected=manifest['inherited_principal_labels']+manifest['new_principal_labels']
    if set(expected)-set(labels):raise RuntimeError('Principal label preservation failure')
    inherited={}
    for name,expected_sha in manifest['inherited_component_blobs'].items():
        actual=git_blob(ROOT/name)
        if actual!=expected_sha:raise RuntimeError(f'Inherited blob mismatch: {name}: {actual}')
        preserved=git_blob(ROOT/'retained-v4'/name)
        if preserved!=expected_sha:raise RuntimeError(f'Retained blob mismatch: {name}')
        inherited[name]=actual
    new_hashes={}
    for name,expected_sha in manifest['new_source_sha256'].items():
        actual=hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
        if actual!=expected_sha:raise RuntimeError(f'New source checksum mismatch: {name}')
        new_hashes[name]=actual
    return {'status':'PASS','utc':datetime.now(timezone.utc).isoformat(),
            'inputs':files,'label_count':len(labels),'principal_labels':len(expected),
            'inherited_principal_labels':len(manifest['inherited_principal_labels']),
            'new_principal_labels':len(manifest['new_principal_labels']),
            'inherited_component_blobs':inherited,'new_source_sha256':new_hashes,
            'missing_references':missing,'missing_citations':sorted(cites-bib),
            'formal_verification':False}

def main() -> None:
    p=argparse.ArgumentParser()
    p.add_argument('--audit',action='store_true',help='Check source and preservation without compiling')
    p.add_argument('--build',action='store_true',help='Audit then compile the full main.tex')
    args=p.parse_args()
    if not (args.audit or args.build):p.error('choose --audit or --build')
    out=ROOT/'validation';out.mkdir(exist_ok=True)
    result=audit()
    (out/'V5_SOURCE_AUDIT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(f"Source audit PASS: {result['principal_labels']} principal labels, {len(result['inputs'])} inputs")
    if args.build:
        if not shutil.which('latexmk'):raise RuntimeError('latexmk is required for --build')
        build=ROOT/'build-v5';build.mkdir(exist_ok=True)
        cmd=['latexmk','-pdf','-interaction=nonstopmode','-halt-on-error',f'-outdir={build}',str(ROOT/'main.tex')]
        run=subprocess.run(cmd,cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,check=False)
        (out/'V5_LATEXMK.log').write_text(run.stdout)
        if run.returncode:raise RuntimeError(f'LaTeX build failed ({run.returncode}); see V5_LATEXMK.log')
        log=(build/'main.log').read_text(errors='replace')
        unresolved=[line for line in log.splitlines() if 'undefined references' in line.lower() or ('LaTeX Warning:' in line and 'undefined' in line)]
        if unresolved:raise RuntimeError('Undefined references/citations remain: '+str(unresolved))
        pdf=build/'main.pdf'
        if not pdf.is_file():raise RuntimeError('No PDF emitted')
        overfull=[line for line in log.splitlines() if 'Overfull \\hbox' in line or 'Overfull \\vbox' in line]
        receipt={'status':'PASS','utc':datetime.now(timezone.utc).isoformat(),
                 'command':cmd,'pdf':'build-v5/main.pdf','pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),
                 'undefined_references_or_citations':unresolved,'overfull_warnings':overfull,
                 'visual_inspection_performed':False,'formal_verification':False}
        (out/'V5_BUILD.json').write_text(json.dumps(receipt,indent=2)+'\n')
        print('Full PDF build PASS; visual review is a separate operation')

if __name__=='__main__':
    try:main()
    except (RuntimeError,OSError,ValueError) as error:
        print(f'ERROR: {error}',file=sys.stderr)
        sys.exit(1)
