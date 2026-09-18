#!/usr/bin/env python3
"""Finite checks for A2 v85. These checks do not replace the manuscript proofs."""
from __future__ import annotations
import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path
import re
import sys
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.special import expit


def charge_checks() -> dict:
    size = 4
    expected = {
        c for c in itertools.product(range(-2, 3), repeat=size)
        if sum(c) == 0 and 0 < sum(max(a, 0) for a in c) <= 2
    }
    realized = set()
    points = range(size + 1)  # The last point is an extra common anchor.
    for x, y, xp, yp in itertools.product(points, repeat=4):
        if x == y or xp == yp:
            continue
        c = [0] * (size + 1)
        for a, v in ((x, 1), (y, -1), (xp, -1), (yp, 1)):
            c[a] += v
        if c[-1] == 0 and any(c[:-1]):
            realized.add(tuple(c[:-1]))
    assert realized == expected
    checked = 0
    for simple in itertools.product((False, True), repeat=size):
        secant_obstruction = any(
            all(c[i] == 0 or simple[i] for i in range(size)) for c in expected
        )
        for double in itertools.product((False, True), repeat=size):
            polar_admissible = not secant_obstruction and not any(double)
            saturated_admissible = sum(simple) <= 1 and not any(double)
            assert polar_admissible == saturated_admissible
            checked += 1
    # A nonsaturated three-pole direction that passes the charge test.
    direction = (1, 3, -4, 0)
    def collinear(c: tuple[int, ...]) -> bool:
        t = Fraction(c[0], direction[0])
        return all(Fraction(a) == t * b for a, b in zip(c, direction))
    assert not any(collinear(c) for c in expected)
    assert (1, -1, 0, 0) in expected
    return {"charge_vectors": len(expected), "saturated_spaces_checked": checked,
            "common_anchor_realization": "pass", "nonsaturated_direction": "pass"}


def fibre_checks() -> dict:
    cases = []
    U = np.array([[0.70, 0.10], [0.20, 0.60], [0.10, 0.30]])
    V = np.array([[0.25, 0.75], [0.75, 0.25]])
    for q in (0, 1, 2, 4):
        clocks = np.arange(4.0, 4.0 + q + 2)
        def F(s: float) -> float:
            return quad(lambda a: float(1.0 / np.prod(clocks-a)), 0.0, s,
                        epsabs=2e-14, epsrel=2e-13)[0]
        max_scalar = 0.0
        max_matrix = 0.0
        extra_separation = []
        for x in (0.3, 0.8, 1.4, 1.9):
            tau, xt = 3.0, 1.04*x
            target = F(xt)-F(x)+F(tau)
            taut = brentq(lambda s: F(s)-target, 2.8, 3.2, xtol=2e-14)
            base = np.log(clocks-x)-np.log(clocks-tau)
            shifted = np.log(clocks-xt)-np.log(clocks-taut)
            coeff = np.polynomial.polynomial.polyfit(
                clocks[:q+1], (base-shifted)[:q+1], q)
            reconstructed = np.polynomial.polynomial.polyval(clocks, coeff)+shifted
            max_scalar = max(max_scalar, float(np.max(np.abs(reconstructed-base))))
            for a, b in zip(expit(base), expit(reconstructed)):
                P = U @ np.diag([a, 1-a]) @ V.T
                Q = U @ np.diag([b, 1-b]) @ V.T
                max_matrix = max(max_matrix, float(np.max(np.abs(P-Q))))
            tnew = clocks[-1]+1
            extra = (np.polynomial.polynomial.polyval(tnew, coeff)
                     +np.log(tnew-xt)-np.log(tnew-taut)
                     -np.log(tnew-x)+np.log(tnew-tau))
            extra_separation.append(abs(float(extra)))
        assert max_scalar < 1e-9
        assert max_matrix < 1e-10
        assert min(extra_separation) > 1e-12
        cases.append({"q": q, "max_scalar_residual": max_scalar,
                      "max_matrix_residual": max_matrix,
                      "minimum_extra_clock_separation": min(extra_separation)})
    return {"scaling_family_cases": cases}


def forward_checks() -> dict:
    rng = np.random.default_rng(850918)
    u, v, q = 3, 4, 2
    clocks = np.arange(4.0, 4.0+q+3)
    r0 = 4.0-3.4
    L = 2+0.5*max(np.sqrt(sum(t**(2*k) for k in range(q+1))+2/r0**2)
                  for t in clocks)
    def draw():
        return (rng.dirichlet(np.ones(u), 2).T,
                rng.dirichlet(np.ones(v), 2).T,
                rng.uniform(0, 2), rng.uniform(3, 3.4),
                rng.uniform(-0.02, 0.02, q+1))
    def vector(w):
        U, V, x, tau, c = w
        return np.r_[U.ravel(), V.ravel(), x, tau, c]
    def obs(w):
        U, V, x, tau, c = w
        f = np.polynomial.polynomial.polyval(clocks, c)+np.log(clocks-x)-np.log(clocks-tau)
        return [U @ np.diag([p, 1-p]) @ V.T for p in expit(f)]
    max_ratio = 0.0
    for _ in range(200):
        w, wp = draw(), draw()
        ratio = max(np.linalg.norm(a-b, 'fro') for a, b in zip(obs(w), obs(wp)))/np.linalg.norm(vector(w)-vector(wp))
        assert ratio <= L+1e-12
        max_ratio = max(max_ratio, float(ratio))
        U, V, *_ = w
        su, sv = np.linalg.svd(U, compute_uv=False)[1], np.linalg.svd(V, compute_uv=False)[1]
        for P in obs(w):
            sig = np.linalg.svd(P, compute_uv=False)[1]
            assert sig <= np.sqrt(2)*min(su, sv)+1e-12
    return {"forward_L": float(L), "largest_tested_ratio": max_ratio,
            "random_pairs_checked": 200}


def geometry_checks() -> dict:
    # First variations for g_theta = exp(2(theta_0+theta_1*x+theta_2*y)) g_Euclid.
    pairs = [((-1., 0.), (1., 0.)), ((0., 1.), (1., 0.)),
             ((0., -1.), (1., 0.))]
    rows = []
    for a, b in pairs:
        a, b = np.array(a), np.array(b)
        midpoint, length = (a+b)/2, np.linalg.norm(a-b)
        rows.append(length*np.r_[1., midpoint])
    A = np.array(rows)
    s = np.linalg.svd(A, compute_uv=False)[-1]
    assert s > 0.5
    # The budget balance h^2 = h^(-2(d-1))/N gives exponent 1/(2d).
    exponents = {str(d): str(Fraction(1, 2*d)) for d in (2, 3, 4)}
    return {"boundary_design_determinant": float(np.linalg.det(A)),
            "boundary_design_min_singular_value": float(s),
            "balanced_mesh_exponents": exponents}


def source_checks(base: Path) -> dict:
    inputs = re.compile(r'\\input\{([^}]+)\}')
    seen: set[Path] = set()
    def expand(path: Path) -> str:
        path = path.resolve()
        if not path.is_file():
            raise AssertionError(f"Missing TeX input: {path}")
        seen.add(path)
        text = re.sub(r'(?<!\\)%[^\n]*', '', path.read_text())
        return inputs.sub(lambda m: expand(base/(m.group(1)+('.tex' if not m.group(1).endswith('.tex') else ''))), text)
    principal = expand(base/'rigidity_v85.tex')
    principal_files = len(seen)
    labels = re.findall(r'\\label\{([^}]+)\}', principal)
    duplicate = [s for s, n in Counter(labels).items() if n > 1]
    assert not duplicate, duplicate
    refs = re.findall(r'\\(?:eqref|ref|pageref)\{([^}]+)\}', principal)
    missing = sorted(set(refs)-set(labels))
    assert not missing, missing
    bib = set(re.findall(r'\\bibitem(?:\[[^]]*\])?\{([^}]+)\}', principal))
    citations = set()
    for group in re.findall(r'\\cite(?:\[[^]]*\])?\{([^}]+)\}', principal):
        citations.update(s.strip() for s in group.split(','))
    assert citations <= bib, sorted(citations-bib)
    old = (base/'article/v84/01_rigidity.tex').read_text()
    new = (base/'article/v85/01_rigidity.tex').read_text()
    env = re.compile(r'\\begin\{(theorem|lemma|proposition|corollary|definition|proof)\}.*?\\end\{\1\}', re.S)
    normalize = lambda s: re.sub(r'\s+', '', s)
    new_blocks = Counter(normalize(m.group(0)) for m in env.finditer(new))
    old_blocks = Counter(normalize(m.group(0)) for m in env.finditer(old))
    assert old_blocks <= new_blocks, 'A mathematical block of v84/01 was changed or lost.'
    old_full = (base/'rigidity_v84_full.tex').read_text()
    new_full = (base/'rigidity_v85_full.tex').read_text()
    old_companion = old_full.split('\\appendix', 1)[1]
    new_companion = new_full.split('\\appendix', 1)[1]
    old_inputs = inputs.findall(old_companion)
    new_inputs = inputs.findall(new_companion)
    for p in old_inputs:
        assert p in new_inputs, f'Lost companion input: {p}'
    # Expanded references may have historical conventions; require its inputs to exist.
    expand(base/'rigidity_v85_full.tex')
    return {"principal_input_files": principal_files, "principal_labels": len(labels),
            "principal_references": len(refs), "bibliography_keys": len(bib),
            "preserved_mathematical_blocks_in_rewritten_module": sum(old_blocks.values()),
            "preserved_companion_inputs": len(old_inputs),
            "all_reachable_input_files": len(seen),
            "v85_sources_sha256": {str(p.relative_to(base)): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in sorted((base/'article/v85').glob('*.tex'))}}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--algebra-only', action='store_true')
    parser.add_argument('--base', type=Path, default=Path('.'))
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = {"purpose": "finite algebraic, numerical, and source consistency checks; not proof certification",
              "charges": charge_checks(), "fibres": fibre_checks(),
              "forward_model": forward_checks(), "geometric_design": geometry_checks()}
    if not args.algebra_only:
        result['sources'] = source_checks(args.base)
    result['status'] = 'PASS'
    text = json.dumps(result, indent=2, sort_keys=True)+'\n'
    if args.output:
        args.output.write_text(text)
    print(text, end='')


if __name__ == '__main__':
    main()
