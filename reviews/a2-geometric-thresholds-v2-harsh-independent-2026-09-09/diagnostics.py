#!/usr/bin/env python3
"""Independent finite diagnostics for A2 geometric thresholds v2.
No repository modules, network, asserts, interval arithmetic or formal proof.
Run: python diagnostics.py > diagnostics_output.json
Deps: numpy, scipy, sympy. Deterministic JSON; nonzero exit on failure.
"""
from __future__ import annotations
import json
import math
import sys
from fractions import Fraction as Q
from collections import Counter
import numpy as np
import sympy as sp
from scipy.linalg import solve_banded, eigvalsh
from scipy.optimize import brentq

checks: list[dict] = []
metrics: dict = {}

def check(name: str, ok: bool, kind: str, detail=None) -> None:
    row = {'name': name, 'passed': bool(ok), 'kind': kind}
    if detail is not None: row['detail'] = detail
    checks.append(row)

def cheb(c: Q, n: int, second: bool=False) -> Q:
    if n == 0: return Q(1)
    a,b=Q(1),2*c if second else c
    for _ in range(1,n): a,b=b,2*c*b-a
    return b

def schur(g: Q, c0: Q, c1: Q, j: int):
    cs=[c0 if i%2==0 else c1 for i in range(j+1)]
    if j==1: return cs[0]/g, -1/g, cs[-1]/g
    a=cs[0]/g; b=-1/g; p=2*cs[1]/g
    for k in range(1,j):
        a-=b*b/p
        edge=-1/g
        last=(cs[j]/g if k==j-1 else 2*cs[k+1]/g)-edge*edge/p
        b=-b*edge/p
        p=last
    return a,b,p

def exact_alternating():
    # Products are rational squares; individual curvatures are unequal.
    cases=[(Q(1,5),Q(6,5),Q(15,8),Q(3,2)),
           (Q(3,20),Q(5,4),Q(9,5),Q(3,2)),
           (Q(1,8),Q(4,3),Q(3),Q(2))]
    for ci,(g,c0,c1,c) in enumerate(cases):
        for j in [1,2,3,4,5,8,9,16,17,32,33,64,65,128]:
            a,b,d=schur(g,c0,c1,j)
            U=cheb(c,j-1,True); T=cheb(c,j)
            sig0sq=c1; sigjsq=c1 if j%2==0 else c0
            sigprod=c1 if j%2==0 else c
            expected=(c*T/(g*sig0sq*U), -c/(g*sigprod*U),c*T/(g*sigjsq*U))
            check(f'schur-{ci}-{j}', (a,b,d)==expected, 'exact_rational')
            det=a*d-b*b
            check(f'determinant-{ci}-{j}', det==c*c*(c*c-1)/(g*g*sig0sq*sigjsq), 'exact_rational')
            check(f'relative-twist-{ci}-{j}', b*b/det==1/((c*c-1)*U*U), 'exact_rational')
        A0=sp.Matrix([[2*sp.Rational(c0),-1],[1,0]])
        A1=sp.Matrix([[2*sp.Rational(c1),-1],[1,0]])
        P=A1*A0
        check(f'monodromy-{ci}',P.det()==1 and P.trace()==4*sp.Rational(c0*c1)-2,'exact_symbolic')

def support_and_inverse():
    t,R,al,be,ze=sp.symbols('t R alpha beta zeta',real=True)
    h=R+(1-sp.cos(6*t))*(al+be*sp.cos(2*t)+ze*sp.sin(2*t))
    hp=sp.diff(h,t); hpp=sp.diff(h,t,2)
    vals=[]
    for r in range(3):
        th=sp.pi*r/3
        b=al+be*sp.cos(2*th)+ze*sp.sin(2*th)
        vals.append(b)
        check(f'support-jets-{r}',sp.simplify(h.subs(t,th)-R)==0 and sp.simplify(hp.subs(t,th))==0 and sp.simplify((h+hpp).subs(t,th)-R-36*b)==0,'exact_symbolic')
    J=sp.Matrix(vals).jacobian([al,be,ze])
    check('three-contact-rank',J.det()!=0,'exact_symbolic')
    # Fourier orthogonality: area/pi = mean(h)^2 + 1/2 sum (1-n^2)(a_n^2+b_n^2).
    modes={2:(be,ze),4:(-be/2,ze/2),6:(-al,0),8:(-be/2,-ze/2)}
    area=(R+al)**2+sum(sp.Rational(1,2)*(1-n*n)*(a*a+b*b) for n,(a,b) in modes.items())
    wanted=R**2+2*R*al-sp.Rational(33,2)*al**2-sp.Rational(45,4)*(be**2+ze**2)
    check('area-fourier-identity',sp.expand(area-wanted)==0,'exact_symbolic')
    check('area-unordered-curvatures',sp.simplify(sum(vals)/3-al)==0 and sp.simplify(sp.Rational(2,3)*sum((v-al)**2 for v in vals)-be**2-ze**2)==0,'exact_symbolic')
    # Direct symbolic algebra for the information bottleneck (not a physical counterexample).
    u,v,w=sp.symbols('u v w',positive=True)
    check('unequal-curvature-product-invariance',sp.simplify((u*w)*(v/w)-u*v)==0,'exact_symbolic')
    nodes=[Q(1,3),Q(1,4),Q(1,5)]; area0=Q(2,7)
    for j in range(1,9):
        C=lambda n:sum(2*x**n/(area0*(1-x**(2*n))) for x in nodes)
        cutoff=31
        F=sum(int(sp.mobius(k))*C(k*j) for k in range(1,cutoff+1,2))
        true=sum(2*x**j/area0 for x in nodes)
        nextk=cutoff+2
        bound=sum(2*x**(nextk*j)/(area0*(1-x**(2*j))**2) for x in nodes)
        check(f'mobius-tail-{j}',abs(F-true)<=bound,'exact_rational')
    for case,xs in enumerate([[.25,.30,.4],[.25,.25,.4],[.30,.30,.30]]):
        unique, mult=np.unique(xs,return_counts=True); d=len(unique)
        weights=2*mult/float(area0)
        F=lambda j:np.dot(weights,unique**j)
        H0=np.array([[F(p+q+1) for q in range(d)] for p in range(d)])
        H1=np.array([[F(p+q+2) for q in range(d)] for p in range(d)])
        rec=eigvalsh(H1,H0)
        V=np.array([rec**j for j in range(1,d+1)])
        wr=np.linalg.solve(V,np.array([F(j) for j in range(1,d+1)]))
        ar=6/wr.sum()
        check(f'hankel-recovery-{case}',np.max(abs(rec-unique))<1e-8 and abs(ar-float(area0))<1e-8 and np.max(abs(ar*wr/2-mult))<1e-7,'noninterval_numeric')
    # Exact coalescence sensitivity in the symmetric pair perturbation.
    x,hv=sp.symbols('x h')
    for j in range(1,9):
        delta=sp.expand((x+hv)**j+(x-hv)**j-2*x**j)
        check(f'coalescence-no-linear-term-{j}',sp.diff(delta,hv).subs(hv,0)==0,'exact_symbolic')
    metrics['area_divided_by_pi']='R^2+2R*alpha-(33/2)*alpha^2-(45/4)*(beta^2+zeta^2)'

# Exact local graph lengths, with unequal curvatures and non-even boundary jets.
gap=.12
kap=np.array([2.1,2.5]); cubic=np.array([.8,-.5]); quartic=np.array([40.,30.])

def length_jets(y):
    idx=np.arange(len(y))%2
    p=kap[idx]*y*y/2+cubic[idx]*y**3/6+quartic[idx]*y**4/24
    p1=kap[idx]*y+cubic[idx]*y*y/2+quartic[idx]*y**3/6
    p2=kap[idx]+cubic[idx]*y+quartic[idx]*y*y/2
    H=gap+p[:-1]+p[1:]; delta=np.diff(y); L=np.hypot(H,delta)
    a=H*p1[:-1]-delta; b=H*p1[1:]+delta
    du=a/L; dv=b/L
    uu=(p1[:-1]**2+H*p2[:-1]+1)/L-a*a/L**3
    vv=(p1[1:]**2+H*p2[1:]+1)/L-b*b/L**3
    uv=(p1[:-1]*p1[1:]-1)/L-a*b/L**3
    # Rationalized excess avoids subtracting j*gap from total action.
    excess=(2*gap*(p[:-1]+p[1:])+(p[:-1]+p[1:])**2+delta**2)/(L+gap)
    return excess,du,dv,uu,vv,uv

def pivots(diag,off):
    out=np.array(diag,copy=True)
    for i in range(1,len(out)): out[i]-=off[i-1]**2/out[i-1]
    return out

def bridge(j,u,v):
    cs=1+gap*kap; c=math.sqrt(cs.prod()); gamma=math.acosh(c)
    sig=np.sqrt(cs[1-np.arange(j+1)%2]); i=np.arange(j+1)
    sinhquot=lambda k:np.exp(-gamma*(j-k))*(-np.expm1(-2*gamma*k))/(-np.expm1(-2*gamma*j))
    y=sig*(sinhquot(j-i)*u/sig[0]+sinhquot(i)*v/sig[-1])
    y[0]=u; y[-1]=v
    residual=0.
    for _ in range(12):
        E,du,dv,uu,vv,uv=length_jets(y)
        if j==1: break
        grad=dv[:-1]+du[1:]; residual=float(np.max(abs(grad)))
        if residual<3e-16: break
        diag=vv[:-1]+uu[1:]; off=uv[1:-1]
        band=np.zeros((3,j-1)); band[1]=diag
        if j>2: band[0,1:]=off; band[2,:-1]=off
        y[1:-1]-=solve_banded((1,1),band,grad)
    E,du,dv,uu,vv,uv=length_jets(y)
    if j>1:
        residual=float(np.max(abs(dv[:-1]+du[1:])))
        pp=pivots(vv[:-1]+uu[1:],uv[1:-1])
        zero=length_jets(np.zeros(j+1))
        p0=pivots(zero[4][:-1]+zero[3][1:],zero[5][1:-1])
        logb=float(np.log(-uv*gap).sum()-np.log(pp/p0).sum())
    else: logb=math.log(-uv[0]*gap)
    factor=c*math.sinh(gamma)/gap
    D=np.diag(1/np.array([sig[0],sig[-1]]))
    S=1/math.sinh(j*gamma)
    H=factor*D@np.array([[1/math.tanh(j*gamma),-S],[-S,1/math.tanh(j*gamma)]])@D
    return y,float(E.sum()),logb,residual,H

def nonlinear_checks():
    rows=[]
    for j in [1,2,3,8,16,32,64,128,256]:
        for eps in [.003,.0015]:
            u,v=eps,-.7*eps
            y,E,lb,res,H=bridge(j,u,v)
            check(f'nonlinear-reflection-{j}-{eps}',res<1e-12,'noninterval_numeric')
            check(f'nonlinear-positive-twist-{j}-{eps}',np.all(-length_jets(y)[5]>0) and math.isfinite(lb),'noninterval_numeric')
            # Cubic boundary contribution on linear stationary bridge.
            cs=1+gap*kap; ga=math.acosh(math.sqrt(cs.prod()))
            sig=np.sqrt(cs[1-np.arange(j+1)%2]); i=np.arange(j+1)
            sq=lambda k:np.exp(-ga*(j-k))*(-np.expm1(-2*ga*k))/(-np.expm1(-2*ga*j))
            yl=sig*(sq(j-i)*u/sig[0]+sq(i)*v/sig[-1])
            cube=cubic[np.arange(j+1)%2]*yl**3/6
            cubic_action=float(cube[0]+cube[-1]+2*cube[1:-1].sum())
            quad=float(np.array([u,v])@H@np.array([u,v])/2)
            rows.append({'j':j,'endpoint_scale':eps,'relative_twist':math.exp(lb),'reflection_residual':res,'quartic_remainder_scaled':(E-quad-cubic_action)/eps**4})
    metrics['nonlinear_bridges']=rows
    # Radial endpoint quadrature; not the author's exact Morse coordinates.
    nr,nt=10,24
    radii,weights=np.polynomial.legendre.leggauss(nr)
    out=[]
    for j in [1,2,5,16]:
        _,_,_,_,H=bridge(j,0.,0.)
        ev,V=np.linalg.eigh(H); invsqrt=(V/np.sqrt(ev))@V.T
        for d in [1e-4,1e-5]:
            integral=0.
            for theta in np.arange(nt)*2*math.pi/nt:
                direction=math.sqrt(2*d)*(invsqrt@np.array([math.cos(theta),math.sin(theta)]))
                def value(r): return bridge(j,*(r*direction))
                top=brentq(lambda r:value(r)[1]-d,.5,1.5,xtol=2e-14)
                for z,w in zip(radii,weights):
                    r=(z+1)*top/2
                    _,E,lb,_,_=value(r)
                    integral+=w*top/2*(1-E/d)*math.exp(lb)*r*2*math.pi/nt
            ratio=2/math.pi*integral
            check(f'onset-quadrature-{j}-{d}',abs(ratio-1)<100*d,'noninterval_numeric',{'ratio':ratio,'tolerance':100*d})
            out.append({'j':j,'offset':d,'probability_over_theoretical_leading_term':ratio})
    metrics['onset_quadrature']=out

def source_and_cut():
    a,b=Q(7,5),Q(-2,3)
    for j in range(1,41):
        w=sum(a if i%2==0 else b for i in range(j+1))
        rhs=(j+1)*(a+b)/2+((a-b)/2 if j%2==0 else 0)
        check(f'axial-parity-{j}',w==rhs,'exact_rational')
    # u=|z|^2 in a fixed disk u<1/4, eta upper=1-u, cut psi=1/2+xi/10-u/3.
    xi,u,eta=sp.symbols('xi u eta',real=True)
    psi=sp.Rational(1,2)+xi/10-u/3; top=1-u; F=1+xi*eta
    I=sp.integrate(sp.integrate(F,(eta,psi,top)),(u,0,sp.Rational(1,4)))
    formula=sp.integrate(sp.integrate(sp.diff(F,xi),(eta,psi,top))-F.subs(eta,psi)*sp.diff(psi,xi),(u,0,sp.Rational(1,4)))
    check('moving-cut-leibniz',sp.simplify(sp.diff(I,xi)-formula)==0,'exact_symbolic')
    missing=sp.integrate(F.subs(eta,psi)*sp.diff(psi,xi),(u,0,sp.Rational(1,4))).subs(xi,0)
    check('moving-cut-nonzero-boundary',missing==Q(1,40),'exact_symbolic')
    metrics['moving_cut_boundary_at_zero_without_angular_factor']=str(missing)

def main():
    exact_alternating(); support_and_inverse(); nonlinear_checks(); source_and_cut()
    payload={'scope':'Independent finite algebraic/local-mechanical corroboration, not an arbitrary-j proof or full-equilibrium simulation.',
             'source_commit':'daeea828a7666acc42adcabdb9ab9057e9e1bac7',
             'total':len(checks),'passed':sum(x['passed'] for x in checks),'categories':dict(Counter(x['kind'] for x in checks)),
             'checks':checks,'metrics':metrics}
    print(json.dumps(payload,indent=2,sort_keys=True,allow_nan=False))
    return 0 if all(x['passed'] for x in checks) else 1

if __name__=='__main__': sys.exit(main())
