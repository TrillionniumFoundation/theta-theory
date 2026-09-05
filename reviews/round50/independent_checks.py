#!/usr/bin/env python3
"""Independent finite checks for the frozen Round 49 manuscript.

This is a referee's reconstruction, NOT the author's 43-test suite, NOT a
source-checkout verifier, and NOT a proof of an all-depth theorem.
Only Python's standard library is used. No network or repository mutation.
Run: python3 reviews/round50/independent_checks.py [--output FILE]
"""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
import math
import platform
from decimal import Decimal as D, localcontext, ROUND_CEILING
from fractions import Fraction as F
from pathlib import Path

FROZEN = "abae39b7efeec5f6995f85fcbe1cc1d10e27fba6"
CHECKS: list[dict] = []


def record(name: str, cases: int, kind: str, detail: str) -> None:
    CHECKS.append(dict(name=name, passed=True, cases=cases, arithmetic=kind, detail=detail))


def mul(a: list[F], b: list[F], n: int) -> list[F]:
    out = [F(0)] * (n + 1)
    for i, x in enumerate(a[:n+1]):
        for j, y in enumerate(b[:n+1-i]):
            out[i+j] += x*y
    return out


def power(a: list[F], k: int, n: int) -> list[F]:
    out = [F(1)] + [F(0)] * n
    for _ in range(k):
        out = mul(out, a, n)
    return out


def divide(a: list[F], b: list[F], n: int) -> list[F]:
    if not b or b[0] == 0:
        raise ValueError("A nonzero constant denominator is required")
    out = [F(0)] * (n+1)
    for k in range(n+1):
        out[k] = ((a[k] if k < len(a) else 0)
                  - sum(b[i]*out[k-i] for i in range(1, min(k, len(b)-1)+1))) / b[0]
    return out


def mv(a: list[list[F]], x: list[F]) -> list[F]:
    return [sum((u*v for u, v in zip(row, x)), F(0)) for row in a]


def inverse(a: list[list[F]]) -> list[list[F]]:
    n = len(a)
    b = [row[:] + [F(i == j) for j in range(n)] for i, row in enumerate(a)]
    for k in range(n):
        pivot = next((r for r in range(k, n) if b[r][k]), None)
        if pivot is None:
            raise ValueError("Singular matrix")
        b[k], b[pivot] = b[pivot], b[k]
        scale = b[k][k]
        b[k] = [v/scale for v in b[k]]
        for r in range(n):
            if r != k:
                scale = b[r][k]
                b[r] = [v-scale*w for v, w in zip(b[r], b[k])]
    return [row[n:] for row in b]


def jacobi(n: int) -> tuple[list[list[F]], list[F], list[F]]:
    aa = [F(2, 3) + F(k, 50*n) for k in range(n-1)]
    bb = [F(7, 2) + F(k, 20*n) for k in range(n)]
    j = [[F(0)]*n for _ in range(n)]
    for k in range(n):
        j[k][k] = bb[k]
        if k+1 < n:
            j[k][k+1] = j[k+1][k] = -aa[k]
    return j, aa, bb


def generator(j: list[list[F]], c: F) -> list[list[F]]:
    n = len(j)
    a = [[F(0)]*(2*n) for _ in range(2*n)]
    for k in range(n):
        a[k][n+k] = 1
        a[n+k][n+k] = -c
        for l in range(n):
            a[n+k][l] = -j[k][l]
    return a


def boundary_powers(a: list[list[F]], count: int, source: int) -> list[F]:
    x = [F(i == source) for i in range(len(a))]
    out = []
    for _ in range(count+1):
        out.append(x[0])
        x = mv(a, x)
    return out


def exact_checks() -> None:
    # Formal sampled-generator identity, normalized to Delta=1.
    n = 18
    log = [F(0)] + [F((-1)**(k+1), k) for k in range(1, n+2)]
    sq = [F(1)]
    for k in range(1, n+2):
        sq.append(sq[-1] * (F(1, 2)-(k-1)) / k)
    lx = log[1:]
    hp = divide(sq[1:], lx, n)  # (sqrt(1+x)-1)/log(1+x)
    sp = sq[:n+1]
    sp[0] += 1
    for r in range(1, 9):
        fr = mul(mul(power(log, r-1, n), lx, n), sp, n)
        assert mul(fr, hp, n) == power(log, r-1, n)
        assert all(abs(v) <= 6*2**k for k, v in enumerate(fr))
        coeff_u = [sum((fr[k]*math.comb(k, l)*(-1)**(k-l)
                       for k in range(l, n+1)), F(0)) for l in range(n+1)]
        assert sum(abs(v) for v in coeff_u) <= 8*4**n
    record("sampled_log_formal_identity", 8, "exact rational",
           "F_r(X)H=A^(r-1) through degree 18, r=1,...,8, Delta normalized to 1")
    record("sampled_log_finite_coefficient_bounds", 8, "exact rational",
           "Cauchy-coefficient and U-polynomial row-sum bounds in those finite examples")

    for n in range(1, 11):
        v = [[F(k**r, math.factorial(r)) for r in range(n+1)] for k in range(n+1)]
        vi = inverse(v)
        row_norm = max(sum(abs(x) for x in row) for row in vi)
        assert row_norm <= 2**n*math.comb(2*n, n) <= 8**n
    record("factorial_vandermonde_row_bound", 10, "exact rational", "Orders N=1,...,10")

    n = 9
    j, aa, bb = jacobi(n)
    c = F(5, 4)
    a = generator(j, c)
    ap = boundary_powers(a, 19, n)
    mu = boundary_powers(j, 16, 0)
    for m in range(1, 9):
        recovered = (-1)**m * sum((F(math.comb(m, k))*c**(m-k)*ap[m+k+1]
                                   for k in range(m+1)), F(0))
        assert recovered == mu[m]
    assert -ap[2] == c
    record("damped_jet_to_moment_identity", 9, "exact rational",
           "Damping and moments m=1,...,8 in a 9-site pinned Jacobi example")

    polys = [[F(1)]]
    rho = [F(1)]
    for k in range(6):
        cur = polys[-1]
        nxt = [F(0)]*(len(cur)+1)
        for l, val in enumerate(cur):
            nxt[l+1] += val
            nxt[l] -= bb[k]*val
        if k:
            for l, val in enumerate(polys[-2]):
                nxt[l] -= aa[k-1]**2*val
        polys.append(nxt)
        rho.append(rho[-1]*aa[k]**2)
    for k in range(1, 7):
        h = [[mu[r+s] for s in range(k)] for r in range(k)]
        hi = inverse(h)
        rhs = [[sum(((polys[l][r] if r <= l else 0)*(polys[l][s] if s <= l else 0)/rho[l]
                     for l in range(k)), F(0)) for s in range(k)] for r in range(k)]
        assert hi == rhs
    for k in range(6):
        pk = polys[k]
        ractual = sum((pk[r]*pk[s]*mu[r+s] for r in range(k+1) for s in range(k+1)), F(0))
        tactual = sum((pk[r]*pk[s]*mu[r+s+1] for r in range(k+1) for s in range(k+1)), F(0))
        assert ractual == rho[k]
        assert tactual/ractual == bb[k]
        assert rho[k+1]/rho[k] == aa[k]**2
    record("inverse_gram_identity", 6, "exact rational", "Matrix sizes 1,...,6")
    record("jacobi_coefficient_reconstruction", 6, "exact rational", "b_k and a_k^2, k=0,...,5")

    for depth in range(6):
        j, aa, _ = jacobi(depth+3)
        jj = [row[:] for row in j]
        delta = F(1, 7)
        jj[depth][depth] += delta
        p = 4*depth+3
        old = boundary_powers(generator(j, c), p, len(j))
        new = boundary_powers(generator(jj, c), p, len(j))
        assert old[:p] == new[:p]
        assert new[p]-old[p] == -delta*math.prod(x*x for x in aa[:depth])
    record("two_way_first_changed_jet", 6, "exact rational",
           "Depths 0,...,5: first changed h derivative is 4J+4 with exact leading coefficient")

    for m in range(1, 8):
        amp = F(3, 2)
        p = [F(k+1, 11) for k in range(m)]
        d = [F((-1)**k, k+2) for k in range(m)]
        avg = F(0)
        for signs in itertools.product((-1, 1), repeat=m):
            avg += sum((p[k]+amp*sum((signs[l]*d[k-l] for l in range(k+1)), F(0)))**2 for k in range(m))
        avg /= 2**m
        exact = sum(x*x for x in p)+amp**2*sum((m-k)*d[k]**2 for k in range(m))
        assert avg == exact
        assert avg >= amp**2*sum(x*x for x in d)
    record("all_sign_block_energy_identity", 7, "exact rational",
           "Full sign enumeration for block lengths 1,...,7, including nonzero intercepts")

    for rho0, w in itertools.product((F(1, 8), F(1, 2), F(1)), (F(1, 4096), F(1, 16))):
        pstar = 1-rho0+rho0*w
        assert pstar >= rho0*w
        assert (pstar > rho0*w) == (rho0 < 1)
    record("enlarged_success_event_probability", 6, "exact rational",
           "p_star=1-rho+rho*w >= rho*w; strict for rho<1")

    assert -F(7, 16)*F(15, 32)+F(1, 64) == -F(97, 512)
    assert -F(9, 16)*F(1, 16)-F(1, 64) == -F(13, 256)
    assert -F(97, 512)+F(13, 256)+F(1, 32) == -F(55, 512)
    assert -F(55, 512) <= -F(1, 16)
    record("posterior_exponent_arithmetic", 4, "exact rational",
           "Numerator, denominator, nuisance, and final exponent margin")

    tiny = F(1, 10**7)
    required = 1-tiny
    assert required > 0
    assert -1 >= -tiny-required and 1 <= tiny+required
    assert not (-1 >= -tiny and 1 <= tiny)
    record("input_representation_error_witness", 3, "exact rational",
           "[-1,1] enclosing [-10^-7,10^-7] requires epsilon >=1-10^-7")

    # Exact inverse-information identity for representative positive inputs.
    a0, v, rho0, p, delta, l, ac = map(F, (2, 3, 1, 1, 1, 7, 11))
    rho0 /= 2; p /= 13; delta /= 5
    kappa = p*delta**2/(4*l*l*ac*ac)
    radius_sq = delta**2/(16*l*l*ac*ac)
    assert 16*v/(a0*a0*rho0*p*radius_sq) == 64*v/(a0*a0*rho0*kappa)
    record("confidence_inverse_information_identity", 1, "exact rational", "Corrected identity in confidence.tex")


def decimal_checks() -> dict:
    # High-precision numerical checks are expressly not interval-certified proofs.
    with localcontext() as ctx:
        ctx.prec = 80
        ln2, ln8, ln4 = D(2).ln(), D(8).ln(), D(4).ln()
        lam, q = D(9), D(72)
        s0 = 7
        delta_clock = D(1)/1024
        d0 = -delta_clock.ln()
        w0, rho = D(1)/4096, D(1)/2
        kb = 12+(D(32).ln()+25*q.ln()+8*d0)/ln8
        ab = -(rho*w0).ln()+D(16).ln()
        cb = D(256).ln()+50*q.ln()+16*d0+kb*ab
        pb = 2+ab/ln8
        cases = 0
        for j, v in itertools.product((1, 2, 3, 6, 11, 51, 101), (D(0), D(1), D(10), D(100))):
            r = 4*(j-1)+8
            nn = max(r, int(((D(32).ln()+25*j*q.ln()+r*d0+v)/ln8).to_integral_value(rounding=ROUND_CEILING)))
            m = nn+1
            log_l = 25*j*q.ln()
            log_a = D(8).ln()+r*d0+nn*ln4
            neglog_kappa = -m*(rho*w0).ln()+2*v+D(4).ln()+2*log_l+2*log_a
            assert D(m) <= kb*j+v/ln8
            assert neglog_kappa <= cb*j+pb*v
            assert log_l+D(16).ln()+r*d0-nn*ln8 <= -v-D(2).ln()
            cases += 1
        record("block_resource_certificates", cases, "80-digit Decimal (not interval-certified)",
               "m, kappa, and truncation inequalities at 28 (depth,log-inverse-accuracy) points")
        pstar = 1-rho+rho*w0
        ab_star = -pstar.ln()+D(16).ln()
        cb_star = D(256).ln()+50*q.ln()+16*d0+kb*ab_star
        pb_star = 2+ab_star/ln8
        def visit_budget(eta: D) -> int:
            a, var, pi, rad, alphac, alphav, g = D(1), D(2), D(1)/8, D(1)/10, D(1)/20, D(1)/20, D(4)
            bv = max(D(1), 16*var/(a*a*pi*rad*rad))
            cv = 4/(alphac*eta)
            lv = 1+cv.ln()+2*(16*bv).ln()
            n = max(D(3), 16*bv*lv, 8/pi*(g/alphav).ln()).to_integral_value(rounding=ROUND_CEILING)
            bound = (4*var*(cv*n*n).ln()/(a*a*n*pi)).sqrt()
            assert bound <= rad/2
            return int(n)
        budgets = [visit_budget(D(1)/4), visit_budget(D('1e-100'))]
        assert budgets[1] > budgets[0]
        record("allocation_sensitive_visit_budget", 2, "80-digit Decimal (not interval-certified)",
               "Fixed sampling mass; making the confidence allocation tiny increases the sufficient budget")
        return dict(box=dict(c=[1,2], a=["1/2",1], b=[3,4], T=1, rho="1/2"),
                    s0=s0, t0="1/2048", Delta="1/1024", w0="1/4096",
                    C_b=str(cb), p_b=str(pb), improved_C_b=str(cb_star), improved_p_b=str(pb_star),
                    old_stage_success="1/8192", enlarged_stage_success="4097/8192",
                    visit_budgets=budgets)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path(__file__).with_name('INDEPENDENT_CHECKS.json'))
    args = parser.parse_args()
    exact_checks()
    examples = decimal_checks()
    payload = dict(schema=1, reviewer="GPT-6 Pro", reviewed_commit=FROZEN,
                   status="passed", python_version=platform.python_version(),
                   script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                   check_groups=len(CHECKS), finite_cases=sum(x['cases'] for x in CHECKS),
                   author_suite_executed=False, source_verifier_executed=False,
                   tex_builds_executed=False, proof_assistant_certification=False,
                   limitations="Finite identities and high-precision examples do not certify universal inequalities, the infinite lattice, or the author's unpublished programs.",
                   checks=CHECKS, numerical_example=examples)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k: payload[k] for k in ('status','check_groups','finite_cases','script_sha256')}, indent=2))
    print('Result:', args.output)

if __name__ == '__main__':
    main()
