#!/usr/bin/env python3
"""Finite algebra/model regressions, not continuum or dynamical certificates."""
from fractions import Fraction as F
from itertools import product
import json
import numpy as np


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def l1(xs):
    return sum(abs(x) for x in xs)


def finite_checks():
    drift_cases = 0
    C = F(3)
    for v in product((F(-1, 2), F(0), F(1, 2)), repeat=4):
        squared = sum(x*x for x in v)
        kappa = squared/(4*C) + F(1, 100)
        tilt = tuple(-x/(2*C) for x in v)
        lhs = -kappa - sum(x*t for x, t in zip(v, tilt))
        rhs = C*sum(t*t for t in tilt)
        require(lhs <= rhs, 'optimized imaginary tilt')
        require(squared <= 4*C*kappa, 'drift/damping inequality')
        drift_cases += 1
    envelope_cases = 0
    CD, a1 = F(12), F(2, 3)
    a = min(a1/2, 1/(2*CD))
    for z in product((F(-2), F(0), F(2)), repeat=2):
        for d in product((F(-1), F(0), F(1)), repeat=2):
            s = sum(x*x for x in d)/CD + F(1, 7)
            energy = s+a1*sum((x-y)**2 for x,y in zip(z,d))
            require(energy >= a*sum(x*x for x in z), 'Gaussian envelope energy')
            envelope_cases += 1
    # Matrix completion of the square, including noncommuting real/imaginary parts.
    rng = np.random.default_rng(5709)
    matrix_cases = 0
    for _ in range(32):
        B = rng.normal(size=(4,4)); S = B.T@B + np.eye(4)
        T = rng.normal(size=(4,4)); T = (T+T.T)/2
        H = S + 1j*T; inv = np.linalg.inv(H)
        a0 = np.linalg.eigvalsh(S).min(); upper = np.linalg.norm(H,2)
        require(np.linalg.eigvalsh(inv.real).min() >= a0/upper**2-1e-11,
                'real inverse Gaussian quadratic form')
        require(abs(np.linalg.det(H)) >= a0**4-1e-10, 'determinant lower bound')
        matrix_cases += 1
    c, tau = F(1,4), F(3,2)
    import sympy as sp
    cs, ts = sp.Rational(c.numerator,c.denominator), sp.Rational(tau.numerator,tau.denominator)
    L = sp.Matrix([[1,0,0,0],[0,1,0,0],[0,0,-ts,1],[0,0,-cs,0]])
    B = sp.Matrix([[2,0,0,0],[1,2,0,0],[0,1,2,0],[1,0,1,2]])
    D=B*B.T; Om=cs*L*D*L.T; A=L.inv()/sp.sqrt(cs)
    require(L.det()==cs and Om.det()==cs**6*D.det(), 'four-dimensional clock determinant')
    require(A*Om*A.T==D, 'coupled bridge second covariance')
    # Integer-count tail sums, only finite checks of the derived envelope.
    sums=[]
    for n in (4,16,64,256):
        m=np.arange(n,30*n+1,dtype=float)
        total=float(np.sum(np.exp(-0.5*(n-m/3)**2/m)/np.sqrt(m)))
        require(0 < total < 30, 'finite count sum bound')
        sums.append(round(total,10))
    # Exact signed normalization against nonnegative true probabilities.
    normalizations=0
    for shift in (F(0),F(1,100),F(1,10),F(-1,10)):
        p=[F(1,4),F(1,4),F(1,2)]
        g=[F(1,4)+shift,F(-1,100),F(1,2)-shift]
        err=l1(x-y for x,y in zip(p,g)); gp=[max(x,F(0)) for x in g]; mass=sum(gp)
        require(abs(mass-1)<=err, 'positive reference normalization')
        require(l1(x-y/mass for x,y in zip(p,gp))/2<=err, 'probability TV factor')
        normalizations+=1
    # Finite observation/path spaces with pairwise path distance two:
    # the fiber BL norm equals signed variation mass on these spaces.
    channels=0; selections=0
    kernel=[[F(3,4),F(1,4)],[F(1,3),F(2,3)],[F(1,2),F(1,2)]]
    for e in (F(1,100), F(1,50), F(1,25)):
        q=[F(1,4),F(1,4),F(1,2)]; H=[F(1,3),F(2,3)]
        ref=[[v*w for w in H] for v in q]
        true=[row[:] for row in ref]; true[0][0]+=e;true[2][1]-=e
        delta=sum(l1(x-y for x,y in zip(a,b)) for a,b in zip(true,ref))
        out=[ [sum(true[z][w]*kernel[z][o] for z in range(3)) for w in range(2)] for o in range(2)]
        rout=[ [sum(ref[z][w]*kernel[z][o] for z in range(3)) for w in range(2)] for o in range(2)]
        eout=sum(l1(x-y for x,y in zip(a,b)) for a,b in zip(out,rout))
        require(eout<=delta,'observation-kernel contraction');channels+=1
        for indices in ((0,),(1,),(0,1)):
            alpha=sum(sum(out[o]) for o in indices); beta=sum(sum(rout[o]) for o in indices)
            require(beta>delta and alpha>=beta-delta,'selected denominator')
            conditional=sum(l1(out[o][w]/alpha-rout[o][w]/beta for w in range(2)) for o in indices)
            require(conditional<=2*delta/(beta-delta),'selected mixed norm')
            scalar=l1(sum(out[o])/alpha-sum(rout[o])/beta for o in indices)/2
            require(scalar<=delta/(beta-delta),'selected output TV')
            selections+=1
    # Negative controls retain precisely the missing implications.
    # Continuous drift v=s with damping s^4 need not be O(sqrt(damping)).
    ratios=[F(1,2**j)**2/(F(1,2**j)**4) for j in range(1,9)]
    require(ratios[-1]>1000*ratios[0],'continuity-only drift control was accepted')
    # Same marginals do not give the graph coupling.
    graph=[F(1,2),F(0),F(0),F(1,2)]; independent=[F(1,4)]*4
    require(l1(x-y for x,y in zip(graph,independent))/2==F(1,2),
            'independent bridges confused with coupled bridges')
    # Weak L^(145/144) plus vanishing mass still permits increasing heights.
    for j in range(1,6):
        height=2**(144*j); width=F(1,2**(145*j))
        require(height*width==F(1,2**j) and height>2**j,'spike negative control')
    # Error of order a rare-event mass need not survive conditioning.
    rare=F(1,1000); absolute_error=2*rare; conditional_variation=F(2)
    require(absolute_error<F(1,100) and conditional_variation==2,
            'postselection mass budget omitted')
    return {'quadratic_tilt_cases':drift_cases,'Gaussian_energy_cases':envelope_cases,
      'complex_matrix_cases':matrix_cases,'exact_clock_covariance_checks':2,
      'finite_count_sums':sums,'signed_normalizations':normalizations,
      'observation_channels':channels,'postselection_cases':selections,
      'negative_control_families':4,'continuum_proof_certified':False,
      'incidence_or_clearance_height_certified':False}

if __name__=='__main__':
    print(json.dumps(finite_checks(),indent=2,sort_keys=True))
