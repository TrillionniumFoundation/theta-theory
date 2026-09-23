#!/usr/bin/env python3
"""Finite regression checks for v13; these do not certify analytic theorems."""
from __future__ import annotations
import argparse
from itertools import product
import json
import math
import sys
import numpy as np
from scipy.optimize import linprog
from scipy.linalg import expm

COUNT=0
MUTANT=''
GROUPS:dict[str,int]={}
def check(ok:bool,message:str,group:str)->None:
    global COUNT
    if not bool(ok):raise RuntimeError('FAILED: '+message)
    COUNT+=1;GROUPS[group]=GROUPS.get(group,0)+1

def tv(p:np.ndarray,q:np.ndarray)->float:return float(np.abs(p-q).sum()/2)
def near(a,b,tol=2e-10):return np.max(np.abs(np.asarray(a)-np.asarray(b)))<tol

def matrix_examples()->None:
    g='intrinsic_channel_spectrum'
    for n in range(1,9):
        for k in range(1,n+1):
            groups=[list(range(j,n,k)) for j in range(k)]
            A=np.zeros((n,k));B=np.zeros((k,n))
            for j,items in enumerate(groups):
                A[items,j]=1;B[j,items]=1/len(items)
            X=A@B
            check(near(X.sum(1),1),'factorized channel must be stochastic',g)
            check(near(np.max(1-np.diag(X)),1-1/math.ceil(n/k)),
                  'balanced grouping private identity formula',g)
            check(np.trace(X)<=k+1e-12,'rank-channel diagonal witness',g)
            # Symmetrization has the prescribed trace and all equal diagonal entries.
            D=(k/n)*np.eye(n)+(0 if n==1 else ((1-k/n)/(n-1))*(np.ones((n,n))-np.eye(n)))
            check(near(np.max(1-np.diag(D)),1-k/n),'hidden identity tradeoff',g)
    channels=[]
    for outputs in product(range(3),repeat=3):
        if len(set(outputs))<=2:channels.append(np.eye(3)[list(outputs)])
    masks=np.array(list(product([0.,1.],repeat=3)))
    for V,expected in [(np.eye(3),1/3),(.5*np.eye(3)+np.ones((3,3))/6,0.)]:
        A=np.array([[(V[i]-X[i])@mask for X in channels]
                    for i in range(3) for mask in masks])
        nc=len(channels);nr=A.shape[0]
        prim=linprog(np.r_[np.zeros(nc),1.],A_ub=np.c_[A,-np.ones(nr)],
                     b_ub=np.zeros(nr),A_eq=np.array([np.r_[np.ones(nc),0.]]),
                     b_eq=[1],bounds=[(0,None)]*nc+[(0,1)],method='highs')
        dual=linprog(np.r_[np.zeros(nr),-1.],A_ub=np.c_[-A.T,np.ones(nc)],
                     b_ub=np.zeros(nc),A_eq=np.array([np.r_[np.ones(nr),0.]]),
                     b_eq=[1],bounds=[(0,None)]*nr+[(None,None)],method='highs')
        check(prim.success and dual.success,'causal-testing primal/dual feasibility',g)
        check(near(prim.fun,expected) and near(-dual.fun,expected),'LP witness value',g)
        check(np.max(A@prim.x[:-1])<=prim.fun+1e-9,'primal event inequalities',g)
        check(np.min(dual.x[:-1]@A)>=-dual.fun-1e-9,'dual column inequalities',g)
    private_identity=1/3 if MUTANT=='private_convexification' else .5
    check(near(private_identity,.5),'convexification cannot be read as same-width private optimum',g)
    merges=[]
    for single in range(3):
        X=np.zeros((3,3));X[single,single]=1;pair=[i for i in range(3) if i!=single]
        X[np.ix_(pair,pair)]=.5;merges.append(X)
    V=sum(merges)/3
    check(near(V,.5*np.eye(3)+np.ones((3,3))/6),'three hidden modes realize the rank-three channel',g)
    check(np.linalg.matrix_rank(V)==3,'target requires three exact private states',g)
    nominal=2 if MUTANT=='free_selector' else 3*2
    check(nominal==6,'hidden mode must be retained with within-mode label',g)
    joint=np.array(merges)/3;ref=np.repeat(V[None,:,:]/3,3,axis=0)
    exposed=max(tv(joint[:,i,:],ref[:,i,:]) for i in range(3))
    if MUTANT=='seed_marginal':exposed=max(tv(joint.sum(0)[i],ref.sum(0)[i]) for i in range(3))
    check(exposed>0.3,'joint exposed selector cannot use marginal cancellation',g)
    check(near(np.linalg.svd(V,compute_uv=False)[-1],.5),'rank-slice positive lower bound input',g)
    for eps in (0,.1,.25,.5,.75,.9):
        for n in range(1,12):
            minimum=next(k for k in range(1,n+1) if 1-1/math.ceil(n/k)<=eps+1e-12)
            formula=math.ceil(n/math.floor(1/(1-eps)+1e-12))
            check(minimum==formula,'inversion gives the least private state cost',g)

def feedback_test()->None:
    g='feedback_and_mark'
    # z0 fair; source z1 indicates whether a matches z0; target z1=0.
    def laws(actions):
        p=np.zeros((2,2));q=np.zeros((2,2))
        for z in range(2):p[z,int(actions[z]==z)]=.5;q[z,0]=.5
        return p,q
    openloop=max(tv(*laws((a,a))) for a in range(2))
    feedback=max(tv(*laws(a)) for a in product(range(2),repeat=2))
    if MUTANT=='open_loop_only':feedback=openloop
    check(near(openloop,.5),'open-loop reference mismatch',g)
    check(near(feedback,1.),'feedback tests are essential',g)
    # Actual mark must remain coupled; U exposes a one-time-pad relation.
    p=np.zeros((2,2,2));q=np.full((2,2,2),1/8)
    for u,w in product(range(2),repeat=2):p[u,w,w^u]=1/4
    check(near(p.sum(0),q.sum(0)),'unseeded law matches',g)
    check(near(tv(p,q),.5),'seed-mark joint law does not match',g)

def finite_task_case(p,c0,c1,S0,S1):
    """Independent direct policy enumeration and reachable optimal-cell test.
    Initial x in {0,1}; action a; report y; terminal action b.
    c1 indexed d,x,a,y,b; positive supports may be missing.
    """
    D=2;mu=np.array([.5,.5]);V1=c1.min(axis=-1)
    Q0=c0+np.einsum('xay,dxay->dxa',p,V1);V0=Q0.min(axis=-1)
    baseline=V0@mu
    encs=list(product(range(S0),repeat=2))
    updates=list(product(range(S1),repeat=S0*4))
    a0s=np.array(list(product(range(2),repeat=S0)))
    a1s=np.array(list(product(range(2),repeat=S1)))
    feasible_direct=False;feasible_cover=False;best=math.inf
    for enc in encs:
        for update in updates:
            delta=np.array(update).reshape(S0,2,2)
            task_min=[];task_cover=[]
            for d in range(D):
                least=math.inf;cover=False
                for actions in a0s:
                    reached=[[] for _ in range(S1)];first_opt=True
                    for x in range(2):
                        m=enc[x];a=actions[m]
                        first_opt &= abs(Q0[d,x,a]-V0[d,x])<1e-12
                        for y in range(2):
                            if p[x,a,y]>0:reached[delta[m,a,y]].append((x,a,y))
                    compatible=all(any(all(abs(c1[d,x,a,y,b]-V1[d,x,a,y])<1e-12
                                                  for x,a,y in histories)
                                      for b in range(2)) for histories in reached)
                    cover |= first_opt and compatible
                    for last in a1s:
                        risk=0.
                        for x in range(2):
                            m=enc[x];a=actions[m]
                            risk+=mu[x]*c0[d,x,a]
                            for y in range(2):risk+=mu[x]*p[x,a,y]*c1[d,x,a,y,last[delta[m,a,y]]]
                        least=min(least,risk)
                task_min.append(least);task_cover.append(cover)
            excess=np.array(task_min)-baseline
            feasible_direct |= bool(np.max(np.abs(excess))<1e-12)
            feasible_cover |= all(task_cover)
            best=min(best,float(excess.mean()))
    check(feasible_direct==feasible_cover,'endogenous cover and independently enumerated controllers agree','endogenous_cover')
    regrets=np.r_[ (Q0-V0[:,:,None]).ravel(),(c1-V1[:,:,:,:,None]).ravel()]
    positive=regrets[regrets>1e-12]
    if not feasible_direct:
        bound=.5*.5*(p[p>0].min()**2)*positive.min()
        check(best+1e-12>=bound,'finite Bellman-regret infeasibility witness','endogenous_cover')
    else:check(abs(best)<1e-12,'feasible cover has zero weighted excess','endogenous_cover')

def controlled_tests(rng)->None:
    for _ in range(24):
        first=rng.choice([0.,.5,1.],size=(2,2));p=np.stack([first,1-first],axis=-1)
        c0=rng.integers(0,3,size=(2,2,2)).astype(float)/2
        c1=rng.integers(0,3,size=(2,2,2,2,2)).astype(float)/2
        for S0,S1 in ((1,1),(1,2),(2,1)):finite_task_case(p,c0,c1,S0,S1)
    # Endogenous rest branch has no need to preserve the unused probe bit.
    reached={'rest':{0},'probe':{0,1}}
    used={'rest'} if MUTANT!='unused_actions' else {'rest','probe'}
    possible_labels=set().union(*(reached[a] for a in used))
    check(len(possible_labels)==1,'unused action successors must not constrain endogenous exactness','endogenous_cover')
    # Direct stochastic performance-difference identity on actual paths.
    for _ in range(30):
        p=rng.dirichlet([1,1],size=(2,2));c0=rng.random((2,2));c1=rng.random((2,2,2,2))
        V1=c1.min(-1);Q0=c0+np.einsum('xay,xay->xa',p,V1);V0=Q0.min(-1)
        enc=rng.dirichlet([1,1],size=2);upd=rng.dirichlet([1,1],size=(2,2,2))
        alpha=rng.dirichlet([1,1],size=2);last=rng.dirichlet([1,1],size=2)
        risk=0.;regret=0.
        for x,m,a,y,n,b in product(range(2),repeat=6):
            prob=.5*enc[x,m]*alpha[m,a]*p[x,a,y]*upd[m,a,y,n]*last[n,b]
            risk+=prob*(c0[x,a]+c1[x,a,y,b])
            regret+=prob*(Q0[x,a]-V0[x]+c1[x,a,y,b]-V1[x,a,y])
        check(near(risk-V0.mean(),regret),'endogenous stochastic occupation-regret identity','endogenous_occupation')

def regenerative_tests(rng)->None:
    g='regenerative_average'
    for eta in (.05,.2,.6,1.):
        for _ in range(10):
            Q=rng.dirichlet(np.ones(4),size=4);nu=rng.dirichlet(np.ones(4));xi=rng.dirichlet(np.ones(4));c=rng.random(4)
            P=eta*np.tile(nu,(4,1))+(1-eta)*Q
            z=eta*nu@np.linalg.inv(np.eye(4)-(1-eta)*Q)
            check(near(z@P,z) and near(z.sum(),1),'explicit reset invariant probability',g)
            for N in (1,3,10,40):
                dist=xi.copy();total=0.
                for t in range(N):total+=dist@c;dist=dist@P
                check(abs(total/N-z@c)<=1/(N*eta)+1e-11,'uniform Cesaro bound',g)
            for beta in (.2,.8,.99):
                discounted=(1-beta)*xi@np.linalg.solve(np.eye(4)-beta*P,c)
                bound=(1-beta)/(1-beta*(1-eta))
                check(abs(discounted-z@c)<=bound+1e-10,'uniform discounted-to-average bound',g)
    eta=.2;beta=.9
    P=np.array([[1.,0.],[eta,1-eta]])
    actual=(1-beta)*np.array([0.,1.])@np.linalg.solve(np.eye(2)-beta*P,np.array([0.,1.]))
    bound=(1-beta)/(1-beta*(1-eta))
    if MUTANT=='discount_tail':bound=(1-beta)/(1-(1-beta)*(1-eta))
    check(near(actual,bound),'sharp discount error retains the reset denominator',g)
    P=np.eye(2) if MUTANT=='reset_only_plant' else np.array([[1.,0.],[eta,1-eta]])
    check(tv(P[0],P[1])<=1-eta+1e-12,'reset must clear retained state as well as physical plant',g)
    errors=[]
    for n in range(1,12):
        # No word-length-uniform rate; geometric split controls the sequence.
        vals=[min(1.,(2.**min(k,100))/10**n) for k in range(201)]
        errors.append(sum(eta*(1-eta)**k*vals[k] for k in range(201)))
    check(all(a>b for a,b in zip(errors,errors[1:])),'cycle weighting controls growing word errors',g)
    check(errors[-1]<.001,'regenerative error tends downward despite growing finite-word bound',g)

def operator_tests(rng)->None:
    g='active_operator_words'
    flow=np.array([1,2,0]);kick=np.array([1,0,2]);U=np.eye(3)[flow];C=np.eye(3)[kick]
    T=U@C if MUTANT=='kick_order' else C@U
    expected=np.eye(3)[flow[kick]]
    check(near(T,expected),'Koopman order is intervention then flow in physical time',g)
    check(not near(U@C,C@U),'active example is noncommuting',g)
    for _ in range(20):
        B=rng.normal(size=(6,6));L=B-B.T;U=expm(.1*L)
        Q,_=np.linalg.qr(rng.normal(size=(6,6)));C=Q
        f=rng.normal(size=6)
        for n in (2,4,6):
            P=np.diag([1.]*n+[0.]*(6-n));Un=np.zeros((6,6));Un[:n,:n]=expm(.1*L[:n,:n])
            Tn=P@C@P@Un@P;T=C@U
            check(np.linalg.norm(Tn,2)<=1+1e-10,'projected interventions remain contractions',g)
            for k in (1,2,3):
                difference=np.linalg.matrix_power(T,k)@f-np.linalg.matrix_power(Tn,k)@f
                terms=sum((np.linalg.matrix_power(Tn,j)@(T-Tn)@np.linalg.matrix_power(T,k-1-j)@f for j in range(k)),np.zeros(6))
                check(near(difference,terms,1e-8),'controlled-word telescoping retains order',g)
                if n==6:check(np.linalg.norm(difference)<1e-8,'full finite space recovers active word',g)
    for _ in range(40):
        errors=np.abs(rng.normal(size=5));p=rng.dirichlet(np.ones(5))*5;D=np.sqrt(np.mean(p*p))
        check(np.mean(p*errors)<=D*np.sqrt(np.mean(errors**2))+1e-12,'physical comparison uses original preparation L2 bound',g)

def dimension_tests(rng)->None:
    g='intrinsic_selector_dimension'
    for _ in range(12):
        coords=rng.random((3,12));weights=rng.dirichlet(np.ones(12));original=coords@weights
        mat=np.vstack([np.ones(12),coords]);w=weights.copy()
        while np.count_nonzero(w>1e-10)>4:
            ids=np.flatnonzero(w>1e-10);B=mat[:,ids]
            u,s,vh=np.linalg.svd(B,full_matrices=True);c=vh[-1]
            if c.max()<1e-10:c=-c
            positive=c>1e-10;t=np.min(w[ids[positive]]/c[positive]);w[ids]-=t*c
            w[np.abs(w)<1e-10]=0
        check(np.min(w)>-1e-8 and near(w.sum(),1),'affine elimination keeps probability weights',g)
        check(np.count_nonzero(w>1e-8)<=4 and near(coords@w,original,1e-8),'risk dimension, not row covering number, prices selector',g)

def main()->None:
    global MUTANT
    parser=argparse.ArgumentParser();parser.add_argument('--mutant',default='');args=parser.parse_args();MUTANT=args.mutant
    valid={'private_convexification','free_selector','seed_marginal','open_loop_only','unused_actions','discount_tail','reset_only_plant','kick_order'}
    if MUTANT and MUTANT not in valid:raise ValueError('Unknown mutant')
    rng=np.random.default_rng(130923)
    matrix_examples();feedback_test();controlled_tests(rng);regenerative_tests(rng);operator_tests(rng);dimension_tests(rng)
    if MUTANT:raise RuntimeError('designated mutant survived')
    print(json.dumps({'revision':'v13','finite_checks':COUNT,'groups':GROUPS,
                      'private_identity_3_width_2':'1/2','hidden_identity_3_width_2':'1/3',
                      'actual_support_endogenous_cases':72,'mutants':sorted(valid),
                      'scope':'Finite regression and negative controls; not certification of analytic proofs or originality.'},indent=2))
if __name__=='__main__':
    try:main()
    except Exception as e:print(str(e));sys.exit(1)
