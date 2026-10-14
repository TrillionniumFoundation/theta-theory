#!/usr/bin/env python3
"""Finite algebraic diagnostics, not a proof of a collision-uniform LLT."""
from fractions import Fraction as F
import itertools, json, math
import numpy as np


def need(ok, msg):
    if not ok:
        raise RuntimeError(msg)


def denom(tau, c, R):
    M = np.array([[1., tau[0]], [0., 1.]])
    for j in range(1, len(tau)):
        kappa = 2./(R*c[j])
        M = np.array([[1.+tau[j]*kappa, tau[j]], [kappa, 1.]]) @ M
    return M[0,1]


def reduced(tau, c, R):
    m=len(tau); c=np.asarray(c,dtype=float)
    L=np.zeros((m+1,m+1))
    for i,t in enumerate(tau):
        v=np.zeros(m+1); v[i]=v[i+1]=1.
        L+=np.outer(v,v)/t
    E=[0,m]; CE=np.diag(c[E]); LEE=L[np.ix_(E,E)]
    G=R*CE+R*R*CE@LEE@CE
    if m>1:
        I=list(range(1,m)); sq=np.diag(np.sqrt(c[I]))
        Z=2*np.eye(m-1)+R*sq@L[np.ix_(I,I)]@sq
        T=CE@L[np.ix_(E,I)]@sq
        G-=R**3*T@np.linalg.solve(Z,T.T)
    return G


def rational_denom(tau, c, R):
    # Exact multiplication of the second column of the optical product.
    b,d=tau[0],F(1)
    for j in range(1,len(tau)):
        k=2/(R*c[j]); b,d=(1+tau[j]*k)*b+tau[j]*d,k*b+d
    return b


def continuant(tau,c,R):
    dm2,dm1=F(1),F(1)
    for j in range(1,len(tau)):
        a=2/(R*c[j])+1/tau[j-1]+1/tau[j]
        dn=a*dm1 if j==1 else a*dm1-dm2/tau[j-1]**2
        dm2,dm1=dm1,dn
    return math.prod(tau)*dm1


def checks():
    count=0; R=F(47,100); tm=F(3,50); q=F(47,59)
    need(2*F(53,100)/(1+F(53,100)**2)+F(1,200)<F(9,10),'section cap')
    need(R+2*R*R/tm==F(47,6),'upper Hessian constant')
    need(F(3)-F(1,32)==F(95,32),'epsilon exponent')
    need((F(3)-F(1,32))/12==F(95,384),'B exponent')
    for m in range(1,5):
        for taus in itertools.product([tm,F(1,5)],repeat=m):
            for inside in itertools.product([F(1,20),F(1,2),F(1)],repeat=m-1):
                cs=(F(1),)+inside+(F(1),)
                b=rational_denom(taus,cs,R)
                need(b==continuant(taus,cs,R),'continuant identity')
                need(b>=tm/q**(m-1),'uniform optical expansion')
                omega=R/b
                for j in range(1,m):
                    need(omega/cs[j]<=R*R/(2*tm*tm)*q**(m-2),'marked incidence bound')
                count+=1
    rng=np.random.default_rng(109)
    floating=0; max_error=0.
    for m in range(1,10):
        for _ in range(50):
            radius=rng.uniform(.45,.47)
            taus=rng.uniform(.06,1.5,size=m)
            cs=rng.uniform(.03,1.,size=m+1)
            cs[0]=rng.uniform(math.sqrt(19)/10,1)
            cs[-1]=rng.uniform(math.sqrt(19)/10,1)
            G=reduced(taus,cs,radius)
            w1=abs(G[0,1])/radius
            w2=radius*cs[0]*cs[-1]/denom(taus,cs,radius)
            err=abs(w1-w2)/max(w2,1e-300)
            max_error=max(max_error,err)
            need(err<1e-8,'Schur complement / optical product disagreement')
            need(np.linalg.eigvalsh(G-radius*np.diag([cs[0],cs[-1]])).min()>-1e-10,'Hessian lower bound')
            need(np.linalg.eigvalsh(G).max()<=float(F(47,6))+1e-10,'Hessian upper bound')
            if m>1:
                for j in range(1,m):
                    edge=cs.copy(); edge[j]=0.
                    G0=reduced(taus,edge,radius)
                    need(abs(G0[0,1])<1e-14,'visited grazing must disconnect mixed Hessian')
                    need(np.linalg.eigvalsh(G0).min()>=9*math.sqrt(19)/200-1e-10,'grazing Schur limit')
                    near=cs.copy(); near[j]=1e-9
                    need(np.linalg.norm(reduced(taus,near,radius)-G0)<1e-6,'continuous grazing extension')
            floating+=1
    # A zero unvisited clearance changes the guard, not the optical product.
    taus=[.2,.3]; cs=[.8,.7,.9]; radius=.46
    positive=radius*cs[0]*cs[-1]/denom(taus,cs,radius)
    need(positive>0,'unvisited-clearance diagnostic needs positive optical weight')
    zero_visited=cs.copy(); zero_visited[1]=0.
    need(abs(reduced(taus,zero_visited,radius)[0,1])<1e-14,'visited-grazing diagnostic')
    residual=0
    for u,a,b,k in itertools.product(range(8),range(8),range(8),[1,2,4]):
        full=max(u-k*(a+b),0); ng=max(u-k*a,0)
        need(0<=ng-full<=k*b,'positive-part residual comparison')
        residual+=1
    return {'exact_rational_optical_cases':count,'floating_Schur_cases':floating,
            'maximum_relative_optical_identity_error':max_error,
            'residual_comparison_cases':residual,
            'visited_vs_unvisited_grazing_distinguished':True,
            'full_raw_LLT_certified_by_tests':False,
            'scope':'matrix identities, finite inequalities, endpoint-limit diagnostics; not physical coverage or uniform residual decay'}

if __name__=='__main__':
    print(json.dumps(checks(),sort_keys=True,indent=2))
