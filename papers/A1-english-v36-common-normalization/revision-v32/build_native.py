#!/usr/bin/env python3
"""Build both native volumes with stable cross-volume reference exports.

This program is included for execution in a complete checkout. Its presence is
not evidence that the native volumes were built in the preparation session.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
from integration import exported_labels


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build(directory: Path, manuscript_commit: str | None = None,
          allow_overfull: bool = False) -> dict:
    directory = directory.resolve()
    for name in ('main.tex', 'companions.tex', 'preamble.tex'):
        if not (directory/name).is_file():
            raise FileNotFoundError(f'Missing native input: {name}')
    compiler = shutil.which('pdflatex')
    if compiler is None:
        raise RuntimeError('pdflatex is required for the complete native build.')
    out = directory/'revision-v32'/'native-build'
    out.mkdir(parents=True, exist_ok=True)
    source_hashes = {str(p.relative_to(directory)):digest(p)
                     for p in sorted(directory.rglob('*'))
                     if p.is_file() and p.suffix in {'.tex','.bib'}
                     and 'native-build' not in p.parts}
    receipt = {
        'status':'STARTED', 'manuscript_commit':manuscript_commit,
        'started_utc':datetime.now(timezone.utc).isoformat(),
        'source_sha256':source_hashes,
        'compiler':subprocess.run([compiler,'--version'],capture_output=True,text=True,
                                   check=True).stdout.splitlines()[0],
        'pdf_visual_inspection':'NOT_PERFORMED_BY_THIS_SCRIPT',
        'passes':[], 'scope':'Complete native main.tex and companions.tex, not the packet.'}
    previous = None
    try:
        for cycle in range(1,7):
            for stem in ('main','companions'):
                cmd=[compiler,'-no-shell-escape','-interaction=nonstopmode',
                     '-halt-on-error','-file-line-error',stem+'.tex']
                proc=subprocess.run(cmd,cwd=directory,capture_output=True,text=True,
                                    encoding='utf-8',errors='replace')
                log_path=out/f'{stem}-pass-{cycle}.stdout.log'
                log_path.write_text(proc.stdout+'\n'+proc.stderr)
                receipt['passes'].append({'volume':stem,'cycle':cycle,
                                          'returncode':proc.returncode,
                                          'stdout_sha256':digest(log_path)})
                if proc.returncode:
                    raise RuntimeError(f'{stem} pass {cycle} failed; see {log_path.name}')
                auxiliary=(directory/(stem+'.aux')).read_text(errors='replace')
                (directory/(stem+'-external.aux')).write_text(exported_labels(auxiliary))
            state=tuple(digest(directory/(s+'-external.aux')) for s in ('main','companions'))
            if cycle >=3 and state == previous:
                break
            previous=state
        else:
            raise RuntimeError('Cross-volume labels did not stabilize within six cycles.')
        warnings={}
        for stem in ('main','companions'):
            log=(directory/(stem+'.log')).read_text(errors='replace')
            hard=('There were undefined references','There were undefined citations',
                  'undefined on input line','multiply defined','Label(s) may have changed',
                  'No file main-external.aux','No file companions-external.aux')
            failures=[w for w in hard if w in log]
            if failures:
                raise RuntimeError(f'Unresolved final {stem} build: {failures}')
            warnings[stem]=[line for line in log.splitlines()
                            if 'Overfull \\hbox' in line or 'Overfull \\vbox' in line]
            if not (directory/(stem+'.pdf')).is_file():
                raise RuntimeError(f'No {stem}.pdf produced.')
        receipt['layout_warnings']=warnings
        if any(warnings.values()) and not allow_overfull:
            raise RuntimeError('Overfull boxes remain. Inspect the PDFs and repair them; '
                               '--allow-overfull records, rather than hides, an explicit exception.')
        receipt['pdfs']={s+'.pdf':{'sha256':digest(directory/(s+'.pdf')),
                                  'bytes':(directory/(s+'.pdf')).stat().st_size}
                         for s in ('main','companions')}
        receipt['status']='COMPILED_REFERENCES_RESOLVED'
        receipt['finished_utc']=datetime.now(timezone.utc).isoformat()
    except Exception as exc:
        receipt['status']='FAILED'
        receipt['failure']=str(exc)
        receipt['finished_utc']=datetime.now(timezone.utc).isoformat()
        (out/'NATIVE_BUILD_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
        raise
    (out/'NATIVE_BUILD_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
    return receipt


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory',type=Path)
    parser.add_argument('--manuscript-commit')
    parser.add_argument('--allow-overfull',action='store_true')
    args=parser.parse_args()
    try:
        receipt=build(args.directory,args.manuscript_commit,args.allow_overfull)
    except Exception as exc:
        print(f'Native build not completed: {exc}',file=sys.stderr)
        return 1
    print(json.dumps({'status':receipt['status'],'pdfs':receipt['pdfs'],
                      'visual_inspection':receipt['pdf_visual_inspection']},indent=2))
    return 0

if __name__=='__main__':
    raise SystemExit(main())
