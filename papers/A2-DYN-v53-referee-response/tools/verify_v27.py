#!/usr/bin/env python3
"""Exact source replay and finite diagnostics, not continuum certification."""
from __future__ import annotations
from pathlib import Path
import argparse,hashlib,json,os,re
import verify_v26 as old
from check_window_events import finite_checks
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT.parent/'A2-DYN-v26-referee-response'
BASE_TREE='6101fe93f514d9586658d748e08a0ffd6c610044'
REPORT='reviews/a2-dyn-v26-external-top4-review-2026-10-07/REFEREE_REPORT.md'
REPORT_BLOB='f75e48fa7276be7be654c61afe3cc276ba44d514'
ordinary=old.ordinary
tree_hash=old.tree_hash

def require(ok: bool,message: str)->None:
    if not ok:raise RuntimeError(message)

def digest(p: Path)->str:return hashlib.sha256(p.read_bytes()).hexdigest()

def source_checks(allow_missing_report=False)->dict:
    require(not(allow_missing_report and os.environ.get('GITHUB_ACTIONS')),'report skip forbidden in Actions')
    man=json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())
    ledger=json.loads((ROOT/'INHERITED_EDITS.json').read_text())
    require(man['revision']==ledger['revision']==27,'revision')
    require(tree_hash(BASE).hex()==BASE_TREE==man['baseline_paper_tree'],'baseline tree')
    require({p.relative_to(BASE).as_posix():digest(p) for p in ordinary(BASE)}==man['baseline_sha256'],'complete baseline hashes')
    bypath={}
    for edit in ledger['edits']:bypath.setdefault(edit['path'],[]).append(edit)
    require(len(ledger['edits'])==6 and set(bypath)=={'main.tex','references.tex'},'exact edit scope')
    for path,edits in bypath.items():
        text=(BASE/path).read_text()
        for e in edits:
            require(text.count(e['before'])==1,'nonunique inherited edit '+path)
            text=text.replace(e['before'],e['after'],1)
        require(text.encode()==(ROOT/path).read_bytes(),'edit replay '+path)
    cores=sorted((BASE/'core').glob('*.tex'));scripts=sorted((BASE/'tools').glob('*.py'))
    require(len(cores)==56 and len(scripts)==52,'baseline source counts')
    for p in cores+scripts:
        require(p.read_bytes()==(ROOT/p.relative_to(BASE)).read_bytes(),'changed inherited file '+p.name)
    actual={p.relative_to(ROOT).as_posix():digest(p) for p in ordinary(ROOT) if p.name!='SOURCE_MANIFEST.json'}
    require(actual==man['source_sha256'],'actual manifest hashes')
    main=(ROOT/'main.tex').read_text()
    require('October 7, 2026. A2-DYN, revision 27' in main,'article identity')
    inputs=re.findall(r'\\input\{(core/[^}]+)\}',main)
    require(len(inputs)==len(set(inputs))==58,'core count')
    require({x+'.tex' for x in inputs}=={p.relative_to(ROOT).as_posix() for p in (ROOT/'core').glob('*.tex')},'omitted core')
    tex=main+'\n'+'\n'.join((ROOT/(x+'.tex')).read_text() for x in inputs)
    oldtex=(BASE/'main.tex').read_text()+'\n'+'\n'.join(p.read_text() for p in cores)
    labels=re.findall(r'\\label\{([^}]+)\}',tex);oldlabels=set(re.findall(r'\\label\{([^}]+)\}',oldtex))
    require(len(labels)==len(set(labels)) and oldlabels<=set(labels),'duplicate or deleted label')
    refs=set(re.findall(r'\\(?:ref|eqref|pageref|autoref)\{([^}]+)\}',tex))
    require(refs<=set(labels),'unresolved references: '+str(refs-set(labels)))
    bib=(ROOT/'references.tex').read_text();oldbib=(BASE/'references.tex').read_text()
    bibitems=set(re.findall(r'\\bibitem\{([^}]+)\}',bib))
    require(set(re.findall(r'\\bibitem\{([^}]+)\}',oldbib))<=bibitems,'removed bibliography item')
    cites=set()
    for group in re.findall(r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}',tex):cites.update(s.strip() for s in group.split(','))
    require(cites<=bibitems,'missing citation')
    require(tex.count(r'\begin{maintheorem}')==19,'Theorems A--S')
    for env in ('theorem','lemma','proposition','corollary','proof','maintheorem','align','equation','tabular'):
        require(tex.count('\\begin{'+env+'}')==tex.count('\\end{'+env+'}'),'unbalanced '+env)
    require(not any(ord(c)<32 and c not in '\n\r\t' for c in tex),'control character')
    needed={'thm:intro-window-remainder','thm:intro-relative-physical-window','lem:window-interval-envelopes',
       'thm:unsmoothed-window-denominator','thm:averaged-common-raw-remainder','lem:projected-window-denominator',
       'lem:actual-return-window-maximal','prop:physical-window-coupling','thm:relative-physical-window',
       'thm:shape-volume-criterion','thm:coherent-raw-cutoff-rate','thm:LLT'}
    require(needed<=set(labels),'missing required theorem')
    for key in ('full_raw_LLT_proved','full_fixed_return_complementary_integral_proved',
         'uniform_long_time_raw_derivative_bound_proved','pointwise_common_raw_remainder_proved',
         'microscopic_exact_event_replacement_proved','stationary_suspension_window_replacement_proved',
         'independent_human_review','formal_proof_certificate'):
        require(man[key] is False,'unsupported completion flag '+key)
    for key in ('unsmoothed_window_denominator_proved','signed_window_average_of_common_remainder_proved',
         'section_start_mesoscopic_physical_event_replacement_proved'):
        require(man[key] is True,'missing scoped theorem flag')
    report=ROOT.parents[1]/REPORT;report_verified=False
    if report.exists():
        data=report.read_bytes();blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        require(blob==REPORT_BLOB==man['controlling_review_blob'],'report identity');report_verified=True
    else:require(allow_missing_report,'controlling report not in checkout')
    return {'baseline_paper_tree':BASE_TREE,'inherited_core_byte_identical':len(cores),
        'inherited_python_files_byte_identical':len(scripts),'retained_mathematical_labels':len(oldlabels),
        'total_labels':len(labels),'included_core_files':len(inputs),'bibliography_items':len(bibitems),
        'exact_inherited_edits':6,'verified_file_count':len(actual),'controlling_report_verified':report_verified,
        'source_sha256':actual}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--allow-missing-report',action='store_true')
    args=parser.parse_args()
    result={'revision':27,'source':source_checks(args.allow_missing_report),
        'new_finite_checks':finite_checks(),
        'inherited_finite_checks':{'v26':old.finite_checks(),'v25':old.old.finite_checks(),
                                 'v24':old.old.old.finite_checks(),**old.old.old.inherited_checks()},
        'continuum_proof_certified':False,'full_raw_LLT_certified':False}
    print(json.dumps(result,indent=2,sort_keys=True))
