#!/usr/bin/env python3
"""Prepare and compile the full v21 manuscript against the pinned v20 source.

This independently checks source identity and the single reviewed formal edit.
It does not certify mathematical correctness. Run from the repository, where
papers/A1-english-v20 is the immutable published sibling.
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
BASE='6f103ad252d7c65f140720f4095585026f7bb1b9'
REVIEW='078f34222b00797203cdf6dd421eab9f9f428c59'
MANIFEST_BLOB='db8414e9ec13e862a7af091c89417fdd2aa6207d'
BASELINE=ROOT.parent/'A1-english-v20'
CHANGED={'main.tex','sections/introduction.tex','sections/exact_kernels.tex',
         'build.py','validate.py','manifest.py','README.md','RESPONSE_TO_REFEREE.md'}
# Compiled statement/proof blocks are compared separately. Only the E20.1
# citation and its feasibility paragraph have a registered replacement.

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def git_blob(data: bytes) -> str:
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()

def apply_reviewed_edits(text: str) -> str:
    edits=json.loads((ROOT/'REVISION_EDITS.json').read_text())
    for before,after in edits['replacements']:
        if text.count(before)!=1:
            raise ValueError('Registered E20.1 edit has no unique source match')
        text=text.replace(before,after,1)
    return text

def verify_history() -> dict:
    data=(BASELINE/'SOURCE_MANIFEST.json').read_bytes()
    if git_blob(data)!=MANIFEST_BLOB:
        raise ValueError('Pinned v20 source manifest changed')
    files=json.loads(data)['files']
    for name,digest in files.items():
        if sha((BASELINE/name).read_bytes())!=digest:
            raise ValueError('Pinned v20 source changed: '+name)
        if name not in CHANGED and sha((ROOT/name).read_bytes())!=digest:
            raise ValueError('Inherited source changed: '+name)
    target='sections/exact_kernels.tex'
    if (ROOT/target).read_text()!=apply_reviewed_edits((BASELINE/target).read_text()):
        raise ValueError('Unregistered exact-kernel edit')
    for name in CHANGED:
        archived=ROOT/'history/v20-editorial'/name.replace('/','__')
        if sha(archived.read_bytes())!=sha((BASELINE/name).read_bytes()):
            raise ValueError('Archived v20 front matter changed: '+name)
    v17=(ROOT/'history/V17_SOURCE_MANIFEST.json').read_bytes()
    if git_blob(v17)!='e8870117088145c9db0f71fc38e9be0ff0d27de2':
        raise ValueError('Pinned original v17 manifest changed')
    inverse='sections/operational_reconstruction.tex'
    if sha((ROOT/inverse).read_bytes())!=json.loads(v17)['files'][inverse]:
        raise ValueError('Original v17 inverse changed')
    return {'pinned_v20_commit':BASE,'pinned_v20_manifest_git_blob':MANIFEST_BLOB,
            'verified_v20_source_files':len(files),
            'unchanged_active_inherited_sources':len(files)-len(CHANGED),
            'original_v17_inverse_independently_anchored':True,
            'exact_kernel_edits_match_registered_replacements':True}

def expand(path: Path, root: Path, stack=()) -> str:
    path=path.resolve();root=root.resolve()
    if path in stack or not path.is_relative_to(root):
        raise ValueError('Cyclic or escaping TeX input: '+str(path))
    text=path.read_text(encoding='utf-8')
    return re.sub(r'\\input\{([^}]+)\}',
                  lambda m:expand(root/(m[1]+'.tex'),root,stack+(path,)),text)

def formal_blocks(text: str):
    proofs=Counter(sha(m.encode()) for m in re.findall(
        r'\\begin\{proof\}.*?\\end\{proof\}',text,re.S))
    pat=r'\\begin\{(theorem|lemma|proposition|corollary)\}.*?\\end\{\1\}'
    statements=Counter(sha(m[0].encode()) for m in re.finditer(pat,text,re.S))
    return proofs,statements

def labels_and_refs(text: str):
    labels=re.findall(r'\\label\{([^}]+)\}',text)
    if len(labels)!=len(set(labels)):
        raise ValueError('Duplicate labels: '+str([k for k,v in Counter(labels).items() if v>1]))
    refs=set(re.findall(r'\\(?:eq)?ref\{([^}]+)\}',text))
    if refs-set(labels):
        raise ValueError('Undefined references: '+str(sorted(refs-set(labels))))
    cites=set()
    for m in re.finditer(r'\\cite(?:\[[^]]*\])*\{([^}]+)\}',text):
        cites.update(s.strip() for s in m[1].split(','))
    bib=set(re.findall(r'\\bibitem(?:\[[^]]*\])?\{([^}]+)\}',text))
    if cites-bib:
        raise ValueError('Missing bibliography keys: '+str(sorted(cites-bib)))
    return set(labels)

def demote(text: str) -> str:
    levels={'section':'subsection','subsection':'subsubsection','subsubsection':'paragraph'}
    return re.sub(r'\\(section|subsection|subsubsection)(\*?)\{',
                  lambda m:'\\'+levels[m[1]]+m[2]+'{',text)

def prepare() -> dict:
    history=verify_history()
    out=ROOT/'build';out.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='a1-v20-anchor-') as tmp:
        baseline=Path(tmp)/'baseline'
        shutil.copytree(BASELINE,baseline,ignore=shutil.ignore_patterns(
            '__pycache__','main.pdf','main.log','main.aux','main.out','validation','build'))
        run=subprocess.run([sys.executable,'build.py','--prepare-only'],cwd=baseline,
                           capture_output=True,text=True,timeout=240)
        (out/'baseline-stdout.txt').write_text(run.stdout+run.stderr)
        if run.returncode:
            raise RuntimeError('Pinned v20 preparer failed; inspect baseline-stdout.txt')
        baseline_text=(baseline/'build/expanded.tex').read_text()
        prior_report=json.loads((baseline/'PRESERVATION_REPORT.json').read_text())
        for path in (baseline/'build').glob('*.tex'):
            if path.name not in {'expanded.tex','v19-baseline-expanded.tex','baseline-expanded.tex'}:
                shutil.copy2(path,out/path.name)
    old_p,old_s=formal_blocks(baseline_text)
    old_l=labels_and_refs(baseline_text)
    if (sum(old_p.values()),sum(old_s.values()))!=(114,117):
        raise ValueError('Pinned v20 formal-block count mismatch')
    amended=apply_reviewed_edits(baseline_text)
    amended_p,amended_s=formal_blocks(amended)
    collision=(ROOT/'core/06b_collision_geometry.tex').read_text()
    i=collision.index(r'\subsection{The global attainable law}')
    j=collision.index(r'\begin{corollary}[Intrinsic bit law]')
    first=collision[:i]
    old_intro=first[first.index('\n')+1:first.index(r'\subsection{Calibration chamber')]
    first=first.replace(old_intro,'\nThe formal future labels determine a uniformly conditioned Newton flag.\nThe following acquisition argument verifies its positive mass before\nwe apply the geometric-to-causal transfer theorem.\n\n',1)
    (out/'collision_flags.tex').write_text(first)
    (out/'collision_direct.tex').write_text(collision[i:j])
    (out/'collision_consequences.tex').write_text(collision[j:])
    groups={
      'app_structural':['sections/structural_classification','sections/affine_geometry'],
      'app_pairings':['sections/kernel_feasibility','sections/universal_attainment',
          'sections/rectangular_attainment','sections/exact_kernels',
          'sections/finite_pairing_comparison','sections/positive_history',
          'sections/covariance_degenerations'],
      'app_additional_geometry':['sections/circular','sections/operational_reconstruction',
          'sections/directional_geometry','sections/uncertainty_geometry'],
      'app_complete_routes':['build/collision_direct','build/05_confluence',
          'build/06_streaming','build/06a_attainable_filtration'],
      'app_decisions':['core/04_observation_algebra','core/07_uniform_resolution',
          'core/08_sequential_value','core/09_common_risk'],
      'app_effective':['sections/effective','build/effective_overview',
          'sections/certified_resources','sections/construction_stability',
          'sections/request_conformance'],
      'app_comparison':['sections/pairing_comparison','sections/structural_comparison',
          'sections/comparison']}
    for name,paths in groups.items():
        parts=[]
        for path in paths:
            text=expand(ROOT/(path+'.tex'),ROOT)
            if path=='build/collision_direct' or name=='app_comparison':
                # The only heading was already a subsection, under this appendix.
                parts.append(text)
            else:
                parts.append(demote(text))
        (out/(name+'.tex')).write_text('\n\n'.join(parts))
    text=expand(ROOT/'main.tex',ROOT)
    new_p,new_s=formal_blocks(text);new_l=labels_and_refs(text)
    if amended_p-new_p or amended_s-new_s or old_l-new_l:
        raise ValueError('A retained proof, statement, or source label is missing')
    unchanged_p=sum((old_p & new_p).values());unchanged_s=sum((old_s & new_s).values())
    if unchanged_p!=113 or unchanged_s!=116:
        raise ValueError('Unexpected unregistered formal changes')
    report={'version':21,'submission_basis':BASE,'controlling_review':REVIEW,
        'historical_source_checks':history,
        'retained_v20_proofs_byte_identical':unchanged_p,
        'retained_v20_statements_byte_identical':unchanged_s,
        'reviewed_exact_kernel_proof_paragraph_replaced':1,
        'reviewed_exact_kernel_statement_citation_replaced':1,
        'retained_v20_labels':len(old_l),
        'compiled_proof_blocks':sum(new_p.values()),
        'compiled_statement_blocks':sum(new_s.values()),
        'new_complete_proofs':sum((new_p-amended_p).values()),
        'new_complete_statements':sum((new_s-amended_s).values()),
        'all_source_references_and_citations_resolved':True,
        'no_unapproved_proof_or_statement_deletions':True,
        'appendix_sources':groups,
        'inherited_preservation_report':prior_report,
        'scope':'Executed identity/dependency checks, not mathematical proof verification.'}
    (out/'expanded.tex').write_text(text)
    (out/'v20-baseline-expanded.tex').write_text(baseline_text)
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
                '-halt-on-error','main.tex'],cwd=ROOT,capture_output=True,text=True,timeout=240)
            (ROOT/f'build/tex-pass-{i}.txt').write_text(run.stdout+run.stderr)
            if run.returncode:
                raise RuntimeError(f'TeX pass {i} failed; inspect build/tex-pass-{i}.txt')
        log=(ROOT/'main.log').read_text(errors='replace')
        bad=[x for x in log.splitlines() if 'undefined' in x.lower() or
             'Overfull' in x or 'multiply defined' in x.lower()]
        if bad:
            raise RuntimeError('TeX warnings: '+str(bad))
        info=subprocess.run(['pdfinfo','main.pdf'],cwd=ROOT,check=True,capture_output=True,text=True)
        pages=int(next(x.split(':',1)[1] for x in info.stdout.splitlines() if x.startswith('Pages:')))
        report.update(pdflatex_passes=3,undefined_or_overfull_warnings=0,pdf_pages=pages,
                      pdf_sha256=sha((ROOT/'main.pdf').read_bytes()))
        (ROOT/'BUILD_REPORT.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':
    main()
