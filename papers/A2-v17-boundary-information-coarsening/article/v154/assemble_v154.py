#!/usr/bin/env python3
"""Materialize the complete v154 article from the locked, complete v153 source.
No inherited theorem, proof, example or remark is removed or rewritten.
"""
from __future__ import annotations
import argparse, collections, hashlib, json, os, re, subprocess
from pathlib import Path

HERE=Path(__file__).resolve().parent
PREV=HERE.parent/'v153'/'geometry.tex'
REVIEW='52ebb8183433ad398f61958219b2af809f721824'
PREV_HASH='19012076587eb5b91f4b8a82970ec496300a84d9e185261a6ce4291195c25c4c'
ALIASES={'thm:pencil-stack-equivalence-v149':'thm:pencil-stack-equivalence',
         'lem:primitive-pencil-v149':'lem:primitive-pencil'}

def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def run(args: list[str], **kw) -> subprocess.CompletedProcess:
    return subprocess.run(args,check=True,text=True,**kw)

def module(name: str) -> str:
    text=(HERE/name).read_text()
    for a,b in ALIASES.items():
        text=text.replace('{'+a+'}','{'+b+'}')
    return text

def once(text: str, old: str, new: str) -> str:
    if text.count(old)!=1:
        raise ValueError(f'Expected one assembly anchor: {old}')
    return text.replace(old,new,1)

def main() -> None:
    ap=argparse.ArgumentParser();ap.add_argument('--build',action='store_true')
    args=ap.parse_args()
    if sha(PREV)!=PREV_HASH:
        raise RuntimeError('Locked complete v153 source hash does not match')
    old=PREV.read_text();start=old.index('\\begin{abstract}')
    body_start=old.index('% BEGIN PRESERVED PART')
    (HERE/'PREVIOUS_FRONTMATTER_V153.tex').write_text(old[start:body_start])
    pre=old[:start].replace('revision 153','revision 154')
    body=old[body_start:]
    anchor='% BEGIN PRESERVED PART 37-common-divisor-strata-v149.tex'
    body=once(body,anchor,module('moduli-v154.tex')+'\n\\part*{Part II. Divisor incidence and homological fibres}\n\n'+anchor)
    anchor='% BEGIN PRESERVED PART 44-conductor-and-collisions-v152.tex'
    body=once(body,anchor,module('homological-v154.tex')+'\n'+module('formal-details-v154.tex')+'\n'+anchor)
    body=once(body,'\\end{thebibliography}',module('references-v154.tex')+'\n\\end{thebibliography}')
    disclosure='''\\paragraph{Revision 154.}
AI assistance was used for the polarized moduli compatibility,
spectral divisor-fibre construction, homological calculations and
proof expansions. The fixed five-variable Betti table uses exact
computer-assisted rational elimination with its complete finite
inputs recorded. The general theorems rely on the written arguments
and the explicitly attributed classical results, not on regression
counts or source-preservation receipts.\n\n'''
    body=once(body,'\\begin{thebibliography}{99}',disclosure+'\\begin{thebibliography}{99}')
    new=pre+module('front-v154.tex')+'\n'+body
    labels=lambda t:re.findall(r'\\label\{([^}]+)\}',t)
    old_labels=labels(old);new_labels=labels(new)
    missing=sorted(set(old_labels)-set(new_labels))
    duplicate=sorted(k for k,v in collections.Counter(new_labels).items() if v>1)
    block_re=re.compile(r'\\begin\{(theorem|lemma|proposition|corollary|definition|example|remark|proof)\}.*?\\end\{\1\}',re.S)
    old_blocks=collections.Counter(m.group(0) for m in block_re.finditer(old))
    new_blocks=collections.Counter(m.group(0) for m in block_re.finditer(new))
    missing_blocks=old_blocks-new_blocks
    refs=set(re.findall(r'\\(?:eqref|ref|pageref)\{([^}]+)\}',new))
    unresolved=sorted(refs-set(new_labels))
    bib=set(re.findall(r'\\bibitem(?:\[[^]]*\])?\{([^}]+)\}',new))
    cites=set()
    for group in re.findall(r'\\cite(?:\[[^]]*\])?\{([^}]+)\}',new):
        cites.update(x.strip() for x in group.split(','))
    missing_cites=sorted(cites-bib)
    if missing or duplicate or missing_blocks or unresolved or missing_cites:
        raise RuntimeError(json.dumps({'missing_labels':missing,'duplicate_labels':duplicate,'missing_math_blocks':len(missing_blocks),'unresolved_references':unresolved,'missing_citations':missing_cites}))
    (HERE/'geometry.tex').write_text(new)
    preservation={'revision':154,'predecessor_sha256':PREV_HASH,'controlling_review_commit':REVIEW,
        'predecessor_labels':len(old_labels),'current_labels':len(new_labels),
        'missing_predecessor_labels':missing,'duplicate_labels':duplicate,
        'predecessor_math_blocks':sum(old_blocks.values()),
        'all_predecessor_math_blocks_retained_byte_for_byte':not missing_blocks,
        'inherited_source_files_modified':False,
        'frontmatter_rewritten_and_previous_frontmatter_archived':True,
        'new_module_cross_reference_aliases':ALIASES}
    (HERE/'NONDELETION_V154.json').write_text(json.dumps(preservation,indent=2)+'\n')
    receipt=dict(preservation)
    receipt.update({'source_commit':os.environ.get('GITHUB_SHA','local-build'),
        'geometry_source_sha256':sha(HERE/'geometry.tex'),
        'input_sha256':{p.name:sha(p) for p in sorted(HERE.glob('*')) if p.suffix in ('.py','.tex') and p.name!='geometry.tex'},
        'compiled':False,'historical_28_checks_rerun':False,
        'Ballico_1993_full_text_comparison_completed':False,
        'general_proofs_certified_by_computation':False,
        'journal_acceptance_asserted':False})
    if args.build:
        for i in range(1,4):
            with (HERE/f'build-pass-{i}.txt').open('w') as out:
                run(['pdflatex','-interaction=nonstopmode','-halt-on-error','-file-line-error','geometry.tex'],cwd=HERE,stdout=out,stderr=subprocess.STDOUT)
        log=(HERE/'geometry.log').read_text(errors='replace')
        bad=[s for s in ('undefined references','There were undefined','multiply defined','Citation `') if s in log]
        overfull=re.findall(r'Overfull \\hbox \(([^)]+)\)',log)
        if bad or overfull:
            raise RuntimeError(f'Final TeX diagnostics: {bad}; overfull hboxes: {overfull}')
        run(['pdftotext','-layout','geometry.pdf','geometry.txt'],cwd=HERE)
        info=run(['pdfinfo','geometry.pdf'],cwd=HERE,capture_output=True).stdout
        pages=int(re.search(r'^Pages:\s+(\d+)',info,re.M).group(1))
        receipt.update({'compiled':True,'pages':pages,'pdf_sha256':sha(HERE/'geometry.pdf'),
                        'pdf_bytes':(HERE/'geometry.pdf').stat().st_size,
                        'clean_references_and_no_overfull_hboxes':True})
    if (HERE/'EXACT_CHECKS_V154.json').exists():
        receipt['exact_checks_sha256']=sha(HERE/'EXACT_CHECKS_V154.json')
    (HERE/'BUILD_RECEIPT_V154.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))

if __name__=='__main__':
    main()
