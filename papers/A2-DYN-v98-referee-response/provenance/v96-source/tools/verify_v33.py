#!/usr/bin/env python3
"""Exact complete-source verification and finite diagnostics, not a proof certificate."""
from __future__ import annotations
from pathlib import Path
import hashlib,json,os,re
import verify_v32 as prior
from check_stationary_overlap import finite_checks
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT.parent/'A2-DYN-v32-referee-response'
BASE_TREE='d6462c94e0cb7a702bf4e46e60da0440fb94a5ac'
REPORT='reviews/a2-dyn-v32-external-top4-review-2026-10-07/REFEREE_REPORT.md'
REPORT_BLOB='9b25d7264504a0cf214d0e473281010505713310'
WORKFLOW='.github/workflows/a2-dyn-v33-qualification.yml'
ordinary,tree_hash=prior.ordinary,prior.tree_hash


def require(ok:bool,message:str)->None:
    if not ok:raise RuntimeError(message)


def digest(p:Path)->str:return hashlib.sha256(p.read_bytes()).hexdigest()


def source_checks()->dict:
    manifest=json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())
    ledger=json.loads((ROOT/'INHERITED_EDITS.json').read_text())
    require(manifest['revision']==ledger['revision']==33,'revision identity')
    require(tree_hash(BASE).hex()==BASE_TREE==manifest['baseline_paper_tree'],'complete baseline tree')
    require({p.relative_to(BASE).as_posix():digest(p) for p in ordinary(BASE)}==manifest['baseline_sha256'],'all baseline hashes')
    edits=ledger['edits'];require(len(edits)==5 and {e['path'] for e in edits}=={'main.tex'},'main-only inherited edits')
    main=(BASE/'main.tex').read_text()
    for e in edits:
        require(main.count(e['before'])==1,'unique edit anchor')
        main=main.replace(e['before'],e['after'],1)
    require(main.encode()==(ROOT/'main.tex').read_bytes(),'exact main replay')
    cores=sorted((BASE/'core').glob('*.tex'));scripts=sorted((BASE/'tools').glob('*.py'))
    require(len(cores)==66 and len(scripts)==71,'complete inherited corpus')
    for p in cores+scripts+[BASE/'references.tex']:
        require(p.read_bytes()==(ROOT/p.relative_to(BASE)).read_bytes(),'unexpected inherited change '+p.name)
    actual={p.relative_to(ROOT).as_posix():digest(p) for p in ordinary(ROOT) if p.name!='SOURCE_MANIFEST.json'}
    require(actual==manifest['source_sha256'],'complete ordinary source manifest')
    inputs=re.findall(r'\\input\{(core/[^}]+)\}',main)
    require(len(inputs)==len(set(inputs))==68,'all 68 core inputs')
    require({s+'.tex' for s in inputs}=={p.relative_to(ROOT).as_posix() for p in (ROOT/'core').glob('*.tex')},'unlisted core')
    tex=main+'\n'+'\n'.join((ROOT/(s+'.tex')).read_text() for s in inputs)
    oldtex=(BASE/'main.tex').read_text()+'\n'+'\n'.join(p.read_text() for p in cores)
    labels=re.findall(r'\\label\{([^}]+)\}',tex);oldlabels=set(re.findall(r'\\label\{([^}]+)\}',oldtex))
    require(len(labels)==len(set(labels)) and len(oldlabels)==887 and oldlabels<=set(labels),'duplicate/deleted labels')
    refs=set(re.findall(r'\\(?:ref|eqref|pageref|autoref)\{([^}]+)\}',tex))
    require(refs<=set(labels),'undefined references '+str(refs-set(labels)))
    require('October 7, 2026. A2-DYN, revision 33' in main,'stale main identity')
    require(main.count(r'\begin{maintheorem}')==24,'Theorems A--X')
    for env in ('theorem','lemma','proposition','corollary','proof','maintheorem','align','equation','tabular','array','aligned'):
        require(tex.count('\\begin{'+env+'}')==tex.count('\\end{'+env+'}'),'unbalanced '+env)
    require(not any(ord(c)<32 and c not in '\n\t\r' for c in tex),'control characters')
    items=set(re.findall(r'\\bibitem\{([^}]+)\}',(ROOT/'references.tex').read_text()));cites=set()
    for group in re.findall(r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}',tex):cites.update(x.strip() for x in group.split(','))
    require(len(items)==18 and cites<=items,'bibliography or citations')
    for key in ('full_raw_LLT_proved','full_fixed_return_complementary_integral_proved',
                'pointwise_common_raw_remainder_proved','microscopic_exact_event_replacement_proved',
                'microscopic_Gaussian_denominator_proved','arbitrary_path_weight_denominator_proved',
                'stationary_microscopic_middle_complement_smallness_proved',
                'independent_human_review','formal_proof_certificate'):
        require(manifest[key] is False,'unsupported endpoint claim '+key)
    for key in ('exact_stationary_physical_singleton_inversion_proved',
                'uniform_physical_time_curvature_measure_bound_proved',
                'pointwise_polynomial_physical_time_tail_proved',
                'original_physical_event_selector_source_TV_proved',
                'stationary_singleton_Gaussian_central_term_proved'):
        require(manifest[key] is True,'missing scoped new result '+key)
    needed={'thm:intro-exact-physical-endpoint','lem:finite-flight-cell-partition',
            'thm:stationary-overlap-regularity','thm:stationary-polynomial-band',
            'thm:physical-time-selector-reconstruction','cor:direct-physical-posterior',
            'lem:two-roof-central-comparison','thm:stationary-singleton-central-term',
            'thm:physical-singleton-reduction','cor:stationary-singleton-denominator-criterion'}
    require(needed<=set(labels),'new theorem missing')
    report=ROOT.parents[1]/REPORT
    if report.exists():
        data=report.read_bytes();blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        require(blob==REPORT_BLOB==manifest['controlling_review_blob'],'exact report bytes');verified=True
    else:
        require(not os.environ.get('GITHUB_ACTIONS'),'remote source lacks controlling report');verified=False
    wf=ROOT.parents[1]/WORKFLOW
    require(digest(wf)==manifest['qualification_workflow_sha256'],'qualification workflow identity')
    require('contents: read' in wf.read_text() and 'contents: write' not in wf.read_text(),'read-only qualification')
    return {'baseline_paper_tree':BASE_TREE,'included_core_files':68,
            'inherited_core_byte_identical':66,'inherited_python_byte_identical':71,
            'retained_mathematical_labels':887,'total_labels':len(labels),'bibliography_items':len(items),
            'exact_inherited_edits':len(edits),'verified_file_count':len(actual),
            'controlling_report_verified':verified,
            'controlling_report_bytes_boundary':None if verified else 'not in local baseline archive; required at remote SHA',
            'qualification_workflow_sha256':digest(wf),'source_sha256':actual}

if __name__=='__main__':
    print(json.dumps({'revision':33,'source':source_checks(),'new_finite_checks':finite_checks(),
        'inherited_finite_checks':{'v32':prior.finite_checks(),'v31':prior.prior.finite_checks()},
        'continuum_proof_certified':False,'full_raw_LLT_certified':False},indent=2,sort_keys=True))
