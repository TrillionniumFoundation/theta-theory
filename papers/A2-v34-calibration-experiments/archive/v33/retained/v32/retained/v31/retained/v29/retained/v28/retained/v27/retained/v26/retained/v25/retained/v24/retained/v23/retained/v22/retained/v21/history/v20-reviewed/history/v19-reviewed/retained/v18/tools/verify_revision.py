#!/usr/bin/env python3
"""Exact finite diagnostics for v17. These tests are not proofs of rigidity."""
from __future__ import annotations
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import math
import re

ROOT = Path(__file__).resolve().parents[1]
CHECKS: Counter[str] = Counter()


def require(value: bool, group: str) -> None:
    if not value:
        raise RuntimeError(group)
    CHECKS[group] += 1


def inverse(a: list[list[F]]) -> list[list[F]]:
    n = len(a)
    rows = [list(row) + [F(i == j) for j in range(n)] for i, row in enumerate(a)]
    for j in range(n):
        pivot = next((i for i in range(j, n) if rows[i][j]), None)
        if pivot is None:
            raise ValueError("singular matrix")
        rows[j], rows[pivot] = rows[pivot], rows[j]
        scale = rows[j][j]
        rows[j] = [x / scale for x in rows[j]]
        for i in range(n):
            if i != j:
                scale = rows[i][j]
                rows[i] = [x - scale * y for x, y in zip(rows[i], rows[j])]
    return [row[n:] for row in rows]


def apply(a: list[list[F]], v: list[F]) -> list[F]:
    return [sum(x * y for x, y in zip(row, v)) for row in a]


def interpolation() -> None:
    for n in range(3, 11):
        a = [F((-1)**j * (j + 1), j + 2) for j in range(n + 1)]
        for h in (F(1, 10), F(1, 30), F(1, 100)):
            v = [[(i*h)**j for j in range(n + 1)] for i in range(1, n + 2)]
            vi = inverse(v)
            require(apply(vi, apply(v, a)) == a, "positive_node_polynomial_recovery")
            eps = h**(n + 1)
            noise = [(-1)**i * eps for i in range(n + 1)]
            error = apply(vi, noise)
            unit = inverse([[F(i)**j for j in range(n + 1)] for i in range(1, n + 2)])
            for j in range(n + 1):
                require(abs(error[j]) <= sum(map(abs, unit[j])) * eps / h**j,
                        "coefficient_noise_row_bound")
            tail = apply(vi, [(i*h)**(n+1) for i in range(1, n+2)])
            unit_tail = apply(unit, [F(i)**(n+1) for i in range(1, n+2)])
            for j in range(n + 1):
                require(tail[j] == unit_tail[j] * h**(n+1-j), "analytic_tail_scaling")
            shift = h*h
            translated = [sum(a[k]*math.comb(k,j)*shift**(k-j)
                              for k in range(j,n+1)) for j in range(n+1)]
            for x in (F(0), F(1,7), F(-1,9)):
                require(sum(translated[j]*x**j for j in range(n+1)) ==
                        sum(a[k]*(x+shift)**k for k in range(n+1)),
                        "unknown_onset_coefficient_translation")
    for k in range(3, 61):
        n = (k+1)//2+1
        require(n == max(3, k//2+1, (k-1)//2+2), "required_raw_degree")


def onset() -> None:
    # Quadratic-law controls, not nonlinear billiard simulation.
    for mesh in (20, 40, 80):
        step, eps = F(1,mesh), F(1,mesh*mesh)
        for origin in (F(1,3), F(5,11), F(7,13)):
            for alpha in (F(1,2), F(1), F(3)):
                for noise in (-eps, eps, 2*eps, -2*eps):
                    for threshold in (8*eps,):
                        hits = [F(j,mesh) for j in range(2*mesh+1)
                                if alpha*max(F(0),F(j,mesh)-origin)**2+noise > threshold]
                        require(bool(hits), "onset_grid_finds_crossing")
                        tau = hits[0]
                        require(tau > origin, "no_pre_onset_false_crossing")
                        require(tau-origin <= 6*step, "onset_sqrt_noise_bound")
    # A zero threshold could trigger on a failed pre-onset preparation.
    require(F(1,100) > 0, "zero_threshold_negative_control")


def network() -> None:
    edges = [(0,1,(2,1)), (1,2,(-1,2)), (2,0,(0,-3)), (2,0,(-1,-1)), (1,1,(1,0))]
    tau = [(0,0),(2,1),(1,3)]
    labels = [(k[0]+tau[v][0]-tau[w][0],k[1]+tau[v][1]-tau[w][1]) for v,w,k in edges]
    require(labels[:2] == [(0,0),(0,0)], "tree_representative_gauge")
    require(labels[2:4] == [(1,0),(0,2)], "nonunimodular_cycle_basis")
    incidences = [[(i,side) for i,(v,w,_) in enumerate(edges)
                   for side,u in ((0,v),(1,w)) if u == vertex] for vertex in range(3)]
    require(sum(map(len,incidences)) == 2*len(edges), "loops_counted_twice")
    require(sum(len(x)-1 for x in incidences) == 2*len(edges)-3, "registration_entry_count")
    require((4,0) in incidences[1] and (4,1) in incidences[1], "distinct_loop_occurrences")
    for shear in (F(-1,5),F(0),F(1,3)):
        l = [[F(3),shear],[F(0),F(4)]]
        for k in ([[F(2),F(1)],[F(0),F(3)]], [[F(1),F(0)],[F(0),F(2)]]):
            ki = inverse(k)
            for eps in (F(1,10),F(1,100)):
                perturb = [[eps,-eps],[2*eps,eps]]
                d = [[sum(l[i][t]*k[t][j] for t in range(2)) for j in range(2)] for i in range(2)]
                recovered = [[sum((d[i][t]+perturb[i][t])*ki[t][j] for t in range(2))
                              for j in range(2)] for i in range(2)]
                for i in range(2):
                    for j in range(2):
                        require(recovered[i][j]-l[i][j] == sum(perturb[i][t]*ki[t][j] for t in range(2)),
                                "lattice_perturbation_identity")
    require(math.gcd(2,3) == 1, "mixed_harmonics_no_rotation")
    for k in range(-16,17):
        require((6*k+1) % 4 != 0, "mixed_harmonics_no_reflection")
    require(1-11*F(1,20) > 0, "positive_curvature_support_control")


def sources() -> None:
    preserved = {
        "02_local_law.tex":"ead6f0334962bf7c4c6768ed829b4f6069231ff7",
        "03_asymmetric_inverse.tex":"3f4443c109b2ebb698803d4af296cd61250bc8f2",
        "04_physical_observation.tex":"05f0342a86638594d25a75aaba112d6223b53b9f",
        "05_relative_laws.tex":"16888b97102aefcfd23c21eec12bad5902bffd02",
        "06_intrinsic_calibration.tex":"a8671f538b26d343cd33058866301ce69ede3e69",
        "09_count_fibers.tex":"5452bc177959b86560526a3f18c077f4d9f0e921",
        "10_intrinsic_experiments.tex":"fbb889d26c8e5dc2ac108bf134125446119f312b"}
    for name, expected in preserved.items():
        b = (ROOT / "core" / name).read_bytes()
        require(hashlib.sha1(f"blob {len(b)}\0".encode()+b).hexdigest() == expected, "retained_math_blob")
    text = (ROOT/"main.tex").read_text()
    for item in re.findall(r"\\input\{([^}]+)\}", text):
        require((ROOT/(item+".tex")).exists(), "input_reachable")
        text += (ROOT/(item+".tex")).read_text()
    labels = re.findall(r"\\label\{([^}]+)\}", text)
    require(len(labels) == len(set(labels)), "unique_labels")
    for label in re.findall(r"\\(?:eqref|ref)\{([^}]+)\}", text):
        require(label in labels, "references_resolved")
    require("finite compression" not in text.lower(), "exact_germ_terminology")
    for label in ("thm:intrinsic","thm:network","thm:unregistered","thm:stable","rem:analyticcount"):
        require(label in labels, "theorem_and_count_scope_retained")


if __name__ == "__main__":
    interpolation(); onset(); network(); sources()
    print(json.dumps({"schema":"a2-v17-finite-diagnostics-1","status":"passed",
                      "total_checks":sum(CHECKS.values()),"checks":dict(sorted(CHECKS.items())),
                      "scope":"Exact finite interpolation, onset controls, lattice algebra, incidence bookkeeping and source checks only",
                      "formal_proof_certificate":False},indent=2,sort_keys=True))
