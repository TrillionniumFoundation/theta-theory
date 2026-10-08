#!/usr/bin/env python3
"""Exact-source replay and finite diagnostics; not continuum certification."""
from __future__ import annotations
from pathlib import Path
import argparse
import hashlib
import json
import os
import re
import verify_v24 as old
from check_high_order_bands import finite_checks

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT.parent / 'A2-DYN-v24-referee-response'
BASE_TREE = 'f15ab9854d022319db374f8ce38f4e6a4273dd84'
REPORT = 'reviews/a2-dyn-v24-external-top4-review-2026-10-07/REFEREE_REPORT.md'
REPORT_BLOB = '9f58ef5d84b9e91d5eadd8d4a49317158db695e0'
ordinary = old.ordinary
tree_hash = old.tree_hash


def require(ok: bool, message: str) -> None:
    if not ok: raise RuntimeError(message)


def digest(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def source_checks(allow_missing_report: bool = False) -> dict:
    require(not (allow_missing_report and os.environ.get('GITHUB_ACTIONS')), 'report check cannot be skipped in Actions')
    man = json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())
    ledger = json.loads((ROOT/'INHERITED_EDITS.json').read_text())
    require(man['revision'] == ledger['revision'] == 25, 'revision')
    require(tree_hash(BASE).hex() == BASE_TREE == man['baseline_paper_tree'], 'baseline ordinary tree')
    require({p.relative_to(BASE).as_posix():digest(p) for p in ordinary(BASE)} == man['baseline_sha256'], 'complete baseline file hashes')
    edits = ledger['edits']
    require(len(edits) == 6 and {e['path'] for e in edits} == {'main.tex'}, 'exact edit scope')
    s = (BASE/'main.tex').read_text()
    for e in edits:
        require(s.count(e['before']) == 1, 'nonunique inherited replacement')
        s = s.replace(e['before'], e['after'], 1)
    require(s.encode() == (ROOT/'main.tex').read_bytes(), 'main is not exact edit replay')
    cores = sorted((BASE/'core').glob('*.tex'))
    scripts = sorted((BASE/'tools').glob('*.py'))
    require(len(cores) == 51, 'incomplete inherited core')
    for p in cores + scripts + [BASE/'references.tex']:
        rel = p.relative_to(BASE)
        require(p.read_bytes() == (ROOT/rel).read_bytes(), 'changed inherited source: '+str(rel))
    actual = {p.relative_to(ROOT).as_posix():digest(p) for p in ordinary(ROOT) if p.name != 'SOURCE_MANIFEST.json'}
    require(actual == man['source_sha256'], 'complete actual source hashes')
    main = (ROOT/'main.tex').read_text()
    inputs = re.findall(r'\\input\{(core/[^}]+)\}', main)
    require(len(inputs) == len(set(inputs)) == 54, 'core inclusion count')
    require({s+'.tex' for s in inputs} == {p.relative_to(ROOT).as_posix() for p in (ROOT/'core').glob('*.tex')}, 'omitted core')
    tex = main+'\n'+'\n'.join((ROOT/(s+'.tex')).read_text() for s in inputs)
    labels = re.findall(r'\\label\{([^}]+)\}', tex)
    oldtex = (BASE/'main.tex').read_text()+'\n'+'\n'.join(p.read_text() for p in cores)
    oldlabels = set(re.findall(r'\\label\{([^}]+)\}', oldtex))
    require(len(labels) == len(set(labels)) and oldlabels <= set(labels), 'duplicate or removed mathematical label')
    refs = set(re.findall(r'\\(?:ref|eqref|pageref|autoref)\{([^}]+)\}', tex))
    require(refs <= set(labels), 'unresolved references: '+str(refs-set(labels)))
    bib = (ROOT/'references.tex').read_text()
    items = set(re.findall(r'\\bibitem\{([^}]+)\}', bib))
    cites = set()
    for group in re.findall(r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}', tex): cites.update(x.strip() for x in group.split(','))
    require(cites <= items, 'missing citation')
    require('October 7, 2026. A2-DYN, revision 25' in main, 'wrong article identity')
    require(tex.count(r'\begin{maintheorem}') == 15, 'Theorems A--O')
    for env in ('theorem','lemma','proposition','corollary','proof','maintheorem','align','equation','tabular'):
        require(tex.count('\\begin{'+env+'}') == tex.count('\\end{'+env+'}'), 'unbalanced '+env)
    require(not any(ord(c)<32 and c not in '\n\r\t' for c in tex), 'TeX control character')
    needed = {'lem:all-small-mass-moments','lem:heterogeneous-cumulant-comparison',
              'thm:high-order-damped-unsmoothing','thm:anisotropic-fixed-count-band',
              'cor:roof-box-fixed-count','cor:anisotropic-same-event','cor:roof-box-raw-budget',
              'app:dependency-guide','thm:intro-anisotropic-band','thm:LLT',
              'thm:rate-preserving-annulus','thm:marked-return-band'}
    require(needed <= set(labels), 'missing required theorem')
    for key in ('full_raw_LLT_proved','full_fixed_return_complementary_integral_proved',
                'uniform_long_time_raw_derivative_bound_proved','exact_physical_event_replacement_proved',
                'full_isotropic_one_tenth_band_proved','independent_human_review','formal_proof_certificate'):
        require(man[key] is False, 'unsupported completion flag '+key)
    for key in ('fixed_arbitrary_order_damped_unsmoothing_proved','anisotropic_fixed_count_band_proved',
                'retained_rate_union_proved','active_box_raw_identity_proved'):
        require(man[key] is True, 'missing new theorem flag '+key)
    report = ROOT.parents[1]/REPORT
    report_verified = False
    if report.exists():
        data = report.read_bytes()
        blob = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        require(blob == REPORT_BLOB == man['controlling_review_blob'], 'controlling report identity')
        report_verified = True
    else:
        require(allow_missing_report, 'controlling report not in checkout')
    return {'baseline_paper_tree':BASE_TREE,'inherited_core_byte_identical':len(cores),
            'inherited_python_files_byte_identical':len(scripts),
            'retained_mathematical_labels':len(oldlabels),'total_labels':len(labels),
            'included_core_files':len(inputs),'bibliography_items':len(items),
            'exact_inherited_edits':len(edits),'verified_file_count':len(actual),
            'controlling_report_verified':report_verified,'source_sha256':actual}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--allow-missing-report',action='store_true',help='local extracted archives only; forbidden in GitHub Actions')
    args = parser.parse_args()
    print(json.dumps({'revision':25,'source':source_checks(args.allow_missing_report),
          'new_finite_checks':finite_checks(),
          'inherited_finite_checks':{'v24':old.finite_checks(), **old.inherited_checks()},
          'continuum_proof_certified':False,'full_raw_LLT_certified':False},indent=2,sort_keys=True))
