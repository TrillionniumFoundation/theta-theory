#!/usr/bin/env python3
"""Exact source replay and regression checks; not continuum proof certification."""
from __future__ import annotations
from pathlib import Path
import hashlib,json,re
import verify_v18 as old
import verify_v17,verify_v16,verify_v15,verify_v14,verify_v13,verify_v11
from check_exponential_windows import finite_checks
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT.parent/'A2-DYN-v18-referee-response'
BASE_TREE='e19803bed418d2a1402781124f91737c136b595b'

def require(ok: bool,message: str) -> None:
    if not ok:raise RuntimeError(message)
def digest(p: Path) -> str:return hashlib.sha256(p.read_bytes()).hexdigest()
def object_hash(kind: str,data: bytes) -> bytes:
    return hashlib.sha1(kind.encode()+b' '+str(len(data)).encode()+b'\0'+data).digest()
def ordinary(root: Path):
    return [p for p in sorted(root.rglob('*')) if p.is_file()
            and not any(s in ('build','evidence','__pycache__') for s in p.relative_to(root).parts)]
def tree_hash(root: Path) -> bytes:
    rows=[]
    for p in root.iterdir():
        if p.name in ('build','evidence','__pycache__'):continue
        if p.is_dir():mode='40000';sha=tree_hash(p);key=p.name+'/'
        else:mode='100755' if p.stat().st_mode&0o111 else '100644';sha=object_hash('blob',p.read_bytes());key=p.name
        rows.append((key,mode.encode()+b' '+p.name.encode()+b'\0'+sha))
    return object_hash('tree',b''.join(row for _,row in sorted(rows)))

def source_checks() -> dict:
    man=json.loads((ROOT/'SOURCE_MANIFEST.json').read_text());ledger=json.loads((ROOT/'INHERITED_EDITS.json').read_text())
    require(man['revision']==19 and ledger['baseline']==man['author_baseline_commit'],'revision/baseline identity')
    require(tree_hash(BASE).hex()==BASE_TREE==man['baseline_paper_tree']==ledger['baseline_paper_tree'],'exact baseline tree')
    baseline={p.relative_to(BASE).as_posix():digest(p) for p in ordinary(BASE)}
    require(baseline==man['baseline_sha256'],'complete baseline file map')
    edits={}
    for e in ledger['edits']:edits.setdefault(e['path'],[]).append(e)
    require(set(edits)=={'main.tex'} and len(ledger['edits'])==5,'inherited edit class')
    old_core=sorted((BASE/'core').glob('*.tex'));scripts=sorted((BASE/'tools').glob('*.py'))
    require(len(old_core)==41,'baseline modules')
    for p in old_core+scripts+[BASE/'main.tex',BASE/'references.tex']:
        rel=p.relative_to(BASE).as_posix();content=p.read_text()
        for e in edits.get(rel,[]):
            require(content.count(e['before'])==1,'nonunique inherited edit '+rel)
            content=content.replace(e['before'],e['after'],1)
        require(content.encode()==(ROOT/rel).read_bytes(),'unreported inherited change '+rel)
    actual={p.relative_to(ROOT).as_posix():digest(p) for p in ordinary(ROOT) if p.name!='SOURCE_MANIFEST.json'}
    require(actual==man['source_sha256'],'complete source hashes')
    main=(ROOT/'main.tex').read_text();require('A2-DYN, revision 19' in main,'revision text')
    inputs=re.findall(r'\\input\{(core/[^}]+)\}',main)
    require(len(inputs)==len(set(inputs))==43,'complete core inclusions')
    require({s+'.tex' for s in inputs}=={p.relative_to(ROOT).as_posix() for p in (ROOT/'core').glob('*.tex')},'unlisted mathematics')
    tex=main+'\n'+'\n'.join((ROOT/(s+'.tex')).read_text() for s in inputs)
    labels=re.findall(r'\\label\{([^}]+)\}',tex)
    oldlabels=set(re.findall(r'\\label\{([^}]+)\}','\n'.join(p.read_text() for p in old_core+[BASE/'main.tex'])))
    require(len(labels)==len(set(labels)) and oldlabels<=set(labels),'duplicate/deleted mathematical label')
    refs=set(re.findall(r'\\(?:ref|eqref|pageref|autoref)\{([^}]+)\}',tex))
    require(refs<=set(labels),'unresolved reference '+str(refs-set(labels)))
    items=set(re.findall(r'\\bibitem\{([^}]+)\}',(ROOT/'references.tex').read_text()))
    cites=set()
    for group in re.findall(r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}',tex):cites.update(s.strip() for s in group.split(','))
    require(cites<=items,'missing citation')
    require(not any(ord(c)<32 and c not in '\n\r' for c in tex),'TeX control character')
    for env in ('theorem','lemma','proposition','corollary','proof','maintheorem'):
        require(tex.count('\\begin{'+env+'}')==tex.count('\\end{'+env+'}'),'unbalanced '+env)
    newlabels={'thm:intro-window-reconstruction','thm:exponential-finite-record','thm:single-log-return-defect',
        'cor:single-log-compressed','thm:window-central-integral','cor:logarithmic-window-conditioning',
        'thm:window-weighted-moments','eq:window-raw-exact-identity','eq:nonempty-window-budget'}
    require(newlabels<=set(labels),'missing new theorem')
    for key in ('full_raw_LLT_proved','full_complementary_integral_proved','uniform_long_time_raw_derivative_bound_proved',
                'exact_physical_event_replacement_proved','uncompressed_power_decay_proved','full_peripheral_circle_bound_proved'):
        require(man[key] is False,'unsupported closure flag '+key)
    for key in ('exponential_finite_record_variation_proved','single_log_return_defect_proved',
                'logarithmic_window_central_and_moment_theorems_proved'):
        require(man[key] is True,'new result flag '+key)
    return {'baseline_paper_tree':BASE_TREE,'included_core_files':len(inputs),
        'inherited_core_byte_identical':len(old_core),'inherited_python_files_byte_identical':len(scripts),
        'retained_mathematical_labels':len(oldlabels),'total_labels':len(labels),'exact_inherited_edits':len(ledger['edits']),
        'retained_bibliography_items':len(items),'verified_file_count':len(actual),'source_sha256':actual}

if __name__=='__main__':
    print(json.dumps({'revision':19,'source':source_checks(),'new_finite_checks':finite_checks(),
        'inherited_v18_checks':old.finite_checks(),'inherited_v17_checks':verify_v17.finite_checks(),
        'inherited_v16_checks':verify_v16.finite_checks(),'inherited_v15_checks':verify_v15.finite_checks(),
        'inherited_v14_algebra':verify_v14.algebra_checks(),'inherited_v14_mechanics':verify_v14.mechanical_checks(),
        'inherited_v13_checks':verify_v13.new_finite_checks(),'inherited_v11_checks':verify_v11.finite_checks(),
        'continuum_proof_certified':False,'full_raw_LLT_certified':False},indent=2,sort_keys=True))
