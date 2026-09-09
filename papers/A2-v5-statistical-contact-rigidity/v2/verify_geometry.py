#!/usr/bin/env python3
"""Exact algebra and finite non-interval diagnostics for geometric thresholds.

The analytic arbitrary-length and full-event proofs are in the manuscript.
Tests of polynomial facing arcs are not a simulation of full equilibrium.
Run with ordinary Python and python -O; failures use explicit exceptions.
Dependencies: numpy, scipy, sympy.
"""
from __future__ import annotations
from fractions import Fraction as Q
import json
import math
import platform
import numpy as np
import sympy as sp
from scipy.linalg import solve_banded, eigh
from scipy.optimize import brentq
from numpy.polynomial.legendre import leggauss

COUNTS = {}

def check(ok, name, group):
    if not bool(ok):
        raise RuntimeError(name)
    COUNTS[group] = COUNTS.get(group, 0) + 1


def cheb(c, j):
    t0,t1,u0,u1=Q(1),c,Q(0),Q(1)
    for _ in range(1,j):
        t0,t1=t1,2*c*t1-t0
        u0,u1=u1,2*c*u1-u0
    return t1,u1


def exact_schur(g, c0, c1, j):
    cs=[c0 if i%2==0 else c1 for i in range(j+1)]
    a=cs[0]/g; edge=-1/g; det=Q(1)
    if j==1: return ((a,edge),(edge,cs[1]/g)),det
    pivot=2*cs[1]/g
    for i in range(1,j):
        det*=pivot
        a-=edge*edge/pivot
        newedge=edge/(g*pivot)
        nxt=(cs[i+1] if i+1==j else 2*cs[i+1])/g-1/(g*g*pivot)
        edge,pivot=newedge,nxt
    return ((a,edge),(edge,pivot)),det


def arcs(y, coeff):
    k,b,d=coeff
    return (.5*k*y*y+b*y**3/6+d*y**4/24,
            k*y+b*y*y/2+d*y**3/6,
            k+b*y+d*y*y/2)


def length_jet(u,v,g,coef0,coef1):
    p,pu,puu=arcs(u,coef0); q,qv,qvv=arcs(v,coef1)
    x=g+p+q; y=v-u; length=np.hypot(x,y)
    du=x*pu-y; dv=x*qv+y
    gu=du/length; gv=dv/length
    hu=(pu*pu+1+x*puu)/length-du*du/length**3
    hv=(qv*qv+1+x*qvv)/length-dv*dv/length**3
    hcross=(pu*qv-1)/length-du*dv/length**3
    excess=(2*g*(p+q)+(p+q)**2+y*y)/(length+g)
    return excess,gu,gv,hu,hv,hcross


def bridge(g, coeff0, coeff1, j, u, v):
    c0=1+g*coeff0[0];c1=1+g*coeff1[0];c=math.sqrt(c0*c1)
    gamma=math.acosh(c);i=np.arange(j+1)
    sig=np.sqrt(np.where(i%2==0,c1,c0))
    ratios=lambda n:np.exp(-gamma*(j-n))*(-np.expm1(-2*gamma*n))/(-math.expm1(-2*gamma*j))
    y=sig*(ratios(j-i)*u/sig[0]+ratios(i)*v/sig[-1])
    left=np.array([coeff0 if k%2==0 else coeff1 for k in range(j)])
    right=np.array([coeff1 if k%2==0 else coeff0 for k in range(j)])
    for iteration in range(12):
        vals=length_jet(y[:-1],y[1:],g,left.T,right.T)
        en,gu,gv,hu,hv,cross=vals
        grad=gv[:-1]+gu[1:]
        if not len(grad) or np.max(np.abs(grad))<2e-15: break
        diag=hv[:-1]+hu[1:]
        band=np.zeros((3,j-1));band[1]=diag
        if j>2:band[0,1:]=cross[1:-1];band[2,:-1]=cross[1:-1]
        y[1:-1]-=solve_banded((1,1),band,grad)
    vals=length_jet(y[:-1],y[1:],g,left.T,right.T)
    en,gu,gv,hu,hv,cross=vals
    diag=hv[:-1]+hu[1:]
    logdet=0.0
    if j>1:
        pivot=diag[0];logdet=math.log(pivot)
        for k in range(1,j-1):
            pivot=diag[k]-cross[k]**2/pivot
            if pivot<=0:raise RuntimeError('Nonpositive interior pivot')
            logdet+=math.log(pivot)
    logtwist=float(np.log(-cross).sum()-logdet)
    logsinh=j*gamma+math.log1p(-math.exp(-2*j*gamma))-math.log(2)
    logtwist0=math.log(c*math.sinh(gamma)/(g*sig[0]*sig[-1]))-logsinh
    zfac=c*math.sinh(gamma)/g
    coth=1+2*math.exp(-2*j*gamma)/(-math.expm1(-2*j*gamma))
    csch=2*math.exp(-j*gamma)/(-math.expm1(-2*j*gamma))
    H=np.array([[zfac*coth/sig[0]**2,-zfac*csch/(sig[0]*sig[-1])],
                [-zfac*csch/(sig[0]*sig[-1]),zfac*coth/sig[-1]**2]])
    coords=np.array([[-arcs(t,coeff0)[0],t] if k%2==0 else
                     [g+arcs(t,coeff1)[0],t] for k,t in enumerate(y)])
    rays=np.diff(coords,axis=0);rays/=np.linalg.norm(rays,axis=1)[:,None]
    residual=0.0
    for k in range(1,j):
        n=np.array([1.0,arcs(y[k],coeff0)[1]]) if k%2==0 else np.array([-1.0,arcs(y[k],coeff1)[1]])
        n/=np.linalg.norm(n)
        reflected=rays[k-1]-2*np.dot(rays[k-1],n)*n
        residual=max(residual,float(np.max(np.abs(reflected-rays[k]))))
    return y,float(en.sum()),logtwist,logtwist0,H,residual


def quadrature_ratio(g, coeff0, coeff1, j, delta):
    _,_,_,_,H,_=bridge(g,coeff0,coeff1,j,0,0)
    nodes,weights=leggauss(12); total=0.0
    for theta in (np.arange(32)+.5)*2*np.pi/32:
        direction=np.array([np.cos(theta),np.sin(theta)])
        initial=math.sqrt(2*delta/(direction@H@direction))
        def energy(rad):
            return bridge(g,coeff0,coeff1,j,*(rad*direction))[1]
        radius=brentq(lambda rr:energy(rr)-delta,initial*.6,initial*1.5,xtol=1e-14)
        for x,w in zip(nodes,weights):
            rad=radius*(x+1)/2
            _,ex,lt,_,_,_=bridge(g,coeff0,coeff1,j,*(rad*direction))
            total+=(2*np.pi/32)*(radius/2)*w*(delta-ex)*math.exp(lt)*rad
    gamma=math.acosh(math.sqrt((1+g*coeff0[0])*(1+g*coeff1[0])))
    return total/(np.pi*delta**2/math.sinh(j*gamma))


def main():
    for g,c0,c1,c in [(Q(1,5),Q(3,2),Q(8,3),Q(2)),
                      (Q(2,7),Q(4,3),Q(3),Q(2)),
                      (Q(1,10),Q(5,4),Q(5,4),Q(5,4))]:
        for j in [1,2,3,4,8,16,32,64]:
            H,detint=exact_schur(g,c0,c1,j);T,U=cheb(c,j)
            s0sq=c1;sjsq=c1 if j%2==0 else c0
            sprod=c1 if j%2==0 else c
            check(H[0][0]==c*T/(g*s0sq*U),'Endpoint 00','exact_jacobi')
            check(H[1][1]==c*T/(g*sjsq*U),'Endpoint 11','exact_jacobi')
            check(H[0][1]==-c/(g*sprod*U),'Endpoint mixed','exact_jacobi')
            detH=H[0][0]*H[1][1]-H[0][1]**2
            check(detH==c*c*(c*c-1)/(g*g*s0sq*sjsq),'Effective determinant','exact_jacobi')
            check(-H[0][1]==(1/g)**j/detint,'Corner cofactor','exact_jacobi')
            check(H[0][1]**2/detH==1/((c*c-1)*U*U),'Universal ratio','exact_jacobi')
    theta=sp.symbols('theta',real=True)
    R,al,be,ze=sp.symbols('R alpha beta zeta',real=True)
    b=al+be*sp.cos(2*theta)+ze*sp.sin(2*theta)
    h=R+(1-sp.cos(6*theta))*b
    for k in range(6):
        angle=sp.pi*k/3
        check(sp.simplify(h.subs(theta,angle)-R)==0,'Same support value','exact_support')
        check(sp.simplify(sp.diff(h,theta).subs(theta,angle))==0,'Axial support point','exact_support')
        check(sp.simplify((h+sp.diff(h,theta,2)).subs(theta,angle)-R-36*b.subs(theta,angle))==0,'Curvature jet','exact_support')
    sample=sp.Matrix([[1,1,0],[1,-sp.Rational(1,2),sp.sqrt(3)/2],[1,-sp.Rational(1,2),-sp.sqrt(3)/2]])
    check(sample.det()!=0,'Independent curvature jets','exact_support')
    A=Q(3,4); xs=[Q(1,3),Q(1,4),Q(1,5)];cutoff=31
    C=lambda j:2/A*sum(x**j/(1-x**(2*j)) for x in xs)
    exact_F=[Q(0)]+[2/A*sum(x**j for x in xs) for j in range(1,8)]
    errors=[]
    for j in range(1,7):
        approx=sum(int(sp.mobius(k))*C(k*j) for k in range(1,cutoff+1,2))
        xmax=max(xs);bound=6/A*xmax**((cutoff+1)*j)/((1-xmax**j)*(1-xmax**(2*j)))
        check(abs(approx-exact_F[j])<=bound,'Mobius truncation with exact tail bound','exact_inverse')
        errors.append(float(abs(approx-exact_F[j])))
    # Exact moment recurrence, followed by a numerical Hankel recovery check.
    polynomial=sp.Poly(sp.prod(sp.Symbol('x')-sp.Rational(x.numerator,x.denominator) for x in xs),sp.Symbol('x'))
    coeff=[Q(int(v.p),int(v.q)) for v in polynomial.all_coeffs()]
    for j in range(1,5):
        check(sum(coeff[k]*exact_F[j+3-k] for k in range(4))==0,'Primitive spectrum recurrence','exact_inverse')
    H0=np.array([[float(exact_F[i+j+1]) for j in range(3)] for i in range(3)])
    H1=np.array([[float(exact_F[i+j+2]) for j in range(3)] for i in range(3)])
    nodes=eigh(H1,H0,eigvals_only=True)
    check(np.max(abs(nodes-np.array(sorted(map(float,xs)))))<1e-10,'Hankel spectral recovery','floating_inverse')
    # Axial source parity and the moving-boundary derivative, checked symbolically.
    a0,a1=Q(2,3),Q(-1,5)
    for j in range(1,33):
        direct=sum(a0 if i%2==0 else a1 for i in range(j+1))
        formula=(j+1)*(a0+a1)/2+(a0-a1)/2*(j%2==0)
        check(direct==formula,'Axial source parity','exact_sources')
    p,zx,zy,eta=sp.symbols('p x y eta',real=True)
    psi=sp.Rational(1,2)+p*zx+p**2*zy;top=1-zx*zx-zy*zy
    F=1+p*eta+zx*zx
    I=sp.integrate(F,(eta,psi,top))
    derivative=sp.integrate(sp.diff(F,p),(eta,psi,top))-F.subs(eta,psi)*sp.diff(psi,p)
    check(sp.simplify(sp.diff(I,p)-derivative)==0,'Moving cut Leibniz term','exact_cut')
    check(sp.simplify(sp.diff(I,p)-sp.integrate(sp.diff(F,p),(eta,psi,top)))!=0,'Boundary term cannot be omitted','exact_cut')
    stress=[]
    cases=[(.12,(3.0,1.2,2.0),(6.0,-.8,1.0)),(.3,(2.5,-1.0,1.5),(4.0,.7,2.0))]
    for g,k0,k1 in cases:
        largest_residual=0.;largest_log_ratio=0.
        for j in [1,2,3,8,32,128,256]:
            for u,v in [(1e-3,-.7e-3),(.3e-3,.8e-3)]:
                y,energy,lt,lt0,H,res=bridge(g,k0,k1,j,u,v)
                small=bridge(g,k0,k1,j,u/2,v/2)
                quad=.5*np.array([u,v])@H@np.array([u,v])
                small_quad=quad/4
                check(res<1e-11,'Specular reflection of non-even facing arcs','floating_nonlinear')
                check(energy>0 and np.isfinite(lt) and abs(lt-lt0)<.02,'Positive relative nonlinear twist','floating_nonlinear')
                check(abs(small[2]-small[3])<=.7*abs(lt-lt0)+1e-10,'Linear relative perturbation scale','floating_nonlinear')
                # Evaluate the cubic term on the linear stationary bridge.
                # Comparing total remainders alone is invalid when cubic and
                # quartic contributions nearly cancel at the larger amplitude.
                c0=1+g*k0[0];c1=1+g*k1[0]
                gamma=math.acosh(math.sqrt(c0*c1));ind=np.arange(j+1)
                sigma=np.sqrt(np.where(ind%2==0,c1,c0))
                ratio=lambda n:np.exp(-gamma*(j-n))*(-np.expm1(-2*gamma*n))/(-math.expm1(-2*gamma*j))
                linear=sigma*(ratio(j-ind)*u/sigma[0]+ratio(ind)*v/sigma[-1])
                beta=np.where(ind%2==0,k0[1],k1[1])
                cubic=float(np.sum((beta[:-1]*linear[:-1]**3+beta[1:]*linear[1:]**3)/6))
                large_error=energy-quad-cubic
                small_error=small[1]-small_quad-cubic/8
                check(abs(small_error)<=.08*abs(large_error)+1e-15,
                      'Quartic remainder after explicit cubic term','floating_nonlinear')
                largest_residual=max(largest_residual,res);largest_log_ratio=max(largest_log_ratio,abs(lt-lt0))
        stress.append({'g':g,'max_reflection_residual':largest_residual,'max_absolute_log_relative_twist':largest_log_ratio})
    quads=[]
    for j in [1,2,3,8]:
        g,k0,k1=cases[0]
        ratios=[quadrature_ratio(g,k0,k1,j,d) for d in [1e-5,2.5e-6]]
        check(abs(ratios[1]-1)<.002,'Unequal-curvature onset coefficient','floating_quadrature')
        check(abs(ratios[1]-1)<=.4*abs(ratios[0]-1)+1e-8,'Radial odd cancellation','floating_quadrature')
        quads.append({'j':j,'offsets':[1e-5,2.5e-6],'ratio_to_predicted_coefficient':ratios})
    print(json.dumps({'status':'PASS','schema':'a2-geometric-thresholds-v2','checks':COUNTS,
        'total_checks':sum(COUNTS.values()),'python':platform.python_version(),
        'mobius_truncation_errors':errors,'nonlinear_facing_arc_stress':stress,'quadrature':quads,
        'scope':'Exact finite algebra and non-interval floating diagnostics. Not a continuum proof, complete equilibrium simulation, or noisy inverse stability result.'},indent=2,sort_keys=True))

if __name__=='__main__':main()
