#!/usr/bin/env python3
"""Finite exact diagnostics of boundary memory, not proof of infinite claims."""
from __future__ import annotations
import itertools,json,random
from fractions import Fraction as F
import sympy as sp
COUNTS={};DETAILS={}
def check(ok,group,detail):
    if not bool(ok):raise RuntimeError(f'{group}: {detail}')
    COUNTS[group]=COUNTS.get(group,0)+1

def cosines(n):
    out=[F(1),F(3,5)]
    while len(out)<n:out.append(F(6,5)*out[-1]-out[-2])
    return out[:n]
def sign(x):return 1 if x>0 else -1

def primitive():
    U=sp.Matrix([[2,-1],[1,2]])/sp.sqrt(5);I=sp.eye(2);Z=sp.diag(1,-1)
    check(U.T*U==I,'exact_qubit_primitive','unitary')
    for p in [sp.Rational(1,2),sp.Rational(1,3),sp.Rational(3,4)]:
        Ks=sp.sqrt(p)*I;Kf=sp.sqrt(1-p)*U
        check(Ks.T*Ks+Kf.T*Kf==I,'exact_qubit_primitive','Kraus normalization')
        check(sp.trace(Kf*sp.diag(1,0)*Kf.T)==1-p,'exact_qubit_primitive','input-independent herald rate')
    rho=sp.diag(1,0);cs=cosines(35)
    for n in range(25):
        check(sp.trace(Z*rho)==sp.Rational(cs[n].numerator,cs[n].denominator),'exact_quantum_recurrence',n)
        check(rho.trace()==1 and rho.det()==0,'exact_quantum_recurrence','pure orbit')
        for r in [-1,1]:
            check(sp.trace((2*I-2*r*Z)*rho)==2-2*r*sp.trace(Z*rho),'exact_quantum_loss',(n,r))
        rho=U*rho*U.T
    p=q=F(1,2);A=p*(1-F(3,5)*q)/(1-F(6,5)*q+q*q)
    check(2-2*A==F(12,13),'exact_one_label_value','12/13')
    cs=cosines(160);partial=sum(p*q**n*abs(c) for n,c in enumerate(cs))
    lo=2-2*(partial+q**len(cs));hi=2-2*partial
    check(F(0)<lo<hi<F(12,13),'exact_full_history_enclosure','strict one-label gap')
    DETAILS['full_history_half_herald']={'lower':str(lo),'upper':str(hi),'decimal_interval':[float(lo),float(hi)],'tail_depth':len(cs)}
    for M in range(1,25):
        last=sign(cs[M-1]);slack=sum(p*q**n*2*(abs(cs[n])- (sign(cs[n]) if n<M else last)*cs[n]) for n in range(len(cs)))
        check(0<=slack<=4*q**M,'exact_prefix_memory_upper',M)
        check(slack+4*q**len(cs)<=4*q**M,'exact_prefix_memory_upper','certified tail')
    for eta in [F(1,10),F(1,3),F(1,2),F(1)]:
        for n in range(25):
            check(2-2*eta*abs(cs[n])>=2-2*abs(cs[n]),'exact_compact_polarization',(eta,n))
    DETAILS['one_label_half_herald']='12/13'

def distinguishing():
    cs=cosines(512);a=[sign(c) for c in cs];Hs={}
    # Every unary deterministic machine from one fixed start is a lollipop.
    for M in range(1,9):
        witnesses=[]
        for ell in range(M):
            for period in range(1,M-ell+1):
                n=ell+period
                while n<len(a) and a[n]==a[ell+(n-ell)%period]:n+=1
                check(n<len(a),'exact_lollipop_witness',(M,ell,period))
                witnesses.append(n)
        Hs[M]=max(witnesses)
    DETAILS['unary_distinguishing_depths']=Hs
    for M in range(1,5):
        H=Hs[M]
        for Q in itertools.product(range(M),repeat=M):
            for outputs in itertools.product([-1,1],repeat=M):
                state=0;match=True
                for n in range(H+1):
                    if outputs[state]!=a[n]:match=False;break
                    state=Q[state]
                check(not match,'exact_exhaustive_deterministic_separation',(M,Q,outputs))
    rng=random.Random(65016);bounds=[]
    for M in range(1,6):
        H=Hs[M];gamma=4*min(abs(cs[n]) for n in range(H+1))
        lower=F(1,2)*gamma/2*(F(1,2)/M)**H
        for k in range(12):
            Q=[]
            for i in range(M):
                nums=[rng.randrange(1,10) for j in range(M)];s=sum(nums)
                Q.append([F(n,s) for n in nums])
            plus=[F(rng.randrange(0,11),10) for i in range(M)]
            dist=[F(int(i==0)) for i in range(M)];slack=F(0)
            for n in range(H+1):
                mean=sum(dist[i]*(2*plus[i]-1) for i in range(M))
                slack+=F(1,2)**(n+1)*2*(abs(cs[n])-mean*cs[n])
                dist=[sum(dist[i]*Q[i][j] for i in range(M)) for j in range(M)]
            check(slack>=lower,'exact_stochastic_gap_certificate',(M,k))
        bounds.append({'M':M,'H':H,'gamma':str(gamma),'lower_bound':str(lower)})
    DETAILS['stochastic_gap_certificates']=bounds

def positive_regular():
    # Two failure letters: identity and bit flip, prepared bit zero, 0/1 audit.
    for n in range(9):
        for word in itertools.product((0,1),repeat=n):
            state=0
            for y in word:state^=y
            check(state==sum(word)%2,'exact_two_letter_residual',word)
    # At n>=1 the fair failure-letter parity is fair. Initial n=0 is zero.
    check(sum(F(1,2)**(n+2) for n in range(1,61))<=F(1,4),
          'exact_regular_one_label','one-label loss 1/4 with tail')
    check(F(1,2)*0+F(1,2)*F(1,2)==F(1,4),'exact_regular_one_label','geometric sum')
    check(max(F(1,2),F(1,2))==F(1,2) and max(F(0),F(1))==1,'exact_robust_tie','randomization essential')
    for p in [F(1,2),F(1,3),F(3,4)]:
        for accept in [F(1),F(1,2),F(1,4)]:
            mean=1/(p*accept);rejected=(1-accept)/accept
            check(p*mean==1+rejected,'exact_boundary_cost_identity',(p,accept))
            check((mean<=1/p)==(accept==1),'exact_boundary_cost_rigidity',(p,accept))
    for p in [F(1,2),F(1,3),F(3,4)]:
        for precision in [4,8,16,24]:
            eps=F(1,2**precision);q=1-p;T=1
            while 4*q**T>eps:T+=1
            check(4*q**T<=eps and (T==1 or 4*q**(T-1)>eps),'exact_precision_stopping_test',(p,precision))
            DETAILS.setdefault('prefix_synthesis_sizes',[]).append({'p':str(p),'epsilon':str(eps),'live_labels':T})

def dissipative():
    cs=cosines(100);p=q=F(1,2)
    for alpha in [F(0),F(1,4),F(1,2),F(3,4),F(1)]:
        x=q*alpha
        one=2-2*p*(1-F(3,5)*x)/(1-F(6,5)*x+x*x)
        partial=sum(p*x**n*abs(cs[n]) for n in range(len(cs)))
        hi=2-2*partial;lo=hi-2*p*x**len(cs)/(1-x)
        check(lo<=hi<=one, 'exact_noisy_value_enclosure', str(alpha))
        if alpha>0:
            check(hi<one,'exact_noisy_strict_gap',str(alpha))
        else:
            check(one==2-2*p,'exact_noisy_tie_endpoint','one label suffices')
        for M in range(1,15):
            last=sign(cs[M-1]);slack=sum(p*x**n*2*(abs(cs[n])-last*cs[n]) for n in range(M,len(cs)))
            check(0<=slack<=4*p*x**M/(1-x),'exact_noisy_tail',str((alpha,M)))
    # Amplitude damping of a classical diagonal qubit has a strict limiting +1 gap.
    for alpha in [F(1,4),F(1,2),F(3,4)]:
        # Start at bit one. Probability of bit one after n failures is alpha**n.
        T=0
        while 16*alpha**T>=4:T+=1
        for n in range(T,T+8):
            mean=1-2*alpha**n
            check(mean>0,'exact_contraction_gap_realization',str((alpha,n)))
    DETAILS['noisy_checks']='Depolarizing irrational rotation and diagonal amplitude-damping certificates; finite exact diagnostics only.'

def two_label_exact():
    import numpy as np
    import math
    x,c,t=sp.symbols('x c t',real=True)
    f=lambda z:(1-c*z)/(1-2*c*z+z*z)
    check(sp.factor(sp.diff(f(t),t)-(c-2*t+c*t*t)/(1-2*c*t+t*t)**2)==0, 'exact_two_label_calculus','derivative')
    check(sp.factor(f(t)-f(x)-(x-t)*(x-c+(1-c*x)*t)/((1-2*c*t+t*t)*(1-2*c*x+x*x)))==0, 'exact_two_label_calculus','secant factor')
    k=sp.symbols('k',positive=True);g=(x+k-(1+k*x)*t)/(1-2*k*t+t*t)
    deriv=((1+k*x)*t*t-2*(x+k)*t+2*k*(x+k)-(1+k*x))/(1-2*k*t+t*t)**2
    check(sp.factor(sp.diff(g,t)-deriv)==0,'exact_two_label_calculus','negative-angle derivative')
    check(2-2*(2*sp.Rational(9,16)-sp.Rational(7,13))==sp.Rational(43,52),'exact_two_label_closed_value','43/52')
    def closed(p,alpha,c):
        x=(1-p)*alpha;A=p*(1-c*x)/(1-2*c*x+x*x)
        if x==0:return 2-2*p,np.eye(2)
        if c>=0:
            ss=math.sqrt(max(0.,1-c*c));peak=c/(1+ss)
            if x<=peak:return 2-2*A,np.eye(2)
            lam=peak/x;Q=np.array([[lam,1-lam],[0.,1.]])
            return 2-2*(p*(1+ss)/ss-A),Q
        k=-c;ss=math.sqrt(max(0.,1-k*k))
        tt=min(x,max(0.,(x+k-ss*math.sqrt(1+2*k*x+x*x))/(1+k*x)))
        B=p*(1+c*tt)/(1+2*c*tt+tt*tt)
        return 2-2*(A+2*(B-A)/(1+tt/x)),np.array([[0.,1.],[tt/x,1-tt/x]])
    def raw(p,alpha,c,Q):
        z=complex(c,math.sqrt(max(0.,1-c*c)))
        v=p*(np.array([1.,0.])@np.linalg.inv(np.eye(2)-((1-p)*alpha)*z*Q)).real
        return 2-2*np.abs(v).sum()
    rng=np.random.default_rng(65065);maxerr=0.;rows=[]
    for c in [-1.,-.9,-.6,-.2,0.,.3,.6,.9,1.]:
        for p in [.2,.5,.8]:
            for alpha in [0.,.4,1.]:
                optimum,Q=closed(p,alpha,c);val=raw(p,alpha,c,Q);err=abs(val-optimum);maxerr=max(maxerr,err)
                check(err<2e-12,'float_two_label_attaining_resolvent',(c,p,alpha))
                check(np.min(Q)>=-1e-14 and np.max(abs(Q.sum(axis=1)-1))<1e-14,'float_two_label_legal_table',(c,p,alpha))
                for _ in range(16):
                    a,b=rng.random(2);Qt=np.array([[1-a,a],[b,1-b]])
                    check(raw(p,alpha,c,Qt)>=optimum-2e-12,'float_two_label_random_table_lower',(c,p,alpha))
                rows.append({'c':c,'p':p,'alpha':alpha,'optimum':optimum,'matrix':Q.tolist()})
    DETAILS['two_label_quantum']={'maximum_resolvent_discrepancy':maxerr,'cases':rows,'scope':'Independent complex-resolvent checks and random table probes, not a proof of global optimality.'}

if __name__=='__main__':
    primitive();distinguishing();positive_regular();dissipative();two_label_exact()
    print(json.dumps({'schema':'theta.r65.finite-diagnostics.v1','status':'PASS','checks_by_group':COUNTS,
                      'total_checks':sum(COUNTS.values()),'details':DETAILS,
                      'limits':'Finite exact rational and algebraic examples. Exhaustive deterministic checks are only for the stated small label counts. Nonperiodicity, compact minimax, randomized impossibility, and general complexity require the written proofs.'},indent=2,sort_keys=True))
