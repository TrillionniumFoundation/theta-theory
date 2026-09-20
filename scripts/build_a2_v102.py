#!/usr/bin/env python3
"""Source-bound native build of the A2 v102 principal and complete record.

Reuse the reviewed literal TeX/PDF graph walker. A native_passed receipt
is written only after all four targets have built and logs are checked.
The receipt names the built source commit, not a later artifact-only commit.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / 'papers/A2-v17-boundary-information-coarsening'
REVIEW = '9e7caa42cce40587828f7e8357c119e127a56805'


def command(*args: str) -> str:
    return subprocess.check_output(args, cwd=ROOT, text=True).strip()


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--output', type=Path, default=ROOT/'revisions/a2-v102/native')
    args = parser.parse_args()
    output = args.output.resolve()
    if not output.is_relative_to(ROOT/'revisions/a2-v102') or output == ROOT/'revisions/a2-v102':
        raise ValueError('Output must be a child directory of revisions/a2-v102')
    spec = importlib.util.spec_from_file_location('a2_native_base', ROOT/'scripts/build_a2_v100.py')
    if spec is None or spec.loader is None:
        raise RuntimeError('Reviewed recursive builder is missing')
    builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(builder)
    entries = [PAPER/f'rigidity_v102{s}.tex' for s in ('', '_supporting', '_archive', '_complete')]
    head = command('git', 'rev-parse', 'HEAD')
    order = builder.build(entries, dry_run=True)
    sources = {Path(__file__).resolve(), ROOT/'scripts/build_a2_v100.py',
               ROOT/'scripts/check_a2_v102.py', ROOT/'.github/workflows/a2-v102.yml'}
    binary_inputs = set()
    for name in order:
        graph = builder.tex_graph(PAPER/name)
        sources.update(graph)
        for source in graph:
            for name_pdf in builder.PDF.findall(builder.text_without_comments(source)):
                pdf = (PAPER/name_pdf).with_suffix('.pdf').resolve()
                if not pdf.with_suffix('.tex').exists():
                    if not pdf.is_relative_to(ROOT) or not pdf.exists():
                        raise RuntimeError(f'Unbound binary input: {pdf}')
                    binary_inputs.add(pdf)
    hashes = {}
    for source in sorted(sources | binary_inputs):
        relative = source.relative_to(ROOT).as_posix()
        committed = subprocess.check_output(['git', 'show', f'{head}:{relative}'], cwd=ROOT)
        if committed != source.read_bytes():
            raise RuntimeError(f'Working source differs from {head}: {relative}')
        hashes[relative] = digest(source)
    changes = command('git','diff','--name-status',REVIEW,head).splitlines()
    if any(not line.startswith('A\t') for line in changes):
        raise RuntimeError('The revision changed an inherited path; inspect before building')
    plan = {'source_head':head,'source_tree':command('git','rev-parse','HEAD^{tree}'),
            'review_base':REVIEW,'native_build_order':order,'source_sha256':hashes,
            'binary_only_input_paths':[p.relative_to(ROOT).as_posix() for p in sorted(binary_inputs)],
            'preservation':'addition-only relative to controlling review', 'changes':changes}
    if args.dry_run:
        print(json.dumps(plan,indent=2,sort_keys=True))
        return
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    (output/'BUILD_PLAN.json').write_text(json.dumps(plan,indent=2,sort_keys=True)+'\n')
    subprocess.run([sys.executable,str(ROOT/'scripts/check_a2_v102.py'),'--output',str(output/'EXACT_DIAGNOSTICS.json')],cwd=ROOT,check=True)
    builder.build(entries,dry_run=False)
    for name in order:
        log=(PAPER/name).with_suffix('.log')
        text=log.read_text(errors='replace')
        bad=('LaTeX Error:', 'There were undefined references', 'multiply defined')
        if any(s in text for s in bad) or ('Citation ' in text and 'undefined' in text):
            raise RuntimeError(f'Unresolved native log: {log}')
    for name,sha in hashes.items():
        if digest(ROOT/name)!=sha:
            raise RuntimeError(f'Source changed during build: {name}')
    outputs={}
    for entry in entries:
        for ext in ('.pdf','.log','.fls','.aux','.out','.toc','.bbl','.blg'):
            item=entry.with_suffix(ext)
            if item.exists():
                dest=output/item.name
                shutil.copy2(item,dest)
                outputs[dest.name]={'sha256':digest(dest),'bytes':dest.stat().st_size}
    record={**plan,'status':'native_passed','outputs':outputs,
            'python':sys.version,'pdflatex':command('pdflatex','--version').splitlines()[0],
            'latexmk':command('latexmk','-v'),'github_run_id':os.environ.get('GITHUB_RUN_ID'),
            'github_run_attempt':os.environ.get('GITHUB_RUN_ATTEMPT'),
            'scope':'Native principal, supporting, archive and complete targets; finite diagnostics, not machine verification of the proofs.',
            'receipt_commit_convention':'This records the built source head. A later artifact-only commit is not claimed to have compiled its own hash.'}
    (output/'RUNTIME_RECEIPT.json').write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'native_passed','source_head':head,'output':str(output)}))


if __name__=='__main__':
    main()
