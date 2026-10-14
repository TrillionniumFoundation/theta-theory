#!/usr/bin/env python3
"""Exact source verification plus finite checks; not a continuum proof certificate."""
from __future__ import annotations
from pathlib import Path
import hashlib, json, os, re
import verify_v31 as prior
from check_positive_conditioning import finite_checks
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT.parent/'A2-DYN-v31-referee-response'
BASE_TREE='06d63ae32efec644d907a0d3d0118c54b8e74c4c'
REPORT='reviews/a2-dyn-v31-external-top4-review-2026-10-07/REFEREE_REPORT.md'
REPORT_BLOB='068e7f72d813f9ce2a558fb237af624d5cca90af'
WORKFLOW='.github/workflows/a2-dyn-v32-qualification.yml'
ordinary,tree_hash=prior.ordinary,prior.tree_hash

def require(ok, message):
    if not ok: raise RuntimeError(message)

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def source_checks():
    manifest=json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())
    ledger=json.loads((ROOT/'INHERITED_EDITS.json').read_text())
    require(manifest['revision']==ledger['revision']==32,'revision identity')
    require(tree_hash(BASE).hex()==BASE_TREE==manifest['baseline_paper_tree'],'exact baseline tree')
    require({p.relative_to(BASE).as_posix():digest(p) for p in ordinary(BASE)}==manifest['baseline_sha256'],'all baseline hashes')
    edits=ledger['edits'];paths={e['path'] for e in edits}
    require(len(edits)==12 and paths=={'main.tex','core/54_dependency_guide.tex','core/63_geometric_raw_regularization.tex','core/64_microscopic_finite_band_inversion.tex'},'exact edit scope')
    for rel in paths:
        text=(BASE/rel).read_text()
        for e in edits:
            if e['path']!=rel:continue
            require(text.count(e['before'])==1,'unique replay anchor '+rel)
            text=text.replace(e['before'],e['after'],1)
        require(text.encode()==(ROOT/rel).read_bytes(),'exact edit replay '+rel)
    cores=sorted((BASE/'core').glob('*.tex'));scripts=sorted((BASE/'tools').glob('*.py'))
    require(len(cores)==64 and len(scripts)==67,'complete inherited core/Python corpus')
    identical=0
    for p in cores+scripts:
        rel=p.relative_to(BASE).as_posix()
        if rel not in paths:
            require(p.read_bytes()==(ROOT/rel).read_bytes(),'unexpected inherited change '+rel)
            if p.suffix=='.tex':identical+=1
    require((BASE/'references.tex').read_bytes()==(ROOT/'references.tex').read_bytes(),'bibliography changed')
    actual={p.relative_to(ROOT).as_posix():digest(p) for p in ordinary(ROOT) if p.name!='SOURCE_MANIFEST.json'}
    require(actual==manifest['source_sha256'],'entire new ordinary source manifest')
    main=(ROOT/'main.tex').read_text();inputs=re.findall(r'\\input\{(core/[^}]+)\}',main)
    require(len(inputs)==len(set(inputs))==66,'all 66 core inputs')
    require({x+'.tex' for x in inputs}=={p.relative_to(ROOT).as_posix() for p in (ROOT/'core').glob('*.tex')},'unlisted core')
    tex=main+'\n'+'\n'.join((ROOT/(x+'.tex')).read_text() for x in inputs)
    oldtex=(BASE/'main.tex').read_text()+'\n'+'\n'.join(p.read_text() for p in cores)
    labels=re.findall(r'\\label\{([^}]+)\}',tex);oldlabels=set(re.findall(r'\\label\{([^}]+)\}',oldtex))
    require(len(labels)==len(set(labels)) and oldlabels<=set(labels) and len(oldlabels)==854,'old or duplicated labels')
    refs=set(re.findall(r'\\(?:ref|eqref|pageref|autoref)\{([^}]+)\}',tex))
    require(refs<=set(labels),'missing references '+str(refs-set(labels)))
    require('October 7, 2026. A2-DYN, revision 32' in main,'stale article revision')
    require(main.count(r'\begin{maintheorem}')==23,'Theorems A--W')
    require('bandwidth of logarithmic size' not in main,'ambiguous bandwidth description')
    for env in ('theorem','lemma','proposition','corollary','proof','maintheorem','align','equation','tabular','array'):
        require(tex.count('\\begin{'+env+'}')==tex.count('\\end{'+env+'}'),'unbalanced '+env)
    require(not any(ord(c)<32 and c not in '\n\t\r' for c in tex),'control character')
    items=set(re.findall(r'\\bibitem\{([^}]+)\}',(ROOT/'references.tex').read_text()));cites=set()
    for group in re.findall(r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}',tex):cites.update(x.strip() for x in group.split(','))
    require(cites<=items,'missing citation')
    for key in ('full_raw_LLT_proved','full_fixed_return_complementary_integral_proved',
                'pointwise_common_raw_remainder_proved','microscopic_exact_event_replacement_proved',
                'microscopic_Gaussian_denominator_proved','arbitrary_path_weight_denominator_proved',
                'independent_human_review','formal_proof_certificate'):
        require(manifest[key] is False,'unsupported raw endpoint flag '+key)
    for key in ('stationary_positive_geometric_extraction_proved','positive_global_mixed_L1_reconstruction_proved',
                'arbitrary_bounded_selector_microscopic_finite_band_reconstruction_proved'):
        require(manifest[key] is True,'missing scoped theorem flag '+key)
    needed={'thm:intro-positive-microscopic-conditioning','lem:source-partition-zero-extension',
            'lem:complete-first-hit-guard','prop:stationary-geometric-extraction',
            'thm:positive-spectral-approximation','thm:all-selector-finite-band',
            'cor:positive-microscopic-posterior','thm:uniform-positive-microscopic-inversion'}
    require(needed<=set(labels),'missing new theorem')
    report=ROOT.parents[1]/REPORT
    if report.exists():
        data=report.read_bytes();blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        require(blob==REPORT_BLOB==manifest['controlling_review_blob'],'exact controlling report')
        verified=True
    else:
        require(not os.environ.get('GITHUB_ACTIONS'),'remote checkout missing controlling report')
        verified=False
    wf=ROOT.parents[1]/WORKFLOW
    require(digest(wf)==manifest['qualification_workflow_sha256'],'exact workflow hash')
    require('contents: read' in wf.read_text() and 'contents: write' not in wf.read_text(),'qualification permissions')
    return {'baseline_paper_tree':BASE_TREE,'included_core_files':len(inputs),
        'inherited_core_byte_identical':identical,'inherited_core_explicitly_edited':64-identical,
        'inherited_python_byte_identical':len(scripts),'retained_mathematical_labels':len(oldlabels),
        'total_labels':len(labels),'bibliography_items':len(items),'exact_inherited_edits':len(edits),
        'verified_file_count':len(actual),'controlling_report_verified':verified,
        'controlling_report_bytes_boundary':None if verified else 'absent from local baseline archive; mandatory in remote checkout',
        'qualification_workflow_sha256':digest(wf),'source_sha256':actual}

if __name__=='__main__':
    print(json.dumps({'revision':32,'source':source_checks(),'new_finite_checks':finite_checks(),
       'inherited_finite_checks':{'v31':prior.finite_checks(),'v30':prior.old.finite_checks()},
       'continuum_proof_certified':False,'full_raw_LLT_certified':False},indent=2,sort_keys=True))
