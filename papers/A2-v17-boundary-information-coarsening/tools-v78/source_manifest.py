#!/usr/bin/env python3
"""Record actual TeX recorder inputs and products, never infer remote CI success."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

def digest(path: Path) -> dict[str, str | int]:
    data=path.read_bytes()
    return {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),
            'git_blob':hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()}

def command(args: list[str]) -> str | None:
    result=subprocess.run(args,capture_output=True,text=True,check=False)
    return result.stdout.strip() if result.returncode==0 else None

def main() -> None:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--build-dir',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args(); root=Path.cwd().resolve(); out=args.build_dir.resolve()
    source_inputs={}; products={}
    for entry in ('two_collision','main','rigidity_v78','periodic_companion_v78'):
        fls=out/f'{entry}.fls'
        if not fls.exists():
            raise RuntimeError(f'Missing recorder: {fls}')
        for line in fls.read_text().splitlines():
            if not line.startswith('INPUT '):
                continue
            path=Path(line[6:]); path=path.resolve() if path.is_absolute() else (root/path).resolve()
            if path.suffix not in ('.tex','.bib','.sty','.cls'):
                continue
            try:
                rel=path.relative_to(root)
            except ValueError:
                continue
            if path.is_file():
                source_inputs[str(rel)]=digest(path)
        pdf=out/f'{entry}.pdf'; info=command(['pdfinfo',str(pdf)])
        if info is None:
            raise RuntimeError(f'Unreadable PDF: {pdf}')
        pages=re.search(r'^Pages:\s+(\d+)',info,re.M)
        log=(out/f'{entry}.log').read_text(errors='replace')
        products[entry]=dict(digest(pdf),pages=int(pages.group(1)) if pages else None,
                            overfull_boxes=log.count('Overfull \\hbox'),
                            unresolved=bool(re.search(r'(Reference|Citation).*undefined|multiply defined',log)))
    report={'kind':'native build with recorded inputs',
      'remote_ci':os.environ.get('GITHUB_ACTIONS')=='true',
      'workflow_run':os.environ.get('GITHUB_RUN_ID'),
      'workflow_attempt':os.environ.get('GITHUB_RUN_ATTEMPT'),
      'build_tools':{str(p):digest(p) for p in sorted(Path('tools-v78').glob('*')) if p.is_file()},
      'repository_commit':command(['git','rev-parse','HEAD']),
      'source_date_epoch':os.environ.get('SOURCE_DATE_EPOCH'),
      'tex_version':command(['pdflatex','--version']).splitlines()[0],
      'source_inputs':dict(sorted(source_inputs.items())), 'products':products,
      'diagnostics':{name:digest(out/name) for name in ('check-v78-normal.json','check-v78-optimized.json')},
      'scope':'Compilation and finite diagnostics are not formal verification or a referee endorsement.'}
    args.output.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'products':products,'recorded_source_inputs':len(source_inputs)},indent=2))

if __name__=='__main__':
    main()
