#!/usr/bin/env python3
"""Exact auxiliary checks for native339; not an orbit or LLT certificate.

Uses only Python's standard library.  Continuous optical bounds, source
collars, all-word summation and the endpoint trace argument are the written
proof obligations; this program does not purport to verify them by sampling.
"""
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


def main():
    sigma, Rplus, tau = F(47, 59), F(47, 100), F(3, 50)
    lam_lower, c_lower, Lambda = F(9, 50), F(2, 5), F(47, 6)
    # sqrt(19)>4 gives both lower bounds without floating point.
    assert 19 > 4**2
    J = max(F(1), Rplus / (2 * tau) * (sigma + 1 / sigma))
    Cc = J * (1 + Rplus / tau * (1 + 1 / sigma))
    C3 = Rplus + 3 * Rplus**2 / tau + 3 * Rplus**3 / tau**2
    CF = 8 * C3 * J**3 * (1 + sigma)**3 / (1 - sigma**3)
    Cw_upper = (2 * Rplus * J * (1 + sigma) / (tau * (1 - sigma))
                + 4 * Cc / c_lower + 2 * Cc)
    E0, E1_upper = Rplus**2 / tau, 500 * Rplus * Cw_upper
    K_upper = Rplus * F(9, 10) * (Lambda / lam_lower) * (
        E1_upper / lam_lower + E0 * CF / lam_lower**2)
    assert J == F(2845, 354)
    assert CF == F(16132182255644462065, 3378910095288)
    assert Cw_upper == F(18557935, 6372)
    assert K_upper == F(396358110646634302372735325, 39411607351439232)
    threshold = next(m for m in range(2, 1000)
                     if K_upper * sigma**(m - 2) < lam_lower / 2)
    assert threshold == 114
    difference = lam_lower / 2 - K_upper * sigma**112
    assert difference.numerator > 0
    assert K_upper * sigma**111 > lam_lower / 2
    # The 112 exponent is m-2 at m=114; m=1,2 have exponent zero.
    assert all(sigma**(m-1) <= sigma**max(m-2, 0) for m in range(1, 120))

    # Reconstruct the horizontal constraint from a local cubic action jet.
    # x'(0), x''(0) are solved from F_x(x(y),y)=-Rb.  No billiard trajectory
    # is substituted for the native action: these are exact algebra checks.
    checked_jets = 0
    for a, e, d, R, b, A, B, C in product(
            (F(1,2), F(7,3)), (F(-2,5), F(1,7)), (F(3),),
            (F(9,20), F(47,100)), (F(-3,5), F(0), F(1,200)),
            (F(-2), F(3)), (F(-1,3), F(2,5)), (F(-1), F(4))):
        assert a*d-e*e > 0
        x1 = -e/a
        x2 = -(A*x1*x1+2*B*x1+C)/a
        # Direct composition of F with the constrained curve.
        direct_second = -R*b*x2 + a*x1*x1+2*e*x1+d
        # Independently differentiate the quotient e/a along that curve.
        da = A*x1+B
        de = B*x1+C
        quotient_derivative = (a*de-e*da)/(a*a)
        derived_second = d-e*e/a+R*b*quotient_derivative
        assert direct_second == derived_second
        assert a*x1*x1+2*e*x1+d == d-e*e/a
        # Angular restriction and charge normalization are exact identities.
        v = -b*e/a
        assert R*(v+b*e/a) == 0
        checked_jets += 1

    # SPD by itself does not imply horizontal restricted convexity.
    # F(x,y)=1/2 (x+y^2)^2: F_x=b -> x=b-y^2 -> F=b^2/2.
    for b in (F(1,5), F(3,2)):
        for y in (F(-1,3), F(0), F(2,7)):
            x=b-y*y
            a=F(1); e=2*y; d=2*x+6*y*y
            assert a*d-e*e == 2*b > 0
            assert (x+y*y)**2/2 == b*b/2

    result = {
        "status": "PASS",
        "arithmetic": "exact fractions; no floating-point acceptance test",
        "native_constants": {"J_star": str(J), "C_c": str(Cc),
                             "C_3": str(C3), "C_F": str(CF),
                             "C_omega_upper": str(Cw_upper),
                             "K_upper": str(K_upper)},
        "threshold": threshold,
        "threshold_comparison": "K_upper*(47/59)^112 < 9/100",
        "threshold_numerator_positive": difference.numerator > 0,
        "exact_difference_numerator_bits": difference.numerator.bit_length(),
        "exact_difference_sha256": sha256(str(difference).encode()).hexdigest(),
        "preceding_integer_fails_this_conservative_certificate": True,
        "exact_cubic_action_jets_checked": checked_jets,
        "curvature_sign_check": "PASS",
        "hessian_only_counterexample_check": "PASS",
        "scope": "Auxiliary constant and chain-rule checks; not a proof of the optical inputs, physical side trace budgets, or the raw local limit theorem."
    }
    output = Path(__file__).with_name("endpoint_isoroof_checks.json")
    output.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
