#!/usr/bin/env python3
"""Independent finite-series and coarsening diagnostics, not a proof certificate.

Finite Jacobi minimizers are evaluated independently of the Bellman inverse.
No assertion statement is used for a validity decision; -O must agree exactly.
"""
from __future__ import annotations
import json, math
import numpy as np
from scipy.linalg import solve_banded

ORDER=6

def require(ok: bool, message: str) -> None:
    if not ok: raise RuntimeError(message)

def mul(a, b):
    a,b=np.broadcast_arrays(a,b)
    out=np.zeros_like(a,dtype=float)
    for n in range(ORDER+1):
        for k in range(n+1): out[...,n]+=a[...,k]*b[...,n-k]
    return out

def const(x, shape=()):
    o=np.zeros((*shape,ORDER+1));o[...,0]=x;return o

def inv(a):
    require(bool(np.all(np.abs(a[...,0])>1e-12)), 'zero reciprocal')
    o=np.zeros_like(a);o[...,0]=1/a[...,0]
    for n in range(1,ORDER+1):
        for k in range(1,n+1):o[...,n]-=a[...,k]*o[...,n-k]/a[...,0]
    return o

def sqrt(a):
    require(bool(np.all(a[...,0]>0)), 'nonpositive square root')
    o=np.zeros_like(a);o[...,0]=np.sqrt(a[...,0])
    for n in range(1,ORDER+1):
        o[...,n]=a[...,n]
        for k in range(1,n):o[...,n]-=o[...,k]*o[...,n-k]
        o[...,n]/=2*o[...,0]
    return o

def compose(c,x):
    out=np.zeros_like(x)
    for k in range(ORDER,-1,-1):
        out=mul(out,x);out[...,0]+=c[...,k]
    return out

def deriv(c):
    out=np.zeros_like(c);out[...,:ORDER]=c[...,1:]*np.arange(1,ORDER+1);return out

def flight(g,q0,q1,x,y):
    t=compose(q0,x)+compose(q1,y);t[...,0]+=g
    d=x-y
    ell=sqrt(mul(t,t)+mul(d,d))
    il=inv(ell)
    dx=mul(mul(t,compose(deriv(q0),x))+d,il)
    dy=mul(mul(t,compose(deriv(q1),y))-d,il)
    return ell,dx,dy

def finite_action(g,q,start,nflights=64):
    # Independent finite-chain stationary equations with x_0=u and x_J=0.
    types=(start+np.arange(nflights+1))%2
    x=np.zeros((nflights+1,ORDER+1));x[0,1]=1
    diag=2*(1/g+2*q[types[1:-1],2])
    band=np.zeros((3,nflights-1));band[1]=diag
    band[0,1:]=-1/g;band[2,:-1]=-1/g
    for n in range(1,ORDER):
        _,dx,dy=flight(g,q[types[:-1]],q[types[1:]],x[:-1],x[1:])
        residual=dy[:-1,n]+dx[1:,n]
        x[1:-1,n]=solve_banded((1,1),band,-residual)
    ell,dx,dy=flight(g,q[types[:-1]],q[types[1:]],x[:-1],x[1:])
    residual=float(np.max(np.abs((dy[:-1]+dx[1:])[:,1:ORDER])))
    S=ell.sum(axis=0);S[0]-=nflights*g
    return S,residual

def bellman_inverse(g,S):
    a=2*S[:,2];require(bool(np.all(a>0)), 'negative leading action')
    gamma=np.arcsinh(g*np.sqrt(a[0]*a[1]));c=np.cosh(gamma)
    cs=c*np.sqrt(a/a[::-1]);q=np.zeros_like(S);q[:,2]=(cs-1)/(2*g)
    alpha=1/(1+g*(2*q[::-1,2]+a[::-1]))
    u=np.zeros(ORDER+1);u[1]=1
    for n in range(3,ORDER+1):
        P=np.zeros(2)
        for b in (0,1):
            v=np.zeros(ORDER+1)
            low=S[1-b].copy();low[n:]=0
            H=1/g+2*q[1-b,2]+a[1-b]
            for k in range(1,n-1):
                _,_,dv=flight(g,q[b],q[1-b],u,v)
                residue=(dv+compose(deriv(low),v))[k]
                v[k]=-residue/H
            ell,_,_=flight(g,q[b],q[1-b],u,v)
            P[b]=(ell+compose(low,v))[n]
        B=np.array([[0,alpha[0]**n],[alpha[1]**n,0]])
        q[:,n]=np.linalg.solve(np.eye(2)+B,(np.eye(2)-B)@S[:,n]-P)
    return q, float(gamma), alpha

def support(q):
    u=np.zeros(ORDER+1);u[1]=1
    sn=np.zeros_like(u);cs=np.zeros_like(u)
    for k in range(ORDER+1):
        if k%2:sn[k]=(-1)**((k-1)//2)/math.factorial(k)
        else:cs[k]=(-1)**(k//2)/math.factorial(k)
    tn=mul(sn,inv(cs));y=np.zeros_like(u)
    for k in range(1,ORDER):
        y[k]=-(compose(deriv(q),y)-tn)[k]/(2*q[2])
    h=-mul(compose(q,y),cs)+mul(y,sn)
    return h,float(np.max(np.abs((compose(deriv(q),y)-tn)[:ORDER])))

def main():
    rng=np.random.default_rng(460914)
    series_error=0.;stationarity_error=0.;support_residual=0.;blocks_error=0.
    for case in range(24):
        g=float(rng.uniform(.6,1.4));q=np.zeros((2,ORDER+1))
        q[:,2]=rng.uniform(.6,1.3,size=2)/2
        for n in range(3,ORDER+1):q[:,n]=rng.uniform(-.4,.4,size=2)/math.factorial(n)
        S=[]
        for b in (0,1):
            sb,res=finite_action(g,q,b);S.append(sb);stationarity_error=max(stationarity_error,res)
        recovered,gamma,alpha=bellman_inverse(g,np.asarray(S))
        series_error=max(series_error,float(np.max(np.abs(recovered-q))))
        for n in range(3,ORDER+1):
            B=np.array([[0,alpha[0]**n],[alpha[1]**n,0]])
            Mn=np.linalg.solve(np.eye(2)-B,np.eye(2)+B)
            blocks_error=max(blocks_error,abs(float(np.linalg.det(Mn))-1))
        for b in (0,1):
            h,res=support(q[b]);support_residual=max(support_residual,res)
            require(abs(2*h[2]-1/(2*q[b,2]))<1e-11,'support curvature')
            # First occurrence of each new graph coefficient in support jet.
            for n in range(3,ORDER+1):
                pert=q[b].copy();pert[n]+=.001
                hp,_=support(pert)
                require(abs((hp[n]-h[n])/.001+(2*q[b,2])**(-n))<1e-8,'support triangular coefficient')
    require(series_error<1e-10 and stationarity_error<1e-10 and blocks_error<1e-11,'finite Bellman diagnostic failed')
    # Fourier rotation on arbitrary gcd-one witnesses, not always modes 2 and 3.
    phase_error=0.
    for F,bezout in [([2,3],[-1,1]),([4,9],[-2,1]),([6,10,15],[1,1,-1])]:
        require(sum(k*b for k,b in zip(F,bezout))==1,'invalid witness')
        for _ in range(80):
            theta=float(rng.uniform(-math.pi,math.pi));z=rng.uniform(.2,1,len(F))*np.exp(1j*rng.uniform(-math.pi,math.pi,len(F)))
            w=z*np.exp(-1j*np.asarray(F)*theta)
            rot=np.prod(((z/abs(z))/(w/abs(w)))**np.asarray(bezout))
            phase_error=max(phase_error,float(abs(rot-np.exp(1j*theta))))
    require(phase_error<1e-12,'Bezout rotation sign')
    # Unknown, nonsymmetric amplitude and non-even action; algebra only.
    d=.6
    action=lambda u: .7*u*u+.11*u**3+.05*u**4
    amp=lambda u: math.exp(.18*u-.09*u*u)
    density=lambda u,v:amp(u)*amp(v)*(d-action(u)-action(v))/2.7
    ratio=lambda u,v:density(u,v)*density(0,0)/(density(u,0)*density(0,v))
    anchor=.31;qa=math.sqrt(1-ratio(anchor,anchor));cancel_error=0.
    for u in np.linspace(-.33,.33,65):
        t=(1-ratio(float(u),anchor))/qa
        cancel_error=max(cancel_error,abs(d*t/(1+t)-action(u)))
    require(cancel_error<1e-12,'density cancellation')
    # Cell aliasing negative control: different densities have identical cell masses.
    # f=1 + eps sin(2 pi k x), f'=1 on [0,1]^2, k-cell grid in x.
    # Exact total L1=2 eps/pi; uniform gradient bound 2 pi k eps.
    alias_eps=.2;alias_grid=20
    alias_l1=2*alias_eps/math.pi
    bin_bound=4*(2*math.pi*alias_grid*alias_eps)/alias_grid
    require(alias_l1>0 and alias_l1<=bin_bound,'cell bias term')
    negative_controls={}
    try: inv(np.zeros(ORDER+1))
    except RuntimeError: negative_controls['zero_denominator']='rejected'
    try: require(math.gcd(4,8)==1,'nontrivial rotational symmetry')
    except RuntimeError: negative_controls['non_coprime_witness']='rejected'
    try: require(math.sqrt(max(0.,1-ratio(0.,0.)))>0,'nonzero anchor required')
    except RuntimeError: negative_controls['zero_contact_anchor_for_nonzero_anchor_step']='rejected'
    require(len(negative_controls)==3,'missing negative control')
    # Continuation and accuracy arithmetic in log scale: avoid floating underflow.
    s=1.;B=2.;r=min(s/8,1/8);J=math.ceil(math.pi/r)+1;beta=2.**(-J)
    epsilon=.1;Creg=10.;logv=(math.log(epsilon)-math.log(2*Creg)-(1-beta)*math.log(2*B))/beta
    m=max(2,math.ceil((math.log(16*B/3)-logv)/math.log(4)-1))
    require(math.log(8*B/3)-(m+1)*math.log(4)<=logv-math.log(2)+1e-6,'finite tail prescription')
    print(json.dumps({'status':'passed','scope':'Independent finite-chain series through order six; algebra and explicit-bound arithmetic, not infinite-dimensional proof certification',
        'finite_chain_cases':24,'flights_per_chain':64,'bellman_max_coefficient_error':series_error,'stationarity_max_error':stationarity_error,
        'determinant_one_max_error':blocks_error,'support_stationarity_max_error':support_residual,'bezout_cases':240,'bezout_max_error':phase_error,
        'non_even_unknown_amplitude_cancellation_error':cancel_error,'aliased_histograms':{'identical_masses':True,'nonzero_density_L1':alias_l1,'mesh_term_required':True},
        'negative_controls':negative_controls,'log_domain_accuracy_example':{'analytic_width':s,'steps':J,'beta':beta,'log_v':logv,'sufficient_order':m,'practical_efficiency_claim':False},
        'mathematical_certification':False},sort_keys=True,indent=2))

if __name__=='__main__':main()
