#!/usr/bin/env python3
"""Build v18 and check every compiled v17 proof/statement is retained.

The original v17 preparer is run unchanged in a temporary reconstruction.
The resulting baseline is compared against the actual expanded v18 text.
These are source-preservation checks, not mathematical proof verification.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
BASE = '1f3838d89a5820b853d1e4b78194293b23e70bd2'
REVIEW = 'a2adb648c08b3c9e803e916f533605203963ee35'
PINNED = {
    'build_v17.py': '0dceca2b90132610c51554886da34de8d47074a4',
    'V17_main.tex': '2e076299956c8eb6d8e5c8162bd8dd8c62d1309d',
    'V17_introduction.tex': 'b28361a59a6b465888f450aa78e4a76654ed6492',
}

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def git_blob(data: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()

def expand(path: Path, root: Path, stack: tuple[Path, ...] = ()) -> str:
    path = path.resolve()
    if path in stack:
        raise ValueError(f'Cyclic TeX input: {path}')
    if not path.is_relative_to(root.resolve()):
        raise ValueError(f'Input escapes manuscript: {path}')
    text = path.read_text(encoding='utf-8')
    return re.sub(r'\\input\{([^}]+)\}',
                  lambda m: expand(root/(m[1]+'.tex'), root, stack+(path,)), text)

def blocks(text: str) -> tuple[Counter, Counter, set[str]]:
    proofs = Counter(sha(m.encode()) for m in
                     re.findall(r'\\begin\{proof\}.*?\\end\{proof\}', text, re.S))
    pattern = r'\\begin\{(theorem|lemma|proposition|corollary)\}.*?\\end\{\1\}'
    statements = Counter(sha(m[0].encode()) for m in re.finditer(pattern, text, re.S))
    labels = re.findall(r'\\label\{([^}]+)\}', text)
    if len(labels) != len(set(labels)):
        raise ValueError('Duplicate labels in compiled source')
    refs = set(re.findall(r'\\(?:eq)?ref\{([^}]+)\}', text))
    if refs-set(labels):
        raise ValueError('Undefined source references: '+str(sorted(refs-set(labels))))
    return proofs, statements, set(labels)

def prepare() -> dict:
    out = ROOT/'build'; out.mkdir(exist_ok=True)
    for name, expected in PINNED.items():
        if git_blob((ROOT/'history'/name).read_bytes()) != expected:
            raise ValueError('Pinned baseline file changed: '+name)
    with tempfile.TemporaryDirectory(prefix='a1-v17-baseline-') as temporary:
        baseline = Path(temporary)/'manuscript'
        shutil.copytree(ROOT, baseline,
                        ignore=shutil.ignore_patterns('build','validation','__pycache__',
                                                     '*.pdf','*.aux','*.log','*.out'))
        shutil.copy2(baseline/'history/build_v17.py', baseline/'build.py')
        shutil.copy2(baseline/'history/V17_main.tex', baseline/'main.tex')
        shutil.copy2(baseline/'history/V17_introduction.tex', baseline/'sections/introduction.tex')
        run = subprocess.run([sys.executable,'build.py','--prepare-only'], cwd=baseline,
                             capture_output=True, text=True, timeout=180)
        (out/'baseline-stdout.txt').write_text(run.stdout+run.stderr)
        if run.returncode:
            raise RuntimeError('Unchanged v17 preparer failed; see baseline-stdout.txt')
        baseline_text = (baseline/'build/expanded.tex').read_text()
        old_report = json.loads((baseline/'PRESERVATION_REPORT.json').read_text())
        for path in (baseline/'build').glob('*.tex'):
            if path.name != 'expanded.tex':
                shutil.copy2(path, out/path.name)
    before_p, before_s, before_l = blocks(baseline_text)
    if (sum(before_p.values()),sum(before_s.values())) != (88,91):
        raise ValueError('Unexpected v17 compiled block counts')
    text = expand(ROOT/'main.tex', ROOT)
    current_p, current_s, current_l = blocks(text)
    if before_p-current_p or before_s-current_s or before_l-current_l:
        raise ValueError('A v17 compiled proof, statement, or label was lost or changed')
    if (sum(current_p.values()),sum(current_s.values())) != (99,102):
        raise ValueError('Expected eleven new complete results and eleven proofs')
    report = {
        'version':18, 'submission_basis':BASE, 'controlling_review':REVIEW,
        'baseline_preparer_git_blob':PINNED['build_v17.py'],
        'retained_v17_proofs_byte_identical':88,
        'retained_v17_statements_byte_identical':91,
        'retained_v17_labels':len(before_l),
        'compiled_proof_blocks':sum(current_p.values()),
        'compiled_statement_blocks':sum(current_s.values()),
        'new_complete_proof_blocks':sum((current_p-before_p).values()),
        'new_complete_statement_blocks':sum((current_s-before_s).values()),
        'all_references_resolved_in_source':True,
        'no_unapproved_proof_deletions':True,
        'inherited_preservation_report':old_report,
        'scope':'Executed source identity and inclusion checks; not proof verification.'}
    (out/'expanded.tex').write_text(text)
    (out/'baseline-expanded.tex').write_text(baseline_text)
    (ROOT/'PRESERVATION_REPORT.json').write_text(json.dumps(report,indent=2)+'\n')
    return report

def main() -> None:
    parser=argparse.ArgumentParser()
    parser.add_argument('--prepare-only',action='store_true')
    args=parser.parse_args()
    report=prepare()
    if not args.prepare_only:
        (ROOT/'main.pdf').unlink(missing_ok=True)
        for number in range(1,4):
            run=subprocess.run(['pdflatex','-no-shell-escape','-interaction=nonstopmode',
                                '-halt-on-error','main.tex'],cwd=ROOT,
                               capture_output=True,text=True,timeout=180)
            (ROOT/f'build/tex-pass-{number}.txt').write_text(run.stdout+run.stderr)
            if run.returncode:
                raise RuntimeError(f'TeX pass {number} failed')
        log=(ROOT/'main.log').read_text(errors='replace')
        bad=[line for line in log.splitlines()
             if 'undefined' in line.lower() or 'Overfull' in line
             or 'multiply defined' in line.lower()]
        if bad:
            raise RuntimeError('TeX warnings: '+str(bad))
        report.update(pdflatex_passes=3,undefined_or_overfull_warnings=0,
                      pdf_sha256=sha((ROOT/'main.pdf').read_bytes()))
        (ROOT/'BUILD_REPORT.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':
    main()
