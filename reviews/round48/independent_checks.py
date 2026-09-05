#!/usr/bin/env python3
"""Independent finite checks for the Round 48 review of frozen Round 47.

Run from the repository: python reviews/round48/independent_checks.py --output receipt.json
Only the SHA-bound author certificate module is imported. This is NOT the
34-test author suite, a full-checkout source verifier, a TeX build, or a formal
proof checker. The allocation issue is proved for every finite horizon in the
report; its test below illustrates the exact algebra, not a simulated theorem.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from math import comb, factorial
from pathlib import Path
import sys

TARGET = "1d10fbf2d1c06e875b5124d39266c7dbb0dd8735"
SOURCE = "ce0e531d65974ca46642e374df61f4299fadf786"
EXPECTED_BLOB = "c1f30bc24637559b4c3798367da9b0c7c63ca551"


def git_blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def multiply(A, B):
    return [[sum((x*y for x, y in zip(row, col)), F(0))
             for col in zip(*B)] for row in A]


def invert(A):
    n = len(A)
    W = [[F(x) for x in row] + [F(i == j) for j in range(n)]
         for i, row in enumerate(A)]
    for k in range(n):
        p = next(i for i in range(k, n) if W[i][k])
        W[k], W[p] = W[p], W[k]
        z = W[k][k]
        W[k] = [x/z for x in W[k]]
        for i in range(n):
            if i != k:
                z = W[i][k]
                W[i] = [x-z*y for x, y in zip(W[i], W[k])]
    return [row[n:] for row in W]


def run(source_root: Path) -> dict:
    module_path = source_root / "tools/round47_certificates.py"
    data = module_path.read_bytes()
    observed = git_blob(data)
    if observed != EXPECTED_BLOB:
        raise ValueError(f"Refusing unreviewed certificate code: {observed}")
    spec = importlib.util.spec_from_file_location("round48_bound_certificate", module_path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    checks, details = [], {}

    def check(name, fn):
        try:
            fn()
            checks.append({"name": name, "status": "passed"})
        except Exception as exc:
            checks.append({"name": name, "status": "failed",
                           "error": f"{type(exc).__name__}: {exc}"})

    c = F(7, 6)
    aa = [F(1, 2) + F(k, 50) for k in range(8)]
    bb = [F(3) + F(k, 7) for k in range(9)]
    J, A = mod.jacobi_matrix(aa, bb), mod.generator(c, aa, bb)
    n = len(bb)

    def series(M, vector, count):
        out = []
        for _ in range(count):
            out.append(vector[0])
            vector = mod.matvec(M, vector)
        return out

    mu = series(J, [F(1)] + [F(0)]*(n-1), 17)
    impulse = [F(0)]*(2*n)
    impulse[n] = 1
    v = series(A, mod.matvec(A, impulse), 33)

    def block_identity():
        AA = multiply(A, A)
        for i in range(2*n):
            for j in range(2*n):
                rhs = -J[i % n][j % n] if i//n == j//n else F(0)
                assert AA[i][j] + c*A[i][j] == rhs
    check("block_identity_exact", block_identity)

    def closed_moments():
        for m in range(9):
            z = (-1)**m * sum((comb(m, k)*c**(m-k)*v[m+k]
                               for k in range(m+1)), F(0))
            assert z == mu[m]
    check("closed_response_moments_orders_0_to_8", closed_moments)

    def gram_inverse():
        polys, rhos = [[F(1)]], [F(1)]
        for k in range(6):
            old = polys[k]
            new = [F(0)] + old
            for i, x in enumerate(old):
                new[i] -= bb[k]*x
            if k:
                for i, x in enumerate(polys[k-1]):
                    new[i] -= aa[k-1]**2*x
            polys.append(new)
            rhos.append(rhos[-1]*aa[k]**2)
        for size in range(1, 7):
            H = [[mu[i+j] for j in range(size)] for i in range(size)]
            S = [[F(0)]*size for _ in range(size)]
            for k in range(size):
                p = polys[k] + [F(0)]*(size-k-1)
                for i in range(size):
                    for j in range(size):
                        S[i][j] += p[i]*p[j]/rhos[k]
            assert S == invert(H)
    check("orthogonal_gram_factorization_sizes_1_to_6", gram_inverse)

    def first_return():
        for depth in range(6):
            new_b = list(bb)
            delta = F(1, 11)
            new_b[depth] += delta
            Ap = mod.generator(c, aa, new_b)
            x, y = list(impulse), list(impulse)
            for r in range(1, 4*depth+5):
                diff = y[0]-x[0]
                if r < 4*depth+4:
                    assert diff == 0
                else:
                    expected = -delta
                    for edge in aa[:depth]:
                        expected *= edge**2
                    assert diff == expected
                x, y = mod.matvec(A, x), mod.matvec(Ap, y)
    check("first_changed_step_derivative_depths_0_to_5", first_return)

    def interpolation():
        for N in range(1, 13):
            V = [[F(k**r, factorial(r)) for r in range(N+1)]
                 for k in range(N+1)]
            norm = max(sum(abs(x) for x in row) for row in invert(V))
            assert norm <= 2**N*comb(2*N, N) <= 8**N
    check("interpolation_induced_norm_orders_1_to_12", interpolation)

    box = mod.Box(1, 2, F(1, 2), 1, 3, 4, 1)
    certs = []
    def grids(mode):
        for depth in (0, 1, 2, 5):
            for delta in (F(1), F(1, 16)):
                cert = mod.grid_certificate(box, depth, delta, mode)
                cert.validate()
                K = (cert.order-8)//4
                mass = F(2)**(-K-3 if mode == "compact" else -K-1)/cert.order
                assert cert.atom_mass == mass
                assert cert.jet_constant*cert.amplification*cert.remainder <= delta/2
                certs.append((mode, depth, str(delta), cert.order))
    check("compact_grid_exact_remainder_and_mass", lambda: grids("compact"))
    check("long_grid_exact_remainder_and_mass", lambda: grids("long"))
    details["grid_orders"] = certs

    def laws():
        u = 1/(256*box.lam)
        for M in (0, 1, 8, 32):
            mass = sum((F(2)**(-k-1) for k in range(M+1)), F(0))
            moment = sum((F(2)**(-k-1)*u*(4*k+9)/2 for k in range(M+1)), F(0))
            assert mass+F(2)**(-M-1) == 1
            assert moment+u*F(4*M+17, 2)*F(2)**(-M-1) == 13*u/2
        assert sum((F(2)**(-k-s-2) for k in range(5) for s in range(1, 6)), F(0)) == F(1,2)*(1-F(1,32))**2
    check("law_normalizations_and_exact_long_mean", laws)

    def secants():
        for Q in (F(16), F(32), F(100)):
            for k in range(1, 33):
                S, I = Q**k, Q**(5*k)
                V = k*I*(1+k*S)
                R = S*S+2*Q**(2*k)*S*V
                T = S*S+2*Q**(2*k+1)*S*V
                assert V <= Q**(9*k) and R <= Q**(13*k) and T <= Q**(14*k)
                assert (T+Q*R)*Q**(2*k) <= Q**(17*k)
                assert (Q**(13*(k+1))+Q**2*Q**(13*k))*Q**(2*k+1)/2 <= Q**(15*(k+1))
    check("secant_exponent_finite_checks", secants)

    def posterior_arithmetic():
        assert -F(13,32)+F(3,32)+F(1,16) == -F(1,4)
    check("posterior_exponent_arithmetic", posterior_arithmetic)

    def allocation_witness():
        # For p_q=2^{-B}, m<=n, and alpha<1, the published radius squared
        # is >= v B/(a^2 n), because log(2)>1/2. B can be chosen AFTER any
        # proposed finite budget, which does not contain allocation p_q.
        n0, a, var, target = 1000, F(1), F(1), F(10)
        power = 4*n0*int(target**2)
        lower_squared = var*power/(a*a*n0)
        assert lower_squared > target**2
        details["allocation_witness"] = {"horizon": n0,
            "allocation_weight": f"2^(-{power})",
            "radius_squared_lower_bound": str(lower_squared),
            "target_radius_squared": str(target**2),
            "scope": "Illustration of the general all-finite-n argument; not the printed observation budget evaluated numerically."}
    check("arbitrary_allocation_radius_obstruction", allocation_witness)

    small = mod.Box(1, F(1001,1000), F(1,2), F(501,1000), 3, F(3001,1000))
    time, radius = F(1,100), F(1,10**7)
    args = dict(tail_depth=4, mesh_radius=F(1,1000), taylor_order=6)
    result = mod.outer_confidence(small, 0, [(time,F(-1),F(1))], **args)
    midpoint_c = (small.c_min+small.c_max)/2
    midpoint_a = (small.a_min+small.a_max)/2
    midpoint_b = (small.b_min+small.b_max)/2
    H = mod.step_polynomial(mod.generator(midpoint_c,[midpoint_a]*4,[midpoint_b]*5),time,6)
    E = result.uniform_error
    def rounding_witness():
        assert result.complete and result.examined_boxes == 1 and len(result.boxes) == 1
        assert H-E > radius+2*E
        details["rounding_witness"] = {"original_band": [str(-radius),str(radius)],
            "outward_band": ["-1","1"], "time": str(time),
            "examined_boxes": result.examined_boxes, "retained_boxes": len(result.boxes),
            "H_exact": str(H), "E_exact": str(E),
            "response_lower_bound": str(H-E),
            "uncorrected_radius": str(radius+2*E),
            "strict_gap": str(H-radius-3*E),
            "scope": "Refutes omission of input-enclosure error relative to original bands, not soundness relative to supplied enlarged bands."}
    check("outward_rounding_missing_error_counterexample", rounding_witness)

    def exact_bands():
        exact = mod.outer_confidence(small,0,[(time,-radius,radius)],**args)
        assert exact.complete and exact.boxes == ()
    check("original_exact_band_correctly_rejected", exact_bands)

    def corrected_rounding():
        eps = 1-radius
        assert H+E <= radius+eps+2*E
    check("corrected_input_error_budget", corrected_rounding)

    def budget_scaling():
        cert = mod.grid_certificate(box, 0, F(1,4), "long")
        rho, a, var = F(1,2), F(2), F(3)
        p, L, A0, delta = cert.atom_mass, cert.jet_constant, cert.amplification, cert.radius
        r = delta/(4*L*A0)
        assert 16*var/(a*a*rho*p*r*r) == 64*var/(a*a*rho*cert.separation)
    check("confidence_budget_inverse_kappa_not_inverse_kappa_squared", budget_scaling)

    def resource_cap():
        try:
            mod.outer_confidence(box,0,[(F(1,100),F(-1),F(1))],
                tail_depth=1, mesh_radius=F(1,100), taylor_order=4, max_boxes=1)
        except mod.ResourceLimit:
            return
        raise AssertionError("Expected ResourceLimit, not a partial confidence set")
    check("outer_resource_cap_rejects_partial_search", resource_cap)

    return {"schema":1, "review_round":48, "review_date":"2026-09-05",
        "target_commit":TARGET, "source_commit":SOURCE,
        "author_module_git_blob":observed, "author_module_sha256":hashlib.sha256(data).hexdigest(),
        "status":"passed" if all(x["status"] == "passed" for x in checks) else "failed",
        "check_count":len(checks), "checks":checks, "details":details,
        "scope":{"finite_independent_checks":True, "author_34_test_suite_rerun":False,
            "complete_checkout_verifier_rerun":False, "tex_build_rerun":False,
            "formal_proof_verification":False}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    receipt = run(args.source_root)
    text = json.dumps(receipt, indent=2, sort_keys=True)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text)
    return 0 if receipt["status"] == "passed" else 1

if __name__ == "__main__":
    raise SystemExit(main())
