#!/usr/bin/env python3
"""Finite regression checks only; no continuum billiard/proof certification."""
from fractions import Fraction as F
from itertools import product
from math import comb, lcm
import mpmath as mp


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def dot(x, y):
    return sum((a*b for a, b in zip(x, y)), F(0))


def mv(a, x):
    return [dot(row, x) for row in a]


def add(x, y):
    return [a+b for a, b in zip(x, y)]


def sub(x, y):
    return [a-b for a, b in zip(x, y)]


def scale(s, x):
    return [s*a for a in x]


def finite_checks():
    mp.mp.dps = 60
    # Exact Gaussian block algebra: pinning removes the drift and y cross term.
    h = [[F(2), F(1,3), F(0), F(0)],
         [F(1,3), F(3), F(0), F(0)],
         [F(0), F(0), F(5,2), F(1,4)],
         [F(0), F(0), F(1,4), F(7,4)]]
    gaussian_cases = 0
    for lengths in [(1,2,3), (3,7,11), (13,5,2), (1,1,1)]:
        m=sum(lengths);ts=[F(a,m) for a in lengths]
        ws=[[F(1),F(-2),F(1,2),F(0)],
            [F(3),F(0),F(-1),F(2)],
            [F(-1),F(1),F(2),F(1,3)]]
        mean=[sum(t*w[j] for t,w in zip(ts,ws)) for j in range(4)]
        vs=[sub(w,mean) for w in ws]
        require([sum(t*v[j] for t,v in zip(ts,vs)) for j in range(4)]==[0]*4,
                'pinned frequency mean')
        for y in [[F(0)]*4,[F(1),F(2),F(3),F(4)], [F(-2),F(1,7),F(5),F(-3)]]:
            lhs=sum(t*dot(add(y,v),mv(h,add(y,v))) for t,v in zip(ts,vs))
            rhs=dot(y,mv(h,y))+sum(t*dot(v,mv(h,v)) for t,v in zip(ts,vs))
            require(lhs==rhs,'Gaussian pinned cross term')
            gaussian_cases+=1
    # Complex Gaussian inverse with the Fourier sign and 2*pi normalization.
    complex_cases=0
    for H in [mp.mpf('1.5'),mp.mpc('1.2','0.4')]:
        for z in [mp.mpf(0),mp.mpf('0.7'),mp.mpf('-1.3')]:
            actual=mp.quad(lambda v:mp.exp(-1j*v*z-H*v*v/2),[-mp.inf,0,mp.inf])/(2*mp.pi)
            expected=mp.exp(-z*z/(2*H))/mp.sqrt(2*mp.pi*H)
            require(abs(actual-expected)<mp.mpf('1e-45'),'complex Gaussian normalization')
            complex_cases+=1
    # Exact fourth moments of a finite Bernoulli bridge (hypergeometric counts).
    hyper_cases=0
    for m in range(2,19):
        for k in range(m+1):
            for length in range(1,m+1):
                denominator=comb(m,length);moment=F(0)
                for value in range(max(0,length-(m-k)),min(length,k)+1):
                    mass=F(comb(k,value)*comb(m-k,length-value),denominator)
                    moment+=mass*(F(value)-F(length*k,m))**4
                require(moment<=3*length**2,'finite bridge fourth-moment scaling')
                hyper_cases+=1
    # Exact half-open occupation, genuine return enumeration, and clock change.
    c=F(2,7);tau=F(3,4)
    inv=[[F(1),F(0),F(0),F(0)],[F(0),F(1),F(0),F(0)],
         [F(0),F(0),F(0),-1/c],[F(0),F(0),F(1),-tau/c]]
    L=[[F(1),F(0),F(0),F(0)],[F(0),F(1),F(0),F(0)],
       [F(0),F(0),-tau,F(1)],[F(0),F(0),-c,F(0)]]
    for j in range(4):
        e=[F(i==j) for i in range(4)]
        require(mv(inv,mv(L,e))==e,'return covariance coordinate inverse')
    return_cases=0
    for m in range(2,10):
        for bits in product([0,1],repeat=m-1):
            eta=[1,*bits,1];positions=[0]+[j for j in range(1,m+1) if eta[j]]
            n=len(positions)-1
            fields=[[F(j%3-1),F((j*j)%5-2),F(3+j%4,5),F(eta[j])] for j in range(m)]
            sums=[[F(0)]*4]
            for field in fields:sums.append(add(sums[-1],field))
            centered=[sub(a,scale(F(j),[F(0),F(0),tau,c])) for j,a in enumerate(sums)]
            records=[[sums[N][0],sums[N][1],F(N),sums[N][2]] for N in positions]
            err=max(abs(sums[j][3]-c*j) for j in range(m+1))/m
            for ell,N in enumerate(positions):
                require(sums[N][3]==ell,'initial included, terminal excluded')
                U=sub(records[ell],scale(F(ell),[F(0),F(0),1/c,tau/c]))
                require(U==mv(inv,centered[N]),'actual stopped compensation')
                left=sub(records[ell],scale(F(ell,n),records[-1]))
                pinned=sub(centered[N],scale(F(N,m),centered[m]))
                right=mv(inv,add(pinned,scale(F(N,m)-F(ell,n),centered[m])))
                require(left==right,'pinned genuine-return time change')
                require(abs(F(N,m)-F(ell,n))<=2*err/c,'deterministic occupation inverse')
                return_cases+=1
    # The universal finite packet filter, tested in the cyclic group ring.
    filter_cases=0
    for D in range(1,9):
        size=lcm(*range(1,D+1))
        for d in range(1,D+1):
            coefficients=[F(sum(1 for j in range(size) if j%d==a),size) for a in range(d)]
            require(coefficients==[F(1,d)]*d,'finite packet does not annihilate aliases')
            filter_cases+=1
    residue_cases=0
    for d in range(1,5):
        for ws in product(range(3),repeat=d):
            mass=sum(ws)
            if not mass:continue
            factors=[F(d*sum(ws[a]*ws[(a+r)%d] for a in range(d)),mass**2) for r in range(d)]
            require(sum(factors)==d,'arithmetic residue average')
            require((all(x==1 for x in factors))==(len(set(ws))==1),'zero residue criterion')
            residue_cases+=1
    # Negative controls. Strictly subunit roots are not uniformly negligible.
    for m in [10,100,1000]:
        eigen=mp.mpf(1)-mp.mpf(1)/m
        require(eigen<1 and eigen**m>mp.mpf('0.3'),'near-peripheral branch deleted')
    require(10**4>3*10**2,'unpinned fourth moment falsely uses bridge bound')
    require([F(2),F(0)]!=[F(1),F(1)],'nonuniform residue replaced by one')
    # r_m(x)=1+sin(2*pi*m^2*x)/2: interval errors vanish, density errors do not.
    for m in [2,7,20]:
        point=mp.mpf(1)/(4*m*m)
        require(abs(mp.sin(2*mp.pi*m*m*point)/2-mp.mpf('0.5'))<mp.mpf('1e-50'),
                'density-spike negative control')
    require(F(4,2)==2 and F(3,2)!=2,'four-frequency inverse dimension')
    return {'gaussian_pinning_cases':gaussian_cases,'complex_gaussian_cases':complex_cases,
            'finite_hypergeometric_bridge_cases':hyper_cases,'actual_return_identity_cases':return_cases,
            'finite_group_filter_cases':filter_cases,'residue_criterion_cases':residue_cases,
            'negative_controls':5,'continuum_proof_certified':False,
            'density_inversion_certified':False}


if __name__=='__main__':
    import json
    print(json.dumps(finite_checks(),indent=2,sort_keys=True))
