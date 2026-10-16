#!/usr/bin/env python3
"""Finite exact certificates and independent raw-instrument diagnostics.
No sample grid is described as proof of a continuum theorem. No assert gates.
"""
from __future__ import annotations
import itertools,json,math
from fractions import Fraction as Q
import numpy as np
import scipy
from scipy.optimize import linprog
COUNTS={};DETAILS={}
def check(ok,group,detail):
    if not bool(ok): raise RuntimeError(f'{group}: {detail}')
    COUNTS[group]=COUNTS.get(group,0)+1

def dot(a,b):return sum((x*y for x,y in zip(a,b)),Q(0))

def exact_boundaries():
    for den in [3,10,101,10001]:
        eps=Q(1,den)
        check(1+eps>1,'exact_boundary_discontinuity','good action becomes infeasible at N=1')
        check(Q(1)-Q(0)==1,'exact_boundary_discontinuity','optimal losses 1 versus 0')
    for T in [1,2,5,20]:
        for den in [2,7,100]:
            eps=Q(1,den);k=Q(2)
            actual=1+eps*(T-1+k)
            bound=eps*(T-1+k)
            check(actual-1==bound,'exact_cost_horizon_sharpness',(T,den))
    for n in [2,4,10,32]:
        risks=[2*Q(i,n)*(1-Q(i,n)) for i in range(n+1)]
        check(risks[0]==risks[-1]==0 and max(risks)==Q(1,2),
              'exact_vertex_risk_failure',n)
        for t in risks:check(t<=Q(1,2),'exact_bernoulli_upper',n)
    # One-call scalar family: exact finite-horizon primal value and analytic lower.
    for T in range(2,13):
        N=Q(3,2);D=(N-1)/T;q=(1-D)/2
        prefix=1+(T-1)*D
        check(prefix+D==N,'exact_bernoulli_reserved_cost',T)
        check(q==(1-D)/2,'exact_bernoulli_half_model_lower',T)
        for i in range(17):
            theta=Q(i,16)
            loss=(1-D)*2*theta*(1-theta)+D*theta
            check(loss<=q+D,'exact_bernoulli_completion',str((T,i)))
    for N,k,T,eps in [(Q(3),Q(2),11,Q(1,200)),(Q(3,2),Q(1),10,Q(1,1000)),(Q(5),Q(3),30,Q(1,10000))]:
        D=min(Q(1),(N-1)/T)
        e=(k-1)*D+N*(eps+eps*(T-1+k))
        p=(N-k)/(N-k+e)
        check(p*(N+e)+(1-p)*k==N,'exact_compact_budget_restoration',(N,k,T))
        check(0<p<=1,'exact_compact_budget_restoration','probability legal')
    # Switching dark path: exact 2x2 integer Kraus computations.
    A=np.array([[0,1],[0,0]],dtype=int);B=A.T;rho=np.diag([0,1])
    check(np.array_equal(A@A,np.zeros((2,2),dtype=int)) and np.array_equal(B@B,np.zeros((2,2),dtype=int)),
          'exact_switching_negative_control','each fixed model terminates within two')
    for _ in range(12):
        rho=A@rho@A.T;check(np.trace(rho)==1,'exact_switching_negative_control','failure under model one')
        rho=B@rho@B.T;check(np.trace(rho)==1,'exact_switching_negative_control','failure under model two')

def lp_data(T,N,models):
    histories=[h for t in range(1,T+1) for h in itertools.product((0,1),repeat=t)]
    variables=[(h,tag) for h in histories for tag in ('c','s0','s1')]
    ix={v:i for i,v in enumerate(variables)};nv=len(variables)+1;qi=nv-1
    eq=[];er=[];ub=[];br=[]
    def zeros():return [Q(0)]*nv
    for h in histories:
        row=zeros()
        for tag in ('c','s0','s1'):row[ix[(h,tag)]]=1
        val=Q(1)
        if len(h)>1:row[ix[(h[:-1],'c')]]=-1;val=Q(0)
        eq.append(row);er.append(val)
    coeffs={}
    for theta in models:
        for state in (0,1):
            c=zeros();s=zeros();v=zeros()
            for h in histories:
                w=math.prod((1-theta if y==state else theta) for y in h)
                if len(h)<T:c[ix[(h,'c')]]+=w
                else:s[ix[(h,'c')]]+=w
                v[ix[(h,'s'+str(1-state))]]+=w
            ub.append([a+b for a,b in zip(c,s)]);br.append(N-1)
            row=v.copy();row[qi]=-1;ub.append(row);br.append(Q(0))
            coeffs[(theta,state)]=(c,s,v)
    obj=zeros();obj[qi]=1
    return histories,ix,eq,er,ub,br,obj,coeffs

def solve_and_certify(T,N,models):
    histories,ix,Aeq,beq,A,b,c,coeffs=lp_data(T,N,models)
    res=linprog(np.array(c,dtype=float),A_ub=np.array(A,dtype=float),b_ub=np.array(b,dtype=float),
        A_eq=np.array(Aeq,dtype=float),b_eq=np.array(beq,dtype=float),bounds=(0,None),method='highs')
    check(res.success,'float_model_net_lp_status',str((T,res.message)))
    # Recover rational primal and dual. This is not a tolerance-based exact claim.
    x=[Q(float(t)).limit_denominator(10**9) for t in res.x]
    y=[Q(float(t)).limit_denominator(10**9) for t in res.ineqlin.marginals]
    z=[Q(float(t)).limit_denominator(10**9) for t in res.eqlin.marginals]
    primal=all(t>=0 for t in x) and all(dot(row,x)<=v for row,v in zip(A,b)) and all(dot(row,x)==v for row,v in zip(Aeq,beq))
    dual=all(t<=0 for t in y) and all(sum((A[j][i]*y[j] for j in range(len(A))),Q(0))+sum((Aeq[j][i]*z[j] for j in range(len(Aeq))),Q(0))<=c[i] for i in range(len(c)))
    pv=dot(c,x);dv=dot(b,y)+dot(beq,z)
    check(primal,'exact_model_net_primal',T)
    check(dual,'exact_model_net_dual',T)
    check(pv==dv,'exact_model_net_strong_duality',(T,str(pv),str(dv)))
    # The raw model interval is theta in [1/5,3/10]. Uniform mesh radius exact.
    eps=max(b-a for a,b in zip(models,models[1:]))/2
    D=min(Q(1),(N-1)/T);e=N*eps*T;gap=D+N*eps+e/(N-1+e)
    p=(N-1)/(N-1+e)
    maxcost=maxloss=0.
    for j in range(101):
        theta=Q(1,5)+Q(j,1000)
        # Recompute raw finite laws at off-grid parameters, with the same plan.
        for state in (0,1):
            cost=Q(1);surv=Q(0);loss=Q(0)
            for h in histories:
                w=math.prod((1-theta if yy==state else theta) for yy in h)
                if len(h)<T:cost+=w*x[ix[(h,'c')]]
                else:surv+=w*x[ix[(h,'c')]]
                loss+=w*x[ix[(h,'s'+str(1-state))]]
            completed=cost+surv
            mixedcost=p*completed+(1-p)
            mixedloss=p*(loss+state*surv)+(1-p)*state
            check(mixedcost<=N,'exact_off_grid_budget',str((T,j,state)))
            check(mixedloss<=pv+gap,'exact_off_grid_risk',str((T,j,state)))
            maxcost=max(maxcost,float(mixedcost));maxloss=max(maxloss,float(mixedloss))
    return {'horizon':T,'budget':str(N),'model_net':[str(t) for t in models],
       'certified_mesh_radius':str(eps),'exact_primal_value':str(pv),'exact_dual_value':str(dv),
       'gap_bound':str(gap),'mixture':str(p),'max_tested_cost':maxcost,'max_tested_loss':maxloss,
       'rational_primal':[str(t) for t in x],'rational_inequality_dual':[str(t) for t in y],
       'rational_equality_dual':[str(t) for t in z],
       'scope':'Primal/dual feasibility is exact for the finite model LP. Off-grid rational points are finite diagnostics; the continuum conclusion requires the manuscript lemma and analytic mesh-radius bound.'}

def quantum():
    rng=np.random.default_rng(63015);I=np.eye(2);U=np.array([[.6,-.8],[.8,.6]])
    ks=[np.diag([.6,.8]),np.diag([.8,.6])];rot=[U@k@U.T for k in ks]
    F0=np.diag([0.,1.]);F1=I-F0;audit=[F0,F1]
    rotated=[U@f@U.T for f in audit]
    def adj(theta,y,X):return (1-theta)*(ks[y]@X@ks[y])+theta*(rot[y]@X@rot[y])
    def evaluate(theta,T,rows):
        def node(h):
            # Output (call cost, continuing effect, terminal loss, call-count).
            if len(h)==T:return np.zeros((2,2)),I.copy(),np.zeros((2,2)),np.zeros((2,2))
            C=I+theta/5*F0;S=np.zeros((2,2));V=np.zeros((2,2));n=I.copy()
            for y in (0,1):
                prob=rows[h+(y,)];cc,ss,vv,nn=node(h+(y,))
                stoploss=sum((prob[r+1]*((1-theta)*audit[r]+theta*rotated[r]) for r in (0,1)),np.zeros((2,2)))
                C+=adj(theta,y,prob[0]*cc);S+=adj(theta,y,prob[0]*ss)
                V+=adj(theta,y,stoploss+prob[0]*vv);n+=adj(theta,y,prob[0]*nn)
            return C,S,V,n
        return node(())
    worst=-1.
    for T in [1,2,3,5,7]:
        rows={h:rng.dirichlet([1.,1.,1.]) for t in range(1,T+1) for h in itertools.product((0,1),repeat=t)}
        for phi,theta in [(0.,.01),(.3,.31),(.5,.54),(.99,1.),(.7,.2)]:
            C,S,V,n=evaluate(phi,T,rows);ct,st,vt,nt=evaluate(theta,T,rows)
            ei=abs(theta-phi);eg=ei/5;ef=ei;kap=1.2
            bounds=[(st-S,ei*n),(vt+st-V-S,ei*n+ef*I),
                    (ct+kap*st-C-kap*S,(eg+ei*(1.2*(T-1)+kap))*n)]
            for number,(diff,bound) in enumerate(bounds):
                for sign in (-1,1):
                    least=float(np.linalg.eigvalsh(bound+sign*diff)[0]);worst=max(worst,-least)
                    check(least>=-2e-12,'float_noncommuting_occupation_operator_bound',(T,phi,theta,number,sign,least))
            # Independent forward accumulation, including decision-dependent loss and costs.
            front={():I/2};fc=fs=fv=fn=0.
            for t in range(T):
                nxt={}
                for h,rho in front.items():
                    fc+=float(np.trace((I+phi/5*F0)@rho));fn+=float(np.trace(rho))
                    for y in (0,1):
                        post=(1-phi)*(ks[y]@rho@ks[y])+phi*(rot[y]@rho@rot[y]);p=rows[h+(y,)]
                        fv+=sum(float(p[r+1]*np.trace(((1-phi)*audit[r]+phi*rotated[r])@post)) for r in (0,1))
                        nxt[h+(y,)]=p[0]*post
                front=nxt
            fs=sum(float(np.trace(r)) for r in front.values())
            for expected,raw in zip([np.trace(X)/2 for X in (C,S,V,n)],[fc,fs,fv,fn]):
                check(abs(float(expected)-raw)<2e-12,'float_forward_backward_raw_parity',(T,phi))
    DETAILS['maximum_operator_bound_violation']=worst
    check(np.linalg.norm(ks[0]@rot[0]-rot[0]@ks[0])>.005,'float_noncommuting_instruments','not scalar or common-basis example')

if __name__=='__main__':
    exact_boundaries()
    DETAILS['exact_model_net_certificates']=[solve_and_certify(T,Q(3,2),[Q(1,5),Q(1,4),Q(3,10)]) for T in range(1,5)]
    quantum()
    print(json.dumps({'schema':'theta.r63.finite-diagnostics.v1','status':'PASS','checks_by_group':COUNTS,
        'total_checks':sum(COUNTS.values()),'numpy':np.__version__,'scipy':scipy.__version__,'seed':63015,
        'details':DETAILS,'limitations':'Finite exact rational primal/dual and boundary certificates, finite off-grid checks, and floating raw quantum operator checks. Not formal proof, continuum sampling proof, independent human review or editorial acceptance.'},sort_keys=True,indent=2))
