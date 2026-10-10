#!/usr/bin/env python3
"""Finite algebra/analytic fixtures. These do not certify Lorentz continuum inputs."""
from __future__ import annotations
import math
from fractions import Fraction
import mpmath as mp
import sympy as sp


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def finite_checks() -> dict:
    # Test a real analytic family with nonzero individual active gradients,
    # zero tangent fraction, and arbitrary finite angular birth order.
    with mp.workdps(120):
        angular_cases = 0
        largest_error = mp.mpf(0)
        for d in (1, 2, 3, 8, 16, 32, 64):
            for radius in ('0.02', '0.08', '0.2'):
                r = mp.mpf(radius)
                t = r**d
                # Solve for alpha / r**d to avoid loss of relative accuracy
                # when the new sector is extremely narrow.
                def f(v):
                    return mp.sin(t*v)/t-mp.cos(t*v)**(d+1)
                v = mp.findroot(f, (mp.mpf('0.8'), mp.mpf('1.0')))
                alpha = t*v
                require(0 < alpha < mp.pi/2, 'positive nonlinear sector')
                require(abs(mp.sin(alpha)-r**d*mp.cos(alpha)**(d+1)) < mp.mpf('1e-100'), 'implicit boundary equation')
                require(0 < v <= 1, 'leading coefficient and orientation')
                # An intentionally loose finite diagnostic of the relative
                # remainder; the manuscript uses the recorded derivative bound.
                bound = 4*(d+1)*r**(2*d)
                require(abs(v-1) <= bound+mp.mpf('1e-110'), 'relative angular-birth remainder')
                largest_error = max(largest_error, abs(v-1))
                angular_cases += 1

        # The outer-annulus comparison is independent of birth order.
        annular_cases = 0
        for d in (0, 1, 2, 3, 8, 64, 1024):
            a = mp.mpf(d)/2
            factor = (mp.power(2, a+1)-1)/(a+1)
            require(factor >= 1, 'mean of nondecreasing leading mode')
            for Hs in ('0.0001', '0.003'):
                H = mp.mpf(Hs)
                K, Kchi = mp.mpf(2), mp.mpf(3)
                require(2*K*mp.sqrt(H) < 1, 'admissible common annulus')
                F = mp.exp((2+mp.sqrt(2))*Kchi*mp.sqrt(H))*(1+mp.sqrt(2)*K*mp.sqrt(H))/(1-2*K*mp.sqrt(H))
                lower = mp.exp(-2*Kchi*mp.sqrt(H))*(1-2*K*mp.sqrt(H))
                for us in ('0.01', '0.3', '0.999'):
                    u = mp.mpf(us)*H
                    r = mp.sqrt(2*u)
                    # Divide both sides by gamma*(2H)**(d/2).
                    upper = mp.exp(Kchi*r)*(1+K*r)*mp.power(u/H, a)
                    require(upper <= F*lower*(1+mp.mpf('1e-100')), 'order-free inner to outer comparison')
                    annular_cases += 1

    product_cases = 0
    for i in range(21):
        for j in range(21):
            x, y = Fraction(i, 100), Fraction(j, 100)
            s = x+y
            require(s <= Fraction(1, 2), 'product regime')
            require((1-x)*(1-y) >= 1-2*s, 'lower relative guard product')
            require((1+x)*(1+y) <= 1+2*s, 'upper relative guard product')
            product_cases += 1

    # The two factors in the final constant must both be present:
    # annulus average <= 2*Q_(2H); center-window length H plus collar 2H.
    H = sp.symbols('H', positive=True)
    require(sp.expand(2*(H+2*H)) == 6*H, 'height constant six')
    r = sp.symbols('r', positive=True)
    u = sp.symbols('u', positive=True)
    require(sp.simplify(sp.diff(r*r/2, r)/r) == 1, 'polar coarea cancellation')
    require(sp.simplify(sp.sqrt(2*(2*H))) == 2*sp.sqrt(H), 'outer radius two sqrt H')

    # Exact root identities must not be inferred from finitely many equal jets.
    x, y = sp.symbols('x y')
    germ_controls = []
    for tested_order in (1, 3, 7, 15):
        f, g = y, y-x**(tested_order+2)
        require(f != g, 'distinct analytic primitive tests')
        require([sp.diff((g-f), x, n).subs(x, 0) for n in range(tested_order+2)] == [0]*(tested_order+2), 'high-order contact fixture')
        require(sp.diff(g-f, x, tested_order+2).subs(x, 0) != 0, 'first nonzero separating jet exists')
        require(sp.diff(f, y).subs({x:0,y:0}) == sp.diff(g, y).subs({x:0,y:0}) == 1, 'nonzero individual gradients')
        germ_controls.append(tested_order)

    # Finite exact Boolean outputs remain zero/one-hot after the physical,
    # initial, half-open occupation and separate terminal decisions.
    one_hot_cases = 0
    for mask in range(1 << 7):
        physical = bool(mask & 1)
        initial = bool(mask & 2)
        terminal = bool(mask & 4)
        visits = [initial]+[bool(mask & (1 << j)) for j in range(3, 7)]
        out = [0]*6
        if physical and initial and terminal:
            out[sum(visits)] = 1
        require(sum(out) <= 1, 'complete one-hot exact-label output')
        if physical and initial and terminal:
            require(out[sum(visits)] == 1, 'half-open occupation label')
        one_hot_cases += 1

    # A zero-center C-infinity guard need not have finite analytic birth order.
    # Exp(-1/r^2)>0 for r>0 and all its Taylor coefficients at zero vanish.
    # Symbolic one-sided limits check finitely many instances, not the theorem.
    flat_limits = []
    for n in (0, 1, 2, 4, 8):
        value = sp.limit(sp.exp(-1/r**2)/r**n, r, 0, dir='+')
        require(value == 0, 'flat guard is not covered by a positive leading jet')
        flat_limits.append(n)

    # A logical countermodel, not a claimed Lorentz orbit: mass at K_m=m.
    # At any fixed cutoff it is eventually absent from the good stratum.
    for K in (1, 4, 16):
        mass_on_good = [int(m <= K) for m in range(2*K, 4*K+1)]
        mass_on_bad = [int(m > K) for m in range(2*K, 4*K+1)]
        require(not any(mass_on_good) and all(mass_on_bad), 'fixed-count exhaustion must not imply ordered tightness')

    # A positive narrow peak can have tiny mass and height one. Such a
    # profile fails the proposed annular domination instead of being deleted.
    inner_peak_height, outer_annular_mass = 1, 0
    require(inner_peak_height > outer_annular_mass, 'mass-only false inference negative control')
    return {
        'analytic_zero_tangent_birth_orders': [1,2,3,8,16,32,64],
        'analytic_angular_cases': angular_cases,
        'order_free_annular_cases': annular_cases,
        'largest_annular_test_birth_order': 1024,
        'relative_guard_product_cases': product_cases,
        'one_hot_exact_label_cases': one_hot_cases,
        'finite_jet_identity_negative_controls': germ_controls,
        'zero_center_flat_guard_negative_controls': flat_limits,
        'zero_tangent_source_retained': True,
        'coarea_and_interval_constants_checked': True,
        'fixed_count_exhaustion_negative_control': True,
        'mass_to_height_negative_control': True,
        'lorentz_word_realization_of_test_orders_claimed': False,
        'continuum_proof_certified': False,
        'full_pointwise_raw_return_LLT_certified': False,
    }


if __name__ == '__main__':
    import json
    print(json.dumps(finite_checks(), indent=2, sort_keys=True))
