#!/usr/bin/env python3
"""Finite orbit algebra and exponent checks; not a billiard proof certificate."""
from __future__ import annotations
from fractions import Fraction as Q
import numpy as np
import mpmath as mp


def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def finite_checks() -> dict:
    gamma=Q(1,28)-Q(1,200); alpha=Q(200,99); kappa=alpha-2
    require(gamma==Q(43,1400) and kappa==Q(2,99), 'main exponents')
    margins=[Q(1,14),gamma,Q(1,14)-Q(2,200),Q(3,14)-Q(1,200),
             Q(1,14)-Q(3,200),Q(1,5)-Q(1,200),1-Q(2,200)]
    require(all(x>=gamma for x in margins) and margins.count(gamma)==1, 'pointwise margins')
    require(Q(6,14)+Q(3,200)<Q(1,2) and Q(2,14)+Q(1,200)<Q(1,2), 'analytic domain')
    require(alpha*gamma-kappa==Q(29,693), 'logarithm absorption')
    require(alpha*Q(99,200)==1 and alpha>2, 'annulus compatible scale')
    require(Q(2,5)*kappa==Q(4,495), 'annular average rate')
    require(1-2*Q(99,200)==Q(1,100), 'old grid conflict')
    require(Q(2,5)-Q(2,495)>0, 'raw normalization cannot be declared vanishing')
    rng=np.random.default_rng(20261006)
    gram_cases=analysis_cases=synthesis_cases=arc_cases=abel_cases=0
    tol=3e-10
    for d in (7,13,23):
        angles=rng.uniform(-np.pi,np.pi,size=d)
        eigen=np.exp(1j*angles)
        e=rng.normal(size=d)+1j*rng.normal(size=d);e=e/np.linalg.norm(e)
        for m in (2,3,5,8):
            correlations=np.array([np.vdot(e,eigen**j*e) for j in range(m)])
            B=float(1+2*sum(abs(correlations[1:])))
            for N in (-31,0,11,147):
                V=np.column_stack([eigen**(N+j)*e for j in range(m)])
                gram=V.conj().T@V
                toeplitz=np.array([[np.vdot(e,eigen**(j-i)*e) for j in range(m)] for i in range(m)])
                require(np.linalg.norm(gram-toeplitz)<tol, 'translated exact Gram')
                require(np.linalg.eigvalsh(gram)[-1]<=B+tol, 'absolute row budget')
                coeff=rng.normal(size=m)+1j*rng.normal(size=m)
                b=rng.normal(size=d)+1j*rng.normal(size=d)
                require(np.linalg.norm(V@coeff)**2<=B*np.linalg.norm(coeff)**2+tol, 'synthesis')
                require(np.linalg.norm(V.conj().T@b)**2<=B*np.linalg.norm(b)**2+tol, 'analysis')
                gram_cases+=1
                for T in (m,m+1,2*m+3,5*m):
                    W=np.column_stack([eigen**(N+j)*e for j in range(T)])
                    require(np.linalg.norm(W.conj().T@b)**2/T<=2*B/m*np.linalg.norm(b)**2+tol, 'block analysis')
                    analysis_cases+=1
                    for xi in (0.0,0.9,3.13):
                        a=np.exp(-1j*np.arange(T)*xi)/T
                        require(np.linalg.norm(W@a)**2<=4*B/m+tol, 'full-circle block synthesis')
                        synthesis_cases+=1
            for xi in np.linspace(-np.pi,np.pi,11):
                dist=abs(np.angle(np.exp(1j*(angles-xi))))
                mass=float(np.sum(abs(e[dist<=1/m])**2))
                require(mass<=(np.pi**2/4)*B/m+tol, 'cyclic arc estimate')
                arc_cases+=1
                for x in (0.05,0.3,0.9,1.0):
                    s=1-x/m
                    norm2=float(np.linalg.norm((1-s)*e/(1-s*np.exp(-1j*xi)*eigen))**2)
                    exact_bound=((1-s)/(1-s**m))**2*m*B
                    require(norm2<=exact_bound+tol, 'block Abel bound')
                    require(exact_bound<=B/m/(1-np.exp(-1))**2+tol, 'Abel uniform constant')
                    abel_cases+=1
    # Conditional weights in a uniform finite probability space.
    d=47; eigen=np.exp(2j*np.pi*np.arange(d)/d);e=np.ones(d)/np.sqrt(d);m=17
    b=np.where(np.arange(d)%3==0,1.0,0.0);p=float(np.mean(b)); b=b/(p*np.sqrt(d))
    B=1+2*sum(abs(np.vdot(e,eigen**j*e)) for j in range(1,m))
    V=np.column_stack([eigen**j*e for j in range(m)])
    require(abs(np.linalg.norm(b)**2-1/p)<tol,'unchanged event normalization')
    require(np.linalg.norm(V.conj().T@b)**2/m<=B/(m*p)+tol,'conditioned mean square')
    # Principal-angle Cauchy scaling in an exactly solvable wrapped-Cauchy model.
    mp.mp.dps=70;cauchy_cases=0;max_final=mp.mpf('0')
    for a in (mp.mpf('0.2'),mp.mpf('0.7'),mp.mpf('2.0')):
        for x in (mp.mpf('-4'),mp.mpf('-0.5'),mp.mpf('0.3'),mp.mpf('3')):
            previous=None
            for k in (3,5,7,9):
                r=mp.mpf(2)**(-k);q=mp.exp(-a*r*r)
                actual=mp.mpf('0.5')+mp.atan((1+q)/(1-q)*mp.tan(r*r*x/2))/mp.pi
                target=mp.mpf('0.5')+mp.atan(x/a)/mp.pi
                error=abs(actual-target)
                if previous is not None:require(error<previous,'Cauchy scale convergence model')
                previous=error;cauchy_cases+=1
            max_final=max(max_final,previous)
    # Negative controls. Small moving averages do not bound an individual lag;
    # the test vector cannot be changed independently at each averaging index.
    require(abs(np.vdot(e,eigen**d*e)-1)<tol,'cyclic return peak')
    require(abs(B-1)<tol and B/m<0.1,'nonvanishing peak despite small average')
    moving=sum(abs(np.vdot(V[:,j],V[:,j]))**2 for j in range(m))/m
    require(moving>10*B/m,'independently moving weights must not be admitted')
    return {'pointwise_lag_exponent':str(gamma),'memory_exponent':str(alpha),
        'short_lag_average_exponent':str(kappa),'annular_average_exponent':'4/495',
        'grid_conflict_exponent':'1/100','log_absorption_margin':'29/693',
        'exact_Gaussian_margin_cases':len(margins),'finite_Gram_cases':gram_cases,
        'finite_analysis_cases':analysis_cases,'finite_modulated_synthesis_cases':synthesis_cases,
        'finite_peripheral_arc_cases':arc_cases,'finite_Abel_cases':abel_cases,
        'conditional_probability_checks':2,'wrapped_Cauchy_cases':cauchy_cases,
        'wrapped_Cauchy_last_error_max':mp.nstr(max_final,8),'negative_controls':2,
        'models_are_not_the_physical_billiard':True,'continuum_proof_certified':False}

if __name__=='__main__':
    import json
    print(json.dumps(finite_checks(),indent=2,sort_keys=True))
