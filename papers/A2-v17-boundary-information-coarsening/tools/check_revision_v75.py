#!/usr/bin/env python3
"""Optimization-safe source preservation and finite algebra diagnostics.

These checks do not certify the analytic proofs or editorial significance.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import re
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]

def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)

def read(name: str) -> str:
    return (ROOT / name).read_text(encoding='utf-8')

def expand(name: str, seen: set[str] | None = None) -> str:
    seen = set() if seen is None else seen
    require(name not in seen, 'Repeated or cyclic active input: ' + name)
    seen.add(name)
    def include(match: re.Match[str]) -> str:
        path = match[1]
        if not path.endswith('.tex'):
            path += '.tex'
        require((ROOT/path).is_file(), 'Missing input: ' + path)
        return expand(path, seen)
    return re.sub(r'\\input\{([^}]+)\}', include, read(name))

def main() -> None:
    baseline = json.loads(read('verification/v75-baseline-preservation.json'))
    require(baseline['base_commit'] == 'c52fa361108a0f716d9e89017cd97eea71b0f3da', 'Baseline changed')
    require(baseline['base_tree'] == '48787e35d236d4a896abe328d78eff0ef154fdee', 'Baseline tree changed')
    require(len(baseline['files']) == 992, 'Incomplete baseline manifest')
    archived = []
    for name, expected in baseline['files'].items():
        require((ROOT/name).is_file(), 'Original source path deleted: ' + name)
        retained = expected['archive'] or name
        data = (ROOT/retained).read_bytes()
        require(len(data) == expected['bytes'] and hashlib.sha256(data).hexdigest() == expected['sha256'],
                'Inherited file not retained exactly: ' + name)
        if expected['archive']:
            archived.append(name)
    dep = json.loads(read('DEPENDENCY_MAP_V75.json'))
    for original, spec in dep['shared_core_slices'].items():
        text = read(original)
        require(text.count(spec['split_marker']) == 1, 'Ambiguous proof split')
        require(read(spec['principal']) == text.split(spec['split_marker'])[0], 'Core proof changed in slice')
    entries = {name: expand(name+'.tex') for name in ('rigidity', 'main', 'two_collision')}
    active = set()
    for name, text in entries.items():
        labs = re.findall(r'\\label\{([^}]+)\}', text)
        require(len(labs) == len(set(labs)), 'Duplicate mathematical label in ' + name)
        active.update(labs)
    retained = json.loads(read('verification/v75-active-labels.json'))
    require(len(retained['inherited_labels']) == 1423 and retained['baseline_count'] == 1423,
            'Incomplete old active-label record')
    require(set(retained['inherited_labels']) <= active, 'Inherited active statement no longer reachable')
    principal = entries['rigidity']
    alias_text = read('journal/full_reference_routes_v75.tex')
    aliases = set(re.findall(r'\\vFullAlias\{([^}]+)\}', alias_text))
    require(aliases == set(dep['external_aliases']), 'External dependency map differs from aliases')
    principal_labels = set(re.findall(r'\\label\{([^}]+)\}', principal))
    refs = set(re.findall(r'\\(?:eqref|ref|autoref)\{([^}]+)\}', principal))
    require(refs <= principal_labels | aliases, 'Unmapped principal references: ' + repr(sorted(refs-principal_labels-aliases)))
    for name in ('article/10b_periodic_contact_inverse_v65', 'article/10c_global_curvature_inverse_v66',
                 'journal/legacy_local_mechanism_v75', 'journal/legacy_graph_support_v75'):
        require('\\input{'+name+'}' in read('main.tex'), 'Full proof route not active: '+name)
    require('\\input{article/10e_sampled_smooth_recovery_v69}' in read('rigidity.tex'), 'Normal-incidence two-offset route omitted')
    old_intro = read('article/00i_main_thesis_v70.tex')
    require('Section~\\ref{sec:v74-moments} reconstructs' in old_intro and 'finite-flight rank defect' in old_intro,
            'R74-P1 roadmap not repaired')
    require('\\input{article/10j_conditioning_example_v75}' in read('article/10i_moment_reconstruction_v74.tex'),
            'R74-P2 example not active')
    cite_keys = set()
    for group in re.findall(r'\\cite(?:\[[^\]]*\])*\{([^}]+)\}', principal):
        cite_keys.update(group.split(','))
    bib_keys = set(re.findall(r'\\bibitem\{([^}]+)\}', read('journal/principal_references_v75.tex')))
    require(cite_keys == bib_keys, 'Principal bibliography not matched to actual citations')
    # Exact affine diagnostic: not a claim that the example is a realized table.
    u,v,p,R,d = sp.symbols('u v p R d', nonzero=True, real=True)
    f = (d+p*u-p*v)/(4*R**2*d)
    integral = lambda g: sp.integrate(sp.integrate(g, (u,-R,R)), (v,-R,R))
    H = sp.Matrix([[integral(u**i*v**j*f) for j in (0,1)] for i in (0,1)])
    a = p*R**2/(3*d)
    require(H == sp.Matrix([[1,-a],[a,0]]), 'Wrong affine moment orientation')
    require(sp.simplify(H.det()-p**2*R**4/(9*d**2)) == 0, 'Wrong affine determinant')
    require(H*sp.Matrix([[0,1/a],[-1/a,1/a**2]]) == sp.eye(2), 'Wrong affine inverse')
    # Preserve a genuine two-sided counter-control: compressed records alone
    # do not distinguish a rank-three finite kernel from the rank-two law.
    f0 = (4+u/2-v/2)/16
    q = lambda x: x*x-sp.Rational(1,3)
    perturb = q(u)*q(v)/100
    for x in (u,v):
        for j in (0,1):
            require(sp.integrate(x**j*perturb, (x,-1,1)) == 0, 'Perturbation visible to first moments')
    require(perturb != 0 and sp.Rational(3,16)-sp.Rational(1,225)>0, 'Negative control lost positivity')
    print(json.dumps({'status':'passed', 'baseline_files_retained_exactly':992,
        'archived_changed_originals':sorted(archived), 'inherited_active_labels':1423,
        'current_active_labels':len(active), 'exact_core_slices':len(dep['shared_core_slices']),
        'external_comparison_aliases':len(aliases), 'principal_citation_entries':len(bib_keys),
        'affine_matrix_and_rank_defect_controls':'passed', 'optimization_safe':True,
        'scope':'Source preservation, active references and finite symbolic identities only; not a formal proof certificate or a top-four acceptance assessment.'}, indent=2,sort_keys=True))

if __name__ == '__main__':
    main()
