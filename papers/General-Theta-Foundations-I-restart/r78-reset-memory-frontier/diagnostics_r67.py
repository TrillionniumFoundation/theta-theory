#!/usr/bin/env python3
"""Finite independent algebraic and raw-instrument diagnostics. Not theorem proofs."""
from __future__ import annotations
import itertools,json,math
import numpy as np
import scipy
import sympy as S
COUNTS={};DETAILS={}
def check(ok,group,detail):
    if not bool(ok):raise RuntimeError(f'{group}: {detail}')
    COUNTS[group]=COUNTS.get(group,0)+1

def chain(k,a):
    Q=S.zeros(k)
    for i in range(k-1):Q[i,i]=a;Q[i,i+1]=1-a
    Q[k-1,k-1]=1
    return Q

def survival(k,a,n):
    return sum(S.binomial(n,j)*(1-a)**j*a**(n-j) for j in range(min(n,k-2)+1))

def psd_exact(A,group):
    check(A==A.T,group,'Hermitian real matrix')
    for size in range(1,A.rows+1):
        for idx in itertools.combinations(range(A.rows),size):
            check(A.extract(idx,idx).det()>=0,group,f'principal minor {idx}')

def exact_audit():
    eps=S.Rational(1,4);h=S.Rational(3,2)
    A=S.diag(1,0);E=S.Matrix([[S.Rational(3,4),S.Rational(1,4)],[S.Rational(1,4),S.Rational(1,4)]])
    T=2*E-S.eye(2);P=S.kronecker_product(A,S.eye(2));AT=S.kronecker_product(A,T);I=S.eye(4)
    for sign in (-1,1):
        mean=-sign*eps*P/2;second=I-sign*eps*AT
        Bp=(second+h*mean)/(2*h*h);Bm=(second-h*mean)/(2*h*h);B0=I-second/(h*h)
        for B in (Bp,Bm,B0):psd_exact(B,'exact_audit_positivity')
        check(Bp+Bm+B0==I,'exact_audit_moments','POVM normalization')
        check(h*(Bp-Bm)==mean,'exact_audit_moments','first moment')
        check(h*h*(Bp+Bm)==second,'exact_audit_moments','second moment')
        for r in (-1,1):
            raw=(h-r)**2*Bp+(-h-r)**2*Bm+r*r*B0
            want=2*I+sign*eps*(r*P-AT)
            check(raw==want,'exact_audit_squared_loss',str((sign,r)))
            psd_exact(raw,'exact_squared_loss_positivity')
    check((h+1)**2==S.Rational(25,4),'exact_audit_squared_loss','pointwise bound')

def exact_hierarchy():
    rows=[]
    for k in range(2,9):
        for a in (S.Rational(1,3),S.Rational(1,2),S.Rational(2,3)):
            Q=chain(k,a);e=S.zeros(1,k);e[0,0]=1;D=S.ones(k,1);D[k-1]=0
            check(Q*S.ones(k,1)==S.ones(k,1),'exact_stochastic_hierarchy','row normalization')
            for n in range(0,2*k+4):
                u=(e*Q**n*D)[0]
                check(u==survival(k,a,n),'exact_survival_formula',str((k,a,n)))
                check(0<=u<=1,'exact_survival_probability',str((k,a,n)))
            H=S.Matrix([[1]+[survival(k,a,i+j) for j in range(k-1)] for i in range(k)])
            det=H.det()
            check(det!=0 and H.rank()==k,'exact_full_response_rank',str((k,a)))
            check(0<survival(k,a,k-1)<1,'exact_randomization_necessary',str((k,a)))
            rows.append({'k':k,'a':str(a),'hankel_determinant':str(det)})
    DETAILS['hierarchy']=rows

def exact_physical_resolvent():
    p=q=S.Rational(1,2);eps=S.Rational(1,4);rows=[]
    for k in (2,3):
        target=chain(k,S.Rational(1,2));Et=S.ones(k,1);Et[k-1]=0
        for M in (1,2):
            obs=chain(M,S.Rational(1,3)) if M>1 else S.ones(1,1)
            D=S.ones(M,1);D[M-1]=S.Rational(1,3)
            for t in (S.Rational(0),S.Rational(1,4),S.Rational(1,2)):
                alive=S.Matrix([[t,1-t],[0,1]])
                P=S.kronecker_product(alive,target,obs)
                initial=S.zeros(1,2*k*M);initial[0]=1
                resolvent=(S.eye(2*k*M)-q*P).inv()
                for sign in (-1,1):
                    losses=S.Matrix([2+2*eps*sign*(int(A==0))*(D[i]-Et[j]) for A in range(2) for j in range(k) for i in range(M)])
                    raw=(p*initial*resolvent*losses)[0]
                    eo=S.zeros(1,M);eo[0]=1;et=S.zeros(1,k);et[0]=1
                    z=q*t
                    gen=(eo*(S.eye(M)-z*obs).inv()*D)[0]-(et*(S.eye(k)-z*target).inv()*Et)[0]
                    formula=2+2*eps*p*sign*gen
                    check(raw==formula,'exact_raw_product_instrument',str((k,M,t,sign)))
                    rows.append({'target_k':k,'observer_M':M,'t':str(t),'sign':sign,'risk':str(raw)})
                cost=(initial*resolvent*S.ones(2*k*M,1))[0]
                check(cost==1/p,'exact_boundary_cost','joint physical/observer resolvent')
    DETAILS['raw_product_risks']=rows

def inf_norm(A):return max(sum(abs(A[i,j]) for j in range(A.cols)) for i in range(A.rows))

def exact_witnesses():
    rows=[];p=q=S.Rational(1,2);tb=S.Rational(1,2);eps=S.Rational(1,4)
    for k in range(2,6):
        a=S.Rational(1,2);K=2*k-3
        H=S.Matrix([[1]+[survival(k,a,i+j) for j in range(k-1)] for i in range(k)])
        Delta=abs(H.det())/(S.factorial(k)*(k-1))
        W=S.Matrix([[(S.Rational(j,K))**n for n in range(K+1)] for j in range(K+1)])
        C0=inf_norm(W.inv());r=min(q*tb,S.Rational(1,2),Delta/(4*C0))/2
        Z=S.Matrix([[(r*S.Rational(j,K))**n for n in range(K+1)] for j in range(K+1)])
        Cr=inf_norm(Z.inv());gap=eps*p*Delta/Cr
        check(Cr<=C0/r**K,'exact_finite_witness','inverse scaling')
        check(Cr*r**(K+1)/(1-r)<=Delta/2,'exact_finite_witness','entire tail controlled')
        check(gap>0,'exact_finite_witness','positive rational risk gap')
        target=chain(k,a);et=S.zeros(1,k);et[0]=1;D=S.ones(k,1);D[k-1]=0
        for M in range(1,k):
            Q=chain(M,a) if M>1 else S.ones(1,1);em=S.zeros(1,M);em[0]=1;d=S.ones(M,1);d[M-1]=0
            targetcoeff=[survival(k,a,n) for n in range(K+1)]
            actualcoeff=[(em*Q**n*d)[0] for n in range(K+1)]
            check(max(abs(u-v) for u,v in zip(targetcoeff,actualcoeff))>=Delta,'exact_hankel_gap',str((k,M)))
            moments=[]
            for j in range(K+1):
                z=r*S.Rational(j,K)
                val=(em*(S.eye(M)-z*Q).inv()*d)[0]-(et*(S.eye(k)-z*target).inv()*D)[0]
                moments.append(abs(val))
                check(0<=z/q<=tb,'exact_finite_witness','actual model parameter')
            check(2*eps*p*max(moments)>=gap,'exact_finite_witness',str((k,M)))
        rows.append({'k':k,'K':K,'delta':str(Delta),'r':str(r),'Cr':str(Cr),'risk_gap':str(gap),'model_count':2*(K+1)})
    DETAILS['rational_finite_witnesses']=rows

def exact_boundary_margin():
    # State-dependent scalar-model laws, and an actual finite rejecting controller.
    for p in (S.Rational(1,4),S.Rational(1,2)):
        q=1-p;T=S.zeros(4);first_letter_matches=(p==S.Rational(1,2));eps=S.Rational(1,2)
        # 0=start,1=one matching failure,2=default,3=post rejection.
        T[0,1 if first_letter_matches else 2]=q
        T[1,2]=q;T[1,3]=p*eps
        T[2,2]=q;T[3,3]=q
        actual=((S.eye(4)-T).inv()*S.ones(4,1))[0]
        expected=1/p+(q*p*eps/p if first_letter_matches else 0)
        check(actual==expected,'exact_boundary_rejection','raw finite controller')
        check(actual<=4,'exact_boundary_rejection','original robust budget')
        if first_letter_matches:
            check((4-1/p)/(q*p)==8,'exact_normalized_cost_margin','positive word margin')
            check(actual>1/p,'exact_boundary_rejection','genuine rejection cost')
    # Exact three-state response-rank check for the irrational quantum target.
    c=[S.Rational(1),S.Rational(3,5)]
    for n in range(1,14):c.append(S.Rational(6,5)*c[-1]-c[-2])
    u=[(1+x)/2 for x in c]
    for size in (3,4,5):
        H=S.Matrix([[u[i+j] for j in range(size)] for i in range(size)])
        check(H.rank()==3,'exact_rank_three_response',str(size))
    check(S.Rational(6,5).q!=1,'exact_rotation_arithmetic','rational trace is not integral')

def floating_joint_instruments():
    rows=[];maxerr=0.0
    for variant in (0.0,0.1,0.2):
        K0=(1+variant)/3*np.array([[1.,1.],[0.,1.]])
        K1=(1-variant)/4*np.array([[1.,0.],[1.,1.]])
        E=np.eye(2)-K0.T@K0-K1.T@K1
        vals,U=np.linalg.eigh(E);Ks=(U*np.sqrt(vals))@U.T
        check(vals.min()>0,'float_primitive_faithfulness','positive herald effect')
        check(np.linalg.norm(K0@K1-K1@K0)>1e-3,'float_noncommuting_failure','noncommuting maps')
        rho=np.array([[.6,.1],[.1,.4]])
        for M in (2,3):
            Q0=np.full((M,M),1/(2*M));Q0+=.5*np.eye(M)
            Q1=np.roll(np.eye(M),1,axis=1)*.7+np.ones((M,M))*.3/M
            D=np.linspace(.2,.8,M);Fplus=np.diag([0.,1.]);Fminus=np.diag([1.,0.])
            score=np.stack([Ks.T@(D[i]*Fplus+(1-D[i])*Fminus)@Ks for i in range(M)])
            def cont(X):
                return np.stack([K0.T@sum(Q0[i,j]*X[j] for j in range(M))@K0+K1.T@sum(Q1[i,j]*X[j] for j in range(M))@K1 for i in range(M)])
            basis=np.eye(M*4).reshape(M*4,M,2,2)
            mat=np.column_stack([cont(X).reshape(-1) for X in basis])
            sol=np.linalg.solve(np.eye(M*4)-mat,score.reshape(-1)).reshape(M,2,2)
            check(np.linalg.norm(sol-score-cont(sol))<1e-12,'float_block_score_resolvent','equation residual')
            for H in sol:
                check(np.linalg.eigvalsh(H).min()>-1e-12 and np.linalg.eigvalsh(H).max()<1+1e-12,'float_score_order','score between zero and identity')
            # Independent forward physical-state recursion, not the adjoint equation.
            physical=np.zeros((M,2,2));physical[0]=rho;rawrisk=0.
            for n in range(50):
                for i in range(M):rawrisk+=np.trace(score[i]@physical[i])
                nxt=np.zeros_like(physical)
                for i in range(M):
                    for j in range(M):nxt[j]+=Q0[i,j]*K0@physical[i]@K0.T+Q1[i,j]*K1@physical[i]@K1.T
                physical=nxt
            adjrisk=float(np.trace(rho@sol[0]));err=abs(rawrisk-adjrisk);maxerr=max(maxerr,err)
            check(err<1e-11,'float_forward_adjoint_identity','infinite resolvent vs forward tail')
            identity=np.tile(np.eye(2),(M,1,1));single=np.eye(2)
            for n in range(12):
                check(np.max(np.abs(identity-single))<1e-12,'float_controller_independent_survival',str(n))
                identity=cont(identity);single=K0.T@single@K0+K1.T@single@K1
            rows.append({'variant':variant,'M':M,'risk':adjrisk,'forward_residual':float(err),'herald_margin':float(vals.min())})
    DETAILS['noncommuting_state_dependent_instruments']=rows;DETAILS['maximum_forward_residual']=maxerr

if __name__=='__main__':
    exact_audit();exact_hierarchy();exact_physical_resolvent();exact_witnesses();exact_boundary_margin();floating_joint_instruments()
    print(json.dumps({'schema':'theta.r67.finite-diagnostics.v1','status':'PASS','checks_by_group':COUNTS,'total_checks':sum(COUNTS.values()),'details':DETAILS,'numpy':np.__version__,'scipy':scipy.__version__,'sympy':S.__version__,'limits':'Finite exact algebra and separate floating raw-instrument diagnostics. Not formal proofs, exhaustive priority, human referee approval or editorial acceptance.'},sort_keys=True,indent=2))
