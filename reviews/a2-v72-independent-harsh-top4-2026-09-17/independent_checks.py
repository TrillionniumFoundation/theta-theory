#!/usr/bin/env python3
"""Independent finite algebra diagnostics for the A2 v72 referee report.

Run with Python 3 and SymPy, optionally --output PATH.  No manuscript code,
network access, or author diagnostic output is imported. These tests are not
certificates of the nonlinear, infinite-dimensional, or statistical theorems.
All checks raise explicitly, and therefore remain active under python -O.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import platform
from pathlib import Path
import sympy as sp


def require(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError('FAILED: ' + label)


def zero(expr: sp.Expr, label: str) -> None:
    require(sp.cancel(expr) == 0, label)


def run() -> dict:
    u, v = sp.symbols('u v', real=True)
    x, y = sp.symbols('x y', real=True)
    d = sp.symbols('d', positive=True)
    zero(d*(d-x-y)/((d-x)*(d-y)) - (1-x*y/((d-x)*(d-y))),
         'abstract cross-ratio identity')
    cases = []
    negative_controls = 0
    radius = sp.Rational(1, 25)
    for p in map(sp.Rational, ['-3/2', '-1/2', '1/2', '3/2']):
        for clock in map(sp.Rational, ['2/3', '5/4']):
            A = -p*u + sp.Rational(2, 3)*u**2 + u**3/5
            C = p*v + sp.Rational(3, 4)*v**2 - v**3/7
            Bminus = 1 + u/7 + u**2/11
            Bplus = 1 - v/9 + v**2/13
            f = Bminus*Bplus*(clock-A-C)/sp.Rational(5, 3)
            f00 = f.subs({u: 0, v: 0})
            ratio = sp.cancel(f*f00/(f.subs(v, 0)*f.subs(u, 0)))
            U, V = sp.cancel(A/(clock-A)), sp.cancel(C/(clock-C))
            zero(ratio-(1-U*V), 'ratio from density')
            kappa = sp.diff(ratio, u, v).subs({u: 0, v: 0})
            zero(kappa-p**2/clock**2, 'mixed derivative clock')
            recovered_clock = abs(p)/sp.sqrt(kappa)
            zero(recovered_clock-clock, 'positive clock branch')
            scale = sp.Rational(7, 11)
            scaled = scale*f
            scaled_ratio = sp.cancel(scaled*scaled.subs({u: 0, v: 0}) /
                                      (scaled.subs(v, 0)*scaled.subs(u, 0)))
            zero(ratio-scaled_ratio, 'scalar normalization invariance')
            residual_lower = clock - (2*abs(p)*radius +
                (sp.Rational(2, 3)+sp.Rational(3, 4))*radius**2 +
                (sp.Rational(1, 5)+sp.Rational(1, 7))*radius**3)
            require(residual_lower > 0, 'positive residual on full square')
            require(1-radius/7-radius**2/11 > 0, 'positive left amplitude')
            require(1-radius/9-radius**2/13 > 0, 'positive right amplitude')
            # Different shapes: the endpoint actions are not equal functions.
            require(sp.cancel(A-C.subs(v, u)) != 0, 'unequal action case')
            for anchor in (-radius, radius):
                va = sp.cancel(clock/p*sp.diff(ratio, u).subs({u: 0, v: anchor}))
                ua = sp.cancel(-clock/p*sp.diff(ratio, v).subs({u: anchor, v: 0}))
                zero(va-V.subs(v, anchor), 'signed right anchor')
                zero(ua-U.subs(u, anchor), 'signed left anchor')
                require(ua != 0 and va != 0, 'nonzero fixed anchors')
                Ur = sp.cancel((1-ratio.subs(v, anchor))/va)
                Vr = sp.cancel((1-ratio.subs(u, anchor))/ua)
                Ar = sp.cancel(clock*Ur/(1+Ur))
                Cr = sp.cancel(clock*Vr/(1+Vr))
                zero(Ar-A, 'left action reconstruction')
                zero(Cr-C, 'right action reconstruction')
                zero(f.subs(v, 0)/f00*(1+Ur)-Bminus, 'left amplitude')
                zero(f.subs(u, 0)/f00*(1+Vr)-Bplus, 'right amplitude')
                Uwrong = sp.cancel((1-ratio.subs(v, anchor))/abs(va))
                Vwrong = sp.cancel((1-ratio.subs(u, anchor))/abs(ua))
                wrong_left = sp.diff(clock*Uwrong/(1+Uwrong), u).subs(u, 0)
                wrong_right = sp.diff(clock*Vwrong/(1+Vwrong), v).subs(v, 0)
                require(wrong_left != -p or wrong_right != p,
                        'absolute-anchor mutation must violate a marked slope')
                negative_controls += 1
                cases.append({'p': str(p), 'd': str(clock), 'anchor': str(anchor),
                              'residual_lower_bound': str(residual_lower), 'pass': True})
    # Diagnostic at normal incidence, not a non-identifiability theorem.
    Rnormal = 1-(u**2/(d-u**2))*(2*v**2/(d-2*v**2))
    zero(sp.diff(Rnormal, u, v).subs({u: 0, v: 0}), 'normal-incidence clock vanishes')
    # Exact finite-flight identity for arbitrary smooth positive beta and
    # anchored E, represented here by a quadratic E and exponential beta.
    p, D, eta, a2, c2 = sp.symbols('p D eta a2 c2', real=True)
    E = a2*u**2/2 + c2*v**2/2 - D*u*v
    residual = d-E+p*u-p*v
    beta = sp.exp(eta*u*v)
    fN = beta*residual
    kN = ((fN*sp.diff(fN, u, v)-sp.diff(fN, u)*sp.diff(fN, v))/fN**2).subs({u:0,v:0})
    zero(kN-(p**2/d**2+D/d+eta), 'finite-flight log-curvature correction')
    # A model scaling symmetry when marked p is not held fixed. This is
    # deliberately outside the fixed-mark theorem, not a billiard example.
    lam = sp.symbols('lam', positive=True)
    zero(lam*d*(lam*d-lam*x-lam*y)/((lam*d-lam*x)*(lam*d-lam*y))
         - d*(d-x-y)/((d-x)*(d-y)), 'unfixed-scale ratio invariance')
    signed_cases = 0
    for r in (3, 4):
        sigmas = [(-1 if i % 2 == 0 else 1)*sp.Rational(i+1, 2*(i+2)) for i in range(r)]
        product = sp.prod(sigmas)
        for degree in range(2, 8):
            T = sp.zeros(r)
            for i in range(r):
                T[i, (i+1) % r] = sigmas[i]**degree
            I = sp.eye(r)
            block = (I+T)*(I-T).inv()
            inverse = (I-T)*(I+T).inv()
            require(block*inverse == I, 'signed cyclic inverse')
            zero(block.det()-(1-(-1)**r*product**degree)/(1-product**degree),
                 'signed cyclic determinant')
            signed_cases += 1
    # Exact transfer/cofactor normalization; no nonlinear billiard realization
    # is inferred from positive rational Jacobi coefficients.
    transfer_cases = 0
    for period in (2, 3, 4):
        ks = [sp.Rational(i+2, i+1) for i in range(period)]
        masses = [sp.Rational(i+1, i+3) for i in range(period)]
        for turns in (1, 2, 3):
            N = period*turns
            H = sp.zeros(N-1)
            for j in range(1, N):
                H[j-1,j-1] = ks[(j-1)%period]+ks[j%period]+masses[j%period]
                if j < N-1:
                    H[j-1,j] = H[j,j-1] = -ks[j%period]
            M = sp.eye(2)
            for j in range(N):
                k, mass = ks[j%period], masses[j%period]
                M = sp.Matrix([[1+mass/k, 1/k], [mass, 1]])*M
            cofactor = sp.prod(ks[j%period] for j in range(N))/H.det()
            zero(cofactor-1/M[0,1], 'cofactor/transfer normalization')
            transfer_cases += 1
    m, s, omega, Gamma = sp.symbols('m s omega Gamma', positive=True)
    alpha = s/(2*(m+s)+2)
    beta_rate = alpha*omega/(omega+alpha*Gamma)
    zero(beta_rate-alpha*(1-alpha*Gamma/(omega+alpha*Gamma)), 'charged rarity balance')
    zero(1-(m+3)/(m+s+3)-s/(m+s+3), 'readout bandwidth exponent')
    return {
        'status': 'passed',
        'python': platform.python_version(), 'sympy': sp.__version__,
        'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'unequal_action_signed_anchor_cases': cases,
        'absolute_anchor_negative_controls': negative_controls,
        'signed_cyclic_cases': signed_cases,
        'transfer_cofactor_cases': transfer_cases,
        'other_exact_checks': ['abstract cross ratio', 'normal clock vanishing',
            'finite-flight mixed log derivative', 'unfixed-scale ratio invariance',
            'charged rarity exponent', 'readout exponent'],
        'scope': 'Finite exact algebra only. No manuscript diagnostics imported; no certification of nonlinear localization, smooth infinite-dimensional inversion, uniform statistical estimates, PDF builds, or physical realizability of the algebraic test models.'
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    text = json.dumps(run(), indent=2, ensure_ascii=False, sort_keys=True) + '\n'
    if args.output:
        args.output.write_text(text, encoding='utf-8')
    else:
        print(text, end='')


if __name__ == '__main__':
    main()
