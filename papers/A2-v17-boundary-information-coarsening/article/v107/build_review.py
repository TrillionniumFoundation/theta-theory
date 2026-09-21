#!/usr/bin/env python3
"""Compile exact v106 and v107 source closures and record reproducible evidence."""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import sys

BASE='5cbbe96cd2ac590bfa2e17bcef97b0630cd91c4a'
REVIEW='bcd8052659a783632de3873af49f05f600a8f764'
PAPER='papers/A2-v17-boundary-information-coarsening'
INPUT=re.compile(r'\\(?:input|include)\{([^}]+)\}')


def cmd(argv: list[str], cwd: Path, check: bool=True) -> subprocess.CompletedProcess:
    return subprocess.run(argv,cwd=cwd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,check=check)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def materialize(repo: Path, commit: str, version: str, dest: Path) -> dict[str,str]:
    pending=[f'article/{version}/paper.tex']; hashes={}
    while pending:
        rel=pending.pop()
        pp=PurePosixPath(rel)
        if pp.is_absolute() or '..' in pp.parts:
            raise ValueError(f'Unsafe TeX input path: {rel}')
        if not pp.suffix: rel += '.tex'
        if rel in hashes: continue
        data=subprocess.check_output(['git','show',f'{commit}:{PAPER}/{rel}'],cwd=repo)
        text=data.decode('utf-8')
        target=dest/rel; target.parent.mkdir(parents=True,exist_ok=True); target.write_bytes(data)
        hashes[rel]=sha(data)
        pending.extend(INPUT.findall(text))
    return dict(sorted(hashes.items()))


def main() -> int:
    repo=Path(cmd(['git','rev-parse','--show-toplevel'],Path.cwd()).stdout.strip())
    head=cmd(['git','rev-parse','HEAD'],repo).stdout.strip()
    out=repo/'build/a2-v107-review'; out.mkdir(parents=True,exist_ok=True)
    receipt={'revision_commit':head,'review_commit':REVIEW,'v106_commit':BASE,
             'evidence_scope':'Native source compilation and finite algebra, not theorem certification',
             'run_url':os.environ.get('A2_RUN_URL'),'versions':{},'errors':[]}
    for tool in ['latexmk','pdflatex','python3']:
        location=shutil.which(tool)
        receipt[tool]=location
        if not location: receipt['errors'].append(f'Missing executable: {tool}')
    if receipt['errors']:
        (out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n'); print(json.dumps(receipt,indent=2)); return 1
    receipt['latexmk_version']=cmd(['latexmk','-v'],repo).stdout
    receipt['pdflatex_version']=cmd(['pdflatex','--version'],repo).stdout
    script=repo/PAPER/'article/v107/checks.py'
    check=cmd([sys.executable,str(script),'--output',str(out/'checks.json')],repo,check=False)
    (out/'checks.stdout.log').write_text(check.stdout)
    receipt['checks_exit_code']=check.returncode
    if check.returncode: receipt['errors'].append('Finite exact checks failed')
    elif (out/'checks.json').exists(): receipt['finite_checks']=json.loads((out/'checks.json').read_text())
    for version,commit in [('v106',BASE),('v107',head)]:
        record={'source_commit':commit,'main':f'{PAPER}/article/{version}/paper.tex'}
        receipt['versions'][version]=record
        try:
            src=out/'sources'/version; pdfdir=out/version; pdfdir.mkdir(parents=True,exist_ok=True)
            record['input_sha256']=materialize(repo,commit,version,src)
            manifest=json.dumps(record['input_sha256'],sort_keys=True).encode()
            record['source_manifest_sha256']=sha(manifest)
            argv=['latexmk','-pdf','-interaction=nonstopmode','-halt-on-error','-file-line-error',
                  f'-outdir={pdfdir}',f'-jobname=A2-{version}',f'article/{version}/paper.tex']
            record['command']=argv
            result=cmd(argv,src,check=False); record['exit_code']=result.returncode
            (pdfdir/'build.stdout.log').write_text(result.stdout)
            logpath=pdfdir/f'A2-{version}.log'
            log=logpath.read_text(errors='replace') if logpath.exists() else result.stdout
            diagnostics=[line for line in log.splitlines() if any(t in line for t in
                ['undefined references','multiply defined','LaTeX Warning: Reference','LaTeX Warning: Citation','Overfull \\hbox','Overfull \\vbox'])]
            record['diagnostics']=diagnostics
            unresolved=any('undefined' in line or 'multiply defined' in line for line in diagnostics)
            pdf=pdfdir/f'A2-{version}.pdf'
            record['native_build_passed']=result.returncode==0 and pdf.exists() and not unresolved
            if pdf.exists():
                record['pdf_sha256']=sha(pdf.read_bytes())
                if shutil.which('pdfinfo'):
                    info=cmd(['pdfinfo',str(pdf)],repo,check=False).stdout
                    (pdfdir/'pdfinfo.txt').write_text(info)
                    pages=re.search(r'^Pages:\s+(\d+)',info,re.M)
                    record['pages']=int(pages.group(1)) if pages else None
            if not record['native_build_passed']: receipt['errors'].append(f'{version} native build or references failed')
        except Exception as exc:
            record['error']=str(exc); receipt['errors'].append(f'{version}: {exc}')
    receipt['status']='passed' if not receipt['errors'] else 'failed'
    receipt['build_script_sha256']=sha(Path(__file__).read_bytes())
    (out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))
    return int(bool(receipt['errors']))

if __name__=='__main__':
    raise SystemExit(main())
