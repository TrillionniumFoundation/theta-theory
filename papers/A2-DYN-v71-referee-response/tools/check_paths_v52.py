#!/usr/bin/env python3
"""Finite regression models for v52; not continuum or path-space certification."""
from fractions import Fraction as Q
from itertools import product
import math
import numpy as np
from scipy.optimize import linprog


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def bl_norm(weights, distances):
    weights = np.asarray(weights, dtype=float)
    n = len(weights)
    rows, rhs = [], []
    for i in range(n):
        for j in range(i):
            row = np.zeros(n); row[i] = 1; row[j] = -1
            rows.extend((row, -row)); rhs.extend((distances[i,j], distances[i,j]))
    ans = linprog(-weights, A_ub=np.array(rows), b_ub=np.array(rhs),
                  bounds=[(-1,1)]*n, method='highs')
    require(ans.success, 'finite BL linear program failed')
    return float(-ans.fun)


def finite_checks():
    rng = np.random.default_rng(5209)
    # The exact half-open convention: a visit at m is not in A_m.
    clock_cases = 0
    for m in range(2,11):
        for interior in product((0,1), repeat=m-1):
            eta = [1, *interior, 1]
            visits = [j for j,e in enumerate(eta) if e]
            n = len(visits)-1
            require(sum(eta[:m]) == n, 'terminal visit entered occupation')
            for l, N in enumerate(visits):
                A = sum(eta[:N])
                require(A == l, 'return clock half-open count')
                B4_unscaled = Q(A)-Q(N*n,m)
                require(Q(N,m)-Q(l,n) == -B4_unscaled/n, 'pinned clock identity')
                clock_cases += 1
    # Rational Gaussian cross-term cancellation and grid pinning.
    gaussian_cases = 0
    Omega = [[Q(3),Q(1),Q(0),Q(0)], [Q(1),Q(2),Q(0),Q(0)],
             [Q(0),Q(0),Q(4),Q(1)], [Q(0),Q(0),Q(1),Q(2)]]
    def dotC(x,y):return sum(x[i]*Omega[i][j]*y[j] for i in range(4) for j in range(4))
    for m in (7,11,23,101):
        stops = [0,m//4,m//2,m]
        lens = [b-a for a,b in zip(stops,stops[1:])]
        weights = [[Q(i+j-2) for j in range(4)] for i in range(3)]
        avg = [sum(Q(lens[i],m)*weights[i][j] for i in range(3)) for j in range(4)]
        v = [[weights[i][j]-avg[j] for j in range(4)] for i in range(3)]
        require(all(sum(lens[i]*v[i][j] for i in range(3))==0 for j in range(4)), 'pinning drift')
        for y in ([Q(1),Q(2),Q(-1),Q(3)], [Q(0)]*4):
            lhs=sum(Q(lens[i],m)*dotC([y[j]+v[i][j] for j in range(4)],
                                     [y[j]+v[i][j] for j in range(4)]) for i in range(3))
            rhs=dotC(y,y)+sum(Q(lens[i],m)*dotC(v[i],v[i]) for i in range(3))
            require(lhs==rhs,'pinned Gaussian mixed term')
            gaussian_cases += 1
    # Exact vector-valued source identity, with a kernel of mass one
    # which changes sign. No positivity of the kernel is assumed.
    rows,paths = 32,4
    physical = rng.random((rows,paths))*.08
    controlled = rng.random((rows,paths))*.3
    complete = controlled+physical
    reference = rng.random((rows,1)) * np.array([[.1,.2,.3,.4]])
    kernel=np.array([-.2,.7,.7,-.2])
    def conv(x):return sum(w*np.roll(x,j,axis=0) for j,w in enumerate(kernel))
    left=complete-reference-physical
    right=(controlled-conv(controlled))+(conv(complete)-reference)-conv(physical)
    require(np.max(np.abs(left-right))<1e-12,'path remainder identity')
    require(abs(sum(kernel)-1)<1e-12 and min(kernel)<0,'signed kernel control')
    # Finite path dual-norm and posterior normalization inequalities.
    grid=np.array([0.,.3,.9,1.4])
    distances=np.abs(grid[:,None]-grid[None,:])
    dual_cases=0
    for _ in range(32):
        P=float(rng.uniform(.1,3)); G=float(rng.uniform(-.4,2))
        law=rng.random(4);law/=sum(law)
        ref=rng.random(4);ref/=sum(ref)
        err=bl_norm(P*law-G*ref,distances)
        require(abs(P-G)<=err+1e-10,'constant test does not recover scalar mass')
        require(P*bl_norm(law-ref,distances)<=2*err+1e-10,'conditional numerator normalization')
        b=float(rng.uniform(0,P)); bad=rng.random(4);bad/=sum(bad)
        E=P*law-G*ref-b*bad
        require(P*bl_norm(law-ref,distances)<=2*b+2*bl_norm(E,distances)+1e-10,
                'common physical posterior charge')
        dual_cases+=1
    # Check the positive roof envelope only on this finite set.
    # Its continuum lower bound is proved in the manuscript.
    s=np.r_[np.linspace(-100,100,10001),0.,-math.pi/2]
    envelope=np.sinc(s/math.pi)**2+np.sinc((s+math.pi/2)/math.pi)**2
    require(np.all(envelope>0),'two-shift envelope has a sampled zero')
    require(np.min((1+s*s)*envelope)>0.1,'sampled envelope lower bound')
    # Endpoint response produces a 1/sqrt(m) normalized path budget.
    for m in (4,16,64,256):
        prefix=rng.uniform(-2,2,(m+1,2));prefix[0]=0
        deriv=(prefix-np.arange(m+1)[:,None]/m*prefix[-1])/math.sqrt(m)
        require(np.max(np.linalg.norm(deriv,axis=1))<=4*math.sqrt(2)/math.sqrt(m)+1e-12,
                'finite endpoint path budget')
    require(Q(1,12)*Q(1,16)==Q(1,192),'ordered band exponent')
    # Negative control 1: scalar and coarse-window laws do not imply
    # same-roof conditional kernels. Alternating deterministic paths.
    conditional=np.array([[1.,0.] if j%2==0 else [0.,1.] for j in range(64)])
    ref=np.array([.5,.5]); d2=np.array([[0.,1.],[1.,0.]])
    require(np.allclose(conditional.mean(axis=0),ref),'oscillatory mixture control')
    mean_bl=np.mean([bl_norm(x-ref,d2) for x in conditional])
    require(abs(mean_bl-.5)<1e-10,'scalar-to-kernel negative control')
    # Negative control 2: a positive remainder may have vanishing mass
    # and unbounded height. Do not claim the pointwise endpoint.
    j=12; H=2**(j*j); mass=Q(1,j); width=mass/H
    require(H*width==mass and H>10**20 and mass<Q(1,10),'positive spike control')
    # Negative control 3: weak path convergence need not be TV convergence.
    # Two distinct atoms at distance 1/m have TV distance 1 and BL 1/m.
    dsmall=np.array([[0.,.001],[.001,0.]])
    require(abs(bl_norm(np.array([1.,-1.]),dsmall)-.001)<1e-9,'weak-versus-TV control')
    # Negative control 4: fixed-B convergence says nothing at B=m.
    require(min(Q(1),Q(2,1000))<Q(1,100) and min(Q(1),Q(1000,1000))==1,
            'count-dependent band control')
    return {'half_open_clock_cases':clock_cases,'exact_gaussian_pin_cases':gaussian_cases,
       'signed_kernel_vector_entries':rows*paths,'finite_BL_norm_cases':dual_cases,
       'finite_envelope_points':len(s),'oscillatory_kernel_mean_BL':float(mean_bl),
       'negative_controls':4,'ordered_remainder_exponent':'1/192',
       'continuum_geometry_certified':False,'infinite_dimensional_compactness_certified':False,
       'positive_physical_height_proved_by_tests':False}

if __name__=='__main__':
    import json
    print(json.dumps(finite_checks(),indent=2,sort_keys=True))
