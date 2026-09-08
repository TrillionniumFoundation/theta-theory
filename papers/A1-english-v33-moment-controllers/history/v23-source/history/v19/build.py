#!/usr/bin/env python3
"""Build the complete v19 manuscript with independently anchored preservation.

Both standalone --prepare-only and validate.py use the same historical
source checks. Identity checks are not certificates of mathematical truth.
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
BASE = 'be8effe038608bef255fa97318a9ee3b4434af2d'
REVIEW = 'e5fff530c95a4f3aa1163a2087838ff2795f052b'
MANIFEST_BLOB = 'f4245151593153b5e8ec77e30449588cdd478dc4'
V17_MANIFEST_BLOB = 'e8870117088145c9db0f71fc38e9be0ff0d27de2'

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def git_blob(data: bytes) -> str:
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()

def verify_history() -> dict:
    archive = ROOT/'history/v18'
    data = (archive/'SOURCE_MANIFEST.json').read_bytes()
    if git_blob(data) != MANIFEST_BLOB:
        raise ValueError('Pinned v18 manifest changed')
    sources = json.loads(data)['files']
    for name, digest in sources.items():
        if sha((archive/name).read_bytes()) != digest:
            raise ValueError('Archived v18 source changed: '+name)
    active = [name for name in sources
              if (name.startswith(('core/','sections/','tests/'))
                  and name != 'sections/introduction.tex')
              or name in {'finite_compiler.py','certified_compiler.py',
                          'construction_contracts.py','references.tex',
                          'references-v9.tex','references-v16.tex','references-v18.tex'}]
    for name in active:
        if sha((ROOT/name).read_bytes()) != sources[name]:
            raise ValueError('Inherited source changed: '+name)
    # This specifically anchors v17's inverse proof, independently of either
    # reconstructed compilation. It closes the standalone-mode observation.
    v17_data = (ROOT/'history/V17_SOURCE_MANIFEST.json').read_bytes()
    if git_blob(v17_data) != V17_MANIFEST_BLOB:
        raise ValueError('Pinned v17 manifest changed')
    inverse = 'sections/operational_reconstruction.tex'
    if sha((ROOT/inverse).read_bytes()) != json.loads(v17_data)['files'][inverse]:
        raise ValueError('Pinned v17 operational inverse changed')
    return {'archived_v18_source_files':len(sources),
            'active_inherited_source_files':len(active),
            'v18_manifest_git_blob':MANIFEST_BLOB,
            'v17_manifest_git_blob':V17_MANIFEST_BLOB,
            'inverse_checked_against_original_v17':True}

def expand(path: Path, root: Path, stack: tuple[Path,...]=()) -> str:
    path=path.resolve()
    if path in stack or not path.is_relative_to(root.resolve()):
        raise ValueError('Cyclic or escaping TeX input: '+str(path))
    text=path.read_text(encoding='utf-8')
    return re.sub(r'\\input\{([^}]+)\}',
                  lambda m: expand(root/(m[1]+'.tex'),root,stack+(path,)),text)

def blocks(text: str):
    proofs=Counter(sha(m.encode()) for m in
                   re.findall(r'\\begin\{proof\}.*?\\end\{proof\}',text,re.S))
    pattern=r'\\begin\{(theorem|lemma|proposition|corollary)\}.*?\\end\{\1\}'
    statements=Counter(sha(m[0].encode()) for m in re.finditer(pattern,text,re.S))
    labels=re.findall(r'\\label\{([^}]+)\}',text)
    if len(labels)!=len(set(labels)):
        raise ValueError('Duplicate labels')
    refs=set(re.findall(r'\\(?:eq)?ref\{([^}]+)\}',text))
    if refs-set(labels):
        raise ValueError('Undefined references: '+str(sorted(refs-set(labels))))
    return proofs,statements,set(labels)

def prepare() -> dict:
    history=verify_history()  # before copying or running any preparer
    out=ROOT/'build';out.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='a1-v18-pinned-') as tmp:
        baseline=Path(tmp)/'manuscript'
        shutil.copytree(ROOT/'history/v18',baseline,
                        ignore=shutil.ignore_patterns('__pycache__'))
        run=subprocess.run([sys.executable,'build.py','--prepare-only'],cwd=baseline,
                           capture_output=True,text=True,timeout=180)
        (out/'baseline-stdout.txt').write_text(run.stdout+run.stderr)
        if run.returncode:
            raise RuntimeError('Pinned v18 preparer failed; see baseline-stdout.txt')
        baseline_text=(baseline/'build/expanded.tex').read_text()
        old_report=json.loads((baseline/'PRESERVATION_REPORT.json').read_text())
        for path in (baseline/'build').glob('*.tex'):
            if path.name!='expanded.tex':
                shutil.copy2(path,out/path.name)
    old_p,old_s,old_l=blocks(baseline_text)
    if (sum(old_p.values()),sum(old_s.values()))!=(99,102):
        raise ValueError('Pinned v18 compiled block count mismatch')
    text=expand(ROOT/'main.tex',ROOT)
    new_p,new_s,new_l=blocks(text)
    if old_p-new_p or old_s-new_s or old_l-new_l:
        raise ValueError('Inherited compiled proof, statement, or label changed')
    if (sum(new_p.values()),sum(new_s.values()))!=(109,112):
        raise ValueError('Expected ten additional complete results and proofs')
    report={'version':19,'submission_basis':BASE,'controlling_review':REVIEW,
            'historical_source_checks':history,
            'retained_v18_proofs_byte_identical':99,
            'retained_v18_statements_byte_identical':102,
            'retained_v18_labels':len(old_l),
            'compiled_proof_blocks':sum(new_p.values()),
            'compiled_statement_blocks':sum(new_s.values()),
            'new_complete_proof_blocks':sum((new_p-old_p).values()),
            'new_complete_statement_blocks':sum((new_s-old_s).values()),
            'all_references_resolved_in_source':True,
            'no_unapproved_proof_deletions':True,
            'inherited_preservation_report':old_report,
            'scope':'Executed source checks, not mathematical proof verification.'}
    (out/'expanded.tex').write_text(text)
    (out/'v18-baseline-expanded.tex').write_text(baseline_text)
    (ROOT/'PRESERVATION_REPORT.json').write_text(json.dumps(report,indent=2)+'\n')
    return report

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--prepare-only',action='store_true')
    args=parser.parse_args();report=prepare()
    if not args.prepare_only:
        (ROOT/'main.pdf').unlink(missing_ok=True)
        for i in range(1,4):
            run=subprocess.run(['pdflatex','-no-shell-escape','-interaction=nonstopmode',
                                '-halt-on-error','main.tex'],cwd=ROOT,capture_output=True,
                               text=True,timeout=180)
            (ROOT/f'build/tex-pass-{i}.txt').write_text(run.stdout+run.stderr)
            if run.returncode:
                raise RuntimeError(f'TeX pass {i} failed')
        log=(ROOT/'main.log').read_text(errors='replace')
        warnings=[x for x in log.splitlines() if 'undefined' in x.lower()
                  or 'Overfull' in x or 'multiply defined' in x.lower()]
        if warnings:
            raise RuntimeError('TeX warnings: '+str(warnings))
        report.update(pdflatex_passes=3,undefined_or_overfull_warnings=0,
                      pdf_sha256=sha((ROOT/'main.pdf').read_bytes()))
        (ROOT/'BUILD_REPORT.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':
    main()
