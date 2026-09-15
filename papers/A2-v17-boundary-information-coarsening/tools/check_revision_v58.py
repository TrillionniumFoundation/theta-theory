#!/usr/bin/env python3
"""Preservation, declared dependency roles, and exact finite block diagnostics.

The general bounds are proved in the manuscript. Tests do not certify the
nonlinear smooth remainder, the infinite-flight argument, or journal significance.
"""
from __future__ import annotations
from collections import Counter
from fractions import Fraction as F
from math import factorial
import hashlib
import json
import re
from source_provenance import blob_id, graph, require
from materialize_revision_v58 import P, ARCHIVE, CHANGES, INTRO, NEW, revised, dependency_map
from materialize_revision_v57 import BLOCK, REF, DEPENDENCY, APPLICATION
from check_revision_v57 import references_by_unit, validate_roles
from check_revision_v56 import coordinate_controls
from check_revision_v55 import reduction_controls


def preservation() -> dict:
    baseline = json.loads((ARCHIVE/'active-source-manifest.json').read_text())
    old = {n: i for group in baseline.values() for n, i in group.items()}
    require(len(old) == 120, 'Unexpected baseline active union')
    total = retained = proofs = 0
    changes = []
    inventory = Counter()
    for name, info in old.items():
        data = (ARCHIVE/name if name in CHANGES else P/name).read_bytes()
        require(len(data) == info['bytes'] and hashlib.sha256(data).hexdigest() == info['sha256']
                and blob_id(data) == info['git_blob'], 'Baseline identity: ' + name)
        original, current = data.decode(), (P/name).read_text()
        require(current == (revised(name, original) if name in CHANGES else original),
                'Unprescribed edit: ' + name)
        before, after = list(BLOCK.finditer(original)), list(BLOCK.finditer(current))
        require(len(before) == len(after), 'Inherited block inventory changed: ' + name)
        for i, (a, b) in enumerate(zip(before, after)):
            total += 1
            proofs += a.group(1) == 'proof'
            inventory[a.group(1)] += 1
            require(a.group(1) == b.group(1), 'Block type changed')
            if a.group() == b.group():
                retained += 1
            else:
                changes.append({'path': name, 'ordinal': i, 'environment': a.group(1),
                                'old_sha256': hashlib.sha256(a.group().encode()).hexdigest(),
                                'new_sha256': hashlib.sha256(b.group().encode()).hexdigest()})
        require(set(re.findall(r'\\label\{([^}]+)\}', original)) <=
                set(re.findall(r'\\label\{([^}]+)\}', current)), 'Inherited label removed')
    require([(x['path'], x['environment']) for x in changes] == [(INTRO, 'theorem'), (INTRO, 'proof')],
            'The amendments exceed the headline strengthening and its proof map')
    added = Counter(m.group(1) for m in BLOCK.finditer((P/NEW).read_text()))
    require(added == {'proposition': 1, 'proof': 1}, 'Unexpected added block inventory')
    union = set()
    counts = {}
    labels_counts = {}
    for entry, group in baseline.items():
        active = graph(P, entry + '.tex')
        expected = set(group) | ({NEW} if entry != 'two_collision' else set())
        require(active == expected, 'Entry graph changed beyond new block input: ' + entry)
        union |= active
        counts[entry] = len(active)
        text = '\n'.join((P/n).read_text() for n in sorted(active))
        labels = re.findall(r'\\label\{([^}]+)\}', text)
        require(len(labels) == len(set(labels)), 'Duplicate label: ' + entry)
        labels_counts[entry] = len(labels)
        refs = set(REF.findall(text))
        external = set(dependency_map()['external_reference_roles']) if entry == 'rigidity' else set()
        if entry == 'main':
            external |= {x for x in refs if x.startswith('TC-')}
        require(refs <= set(labels) | external, 'Missing reference: ' + str(refs - set(labels) - external))
        cites = {k.strip() for c in re.findall(r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}', text) for k in c.split(',')}
        bib = set(re.findall(r'\\bibitem(?:\[[^\]]*\])?\{([^}]+)\}', text))
        require(cites <= bib, 'Missing citation: ' + str(cites - bib))
    require(union == set(old) | {NEW}, 'Unexpected union')
    return {'inherited_active_sources': len(old), 'active_sources': len(union),
            'byte_identical_in_place': len(old) - len(CHANGES), 'archived_amended_inputs': list(CHANGES),
            'inherited_statement_proof_blocks': total, 'verbatim_blocks': retained,
            'amended_blocks': changes, 'inherited_proofs': proofs,
            'inherited_inventory': dict(sorted(inventory.items())), 'added_inventory': dict(sorted(added.items())),
            'entry_counts': counts, 'entry_label_counts': labels_counts,
            'count_scope': 'Per source path, including shared display copies; not a count of independent results.'}


def dependencies() -> dict:
    declared = json.loads((P/'journal/DEPENDENCY_MAP_V58.json').read_text())
    require(declared == dependency_map(), 'Declaration differs from reading-derived map')
    roles = declared['external_reference_roles']
    units = {}
    for name in graph(P, 'rigidity.tex'):
        units.update(references_by_unit((P/name).read_text()))
    validate_roles(units, roles)
    require(DEPENDENCY in units[APPLICATION], 'Acquisition input removed')
    fixture = (r'\begin{corollary}\label{' + APPLICATION + r'}Assume \ref{' + DEPENDENCY +
               r'}.\end{corollary}\begin{proof}Apply its conclusion.\end{proof}')
    fu = references_by_unit(fixture)
    validate_roles(fu, roles)
    wrong = dict(roles)
    wrong[DEPENDENCY] = 'background_comparison'
    for candidate, chosen in [(fu, wrong), (references_by_unit(fixture.replace(APPLICATION, 'thm:rogue')), roles)]:
        failed = False
        try:
            validate_roles(candidate, chosen)
        except RuntimeError:
            failed = True
        require(failed, 'An undeclared or misclassified statement-level import was accepted')
    return {'external_reference_roles': roles, 'occurrences': len(declared['occurrences']),
            'statement_only_import_negative_controls': 'passed',
            'scope': 'Reading-derived declarations checked against syntax; not a semantic independence certificate.'}


def norm(a) -> F:
    return max(sum(abs(x) for x in row) for row in a)


def mv(a, v):
    return tuple(sum(x*y for x, y in zip(row, v)) for row in a)


def blocks(t: F, r: F, n: int):
    z = t**(2*n)
    d = (1 + z)/(1 - z)
    u, v = 2*(r*t)**n/(1-z), 2*(t/r)**n/(1-z)
    return ((d, u), (v, d)), ((d, -u), (-v, d))


def block_controls() -> dict:
    count = 0
    for t in map(F, ['1/50','1/8','1/3','1/2','3/4','9/10','99/100']):
        c, theta = (t + 1/t)/2, (1+t*t)/2
        C, K = (3+t**6)/(1-t**6), 4/(1-t**6)
        for w in map(F, ['1/100','1/4','1/2','3/4','99/100']):
            r = (1-w)/c + w*c
            require(c*r > 1 and c/r > 1, 'Fixture is not geometrically admissible')
            require(r*t < theta and t/r < theta, 'Admissible contraction')
            for n in range(3, 41):
                a, ai = blocks(t, r, n)
                require(a[0][0]*a[1][1] - a[0][1]*a[1][0] == 1, 'Determinant')
                for i in range(2):
                    for j in range(2):
                        require(sum(ai[i][k]*a[k][j] for k in range(2)) == (i==j), 'Inverse')
                require(norm(a) <= C and norm(ai) <= C, 'Uniform bound')
                for b in (a, ai):
                    correction = tuple(tuple(b[i][j]-(i==j) for j in range(2)) for i in range(2))
                    require(norm(correction) <= K*theta**n, 'Identity approach')
                require(a[0][0] == 1 + 2*t**(2*n)/(1-t**(2*n)), 'Own-contact multiplicities')
                require(a[0][1] == 2*r**n*t**n/(1-t**(2*n)), 'Cross-contact multiplicities')
                delta = (F(n,7), F(-n,11))
                image = mv(a, delta)
                require(mv(ai, image) == delta, 'Top-degree comparison')
                require(max(map(abs,delta))/C <= max(map(abs,image)) <= C*max(map(abs,delta)), 'Two-sided top-degree bound')
                count += 1
    # Direct coefficient-space tests, on finite-support factorial-normalized jets.
    t, r, R = F(1,3), F(7,5), F(3,2)
    theta, K, C = (1+t*t)/2, 4/(1-t**6), (3+t**6)/(1-t**6)
    source_norm = image_norm = inverse_norm = correction_norm = F(0)
    for n in range(3, 24):
        x = (F((-1)**n,n+1), F(1,n+2))
        a, ai = blocks(t,r,n)
        y, z = mv(a,x), mv(ai,x)
        wt, wtg = R**n/factorial(n), (R/theta)**n/factorial(n)
        source_norm += wt*max(map(abs,x))
        image_norm += wt*max(map(abs,y))
        inverse_norm += wt*max(map(abs,z))
        correction_norm += wtg*(max(abs(y[i]-x[i]) for i in range(2)) + max(abs(z[i]-x[i]) for i in range(2)))
    require(max(image_norm,inverse_norm) <= C*source_norm, 'Coefficient-space boundedness')
    require(correction_norm <= 2*K*source_norm, 'Coefficient-radius correction')
    # Determinant one with inadmissible curvature does not imply the bound.
    bad, _ = blocks(F(1,2),F(4),8)
    require(F(5,4)/4 < 1 and norm(bad) > (3+F(1,2)**6)/(1-F(1,2)**6), 'Admissibility negative control')
    # Wrong endpoint multiplicity is detected even with equal curvatures.
    a, _ = blocks(F(1,2),F(1),3)
    require((a[0][0]+1)*(a[1][1]+1)-a[0][1]*a[1][0] != 1, 'Multiplicity negative control')
    # Block-diagonal radius gain cannot be assigned to the identity part.
    n=30; a,_=blocks(t,r,n)
    require(norm(a)*theta**(-n) > K, 'Full diagonal radius-gain negative control')
    # Identity diagonal in an unrelated triangular map can hide growing inverse norms.
    triangular = []
    for m in (2,4,8,16):
        lower = [[int(i==j)-2*int(i==j+1) for j in range(m)] for i in range(m)]
        inverse = [[2**(i-j) if i>=j else 0 for j in range(m)] for i in range(m)]
        for i in range(m):
            for j in range(m):
                require(sum(lower[i][k]*inverse[k][j] for k in range(m)) == int(i==j),
                        'Explicit triangular inverse product')
        require(norm(inverse) == 2**m-1, 'Triangular row-sum formula')
        triangular.append({'dimension':m, 'inverse_infinity_norm':norm(inverse)})
    require(triangular[-1]['inverse_infinity_norm'] > 60000, 'Triangular-coupling negative control')
    return {'admissible_rational_blocks':count,'orders':[3,40],
            'fixed_lower_jet_and_finite_coefficient_controls':'passed',
            'negative_controls':['nonpositive curvature excluded','endpoint multiplicity','radius gain belongs to correction only','identity diagonal does not control triangular inverse'],
            'abstract_triangular_comparison':triangular,
            'scope':'Exact finite algebra only; fixtures do not simulate a billiard or prove an all-order nonlinear inverse.'}


if __name__ == '__main__':
    print(json.dumps({'status':'passed','mathematical_certification':False,
                      'preservation':preservation(),'dependency_roles':dependencies(),
                      'uniform_block_controls':block_controls(),
                      'retained_graph_support_controls':coordinate_controls(),
                      'retained_stopped_experiment_controls':reduction_controls()},sort_keys=True,indent=2))
