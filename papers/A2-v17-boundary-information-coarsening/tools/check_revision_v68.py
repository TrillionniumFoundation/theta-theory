#!/usr/bin/env python3
"""A2 v68 source retention and scoped exact controls, not a proof certificate.

Only the standard library is used. The previous pure mathematical control
routine is deliberately reused; this is not an independent referee checker.
"""
from __future__ import annotations
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import re
import stat

from check_revision_v67 import (
    require, blob, eye, inverse, matadd, matmul, matnorm,
    rational_checks as preceding_mathematical_controls,
)

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'history/v67-review-baseline'
NEW = 'article/10d_smooth_contact_rigidity_v68.tex'
EDITED = {
    'README.md', 'main.tex', 'rigidity.tex',
    'article/00_structural_introduction_v48.tex',
    'article/00g_contact_synthesis_v66.tex', 'article/00h_abstract_v66.tex',
    'article/10b_periodic_contact_inverse_v65.tex',
    'article/10c_global_curvature_inverse_v66.tex',
    'journal/00_principal_introduction_v61.tex',
}


def active(entry: str, old: bool = False, found: set[str] | None = None) -> set[str]:
    found = set() if found is None else found
    if entry in found:
        return found
    found.add(entry)
    path = (BASE if old and entry in EDITED else ROOT) / entry
    require(path.is_file(), 'Missing native input: ' + entry)
    text = re.sub(r'(?<!\\)%[^\n]*', '', path.read_text())
    for name in re.findall(r'\\(?:input|include)\s*\{([^}]+)\}', text):
        active(name if name.endswith('.tex') else name + '.tex', old, found)
    return found


def source_checks() -> dict:
    records = json.loads((BASE / 'SOURCE_MANIFEST.json').read_text())['files']
    require(len(records) == 855, 'Unexpected v67 baseline size')
    unchanged, archived, labels, readonly = 0, [], 0, 0
    for name, rec in records.items():
        current = ROOT / name
        require(current.is_file() and not current.is_symlink(), 'Removed inherited source: ' + name)
        expected = BASE / name if name in EDITED else current
        data = expected.read_bytes()
        require(len(data) == rec['bytes'] and hashlib.sha256(data).hexdigest() == rec['sha256']
                and blob(data) == rec['git_blob'], 'Baseline byte identity failed: ' + name)
        mode = int(rec['mode'], 8) & 0o777
        actual_mode = stat.S_IMODE(current.stat().st_mode)
        archive_mode = stat.S_IMODE(expected.stat().st_mode)
        if actual_mode == 0o444 and archive_mode == 0o444:
            readonly += 1  # freeze_git_source deliberately makes every snapshot file read-only.
        else:
            require(actual_mode == mode and archive_mode == mode, 'Mode changed: ' + name)
        if name in EDITED:
            require(current.read_bytes() != data, 'Unnecessarily archived unedited path: ' + name)
            archived.append(name)
            if name.endswith('.tex'):
                now = current.read_text()
                for label in re.findall(r'\\label\{([^}]+)\}', data.decode()):
                    require('\\label{' + label + '}' in now, 'Removed inherited label: ' + label)
                    labels += 1
        else:
            unchanged += 1
    require(set(archived) == EDITED, 'Archive inventory mismatch')
    require(readonly in (0, len(records)), 'Mixed immutable/working-tree mode policy')
    old = {e: active(e + '.tex', True) for e in ('main', 'rigidity', 'two_collision')}
    new = {e: active(e + '.tex') for e in old}
    for e in old:
        expected = {NEW} if e != 'two_collision' else set()
        require(old[e] <= new[e] and new[e] - old[e] == expected,
                'Unintended active-input change: ' + e)
    smooth = (ROOT / NEW).read_text()
    needed = ('lem:v68-real-visits', 'prop:v68-weighted-separation',
              'thm:v68-smooth-rigidity', 'lem:v68-finite-comparison',
              'thm:v68-smooth-stability', 'prop:v68-flat-family',
              'eq:v68-integrated-envelope', 'eq:v68-flat-signal')
    for label in needed:
        require('\\label{' + label + '}' in smooth, 'Missing new proof statement: ' + label)
    old_correction = (ROOT / 'article/10c_global_curvature_inverse_v66.tex').read_text()
    for label in ('eq:v67-residual-error', 'eq:v67-complete-stopping-error',
                  'eq:v67-off-fixed-recursion', 'eq:v67-propagation-constants'):
        require('\\label{' + label + '}' in old_correction, 'Lost v67 correction: ' + label)
    return {'inherited_files': len(records), 'inherited_unchanged': unchanged,
            'edited_originals_archived_exactly': sorted(archived),
            'inherited_labels_retained_in_edited_tex': labels,
            'active_by_entry': {e: len(v) for e, v in new.items()},
            'active_union': len(set().union(*new.values())),
            'old_active_union': len(set().union(*old.values())),
            'sole_added_active_input': NEW,
            'mode_scope': ('Read-only frozen copies; original Git modes checked by the source manifest and materializer'
                           if readonly else 'Original filesystem modes verified against the reviewed manifest')}


def scale(a, q):
    return [[q * x for x in row] for row in a]


def diagonal(xs):
    return [[x if i == j else F(0) for j in range(len(xs))] for i, x in enumerate(xs)]


def weighted_controls() -> dict:
    matrices = comparisons = thresholds = 0
    orders = []
    for r in range(2, 7):
        for seed, a in enumerate((F(2, 3), F(3, 4), F(4, 5), F(5, 6))):
            m = 3
            while 6 * a**m / (1 - a**m) >= 1:
                m += 1
            require(a**m < F(1, 7), 'Threshold equivalence failed')
            if m > 3:
                require(a**(m-1) >= F(1, 7), 'Chosen order is not minimal')
            thresholds += 1
            orders.append(m)
            for n in (m, m+1, m+3):
                theta = 6 * a**n / (1-a**n)
                sig = [(-1 if (i+seed) % 3 == 0 else 1) * a * F(7+(i+seed) % 3, 10)
                       for i in range(r)]
                t = [[F(0) for _ in range(r)] for _ in range(r)]
                for i in range(r):
                    t[i][(i+1) % r] = sig[i]**n
                alpha = [F(1, 2) + F((i+seed) % 5, 8) for i in range(r)]
                weight = [F(1) + F((i+seed) % 5, 2) for i in range(r)]
                tail = matmul(diagonal(weight), matmul(t, inverse(matadd(eye(r), t, -1))))
                require(matnorm(tail) <= 3*a**n/(1-a**n), 'Weighted tail bound failed')
                operator = matadd(diagonal(alpha), tail)
                inv = inverse(operator)
                bound = 2/(1-theta)
                require(matnorm(inv) <= bound, 'Separating inverse bound failed')
                require(matmul(inv, operator) == eye(r), 'Exact inverse identity failed')
                matrices += 1
                for j in range(3):
                    h = [[F((-1)**(i+j)*(i+j+1), r+1)] for i in range(r)]
                    g = matmul(operator, h)
                    require(matnorm(h) <= bound*matnorm(g), 'Functional finite control failed')
                    comparisons += 1
    # The weaker C*rho^j bound is compatible with an expansive first visit.
    c, rho = F(2), F(3, 4)
    require(c*rho > 1, 'Invalid negative control')
    require(all(c**m*rho**m/(1-rho**m) > 1 for m in range(2, 40)),
            'Constant-one negative control failed')
    return {'positive_class_thresholds': thresholds, 'minimal_orders': sorted(set(orders)),
            'signed_cyclic_inverse_controls': matrices,
            'finite_vector_separation_controls': comparisons,
            'constant_one_negative_control': True,
            'scope': 'Exact finite operator models; not actual globally realized billiards'}


def nonlinear_visit_controls() -> dict:
    # Real nonlinear maps X(u)=s*u/(1+b*u), fixing zero.  On |u|<=R their
    # derivative magnitude is at most |s|/(1-|b|R)^2, strictly below a.
    total = weighted = 0
    R, a = F(1, 5), F(3, 4)
    specs = ((F(1, 2), F(1, 4)), (-F(2, 5), -F(1, 3)),
             (F(3, 7), F(2, 5)))
    for s, b in specs:
        require(abs(s)/(1-abs(b)*R)**2 < a, 'Bad nonlinear contraction margin')
    for numerator in range(-10, 11):
        if numerator == 0:
            continue
        u = R*F(numerator, 10)
        x = u
        for j in range(1, 25):
            s, b = specs[(j-1) % len(specs)]
            x = s*x/(1+b*x)
            require(abs(x) <= a**j*abs(u), 'Composition contraction failed')
            total += 1
            for m in (7, 8, 11):
                require(abs(x**m/u**m) <= a**(j*m), 'Nonlinear weighted evaluation failed')
                weighted += 1
        for m in (7, 8, 11):
            finite = sum((3*a**(j*m) for j in range(1, 25)), F(0))
            remainder = 3*a**(25*m)/(1-a**m)
            require(finite+remainder == 3*a**m/(1-a**m), 'Infinite-tail certificate identity failed')
    return {'nonlinear_composition_samples': total, 'weighted_samples': weighted,
            'finite_tail_plus_geometric_remainder': True,
            'scope': 'Finite rational nonlinear maps, not a replacement for actual half-line uniqueness'}


def polynomial_and_quotient_controls() -> dict:
    aligned = quotients = 0
    for a in (F(1, 3), F(1, 2), F(2, 3)):
        for m in range(3, 12):
            h = {n: F((-1)**n*(n+1), 11) for n in range(2, m+4)}
            # Exact action of the endpoint-multiplicity model on monomials.
            action = {n: c*(1+a**n)/(1-a**n) for n, c in h.items()}
            recovered = {n: c*(1-a**n)/(1+a**n) for n, c in action.items()}
            require(h == recovered, 'Signed-jet scalar model inverse failed')
            polynomial = {n: c for n, c in h.items() if n < m}
            residual = {n: c for n, c in h.items() if n >= m}
            require(set(polynomial).isdisjoint(residual) and polynomial | residual == h,
                    'Jet alignment failed')
            require(all(n >= m for n in residual), 'Residual has a low jet')
            aligned += 1
    # f_d = amplitude*(d-H)/Z_d. Both amplitude and unknown normalizers cancel.
    for d1 in (F(1), F(3, 2), F(2)):
        for d2 in (F(3), F(4)):
            for H in (F(0), F(1, 11), F(2, 7)):
                for amp in (F(2, 3), F(7, 5)):
                    z1,z2,amp0 = F(7, 4),F(11, 6),F(1)
                    f1,f2 = amp*(d1-H)/z1,amp*(d2-H)/z2
                    f10,f20 = amp0*d1/z1,amp0*d2/z2
                    q = f1*f20/(f2*f10)
                    got = d1*d2*(1-q)/(d2-d1*q)
                    require(got == H, 'Two-offset action extraction failed')
                    quotients += 1
    return {'polynomial_alignment_models': aligned, 'two_offset_cancellation_controls': quotients}


def flat_controls() -> dict:
    # d^n/du^n exp(-1/u^2)=P_n(1/u) exp(-1/u^2).
    # P_(n+1)=2*z^3*P_n-z^2*P_n'. Every finite polynomial is killed by the exponential.
    p = {0: 1}
    records = []
    for n in range(25):
        require(p[max(p)] == 2**n and max(p) == 3*n, 'Flat leading derivative coefficient failed')
        records.append({'order': n, 'degree': max(p), 'leading_coefficient': p[max(p)]})
        q = {}
        for degree, coeff in p.items():
            q[degree+3] = q.get(degree+3, 0) + 2*coeff
            if degree:
                q[degree+1] = q.get(degree+1, 0) - degree*coeff
        p = {degree: coeff for degree, coeff in q.items() if coeff}
    inequalities = 0
    for a in (F(1, 3), F(1, 2), F(3, 4), F(9, 10)):
        for j in range(1, 51):
            require(a**(-2*j)-1 >= j*(a**(-2)-1), 'Flat tail Bernoulli inequality failed')
            inequalities += 1
    return {'derivative_recurrences': len(records), 'derivative_records': records,
            'flat_tail_exponent_inequalities': inequalities,
            'scope': 'Finite algebraic checks; flatness and the actual area correction are proved in the text'}


def main() -> None:
    result = {'revision': 68, 'status': 'passed', 'source': source_checks(),
              'new_controls': {'weighted': weighted_controls(),
                               'nonlinear_visits': nonlinear_visit_controls(),
                               'polynomial_and_two_offset': polynomial_and_quotient_controls(),
                               'flat': flat_controls()},
              'retained_v67_mathematical_controls': preceding_mathematical_controls(),
              'scope': 'Source retention and scoped finite diagnostics. Not a proof certificate, global billiard realization, or independent referee computation.'}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
