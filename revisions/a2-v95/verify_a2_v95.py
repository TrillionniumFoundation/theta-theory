#!/usr/bin/env python3
"""Exact-head source preservation and full-build audit for A2 v95.

This checks source identity and reproducibility, not theorem correctness.
Run from a real checkout; the controlling review commit must be available.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tarfile

ROOT=Path(__file__).resolve().parents[2]
PAPER='papers/A2-v17-boundary-information-coarsening/'
BASE='dbbad2d84c6a3b358bddabf84dc16f0b09b38634'
OLD=PAPER+'article/v94/paper.tex'
ENTRY=PAPER+'rigidity_v95.tex'
INPUT=re.compile(r'\\(?:input|include)\{([^}]+)\}')


def git(*args: str) -> bytes:
    return subprocess.check_output(['git','-C',str(ROOT),*args])


def source_graph(entry: str, historical: bool=False) -> dict[str,bytes]:
    seen: dict[str,bytes]={}
    def visit(path: str):
        if path in seen:
            return
        if '..' in Path(path).parts:
            raise ValueError('Parent-directory TeX input is not admitted')
        data=git('show',f'{BASE}:{path}') if historical else (ROOT/path).read_bytes()
        seen[path]=data
        for name in INPUT.findall(data.decode('utf-8')):
            if not name.endswith('.tex'):
                name+='.tex'
            visit(PAPER+name)
    visit(entry)
    return seen


def main() -> None:
    parser=argparse.ArgumentParser()
    parser.add_argument('--receipt',type=Path,required=True)
    parser.add_argument('--compiled',action='store_true')
    parser.add_argument('--package',type=Path)
    args=parser.parse_args()
    head=git('rev-parse','HEAD').decode().strip()
    if os.environ.get('GITHUB_SHA') and os.environ['GITHUB_SHA']!=head:
        raise AssertionError('Runtime HEAD differs from GITHUB_SHA')
    git('merge-base','--is-ancestor',BASE,head)
    manifest=json.loads((ROOT/'revisions/a2-v95/SOURCE_MANIFEST.json').read_text())
    assert manifest['controlling_review_commit']==BASE
    expected=manifest['new_source_sha256']
    for path,sha in expected.items():
        actual=hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
        assert actual==sha, f'New source identity mismatch: {path}'
    old=source_graph(OLD,True)
    active=source_graph(ENTRY)
    inherited=set(old)-{OLD}
    assert inherited<=set(active), f'Missing inherited modules: {sorted(inherited-set(active))}'
    for path in inherited:
        assert active[path]==old[path], f'Inherited source changed: {path}'
    # The only theorem inside the old entrypoint is retained verbatim.
    start=old[OLD].index(b'\\begin{theorem}[Normalization, clock design, and spectral recovery]')
    end=old[OLD].index(b'\\end{theorem}',start)+len(b'\\end{theorem}')
    assert old[OLD][start:end] in active[PAPER+'article/v95/global_statements.tex']
    assert (ROOT/OLD).read_bytes()==old[OLD], 'Historical entrypoint was changed'
    changes=git('diff','--name-status',BASE,head).decode().splitlines()
    assert all(line.startswith('A\t') for line in changes), 'Revision must be addition-only'
    allowed=('revisions/a2-v95/',PAPER+'article/v95/',PAPER+'rigidity_v95.tex',
             PAPER+'core_v95.tex','.github/workflows/a2-v95-native.yml')
    assert all(line.split('\t',1)[1].startswith(allowed) for line in changes)
    labels={}
    for path,data in active.items():
        for label in re.findall(r'\\label\{([^}]+)\}',data.decode()):
            assert label not in labels, f'Duplicate label {label}: {path}, {labels.get(label)}'
            labels[label]=path
    result={'head':head,'controlling_review_commit':BASE,'status':'source-audit-passed',
            'active_tex':sorted(active),'inherited_active_count':len(inherited),
            'preserved_entrypoint_theorem':True,'full_build_checked':False,
            'active_sha256':{p:hashlib.sha256(d).hexdigest() for p,d in active.items()},
            'meaning':'Source identity and build audit; not mathematical proof verification.'}
    if args.compiled:
        log=(ROOT/PAPER/'rigidity_v95.log').read_text(errors='replace')
        forbidden=(r'LaTeX Warning: (?:Reference|Citation).*undefined',
                   r'There were undefined references',r'There were multiply-defined labels',
                   r'Overfull \\[hv]box')
        assert not any(re.search(pattern,log) for pattern in forbidden), 'Unclean full TeX log'
        fls=(ROOT/PAPER/'rigidity_v95.fls').read_text(errors='replace')
        opened=set()
        for line in fls.splitlines():
            if line.startswith('INPUT '):
                p=Path(line[6:])
                p=p if p.is_absolute() else ROOT/PAPER/p
                try:
                    opened.add(p.resolve().relative_to(ROOT).as_posix())
                except ValueError:
                    pass
        assert set(active)<=opened, f'Compiled graph omits: {sorted(set(active)-opened)}'
        pdf=ROOT/PAPER/'rigidity_v95.pdf'
        assert pdf.stat().st_size>1000
        result.update(status='full-build-audit-passed',full_build_checked=True,
                      pdf_sha256=hashlib.sha256(pdf.read_bytes()).hexdigest(),
                      log_sha256=hashlib.sha256(log.encode()).hexdigest())
    args.receipt.parent.mkdir(parents=True,exist_ok=True)
    args.receipt.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    if args.package:
        names=set(active)|set(expected)|{'revisions/a2-v95/SOURCE_MANIFEST.json',
            'reviews/a2-v94-independent-harsh-top4-2026-09-19/REFEREE_REPORT.md'}
        args.package.parent.mkdir(parents=True,exist_ok=True)
        with tarfile.open(args.package,'w:gz') as out:
            for name in sorted(names):
                out.add(ROOT/name,arcname=name)
    print(json.dumps({k:v for k,v in result.items() if k not in ('active_sha256','active_tex')},indent=2))

if __name__=='__main__':
    main()
