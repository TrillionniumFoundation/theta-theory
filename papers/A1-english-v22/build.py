#!/usr/bin/env python3
"""Build v22 from a pinned v21 baseline; check preservation and registered edits.

These are source-identity and dependency checks, not proof certification.
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

ROOT=Path(__file__).resolve().parent
BASELINE=ROOT.parent/'A1-english-v21'
BASE='7c44bdccc91667c583b5d5cbcff3f8d9160a57d6'
REVIEW='36910a7c6fd08e5ad2e8e10db7c2d8c71c463de8'
MANIFEST_BLOB='14d877c7db051926fe461ccfbe007093a786e860'
CHANGED={'main.tex','sections/introduction.tex','build.py','validate.py',
         'manifest.py','README.md','RESPONSE_TO_REFEREE.md'}

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def git_blob(data: bytes) -> str:
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()

def verify_history() -> dict:
    data=(BASELINE/'SOURCE_MANIFEST.json').read_bytes()
    if git_blob(data)!=MANIFEST_BLOB:
        raise ValueError('Pinned v21 manifest changed')
    files=json.loads(data)['files']
    for name,digest in files.items():
        if sha((BASELINE/name).read_bytes())!=digest:
            raise ValueError('Pinned v21 source changed: '+name)
        if name not in CHANGED and sha((ROOT/name).read_bytes())!=digest:
            raise ValueError('Inherited source changed: '+name)
    for name in CHANGED|{'SOURCE_MANIFEST.json'}:
        archive=ROOT/'history/v21-editorial'/name.replace('/','__')
        if archive.read_bytes()!=(BASELINE/name).read_bytes():
            raise ValueError('Archived v21 source changed: '+name)
    return {'v21_commit':BASE,'v21_manifest_git_blob':MANIFEST_BLOB,
            'verified_v21_source_files':len(files),
            'unchanged_inherited_sources':len(files)-len(CHANGED),
            'archived_replaced_editorial_and_build_sources':len(CHANGED)+1}

def expand(path: Path, root: Path, stack=()) -> str:
    path=path.resolve();root=root.resolve()
    if path in stack or not path.is_relative_to(root):
        raise ValueError('Cyclic or escaping input: '+str(path))
    text=path.read_text(encoding='utf-8')
    return re.sub(r'\\input\{([^}]+)\}',
        lambda m:expand(root/(m[1]+'.tex'),root,stack+(path,)),text)

def formal_blocks(text: str):
    proofs=Counter(sha(m.encode()) for m in re.findall(
        r'\\begin\{proof\}.*?\\end\{proof\}',text,re.S))
    statements=Counter(sha(m[0].encode()) for m in re.finditer(
        r'\\begin\{(theorem|lemma|proposition|corollary)\}.*?\\end\{\1\}',text,re.S))
    return proofs,statements

def labels_and_refs(text: str):
    labels=re.findall(r'\\label\{([^}]+)\}',text)
    duplicate=[k for k,v in Counter(labels).items() if v>1]
    if duplicate:raise ValueError('Duplicate labels: '+repr(duplicate))
    missing=set(re.findall(r'\\(?:eq)?ref\{([^}]+)\}',text))-set(labels)
    if missing:raise ValueError('Undefined references: '+repr(sorted(missing)))
    cites=set()
    for m in re.finditer(r'\\cite(?:\[[^]]*\])*\{([^}]+)\}',text):
        cites.update(t.strip() for t in m[1].split(','))
    bib=set(re.findall(r'\\bibitem(?:\[[^]]*\])?\{([^}]+)\}',text))
    if cites-bib:raise ValueError('Missing citations: '+repr(sorted(cites-bib)))
    return set(labels)

def route_edits(text: str) -> str:
    for before,after in json.loads((ROOT/'REVISION_EDITS_V22.json').read_text())['replacements']:
        if text.count(before)!=1:raise ValueError('Nonunique registered E21.2 edit')
        text=text.replace(before,after,1)
    return text

def prepare() -> dict:
    history=verify_history()
    out=ROOT/'build';out.mkdir(exist_ok=True)
    # Reconstruct generated v21 sources rather than trusting an old build directory.
    # The sibling v20 anchor is copied, not edited or run in place.
    with tempfile.TemporaryDirectory(prefix='a1-v22-baseline-') as tmp:
        papers=Path(tmp)/'papers';papers.mkdir()
        for name in ('A1-english-v20','A1-english-v21'):
            shutil.copytree(ROOT.parent/name,papers/name,ignore=shutil.ignore_patterns(
                '__pycache__','build','validation','main.pdf','main.log','main.aux','main.out'))
        baseline=papers/'A1-english-v21'
        result=subprocess.run([sys.executable,'build.py','--prepare-only'],cwd=baseline,
                              capture_output=True,text=True,timeout=240)
        (out/'baseline-stdout.txt').write_text(result.stdout+result.stderr)
        if result.returncode:raise RuntimeError('Pinned v21 preparation failed')
        baseline_text=(baseline/'build/expanded.tex').read_text()
        prior_report=json.loads((baseline/'PRESERVATION_REPORT.json').read_text())
        for path in (baseline/'build').glob('*.tex'):
            if 'expanded' not in path.name:
                shutil.copyfile(path,out/path.name)
    old_p,old_s=formal_blocks(baseline_text)
    if (sum(old_p.values()),sum(old_s.values()))!=(120,122):
        raise ValueError('Pinned v21 formal-block counts changed')
    original=(out/'collision_consequences.tex').read_text()
    (out/'collision_consequences.tex').write_text(route_edits(original))
    expected_p,expected_s=formal_blocks(route_edits(baseline_text))
    text=expand(ROOT/'main.tex',ROOT)
    new_p,new_s=formal_blocks(text)
    old_labels=labels_and_refs(baseline_text);new_labels=labels_and_refs(text)
    if expected_p-new_p or expected_s-new_s or old_labels-new_labels:
        raise ValueError('Retained mathematical content or label missing')
    same_p=sum((old_p&new_p).values());same_s=sum((old_s&new_s).values())
    if (same_p,same_s)!=(118,122):
        raise ValueError('Unregistered formal-block edits')
    intro=(ROOT/'sections/introduction.tex').read_text()
    for definition in ('I=[l,u]=[0,1]','D=a_{r-1}','h_A(m)=|mA|','0A=\\{0\\}'):
        if definition not in intro:raise ValueError('Missing E21.1 definition: '+definition)
    if '19th Scandinavian' in (ROOT/'references-v22.tex').read_text():
        raise ValueError('E21.3 metadata not corrected')
    if '\\ref{thm:intrinsic-checkpoint}' in (out/'collision_consequences.tex').read_text():
        raise ValueError('E21.2 consequence still uses alternative route')
    report={'version':22,'submission_basis':BASE,'controlling_review':REVIEW,
      'historical_source_checks':history,'retained_v21_proofs_byte_identical':same_p,
      'retained_v21_statements_byte_identical':same_s,'citation_only_proofs_amended':2,
      'retained_v21_labels':len(old_labels),'compiled_proof_blocks':sum(new_p.values()),
      'compiled_statement_blocks':sum(new_s.values()),
      'new_complete_proofs':sum((new_p-expected_p).values()),
      'new_complete_statements':sum((new_s-expected_s).values()),
      'all_source_references_and_citations_resolved':True,
      'no_unregistered_mathematical_deletions':True,'setup_symbols_checked':True,
      'inherited_preservation_report':prior_report,
      'scope':'Executed source-identity and dependency checks, not mathematical proof certification.'}
    (out/'expanded.tex').write_text(text)
    (out/'v21-baseline-expanded.tex').write_text(baseline_text)
    (ROOT/'PRESERVATION_REPORT.json').write_text(json.dumps(report,indent=2)+'\n')
    return report

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--prepare-only',action='store_true')
    args=parser.parse_args();report=prepare()
    if not args.prepare_only:
        (ROOT/'main.pdf').unlink(missing_ok=True)
        for i in range(1,4):
            result=subprocess.run(['pdflatex','-no-shell-escape','-interaction=nonstopmode',
                '-halt-on-error','main.tex'],cwd=ROOT,capture_output=True,text=True,timeout=240)
            (ROOT/f'build/tex-pass-{i}.txt').write_text(result.stdout+result.stderr)
            if result.returncode:raise RuntimeError('TeX pass failed: '+str(i))
        log=(ROOT/'main.log').read_text(errors='replace')
        bad=[s for s in log.splitlines() if 'undefined' in s.lower() or
             'Overfull' in s or 'multiply defined' in s.lower()]
        if bad:raise RuntimeError('TeX warnings: '+repr(bad))
        info=subprocess.run(['pdfinfo','main.pdf'],cwd=ROOT,check=True,capture_output=True,text=True)
        pages=int(next(s.split(':',1)[1] for s in info.stdout.splitlines() if s.startswith('Pages:')))
        report.update(pdflatex_passes=3,undefined_or_overfull_warnings=0,pdf_pages=pages,
                      pdf_sha256=sha((ROOT/'main.pdf').read_bytes()))
        (ROOT/'BUILD_REPORT.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
