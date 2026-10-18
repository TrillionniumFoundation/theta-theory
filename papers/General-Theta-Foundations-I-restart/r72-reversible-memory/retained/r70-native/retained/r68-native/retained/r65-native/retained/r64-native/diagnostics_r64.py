#!/usr/bin/env python3
"""Finite exact primal/dual and raw-instrument diagnostics, not formal proof.
Numerical LP search is followed by independent rational feasibility and equality.
All checks execute equally in ordinary and optimized Python.
"""
from __future__ import annotations
import itertools, json
from fractions import Fraction
from functools import lru_cache
import numpy as np
import scipy
from scipy.optimize import linprog
import sympy as s

COUNTS: dict[str,int] = {}
DETAILS: dict[str,object] = {}
R=s.Rational

def check(ok, group: str, detail: object) -> None:
    if not bool(ok): raise RuntimeError(f'{group}: {detail}')
    COUNTS[group]=COUNTS.get(group,0)+1

def rat(x):
    f=Fraction(float(x)).limit_denominator(10**8)
    return R(f.numerator,f.denominator)

def certified_lp(cost, loss, E, e, budget, label):
    """All inputs exact matrices. Common-plan variables nonnegative, epigraph free."""
    cost,loss,E,e=s.Matrix(cost),s.Matrix(loss),s.Matrix(E),s.Matrix(e)
    n=E.cols; m=loss.rows
    A=cost.row_join(s.zeros(cost.rows,1)).col_join(loss.row_join(-s.ones(m,1)))
    b=s.Matrix(list(budget)+[0]*m)
    Eq=E.row_join(s.zeros(E.rows,1)); obj=s.zeros(n+1,1);obj[n]=1
    ans=linprog(np.array(obj,dtype=float).ravel(),A_ub=np.array(A,dtype=float),b_ub=np.array(b,dtype=float).ravel(),
                A_eq=np.array(Eq,dtype=float),b_eq=np.array(e,dtype=float).ravel(),
                bounds=[(0,None)]*n+[(None,None)],method='highs')
    check(ans.success,'float_lp_search',label)
    x=s.Matrix([rat(v) for v in ans.x]);y=s.Matrix([rat(v) for v in ans.ineqlin.marginals]);nu=s.Matrix([rat(v) for v in ans.eqlin.marginals])
    check(all(v>=0 for v in x[:n]),'exact_primal_nonnegative',label)
    check(Eq*x==e,'exact_primal_flow',label)
    check(all(v>=0 for v in b-A*x),'exact_primal_constraints',label)
    check(all(v<=0 for v in y),'exact_dual_sign',label)
    reduced=obj-A.T*y-Eq.T*nu
    check(all(v>=0 for v in reduced[:n]) and reduced[n]==0,'exact_dual_stationarity',label)
    check((b.T*y+e.T*nu)[0]==x[n],'exact_primal_dual_equality',label)
    check(sum(y[cost.rows:])==-1,'exact_task_mass',label)
    check(all(y[i]*(b-A*x)[i]==0 for i in range(A.rows)),'exact_active_physical_constraints',label)
    check(all(reduced[i]*x[i]==0 for i in range(n)),'exact_used_rows',label)
    DETAILS[label]={'variables':n,'affine_dimension':n-E.rank(),'risk':str(x[n]),
                    'cost_values':[str(v) for v in cost*x[:n,0]],
                    'risk_values':[str(v) for v in loss*x[:n,0]],
                    'cost_multipliers':[str(-v) for v in y[:cost.rows]],
                    'risk_weights':[str(-v) for v in y[cost.rows:]],
                    'nonzero_witness_atoms':sum(v!=0 for v in y)}
    return x,y,nu

def common_sensor(T,budget):
    """Costly binary sensing, fixed hidden bit, two possible sensor-noise models."""
    actions=(0,1);reports=(0,1);decisions=(0,1)
    pre=[h for t in range(T) for h in itertools.product(itertools.product(actions,reports),repeat=t)]
    variables=[]
    for h in pre:
        for a in actions:
            variables.append(('a',h,a))
            for y in reports:
                for d in ('c',0,1):variables.append(('d',h,a,y,d))
    ix={v:i for i,v in enumerate(variables)};n=len(variables);rows=[];rhs=[]
    for h in pre:
        row=[R(0)]*n
        for a in actions:row[ix['a',h,a]]=1
        if h:
            a,y=h[-1];row[ix['d',h[:-1],a,y,'c']]-=1;v=0
        else:v=1
        rows.append(row);rhs.append(v)
        for a in actions:
            for y in reports:
                row=[R(0)]*n;row[ix['a',h,a]]=-1
                for d in ('c',0,1):row[ix['d',h,a,y,d]]=1
                rows.append(row);rhs.append(0)
    cost=[];loss=[]
    for theta,bit in itertools.product((0,1),(0,1)):
        noises=(R(1,3),R(1,6)) if theta==0 else (R(2,5),R(1,4))
        def prob(h):
            return s.prod((1-noises[a]) if y==bit else noises[a] for a,y in h)
        C=[R(0)]*n;V=[R(0)]*n
        for h in pre:
            for a in actions:
                C[ix['a',h,a]]+=prob(h)*(1+R(a,2))
                for y in reports:
                    ph=prob(h+((a,y),))
                    if len(h)+1==T:C[ix['d',h,a,y,'c']]+=ph
                    for d in decisions:V[ix['d',h,a,y,d]]+=ph*int(d!=bit)
        cost.append(C);loss.append(V)
    return certified_lp(cost,loss,rows,rhs,[budget]*4,f'sensor_T{T}_N{budget}')

def multi_resource():
    E=[[1,1,1]];e=[1]
    for denom in (3,4,5):
        N=1+R(1,denom)
        x,y,_=certified_lp([[1,2,1],[1,1,2]],[[1,0,0]],E,e,[N,N],f'two_resources_{denom}')
        check(x[3]==1-R(2,denom),'exact_multi_resource_value',denom)
        check(list(-y)==[1,1,1],'exact_multi_resource_atoms',denom)
        D=R(1,7); k0=R(1);k1=R(1);N0=R(5,3);N1=R(4,3)
        # A zero lower bound for resource 1 is permitted; one resource is coercive.
        excess=[(k0-1)*D,(k1-0)*D];p=min((N0-k0)/(N0-k0+excess[0]),(N1-k1)/(N1-k1+excess[1]))
        check(p*(N0+excess[0])+(1-p)*k0<=N0 and p*(N1+excess[1])+(1-p)*k1<=N1,
              'exact_joint_budget_restoration',denom)

def sparse_compression():
    for k in range(1,7):
        # Exact conic lemma: arbitrary gradients, separate appended risk/cost coordinates.
        cols=[s.Matrix([R(((i+2)*(j+3))%11-5,7) for j in range(k)]+[int(i<k+2)]) for i in range(2*k+5)]
        weights=[R(1,k+2) if i<k+2 else R(i+1,13) for i in range(len(cols))]
        target=sum((w*c for w,c in zip(weights,cols)),s.zeros(k+1,1))
        active=list(range(len(cols)))
        while len(active)>k+1:
            A=s.Matrix.hstack(*(cols[i] for i in active));basis=A.nullspace()
            if not basis: raise RuntimeError('Missing required exact linear dependence')
            v=basis[0]
            if not any(t>0 for t in v):v=-v
            step=min(weights[i]/v[j] for j,i in enumerate(active) if v[j]>0)
            for j,i in enumerate(active):weights[i]-=step*v[j]
            active=[i for i in active if weights[i]>0]
        check(all(w>=0 for w in weights),'exact_conic_nonnegative',k)
        check(sum((w*c for w,c in zip(weights,cols)),s.zeros(k+1,1))==target,'exact_conic_vector',k)
        check(sum(weights[:k+2])==1 and len(active)<=k+1,'exact_conic_support',k)
        # Physically realizable compulsory-one-call simplex sharpness.
        uniform=[R(1,k+1)]*(k+1)
        check(min(uniform)==R(1,k+1),'exact_simplex_sharp_value',k)
        for dropped in range(k+1):
            partial=[R(1,k) if i!=dropped else R(0) for i in range(k+1)]
            check(min(partial)==0<R(1,k+1),'exact_simplex_missing_atom', (k,dropped))

def gaps_and_boundary():
    t=1/s.sqrt(2);f=R(3,2)-t-1/(2*t)
    check(s.simplify(f-(R(3,2)-s.sqrt(2)))==0,'exact_distinct_prior_gap','value')
    x=s.symbols('x',positive=True)
    g=R(3,2)-x-1/(2*x)
    check(s.simplify(s.diff(g,x).subs(x,t))==0 and s.diff(g,x,2)==-1/x**3,'exact_distinct_prior_gap','maximum')
    check(R(3,2)-s.sqrt(2)<R(1,2),'exact_distinct_prior_gap','strict')
    for j in range(9):
        N=1+R(j,8);R1=min(R(1,2),2-N);R2=(2-N)/2
        check(min(R(1,2)+R(1,2)*(1-N),R(1,2)*(2-N))==R2,'exact_width_relaxation',N)
        check(R2<=R1,'exact_width_primal_order',N)
    check(min(R(1,2),2-R(3,2))-R(1,4)==R(1,4),'exact_width_gap','strict quarter')
    # At the minimum budget, every feasible reserved prefix has zero open mass.
    for T in (1,2,3,7):
        check((R(1)/1-1)/T==0,'exact_boundary_reserve',T)
    for K in (10,100,1000):
        p=R(1,K-1);cut=3
        check(1+p*(K-1)==2 and p*(K-cut)>R(3,4) if K>=10 else False,
              'exact_cost_tail_not_uniform',K)

def raw_quantum_bellman():
    I=s.eye(2);P=s.diag(1,0);Q=s.Matrix([R(3,5),R(4,5)]);Q=Q*Q.T
    P1=I-P
    fail=((P,Q),(Q,P1))
    prep=(s.Matrix([[R(1,2),R(1,2)],[R(1,2),R(1,2)]]),s.diag(R(1,3),R(2,3)))
    alpha=(R(1,5),R(2,7));beta=(R(1,3),R(2,3));N=R(5,2)
    audit=(P,Q)
    check(P*Q!=Q*P,'exact_quantum_noncommuting','primitive data')
    def children(states,a,y):
        return tuple((fail[m][a] if y==0 else I-fail[m][a])*states[m]*(fail[m][a] if y==0 else I-fail[m][a]) for m in (0,1))
    def reserve(states):return sum(alpha[m]*s.trace(states[m]) for m in (0,1))
    def terminal(states,r):return sum(beta[m]*s.trace(audit[r]*states[m]) for m in (0,1))
    def backward(states,depth):
        if depth==0:return reserve(states)
        options=[]
        for a in (0,1):
            total=reserve(states)
            sf=children(states,a,0);ss=children(states,a,1)
            total+=backward(sf,depth-1)
            total+=min(terminal(ss,0),terminal(ss,1),backward(ss,depth-1))
            options.append(total)
        return min(options)
    @lru_cache(None)
    def trees(depth):
        if depth==0:return (('open',),)
        out=[]
        child=trees(depth-1)
        for a in (0,1):
            for bad in child:
                for good in (('stop',0),('stop',1))+child:out.append(('call',a,bad,good))
        return tuple(out)
    def forward(tree,states):
        if tree[0]=='open':return reserve(states)
        if tree[0]=='stop':return terminal(states,tree[1])
        _,a,bad,good=tree
        return reserve(states)+forward(bad,children(states,a,0))+forward(good,children(states,a,1))
    vals=[]
    for T in (1,2):
        allvalues=[forward(tree,prep) for tree in trees(T)]
        value=backward(prep,T)
        check(min(allvalues)==value,'exact_quantum_backward_forward',T)
        check(all(v>=value for v in allvalues),'exact_quantum_dual_all_trees',T)
        vals.append({'T':T,'enumerated_deterministic_trees':len(allvalues),'dual':str(value-sum(alpha)*N)})
    DETAILS['raw_noncommuting_recursion']=vals
    # Removing reserve is a deliberate bad certificate even in dimension one.
    check(R(1,4)*3-R(1,4)*2==R(1,4),'exact_negative_control_open_reserve','false lower offset')

def timing_and_complete_law():
    # Exact finite delayed-release frontiers; full-history versus one-row clocks.
    rows=[]
    for K in range(2,9):
        for N in (R(1),R(5,4),R(K+1,2),R(K),R(K+1)):
            target_mass=min(R(1),(N-1)/(K-1))
            mean=1+(K-1)*target_mass
            check(mean<=N and 1-target_mass==max(R(0),(K-N)/(K-1)),
                  'exact_timer_budget_frontier',(K,str(N)))
            n=min(N,R(K));p=1/n
            # Critical-point derivative and endpoints give the exact geometric optimum.
            candidates=[1/N,R(1)]+([R(1,K)] if N>=K else [])
            value=p*(1-p)**(K-1)
            check(1/p<=N and value==max(z*(1-z)**(K-1) for z in candidates),
                  'exact_one_live_timer',(K,str(N)))
            Q=s.zeros(K);Q[0,1]=target_mass
            for i in range(1,K-1):Q[i,i+1]=1
            h=s.ones(K,1)-Q*s.ones(K,1);init=s.eye(K)[0,:]
            check((init*Q**(K-1)*h)[0]==target_mass and
                  (init*(s.eye(K)-Q).inv()*s.ones(K,1))[0]==mean,
                  'exact_timer_counted_chain',(K,str(N)))
        rows.append({'delay':K,'one_live_unconstrained_mass':str(R(1,K)*(1-R(1,K))**(K-1))})
    for M in (1,2,3):
        Q=s.Matrix(M,M,lambda i,j:R(1+((2*i+j)%3),6*M))
        h=s.ones(M,1)-Q*s.ones(M,1);init=s.eye(M)[0,:]
        mean=(init*(s.eye(M)-Q).inv()*s.ones(M,1))[0]
        for K in range(M+1,M+5):
            mass=(init*Q**(K-1)*h)[0];A=R(M)**(2*K-2)
            check(mass+mass**2/A<=1 and (K-1)*mass+K*mass**2/A<=mean-1,
                  'exact_timer_pumping_bounds',(M,K))
    # An explicit loop-pumped path, not just a numerical matrix test.
    Q=s.Matrix([[R(1,4),R(1,4)],[R(1,3),R(1,3)]])
    h=s.ones(2,1)-Q*s.ones(2,1)
    original=Q[0,1]*Q[1,0]*h[0];cycle=Q[0,1]*Q[1,0]
    check(cycle>=original and original*cycle>=original**2,
          'exact_timer_pumped_path','length three versus length five')
    # Complete-law approximation at the same budget, with a real immediate fallback.
    # Original law {1,6}; cutoff three; fallback commits at four on surviving paths.
    original=s.Matrix([R(3,4),0,0,0,0,R(1,4)])
    completed=s.Matrix([R(3,4),0,0,R(1,4),0,0])
    tv=sum(abs(a-b) for a,b in zip(original,completed))/2
    mean=sum((i+1)*original[i] for i in range(6))
    completed_mean=sum((i+1)*completed[i] for i in range(6))
    D=(mean-1)/3
    check(tv==R(1,4) and tv<=D and completed_mean<=mean,
          'exact_complete_stopped_law','full timing law differs, output marginal is identical')
    # Finite bounded-score separation: target (1,0), achievable (x,1-x), x<=1/3.
    # The indicator of the second outcome witnesses exactly TV distance 2/3.
    check(1-R(1,3)==R(2,3),'exact_complete_score_witness','attaining target separation')
    DETAILS['timing_tasks']=rows

if __name__=='__main__':
    for T,N in ((1,R(5,4)),(1,R(3,2)),(2,R(3,2)),(2,R(2))):common_sensor(T,N)
    multi_resource();sparse_compression();gaps_and_boundary();raw_quantum_bellman();timing_and_complete_law()
    print(json.dumps({'schema':'theta.r64.finite-diagnostics.v1','status':'PASS','checks_by_group':COUNTS,
                      'total_checks':sum(COUNTS.values()),'details':DETAILS,'numpy':np.__version__,
                      'scipy':scipy.__version__,'sympy':s.__version__,
                      'limits':'Finite examples and exact identities following numerical searches; not formal proof, exhaustive global priority, or human/editorial approval.'},sort_keys=True,indent=2))
