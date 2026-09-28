#!/usr/bin/env python3
"""Source-preservation and finite calibration diagnostics; not a proof certificate."""
from __future__ import annotations
from collections import Counter
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path
import re
import sympy as sp
from materialize_revision_v47 import ARCHIVE, CHANGES, P, blob, require, revised
from source_provenance import graph


def preservation() -> dict:
    manifest = json.loads((ARCHIVE / 'active-source-manifest.json').read_text())
    old = {}
    for entry in manifest.values():
        old.update(entry)
    unchanged = 0
    before_counts = Counter()
    for name, info in old.items():
        target = ARCHIVE / name if name in CHANGES else P / name
        data = target.read_bytes()
        require(hashlib.sha256(data).hexdigest() == info['sha256'], 'Baseline SHA-256: ' + name)
        require(blob(data) == info['git_blob'], 'Baseline Git blob: ' + name)
        before_counts.update(re.findall(r'\\begin\{(theorem|lemma|proposition|corollary|definition|remark|proof)\}', data.decode()))
        if name in CHANGES:
            require((P / name).read_text() == revised(name, data.decode()), 'Unexpected source edit: ' + name)
        else:
            unchanged += 1
    current = graph(P, 'main.tex') | graph(P, 'two_collision.tex')
    require(set(old) <= current, 'Inherited active input removed')
    added = sorted(current - set(old))
    require(added == ['article/01h_calibration_overview_v47.tex',
                      'article/23l_calibrated_histograms_v47.tex'], 'Unexpected active-input delta')
    before = re.findall(r'\\input\{([^}]+)\}', (ARCHIVE / 'main.tex').read_text())
    after = re.findall(r'\\input\{([^}]+)\}', (P / 'main.tex').read_text())
    require([x for x in after if x + '.tex' not in added] == before, 'Inherited input order changed')
    new_counts = Counter()
    for name in added:
        new_counts.update(re.findall(r'\\begin\{(theorem|lemma|proposition|corollary|definition|remark|proof)\}', (P / name).read_text()))
    text = '\n'.join((P / name).read_text() for name in sorted(current))
    labels = re.findall(r'\\label\{([^}]+)\}', text)
    require(len(labels) == len(set(labels)), 'Duplicate active label')
    allrefs = set(re.findall(r'\\(?:ref|eqref|pageref|autoref)\{([^}]+)\}', text))
    missing = sorted(x for x in allrefs if x not in labels and not x.startswith('TC-'))
    require(not missing, 'Undefined active internal references: ' + str(missing))
    return {'baseline_active_files': len(old), 'active_files': len(current),
            'byte_identical_inherited_files': unchanged, 'edited_inherited_files': sorted(CHANGES),
            'new_active_files': added, 'inherited_environments': dict(sorted(before_counts.items())),
            'added_environments': dict(sorted(new_counts.items())),
            'all_inherited_inputs_and_order_preserved': True,
            'archived_originals_verified': True, 'active_labels': len(labels)}


def finite_diagnostics() -> dict:
    # Exact cap-family TV: a functional normalization check, not a billiard example.
    d, D = sp.symbols('d D', positive=True)
    c = d * D / (d + D)
    difference = 2*c*(1/d-1/D) - c**2*(1/d**2-1/D**2)
    require(sp.simplify(difference-(D-d)/(D+d)) == 0, 'Offset normalization identity')
    eps, j = sp.symbols('eps j', positive=True)
    amplified = sp.simplify(((D-d)/(D+d)).subs(D, d+j*eps))
    require(sp.simplify(amplified - j*eps/(2*d+j*eps)) == 0, 'Missing flight amplification')
    # A bounded-displacement functional map moves only the rightmost strip in
    # every even cell. Exact rational cell vectors verify the factor two and
    # give a negative control for deleting chart error. Not a physical chart.
    cases = []
    for q in (2, 4, 8, 16):
        r = F(1, 10*q)
        before = [F(1, q)] * q + [F(0)]
        after = before.copy()
        for k in range(0, q, 2):
            after[k] -= r
            after[k+1] += r
        discrepancy = sum(abs(a-b) for a, b in zip(before, after))
        mismatch = (q//2) * r
        require(sum(after) == 1 and min(after) >= 0, 'Invalid probability vector')
        require(discrepancy == 2*mismatch and discrepancy > 0, 'Cell coupling/negative control')
        # Q1=[0,1]^2 has r1=1/2; enclosing square translated is harmless.
        tube_bound = 8*r*(F(1, 2)+r)*(q+1)
        require(mismatch <= tube_bound, 'Explicit tube union bound')
        cases.append({'q': q, 'r': str(r), 'L1': str(discrepancy), 'mismatch': str(mismatch)})
    # Exercise the printed finite design prescription with moderate supplied
    # observation tolerances. This is not evaluation of an unknown A_m.
    eta, e, r1, Cbin, H, Coff, Cchi, tau, C0 = .02, .03, .5, 4., 3., 2., 5., .75, 2.
    L, alpha, J0, h0, a = 8, .01, 20, .05, .1
    q = max(1, math.ceil(8*Cbin*r1/eta)); delta = 2*r1/q
    J = max(2, J0)
    J += J % 2
    while 2*C0*tau**J > eta/32:
        J += 2
    h = min(h0/2, a/2, J*e/4, eta/(64*Coff), (r1/Cchi)**2,
            (eta/(1024*H*r1*(q+1)*Cchi))**2)
    r = Cchi*math.sqrt(h)
    V = 8*r*(r1+r)*(q+1)
    b = 2*C0*tau**J + 2*Coff*h + 2*H*V
    K = q*q+1
    n = math.ceil(64/eta**2 * (math.sqrt(K)+math.sqrt(2*math.log(L/alpha)))**2)
    u = math.sqrt(K/n)+math.sqrt(2*math.log(L/alpha)/n)
    selection = min(e/2, eta/4)
    gap = 2*h/J+selection
    hist = 2*(u+b)+Cbin*delta+selection
    require(J % 2 == 0 and J >= J0 and h > 0, 'Finite same-flight prescription')
    require(Cbin*delta <= eta/4*(1+1e-12), 'Mesh budget')
    require(2*Coff*h <= eta/32*(1+1e-12), 'Timing budget')
    require(2*H*V <= eta/32*(1+1e-12), 'Chart budget')
    require(u <= eta/8*(1+1e-12) and b <= 3*eta/32*(1+1e-12), 'Sampling/bias budget')
    require(gap <= e and hist <= 15*eta/16*(1+1e-12), 'Final inverse arguments')
    # Union bound for four distinct error events uses no independence.
    return {'quadratic_cap_TV': '(D-d)/(D+d)', 'programmed_offset_TV': str(amplified),
            'exact_cell_cases': cases, 'cell_scope': 'Functional bounded-displacement maps, not billiard realizations.',
            'finite_design': {'q': q, 'J': J, 'h': h, 'n': n,
                              'gap_argument': gap, 'gap_budget': e,
                              'histogram_argument': hist, 'histogram_budget': eta},
            'scope': 'Finite algebra and inequalities; no infinite-orbit or minimax certification.'}


def main() -> None:
    print(json.dumps({'status': 'passed', 'mathematical_certification': False,
                      'preservation': preservation(), 'diagnostics': finite_diagnostics()},
                     indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
