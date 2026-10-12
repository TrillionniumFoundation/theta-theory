#!/usr/bin/env python3
"""Frozen-source replay and finite checks, not continuum proof certification."""
from __future__ import annotations
from pathlib import Path
import hashlib,json,re
import verify_v20,verify_v19,verify_v18,verify_v17,verify_v16,verify_v15,verify_v14,verify_v13,verify_v11
from check_fixed_count import finite_checks
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT.parent/'A2-DYN-v20-referee-response'
BASE_TREE='cbfa76a8957d3d327655a9969d55cb4a9d3e24bb'
ordinary=verify_v20.ordinary
tree_hash=verify_v20.tree_hash

def require(ok: bool,message: str) -> None:
    if not ok:raise RuntimeError(message)
def digest(p:Path)->str:return hashlib.sha256(p.read_bytes()).hexdigest()

def source_checks()->dict:
    man=json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())
    ledger=json.loads((ROOT/'INHERITED_EDITS.json').read_text())
    require(man['revision']==22 and ledger['baseline']==man['author_baseline_commit'],'revision/baseline')
    require(tree_hash(BASE).hex()==BASE_TREE==man['baseline_paper_tree']==ledger['baseline_paper_tree'],'frozen baseline tree')
    require({p.relative_to(BASE).as_posix():digest(p) for p in ordinary(BASE)}==man['baseline_sha256'],'complete baseline hashes')
    edits={}
    for e in ledger['edits']:edits.setdefault(e['path'],[]).append(e)
    require(set(edits)=={'main.tex','references.tex'} and len(ledger['edits'])==8,'inherited edit set')
    old_core=sorted((BASE/'core').glob('*.tex'));scripts=sorted((BASE/'tools').glob('*.py'))
    require(len(old_core)==45,'baseline module count')
    for p in old_core+scripts+[BASE/'main.tex',BASE/'references.tex']:
        rel=p.relative_to(BASE).as_posix();s=p.read_text()
        for e in edits.get(rel,[]):
            require(s.count(e['before'])==1,'nonunique inherited edit '+rel)
            s=s.replace(e['before'],e['after'],1)
        require(s.encode()==(ROOT/rel).read_bytes(),'unreported inherited change '+rel)
    require(all(p.read_bytes()==(ROOT/'core'/p.name).read_bytes() for p in old_core),'changed inherited core')
    actual={p.relative_to(ROOT).as_posix():digest(p) for p in ordinary(ROOT) if p.name!='SOURCE_MANIFEST.json'}
    require(actual==man['source_sha256'],'complete actual file hashes')
    main=(ROOT/'main.tex').read_text();require('A2-DYN, revision 22' in main,'revision text')
    inputs=re.findall(r'\\input\{(core/[^}]+)\}',main)
    require(len(inputs)==len(set(inputs))==47,'core inclusion count')
    require({s+'.tex' for s in inputs}=={p.relative_to(ROOT).as_posix() for p in (ROOT/'core').glob('*.tex')},'omitted mathematics')
    tex=main+'\n'+'\n'.join((ROOT/(s+'.tex')).read_text() for s in inputs)
    labels=re.findall(r'\\label\{([^}]+)\}',tex)
    oldlabels=set(re.findall(r'\\label\{([^}]+)\}','\n'.join(p.read_text() for p in old_core+[BASE/'main.tex'])))
    require(len(labels)==len(set(labels)) and oldlabels<=set(labels),'duplicate/deleted label')
    refs=set(re.findall(r'\\(?:ref|eqref|pageref|autoref)\{([^}]+)\}',tex))
    require(refs<=set(labels),'unresolved references '+str(refs-set(labels)))
    bib=(ROOT/'references.tex').read_text()
    items=set(re.findall(r'\\bibitem\{([^}]+)\}',bib));olditems=set(re.findall(r'\\bibitem\{([^}]+)\}',(BASE/'references.tex').read_text()))
    require(items==olditems|{'DJS'},'bibliography retention')
    cites=set()
    for group in re.findall(r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}',tex):cites.update(s.strip() for s in group.split(','))
    require(cites<=items,'missing citation')
    require(not any(ord(c)<32 and c not in '\n\r' for c in tex),'TeX control character')
    for env in ('theorem','lemma','proposition','corollary','proof','maintheorem','align','equation'):
        require(tex.count('\\begin{'+env+'}')==tex.count('\\end{'+env+'}'),'unbalanced '+env)
    required={'thm:intro-fixed-return-annulus','lem:all-finite-product','prop:connected-collision-summability',
      'thm:finite-spectral-jet','cor:finite-jet-damping','lem:fixed-count-damped-comparison',
      'thm:fixed-return-inner-annulus','cor:fixed-count-expanded-band','prop:finite-order-band-range',
      'cor:expanded-same-event-band','thm:expanded-count-localized-inversion','eq:expanded-raw-error-budget'}
    require(required<=set(labels),'new proof missing')
    require(tex.count(r'\begin{maintheorem}')==12,'Theorems A--L missing')
    for key in ('full_raw_LLT_proved','full_fixed_return_complementary_integral_proved','uncompressed_unitary_operator_norm_decay_proved',
      'uniform_long_time_raw_derivative_bound_proved','exact_physical_event_replacement_proved'):
        require(man[key] is False,'unsupported completion flag '+key)
    for key in ('fixed_count_inner_annulus_proved','expanded_marked_central_band_proved','finite_order_spectral_jet_proved'):
        require(man[key] is True,'new result flag '+key)
    return {'baseline_paper_tree':BASE_TREE,'included_core_files':len(inputs),'inherited_core_retained':len(old_core),
      'inherited_core_byte_identical':len(old_core),'inherited_python_files_byte_identical':len(scripts),
      'retained_mathematical_labels':len(oldlabels),'total_labels':len(labels),'exact_inherited_edits':len(ledger['edits']),
      'retained_bibliography_items':len(olditems),'bibliography_items':len(items),'verified_file_count':len(actual),'source_sha256':actual}

if __name__=='__main__':
    print(json.dumps({'revision':22,'source':source_checks(),'new_finite_checks':finite_checks(),
      'inherited_v20_checks':verify_v20.finite_checks(),'inherited_v19_checks':verify_v19.finite_checks(),
      'inherited_v18_checks':verify_v18.finite_checks(),'inherited_v17_checks':verify_v17.finite_checks(),
      'inherited_v16_checks':verify_v16.finite_checks(),'inherited_v15_checks':verify_v15.finite_checks(),
      'inherited_v14_algebra':verify_v14.algebra_checks(),'inherited_v14_mechanics':verify_v14.mechanical_checks(),
      'inherited_v13_checks':verify_v13.new_finite_checks(),'inherited_v11_checks':verify_v11.finite_checks(),
      'continuum_proof_certified':False,'full_raw_LLT_certified':False},indent=2,sort_keys=True))
