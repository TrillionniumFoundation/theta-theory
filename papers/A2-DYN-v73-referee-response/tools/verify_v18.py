#!/usr/bin/env python3
"""Source replay and finite algebra. This does not certify continuum proofs."""
from __future__ import annotations
from pathlib import Path
from fractions import Fraction as F
import hashlib
import json
import re
import mpmath as mp
import verify_v11
import verify_v13
import verify_v14
import verify_v15
import verify_v16
import verify_v17 as old
from check_raw_jets import raw_jet_checks

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT.parent/'A2-DYN-v17-referee-response'

def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)

def digest(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def source_checks() -> dict:
    man=json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())
    ledger=json.loads((ROOT/'INHERITED_EDITS.json').read_text())
    require(man['revision']==18, 'revision')
    require(ledger['baseline']==man['author_baseline_commit'], 'baseline identity')
    edits={}
    for e in ledger['edits']: edits.setdefault(e['path'],[]).append(e)
    require(set(edits)=={'main.tex','references.tex'}, 'unlisted inherited edit class')
    old_core=sorted((BASE/'core').glob('*.tex'))
    require(len(old_core)==39, 'baseline core count')
    inherited=old_core+[BASE/'main.tex',BASE/'references.tex']
    for p in inherited:
        rel=p.relative_to(BASE).as_posix()
        require(digest(p)==man['baseline_sha256'][rel], 'baseline hash '+rel)
        text=p.read_text()
        for e in edits.get(rel,[]):
            require(text.count(e['before'])==1, 'edit not unique '+rel)
            text=text.replace(e['before'],e['after'],1)
        require(text.encode()==(ROOT/rel).read_bytes(), 'unreported edit '+rel)
    scripts=sorted((BASE/'tools').glob('*.py'))
    for p in scripts:
        require(p.read_bytes()==(ROOT/'tools'/p.name).read_bytes(), 'inherited script '+p.name)
    actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file()
            and not any(x in ('build','evidence','__pycache__') for x in p.parts)
            and p.name!='SOURCE_MANIFEST.json'}
    require(actual==set(man['source_sha256']), 'source map completeness')
    for rel,h in man['source_sha256'].items(): require(digest(ROOT/rel)==h, 'source hash '+rel)
    main=(ROOT/'main.tex').read_text()
    require('A2-DYN, revision 18' in main, 'version metadata')
    inputs=re.findall(r'\\input\{(core/[^}]+)\}',main)
    require(len(inputs)==len(set(inputs))==41, 'core inclusion count')
    require({x+'.tex' for x in inputs}=={p.relative_to(ROOT).as_posix() for p in (ROOT/'core').glob('*.tex')}, 'unlisted core')
    tex=main+'\n'+'\n'.join((ROOT/(x+'.tex')).read_text() for x in inputs)
    labels=re.findall(r'\\label\{([^}]+)\}',tex)
    oldlabels=set(re.findall(r'\\label\{([^}]+)\}','\n'.join(p.read_text() for p in inherited)))
    require(len(labels)==len(set(labels)), 'duplicate label')
    require(oldlabels<=set(labels), 'deleted mathematical label')
    refs=set(re.findall(r'\\(?:ref|eqref|pageref|autoref)\{([^}]+)\}',tex))
    require(refs<=set(labels), 'unresolved references '+str(refs-set(labels)))
    items=set(re.findall(r'\\bibitem\{([^}]+)\}',(ROOT/'references.tex').read_text()))
    cites=set()
    for g in re.findall(r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}',tex): cites.update(x.strip() for x in g.split(','))
    require(cites<=items, 'unresolved citations')
    olditems=set(re.findall(r'\\bibitem\{([^}]+)\}',(BASE/'references.tex').read_text()))
    require(olditems<=items and items-olditems=={'CMInt'}, 'bibliography entry retention')
    for env in ('theorem','lemma','proposition','corollary','proof','maintheorem'):
        require(tex.count('\\begin{'+env+'}')==tex.count('\\end{'+env+'}'), 'unbalanced '+env)
    require(not any(ord(c)<32 and c not in '\n\r' for c in tex), 'TeX control character')
    expected={'thm:intro-finite-count-extraction','lem:finite-graph-density',
              'lem:power-log-jet','prop:finite-jet-subtraction',
              'thm:finite-count-raw-extraction','lem:central-count-support',
              'thm:finite-extraction-central-inversion','cor:finite-extraction-error-budget',
              'eq:central-count-Schwartz-tail','prop:cutoff-finite-band-budget',
              'thm:intro-peripheral-neighborhood','thm:LLT',
              'thm:joint-uniform-nondegeneracy','lem:raw-residual-sum'}
    require(expected<=set(labels), 'missing load-bearing theorem')
    for key in ('full_raw_LLT_proved','full_complementary_integral_proved',
                'uniform_long_time_raw_derivative_bound_proved',
                'exact_physical_event_replacement_proved','uncompressed_power_decay_proved'):
        require(man[key] is False, 'unsupported full-closure flag '+key)
    for key in ('finite_count_raw_extraction_proved',
                'finite_count_second_derivative_sum_proved','exact_central_count_identity_proved'):
        require(man[key] is True, 'wrong finite extraction record '+key)
    return {'included_core_files':len(inputs),'inherited_core_byte_identical':len(old_core),
            'inherited_python_files_byte_identical':len(scripts),'retained_mathematical_labels':len(oldlabels),
            'total_labels':len(labels),'exact_inherited_edits':len(ledger['edits']),
            'retained_bibliography_items':len(olditems),'total_bibliography_items':len(items),'verified_file_count':len(actual),
            'source_sha256':man['source_sha256']}


def finite_checks() -> dict:
    return raw_jet_checks()

if __name__=='__main__':
    print(json.dumps({'revision':18,'source':source_checks(),'new_finite_checks':finite_checks(),
                      'inherited_v17_checks':old.finite_checks(),
                      'inherited_v16_checks':verify_v16.finite_checks(),
                      'inherited_v15_checks':verify_v15.finite_checks(),
                      'inherited_v14_algebra':verify_v14.algebra_checks(),
                      'inherited_v14_mechanics':verify_v14.mechanical_checks(),
                      'inherited_v13_checks':verify_v13.new_finite_checks(),
                      'inherited_v11_checks':verify_v11.finite_checks(),
                      'continuum_proof_certified':False,'full_raw_LLT_certified':False},indent=2,sort_keys=True))
