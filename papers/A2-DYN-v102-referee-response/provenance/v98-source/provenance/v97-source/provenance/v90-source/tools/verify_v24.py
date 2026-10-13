#!/usr/bin/env python3
"""Exact-source and finite algebra checks; not proof or publication certification."""
from pathlib import Path
import hashlib,json,re
import verify_v23 as old
from check_multiscale_stopping import finite_checks
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT.parent/'A2-DYN-v23-referee-response'
BASE_TREE='37e6f9a75ad1a6bb4f2c8710494cc50edac9e7c9'
ordinary=old.ordinary
tree_hash=old.tree_hash

def require(ok,message):
    if not ok:raise RuntimeError(message)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def source_checks():
    man=json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())
    ledger=json.loads((ROOT/'INHERITED_EDITS.json').read_text())
    require(man['revision']==24 and ledger['revision']==24,'revision')
    require(tree_hash(BASE).hex()==BASE_TREE==man['baseline_paper_tree'],'baseline tree')
    require({p.relative_to(BASE).as_posix():digest(p) for p in ordinary(BASE)}==man['baseline_sha256'],'baseline file hashes')
    edits=ledger['edits']
    require(len(edits)==5 and {e['path'] for e in edits}=={'main.tex'},'exact edit scope')
    s=(BASE/'main.tex').read_text()
    for e in edits:
        require(s.count(e['before'])==1,'nonunique exact edit')
        s=s.replace(e['before'],e['after'],1)
    require(s.encode()==(ROOT/'main.tex').read_bytes(),'main not exact replay')
    cores=sorted((BASE/'core').glob('*.tex'))
    scripts=sorted((BASE/'tools').glob('*.py'))
    require(len(cores)==49,'incomplete inherited mathematics')
    for p in cores+scripts+[BASE/'references.tex']:
        rel=p.relative_to(BASE)
        require(p.read_bytes()==(ROOT/rel).read_bytes(),'changed inherited source: '+str(rel))
    actual={p.relative_to(ROOT).as_posix():digest(p) for p in ordinary(ROOT) if p.name!='SOURCE_MANIFEST.json'}
    require(actual==man['source_sha256'],'complete actual source manifest')
    main=(ROOT/'main.tex').read_text()
    inputs=re.findall(r'\\input\{(core/[^}]+)\}',main)
    require(len(inputs)==len(set(inputs))==51,'core inclusion count')
    require({s+'.tex' for s in inputs}=={p.relative_to(ROOT).as_posix() for p in (ROOT/'core').glob('*.tex')},'omitted core')
    tex=main+'\n'+'\n'.join((ROOT/(s+'.tex')).read_text() for s in inputs)
    labels=re.findall(r'\\label\{([^}]+)\}',tex)
    oldtex=(BASE/'main.tex').read_text()+'\n'+'\n'.join(p.read_text() for p in cores)
    oldlabels=set(re.findall(r'\\label\{([^}]+)\}',oldtex))
    require(len(labels)==len(set(labels)) and oldlabels<=set(labels),'duplicate/deleted label')
    refs=set(re.findall(r'\\(?:ref|eqref|pageref|autoref)\{([^}]+)\}',tex))
    require(refs<=set(labels),'unresolved labels: '+str(refs-set(labels)))
    items=set(re.findall(r'\\bibitem\{([^}]+)\}',(ROOT/'references.tex').read_text()))
    cites=set()
    for group in re.findall(r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}',tex):cites.update(x.strip() for x in group.split(','))
    require(cites<=items,'missing bibliography entry')
    require('A2-DYN, revision 24' in main,'stale article date')
    require(tex.count(r'\begin{maintheorem}')==14,'Theorems A--N')
    for env in ('theorem','lemma','proposition','corollary','proof','maintheorem','align','equation'):
        require(tex.count('\\begin{'+env+'}')==tex.count('\\end{'+env+'}'),'unbalanced '+env)
    require(not any(ord(c)<32 and c not in '\n\r\t' for c in tex),'TeX control character')
    needed={'thm:multiscale-marked-stopping','lem:all-anchored-collision-moments',
      'thm:all-marked-gaussian-moments','thm:rate-preserving-annulus',
      'cor:rate-preserving-same-event','cor:rate-preserving-raw-budget','thm:LLT'}
    require(needed<=set(labels),'missing theorem')
    for key in ('full_raw_LLT_proved','full_fixed_return_complementary_integral_proved',
        'uniform_long_time_raw_derivative_bound_proved','exact_physical_event_replacement_proved'):
        require(man[key] is False,'unsupported completion flag')
    for key in ('quarter_order_stopping_proved','all_fixed_marked_moments_proved','rate_preserving_band_proved'):
        require(man[key] is True,'new theorem flag')
    report=ROOT.parents[1]/'reviews/a2-dyn-v22-external-top4-review-2026-10-06/REFEREE_REPORT.md'
    b=report.read_bytes()
    report_blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
    require(report_blob==man['controlling_review_blob'],'controlling report identity')
    return {'baseline_paper_tree':BASE_TREE,'inherited_core_byte_identical':len(cores),
      'inherited_python_files_byte_identical':len(scripts),'retained_mathematical_labels':len(oldlabels),
      'total_labels':len(labels),'included_core_files':len(inputs),'bibliography_items':len(items),
      'exact_inherited_edits':len(edits),'verified_file_count':len(actual),'source_sha256':actual}

def inherited_checks():
    return {'v23':old.finite_checks(),'v22':old.verify_v22.finite_checks(),
      'v20':old.verify_v20.finite_checks(),'v19':old.verify_v19.finite_checks(),
      'v18':old.verify_v18.finite_checks(),'v17':old.verify_v17.finite_checks(),
      'v16':old.verify_v16.finite_checks(),'v15':old.verify_v15.finite_checks(),
      'v14_algebra':old.verify_v14.algebra_checks(),'v14_mechanics':old.verify_v14.mechanical_checks(),
      'v13':old.verify_v13.new_finite_checks(),'v11':old.verify_v11.finite_checks()}

if __name__=='__main__':
    print(json.dumps({'revision':24,'source':source_checks(),'new_finite_checks':finite_checks(),
      'inherited_finite_checks':inherited_checks(),'continuum_proof_certified':False,
      'full_raw_LLT_certified':False},indent=2,sort_keys=True))
