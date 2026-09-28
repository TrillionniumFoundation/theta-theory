#!/usr/bin/env python3
"""A2 v92 source audit and finite diagnostics; not a formal proof checker.
Run from any directory with Python 3.10+, numpy and sympy. No network access.
The optional --output is the only diagnostic output file written by this script.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "papers/A2-v17-boundary-information-coarsening"
PIN = "aa6798d9030a7f75e95488441fec6058e52c566a"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def source_audit() -> dict:
    active: dict[str, bytes] = {}
    def visit(path: Path) -> None:
        key = path.relative_to(BASE).as_posix()
        require(key not in active, f"Repeated or circular input: {key}")
        active[key] = path.read_bytes()
        for name in re.findall(r"\\input\{([^}]+)\}", active[key].decode()):
            visit(BASE / name)
    visit(BASE / "rigidity_v92.tex")
    manifest = json.loads(Path(__file__).with_name("SOURCE_MANIFEST.json").read_text())
    require(manifest["source_pin"] == PIN, "Incorrect source pin")
    require(set(active) == set(manifest["active_sources"]), "Active graph/manifest mismatch")
    for name, data in active.items():
        expected = manifest["active_sources"][name]
        require(hashlib.sha256(data).hexdigest() == expected["sha256"], f"Hash mismatch: {name}")
    for name, expected in manifest["inherited_git_blobs"].items():
        require(blob((BASE / name).read_bytes()) == expected, f"Inherited file changed: {name}")
    for name, expected in manifest["verification_sources"].items():
        require(hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == expected, f"Verifier hash: {name}")
    text = "\n".join(data.decode() for data in active.values())
    labels = re.findall(r"\\label\{([^}]+)\}", text)
    refs = set(re.findall(r"\\(?:ref|eqref)\{([^}]+)\}", text))
    bib = set(re.findall(r"\\bibitem\{([^}]+)\}", text))
    cites = {k.strip() for group in re.findall(r"\\cite\{([^}]+)\}", text) for k in group.split(",")}
    require(all(n == 1 for n in Counter(labels).values()), "Duplicate labels")
    require(refs <= set(labels), f"Missing references: {refs - set(labels)}")
    require(cites <= bib, f"Missing bibliography: {cites - bib}")
    old = (BASE / "article/v91/intrinsic_modulus.tex").read_text()
    new = (BASE / "article/v92/intrinsic_modulus.tex").read_text()
    require(re.findall(r"\\label\{([^}]+)\}", old) == re.findall(r"\\label\{([^}]+)\}", new), "Inherited modulus labels removed")
    return {"active_files": len(active), "labels": len(labels), "bibliography_entries": len(bib),
            "inherited_blobs_verified": len(manifest["inherited_git_blobs"])}


def forward(theta: np.ndarray, d: int, nodes: np.ndarray) -> np.ndarray:
    u, v = np.vstack([theta[:2], 1-theta[:2]]), np.vstack([theta[2:4], 1-theta[2:4]])
    weights = np.r_[theta[4], 1-theta[4]]
    co = theta[5:].reshape(2, d)
    fs = nodes[:, None]**d + sum(nodes[:, None]**j * co[:, j] for j in range(d))
    probs = fs * weights / (fs @ weights)[:, None]
    return np.array([u @ np.diag(p) @ v.T for p in probs]).reshape(-1)


def theta_for(a: float, b: float, roots: np.ndarray, alpha: float = .5) -> np.ndarray:
    co = np.array([np.poly(r)[::-1][:-1] for r in roots])
    return np.r_[(1+a)/2, (1-a)/2, (1+b)/2, (1-b)/2, alpha, co.ravel()]


def geometry(theta: np.ndarray, d: int, nodes: np.ndarray) -> tuple:
    p = forward(theta, d, nodes)
    require(p.min() > 0, "Cell positivity")
    step = 1e-25
    j = np.column_stack([forward(theta.astype(complex) + 1j*step*v, d, nodes).imag/step for v in np.eye(len(theta))])
    h = np.repeat(1/len(nodes), len(p))/p
    white = np.sqrt(h)[:, None]*j
    left, singular, right = np.linalg.svd(white, full_matrices=False)
    require(singular[-1] > 1e-13*singular[0], "Diagnostic chart too ill-conditioned")
    return p, j, h, white, singular, right


def affine_conditions(theta: np.ndarray, nodes: np.ndarray) -> tuple:
    p, j, h, white, singular, right = geometry(theta, 1, nodes)
    g = np.zeros((2, 7)); g[:, 5:] = -np.eye(2)
    root_map = (g @ right.T)/singular
    cov = root_map @ root_map.T
    condition = float(np.sqrt(np.diag(cov).max()))
    u, v = np.vstack([theta[:2], 1-theta[:2]]), np.vstack([theta[2:4], 1-theta[2:4]])
    alpha = np.array([theta[4], 1-theta[4]])
    B = sum(np.linalg.norm(np.linalg.inv(v.T) @ np.diag(np.eye(2)[i]/alpha) @ np.linalg.inv(u), 2) for i in range(2))
    W = np.column_stack([np.ones(len(nodes)), nodes])
    Q, _ = np.linalg.qr(W, mode="complete")
    tau = np.linalg.norm(Q[:, 2:].T @ p.reshape(-1, 4))
    return condition, float(B + 1/tau), (p, j, h, singular, right, g, cov)


def regular_bridge() -> dict:
    nodes = np.array([0., .5, 2., 4.])
    theta = theta_for(.6, .45, np.array([[-2.], [-.5]]), .4)
    c, eta_inverse, (p, j, h, singular, right, g, cov) = affine_conditions(theta, nodes)
    row = int(np.argmax(np.diag(cov)))
    direction = right.T @ ((right @ g[row])/singular**2)
    direction /= np.sqrt(np.sum(h*(j @ direction)**2))
    eps = 1e-6/np.linalg.norm(direction)
    plus, minus = theta+eps*direction, theta-eps*direction
    hp = np.sqrt(np.mean(np.sum((np.sqrt(forward(plus, 1, nodes).reshape(-1, 4))-np.sqrt(p.reshape(-1, 4)))**2, axis=1)))
    hm = np.sqrt(np.mean(np.sum((np.sqrt(forward(minus, 1, nodes).reshape(-1, 4))-np.sqrt(p.reshape(-1, 4)))**2, axis=1)))
    distance = np.max(np.abs(np.sort(-plus[5:])-np.sort(-minus[5:])))
    ratio = distance/max(hp, hm)/(4*c)
    require(abs(ratio-1) < 2e-5, "Regular Hellinger factor four")
    angle = np.linspace(0, 2*np.pi, 100001)
    errors = []
    for epsilon in (.1, .5, 1.):
        ordered = np.sort(np.vstack([np.cos(angle), epsilon*np.sin(angle)]), axis=0)
        diameter = np.max(ordered.max(axis=1)-ordered.min(axis=1))
        exact = 1+epsilon/np.sqrt(1+epsilon**2)
        errors.append(abs(diameter-exact))
    require(max(errors) < 7e-5, "Collision quotient formula")
    return {"paired_radius_ratio_over_4c": ratio, "collision_grid_max_error": max(errors), "Fisher_condition": c}


def binary_normal_form() -> dict:
    z, h, x, a, b, epsilon = sp.symbols("z h x a b epsilon", real=True)
    U = sp.Matrix([[1+a, 1-a], [1-a, 1+a]])/2
    V = sp.Matrix([[1+b, 1-b], [1-b, 1+b]])/2
    K = U*sp.diag(z-h-x, z-h+x)*V.T/2
    P = K/(z-h)
    signs = sp.Matrix([1, -1]); ones = sp.ones(2, 1)
    require(sp.simplify((signs.T*P*ones)[0]+a*x/(z-h)) == 0, "ax moment")
    require(sp.simplify((ones.T*P*signs)[0]+b*x/(z-h)) == 0, "bx moment")
    require(sp.simplify((signs.T*P*signs)[0]-a*b) == 0, "ab moment")
    E = epsilon*signs*signs.T/4
    target = (a*b*((z-h)**2-x*x)+epsilon*(z-h))/4
    require(sp.expand((K+E).det()-target) == 0 and sum(E) == 0, "Admissible determinant tangent")
    for d in (1, 2, 3, 5):
        chi = ((z-h-x)**d-(z-h+x)**d)/((z-h-x)**d+(z-h+x)**d)
        require(sp.simplify(sp.diff(chi, x).subs(x, 0)+d/(z-h)) == 0, "Contrast leading term")
    nodes = np.array([0., .4, 1., 2., 4.])
    records = []
    for exponents in ((1, 1, 1), (1, 2, 1), (1, 1, 2), (1, 2, 3)):
        pexp, qexp, rexp = exponents
        # The channel-dominated arc enters its asymptotic regime later.
        grid = np.array([.02, .01, .005, .0025]) if exponents == (1, 2, 1) else np.array([.14, .10, .07, .05])
        values, ratios = [], []
        for s in grid:
            av, bv, xv = .8*s**pexp, .7*s**qexp, .6*s**rexp
            theta = theta_for(av, bv, np.array([[-1-xv], [-1+xv]]))
            c, eta, _ = affine_conditions(theta, nodes)
            scale = 1/(av*bv)+1/(xv*np.sqrt(av*av+bv*bv))
            values.append(c); ratios.append(c/scale)
            require(c <= 10*eta, "Condition/certificate bound")
        slope = -float(np.log(values[-1]/values[-2])/np.log(grid[-1]/grid[-2]))
        expected = max(pexp+qexp, rexp+min(pexp, qexp))
        require(abs(slope-expected) < .15, f"Phase slope {exponents}: {slope}")
        require(max(ratios)/min(ratios) < 1.5, "Nonuniform phase diagnostic")
        records.append({"arc": list(exponents), "predicted_exponent": expected, "last_slope": slope,
                        "condition_over_scale_range": [min(ratios), max(ratios)]})
    return {"exact_moment_and_determinant_identities": True, "arcs": records}


def vanishing_cell_floor() -> dict:
    nodes = np.array([0., .5, 2., 4.])
    base = theta_for(.6, .45, np.array([[-2.], [-.5]]), .4)
    records = []
    for epsilon in (.1, .03, .01, .003, .001, .0003, .0001):
        theta = base.copy(); theta[:2] = 1-epsilon*(1-base[:2])
        c, eta, _ = affine_conditions(theta, nodes)
        records.append({"epsilon": epsilon, "c_sqrt_epsilon": c*np.sqrt(epsilon),
                        "eta_inverse_times_epsilon": eta*epsilon, "c_over_eta_inverse": c/eta})
    require(records[-1]["c_over_eta_inverse"] < .13*records[0]["c_over_eta_inverse"], "Reverse-comparison separation")
    require(max(r["c_sqrt_epsilon"] for r in records[-3:])/min(r["c_sqrt_epsilon"] for r in records[-3:]) < 1.05, "Fisher thinning order")
    return {"row_thinning": records}


def quartic_profile() -> dict:
    nodes = np.array([0., .3, 1., 2., 4.])
    roots = np.array([[-1., -1.], [-2., -.25]])
    theta = theta_for(.65, .4, roots, .45)
    p, j, h, white, singular, right = geometry(theta, 2, nodes)
    N = np.zeros((9, 8)); N[:5, :5] = np.eye(5)
    N[5:7, 5] = [1, 1]; N[7:9, 6] = [.25, 1]; N[7:9, 7] = [2, 1]
    D = np.zeros(9); D[5] = 1
    coefficients = np.linalg.lstsq(white @ N, white @ D, rcond=None)[0]
    a0 = N @ coefficients
    residual = white @ (D-a0)
    S = float(residual @ residual)
    require(S > 0 and len(singular) == 9, "Repeated-root ambient rank / Schur positivity")
    constant = np.sqrt(2)*S**(-.25)
    ratios = []
    for s in (.01, .005, .0025, .00125):
        new = theta+s*s*a0
        shifted = roots.copy()
        shifted[0] = [-1-s-s*s*coefficients[5]/2, -1+s-s*s*coefficients[5]/2]
        for i, r in enumerate(roots[1]):
            deriv = -(a0[7]+a0[8]*r)/(2*r+theta[8])
            shifted[1, i] += s*s*deriv
        new[5:] = np.array([np.poly(rr)[::-1][:-1] for rr in shifted]).ravel()
        pn = forward(new, 2, nodes)
        require(pn.min() > 0 and np.all((new[:5] > 0) & (new[:5] < 1)), "Profile path admissibility")
        distance = np.max(np.abs(np.sort(shifted.ravel())-np.sort(roots.ravel())))
        hell = np.sqrt(np.mean(np.sum((np.sqrt(pn.reshape(-1, 4))-np.sqrt(p.reshape(-1, 4)))**2, axis=1)))
        ratios.append(float(distance/np.sqrt(hell)/constant))
    require(abs(ratios[-1]-1) < .01, f"Quartic leading constant: {ratios}")
    crossover = []
    for delta in (0., 1e-6, 1e-3, .02):
        for t in (1e-10, 1e-7, 1e-4, 1e-2):
            displacement = t/(np.sqrt(delta*delta+t)+delta)
            scale = t/(delta+np.sqrt(t))
            crossover.append(displacement/scale)
    require(min(crossover) >= .49 and max(crossover) <= 1.01, "Double-root crossover")
    return {"ambient_rank": 9, "profiled_S": S, "predicted_constant": constant,
            "path_ratio_to_constant": ratios, "crossover_ratio_range": [min(crossover), max(crossover)]}


def flag_cancellation_and_exposure() -> dict:
    z, epsilon = sp.symbols("z epsilon", real=True)
    T = sp.Matrix([[z*z, z, 1], [0, z*z, z], [0, 0, z*z]])
    inverse = T.inv()
    require(inverse[0, 2] == 0 and inverse[0, 1] == -z**-3, "Exact flag cancellation")
    L = (sp.eye(3)+sp.ones(3))/4
    M = L*T*L.T/3
    q = sum(M)
    require(sp.expand(q-z*z-sp.Rational(2, 3)*z-sp.Rational(1, 3)) == 0, "Cancellation example normalization")
    e1, e2, e3 = sp.eye(3)[:, 0], sp.eye(3)[:, 1], sp.eye(3)[:, 2]
    perturbation = e2*(e1-e2).T
    E = L*perturbation*L.T/3
    require(sum(E) == 0, "Zero-sum exposed perturbation")
    det_ratio = sp.cancel((T+epsilon*perturbation).det()/T.det())
    require(sp.simplify(det_ratio-(1+epsilon*((e1-e2).T*inverse*e2)[0])) == 0, "Rank-one determinant lemma")
    floors = [float((M+sp.Rational(1, 10000)*E)[i, j].subs(z, n)/q.subs(z, n)) for n in range(1, 6) for i in range(3) for j in range(3)]
    require(min(floors) > 0, "Positive normalized cancellation family")
    examples = []
    for k in (2, 3, 4):
        J = sp.zeros(k)
        for i in range(k-1): J[i, i+1] = 1
        diagonal = sp.diag(*range(1, k+1))
        Tn = z*z*sp.eye(k)+z*diagonal+J
        require(diagonal*J-J*diagonal != sp.zeros(k), "Noncommuting coefficients")
        leading = Tn.inv().applyfunc(lambda entry: sp.limit(z**k*entry, z, 0))
        expected = (-1)**(k-1)/sp.factorial(k)
        require(leading[0, k-1] == expected, "Noncommuting leading Laurent term")
        u, v = sp.eye(k)[:, k-1], sp.eye(k)[:, 0]-sp.eye(k)[:, k-1]
        require(sum(u*v.T) == 0 and (v.T*leading*u)[0] != 0, "Flag exposure")
        # The maximally confluent diagonal has order kd, here d=2.
        Td = z*z*sp.eye(k)+J
        lead_d = sp.limit(z**(2*k)*Td.inv()[0, k-1], z, 0)
        require(lead_d == (-1)**(k-1), "Sharp kd path")
        examples.append({"k": k, "noncommuting_pole_order": k, "confluent_pole_order": 2*k})
    return {"uncorrected_path_count": 6, "actual_pole_order": 3,
            "positive_cell_floor": min(floors), "rank_one_identity": str(det_ratio), "sharp_examples": examples}


def legacy_diagnostics() -> dict:
    result = subprocess.run([sys.executable, str(ROOT / "revisions/a2-v91/verify_a2_v91.py")],
                            capture_output=True, text=True, check=True, timeout=90)
    data = json.loads(result.stdout)
    require(data["status"] == "passed", "Legacy diagnostic status")
    return data


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    results = {"status": "passed", "scope": "Finite symbolic/numerical diagnostics, not formal proof verification",
               "source_pin": PIN, "source_audit": source_audit(),
               "regular_bridge": regular_bridge(), "binary_normal_form": binary_normal_form(),
               "vanishing_cell_floor": vanishing_cell_floor(), "quartic_profile": quartic_profile(),
               "flag_cancellation_and_exposure": flag_cancellation_and_exposure(),
               "legacy_v91": legacy_diagnostics(),
               "versions": {"python": sys.version.split()[0], "numpy": np.__version__, "sympy": sp.__version__}}
    text = json.dumps(results, indent=2, sort_keys=True)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
