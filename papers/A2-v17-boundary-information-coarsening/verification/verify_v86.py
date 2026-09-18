#!/usr/bin/env python3
"""Reproducible identities and source checks for A2 v86; not proof certification."""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import re
import subprocess
from typing import Any

import numpy as np
import sympy as sp

BASE_COMMIT = "65cd70c44e1bb5f679bd3e0397c6d66da139102c"
INCLUDE = re.compile(r"\\(?:input|include)\{([^}]+)\}")
LABEL = re.compile(r"\\label\{([^}]+)\}")
REF = re.compile(r"\\(?:ref|eqref|pageref|autoref)\{([^}]+)\}")
CITE = re.compile(r"\\cite(?:\[[^]]*\])?\{([^}]+)\}")
BIB = re.compile(r"\\bibitem(?:\[[^]]*\])?\{([^}]+)\}")


def exact_zero(expr: Any) -> None:
    values = list(expr) if isinstance(expr, sp.MatrixBase) else [expr]
    for value in values:
        assert sp.factor(value) == 0, sp.factor(value)


def symbolic_identities() -> dict[str, Any]:
    T, x, tau, r = sp.symbols("T x tau r", real=True)
    u, v, s, t = sp.symbols("u v s t", real=True)
    U, V = sp.Matrix([[u, v], [1-u, 1-v]]), sp.Matrix([[s, t], [1-s, 1-t]])
    C1, C2 = U[:, 0]*V[:, 0].T, U[:, 1]*V[:, 1].T
    h = r*x+(1-r)*tau
    P = r*(T-x)/(T-h)*C1+(1-r)*(T-tau)/(T-h)*C2
    exact_zero(P-(r*C1+(1-r)*C2+r*(1-r)*(tau-x)*(C1-C2)/(T-h)))
    K = r*(T-x)*C1+(1-r)*(T-tau)*C2
    exact_zero(K.det()-r*(1-r)*U.det()*V.det()*(T-x)*(T-tau))
    b, c = sp.symbols("b c")
    exact_zero((b*C1+c*C2).det()-b*c*U.det()*V.det())

    # The one-clock construction: signed auxiliary S, positive actual channels.
    p0, p1 = sp.symbols("p0 p1", positive=True)
    w0, w1, one = sp.Matrix([p0, 1-p0]), sp.Matrix([p1, 1-p1]), sp.ones(2, 1)
    S = sp.eye(2)+(w0-w1)*one.T
    Si = sp.eye(2)-(w0-w1)*one.T
    exact_zero(S*Si-sp.eye(2))
    exact_zero(S*w1-w0)
    Un = U*S
    Vn = V*sp.diag(*w0)*Si.T*sp.diag(1/p1, 1/(1-p1))
    exact_zero(one.T*Un-one.T)
    exact_zero(one.T*Vn-one.T)
    exact_zero(Un*sp.diag(*w1)*Vn.T-U*sp.diag(*w0)*V.T)

    # Marginal-preserving least-favourable family at all clocks.
    eu, ev, lam, z = sp.symbols("eu ev lam z", real=True, nonzero=True)
    m, e = sp.Matrix([sp.Rational(1, 2)]*2), sp.Matrix([1, -1])
    def law(l: Any) -> sp.Matrix:
        A = sp.Matrix.hstack(m+eu*e/(2*l), m-eu*e/(2*l))
        B = sp.Matrix.hstack(m+ev*e/(2*l), m-ev*e/(2*l))
        return A*sp.diag(sp.Rational(1, 2)+l*z, sp.Rational(1, 2)-l*z)*B.T
    L0, L1 = law(1), law(lam)
    exact_zero((L1-L0)*one)
    exact_zero(one.T*(L1-L0))
    exact_zero(L1-L0-eu*ev*(lam**-2-1)*e*e.T/4)

    # False shared calibrations permit one direct and at most two swapped levels.
    T1, T2, a1, a2, b1, b2 = sp.symbols("T1 T2 a1 a2 b1 b2")
    direct = a1*x+T1*(1-a1)-a2*x-T2*(1-a2)
    swap = (T1-T2)*(T1-x)*(T2-x)-b1*(T2-x)+b2*(T1-x)
    assert sp.Poly(direct, x).degree() == 1
    assert sp.Poly(swap, x).degree() == 2
    exact_zero(sp.Poly(swap, x).LC()-(T1-T2))
    local = sp.symbols("local", nonzero=True)
    for ramification in range(1, 7):
        exact_zero(sp.diff(local**ramification, local)/local**(2*ramification)
                   - ramification/local**(ramification+1))
    return {"branched_tangent_pole_orders": 6, "matrix_pole": True, "determinant_polynomial": True,
            "rank_one_span_cancellation": True, "one_clock_channel_transform": True,
            "exact_marginal_preservation": True, "joint_interaction_identity": True,
            "direct_degree": 1, "swapped_degree": 2}


def channel(eps: float) -> np.ndarray:
    return np.array([[.5+eps/2, .5-eps/2], [.5-eps/2, .5+eps/2]])


def forward(U: np.ndarray, V: np.ndarray, x: float, tau: float,
            a: float, clocks: np.ndarray) -> np.ndarray:
    p = a*(clocks-x)/(a*(clocks-x)+clocks-tau)
    return np.array([U @ np.diag([q, 1-q]) @ V.T for q in p])


def numerical_checks() -> dict[str, Any]:
    rng = np.random.default_rng(860918)
    clocks = np.array([5., 7., 10.])
    max_identity_error = 0.
    max_marginal_error = 0.
    scaled_changes = []
    for eu, ev in itertools.product([.5, .1, .02, .005], repeat=2):
        x0, tau0, t = 1., 3., .08
        d, lam = (tau0-x0)/2, 1-t/((tau0-x0)/2)
        P0 = forward(channel(eu), channel(ev), x0, tau0, 1., clocks)
        Pt = forward(channel(eu/lam), channel(ev/lam), x0+t, tau0-t, 1., clocks)
        target = eu*ev/4*(lam**-2-1)*np.array([[1., -1.], [-1., 1.]])
        err = float(np.max(np.abs(Pt-P0-target)))
        marg = max(float(np.max(np.abs((Pt-P0).sum(axis=1)))),
                   float(np.max(np.abs((Pt-P0).sum(axis=2)))))
        max_identity_error = max(max_identity_error, err)
        max_marginal_error = max(max_marginal_error, marg)
        scaled_changes.append(float(np.max(np.linalg.norm(Pt-P0, axis=(1, 2)))/(eu*ev*t)))
        assert np.min(Pt) > .03
        assert err < 1e-13 and marg < 1e-13
    # Exact singular families remain equal, even with a nonzero other contrast.
    for eu, ev in [(0., .3), (.3, 0.), (0., 0.)]:
        P0 = forward(channel(eu), channel(ev), 1., 3., 1., clocks)
        Pt = forward(channel(eu/.9), channel(ev/.9), 1.1, 2.9, 1., clocks)
        assert np.max(np.abs(Pt-P0)) < 1e-14

    # Enumerate all sitewise label choices in a four-site calibration.
    calibration_trials = 0
    for _ in range(80):
        ts = np.array([5., 8.])
        xs = np.sort(rng.uniform(.1, 3., 4))
        if np.min(np.diff(xs)) < .02:
            continue
        k = rng.uniform(.2, 2., 2)
        odds = (ts[None, :]-xs[:, None])*k
        retained = []
        for flips in itertools.product([False, True], repeat=4):
            vals = odds.copy()
            vals[np.array(flips)] = 1/vals[np.array(flips)]
            A = np.column_stack([vals[:, 0], -vals[:, 1]])
            h, *_ = np.linalg.lstsq(A, np.repeat(ts[0]-ts[1], 4), rcond=None)
            if np.min(h) > 0 and np.max(np.abs(A@h-(ts[0]-ts[1]))) < 1e-9:
                retained.append(1/h)
        assert retained and all(np.max(np.abs(v-k)) < 1e-7 for v in retained)
        calibration_trials += 1
    return {"weak_channel_grid_cases": 16, "singular_exact_cases": 3,
            "max_joint_identity_error": max_identity_error,
            "max_marginal_error": max_marginal_error,
            "change_divided_by_rho_times_t": [min(scaled_changes), max(scaled_changes)],
            "four_site_orientation_trials": calibration_trials,
            "random_seed": 860918}


def source_graph(base: Path, entry: str) -> dict[str, Any]:
    labels: list[str] = []
    refs: list[str] = []
    cites: list[str] = []
    bibs: list[str] = []
    files: list[str] = []
    def visit(path: Path, stack: tuple[Path, ...] = ()) -> None:
        if path in stack:
            raise AssertionError(f"Cyclic TeX input: {path}")
        if not path.is_file():
            raise AssertionError(f"Missing TeX input: {path}")
        text = re.sub(r"(?<!\\)%[^\n]*", "", path.read_text())
        files.append(str(path.relative_to(base)))
        labels.extend(LABEL.findall(text))
        refs.extend(REF.findall(text))
        cites.extend(k.strip() for cs in CITE.findall(text) for k in cs.split(","))
        bibs.extend(BIB.findall(text))
        for child in INCLUDE.findall(text):
            visit(base / (child if child.endswith(".tex") else child+".tex"), stack+(path,))
    visit(base/entry)
    duplicates = sorted(k for k in set(labels) if labels.count(k) > 1)
    duplicate_bibs = sorted(k for k in set(bibs) if bibs.count(k) > 1)
    missing_refs = sorted(set(refs)-set(labels))
    missing_cites = sorted(set(cites)-set(bibs))
    assert not duplicates, duplicates
    assert not duplicate_bibs, duplicate_bibs
    assert not missing_refs, missing_refs
    assert not missing_cites, missing_cites
    return {"entry": entry, "files": len(files), "labels": len(labels),
            "citations": len(set(cites)), "duplicate_labels": duplicates,
            "missing_references": missing_refs, "missing_citations": missing_cites}


def preservation(base: Path) -> dict[str, Any]:
    root = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], cwd=base,
                                        text=True).strip())
    old_paths = subprocess.check_output(["git", "ls-tree", "-r", "--name-only", BASE_COMMIT],
                                        cwd=root, text=True).splitlines()
    changed = subprocess.check_output(["git", "diff", "--name-only", BASE_COMMIT, "HEAD"],
                                      cwd=root, text=True).splitlines()
    modified_inherited = sorted(set(old_paths).intersection(changed))
    assert not modified_inherited, modified_inherited
    # Full edition retains every companion input, in the same order.
    prefix = "papers/A2-v17-boundary-information-coarsening/"
    old_full = subprocess.check_output(["git", "show", BASE_COMMIT+":"+prefix+"rigidity_v85_full.tex"],
                                       cwd=root, text=True)
    old_inputs = [p for p in INCLUDE.findall(old_full) if not p.startswith("article/v85/")]
    new_inputs = INCLUDE.findall((base/"rigidity_v86_full.tex").read_text())
    assert [p for p in new_inputs if p in old_inputs] == old_inputs
    principal = (base/"article/v86/principal_body.tex").read_text()
    assert r"\input{article/v85/principal_body}" in principal
    return {"base": BASE_COMMIT, "inherited_files": len(old_paths),
            "modified_inherited_files": modified_inherited,
            "companion_inputs_preserved": len(old_inputs)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--core-only", action="store_true", help="Do not claim inherited-source checks")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    base = args.base.resolve()
    result: dict[str, Any] = {"status": "passed", "proof_certification": False,
                              "scope": "new core" if args.core_only else "all v86 editions"}
    result["symbolic"] = symbolic_identities()
    result["numerical"] = numerical_checks()
    entries = ["rigidity_v86_core.tex"] if args.core_only else [
        "rigidity_v86.tex", "rigidity_v86_full.tex", "rigidity_v86_core.tex"]
    result["source_graphs"] = [source_graph(base, e) for e in entries]
    result["preservation"] = "not run in core-only mode" if args.core_only else preservation(base)
    result["new_source_sha256"] = {
        str(p.relative_to(base)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted((base/"article/v86").glob("*.tex"))}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
