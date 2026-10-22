#!/usr/bin/env python3
"""Exact algebra and finite physical diagnostics for modules 274--275.

No test is a certificate of a continuum theorem, uniform pressure,
all-word summability, or the original raw pointwise local limit theorem.
All failures are explicit under both ordinary and optimized Python.
"""
from __future__ import annotations
import json
import math
from fractions import Fraction as F
import numpy as np
import sympy as sp


def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def exact_algebra() -> dict:
    a, d, e, R = sp.symbols('a d e R', nonzero=True, real=True)
    delta = a*d-e*e
    B = sp.Matrix([[-a/e,-R/e],[-delta/(R*e),-d/e]])
    J = sp.diag(1,-1)
    M = J*B.inv()*J*B
    require(sp.simplify(B.det()-1)==0, 'half map determinant')
    require(sp.simplify(M.det()-1)==0, 'return determinant')
    require(sp.simplify(sp.trace(M)-2-4*delta/e**2)==0, 'trace sign and factor four')
    require(sp.simplify((sp.eye(2)-M).det()+4*delta/e**2)==0, 'signed stability determinant')
    c, omega, chi = sp.symbols('c omega chi', positive=True)
    require(sp.simplify(1/(4*sp.pi*R*c)/(chi/(R*omega))-omega/(4*sp.pi*c*chi))==0,
            'clearance-to-roof normalization')
    # Squared coefficients avoid an unjustified sign choice in a symbolic square root.
    lhs = (e/R)**2/(4*c*c*delta)
    rhs = 1/(R*R*c*c*(4*delta/e**2))
    require(sp.simplify(lhs-rhs)==0,'critical coefficient')
    require(F(6,1)/(F(47,1)*F(47,100))==F(600,2209),'uniform determinant growth constant')
    q1,q2=sp.symbols('q1 q2', real=True)
    # A nonlinear coordinate map explicitly checks the noncritical Hessian term.
    Q=sp.Matrix([q1+q1*q2,q2+q1*q1]); G=sp.Matrix([[a,e],[e,d]])
    Fq=(Q.T*G*Q)[0]/2 + Q[0]
    grad=G*Q+sp.Matrix([1,0]); A=Q.jacobian([q1,q2])
    correction=sum((grad[i]*sp.hessian(Q[i],[q1,q2]) for i in range(2)),sp.zeros(2))
    require((sp.hessian(Fq,[q1,q2])-A.T*G*A-correction).applyfunc(sp.simplify)==sp.zeros(2),
            'noncritical Hessian chain term')
    return {'symbolic_identities':7,'half_map_determinant':1,
            'stability_determinant':'det(I-M)=-4*(a*d-e^2)/e^2',
            'critical_coefficient':'omega/(2*c_star*sqrt(det(G)))',
            'noncritical_hessian_correction_retained':True}


def mm(A, B):
    return [[sum(A[i][k]*B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]


def power(A, n):
    B=[[F(1),F(0)],[F(0),F(1)]]
    for _ in range(n): B=mm(B,A)
    return B


def normal_orbits_exact() -> dict:
    """Real period-two horizontal trajectories, not a replacement dynamics.

    Compute the action Schur complement by exact rational elimination, and
    compare its generating derivative with the mth power of the true
    one-flight derivative. All rays lie on the horizontal gap between the
    actual disks at (0,0) and (1,0). Nearby third disks stay clear.
    """
    cases=0; accepted=0
    for R in [F(9,20),F(23,50),F(47,100)]:
        tau=1-2*R
        require(tau>0, 'positive physical roof')
        endpoint=R+R*R/tau; edge=R*R/tau
        step=[[-(1+tau/R),-tau/R],[-(2+tau/R),-(1+tau/R)]]
        for m in range(1,33):
            # Eliminate interior vertices of the exact normal broken-path Hessian.
            aa=endpoint; ee=edge; dd=endpoint if m==1 else 2*endpoint
            for j in range(1,m):
                aa=aa-ee*ee/dd
                ee=-ee*edge/dd
                dd=(endpoint if j==m-1 else 2*endpoint)-edge*edge/dd
            det=aa*dd-ee*ee
            require(det>0 and ee!=0,'positive reduced action and nonzero signed corner')
            reduced=[[-aa/ee,-R/ee],[-det/(R*ee),-dd/ee]]
            expected=power(step,m)
            require(reduced==expected,'actual normal trajectory vs action Schur complement')
            full=power(step,2*m); tr=full[0][0]+full[1][1]
            require(tr-2==4*det/(ee*ee),'physical return stability coefficient')
            # Equality of the two density coefficients, with c_star cancelled and squared.
            require(ee*ee/(4*R*R*det)==1/(R*R*(tr-2)), 'physical density normalization')
            # Original section at the normal state (0,0), not at (pi,0).
            forward=sum(j%2==0 for j in range(m))
            reverse=forward
            whole=sum(j%2==0 for j in range(2*m))
            if m%2==0:
                require(forward==m//2 and whole==forward+reverse,'original occupation identity')
                accepted+=1
            # These roofs are not asserted to be in the large-m central roof window.
            cases+=1
    return {'exact_physical_half_orbits':cases,'original_event_even_half_lengths':accepted,
            'radii':['9/20','23/50','47/100'],'half_lengths':'1..32',
            'third_disk_clearance':'at least sqrt(3)/2-R > 0',
            'central_window_or_capacity_claim':False}


def physical_ray_checks() -> dict:
    # Ray tracing is independent of the endpoint-action Schur calculation.
    centers=np.array([(i+j/2,math.sqrt(3)*j/2) for i in range(-4,5) for j in range(-4,5)])
    def step(alpha,p,R):
        n=np.array([math.cos(alpha),math.sin(alpha)])
        tangent=np.array([-n[1],n[0]])
        q=R*n;v=math.sqrt(1-p*p)*n+p*tangent
        rel=centers-q;along=rel@v
        disc=R*R-(np.sum(rel*rel,axis=1)-along*along)
        roots=along-np.sqrt(np.maximum(disc,0))
        valid=(disc>1e-12)&(roots>1e-9)
        roots=np.where(valid,roots,np.inf);i=int(np.argmin(roots));tau=float(roots[i])
        require(math.isfinite(tau),'next physical hit exists in diagnostic scan')
        require(tau+2*R<math.sqrt(3)*5/2,'finite scan completeness bound')
        q2=q+tau*v;normal=(q2-centers[i])/R
        require(abs(np.linalg.norm(normal)-1)<1e-10,'circle intersection')
        v2=v-2*np.dot(v,normal)*normal
        al=math.atan2(normal[1],normal[0]);pp=float(np.dot(v2,np.array([-normal[1],normal[0]])))
        return al,pp,tau,centers[i]
    def angular_difference(a,b): return math.atan2(math.sin(a-b),math.cos(a-b))
    max_derivative_error=0.; roof_error=0.; closure_error=0.;cases=0
    eps=1e-6
    for R in [.45,.46,.47]:
        t=1-2*R;reference=-np.array([[1+t/R,t/R],[2+t/R,1+t/R]])
        for alpha in [0.,math.pi]:
            base=step(alpha,0.,R)
            D=np.zeros((2,2))
            for j in range(2):
                args=[alpha,0.];args[j]+=eps;plus=step(*args,R)
                args=[alpha,0.];args[j]-=eps;minus=step(*args,R)
                D[0,j]=angular_difference(plus[0],minus[0])/(2*eps)
                D[1,j]=(plus[1]-minus[1])/(2*eps)
            err=float(np.max(np.abs(D-reference)));max_derivative_error=max(max_derivative_error,err)
            require(err<2e-8,'independent physical ray derivative')
            second=step(base[0],base[1],R)
            ce=max(abs(angular_difference(second[0],alpha)),abs(second[1]),np.linalg.norm(base[3]+second[3]))
            closure_error=max(closure_error,float(ce));roof_error=max(roof_error,abs(base[2]+second[2]-2*t))
            require(ce<1e-10,'actual period-two closure with displacement zero')
            cases+=1
    return {'physical_ray_base_states':cases,'max_derivative_absolute_error':max_derivative_error,
            'max_closure_error':closure_error,'max_two_flight_roof_error':roof_error,
            'finite_difference_step':eps,'interpretation':'diagnostic, not a continuum proof'}


def positive_band_and_fold_checks() -> dict:
    band=0;fold=0;max_ratio=0.
    for ell in range(1,9):
        kappa=math.factorial(ell)
        for h in [.00001,.001,.02,.1,1.,3.]:
            for a in [-3.,-1.,-.1,0.,.02,.4,2.]:
                # f(theta)=theta^ell on R, with exact monotone branch inverses.
                if ell%2:
                    inv=lambda x: math.copysign(abs(x)**(1/ell),x)
                    length=inv(a+h)-inv(a)
                else:
                    length=2*(max(a+h,0)**(1/ell)-max(a,0)**(1/ell))
                bound=2*ell*(h/kappa)**(1/ell)
                require(length<=bound*(1+2e-14),'finite type band constant')
                band+=1
    for a in [.5,1.,2.,4.]:
        for b in [.25,1.,3.]:
            for delta in [.0001,.01,.2,1.]:
                for t in np.linspace(-.2,2.,301)*b*delta:
                    D=2*math.sqrt(2/a)/b*(math.sqrt(max(float(t),0))-math.sqrt(max(float(t)-b*delta,0)))
                    bound=2*math.sqrt(2*delta/(a*b))
                    require(D>=-1e-14 and D<=bound*(1+1e-12),'integrated fold constant')
                    max_ratio=max(max_ratio,D/bound);fold+=1
                # Exact maximizer t=b*delta attains the theorem constant.
                peak=2*math.sqrt(2/a)/b*math.sqrt(b*delta)
                require(abs(peak-2*math.sqrt(2*delta/(a*b)))<1e-12,'sharp fold normalization')
    # Simple fold conditional density diverges at its own minimum; integrating u differs.
    return {'finite_type_band_cases':band,'integrated_fold_cases':fold,
            'grid_peak_to_bound_ratio':max_ratio,'fixed_clearance_Linfinity_assumed':False}


def radial_sector_checks() -> dict:
    # Perturbed positive quadratic action; only an analytic proof diagnostic.
    angles=(np.arange(16384)+.5)*(2*math.pi/16384)
    c=np.cos(angles);sn=np.sin(angles); cases=0;max_ratio=0.
    for beta in [-.2,0.,.2]:
        K=6*abs(beta);r0=.2;Lw=.1;w0=.7
        require(K*r0<=1,'radial Hessian budget')
        for s in [1e-8,1e-6,1e-4,.001,.009]:
            require(0<s<r0*r0/3,'radial roof range')
            r=np.full_like(c,math.sqrt(2*s))
            for _ in range(12):
                r-=(r*r/2+beta*r**3*c**3-s)/(r+3*beta*r*r*c**3)
            require(float(np.max(np.abs(r*r/2+beta*r**3*c**3-s)))<2e-15,'radial inversion')
            denom=r+3*beta*r*r*c**3
            weight=(w0+.1*r*c)*r/denom
            for mask in [np.ones_like(c,dtype=bool),c>0,(c>0)&(sn>0),np.sin(11*angles)>0]:
                D=2*math.pi*float(np.mean(weight*mask));fraction=float(mask.mean())
                error=abs(D-2*math.pi*w0*fraction)
                bound=2*math.pi*math.sqrt(3)*(2*Lw+K*w0)*math.sqrt(s)
                require(error<=bound+2e-12,'selector-uniform radial remainder')
                max_ratio=max(max_ratio,error/bound);cases+=1
    return {'radial_selector_cases':cases,'angular_quadrature_points':len(angles),
            'max_error_to_proved_bound_ratio':max_ratio,
            'uses_analytic_test_actions_not_replacement_physics':True}


def main() -> None:
    out={'status':'passed','scope':'Finite auxiliary diagnostics only; no uniform dynamical or LLT certificate.',
         'symbolic':exact_algebra(),'exact_physical':normal_orbits_exact(),
         'physical_ray':physical_ray_checks(),'band_fold':positive_band_and_fold_checks(),
         'radial':radial_sector_checks()}
    print(json.dumps(out,indent=2,sort_keys=True,allow_nan=False))


if __name__=='__main__': main()
