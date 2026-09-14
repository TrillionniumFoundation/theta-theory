#!/usr/bin/env python3
"""Exact source-preservation and finite linearization controls; not a proof certificate."""
from __future__ import annotations
from collections import Counter
import hashlib
import json
import re
import sympy as s
from materialize_revision_v48 import ARCHIVE, CHANGES, NEW_INPUTS, P, revised
from source_provenance import blob_id, graph, require
from check_revision_v47 import finite_diagnostics as calibration_diagnostics


def preservation() -> dict:
    manifest = json.loads((ARCHIVE/'active-source-manifest.json').read_text())
    old = {name: info for entry in manifest.values() for name, info in entry.items()}
    before = Counter()
    for name, info in old.items():
        path = ARCHIVE/name if name in CHANGES else P/name
        data = path.read_bytes()
        require(hashlib.sha256(data).hexdigest() == info['sha256'], 'SHA-256: ' + name)
        require(blob_id(data) == info['git_blob'], 'Git blob: ' + name)
        before.update(re.findall(r'\\begin\{(theorem|lemma|proposition|corollary|definition|remark|proof)\}', data.decode()))
        if name in CHANGES:
            require((P/name).read_text() == revised(name, data.decode()), 'Unexpected active edit: ' + name)
    current = graph(P, 'main.tex') | graph(P, 'two_collision.tex')
    require(set(old) <= current, 'Inherited active source omitted')
    require(current-set(old) == set(NEW_INPUTS), 'Unexpected new active-source set')
    old_order = re.findall(r'\\input\{([^}]+)\}', (ARCHIVE/'main.tex').read_text())
    new_order = re.findall(r'\\input\{([^}]+)\}', (P/'main.tex').read_text())
    require([x for x in new_order if x+'.tex' not in NEW_INPUTS] == old_order, 'Inherited input order changed')
    additions = Counter()
    for name in NEW_INPUTS:
        additions.update(re.findall(r'\\begin\{(structuraltheorem|theorem|lemma|proposition|corollary|definition|remark|proof)\}', (P/name).read_text()))
    alltext = '\n'.join((P/name).read_text() for name in sorted(current))
    labels = re.findall(r'\\label\{([^}]+)\}', alltext)
    require(len(labels) == len(set(labels)), 'Duplicate active labels')
    refs = set(re.findall(r'\\(?:ref|eqref|autoref|pageref)\{([^}]+)\}', alltext))
    missing = sorted(x for x in refs if x not in labels and not x.startswith('TC-'))
    require(not missing, 'Missing references: ' + str(missing))
    return {'baseline_active_inputs': len(old), 'active_inputs': len(current),
        'byte_identical_inherited_inputs': len(old)-len(CHANGES),
        'archived_and_deterministically_amended_inputs': list(CHANGES),
        'new_inputs': list(NEW_INPUTS), 'all_inherited_inputs_and_theorem_proofs_retained': True,
        'inherited_environments': dict(sorted(before.items())),
        'added_environments': dict(sorted(additions.items())), 'active_labels': len(labels)}


def differential_controls() -> dict:
    # A functional algebra check, not a numerical billiard reconstruction.
    e,d,x,y,z = s.symbols('e d x y z', real=True)
    Su,Sv,Sa = x+e*x**2, y-e*y**2, z+e*z**2
    Bu,Bv,Ba = 1+e, 1+2*e, 1-3*e
    B0,Z = 1-e, 2+e
    def f(S1,S2,B1,B2): return B1*B2*(d-S1-S2)/Z
    R = s.cancel(f(Su,Sv,Bu,Bv)*f(0,0,B0,B0)/(f(Su,0,Bu,B0)*f(0,Sv,B0,Bv)))
    expected = 1-(Su/(d-Su))*(Sv/(d-Sv))
    require(s.cancel(R-expected) == 0, 'Amplitude cancellation')
    require(s.cancel(s.diff(R,e)-s.diff(expected,e)) == 0, 'Differentiated ratio')
    # At a nonzero convex anchor the positive root equals Sa/(d-Sa).
    R_ua = 1-(Su/(d-Su))*(Sa/(d-Sa)); R_aa = 1-(Sa/(d-Sa))**2
    q = Sa/(d-Sa); t = Su/(d-Su)
    dt = -s.diff(R_ua,e)/q+t*s.diff(R_aa,e)/(2*q**2)
    require(s.cancel(dt-s.diff(t,e)) == 0, 'Anchor differential sign/factor')
    require(s.cancel(d*dt/(1+t)**2-s.diff(Su,e)) == 0, 'Action differential')
    # A witness requiring three harmonics; no pair here has gcd one.
    U = s.symbols('U', nonzero=True)
    F = (6,10,15); a = (1,1,-1)
    require(sum(k*v for k,v in zip(F,a)) == 1, 'Bezout witness')
    recovered = s.prod((U**(-k))**(-v) for k,v in zip(F,a))
    require(s.simplify(recovered-U) == 0, 'Rotation reconstruction')
    # Fixed non-unimodular gains must recover arbitrary lattice tangents.
    M = s.Matrix([[2,1],[0,3]])
    DL = s.Matrix([[s.Rational(1,3),s.Rational(-2,5)],[s.Rational(7,11),s.Rational(4,9)]])
    require((DL*M)*M.inv() == DL, 'Lattice differential')
    require(DL*M != DL, 'Control fails to distinguish omitted inverse')
    x0 = s.symbols('x0', real=True)
    require(s.diff(x0**3,x0).subs(x0,0) == 0, 'Injectivity/immersion negative control')
    # Exercise determinant-one blocks with unequal type factors through order 12.
    blocks=[]
    for n in range(3,13):
        r=s.Rational(1,3)**n
        coth=(1+r*r)/(1-r*r); csch=2*r/(1-r*r)
        B=s.Matrix([[coth,2**n*csch],[s.Rational(1,2)**n*csch,coth]])
        require(B.det() == 1, 'Block determinant at order '+str(n))
        v=s.Matrix([s.Rational(n,7),s.Rational(-n,11)])
        require(B.inv()*(B*v) == v, 'Block tangent inverse')
        blocks.append(n)
    return {'amplitude_and_normalization_cancellation': True,
        'anchor_and_action_differential_identities': True,
        'finite_harmonic_witness': {'indices':F,'bezout_coefficients':a},
        'non_unimodular_gain_determinant': int(M.det()),
        'finite_jet_block_orders':blocks,
        'negative_controls': ['injective x^3 need not be an immersion', 'omitting M inverse changes lattice tangent'],
        'scope': 'Exact finite algebra only; analytic propagation and infinite-flight estimates are proved in the manuscript.'}


if __name__ == '__main__':
    print(json.dumps({'status':'passed','mathematical_certification':False,
        'preservation':preservation(),'differential_controls':differential_controls(),
        'retained_v47_finite_calibration_controls':calibration_diagnostics()},indent=2,sort_keys=True))
