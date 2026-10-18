#!/usr/bin/env python3
"""Finite exact arithmetic and independent matrix probes for R71.
The limiting theorems are proved in TeX; finite data do not determine an
irrationality exponent. All checks remain active under python -O.
"""
from __future__ import annotations
from fractions import Fraction as F
import json, math
import numpy as np
import scipy
import sympy as sp
COUNTS: dict[str,int] = {}
DETAILS: dict[str,object] = {}

def check(ok: bool, group: str, detail: object) -> None:
    if not bool(ok):
        raise RuntimeError(f'{group}: {detail}')
    COUNTS[group] = COUNTS.get(group,0)+1

def error(x: F, q: int) -> F:
    y=x*q
    a=y.numerator//y.denominator
    return min(abs(y-a),abs(y-a-1))/q

def envelope(x: F, eps: F) -> tuple[F,int,int]:
    if eps<=0: raise ValueError('positive noise required')
    best=max(F(3),error(x,1)/eps); owner=1; q=1
    # Every omitted denominator is >=q, giving a certified finite termination.
    while q<=best:
        candidate=max(F(3),F(q),error(x,q)/eps)
        if candidate<best: best,owner=candidate,q
        q+=1
    return best,owner,q-1

def convergents(letters: list[int]) -> list[tuple[int,int]]:
    p0,p1,q0,q1=1,0,0,1
    rows=[(p1,q1)]
    for a in letters:
        if a<1: raise ValueError('positive partial quotients required')
        p0,p1=p1,a*p1+p0; q0,q1=q1,a*q1+q0
        rows.append((p1,q1))
    return rows

def exact_envelopes() -> None:
    results=[]
    for x in (F(1,3),F(2,7),F(8,21),F(55,144),F(102,277)):
        for eps in (F(1,4),F(1,100),F(1,10000),F(1,1000000)):
            A,q,visited=envelope(x,eps)
            brute=min(max(F(3),F(k),error(x,k)/eps) for k in range(1,math.ceil(A)+31))
            check(A==brute,'exact_envelope_complete_search',(str(x),str(eps)))
            check(visited+1>A and q<=visited,'exact_envelope_stopping',(q,visited,str(A)))
            for B in (1,2,5,11):
                truncated=min(max(F(3),F(k),error(x,k)/eps) for k in range(1,B+1))
                check(min(truncated,F(B+1))<=A<=truncated,
                      'exact_envelope_truncation',(str(x),str(eps),B))
            results.append({'phase':str(x),'epsilon':str(eps),'envelope':str(A),'denominator':q})
    # A single-denominator shortcut is not a lower certificate for the envelope.
    x=F(55,144);eps=F(1,1000000)
    actual=envelope(x,eps)[0]
    check(max(F(3),error(x,1)/eps)>actual,'exact_negative_one_denominator','q=1 overstates minimum')
    DETAILS['rational_envelope_cases']=results

def exact_continued_fractions() -> None:
    samples=[]
    for prefix in ([2],[2,3],[3,1,2],[1,2,3]):
        rows=convergents(list(prefix));p,Q=rows[-1];pp,QQ=rows[-2]
        check(abs(p*QQ-pp*Q)==1,'exact_convergent_basis',prefix)
        for a in (2,3,7,19):
            tail=F(a)+F(2,5)
            # Rational complete quotient tests a finite identity; it is NOT an irrational phase claim.
            x=(p*tail+pp)/(Q*tail+QQ)
            Qnext=a*Q+QQ;pnext=a*p+pp
            E=Q*x-p;Ep=QQ*x-pp
            check(abs(E)==1/(Q*tail+QQ) and Ep==-tail*E,
                  'exact_complete_quotient_identity',(prefix,a))
            check(F(1,Qnext+Q)<abs(E)<F(1,Qnext),
                  'exact_convergent_error_interval',(prefix,a))
            for q in range(1,Qnext):
                check(q*error(x,q)>=abs(E),'exact_best_second_kind',(prefix,a,q))
            eps=F(1,Q*Qnext*Qnext)
            A,owner,_=envelope(x,eps)
            check(F(Qnext,2)<=A<=Qnext,'exact_crossover_envelope',(prefix,a,str(A)))
            for q in range(1,(Qnext+1)//2):
                check(error(x,q)/eps>=F(Qnext,2),
                      'exact_crossover_all_denominators',(prefix,a,q))
            samples.append({'prefix':prefix,'next_partial':a,'Q':Q,'Q_next':Qnext,
                            'epsilon':str(eps),'envelope':str(A),'owner':owner})
    DETAILS['finite_cf_crossover_cases']=samples
    fluctuations=[]
    p,Q=3,7;pp,QQ=1,2
    for a in (10,50,200):
        tail=F(a)+F(2,5);x=(p*tail+pp)/(Q*tail+QQ);Qnext=a*Q+QQ
        e=error(x,Q);low_eps=e/Q;cross_eps=F(1,Q*Qnext*Qnext)
        low=envelope(x,low_eps)[0];high=envelope(x,cross_eps)[0]
        # Cube both expressions to keep all checks rational.
        check(low_eps*low**3<=Q**2*e<F(Q,Qnext),
              'exact_low_scale_normalization',a)
        check(cross_eps*high**3>=F(Qnext,8*Q),
              'exact_high_scale_normalization',a)
        fluctuations.append({'next_partial':a,'ratio':str(F(Qnext,Q)),
                             'low_normalized_cube':str(low_eps*low**3),
                             'crossover_normalized_cube':str(cross_eps*high**3)})
    DETAILS['finite_large_partial_probes']=fluctuations
    mu=sp.symbols('mu',positive=True)
    equality=sp.factor(1/(mu+1)-(mu-1)/(2*mu-1))
    check(sp.factor(equality*(mu+1)*(2*mu-1))==-mu*(mu-2),
          'exact_exponent_equality','only mu=2 on [2,infinity)')
    for mu0 in (F(2),F(5,2),F(3),F(10)):
        lower=1/(mu0+1);upper=(mu0-1)/(2*mu0-1)
        check(0<lower<=F(1,3)<=upper<F(1,2),
              'exact_exponent_ranges',str(mu0))

def float_envelope(x: float,eps: float) -> tuple[float,int]:
    er=lambda q:abs(q*x-round(q*x))/q
    best=max(3.,er(1)/eps);owner=1;q=1
    while q<=best:
        value=max(3.,float(q),er(q)/eps)
        if value<best:best,owner=value,q
        q+=1
        if q>100000:raise RuntimeError('unexpected diagnostic search size')
    return best,owner

def polygon_matrix(x: float,eps: float,q: int) -> tuple[np.ndarray,np.ndarray]:
    alpha=1-eps;er=abs(q*x-round(q*x))/q
    size=q*max(math.ceil(3/q),math.ceil(4*math.pi**2*er/(q*eps)))
    # The inherited construction uses the adjacent polygon chord and J.
    phase=(2*math.pi*x)%(2*math.pi);j=int(math.floor(size*(x%1)))%size
    w0=np.exp(2j*math.pi*j/size);w1=np.exp(2j*math.pi*(j+1)/size)
    target=alpha*np.exp(1j*phase)
    ab=np.linalg.solve(np.array([[w0.real,w1.real],[w0.imag,w1.imag]]),
                       np.array([target.real,target.imag]))
    c=1-ab.sum()
    check(min(ab[0],ab[1],c)>-2e-11,'float_polygon_mixture_nonnegative',(x,eps,size))
    Q=np.full((size,size),c/size)
    indices=np.arange(size)
    Q[indices,(indices+j)%size]+=ab[0]
    Q[indices,(indices+j+1)%size]+=ab[1]
    v=np.exp(2j*math.pi*indices/size)
    check(np.max(np.abs(Q.sum(axis=1)-1))<2e-12,'float_stochastic_rows',size)
    check(np.max(np.abs(Q@v-target*v))<2e-11,'float_exact_mode_intertwining',size)
    return Q,v

def matrix_probes() -> None:
    rows=[];maxerr=0.
    phases=((3-math.sqrt(5))/2,math.sqrt(2)-1,math.atan2(4,3)/(2*math.pi),2/7,0.4000137)
    for x in phases:
        for eps in (.1,.01,.001):
            A,q=float_envelope(x,eps);Q,v=polygon_matrix(x,eps,q);M=len(Q)
            check(M<=(1+4*math.pi**2)*A+1e-8,'float_envelope_constructive_upper',(x,eps,M,A))
            gamma=.7;phi=.37;d=(1+gamma*np.real(np.exp(1j*phi)*v))/2
            check(d.min()>=0 and d.max()<=1,'float_bounded_decoder',(x,eps))
            row=np.eye(M)[0];theta=2*math.pi*x;alpha=1-eps
            U=np.array([[math.cos(theta/2),-math.sin(theta/2)],
                        [math.sin(theta/2),math.cos(theta/2)]])
            rho=np.array([[(1+gamma*math.cos(phi))/2,gamma*math.sin(phi)/2],
                          [gamma*math.sin(phi)/2,(1-gamma*math.cos(phi))/2]])
            for n in range(35):
                target=(1+gamma*alpha**n*math.cos(n*theta+phi))/2
                err=max(abs(row@d-target),abs(row@d-rho[0,0]));maxerr=max(maxerr,err)
                check(err<3e-10,'float_raw_qubit_response',(x,eps,n))
                row=row@Q;rho=alpha*U@rho@U.T+(1-alpha)*np.eye(2)/2
            for k in (1,2,3,5,11):
                sector=alpha**k*(math.cos(k*theta)+abs(math.sin(k*theta))*math.tan(math.pi/M))
                check(sector<=1+1e-11,'float_power_sector',(x,eps,k))
            # The same private machine with one live cemetery state realizes leakage.
            lam=.37;Qhat=np.zeros((M+1,M+1));Qhat[:M,:M]=lam*Q
            Qhat[:M,M]=1-lam;Qhat[M,M]=1;dhat=np.r_[d,0.];row=np.eye(M+1)[0]
            for n in range(16):
                target=lam**n*(1+gamma*alpha**n*math.cos(n*theta+phi))/2
                check(abs(row@dhat-target)<2e-11,'float_leakage_same_response',(x,eps,n))
                row=row@Qhat
            rows.append({'phase':x,'epsilon':eps,'envelope_estimate':A,'denominator':q,'constructed_labels':M})
    # Exact first-sector threshold is independently known for these finite M.
    for M in range(3,10):
        theta=math.pi/M;alpha=math.cos(math.pi/M);eps=1-alpha
        A,_=float_envelope(theta/(2*math.pi),eps)
        check(A/2<=M+1e-10 and M<=(1+4*math.pi**2)*A,
              'float_known_exact_memory_vs_envelope',M)
        if M>3:
            wrong=alpha*(math.cos(theta)+math.sin(theta)*math.tan(math.pi/(M-1)))
            check(wrong>1+1e-12,'float_negative_smaller_threshold_size',M)
    DETAILS['matrix_probes']=rows;DETAILS['maximum_independent_response_residual']=maxerr

if __name__=='__main__':
    exact_envelopes();exact_continued_fractions();matrix_probes()
    print(json.dumps({'schema':'theta.r71.finite-diagnostics.v1','status':'PASS',
        'checks_by_group':COUNTS,'total_checks':sum(COUNTS.values()),'details':DETAILS,
        'numpy':np.__version__,'scipy':scipy.__version__,'sympy':sp.__version__,
        'limits':'Finite rational identities and floating stochastic/quantum examples only. Rational test tails do not establish irrationality exponents. No continuum proof, formal proof assistant, independent human assessment, exhaustive priority or editorial acceptance is asserted.'},indent=2,sort_keys=True))
