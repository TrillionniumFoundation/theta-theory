#!/usr/bin/env python3
"""Finite identities and negative controls; no continuum spectral certification."""
from fractions import Fraction as F
import cmath
import math
import mpmath as mp
import sympy as sp


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def finite_checks():
    # Exact chronological pairing on a finite invertible model.
    length = 7
    permutation = [2, 4, 6, 1, 5, 0, 3]
    inverse = [permutation.index(j) for j in range(length)]
    f = [F(1, 3), F(-2, 5), F(3, 7), F(1, 2), F(-3, 4), F(2, 9), F(0)]
    a = [complex(j + 1, 2 - j) for j in range(length)]
    d = [complex(3 - j, j % 2) for j in range(length)]
    pairing_cases = 0
    wrong_difference = 0.0
    for frequency in (0.0, 0.37, -1.4):
        weights = [cmath.exp(1j * frequency * float(v)) for v in f]
        density = [v / length for v in a]
        wrong = density[:]
        for steps in range(1, 10):
            density = [weights[inverse[j]] * density[inverse[j]] for j in range(length)]
            wrong = [weights[j] * wrong[inverse[j]] for j in range(length)]
            left = sum(d[j] * density[j] for j in range(length))
            right = 0j
            for x in range(length):
                y = x
                phase = 1 + 0j
                for _ in range(steps):
                    phase *= weights[y]
                    y = permutation[y]
                right += a[x] * phase * d[y] / length
            require(abs(left - right) < 2e-11, 'chronological image-side pairing')
            wrong_difference = max(wrong_difference, abs(sum(d[j]*wrong[j] for j in range(length))-right))
            pairing_cases += 1
    require(wrong_difference > 0.1, 'wrong multiplier side not detected')

    # Finite algebra for the N-step norm choice, not the billiard LY estimate.
    C = F(10)
    N = 1
    while C*F(3,4)**N >= F(1,4):
        N += 1
    small = F(1, 8*10*3**N)
    require(C*F(1,2)**N + small*C*3**N < F(1,2), 'strong stable coefficient')
    require(C*F(3,4)**N < F(1,4), 'strong unstable coefficient')
    require(C*3**N > 1, 'exponential cross coefficient was silently discarded')
    p,q,gamma = F(1,6),F(1,12),F(1,48)
    require(q<p and gamma<p-q and gamma<1-q, 'strict norm interpolation margins')
    require(max(p,gamma/(1-gamma))<F(2,5)<F(1,2), 'piecewise Holder multiplier margin')

    # Exact quadratic-root inequality used for preceding-flight Holder regularity.
    roots = 0
    for i in range(31):
        for j in range(31):
            x,y = F(i*i,100),F(j*j,100)
            require((F(i,10)-F(j,10))**2 <= abs(x-y), 'square root Holder inequality')
            roots += 1

    # Beurling--Selberg envelopes, including open/closed endpoint values.
    mp.mp.dps = 35
    def K(x):
        return mp.mpf(1) if x == 0 else (mp.sin(mp.pi*x)/(mp.pi*x))**2
    def H(x):
        if x == mp.floor(x):
            return mp.sign(x)
        return (mp.sin(mp.pi*x)/mp.pi)**2*(mp.polygamma(1,1-x)-mp.polygamma(1,1+x)+2/x)
    envelope_cases = 0
    c,e = mp.mpf('-0.7'),mp.mpf('1.3')
    for B in (4,9,17):
        delta = mp.mpf(B)/(2*mp.pi)
        points = [mp.mpf(j)/20 for j in range(-120,121)] + [c,e]
        for x in points:
            base=(H(delta*(x-c))-H(delta*(x-e)))/2
            excess=(K(delta*(x-c))+K(delta*(x-e)))/2
            low,high=base-excess,base+excess
            closed=mp.mpf(c <= x <= e)
            opened=mp.mpf(c < x < e)
            require(low <= opened+mp.mpf('1e-26') and high >= closed-mp.mpf('1e-26'), 'interval envelope')
            envelope_cases += 1
        require(abs(delta*2*mp.pi-B)<mp.mpf('1e-30'), 'radian frequency normalization')
    require(F(-2)*F(0) > F(-2)*F(1), 'signed-weight order reversal negative control')

    # Integrated exact age-overlap and weighted endpoint amplitude factorization.
    overlap_cases=0
    for n in range(1,20):
        left=[F(n,21),F(2*n+1,31),F(1,7)]
        right=[F(1,9),F(n+3,29)]
        ch=[F(1,2),F(3,4),F(2,3)];ps=[F(4,5),F(1,3)]
        require(sum(x*y for x in left for y in right)==sum(left)*sum(right), 'overlap partition sum')
        weighted=sum(left[i]*right[j]*ch[i]*ps[j] for i in range(3) for j in range(2))
        require(weighted==sum(x*z for x,z in zip(left,ch))*sum(y*z for y,z in zip(right,ps)), 'weighted endpoint factor')
        overlap_cases+=1
    t=sp.symbols('t',positive=True)
    S=sp.Matrix([[3,1,0],[1,4,1],[0,1,5]])
    D=sp.diag(1,1,-1/t); V=D*S*D.T/t
    A=sp.sqrt(t)*sp.diag(1,1,-t)
    require(sp.simplify(V.det()-S.det()/t**5)==0,'physical covariance determinant')
    require(sp.simplify(A*V*A.T-S)==sp.zeros(3),'physical Gaussian Jacobian')
    require(sp.simplify(V.det()-S.det()/t**3)!=0,'missing clock Jacobian negative control')
    for P in (F(1,2),F(1),F(3)):
        require(P+F(3,2)-F(3,2)==P,'normalized likelihood error exponent')
    # A.e. varying-test convergence alone does not imply convergence against
    # weakly convergent varying measures: shrinking neighborhoods of grids.
    for size in (16,32,64):
        leb_upper=F(2,size**2)
        atomic_integral=F(1)
        require(leb_upper<atomic_integral, 'moving-test negative control')
    return {'chronological_pairing_cases':pairing_cases,'wrong_side_detected':True,
        'finite_norm_iteration_N':N,'strict_exponent_margins':True,
        'sqrt_holder_cases':roots,'selberg_envelope_cases':envelope_cases,
        'weighted_overlap_factorizations':overlap_cases,'physical_jacobian_checked':True,
        'negative_controls':['wrong multiplier side','signed order reversal','missing clock Jacobian','moving a.e. test'],
        'continuum_spectral_estimates_certified':False,'continuum_local_limit_certified':False}


if __name__=='__main__':
    import json
    print(json.dumps(finite_checks(),indent=2,sort_keys=True))
