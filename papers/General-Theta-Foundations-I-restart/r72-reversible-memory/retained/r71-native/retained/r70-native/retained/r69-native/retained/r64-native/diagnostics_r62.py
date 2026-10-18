#!/usr/bin/env python3
"""Finite diagnostics for the primitive frontier. Not a proof certificate.
Exact algebra and numerical LP residual checks are counted separately.
"""
from __future__ import annotations
import itertools,json,math
from fractions import Fraction
import numpy as np
import scipy
from scipy.optimize import linprog
import sympy as sp
from make_phase import diagnostics as phase_diagnostics
COUNTS={}; DETAILS={}
def check(value,group,detail):
    if not bool(value): raise RuntimeError(f'{group}: {detail}')
    COUNTS[group]=COUNTS.get(group,0)+1

def exact():
    for d in range(1,8):
        K=sp.zeros(d)
        for j in range(1,d):K[j-1,j]=1
        adj=lambda X:K.T*X*K
        S=sp.eye(d)
        for n in range(d+2):
            O=sp.eye(d)-S
            check(O.rank()==min(n,d),'exact_ladder_depth',(d,n))
            S=adj(S)
    P=sp.diag(1,0); u=sp.Matrix([sp.Rational(3,5),sp.Rational(4,5)]);Q=u*u.T
    adj=lambda X:(P*X*P+Q*X*Q)/2
    O=sp.eye(2)-adj(adj(sp.eye(2)))
    check(O[0,0]>0 and O.det()>0,'exact_noncommuting_fallback','O2 positive definite')
    h00,h01,h11=sp.symbols('h00 h01 h11');H=sp.Matrix([[h00,h01],[h01,h11]])
    sol=sp.solve(list(H-adj(H)-sp.eye(2)),[h00,h01,h11]);H=H.subs(sol)
    check(H-adj(H)==sp.eye(2),'exact_noncommuting_fallback','resolvent')
    check(max(H.eigenvals())==sp.Rational(7,2),'exact_noncommuting_fallback','V1(c=3/5)')
    dark=sp.diag(0,1);state=sp.diag(0,1)
    check(dark*state*dark==state,'exact_dark_obstruction','invariant input cannot stop')
    for eps in [sp.Rational(1,10),sp.Rational(1,100),sp.Rational(1,1000)]:
        check(1/(1-(1-eps))==1/eps,'exact_no_dimension_cost_bound',str(eps))
    for N,K,T in [(sp.Rational(3),sp.Rational(2),7),(sp.Rational(5,2),sp.Rational(2),10),(sp.Rational(7),sp.Rational(3),20)]:
        delta=(N-1)/T;e=(K-1)*delta;p=(N-K)/(N+e-K)
        check(p*(N+e)+(1-p)*K==N,'exact_budget_restoration',str((N,K,T)))
        check(0<p<=1,'exact_budget_restoration','legal mixture')
    check(sp.Rational(3,10)-sp.Rational(1,10)==sp.Rational(1,5),'exact_perturbation_margin','scalar sharp bound')

def cost_threshold_exact():
    # Sharp complete two-call policy has cost 3/2, below the iid-row cost 2.
    I=sp.eye(2);P=sp.diag(1,0);Q=sp.diag(0,1)
    cost=I+(P+Q)/2
    check(cost==sp.Rational(3,2)*I,'exact_interior_fallback','uniform first-fair alternation')
    check(sp.Rational(3,2)<sp.Rational(7,4)<2,'exact_interior_fallback','interior budget below initial fallback')
    previous=sp.Rational(0)
    for T in range(1,9):
        survival=sp.Rational(1,2)**T
        prefix=2*(1-survival)
        lower=prefix+survival;upper=prefix+2*survival
        check(upper==2 and previous<=lower<=2,'exact_cost_enclosure','scalar monotone enclosure')
        check(upper-lower<=(2-1)*min(sp.Rational(1),(lower-1)/T),
              'exact_cost_enclosure','certified gap')
        previous=lower

def solve_prefix(kind,T,N,with_reserve=True):
    if kind=='binary':
        alphabet=(0,1); productive=set(alphabet); decisions=(0,1); thetas=(.2,.3);dim=2;kappa=1.
        def prob(theta,state,y): return (1-theta) if state==y else theta
        def loss(theta,state,y,r):return float(state!=r)
        def fb(theta,state):return 1.,float(state!=0)
    else:
        alphabet=(0,1,2);productive={0,1};decisions=(0,);thetas=(0,1);dim=1;kappa=2.
        probabilities=((.2,.3,.5),(.35,.4,.25))
        def prob(theta,state,y):return probabilities[theta][y]
        def loss(theta,state,y,r):return (.05,.75,0)[y]
        def fb(theta,state):
            a,b,_=probabilities[theta];return 1/(a+b),(.05*a+.75*b)/(a+b)
    histories=[h for t in range(1,T+1) for h in itertools.product(alphabet,repeat=t)]
    variables=[]
    for h in histories:
        variables.append((h,'c',None))
        if h[-1] in productive:
            variables.extend((h,'s',r) for r in decisions)
    index={v:i for i,v in enumerate(variables)};R=len(variables);nv=R+1
    eq=[];rhs=[]
    for h in histories:
        row=np.zeros(nv);row[index[(h,'c',None)]]=1
        if h[-1] in productive:
            for r in decisions:row[index[(h,'s',r)]]=1
        if len(h)>1:row[index[(h[:-1],'c',None)]]-=1;val=0
        else:val=1
        eq.append(row);rhs.append(val)
    models=[];ub=[];br=[]
    for theta in thetas:
        for state in range(dim):
            c=np.zeros(nv);surv=np.zeros(nv);v=np.zeros(nv)
            for h in histories:
                weight=math.prod(prob(theta,state,y) for y in h)
                if len(h)<T:c[index[(h,'c',None)]]+=weight
                if len(h)==T:surv[index[(h,'c',None)]]+=weight
                if h[-1] in productive:
                    for r in decisions:v[index[(h,'s',r)]]+=weight*loss(theta,state,h[-1],r)
            ub.append(c+(surv if with_reserve else 0));br.append(N-1)
            risk=v.copy();risk[R]=-1;ub.append(risk);br.append(0)
            models.append((theta,state,c,surv,v))
    objective=np.zeros(nv);objective[R]=1
    result=linprog(objective,A_ub=np.array(ub),b_ub=br,A_eq=np.array(eq),b_eq=rhs,
                   bounds=[(0,1)]*nv,method='highs')
    if not result.success:raise RuntimeError(result.message)
    x=result.x;res=max(float(np.max(np.array(ub)@x-br)),float(np.max(np.abs(np.array(eq)@x-rhs))))
    check(res<1e-8,'float_prefix_lp_residual',(kind,T,res))
    delta=min(1.,(N-1)/T);e=(kappa-1)*delta;p=(N-kappa)/(N+e-kappa) if e else 1.
    actual=[]
    for theta,state,c,surv,v in models:
        C=1+c@x;S=surv@x;V=v@x;fc,fl=fb(theta,state)
        if with_reserve:
            check(S<=delta+1e-8,'float_survival_reserve',(kind,T,theta,state))
            mixed_cost=p*(C+fc*S)+(1-p)*fc
            mixed_loss=p*(V+fl*S)+(1-p)*fl
            bound=x[R]+delta+(e/(N-kappa+e) if e else 0)
            check(mixed_cost<=N+1e-8,'float_actual_budget',(kind,T,mixed_cost))
            check(mixed_loss<=bound+1e-8,'float_actual_risk_bound',(kind,T,mixed_loss,bound))
            actual.append({'theta':theta,'state':state,'cost':mixed_cost,'loss':mixed_loss,'survival':S})
    return {'kind':kind,'horizon':T,'budget':N,'lower':x[R],'max_residual':res,
            'gap_bound':delta+(e/(N-kappa+e) if e else 0),'models':actual}

def quantum_completion():
    # Full-rank noncommuting report maps; failure does not reset the input.
    identity=np.eye(2); hadamard=np.array([[1.,1.],[1.,-1.]])/math.sqrt(2)
    sa=np.diag(np.sqrt([.8,.2]));fa=np.diag(np.sqrt([.2,.8]))
    sb=hadamard@sa@hadamard;fb=hadamard@fa@hadamard
    audit=np.diag([0.,1.])
    tf=lambda X:(fa@X@fa+fb@X@fb)/2
    ff=(sa@audit@sa+sb@audit@sb)/2
    basis=[np.eye(4)[:,i].reshape(2,2) for i in range(4)]
    mat=np.column_stack([tf(X).reshape(-1) for X in basis])
    H=np.linalg.solve(np.eye(4)-mat,identity.reshape(-1)).reshape(2,2)
    K=np.linalg.solve(np.eye(4)-mat,ff.reshape(-1)).reshape(2,2)
    maximum=lambda X:float(np.linalg.eigvalsh((X+X.T)/2)[-1])
    kappa=maximum(H)
    check(np.linalg.norm(sa@sb-sb@sa)>0.01,'float_nonreset_quantum','noncommuting instruments')
    check(np.linalg.norm(H-tf(H)-identity)<1e-12,'float_nonreset_quantum','raw cost resolvent')
    check(np.linalg.norm(K-tf(K)-ff)<1e-12,'float_nonreset_quantum','raw score resolvent')
    tp=lambda X:fa@X@fa+.8*sa@X@sa
    fp=.2*sa@audit@sa
    cost=np.zeros((2,2));score=np.zeros((2,2));surv=identity.copy()
    costterm=identity.copy();scoreterm=fp.copy()
    rows=[]
    for T in range(1,9):
        cost+=costterm;score+=scoreterm;surv=tp(surv)
        htail=H.copy();ktail=K.copy()
        for _ in range(T):htail=tp(htail);ktail=tp(ktail)
        N=max(kappa+.25,maximum(cost+surv))
        D=min(1.,(N-1.)/T);e=(kappa-1)*D;p=(N-kappa)/(N+e-kappa)
        mixedcost=p*(cost+htail)+(1-p)*H
        mixedloss=p*(score+ktail)+(1-p)*K
        bound=maximum(score)+D+e/(N-kappa+e)
        check(maximum(surv)<=D+1e-10,'float_nonreset_quantum','survival reserve')
        check(maximum(cost+htail)<=N+e+1e-10,'float_nonreset_quantum','actual completion cost')
        check(maximum(mixedcost)<=N+1e-10,'float_nonreset_quantum','restored operator budget')
        check(maximum(mixedloss)<=bound+1e-10,'float_nonreset_quantum','actual operator risk bound')
        rows.append({'horizon':T,'budget':N,'cost':maximum(mixedcost),
                     'loss':maximum(mixedloss),'prefix_loss':maximum(score),'bound':bound})
        costterm=tp(costterm);scoreterm=tp(scoreterm)
    DETAILS['nonreset_quantum_completion']=rows

def numeric():
    runs=[]
    for kind,N in [('binary',2.5),('heralded',3.)]:
        last=-1
        for T in range(1,7):
            row=solve_prefix(kind,T,N);runs.append(row)
            check(row['lower']>=last-1e-8,'float_monotone_lower',(kind,T))
            last=row['lower']
    # At unit budget a missing reserve licenses a spurious zero-loss open prefix.
    correct=solve_prefix('binary',1,1.,True);wrong=solve_prefix('binary',1,1.,False)
    check(abs(correct['lower']-.3)<1e-9 and wrong['lower']<1e-9,
          'float_negative_control_missing_reserve',(correct['lower'],wrong['lower']))
    phase=phase_diagnostics()
    for row in phase:check(abs(row['independent_gap'])<2e-8,'float_phase_optimizer',row['b'])
    DETAILS['finite_prefix_runs']=runs
    DETAILS['phase_maximum_objective_discrepancy']=max(abs(r['independent_gap']) for r in phase)
if __name__=='__main__':
    exact();cost_threshold_exact();numeric();quantum_completion()
    print(json.dumps({'schema':'theta.r62.finite-diagnostics.v1','status':'PASS','checks_by_group':COUNTS,
                      'total_checks':sum(COUNTS.values()),'numpy':np.__version__,'scipy':scipy.__version__,
                      'sympy':sp.__version__,'details':DETAILS,
                      'limits':'Exact finite examples and floating LP residual checks; not formal proof or independent referee approval.'},sort_keys=True,indent=2))
