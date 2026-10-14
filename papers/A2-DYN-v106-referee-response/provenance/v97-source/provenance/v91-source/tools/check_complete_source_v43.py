#!/usr/bin/env python3
"""Finite regression models only; no continuum proof certificate."""
from fractions import Fraction as F
from math import factorial
import cmath
import json
import mpmath as mp
import sympy as sp


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def must_reject(callback, message):
    try:
        callback()
    except RuntimeError:
        return
    raise RuntimeError('negative control did not reject: '+message)


def jet_majorant(alpha, k, d):
    a = mp.mpf(alpha.numerator)/alpha.denominator+1
    return d**a*sum(mp.mpf(factorial(k))/factorial(k-j)*(-mp.log(d))**(k-j)/a**(j+1)
                    for j in range(k+1))


def finite_checks():
    mp.mp.dps = 40
    cases = 0
    for alpha in (F(-3,4), F(-1,2), F(0), F(1,2), F(1)):
        a = mp.mpf(alpha.numerator)/alpha.denominator+1
        for k in range(4):
            for level in (2, 8, 20):
                d = mp.mpf(2)**(-level)
                exact = jet_majorant(alpha, k, d)
                numeric = mp.quad(lambda y: mp.exp(-a*y)*y**k, [-mp.log(d), mp.inf])
                require(abs(exact-numeric) < mp.mpf('1e-32')*(1+abs(exact)), 'power-log integral')
                cases += 1
    # The fixed transition polynomial has matching first and second derivatives.
    x = sp.symbols('x', real=True)
    psi = 1-10*x**3+15*x**4-6*x**5
    require(psi.subs(x,0)==1 and psi.subs(x,1)==0, 'cutoff values')
    require(all(sp.diff(psi,x,j).subs(x,t)==0 for j in (1,2) for t in (0,1)), 'cutoff derivative traces')
    require(sp.factor(sp.diff(psi,x)) == -30*x**2*(x-1)**2, 'cutoff monotonicity')
    # Explicit dyadic radii preserve the coefficients while meeting every budget.
    terms = [(F(-1,2), 1, F(3)), (F(0), 0, F(2)), (F(1), 2, F(1,3))]
    allocations = []
    for budget in (F(1,4), F(1,100), F(1,10000)):
        level = 1
        while True:
            d = mp.mpf(2)**(-level)
            mass = sum(float(abs(c))*jet_majorant(a,k,d) for a,k,c in terms)
            if mass <= float(budget):
                break
            level += 1
            require(level < 200, 'dyadic search did not terminate in finite test')
        allocations.append(level)
        require(tuple(c for a,k,c in terms)==(F(3),F(2),F(1,3)), 'jet coefficient changed')
    # Compact W21 model with exact value and first-derivative traces.
    q = x**2*(1-x)**2
    require(all(sp.diff(q,x,j).subs(x,t)==0 for j in (0,1) for t in (0,1)), 'residual traces')
    a0 = sp.integrate(q,(x,0,1))
    r0 = (3-sp.sqrt(3))/6
    r1 = (3+sp.sqrt(3))/6
    a2 = sp.simplify(sp.integrate(sp.diff(q,x,2),(x,0,r0))
        -sp.integrate(sp.diff(q,x,2),(x,r0,r1))+sp.integrate(sp.diff(q,x,2),(x,r1,1)))
    require(a0==sp.Rational(1,30) and a2==4*sp.sqrt(3)/9, 'exact W21 norms')
    fourier_cases=0
    for b in (mp.mpf('0.1'),mp.mpf(1),mp.mpf(3),mp.mpf(10),mp.mpf(30)):
        h = mp.quad(lambda t: mp.exp(1j*b*t)*t*t*(1-t)**2,[0,1])
        require(abs(h) <= min(mp.mpf(1)/30,4*mp.sqrt(3)/(9*b*b))+mp.mpf('1e-32'), 'Fourier envelope')
        fourier_cases += 1
    # Allocate the pointwise error against a complete reference probability.
    masses=[F(0),F(1,10),F(1,5),F(3,10),F(2,5)]
    require(sum(masses)==1, 'reference probability')
    delta=mp.mpf('0.00001');total=mp.mpf(0)
    for j,beta in enumerate(masses):
        if not beta:
            continue
        A2=mp.mpf(1+j)**3;mass=mp.mpf(beta.numerator)/beta.denominator
        band=max(mp.mpf(1),A2/(mp.pi*delta*mass))
        error=A2/(mp.pi*band)
        require(error <= delta*mass+mp.mpf('1e-35'), 'component bandwidth certificate')
        total+=error
    require(total <= delta+mp.mpf('1e-35'), 'summed pointwise certificate')
    # The source component is fixed before L, not normalized by the cutoff event.
    reference={m:F(1,2**m) for m in range(1,16)}
    def packet(L):
        return {m: (reference[m], F(1,100)*reference[m], (F(1),F(0)))
                for m in range(1,L+1)}
    compatibility_cases=0
    for L in range(1,10):
        small=packet(L)
        for Lprime in range(L,16):
            big=packet(Lprime)
            restricted={m:v for m,v in big.items() if m<=L}
            require(restricted==small, 'component restriction identity')
            compatibility_cases+=len(small)
    # Arithmetic class, not just total autocorrelation (which is even in r).
    residue_cases=0
    for d in range(1,8):
        weights=[F(j+1,d*(d+1)//2) for j in range(d)]
        root=cmath.exp(2j*mp.pi/d)
        for ell in range(d):
            for r in range(d):
                total_res=sum(root**(-j*r)*float(weights[ell])*root**(-j*ell)
                    *sum(float(weights[h])*root**(j*h) for h in range(d)) for j in range(d))
                wanted=d*weights[ell]*weights[(ell+r)%d]
                require(abs(total_res-float(wanted))<1e-10, 'arithmetic class orientation')
                residue_cases+=1
    # Adversarial finite checks: these false implications must not be admitted.
    must_reject(lambda: require(F(1)<=F(1,100), 'small mass does not bound edge height'), 'height')
    must_reject(lambda: require([2**j for j in range(1,15)][-1]<1, 'individual Fourier L1 does not sum'), 'joint Fourier')
    must_reject(lambda: require(reference[1]/sum(reference[m] for m in range(1,3))
                               ==reference[1]/sum(reference[m] for m in range(1,4)), 'cutoff-conditioned law changed'), 'cutoff normalization')
    must_reject(lambda: require((F(3)*F(1,100))==F(3), 'mass allocation must not scale coefficients'), 'coefficient scaling')
    w=[F(1,6),F(2,6),F(3,6)]
    must_reject(lambda: require(w[0]*w[1]==w[0]*w[-1], 'wrong class residue orientation'), 'orientation')
    require(F(1,2**12)/F(1,2**24)==2**12, 'per-component Fourier scaling')
    return {'power_log_integral_cases':cases,'dyadic_localization_levels':allocations,
            'cutoff_trace_checks':6,'compact_residual_A0':str(a0),'compact_residual_A2':str(a2),
            'fourier_envelope_cases':fourier_cases,'pointwise_budget_components':4,
            'cutoff_compatibility_cases':compatibility_cases,'arithmetic_class_cases':residue_cases,
            'negative_controls':5,'finite_models_are_not_continuum_proofs':True}

if __name__=='__main__':
    print(json.dumps(finite_checks(),indent=2,sort_keys=True))
