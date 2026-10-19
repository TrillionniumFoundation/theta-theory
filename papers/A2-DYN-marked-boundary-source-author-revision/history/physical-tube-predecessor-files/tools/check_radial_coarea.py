#!/usr/bin/env python3
"""Exact algebra and genuine finite billiard diagnostics for core 286.

These tests do not certify uniform curve growth, a continuous probability
bound, a complete root sum, or the raw local limit theorem.  The ray tracer
uses a finite lattice search box; every accepted flight is an actual nearest
positive disk hit in that box.  All diagnostic limitations are in the output.
"""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path
from typing import Any
import numpy as np
import sympy as sp
from check_cross_flight import CENTERS, next_hit, perp


def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def relative(a: np.ndarray | float, b: np.ndarray | float) -> float:
    return float(np.linalg.norm(np.asarray(a)-np.asarray(b)) /
                 max(1.0, float(np.linalg.norm(np.asarray(a))),
                     float(np.linalg.norm(np.asarray(b)))))


def exact_checks() -> dict[str, Any]:
    a,b,d,R,r,ct,st=sp.symbols('a b d R r ct st', real=True, nonzero=True)
    G=sp.Matrix([[a,b],[b,d]]);D=sp.diag(-1,1);z=r*sp.Matrix([ct,st])
    inv=G.inv(); qz=R*inv*D
    require(sp.simplify(qz.T*(R*D*z)-D*(G/R**2).inv()*D*z)==sp.zeros(2,1),
            'endpoint momentum gradient chain rule')
    B=sp.Matrix([[-a/b,-R/b],[-G.det()/(R*b),-d/b]])
    require(sp.simplify(B.det()-1)==0, 'generating matrix determinant')
    # The analytic lower-left derivative has magnitude det(G)/(R*abs(b)).
    u=R*b/G.det()  # signed proxy; identities hold with absolute b as well
    e=sp.Matrix([ct,st]);h=(e.T*D*(G/R**2).inv()*D*e)[0]
    c=sp.symbols('c',positive=True)
    require(sp.simplify((u*r/(4*sp.pi*c))/(r*h)-u/(4*sp.pi*c*h))==0,
            'exact radial coarea cancellation')
    # All continuum Schur inequalities are proved variationally in the text;
    # these are independent exact rational tests, not their proof.
    chains=0
    for m in range(1,10):
        for v in range(9):
            RR=[sp.Rational(9,20),sp.Rational(23,50),sp.Rational(47,100)][v%3]
            cs=[sp.Rational(9,10)]+[
                [sp.Rational(1,10**6),sp.Rational(1,2),sp.Rational(99,100)][(i+v)%3]
                for i in range(1,m)]+[sp.Rational(4,5)]
            ts=[sp.Rational(3,50)+(sp.Rational((i+v)%7,25)) for i in range(m)]
            H=sp.zeros(m+1)
            for i,cc in enumerate(cs):H[i,i]+=RR*cc*(1 if i in (0,m) else 2)
            for i,tau in enumerate(ts):
                vv=sp.zeros(m+1,1);vv[i]=cs[i];vv[i+1]=cs[i+1]
                H+=RR**2/tau*vv*vv.T
            inds=[0,m];GG=H.extract(inds,inds)
            if m>1:
                interior=list(range(1,m));C=H.extract(inds,interior)
                GG-=C*H.extract(interior,interior).inv()*C.T
            low=GG-RR*sp.diag(cs[0],cs[-1])
            require(low[0,0]>=0 and low[1,1]>=0 and low.det()>=0,'exact Schur lower bound')
            upper=(sp.Rational(320,9) if m==1 else sp.Rational(170,9))*sp.eye(2)-GG/RR**2
            require(upper[0,0]>=0 and upper[1,1]>=0 and upper.det()>=0,'exact global endpoint upper bound')
            require(GG.det()>0 and GG[0,1]!=0,'nondegenerate exact optical reduction')
            chains+=1
    # Positive polar integrals and the physical gradient normalization.
    A,gamma=sp.symbols('A gamma',positive=True)
    for gg in [sp.Rational(0),sp.Rational(1,2),sp.Rational(1),sp.Rational(3,2)]:
        val=sp.integrate(2*sp.pi*r**(1-gg),(r,0,A))
        require(sp.simplify(val-2*sp.pi*A**(2-gg)/(2-gg))==0,'singularity budget integral')
    return {'symbolic_matrix_and_normalization_identities':4,
            'exact_rational_schur_chains':chains,'exact_polar_integrals':4,
            'smallest_interior_test_incidence':'1/1000000',
            'uniform_dynamical_inputs_certified':False}


def horizon_checks() -> dict[str, Any]:
    from fractions import Fraction as F
    widths=[]
    for a,t in [(0,F(1,60)),(5,F(1,60)),(2,F(1,12)),(1,F(1,5))]:
        P=(1+2*t) if a==0 else (F(2*a+1)+3*t)/F(2*(a*a+a+1))+1-(2*a+1)*t
        sq=F(3,16)*P*P/(1+3*t*t);gap=F(81,400)-sq
        require(gap>0,'strict all-direction covering margin')
        widths.append({'vector_a':a,'parameter':str(t),'width_squared':str(sq),'squared_margin':str(gap)})
    require(F(3847,124)<F(28,5)**2,'explicit uniform physical horizon comparison')
    counts={}
    for Q in [42,43]:
        pts=[(a,b) for a in range(-7,8) for b in range(-7,8) if 0<a*a+a*b+b*b<=Q]
        require(len(pts)=={42:150,43:162}[Q],'exact quadratic-form candidate count')
        counts[str(Q)]={'nonzero_count':len(pts),'nonnegative_row_counts':[sum(a*a+a*b+b*b<=Q for a in range(-7,8)) for b in range(8)]}
    require(42<F(327,50)**2<43 and 42<F(1311,200)**2<43 and 43<F(657,100)**2<44,
            'enclosing squared radii and integer cutoffs')
    return {'exact_orientation_widths':widths,'free_flight_bound_squared':'3847/124',
            'rational_enclosing_horizon':'28/5','exact_lattice_counts':counts,
            'first_hit_branch_upper_bound':301,'angular_partition_interval_upper_bound':1201,
            'scope':'exact arithmetic diagnostic; continuum geometric argument is the native proof 287'}


def orbit(alpha: float, p: float, R: float, m: int) -> dict[str, Any]:
    """Differentiate the true specular flight equations forward analytically."""
    require(abs(p)<1,'outgoing momentum in physical range')
    n=np.array([math.cos(alpha),math.sin(alpha)]);t=perp(n);c=math.sqrt(1-p*p)
    q=R*n;v=c*n+p*t
    dq=np.column_stack((R*t,np.zeros(2)))
    dv=np.column_stack((c*t-p*n,-p/c*n+t))
    L=0.;dL=np.zeros(2);word=[];flights=[];incs=[];clearances=[]
    for _ in range(m):
        hit,nv,tau,inc,idx=next_hit(q,v,R)
        raw_n=(hit-CENTERS[idx])/R
        require(abs(float(np.linalg.norm(raw_n))-1)<2e-8,'actual disk contact')
        # Do not differentiate a nearest-hit choice or a normalized proxy:
        # on a fixed strict word the exact physical implicit contact gives
        # the derivative below; roundoff in a unit normal is only diagnostic.
        dh0=dq+tau*dv
        dtau=-(raw_n@dh0)/float(raw_n@v)
        dh=dh0+np.outer(v,dtau);dn=dh/R
        vd=float(v@raw_n)
        dnewv=dv-2*(np.outer(raw_n,raw_n@dv+v@dn)+vd*dn)
        rel=CENTERS-q;foot=rel@v;impact=np.abs(rel@perp(v))-R
        candidates=(foot>1e-8)&(foot<tau-1e-8)
        candidates[idx]=False
        # Negative impact would mean an unvisited obstacle on the free segment.
        # The departure disk has no interior foot along an outgoing flight.
        cl=float(np.min(impact[candidates])) if np.any(candidates) else None
        require(cl is None or cl>=-1e-7,'unvisited obstacle cuts an alleged free flight')
        tang=perp(raw_n);dalpha=tang@dn
        pm=float(nv@tang);cm=float(nv@raw_n)
        dp=dnewv.T@tang-cm*dalpha
        dalpha=np.asarray(dalpha);dp=np.asarray(dp)
        L+=tau;dL+=dtau
        word.append(int(idx));flights.append(float(tau));incs.append(float(inc));clearances.append(cl)
        q=hit;v=nv;dq=dh;dv=dnewv
    M=np.vstack((dalpha,dp))
    return {'L':L,'dL':dL,'M':M,'pm':pm,'word':word,'flights':flights,
            'incidences':incs,'unvisited_clearances':clearances,'alpha0':alpha,'p0':p,'R':R,'m':m}


def physical_checks() -> tuple[dict[str, Any],list[dict[str, Any]]]:
    rng=np.random.default_rng(2026101607);rows=[];errors=[];metric_tests=0;finite_diffs=0
    rho=.94;K=(100/47)*math.sqrt(1-rho*rho);D=np.diag([-1.,1.])
    excluded_momentum=0;excluded_condition=0;chart_changes=0
    for run in range(480):
        R=[.45,.46,.47][run%3];m=[1,2,3,4,5,7][run%6]
        alpha=float(rng.uniform(-math.pi,math.pi));p=float(rng.uniform(-.65,.65))
        o=orbit(alpha,p,R,m);M=o['M'];z=np.array([p,o['pm']])
        if np.linalg.norm(z)>=rho:excluded_momentum+=1;continue
        # Large tangent condition numbers are not presented as validated
        # finite-difference cases; retained counts disclose this restriction.
        cond=float(np.linalg.cond(M))
        if cond>1e13:excluded_condition+=1;continue
        G=R*np.array([[M[0,0]/M[0,1],-1/M[0,1]],[-1/M[0,1],M[1,1]/M[0,1]]])
        eig=np.linalg.eigvalsh(G/R**2);U=320/9 if m==1 else 170/9
        require(eig[0]>=K-1e-7 and eig[1]<=U+1e-7,'actual physical endpoint metric bounds')
        require(np.linalg.det(G)>0,'actual endpoint action positivity')
        expected=np.array([-R*p+R*o['pm']*M[0,0], R*o['pm']*M[0,1]])
        first=relative(o['dL'],expected)
        require(first<2e-7,'physical first variation failed')
        Dz=np.vstack((np.array([0.,1.]),M[1]))
        actual_grad=np.linalg.solve(Dz.T,o['dL'])
        predicted=D@np.linalg.solve(G/R**2,D@z)
        graderr=relative(actual_grad,predicted)
        require(graderr<3e-5,'momentum gradient exact chain-rule identity')
        r=float(np.linalg.norm(z));e=z/r;h=float(e@D@np.linalg.solve(G/R**2,D@e))
        radialerr=abs(float(actual_grad@e)-r*h)
        require(radialerr<4e-5,'nonlinear radial roof derivative')
        u_actual=1/abs(M[1,0]);u_hessian=R*abs(G[0,1])/np.linalg.det(G)
        uerr=relative(u_actual,u_hessian)
        require(uerr<2e-7,'physical coarea root Jacobian')
        metric_tests+=1
        differr=None
        if m<=3 and cond<1e9 and min(o['incidences'])>.08:
            step=1e-7/max(1.,float(np.linalg.norm(M)))
            if step>1e-12:
                plus=orbit(alpha+step,p,R,m);minus=orbit(alpha-step,p,R,m)
                if plus['word']==o['word']==minus['word']:
                    fd=(plus['L']-minus['L'])/(2*step)
                    differr=relative(fd,o['dL'][0]);require(differr<4e-3,'same-word independent physical finite difference')
                    finite_diffs+=1
                else:chart_changes+=1
        errors.append([first,graderr,radialerr,uerr])
        rows.append({k:o[k] for k in ['alpha0','p0','R','m','L','pm','word','flights','incidences','unvisited_clearances']} |
                    {'momentum_radius':r,'metric_eigenvalues':eig.tolist(),'root_jacobian':float(u_actual),
                     'first_variation_error':first,'momentum_gradient_error':graderr,
                     'radial_derivative_error':radialerr,'root_jacobian_error':uerr,
                     'same_word_finite_difference_error':differr,'tangent_condition_number':cond})
    require(metric_tests>150 and finite_diffs>60,'insufficient actual physical verification cases')
    return {'attempted_physical_orbits':480,'accepted_metric_cases':metric_tests,
            'independent_same_word_finite_differences':finite_diffs,
            'excluded_outside_momentum_disk':excluded_momentum,
            'excluded_tangent_ill_conditioned':excluded_condition,'finite_difference_chart_changes':chart_changes,
            'max_errors_first_variation_momentum_gradient_radial_root':np.max(np.array(errors),axis=0).tolist()},rows


def radial_arms() -> tuple[dict[str, Any],list[dict[str, Any]]]:
    """Continue real alternating normal collision words, without changing L."""
    rows=[];max_residual=0.;rho=.2;K=(100/47)*math.sqrt(1-rho*rho)
    for R in [.45,.46,.47]:
        for m in [1,2,3,4,5]:
            origin=orbit(0.,0.,R,m);word=origin['word'];critical=m*(1-2*R)
            require(abs(origin['L']-critical)<1e-10,'actual normal orbit roof')
            for theta in np.linspace(.1,2*math.pi-.1,12):
                alpha=0.
                for radius in [.002,.008,.025,.06,.12]:
                    p=radius*math.cos(float(theta));target=radius*math.sin(float(theta))
                    # Newton uses the exact actual first-hit derivative and
                    # fails rather than continuing a nonphysical word.
                    for _ in range(25):
                        o=orbit(alpha,p,R,m)
                        require(o['word']==word,'radial diagnostic escaped its physical word')
                        residual=o['pm']-target
                        if abs(residual)<2e-11:break
                        alpha-=residual/o['M'][1,0]
                    else:raise RuntimeError('actual inverse-momentum continuation failed')
                    require(abs(residual)<2e-11,'inverse-momentum root residual')
                    max_residual=max(max_residual,abs(residual))
                    excess=o['L']-critical;U=320/9 if m==1 else 170/9
                    lower=radius*radius/(2*U);upper=radius*radius/(2*K)
                    require(excess>=lower-1e-10 and excess<=upper+1e-10,'nonlinear physical critical band inequality')
                    rows.append({'R':R,'m':m,'theta':float(theta),'radius':radius,
                                 'alpha0':alpha,'p0':p,'pm':o['pm'],'critical_physical_roof':critical,
                                 'physical_roof':o['L'],'excess':excess,'proved_lower_bound':lower,
                                 'proved_upper_bound':upper,'root_residual':residual,
                                 'word':word,'flights':o['flights'],'incidences':o['incidences']})
    return {'actual_critical_origin_points':len(rows),'max_inverse_momentum_residual':max_residual,
            'collision_counts':[1,2,3,4,5],'radii':[.45,.46,.47]},rows


def main() -> None:
    ap=argparse.ArgumentParser();ap.add_argument('--details',type=Path);args=ap.parse_args()
    exact=exact_checks();horizon=horizon_checks();phys,rows=physical_checks();arms,arows=radial_arms()
    result={'status':'passed','exact':exact,'explicit_horizon':horizon,'actual_orbits':phys,'actual_radial_arms':arms,
            'scope':'finite algebra and true finite specular trajectory diagnostics, not proof certification',
            'uniform_root_sum_certified':False,'original_roof_supremum_bound_certified':False,
            'full_raw_pointwise_LLT_proved':False,
            'limitations':['Finite diagnostic lattice box, not a proof of the finite-horizon constant.',
                           'Ill-conditioned derivative and out-of-momentum-disk exclusions are counted.',
                           'Radial continuation samples one genuine alternating family; all-family theorem is analytic.',
                           'No floating-point output proves the all-words, all-time, measure or ordered-limit claims.']}
    if args.details:
        args.details.parent.mkdir(parents=True,exist_ok=True)
        args.details.write_text(json.dumps({'physical_orbits':rows,'critical_origin_arms':arows},indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
