#!/usr/bin/env python3
"""Retention and independent finite controls for the v65 periodic contact inverse.

Finite arithmetic/geometry diagnostics are not proofs of the limiting action,
Banach-space inverse, analytic continuation, or exceptional significance.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import re
import sys
import numpy as np
import sympy as sp
from scipy.linalg import solve_banded
from source_provenance import require, graph, strip_comments
from check_revision_v64 import transfer_controls, geometric_controls

ROOT = Path(__file__).resolve().parents[1]
MODIFIED = {
    'main.tex', 'rigidity.tex', 'README.md',
    'article/00_structural_introduction_v48.tex',
    'journal/00_principal_introduction_v61.tex',
    'article/00e_periodic_mechanism_overview_v64.tex',
    'journal/references_v56.tex',
}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def preservation() -> dict:
    archive = ROOT/'history/v64-review-baseline'
    manifest = json.loads((archive/'SOURCE_MANIFEST.json').read_text())
    files = manifest['files']
    changed = []
    for name, info in sorted(files.items()):
        target = ROOT/name
        require(target.is_file(), f'Inherited path missing: {name}')
        old = archive/name if name in MODIFIED else target
        data = old.read_bytes()
        blob = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        require(len(data) == info['bytes'] and sha(data) == info['sha256']
                and blob == info['git_blob'], f'Baseline differs: {name}')
        if target.read_bytes() != data:
            changed.append(name)
    require(set(changed) == MODIFIED, 'Unexpected set of modified inherited files')

    def old_graph(entry: str) -> set[str]:
        seen: set[str] = set()
        def visit(name: str) -> None:
            if name in seen:
                return
            require(name in files, 'Baseline input absent: '+name)
            seen.add(name)
            path = archive/name if name in MODIFIED else ROOT/name
            for child in re.findall(r'\\input\{([^}]+)\}', strip_comments(path.read_text())):
                visit(child if child.endswith('.tex') else child+'.tex')
        visit(entry)
        return seen
    old_all: set[str] = set()
    new_all: set[str] = set()
    counts = {}
    for entry in ('main.tex', 'rigidity.tex', 'two_collision.tex'):
        old = old_graph(entry)
        # Match the retained recorder engine's definition of active TeX inputs.
        current = set(graph(ROOT, entry))
        old_all |= old
        new_all |= current
        require(old <= current, 'An inherited active mathematical input was removed')
        counts[entry] = {'baseline': len(old), 'current': len(current)}
    require(len(files) == 800 and len(old_all) == 129 and len(new_all) == 131,
            'Unexpected baseline or active source census')
    new = (ROOT/'article/10b_periodic_contact_inverse_v65.tex').read_text()
    statements = len(re.findall(r'\\begin\{(?:lemma|proposition|theorem|corollary)\}', new))
    require(statements == 9, 'Unexpected new statement count')
    active_text = '\n'.join((ROOT/p).read_text() for p in sorted(new_all))
    labels = re.findall(r'\\label\{([^}]+)\}', strip_comments(active_text))
    for entry in ('main.tex', 'rigidity.tex', 'two_collision.tex'):
        text = '\n'.join((ROOT/p).read_text() for p in graph(ROOT, entry))
        entry_labels = re.findall(r'\\label\{([^}]+)\}', strip_comments(text))
        require(len(entry_labels) == len(set(entry_labels)), 'Duplicate label within '+entry)
    needed = re.findall(r'\\(?:ref|eqref)\{(.*?v65[^}]+)\}', active_text)
    require(set(needed) <= set(labels), 'Undefined v65 reference')
    return {'baseline_source': manifest['source_commit'], 'inherited_files': len(files),
            'unchanged_inherited_files': len(files)-len(changed),
            'modified_files_with_byte_exact_archives': sorted(changed),
            'active_inputs': counts, 'distinct_old_active': len(old_all),
            'distinct_new_active': len(new_all), 'new_section_statements': statements,
            'scope': 'All inherited mathematical proof modules, including the complete v64 periodic forward section, are byte-identical; entry points and listed framing files have exact archives.'}


def cyclic_controls() -> dict:
    cases = signed_controls = 0
    for r in range(2, 8):
        for pattern in range(3):
            sig = [sp.Rational(i+2, 3*i+9)*(-1 if (pattern == 1 or (pattern == 2 and i % 2 == 0)) else 1)
                   for i in range(r)]
            lam = sp.prod(sig)
            for n in range(2, 10):
                T = sp.zeros(r)
                for b in range(r):
                    T[b, (b+1) % r] = sig[b]**n
                I = sp.eye(r)
                C = (I+T)*(I-T).inv()
                # Independent visit enumeration, summing each phase's full turns.
                visits = I.copy()
                for b in range(r):
                    weight = sp.S.One
                    for j in range(1, r+1):
                        weight *= sig[(b+j-1) % r]**n
                        visits[b, (b+j) % r] += 2*weight/(1-lam**n)
                require(C == visits, 'Cyclic block differs from direct visit sum')
                require(C.det() == (1-(-1)**r*lam**n)/(1-lam**n), 'Signed determinant')
                require((I-T)*(I+T).inv()*C == I, 'Cyclic inverse')
                require(T**r == lam**n*I, 'Return identity')
                a = max(abs(x) for x in sig)**n
                bound = (1+a)/(1-a)
                for mat in (C, C.inv()):
                    require(max(sum(abs(mat[i, j]) for j in range(r)) for i in range(r)) <= bound,
                            'Block norm bound')
                if pattern and n % 2:
                    tabs = abs(T)
                    require((I+tabs)*(I-tabs).inv() != C, 'Odd-degree sign control not detected')
                    signed_controls += 1
                # Incorrectly counting the endpoint twice gives a different response.
                require(visits+I != C, 'Endpoint multiplicity control')
                cases += 1
    return {'exact_rational_blocks': cases, 'physical_cycle_lengths': list(range(2, 8)),
            'degrees': list(range(2, 10)), 'odd_degree_orientation_negative_controls': signed_controls,
            'endpoint_multiplicity_negative_controls': cases}


def quadratic_solution(k: np.ndarray, c: np.ndarray, eps: np.ndarray, b: int, N: int=120):
    r = len(c)
    idx = (b+np.arange(N+1)) % r
    diag = k[idx[1:-1]-1]+k[idx[1:-1]]+2*c[idx[1:-1]]
    off = -eps[idx[1:-2]]*k[idx[1:-2]]
    ab = np.zeros((3, N-1)); ab[1] = diag; ab[0, 1:] = off; ab[2, :-1] = off
    rhs = np.zeros(N-1); rhs[0] = eps[b]*k[b]
    x = np.r_[1., solve_banded((1, 1), ab, rhs), 0.]
    value = k[b]+c[b]-eps[b]*k[b]*x[1]
    return value, x


def curvature_controls() -> dict:
    derivative_error = visit_error = 0.
    entries = phases = 0
    for r in (2, 3, 4, 5, 6):
        k = np.array([.7+.13*i for i in range(r)])
        c = np.array([.22+.071*((2*i+1) % r) for i in range(r)])
        for signs in (1, -1):
            eps = np.full(r, signs)
            sig = np.array([quadratic_solution(k, c, eps, b)[1][1] for b in range(r)])
            T = np.zeros((r, r))
            for b in range(r): T[b, (b+1) % r] = sig[b]**2
            C = np.linalg.solve((np.eye(r)-T).T, (np.eye(r)+T).T).T
            for b in range(r):
                _, x = quadratic_solution(k, c, eps, b)
                require(0 < abs(sig[b]) < 1, 'Contracting signed Jacobi step')
                for t in range(r):
                    direct = float(b == t)+2*sum(x[j]**2 for j in range(1, len(x)-1) if (b+j) % r == t)
                    visit_error = max(visit_error, abs(C[b, t]-direct))
                    step = 2e-5
                    cp = c.copy(); cm = c.copy(); cp[t] += step; cm[t] -= step
                    fd = (quadratic_solution(k, cp, eps, b)[0]-quadratic_solution(k, cm, eps, b)[0])/(2*step)
                    derivative_error = max(derivative_error, abs(fd-C[b, t]))
                    entries += 1
                phases += 1
    require(visit_error < 1e-12 and derivative_error < 2e-8, 'Curvature Jacobian disagrees with action Hessian')
    return {'phase_solutions': phases, 'curvature_jacobian_entries': entries,
            'max_finite_difference_error': format(derivative_error, '.4e'),
            'max_direct_visit_error': format(visit_error, '.4e'),
            'finite_chain_length': 120}


class GraphTriangle:
    """Actual Euclidean chords in fixed projection sensors, not Jacobi surrogates."""
    def __init__(self, skew: bool):
        self.q = np.array([[0., 0.], [.79, 0.], [.37 if skew else .395, .71 if skew else .79*np.sqrt(3)/2]])
        self.n = np.empty((3, 2)); self.t = np.empty((3, 2))
        self.length = np.linalg.norm(np.roll(self.q, -1, axis=0)-self.q, axis=1)
        self.e0 = (np.roll(self.q, -1, axis=0)-self.q)/self.length[:, None]
        for i in range(3):
            v = self.e0[i]-self.e0[(i-1) % 3]
            self.n[i] = v/np.linalg.norm(v)
            self.t[i] = [-self.n[i, 1], self.n[i, 0]]
        self.nu = np.sum(self.n*self.e0, axis=1)
        self.p = np.sum(self.t*self.e0, axis=1)/self.nu
        self.coef = np.array([[1.1, .23, -.07], [1.25, -.19, .1], [1.03, .11, .05]])

    def point(self, i: int, x: float):
        i %= 3; c, d, f = self.coef[i]
        F = c*x*x/2+d*x**3/6+f*x**4/24
        F1 = c*x+d*x*x/2+f*x**3/6; F2 = c+d*x+f*x*x/2
        return (self.q[i]+(self.t[i]*x-self.n[i]*F)/self.nu[i],
                (self.t[i]-self.n[i]*F1)/self.nu[i], -self.n[i]*F2/self.nu[i])

    def edge(self, i: int, x: float, y: float):
        a, ax, axx = self.point(i, x); b, by, byy = self.point(i+1, y)
        diff = b-a; length = np.linalg.norm(diff); e = diff/length
        ex, ey = np.dot(e, ax), np.dot(e, by)
        return (length, -ex, ey, (ax@ax-ex*ex)/length-e@axx,
                -(ax@by-ex*ey)/length, (by@by-ey*ey)/length+e@byy, e)

    def bridge(self, b: int, u: float, N: int=60):
        x = np.zeros(N+1); x[0] = u
        for it in range(16):
            ed = [self.edge(b+j, x[j], x[j+1]) for j in range(N)]
            g = np.array([ed[j-1][2]+ed[j][1] for j in range(1, N)])
            if np.max(abs(g)) < 3e-14: break
            diag = np.array([ed[j-1][5]+ed[j][3] for j in range(1, N)])
            off = np.array([ed[j][4] for j in range(1, N-1)])
            ab = np.zeros((3, N-1)); ab[1] = diag; ab[0, 1:] = off; ab[2, :-1] = off
            x[1:-1] -= solve_banded((1, 1), ab, g)
        require(np.max(abs(g)) < 1e-12, 'Actual chord stationarity')
        value = sum(ed[j][0]-self.length[(b+j) % 3]+self.p[(b+j) % 3]*x[j]-self.p[(b+j+1) % 3]*x[j+1] for j in range(N))
        return value, x, ed, float(np.max(abs(g)))


def chord_envelope_controls() -> dict:
    max_error = max_residual = hess_error = 0.; cases = 0
    for skew in (False, True):
        model = GraphTriangle(skew)
        for b in range(3):
            e = model.edge(b, 0., 0.)
            expected = [1/model.length[b]+model.coef[b, 0], 1/model.length[b], 1/model.length[b]+model.coef[(b+1) % 3, 0]]
            hess_error = max(hess_error, np.max(abs(np.array(e[3:6])-expected)))
            for u in (-.027, .019):
                _, x, edges, residual = model.bridge(b, u)
                max_residual = max(max_residual, residual)
                for t in range(3):
                    for degree in (2, 3):
                        fac = 2 if degree == 2 else 6
                        direct = ((edges[0][6]@model.n[b])/model.nu[b])*u**degree/fac if b == t else 0.
                        for j in range(1, len(x)-1):
                            i = (b+j) % 3
                            if i == t:
                                weight = (edges[j][6]-edges[j-1][6])@model.n[i]/model.nu[i]
                                direct += weight*x[j]**degree/fac
                        step = 1e-4
                        model.coef[t, degree-2] += step; vp = model.bridge(b, u)[0]
                        model.coef[t, degree-2] -= 2*step; vm = model.bridge(b, u)[0]
                        model.coef[t, degree-2] += step
                        fd = (vp-vm)/(2*step)
                        max_error = max(max_error, abs(fd-direct))
                        cases += 1
    require(hess_error < 2e-13 and max_error < 2e-8, 'Euclidean chord envelope or scaled Hessian mismatch')
    return {'actual_models': ['equilateral-fixed-normal-graphs', 'scalene-fixed-normal-graphs'],
            'nonlinear_envelope_comparisons': cases, 'variation_degrees': [2, 3],
            'flights': 60, 'max_envelope_finite_difference_error': format(max_error, '.4e'),
            'max_stationarity_residual': format(max_residual, '.4e'),
            'max_scaled_edge_hessian_error': format(hess_error, '.4e')}


def offset_controls() -> dict:
    # Rational polynomial amplitudes and actions on a rational square.  Exact
    # normalizers are integrated; there is no hidden equality between offsets.
    u, v = sp.symbols('u v')
    cases = axis_cases = gauge_controls = 0
    for momentum in (sp.Rational(1, 5), sp.Rational(-2, 7)):
        Sm = u*u+u**3/3; Sp = 3*v*v/2-v**3/4
        A = Sm-momentum*u; C = Sp+momentum*v
        Bm = 1+u/3+u*u; Bp = 1-v/4+v*v/2
        d1, d2 = sp.Rational(1, 8), sp.Rational(1, 5)
        raw = [Bm*Bp*(d-A-C) for d in (d1, d2)]
        Z = [sp.integrate(expr, (u, -sp.Rational(1, 20), sp.Rational(1, 20)),
                          (v, -sp.Rational(1, 20), sp.Rational(1, 20))) for expr in raw]
        require(Z[0] != Z[1] and min(Z) > 0, 'Unequal physical normalizers')
        f = [expr/z for expr, z in zip(raw, Z)]
        for uu in map(sp.Rational, ('-1/25', '-1/50', '0', '1/50', '1/25')):
            for vv in map(sp.Rational, ('-1/25', '-1/50', '0', '1/50', '1/25')):
                val = [expr.subs({u: uu, v: vv}) for expr in f]
                origin = [expr.subs({u: 0, v: 0}) for expr in f]
                require(min(val) > 0, 'Positive window floor')
                Q = val[0]*origin[1]/(val[1]*origin[0])
                H = d1*d2*(1-Q)/(d2-d1*Q)
                require(H == (A+C).subs({u: uu, v: vv}), 'Two-offset action recovery')
                if uu != vv:
                    require(H != (Sm+Sp).subs({u: uu, v: vv}), 'Physical gauge negative control')
                    gauge_controls += 1
                cases += 1
            for d, ff in zip((d1, d2), f):
                origin = ff.subs({u: 0, v: 0})
                require(ff.subs({u: uu, v: 0})/origin*d/(d-A.subs(u, uu)) == Bm.subs(u, uu), 'Future amplitude')
                require(ff.subs({u: 0, v: uu})/origin*d/(d-C.subs(v, uu)) == Bp.subs(v, uu), 'Past amplitude')
                axis_cases += 2
    return {'exact_rational_two_offset_points': cases, 'exact_amplitude_axis_checks': axis_cases,
            'oblique_physical_gauge_negative_controls': gauge_controls,
            'normalization': 'Each density has its own exact integral on the positive square.'}


def main() -> None:
    result = {'schema': 'a2-v65-retention-and-finite-controls-1', 'status': 'passed',
              'preservation': preservation(), 'signed_cyclic_blocks': cyclic_controls(),
              'curvature_inverse': curvature_controls(), 'actual_chord_envelope': chord_envelope_controls(),
              'two_offset_extraction': offset_controls(),
              'retained_v64_transfer_controls': transfer_controls(),
              'retained_v64_geometric_controls': geometric_controls(),
              'limits': 'Exact finite algebra, floating-point finite geometric diagnostics, and byte retention. Not an infinite-dimensional proof certificate, exhaustive novelty audit, or editorial acceptance.'}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
