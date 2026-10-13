#!/usr/bin/env python3
"""Exact source and finite regressions; never continuum proof certification."""
from __future__ import annotations
from pathlib import Path
import hashlib,json,re
import verify_v19,verify_v18,verify_v17,verify_v16,verify_v15,verify_v14,verify_v13,verify_v11
from check_direct_orbit import finite_checks
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT.parent/'A2-DYN-v19-referee-response'
BASE_TREE='57ea4229c9e344f9d61fd08be6ef7f7954d29feb'
ordinary=verify_v19.ordinary
tree_hash=verify_v19.tree_hash

def require(ok: bool,message: str) -> None:
    if not ok:raise RuntimeError(message)
def digest(p: Path) -> str:return hashlib.sha256(p.read_bytes()).hexdigest()

def source_checks() -> dict:
    man=json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())
    ledger=json.loads((ROOT/'INHERITED_EDITS.json').read_text())
    require(man['revision']==20 and ledger['baseline']==man['author_baseline_commit'],'revision/baseline')
    require(tree_hash(BASE).hex()==BASE_TREE==man['baseline_paper_tree']==ledger['baseline_paper_tree'],'frozen baseline tree')
    baseline={p.relative_to(BASE).as_posix():digest(p) for p in ordinary(BASE)}
    require(baseline==man['baseline_sha256'],'complete baseline hashes')
    edits={}
    for e in ledger['edits']:edits.setdefault(e['path'],[]).append(e)
    require(set(edits)=={'main.tex','core/39_compressed_return_resolvents.tex','core/40_finite_count_edge_extraction.tex'}
            and len(ledger['edits'])==7,'inherited edit set')
    old_core=sorted((BASE/'core').glob('*.tex'));scripts=sorted((BASE/'tools').glob('*.py'))
    require(len(old_core)==43,'baseline module count')
    identical=0
    for p in old_core+scripts+[BASE/'main.tex',BASE/'references.tex']:
        rel=p.relative_to(BASE).as_posix();content=p.read_text()
        for e in edits.get(rel,[]):
            require(content.count(e['before'])==1,'nonunique inherited edit '+rel)
            content=content.replace(e['before'],e['after'],1)
        require(content.encode()==(ROOT/rel).read_bytes(),'unreported inherited change '+rel)
        if p in old_core and p.read_bytes()==(ROOT/rel).read_bytes():identical+=1
    require(identical==41,'byte-identical core count')
    actual={p.relative_to(ROOT).as_posix():digest(p) for p in ordinary(ROOT) if p.name!='SOURCE_MANIFEST.json'}
    require(actual==man['source_sha256'],'complete source hashes')
    main=(ROOT/'main.tex').read_text();require('A2-DYN, revision 20' in main,'revision text')
    inputs=re.findall(r'\\input\{(core/[^}]+)\}',main)
    require(len(inputs)==len(set(inputs))==45,'complete core inclusions')
    require({s+'.tex' for s in inputs}=={p.relative_to(ROOT).as_posix() for p in (ROOT/'core').glob('*.tex')},'unlisted core')
    tex=main+'\n'+'\n'.join((ROOT/(s+'.tex')).read_text() for s in inputs)
    labels=re.findall(r'\\label\{([^}]+)\}',tex)
    oldlabels=set(re.findall(r'\\label\{([^}]+)\}','\n'.join(p.read_text() for p in old_core+[BASE/'main.tex'])))
    require(len(labels)==len(set(labels)) and oldlabels<=set(labels),'duplicate/deleted label')
    refs=set(re.findall(r'\\(?:ref|eqref|pageref|autoref)\{([^}]+)\}',tex))
    require(refs<=set(labels),'unresolved references '+str(refs-set(labels)))
    items=set(re.findall(r'\\bibitem\{([^}]+)\}',(ROOT/'references.tex').read_text()))
    olditems=set(re.findall(r'\\bibitem\{([^}]+)\}',(BASE/'references.tex').read_text()))
    require(items==olditems,'bibliography retention')
    cites=set()
    for group in re.findall(r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}',tex):cites.update(s.strip() for s in group.split(','))
    require(cites<=items,'missing citation')
    require(not any(ord(c)<32 and c not in '\n\r' for c in tex),'TeX control character')
    for env in ('theorem','lemma','proposition','corollary','proof','maintheorem','align','equation'):
        require(tex.count('\\begin{'+env+'}')==tex.count('\\end{'+env+'}'),'unbalanced '+env)
    required={'thm:intro-direct-annular-averages','prop:grid-scale-separation','lem:pointwise-lag-Gaussian',
              'lem:finite-orbit-frame','thm:direct-moving-averages','thm:weighted-annular-averages',
              'cor:direct-annular-averages','thm:cyclic-peripheral-bounds','thm:spectral-Cauchy-limit',
              'eq:normalized-annular-integral','eq:principal-angle-rounding'}
    require(required<=set(labels),'new result missing')
    for key in ('full_raw_LLT_proved','fixed_return_complementary_integral_proved','uncompressed_operator_norm_decay_proved',
                'uniform_long_time_raw_derivative_bound_proved','exact_physical_event_replacement_proved'):
        require(man[key] is False,'unsupported completion flag '+key)
    for key in ('direct_uncompressed_moving_averages_proved','weighted_unchanged_event_averages_proved',
                'full_angle_cyclic_vector_bounds_proved','spectral_Cauchy_limit_proved'):
        require(man[key] is True,'new result flag '+key)
    return {'baseline_paper_tree':BASE_TREE,'included_core_files':len(inputs),
            'inherited_core_retained':len(old_core),'inherited_core_byte_identical':identical,
            'inherited_python_files_byte_identical':len(scripts),'retained_mathematical_labels':len(oldlabels),
            'total_labels':len(labels),'exact_inherited_edits':len(ledger['edits']),
            'retained_bibliography_items':len(items),'verified_file_count':len(actual),'source_sha256':actual}

if __name__=='__main__':
    print(json.dumps({'revision':20,'source':source_checks(),'new_finite_checks':finite_checks(),
        'inherited_v19_checks':verify_v19.finite_checks(),'inherited_v18_checks':verify_v18.finite_checks(),
        'inherited_v17_checks':verify_v17.finite_checks(),'inherited_v16_checks':verify_v16.finite_checks(),
        'inherited_v15_checks':verify_v15.finite_checks(),'inherited_v14_algebra':verify_v14.algebra_checks(),
        'inherited_v14_mechanics':verify_v14.mechanical_checks(),'inherited_v13_checks':verify_v13.new_finite_checks(),
        'inherited_v11_checks':verify_v11.finite_checks(),'continuum_proof_certified':False,
        'full_raw_LLT_certified':False},indent=2,sort_keys=True))
