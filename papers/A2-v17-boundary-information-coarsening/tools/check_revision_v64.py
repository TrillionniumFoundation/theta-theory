#!/usr/bin/env python3
"""Fail-closed source retention and finite geometric controls for A2 v64.

These controls do not certify infinite-dimensional proofs or journal significance.
Ordinary and optimized Python execute the same checks (no removable assertions).
"""
from __future__ import annotations
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import re
import numpy as np
from scipy.linalg import solve_banded
from source_provenance import graph, strip_comments, INPUT, require

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / 'history/v63-review-baseline'
MODIFIED = {'README.md', 'main.tex', 'rigidity.tex',
            'article/00_structural_introduction_v48.tex',
            'journal/00_principal_introduction_v61.tex'}
NEW_INPUTS = {'article/00e_periodic_mechanism_overview_v64.tex',
              'article/10a_periodic_itinerary_relative_v64.tex'}


def blob(data: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def base_bytes(name: str) -> bytes:
    return ((ARCHIVE if name in MODIFIED else ROOT) / name).read_bytes()


def base_graph(name: str, seen: set[str] | None = None) -> set[str]:
    seen = set() if seen is None else seen
    if name in seen:
        return seen
    seen.add(name)
    for raw in INPUT.findall(strip_comments(base_bytes(name).decode())):
        require(re.fullmatch(r'[A-Za-z0-9_./-]+', raw) is not None, 'Dynamic baseline input')
        base_graph(raw if raw.endswith('.tex') else raw + '.tex', seen)
    return seen


def preservation() -> dict:
    mf = json.loads((ARCHIVE / 'SOURCE_MANIFEST.json').read_text())
    require(mf['source_commit'] == 'f5517519440b897707ddc60deeafba19e86bb5a5', 'Wrong baseline')
    require(mf['source_tree'] == 'b042811c7ceb2c5fd841b2a03ab0b8c232c39dce', 'Wrong baseline tree')
    require(len(mf['files']) == 784, 'Unexpected baseline inventory')
    changed = []
    for name, meta in mf['files'].items():
        p = ROOT / name
        require(p.is_file() and not p.is_symlink(), 'Inherited path missing: ' + name)
        require(bool(p.stat().st_mode & 0o111) == (meta['mode'] == '100755'), 'Mode change: ' + name)
        original = base_bytes(name)
        require((len(original), hashlib.sha256(original).hexdigest(), blob(original)) ==
                (meta['bytes'], meta['sha256'], meta['git_blob']), 'Baseline bytes: ' + name)
        if p.read_bytes() != original:
            require(name in MODIFIED, 'Unapproved inherited change: ' + name)
            changed.append(name)
    require(set(changed) == MODIFIED, 'Changed-path authorization mismatch')
    old, new = set(), set()
    for stem in ('main', 'rigidity', 'two_collision'):
        old |= base_graph(stem + '.tex')
        new |= graph(ROOT, stem + '.tex')
    require(len(old) == 127 and old <= new and new - old == NEW_INPUTS, 'Active proof retention')
    stat = 'article/23f2_finite_experiment_analytic_inverse_v62.tex'
    require((ROOT / stat).read_bytes() == base_bytes(stat), 'Finite-experiment source changed')
    require(r'\label{eq:v63-pilot-time}' in (ROOT / stat).read_text(), 'Ceiling correction lost')
    bodies = re.findall(r'\\begin\{(?:theorem|lemma|corollary|proposition)\}', (ROOT / stat).read_text())
    require(len(bodies) == 5, 'Finite-experiment statement inventory changed')
    # Exact insertion only in the two inherited introductions.
    insertion = '\\input{article/00e_periodic_mechanism_overview_v64}\n\n'
    for name in ('journal/00_principal_introduction_v61.tex', 'article/00_structural_introduction_v48.tex'):
        require((ROOT / name).read_text().replace(insertion, '') == base_bytes(name).decode(),
                'Introduction exceeds authorized shared insertion: ' + name)
    return {'inherited_files_retained': 784, 'inherited_byte_identical': 784 - len(changed),
            'archived_originals': len(changed), 'modified_paths': sorted(changed),
            'inherited_active_inputs': len(old), 'current_active_inputs': len(new),
            'added_active_inputs': sorted(new - old), 'unchanged_finite_experiment_statements': 5}


def mm(a, b):
    return [[sum(a[i][s]*b[s][j] for s in range(2)) for j in range(2)] for i in range(2)]


def transfer_controls() -> dict:
    cases = 0
    eye = [[F(1), F(0)], [F(0), F(1)]]
    for period in (2, 4, 6):
        for seed in range(1, 7):
            k = [F(seed + i + 2, i + 2) for i in range(period)]
            m = [F(2*seed + i + 1, i + 3) for i in range(period)]
            for b in range(period):
                ks = [k[(b+i) % period] for i in range(period)]
                ms = [m[(b+i) % period] for i in range(period)]
                M = eye
                for ki, mi in zip(ks, ms):
                    M = mm([[1+mi/ki, 1/ki], [mi, F(1)]], M)
                require(M[0][0]*M[1][1]-M[0][1]*M[1][0] == 1, 'Transfer determinant')
                trace = M[0][0]+M[1][1]
                require(trace > 2, 'Positive Floquet exponent')
                power = eye
                U0, U1 = F(0), F(1)
                for n in range(1, 6):
                    power = mm(M, power)
                    N = n*period
                    diag = [ks[(i-1) % period] + ks[i % period] + ms[i % period]
                            for i in range(1, N)]
                    det_prev, det = F(1), diag[0]
                    for i in range(1, len(diag)):
                        det_prev, det = det, diag[i]*det-ks[i % period]**2*det_prev
                    product = F(1)
                    for i in range(N):
                        product *= ks[i % period]
                    require(product/det == 1/power[0][1], 'Cofactor/transfer exact identity')
                    require(power[0][1] == M[0][1]*U1, 'Cayley-Hamilton exact identity')
                    U0, U1 = U1, trace*U1-U0
                    cases += 1
    return {'exact_rational_transfer_cofactor_cases': cases, 'periods': [2, 4, 6],
            'maximum_repetitions': 5}


class Triangle:
    """Actual circular obstacles constructed from a scalene contact triangle."""
    def __init__(self, skew: bool):
        ell = 2.5-np.sqrt(3.0)
        q = np.array([[0., 0.], [ell, 0.], [ell/2, np.sqrt(3.)*ell/2]])
        if skew:
            q[1] += [0.022, -0.008]
            q[2] += [-0.014, 0.027]
        self.radii = np.array([1., 1.025, .985]) if skew else np.ones(3)
        normals, nus = [], []
        for i in range(3):
            a, b = q[(i-1) % 3]-q[i], q[(i+1) % 3]-q[i]
            a, b = a/np.linalg.norm(a), b/np.linalg.norm(b)
            nuvec = (a+b)/np.linalg.norm(a+b)
            normals.append(nuvec)
            nus.append(np.dot(b, nuvec))
        self.normals = np.array(normals)
        self.nu = np.array(nus)
        self.centers = q-self.radii[:, None]*self.normals
        self.q = q
        self.lengths = np.array([np.linalg.norm(q[(i+1) % 3]-q[i]) for i in range(3)])
        self.k = 1/self.lengths
        self.m = 2/(self.radii*self.nu)
        for i in range(3):
            for j in range(i):
                require(np.linalg.norm(self.centers[i]-self.centers[j]) > self.radii[i]+self.radii[j],
                        'Actual disks overlap')
            a, b = q[(i+1) % 3], q[(i+2) % 3]
            t = np.clip(np.dot(self.centers[i]-a, b-a)/np.dot(b-a, b-a), 0, 1)
            require(np.linalg.norm(self.centers[i]-(a+t*(b-a))) > self.radii[i], 'Third disk blocks flight')

    def chart(self, i, x):
        j = i % 3
        sign = (-1.)**i
        angle = sign*x/(self.nu[j]*self.radii[j])
        ca, sa = np.cos(angle), np.sin(angle)
        n = self.normals[j]
        rot = np.array([ca*n[0]-sa*n[1], sa*n[0]+ca*n[1]])
        tangent = sign*np.array([-rot[1], rot[0]])/self.nu[j]
        return self.centers[j]+self.radii[j]*rot, tangent, -rot/(self.radii[j]*self.nu[j]**2)

    def edge(self, i, x, y):
        a, t, aa = self.chart(i, x)
        b, s, bb = self.chart(i+1, y)
        diff = b-a
        length = np.linalg.norm(diff)
        e = diff/length
        et, es = np.dot(e, t), np.dot(e, s)
        xx = (np.dot(t, t)-et**2)/length-np.dot(e, aa)
        yy = (np.dot(s, s)-es**2)/length+np.dot(e, bb)
        xy = -(np.dot(t, s)-et*es)/length
        return length, -et, es, xx, xy, yy

    def bridge(self, N, u, v):
        x = np.zeros(N+1)
        x[0], x[-1] = u, v
        for iteration in range(30):
            e = np.array([self.edge(i, x[i], x[i+1]) for i in range(N)])
            grad = e[:-1, 2]+e[1:, 1]
            diag = e[:-1, 5]+e[1:, 3]
            off = e[1:-1, 4]
            if np.max(np.abs(grad)) < 5e-14:
                break
            band = np.zeros((3, N-1))
            band[1] = diag
            band[0, 1:] = off
            band[2, :-1] = off
            x[1:-1] -= solve_banded((1, 1), band, grad)
        require(np.max(np.abs(grad)) < 2e-12, 'Finite stationary solve residual')
        # Stable log determinant, not finite differences of an exponentially small twist.
        pivot = diag[0]
        require(pivot > 0 and np.all(e[:, 4] < 0), 'Positivity/twist failure')
        logdet = np.log(pivot)
        for i in range(1, N-1):
            pivot = diag[i]-off[i-1]**2/pivot
            require(pivot > 0, 'Positive tridiagonal pivots')
            logdet += np.log(pivot)
        logflux = np.log(-e[:, 4]).sum()-logdet
        return float(logflux), float(e[:, 0].sum()), x


def geometric_controls() -> dict:
    hess_error = stationarity = factor_error = 0.
    hessian_cases = bridge_cases = gauge_cases = 0
    raw_twists = []
    for skew in (False, True):
        model = Triangle(skew)
        for i in range(6):
            e = model.edge(i, 0., 0.)
            ki, mi, mj = model.k[i % 3], model.m[i % 3], model.m[(i+1) % 3]
            hess_error = max(hess_error, np.max(np.abs(np.array(e[3:])-[ki+mi/2, -ki, ki+mj/2])))
            stationarity = max(stationarity, abs(model.edge(i-1, 0., 0.)[2]+e[1]))
            hessian_cases += 1
        require(hess_error < 5e-13 and stationarity < 5e-14, 'Geometric Hessian/reflection identity')
        p = -model.edge(0, 0., 0.)[1]
        # The physical residual is not the residual for the gauged action.
        for u, v in ((.013, -.017), (-.019, .011), (.005, .014)):
            N = 12
            logf, W, x = model.bridge(N, u, v)
            ref = sum(model.lengths)*N/3
            E = W-ref+p*u-p*v
            actual = ref+.08-W
            gauged = .08-E+p*u-p*v
            require(abs(actual-gauged) < 2e-14, 'Restored endpoint gauge')
            require(abs(actual-(.08-E)) > 1e-4, 'Oblique-gauge negative control not detected')
            gauge_cases += 1
        Nbig = 48
        log0, _, _ = model.bridge(Nbig, 0., 0.)
        for u, v in ((.013, -.017), (-.019, .011), (.005, .014), (.012, .009)):
            logleft = model.bridge(Nbig, u, 0.)[0]-log0
            logright = model.bridge(Nbig, 0., v)[0]-log0
            target = logleft+logright
            for N in (6, 12, 18, 24):
                logbase = model.bridge(N, 0., 0.)[0]
                current = model.bridge(N, u, v)[0]-logbase
                err = abs(np.expm1(current-target))
                if N >= 18:
                    factor_error = max(factor_error, err)
                require(err < (.001 if N == 6 else 2e-6), 'Two-ended relative finite control')
                bridge_cases += 1
            raw_twists.append(float(np.exp(model.bridge(24, 0., 0.)[0])))
    require(factor_error < 2e-9, 'Long-bridge factorization tolerance')
    # Format reported floats deterministically; they are diagnostics, not rigorous enclosures.
    return {'actual_orbit_models': ['equilateral-three-disk', 'scalene-unequal-three-disk'],
            'geometric_edge_hessian_cases': hessian_cases,
            'max_hessian_error': format(hess_error, '.4e'),
            'max_reflection_residual': format(stationarity, '.4e'),
            'two_ended_bridge_comparisons': bridge_cases,
            'max_relative_factorization_error_N_ge_18': format(factor_error, '.4e'),
            'oblique_gauge_checks_and_negative_controls': gauge_cases,
            'reference_twist_24_flights_range': [format(min(raw_twists), '.4e'), format(max(raw_twists), '.4e')]}


def main() -> None:
    result = {'schema': 'a2-v64-source-and-finite-geometric-controls-1', 'status': 'passed',
              'preservation': preservation(), 'exact_controls': transfer_controls(),
              'floating_point_geometric_controls': geometric_controls(),
              'limits': 'Finite controls and source retention, not an infinite-dimensional proof, exhaustive priority investigation, or editorial certification.'}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
