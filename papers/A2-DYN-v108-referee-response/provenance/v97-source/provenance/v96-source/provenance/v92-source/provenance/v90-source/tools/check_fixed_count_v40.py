#!/usr/bin/env python3
"""Finite algebra/regression checks only; no continuum billiard certificate."""
from fractions import Fraction as F
import math
import numpy as np


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def finite_checks():
    rng = np.random.default_rng(400839)
    length_cases = 0
    for sigma in (1/8, 1/5, 1/2):
        for r in range(1, 65):
            lengths = rng.integers(1, 101, size=r).astype(float)
            lhs = float(np.sum(lengths**sigma))
            rhs = r**(1-sigma)*float(np.sum(lengths))**sigma
            require(lhs <= rhs*(1+2e-13), 'refined length Jensen factor')
            length_cases += 1

    # Model monotone stable images; these are not simulated billiard curves.
    # Each rectangular boundary has one preimage at most on each image.
    rectangles = [(F(1,10),F(3,10),F(1,5),F(2,5)),
                  (F(2,5),F(3,5),F(1,10),F(1,2)),
                  (F(7,10),F(9,10),F(1,5),F(4,5))]
    curves = []
    cuts = {F(0),F(1)}
    cut_cases = 0
    def occupation(x, curve):
        scale, shift, height = curve
        a = scale*x + shift
        p = height-scale*x
        return int(any(lo<a<hi and bot<p<top for lo,hi,bot,top in rectangles))
    for m in range(1, 33):
        j=m-1
        scale=F(2,3)**j
        shift=F((7*j)%11,20)
        height=F(5+(3*j)%7,10)
        curve=(scale,shift,height);curves.append(curve)
        for lo,hi,bot,top in rectangles:
            for x in ((lo-shift)/scale,(hi-shift)/scale,(height-bot)/scale,(height-top)/scale):
                if 0<x<1:cuts.add(x)
        require(len(cuts)-1 <= 1+4*len(rectangles)*m, 'linear all-time union of cuts')
        ordered=sorted(cuts)
        for left,right in zip(ordered,ordered[1:]):
            p=(2*left+right)/3;q=(left+2*right)/3
            require([occupation(p,c) for c in curves]==[occupation(q,c) for c in curves],
                    'occupation itinerary changes inside a refined cell')
            cut_cases += 1

    # The block is chosen before the unstable coefficient. The weak term
    # grows linearly and is convolved with the strong geometric contraction.
    C=4.;theta=.89;stable=.91;unstable=.93;cross=1.17
    N=1
    while max(C*(1+N)*(theta**N+stable**N),C*(1+N)*unstable**N)>=.25:
        N+=1
        require(N<10000,'block selection did not terminate')
    a=1/(8*C*(1+N)*cross**N)
    require(a*C*(1+N)*cross**N<.25,'unstable cross not absorbed')
    require(C*(1+1)*(theta+stable)>.25,'negative control: premature block')
    for m in range(1, 257):
        convolution=sum(2.**(-j)*(1+(m-1-j)*N) for j in range(m))
        require(convolution<=2*(1+m*N),'polynomial weak remainder convolution')

    # Exact nonnegative cross correlation versus its finite Fourier form.
    fourier_cases=0
    for d in range(1, 18):
        w=rng.integers(0,9,size=d).astype(float)
        if not w.any():w[0]=1
        c=float(w.sum());w/=c;c=1.
        wa=w*rng.integers(0,7,size=d)
        wd=w*rng.integers(0,7,size=d)
        residues=[];selected=[]
        for r in range(d):
            direct=d*sum(w[l]*w[(l+r)%d] for l in range(d))
            cross_direct=d*sum(wa[l]*wd[(l+r)%d] for l in range(d))
            inverse=0j;cross_inverse=0j
            for j in range(d):
                phase=np.exp(2j*np.pi*j*np.arange(d)/d)
                inverse+=np.exp(-2j*np.pi*j*r/d)*abs(np.dot(w,phase))**2
                cross_inverse+=np.exp(-2j*np.pi*j*r/d)*np.dot(wa,phase.conjugate())*np.dot(wd,phase)
            require(abs(inverse-direct)<3e-11,'section residue Fourier sign or normalization')
            require(abs(cross_inverse-cross_direct)<2e-9,'selected endpoint conjugation')
            require(-1e-13<=direct<=d+1e-13,'arithmetic factor positivity or upper bound')
            residues.append(direct);selected.append(cross_direct);fourier_cases+=1
        require(abs(sum(residues)/d-1)<2e-12,'period-average normalization')
        require(abs(sum(selected)/d-float(wa.sum()*wd.sum()))<2e-11,'selected period average')
        for length in (d,10*d+1,100*d+3):
            mean=sum(residues[j%d] for j in range(length))/length
            require(abs(mean-1)<=d*d/length+1e-12,'fine-window period averaging')
    wa=np.array([1.,2.,5.]);wd=np.array([7.,0.,2.])
    forward=sum(wa[l]*wd[(l+1)%3] for l in range(3))
    backward=sum(wa[l]*wd[(l-1)%3] for l in range(3))
    require(abs(forward-backward)>1,'negative control: lost endpoint orientation')
    # A nontrivial arithmetic factor is not automatically one.
    require(3*sum(F(x)**2 for x in (F(1),F(0),F(0)))==3,
            'negative control: all residues declared unmodulated')

    # Finite physical unitary model: q(Tx)/q(x)=e^{i(u kappa+v eta+s)}.
    # This periodic map is not a mixing billiard; it tests only exact algebra.
    L=8;d=5;h=1
    levels=np.array([0,1,1,3,4,2,0,4])
    eta=np.array([1,0,1,1,0,1,0,1],dtype=float)
    kappa=np.roll(levels,-1)-levels-h-eta
    u=v=2*np.pi/d;s=2*np.pi*h/d;zeta=np.exp(-1j*s)
    q=np.exp(2j*np.pi*levels/d)
    phase=np.exp(1j*(u*kappa+v*eta))
    U=np.zeros((L,L),dtype=complex)
    for x in range(L):U[(x+1)%L,x]=phase[x]
    require(np.linalg.norm(U.conj().T@U-np.eye(L))<1e-12,'unitary convention')
    require(np.linalg.norm(U@q-zeta*q)<1e-12,'nonunit scalar eigenphase sign')
    P=np.zeros_like(U);power=np.eye(L,dtype=complex)
    for j in range(L):
        P+=zeta**(-j)*power/L;power=U@power
    expected=np.outer(q,q.conjugate())/L
    require(np.linalg.norm(P-expected)<1e-11,'physical Cesaro projector')
    coefficient=np.vdot(eta,P@eta)/L
    residue=abs(np.mean(eta*q))**2
    require(abs(coefficient-residue)<1e-12,'actual section residue')
    left=(np.exp(1j*v)-1)*np.mean(eta*q)
    scalar=(np.exp(-1j*s)-1)*np.mean(q)
    physical=np.mean((np.exp(1j*u*kappa)-1)*np.exp(1j*v*eta)*q)
    require(abs(left-(scalar-physical))<1e-12,'nonzero displacement source identity')
    require(abs(scalar)>1e-3 and abs(left+physical)>1e-3,
            'negative control: omitted scalar phase')
    for m in range(1,33):
        power=np.linalg.matrix_power(U,m)
        integral=0j
        for x in range(L):
            accumulated=1+0j
            for j in range(m):accumulated*=phase[(x+j)%L]
            integral+=eta[x]*eta[(x+m)%L]*accumulated/L
        require(abs(np.vdot(eta,power@eta)/L-integral)<2e-12,'fixed-clock physical pairing')

    # A branch strictly inside the unit disk at each positive parameter
    # cannot be dropped uniformly when the parameter changes with m.
    for m in (16,32,64,128,256,512):
        near=(m/(m+1))**m
        require(near>.3,'negative control: near-resonant branch lost')
    # Bounded clock partial sums still do not imply fixed coefficient decay.
    oscillatory=[(-1)**m for m in range(1,101)]
    require(max(abs(sum(oscillatory[:m])) for m in range(1,101))==1
            and abs(oscillatory[-1])==1,'Abel/coefficient negative control')
    return {'length_sum_cases':length_cases,'occupation_cell_cases':cut_cases,
            'occupation_model_horizons':32,'block_length':N,
            'polynomial_recurrence_cases':256,'finite_residue_cases':fourier_cases,
            'fixed_clock_unitary_cases':32,'nonunit_scalar_residue_checked':True,
            'nonzero_physical_frequency_source_identity_checked':True,
            'near_resonant_parameter_cases':6,'negative_controls':6,
            'finite_models_are_not_continuum_proofs':True}


if __name__=='__main__':
    import json
    print(json.dumps(finite_checks(),indent=2,sort_keys=True))
