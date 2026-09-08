#!/usr/bin/env python3
"""Build v23; preserve all v22 formal blocks and verify the pinned source chain.

Source preservation is an execution check, not a certificate of mathematical truth.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib,json,re,shutil,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
BASELINE=ROOT.parent/'A1-english-v22'
BASE='5f745a863dac637496bd5eb20341f12cecb71ab1'
REVIEW='325e89b9c012830cbd219fec0cff7c52b8e8d321'
MANIFEST_BLOB='a2fea657ca31b1e824cff9393f02c4aa78c2ad54'
CHANGED={'main.tex','sections/introduction.tex','sections/algebra_multistep.tex',
         'build.py','validate.py','manifest.py','README.md','RESPONSE_TO_REFEREE.md'}
def sha(b): return hashlib.sha256(b).hexdigest()
def git_blob(b): return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def verify_history():
    data=(BASELINE/'SOURCE_MANIFEST.json').read_bytes()
    if git_blob(data)!=MANIFEST_BLOB: raise ValueError('Pinned v22 manifest changed')
    files=json.loads(data)['files']
    for name,digest in files.items():
        if sha((BASELINE/name).read_bytes())!=digest:
            raise ValueError('Pinned v22 source changed: '+name)
        if name not in CHANGED and sha((ROOT/name).read_bytes())!=digest:
            raise ValueError('Inherited source changed: '+name)
    return {'v22_commit':BASE,'v22_manifest_git_blob':MANIFEST_BLOB,
            'verified_v22_source_files':len(files),
            'unchanged_inherited_source_files':len(files)-len(CHANGED),
            'changed_source_originals_preserved_in':'../A1-english-v22/'}
def expand(path,root,stack=()):
    path=path.resolve();root=root.resolve()
    if path in stack or not path.is_relative_to(root):
        raise ValueError('Cyclic or escaping TeX input')
    text=path.read_text()
    return re.sub(r'\\input\{([^}]+)\}',
        lambda m:expand(root/(m[1]+'.tex'),root,stack+(path,)),text)
def formal_blocks(text):
    proofs=Counter(sha(m.encode()) for m in re.findall(
        r'\\begin\{proof\}.*?\\end\{proof\}',text,re.S))
    statements=Counter(sha(m[0].encode()) for m in re.finditer(
        r'\\begin\{(theorem|lemma|proposition|corollary)\}.*?\\end\{\1\}',text,re.S))
    return proofs,statements
def labels_and_refs(text):
    labels=re.findall(r'\\label\{([^}]+)\}',text)
    duplicate=[k for k,v in Counter(labels).items() if v>1]
    missing=set(re.findall(r'\\(?:eq)?ref\{([^}]+)\}',text))-set(labels)
    cites=set()
    for m in re.finditer(r'\\cite(?:\[[^]]*\])*\{([^}]+)\}',text):
        cites.update(x.strip() for x in m[1].split(','))
    bib=set(re.findall(r'\\bibitem(?:\[[^]]*\])?\{([^}]+)\}',text))
    if duplicate or missing or cites-bib:
        raise ValueError(f'Reference errors: {duplicate}; {missing}; {cites-bib}')
    return set(labels)
def prepare():
    history=verify_history();out=ROOT/'build';out.mkdir(exist_ok=True)
    # Rebuild generated inputs from immutable sibling sources in a temporary copy.
    # Never edit or execute baseline preparation in the published baseline itself.
    with tempfile.TemporaryDirectory(prefix='a1-v23-') as tmp:
        papers=Path(tmp)/'papers';papers.mkdir()
        for version in (20,21,22):
            name=f'A1-english-v{version}'
            shutil.copytree(ROOT.parent/name,papers/name,ignore=shutil.ignore_patterns(
                '__pycache__','build','validation','main.pdf','main.log','main.aux','main.out'))
        baseline=papers/'A1-english-v22'
        p=subprocess.run([sys.executable,'build.py','--prepare-only'],cwd=baseline,
                         capture_output=True,text=True,timeout=300)
        (out/'baseline-stdout.txt').write_text(p.stdout+p.stderr)
        if p.returncode: raise RuntimeError('Pinned v22 preparation failed')
        old=(baseline/'build/expanded.tex').read_text()
        for file in (baseline/'build').glob('*.tex'):
            if 'expanded' not in file.name: shutil.copyfile(file,out/file.name)
    oldp,olds=formal_blocks(old)
    if (sum(oldp.values()),sum(olds.values()))!=(127,129):
        raise ValueError('Pinned v22 formal-block counts changed')
    text=expand(ROOT/'main.tex',ROOT);newp,news=formal_blocks(text)
    oldlabels=labels_and_refs(old);newlabels=labels_and_refs(text)
    if oldp-newp or olds-news or oldlabels-newlabels:
        raise ValueError('Inherited formal statement, proof, or label missing/changed')
    algebra=(ROOT/'sections/algebra_multistep.tex').read_text()
    for marker in ('def:algebra-risks','eq:algebra-risk-causal-average',
                   'eq:algebra-risk-causal-worst','prop:algebra-saturation'):
        if marker not in algebra: raise ValueError('Missing E22 risk/scope addition')
    direct=(ROOT/'sections/algebra_saturated_geometry.tex').read_text()
    for marker in ('eq:algebra-direct-cover','eq:algebra-direct-metric',
                   'eq:algebra-saturated-sandwich'):
        if marker not in direct: raise ValueError('Missing direct proof component')
    if '\\input{sections/algebra_transfer_alternative}' not in (ROOT/'main.tex').read_text():
        raise ValueError('Alternative proof not active')
    report={'version':23,'submission_basis':BASE,'controlling_review':REVIEW,
       'historical_source_checks':history,
       'v22_statements_preserved_byte_identical':sum(olds.values()),
       'v22_proofs_preserved_byte_identical':sum(oldp.values()),
       'v22_labels_preserved':len(oldlabels),
       'compiled_statement_blocks':sum(news.values()),
       'compiled_proof_blocks':sum(newp.values()),
       'new_statement_blocks':sum((news-olds).values()),
       'new_proof_blocks':sum((newp-oldp).values()),
       'all_source_references_and_citations_resolved':True,
       'no_inherited_formal_content_deleted_or_weakened':True,
       'scope':'Executed source preservation and reference checks, not proof certification.'}
    (out/'expanded.tex').write_text(text)
    (out/'v22-baseline-expanded.tex').write_text(old)
    (ROOT/'PRESERVATION_REPORT.json').write_text(json.dumps(report,indent=2)+'\n')
    return report
def main():
    p=argparse.ArgumentParser();p.add_argument('--prepare-only',action='store_true');args=p.parse_args()
    report=prepare()
    if not args.prepare_only:
        (ROOT/'main.pdf').unlink(missing_ok=True)
        for n in range(1,4):
            r=subprocess.run(['pdflatex','-no-shell-escape','-interaction=nonstopmode',
                '-halt-on-error','main.tex'],cwd=ROOT,capture_output=True,text=True,timeout=300)
            (ROOT/f'build/tex-pass-{n}.txt').write_text(r.stdout+r.stderr)
            if r.returncode: raise RuntimeError('TeX pass failed: '+str(n))
        log=(ROOT/'main.log').read_text(errors='replace')
        bad=[s for s in log.splitlines() if 'undefined' in s.lower() or
             'Overfull' in s or 'multiply defined' in s.lower()]
        if bad: raise RuntimeError('TeX warnings: '+repr(bad))
        info=subprocess.run(['pdfinfo','main.pdf'],cwd=ROOT,check=True,capture_output=True,text=True)
        pages=int(next(s.split(':',1)[1] for s in info.stdout.splitlines() if s.startswith('Pages:')))
        report.update(pdflatex_passes=3,undefined_or_overfull_warnings=0,pdf_pages=pages,
                      pdf_sha256=sha((ROOT/'main.pdf').read_bytes()))
        (ROOT/'BUILD_REPORT.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
