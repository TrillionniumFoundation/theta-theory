#!/usr/bin/env python3
"""Finite controls for A2 v59; not proofs of the infinite-dimensional theorems.
No manuscript checker is imported. Requires NumPy and SciPy.
Run with normal Python or python -O; checks do not use removable assert statements.
"""
from fractions import Fraction as F
import json, math
import numpy as np
from scipy.optimize import root

def require(ok,message):
    if not ok: raise RuntimeError(message)

def tail_and_green():
    tails=[]
    for rho in [F(1,3),F(3,5),F(4,5),F(9,10)]:
        W=F(3,2);astar=F(1,2);m=4
        while 2*W/astar*rho**m/(1-rho**m)>=F(1,2): m+=1
        q=2*W/astar*rho**m/(1-rho**m)
        require(q<F(1,2),'Tail choice failed')
        prev=None
        for n in range(m,m+40):
            majorant=2*W*rho**n/((1-rho)*(1-rho**n))
            if prev is not None: require(majorant<prev,'Nondecreasing compactness majorant')
            prev=majorant
        tails.append({'rho':str(rho),'chosen_m':m,'q_m':str(q),'tail_inverse_bound':str(1/astar/(1-q))})
    rows=0
    for t,beta in [(F(1,4),F(1,2)),(F(1,2),F(3,4)),(F(4,5),F(9,10))]:
        bound=1/(1-t/beta)+t*beta/(1-t*beta)
        for i in range(1,61):
            val=sum(t**abs(i-k)*beta**(k-i) for k in range(1,81))
            require(val<=bound,'Weighted Green row bound failed');rows+=1
    return {'tail_parameters':tails,'exact_weighted_green_rows':rows}

def finite_stationary_envelope():
    records=[];worst=0.;negative_controls=0
    for g,kappas in [(1.1,(.6,1.7)),(.8,(2.,.8))]:
        for b in [0,1]:
            for N in [5,12]:
                for u in [-.08,-.05,.05,.08]:
                    for m in [3,4]:
                        typ=(b+np.arange(N+1))%2
                        kap=np.array(kappas)[typ]
                        cubic=np.array([.18,-.27])[typ]
                        quartic=np.array([.4,.25])[typ]
                        v=np.array([1.,.35])[typ]
                        def flight(x,s):
                            psi=kap*x*x/2+cubic*x**3/6+quartic*x**4/24+s*v*x**m
                            dp=kap*x+cubic*x*x/2+quartic*x**3/6+s*v*m*x**(m-1)
                            dpsi=psi[:-1]+psi[1:];h=g+dpsi;dx=np.diff(x)
                            lengths=np.sqrt(h*h+dx*dx)
                            return dpsi,h,dx,lengths,dp
                        def solve(s):
                            def grad(z):
                                x=np.r_[u,z,0.];dpsi,h,dx,l,dp=flight(x,s)
                                return (h[:-1]*dp[1:-1]+dx[:-1])/l[:-1]+(h[1:]*dp[1:-1]-dx[1:])/l[1:]
                            ans=root(grad,u*.5**np.arange(1,N),tol=1e-11)
                            require(np.max(np.abs(grad(ans.x)))<2e-12,'Stationarity residual')
                            x=np.r_[u,ans.x,0.];dpsi,h,dx,l,dp=flight(x,s)
                            # Stable evaluation of sum(length - g).
                            action=np.sum((dpsi*(2*g+dpsi)+dx*dx)/(l+g))
                            return x,action,h/l
                        x,a,w=solve(0.)
                        eta=v*x**m
                        envelope=float(np.sum(w*(eta[:-1]+eta[1:])))
                        step=2e-4
                        difference=(solve(step)[1]-solve(-step)[1])/(2*step)
                        error=abs(difference-envelope)/max(abs(envelope),1e-14)
                        require(error<3e-6,'Finite stationary-envelope discrepancy')
                        wrong=envelope+w[0]*eta[0] # Deliberately double initial contact.
                        require(abs(wrong-difference)>max(1e-8,abs(envelope)*.1),'Negative control not separated')
                        negative_controls+=1;worst=max(worst,error)
                        records.append({'g':g,'kappa':list(kappas),'start_type':b,'flights':N,'endpoint':u,'variation_degree':m,'envelope':envelope,'finite_difference':difference,'relative_error':error})
    return {'configurations':len(records),'worst_relative_error':worst,'doubled_initial_visit_negative_controls':negative_controls,'records':records}

def topology_control():
    # h_N(z)=(z/R)^N, R=1. Analytic norm=1, while each fixed derivative on |x|<=1/2 vanishes.
    data=[]
    for N in [8,16,32,64,128]:
        k=3;bound=max(math.prod(range(N-j+1,N+1))*.5**(N-j) for j in range(k+1))
        data.append({'degree':N,'H_infinity_norm':1,'C3_inner_interval_bound':bound})
    require(data[-1]['C3_inner_interval_bound']<1e-25,'Topology control failed')
    return data

if __name__=='__main__':
    result={'scope':'Exact finite scalar bounds, finite local stationary chains, and a topology illustration only. No global periodic realization, complex Banach inverse, trace-class limit, or statistical theorem is certified.','imports_author_checker':False,'tail_and_green':tail_and_green(),'stationary_envelope':finite_stationary_envelope(),'analytic_vs_real_topology':topology_control()}
    print(json.dumps(result,indent=2,sort_keys=True))
