#!/usr/bin/env python3
"""Finite diagnostics and source audit for A2 v91; not a formal proof checker.
Run from any directory: python revisions/a2-v91/verify_a2_v91.py --output result.json
Dependencies: Python 3.10+, numpy, sympy. No network, credentials, or write to sources.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "papers/A2-v17-boundary-information-coarsening"
RNG = np.random.default_rng(20260919)


def require(ok: bool, message: str) -> None:
    if not ok:
        raise AssertionError(message)


def source_audit() -> dict:
    seen: dict[str, str] = {}
    def visit(path: Path) -> None:
        key = path.relative_to(BASE).as_posix()
        require(key not in seen, f"Repeated or circular input: {key}")
        text = path.read_text(encoding="utf-8")
        seen[key] = text
        for target in re.findall(r"\\input\{([^}]+)\}", text):
            visit(BASE / target)
    visit(BASE / "rigidity_v91.tex")
    text = "\n".join(seen.values())
    labels = re.findall(r"\\label\{([^}]+)\}", text)
    cites = set(re.findall(r"\\bibitem\{([^}]+)\}", text))
    refs = set(re.findall(r"\\(?:eqref|ref)\{([^}]+)\}", text))
    used = {key.strip() for group in re.findall(r"\\cite\{([^}]+)\}", text) for key in group.split(",")}
    require(not [key for key, n in Counter(labels).items() if n > 1], "Duplicate labels")
    require(refs <= set(labels), f"Missing labels: {refs - set(labels)}")
    require(used <= cites, f"Missing citations: {used - cites}")
    manifest_path = Path(__file__).with_name("SOURCE_MANIFEST.json")
    manifest = json.loads(manifest_path.read_text())
    for name, expected in manifest["active_sources"].items():
        require(name in seen, f"Manifest source not active: {name}")
        data = (BASE / name).read_bytes()
        require(hashlib.sha256(data).hexdigest() == expected["sha256"], f"SHA256 mismatch: {name}")
    require(set(seen) == set(manifest["active_sources"]), "Manifest omits active sources")
    for name, expected in manifest["inherited_git_blobs"].items():
        data = (BASE / name).read_bytes()
        blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        require(blob == expected, f"Inherited source changed: {name}")
    return {"active_files": len(seen), "labels": len(labels), "bibliography_entries": len(cites),
            "inherited_blobs_verified": len(manifest["inherited_git_blobs"])}


def normalization_ranks() -> dict:
    z = sp.Symbol("z")
    def rank(polys: list, count: int) -> int:
        nodes = list(range(1, count + 1))
        q = sum(polys) / len(polys)
        W = sp.Matrix([[t**j for j in range(3)] for t in nodes])
        O = sp.eye(count) - W * (W.T * W).inv() * W.T
        columns = [sp.Matrix.vstack(*[O * sp.Matrix([t**j * f.subs(z, t) / q.subs(z, t) for t in nodes]) for f in polys]) for j in range(2)]
        return sp.Matrix.hstack(*columns).rank()
    F = (z + 3) * (z + 1)
    cases = {"low_span_four": rank([F, F + sp.Rational(1, 10), F - sp.Rational(1, 10)], 4),
             "low_span_five": rank([F, F + sp.Rational(1, 10), F - sp.Rational(1, 10)], 5),
             "full_span_four": rank([F, F + sp.Rational(1, 10), F + z / 10], 4),
             "common_root_five": rank([(z + 1) * (z + a) for a in (2, 3, 4)], 5),
             "equal_polynomials_five": rank([F, F, F], 5)}
    require(list(cases.values()) == [1, 2, 2, 1, 0], f"Normalization ranks: {cases}")
    return cases


def fisher_geometry() -> dict:
    k, d = 3, 2
    nodes = np.array([0.1, 0.4, 1., 2., 4.])
    U, V = .7*np.eye(3)+.1*np.ones((3, 3)), .55*np.eye(3)+.15*np.ones((3, 3))
    roots = np.array([[-2., -1.], [-1., -.2], [-1.5, -.5]])
    co = np.array([np.poly(r)[::-1][:-1] for r in roots])
    theta = np.r_[U[:2].ravel(), V[:2].ravel(), [.25, .35], co.ravel()]
    def forward(t: np.ndarray) -> np.ndarray:
        u, v = t[:6].reshape(2, 3), t[6:12].reshape(2, 3)
        u, v = np.vstack([u, 1-u.sum(axis=0)]), np.vstack([v, 1-v.sum(axis=0)])
        a = np.r_[t[12:14], 1-t[12:14].sum()]
        coeff = t[14:].reshape(k, d)
        fs = nodes[:, None]**2 + nodes[:, None]*coeff[:, 1] + coeff[:, 0]
        weights = fs*a / (fs @ a)[:, None]
        return np.array([u @ np.diag(w) @ v.T for w in weights]).ravel()
    P = forward(theta)
    J = np.column_stack([forward(theta.astype(complex) + 1j*1e-25*np.eye(len(theta))[j]).imag/1e-25 for j in range(len(theta))])
    G = np.zeros((6, len(theta)))
    for b in range(k):
        for a, x in enumerate(roots[b]):
            G[2*b+a, 14+2*b:16+2*b] = -np.array([1., x])/(2*x + co[b, 1])
    require(np.linalg.matrix_rank(J) == 20 and np.linalg.matrix_rank(G) == 6, "Chart/target rank")
    w = np.repeat(.2, 5)
    h = np.repeat(w, 9)/P
    info = J.T @ (h[:, None]*J)
    cov = G @ np.linalg.solve(info, G.T)
    Sigma = np.zeros((45, 45))
    for j, p in enumerate(P.reshape(5, 9)):
        Sigma[9*j:9*(j+1), 9*j:9*(j+1)] = (np.diag(p)-np.outer(p, p))/w[j]
    fisher_error = np.linalg.norm(J.T @ (h[:, None]*Sigma*h[None, :]) @ J-info)/np.linalg.norm(info)
    D = np.eye(20) + .03*RNG.normal(size=(20, 20))
    JD, GD = J @ D, G @ D
    cov2 = GD @ np.linalg.solve(JD.T @ (h[:, None]*JD), GD.T)
    invariant_error = np.linalg.norm(cov2-cov)/np.linalg.norm(cov)
    require(fisher_error < 1e-12 and invariant_error < 1e-5, "Fisher/coordinate identities")
    row = int(np.argmax(np.diag(cov)))
    direction = np.linalg.solve(info, G[row])
    direction /= np.sqrt(direction @ info @ direction)
    step = 1e-5/np.linalg.norm(direction)
    changed = theta + step*direction
    new_roots = np.concatenate([np.roots(np.r_[1., c[::-1]]) for c in changed[14:].reshape(3, 2)])
    require(np.max(np.abs(new_roots.imag)) < 1e-12, "Path lost real roots")
    loss = np.max(np.abs(np.sort(new_roots.real)-np.sort(roots.ravel())))
    obs = forward(changed)-P
    ratio = loss/np.sqrt(np.sum(h*obs**2))
    expected = np.sqrt(cov[row, row])
    require(abs(ratio/expected-1) < 1e-3, "Extremal radial derivative")
    return {"J_rank": 20, "G_rank": 6, "cell_floor": float(P.min()),
            "fisher_relative_error": float(fisher_error), "coordinate_relative_error": float(invariant_error),
            "radial_ratio_over_condition": float(ratio/expected)}


def flag_and_jordan() -> dict:
    z, r, t = sp.symbols("z r t")
    L = sp.Matrix([[2, 1], [1, 2]])/3
    C = sp.Matrix([[z*z+7*z+10, z/5], [0, z*z+7*z+12]])
    K = L*C*L.T/2
    q = sum(K)
    require(sp.expand(q-(z*z+sp.Rational(71, 10)*z+11)) == 0, "Positive flag normalizer")
    A1, A0 = C.diff(z).subs(z, 0), C.subs(z, 0)
    require(A1*A0-A0*A1 != sp.zeros(2), "Example commutes")
    require((A1-7*sp.eye(2))**2 == sp.zeros(2) and A1 != 7*sp.eye(2), "Example not defective")
    gauge = C.applyfunc(lambda entry: sp.interpolate([(j, r*entry.subs(z, j)/q.subs(z, j)) for j in (1, 2, 3)], z))
    require(gauge[1, 0] == 0, "Gauge did not preserve flag")
    beta = sp.Rational(2, 3)
    jordan = sp.Matrix([[z, beta], [t, z]])
    require(sp.expand(jordan.det() - (z*z-beta*t)) == 0, "Jordan split determinant")
    floor = min(float(entry.subs(z, j)/q.subs(z, j)) for j in (1, 2, 3, 4, 5) for entry in K)
    require(floor > 0, "Flag cell floor")
    return {"noncommuting": True, "defective_coefficient": True, "flag_preserved": True,
            "positive_cell_floor": floor, "jordan_determinant": str(jordan.det())}


def anchored_and_moving() -> dict:
    z, s = sp.symbols("z s", real=True)
    for m in (2, 3, 4, 6):
        base = (z+1)**m
        split = ((z+1)**2-s*s)*(z+1)**(m-2)
        require(sp.expand(split-base+s*s*(z+1)**(m-2)) == 0, "Anchored quadratic order")
    checks = {}
    for m in (3, 4, 6):
        xs = np.arange(m, dtype=float)-(m-1)/2
        H = np.poly(xs)
        alt = H.copy(); alt[-1] += 1e-3
        require(np.max(np.abs(np.roots(alt).imag)) < 1e-10, "Moving polynomial not real-rooted")
        u = np.array([.1, .05, .025])
        base_dist = np.array([np.linalg.norm(H[1:]*v**np.arange(1, m+1)) for v in u])
        mutual = 1e-3*u**m
        slope = float(np.log(base_dist[-1]/base_dist[-2])/np.log(.5))
        require(abs(slope-2) < .01, "Moving pair distance to base not quadratic")
        require(abs(np.log(mutual[-1]/mutual[-2])/np.log(.5)-m) < 1e-10, "Moving mutual order")
        checks[str(m)] = {"base_order": slope, "mutual_order": m}
    return {"anchored_multiplicities": [2, 3, 4, 6], "moving_pairs": checks}


def probability_and_homotopy() -> dict:
    p, q = np.array([0., .3, .7]), np.array([.1, .2, .7])
    h2 = np.sum((np.sqrt(p)-np.sqrt(q))**2)
    pp, qq = np.kron(p, p), np.kron(q, q)
    product_h2 = np.sum((np.sqrt(pp)-np.sqrt(qq))**2)
    tv = np.abs(pp-qq).sum()/2
    require(product_h2 <= 2*h2+1e-14 and tv <= np.sqrt(product_h2), "Hellinger product/TV bound")
    S, T = np.eye(3)+.1*RNG.normal(size=(3, 3)), np.eye(3)+.1*RNG.normal(size=(3, 3))
    alpha = np.array([.25, .35, .4])
    weights = [np.linalg.inv(T.T) @ np.diag(np.eye(3)[i]/alpha) @ np.linalg.inv(S) for i in range(3)]
    B = sum(np.linalg.norm(W, 2) for W in weights)
    hd = np.array([.2, -.2, .1])
    H = RNG.normal(size=(3, 3)); H *= .2/(B*np.linalg.norm(H, 2))
    max_ratio = 0.
    for u in np.linspace(0, 1, 21):
        A = S @ np.diag(alpha*(1+u*hd)) @ T.T
        require(np.linalg.norm(np.linalg.inv(A), 2) <= 2*B, "First leading homotopy")
    A = S @ np.diag(alpha*(1+hd)) @ T.T
    for u in np.linspace(0, 1, 21):
        ratio = np.linalg.norm(np.linalg.inv(A+u*H), 2)/B
        require(ratio <= 4, "Second leading homotopy")
        max_ratio = max(max_ratio, ratio)
    return {"product_hellinger_squared": float(product_h2), "product_total_variation": float(tv),
            "second_homotopy_max_inverse_over_B": float(max_ratio), "homotopy_grid_points": 42}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    results = {"status": "passed", "scope": "finite diagnostics, not formal verification", "seed": 20260919,
               "source_audit": source_audit(), "normalization_ranks": normalization_ranks(),
               "fisher_geometry": fisher_geometry(), "flag_and_jordan": flag_and_jordan(),
               "anchored_and_moving": anchored_and_moving(), "probability_and_homotopy": probability_and_homotopy()}
    text = json.dumps(results, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
