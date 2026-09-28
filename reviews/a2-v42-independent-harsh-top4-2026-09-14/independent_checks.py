#!/usr/bin/env python3
"""Independent finite diagnostics for A2 v42; not a proof or native build.
Run: python independent_checks.py --output RESULTS.json
The implementation is independent of the manuscript's code and has no network I/O.
"""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
import math
import platform
from fractions import Fraction as F
from pathlib import Path
import numpy as np
import scipy
from scipy.integrate import quad
from scipy.linalg import solve_banded

SOURCE = '6b30aaacf7db2b5df3ae3771a5b2d1f0ba1b18ad'


def density_checks() -> dict:
    d = F(3, 2)
    def S(x): return x*x/F(2) + x**3/F(7) + x**4/F(11)
    def B(x): return 1 + x/F(5) + x*x/F(9)
    def f(x,y): return B(x)*B(y)*(d-S(x)-S(y))/F(13,7)
    def R(x,y): return f(x,y)*f(F(0),F(0))/(f(x,F(0))*f(F(0),y))
    grid = [F(i,40) for i in range(-12,13)]
    pairs = 0
    for x,y in itertools.product(grid,repeat=2):
        assert 1-R(x,y) == S(x)*S(y)/((d-S(x))*(d-S(y)))
        pairs += 1
    recovered = 0
    for a in (F(-1,4), F(1,5), F(3,10)):
        q = S(a)/(d-S(a))
        assert q > 0 and q*q == 1-R(a,a)
        for x in grid:
            t = (1-R(x,a))/q
            assert d*t/(1+t) == S(x)
            assert f(x,F(0))/f(F(0),F(0))*(1+t) == B(x)
            recovered += 1
    assert S(F(1,5)) != S(F(-1,5))
    return {'exact_pair_identities':pairs, 'exact_action_amplitude_recoveries':recovered,
            'anchors':3, 'non_even_action':True, 'nonconstant_amplitude':True}


def prufer_edges(code: tuple[int,...], n: int) -> list[tuple[int,int]]:
    degree = [1]*n
    for x in code: degree[x] += 1
    edges=[]
    for x in code:
        leaf=next(i for i in range(n) if degree[i]==1)
        edges.append((leaf,x)); degree[leaf]-=1; degree[x]-=1
    left=[i for i in range(n) if degree[i]==1]
    if n>1: edges.append((left[0],left[1]))
    return edges


def parent_vertices(edges: list[tuple[int,int]], n: int, root: int) -> set[int]:
    adjacency=[[] for _ in range(n)]
    for a,b in edges: adjacency[a].append(b); adjacency[b].append(a)
    seen={root}; stack=[root]; parents=set()
    while stack:
        u=stack.pop()
        for v in adjacency[u]:
            if v not in seen:
                seen.add(v); stack.append(v); parents.add(u)
    assert len(seen)==n
    return parents


def reroot_checks() -> dict:
    trees=cases=0
    for n in range(1,7):
        codes = [()] if n<=2 else itertools.product(range(n),repeat=n-2)
        for code in codes:
            edges=[] if n==1 else prufer_edges(tuple(code),n)
            parents=[parent_vertices(edges,n,r) for r in range(n)]
            trees+=1
            for old in range(n):
                free=sorted(set(range(n))-parents[old])
                for mask in range(1<<len(free)):
                    rigid=parents[old] | {v for i,v in enumerate(free) if mask>>i&1}
                    for new in rigid:
                        assert parents[new] <= rigid
                        cases+=1
    edge=[(0,1),(1,2)]; rigid={0,1}
    assert parent_vertices(edge,3,0)<=rigid
    assert not parent_vertices(edge,3,2)<=rigid
    return {'labelled_trees_n1_through_n6':trees,'valid_reroot_cases':cases,
            'symmetric_leaf_negative_control_detected':True,
            'scope':'Combinatorial abstraction after analytic signature uniqueness; not the analytic lemma.'}


def green_checks() -> dict:
    worst=0.0
    for g,k0,k1 in ((.7,.4,1.9),(1.,1.,1.),(1.3,2.1,.35)):
        c=np.array([1+g*k0,1+g*k1]); cc=math.sqrt(float(np.prod(c)))
        gamma=math.acosh(cc)
        for b in (0,1):
            i=np.arange(1,81); types=(b+i)%2; sig=np.sqrt(c[1-types])
            G=g*np.outer(sig,sig)/(2*cc*math.sinh(gamma))*(
                np.exp(-gamma*np.abs(i[:,None]-i[None,:]))-
                np.exp(-gamma*(i[:,None]+i[None,:])))
            H=np.diag(2*c[types]/g)+np.diag(np.full(79,-1/g),1)+np.diag(np.full(79,-1/g),-1)
            # The last row has a deliberately omitted infinite tail; exclude it.
            error=float(np.max(np.abs((H@G-np.eye(80))[:-1,:])))
            worst=max(worst,error)
    assert worst<1e-12
    return {'configurations':6,'sites':80,'max_interior_recurrence_residual':worst}


def stationary_action(u: float,b: int,varied: int|None) -> tuple[float,float]:
    N=80; g=.9; kapp=np.array([.55,1.6]); cubic=np.array([.3,-.2]); quart=np.array([.4,.25])
    c=1+g*kapp; gamma=math.acosh(math.sqrt(float(np.prod(c))))
    i=np.arange(N+1); typ=(b+i)%2
    x=np.where(i%2==0,1.,math.sqrt(c[b]/c[1-b]))*np.exp(-gamma*i)*u
    x[-1]=0.
    fifth=np.where(typ==varied,.35,0.) if varied is not None else np.zeros(N+1)
    def evaluate(z):
        psi=kapp[typ]*z*z/2+cubic[typ]*z**3/6+quart[typ]*z**4/24+fifth*z**5/120
        dp=kapp[typ]*z+cubic[typ]*z*z/2+quart[typ]*z**3/6+fifth*z**4/24
        dd=kapp[typ]+cubic[typ]*z+quart[typ]*z*z/2+fifth*z**3/6
        h=g+psi[:-1]+psi[1:]; d=z[1:]-z[:-1]; ell=np.hypot(h,d)
        gy=(h*dp[:-1]-d)/ell; gz=(h*dp[1:]+d)/ell
        yy=(dp[:-1]**2+h*dd[:-1]+1-gy**2)/ell
        zz=(dp[1:]**2+h*dd[1:]+1-gz**2)/ell
        yz=(dp[:-1]*dp[1:]-1-gy*gz)/ell
        val=float(np.sum(((psi[:-1]+psi[1:])*(h+g)+d*d)/(ell+g)))
        grad=gz[:-1]+gy[1:]; diag=zz[:-1]+yy[1:]; off=yz[1:-1]
        return val,grad,diag,off
    for _ in range(30):
        val,grad,diag,off=evaluate(x)
        if np.max(np.abs(grad))<2e-15: break
        band=np.zeros((3,N-1));band[1]=diag;band[0,1:]=off;band[2,:-1]=off
        step=solve_banded((1,1),band,-grad)
        x[1:-1]+=step
    val,grad,_,_=evaluate(x); residual=float(np.max(np.abs(grad)))
    assert residual<2e-12
    return val,residual


def finite_remainder_checks() -> dict:
    g=.9;c=1+g*np.array([.55,1.6]); gamma=math.acosh(math.sqrt(float(np.prod(c))))
    rows=[]; max_res=0.; solves=0
    for b,r in itertools.product((0,1),repeat=2):
        coefficient=(1/math.tanh(5*gamma) if b==r else
                     (math.sqrt(c[b]/c[1-b])**5)/math.sinh(5*gamma))*.35/120
        for u in (.1,.05,.025):
            ratios=[]
            for sign in (1.,-1.):
                a,e=stationary_action(sign*u,b,None); v,ee=stationary_action(sign*u,b,r)
                ratios.append((v-a)/(sign*u)**5); max_res=max(max_res,e,ee); solves+=2
            average=sum(ratios)/2
            rows.append({'starting_type':b,'varied_type':r,'absolute_endpoint':u,
                         'predicted_fifth_order_coefficient':float(coefficient),
                         'signed_average_observed':average,'absolute_error':abs(average-coefficient)})
    finest=[x['absolute_error'] for x in rows if x['absolute_endpoint']==.025]
    assert max(finest)<2e-6
    return {'finite_stationary_solves':solves,'edges':80,'max_stationarity_residual':max_res,
            'max_finest_coefficient_error':max(finest),'rows':rows,
            'scope':'A fifth-degree perturbation preserving graph jets through degree four, not arbitrary flat remainders.'}


def poisson_checks() -> dict:
    R=3.; rows=[]
    for z in (-1.,0.,1.):
        for k in (100,400,1600):
            h=1-z/k
            target=2*(R-z)
            if z>=0:
                missing=(R*R-z*z)/k; common=target-missing; exterior=0.
            else:
                missing=R*R/k; common=target-missing; exterior=z*z/(k*h*h)
            l1=abs(1/h**2-1)*common+missing+exterior
            actual=(2*(R-z)-(R*R-z*z)/k)/h**2
            integral=quad(lambda y: 2*(1-y/k)/h**2,z,R,epsabs=1e-12)[0]
            assert abs(actual-integral)<1e-11
            assert k*l1<30
            a=1-R/k; beta=.25
            def integrand(x):
                t=beta*z*x/k
                root_delta=t/(math.sqrt(1+t)+1)
                return root_delta**2*8/(3*math.pi*a*a)*(a-x*x)**1.5
            H2=quad(integrand,-math.sqrt(a),math.sqrt(a),epsabs=1e-18)[0]
            expected=beta*beta*z*z*a/24
            assert abs(k*k*H2-expected)<1e-8
            rows.append({'z':z,'k':k,'layer_intensity_L1':l1,'k_times_L1':k*l1,
                         'scaled_layer_mass':actual,'bulk_H2':H2,'k2_bulk_H2':k*k*H2})
    neg=[]
    for k in (10**4,10**6,10**8):
        amp=.5*k**(-.25)
        def bad_integrand(x):
            t=amp*x; delta=t/(math.sqrt(1+t)+1)
            return delta*delta*8/(3*math.pi)*(1-x*x)**1.5
        h2=quad(bad_integrand,-1,1,epsabs=1e-18)[0]
        product=-2*math.expm1(k*math.log1p(-h2/2))
        neg.append({'k':k,'trace_tilt':amp,'product_H2':product})
    assert neg[-1]['product_H2']>1.9
    return {'rows':rows,'trace_only_negative_control':neg,
            'scope':'Exactly normalized parabolic-ceiling model; negative control deliberately violates the manuscript bulk bound.'}


def main() -> None:
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=Path('RESULTS.json'))
    args=parser.parse_args()
    result={'reviewed_source_commit':SOURCE,'status':'passed',
            'environment':{'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__},
            'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'density':density_checks(),'rerooting':reroot_checks(),'green':green_checks(),
            'finite_smooth_remainder':finite_remainder_checks(),'poisson_layer_bulk':poisson_checks(),
            'native_manuscript_compiled':False,'PDF_visually_inspected':False,
            'warning':'Finite independent diagnostics do not prove the infinite theorems or certify the full submission.'}
    args.output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('finite_smooth_remainder','poisson_layer_bulk')},indent=2))
    print('remainder max finest error:',result['finite_smooth_remainder']['max_finest_coefficient_error'])
    print('maximum stationarity residual:',result['finite_smooth_remainder']['max_stationarity_residual'])
    print('wrote',args.output)

if __name__=='__main__': main()
