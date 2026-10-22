#!/usr/bin/env python3
"""Exact algebra and deterministic physical-ray diagnostics; not a proof certificate."""
from __future__ import annotations
import json
import math
from fractions import Fraction as F
import numpy as np
import sympy as sp


def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def exact_checks() -> dict:
    alpha, phi, radius, zx, zy = sp.symbols('alpha phi R zx zy', real=True)
    theta = alpha + phi
    q = sp.Matrix([radius*sp.cos(alpha), radius*sp.sin(alpha)])
    v = sp.Matrix([sp.cos(theta), sp.sin(theta)])
    vp = sp.Matrix([-sp.sin(theta), sp.cos(theta)])
    z = sp.Matrix([zx, zy])
    b = (z-q).dot(vp)
    determinant = sp.trigsimp(sp.Matrix([theta,b]).jacobian([alpha,phi]).det())
    require(sp.trigsimp(determinant-radius*sp.cos(phi)) == 0, 'line Jacobian in alpha,phi')
    # dp = cos(phi) dphi, so the alpha,p Jacobian is R on regular states.
    slope = sp.symbols('h', real=True)
    derivative = sp.diff(b,alpha)/radius + slope*sp.diff(b,phi)
    expected = -sp.cos(phi) - (z-q).dot(v)*(1/radius+slope)
    require(sp.trigsimp(sp.expand_trig(derivative-expected)) == 0, 'signed strip derivative')
    lo, hi, gap, delta = F(9,20),F(47,100),F(3,50),F(3,200)
    require(1-2*hi==gap and delta==gap/4, 'uniform disk gap')
    margin=1/hi-1/(1-hi); a0=(gap-delta)/hi
    require(margin==F(600,2491)>0 and a0==F(9,94)>0,'transversality constants')
    require(2*hi+delta<1,'marked tube free of all other actual disks')
    depth_cases=0
    for m in range(1,257):
        ds=[min(j,m-1-j) for j in range(m)]
        require(all(ds.count(d)<=2 for d in set(ds)), 'two collision-end layers')
        for a in [F(0),F(1,4),F(1,2),F(3,4)]:
            # Finite sum domination for a representative exact rational r.
            rr=F(4,5)
            require(sum(rr**d for d in ds)<=2/(1-rr),'geometric sum')
            depth_cases+=1
    # The interpolation inequality is checked exactly at rational a=0,1/2 via squares.
    interpolation_cases=0
    for xi in range(1,80):
        for di in range(1,40):
            x,D=F(xi,13),F(di,17)
            require(min(x,D)<=D, 'a=0 bound')
            require(min(x,D)**2/x<=D, 'a=1/2 interpolation')
            interpolation_cases+=1
    return {'alpha_phi_jacobian':'R*cos(phi)', 'alpha_p_jacobian':'R',
            'strip_derivative':'-cos(phi)-t*(1/R+h)',
            'gap_minus_delta':str(gap-delta),'angle_margin':str(margin),
            'grazing_uniform_derivative':str(a0), 'depth_cases':depth_cases,
            'interpolation_cases':interpolation_cases}


def lattice(extent: int=4) -> np.ndarray:
    return np.array([(i+j/2,math.sqrt(3)*j/2) for i in range(-extent,extent+1)
                     for j in range(-extent,extent+1)],dtype=float)


def flight(q: np.ndarray,v: np.ndarray,R: float,centers: np.ndarray):
    rel=centers[None,:,:]-q[:,None,:]
    along=np.einsum('bci,bi->bc',rel,v)
    dist2=np.einsum('bci,bci->bc',rel,rel)-along*along
    disc=R*R-dist2
    near=along-np.sqrt(np.maximum(disc,0))
    valid=(disc>1e-13)&(near>1e-10)
    roots=np.where(valid,near,np.inf)
    idx=np.argmin(roots,axis=1)
    tau=roots[np.arange(len(q)),idx]
    require(bool(np.isfinite(tau).all()),'finite scan did not find a physical next hit')
    return tau,idx,along,dist2


def physical_diagnostics() -> dict:
    centers=lattice(); rng=np.random.default_rng(20261015)
    rows=[]; count=60000; max_tau=0.; gap_min=math.inf; derivative_min=math.inf
    for R in [0.45,0.46,0.47]:
        counts=[]
        for start in range(0,count,1000):
            n=min(1000,count-start)
            alpha=rng.uniform(-math.pi,math.pi,n); p=rng.uniform(-1,1,n)
            phi=np.arcsin(p); theta=alpha+phi
            q=R*np.column_stack((np.cos(alpha),np.sin(alpha)))
            v=np.column_stack((np.cos(theta),np.sin(theta)))
            tau,hit,along,dist2=flight(q,v,R,centers)
            max_tau=max(max_tau,float(tau.max()))
            # Truncate the scanned domain safely only for this diagnostic: every disk
            # outside the index box is beyond all measured flights, checked by bound.
            boundary_min=3.0 # |i|>=5 or |j|>=5 implies norm >= sqrt(3)*5/2 > 4.3.
            require(bool((tau+2*R+0.015<boundary_min).all()),'scan completeness margin')
            b=(centers[None,:,:]-q[:,None,:])[:,:,0]*(-v[:,1,None])+(centers[None,:,:]-q[:,None,:])[:,:,1]*v[:,0,None]
            clearance=np.sqrt(np.maximum(dist2,0))-R
            mark=(along>0)&(along<tau[:,None])&(clearance>1e-11)&(clearance<0.015)
            mark[np.arange(n),hit]=False
            counts.extend(mark.sum(axis=1).tolist())
            bi,ci=np.where(mark)
            if len(bi):
                g=(1-2*R)-clearance[bi,ci]
                require(bool((along[bi,ci]+1e-9>=g).all()),'initial foot separation')
                require(bool((tau[bi]-along[bi,ci]+1e-9>=g).all()),'terminal foot separation')
                gap_min=min(gap_min,float(np.minimum(along[bi,ci],tau[bi]-along[bi,ci]).min()))
                deriv=np.cos(phi[bi])+along[bi,ci]/R # h=0, weakest increasing graph slope
                require(bool((deriv>=9/94-1e-9).all()),'uniform strip derivative in actual samples')
                derivative_min=min(derivative_min,float(deriv.min()))
        arr=np.array(counts,dtype=float); expected=0.015/R
        se=float(arr.std(ddof=1)/math.sqrt(count))
        rows.append({'R':R,'sample_count':count,'mean_near_miss_count':float(arr.mean()),
                     'exact_flux_prediction':expected,'standard_error':se,
                     'standardized_difference':float((arr.mean()-expected)/se)})
    # Reconstruct near misses from line parameters: a diagnostic of the exact inverse map.
    inverse_cases=0; clearance_error=0.; impact_error=0.
    for R in [0.45,0.46,0.47]:
        n=2000; theta=rng.uniform(-math.pi,math.pi,n);u=rng.uniform(1e-5,0.01499,n)
        sig=rng.choice([-1.,1.],n)
        v=np.column_stack((np.cos(theta),np.sin(theta))); vp=np.column_stack((-np.sin(theta),np.cos(theta)))
        foot=-sig[:,None]*(R+u)[:,None]*vp
        back,prev,_,_=flight(foot,-v,R,centers)
        q=foot-back[:,None]*v
        forward,nxt,along,dist2=flight(q,v,R,centers)
        origin=np.argmin(np.einsum('ci,ci->c',centers,centers))
        require(bool((prev!=origin).all() and (nxt!=origin).all()),'mark counted as actual collision')
        require(bool((back>0).all() and (back<forward).all()),'inverse foot not interior')
        require(bool((forward+2*R+0.015<3.0).all()),'inverse scan completeness margin')
        measured=np.sqrt(np.maximum(dist2[:,origin],0))-R
        err=np.max(np.abs(measured-u));clearance_error=max(clearance_error,float(err))
        require(bool(err<1e-8),'inverse clearance mismatch')
        nvec=(q-centers[prev])/R
        p=np.einsum('bi,bi->b',np.column_stack((-nvec[:,1],nvec[:,0])),v)
        require(bool((np.abs(p)<1+1e-9).all()),'physical outgoing p')
        require(bool((np.einsum('bi,bi->b',nvec,v)>0).all()),'not an outgoing collision')
        inverse_cases+=n
    return {'stationary_flux_diagnostics':rows,'sampled_max_flight':max_tau,
            'sampled_min_endpoint_foot_distance':gap_min,'sampled_min_strip_derivative':derivative_min,
            'inverse_line_cases':inverse_cases,'max_inverse_clearance_error':clearance_error,
            'scope':'Deterministic floating-point diagnostics only; no continuous geometry or LLT certification.'}


def main() -> None:
    print(json.dumps({'exact_algebra':exact_checks(),'physical_diagnostics':physical_diagnostics(),
                      'status':'all_explicit_program_checks_passed',
                      'not_certified':['uniform dynamical growth','target-roof m^-2 bound','full raw LLT']},
                     sort_keys=True,indent=2))

if __name__=='__main__': main()
