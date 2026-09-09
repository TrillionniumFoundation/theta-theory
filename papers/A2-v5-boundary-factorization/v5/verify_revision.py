#!/usr/bin/env python3
"""Independent finite v5 diagnostics: no repository implementation imports.

Exact identities and ordinary/high-precision non-interval calculations are
reported separately. These checks are not certificates for continuum theorems.
Run normally and with python -O; explicit exceptions enforce every check.
"""
from __future__ import annotations
import json
import math
import platform
from collections import Counter
import numpy as np
import sympy as sp
import mpmath as mp
from scipy.linalg import solve_banded

CHECKS: list[dict] = []
def require(ok, name: str, kind: str, value=None) -> None:
    if not bool(ok):
        raise RuntimeError(f'{kind}: {name}: {value}')
    out={'name':name,'kind':kind,'passed':True}
    if value is not None: out['value']=value
    CHECKS.append(out)

def exact() -> None:
    c,q,z,h,t,v,b=sp.symbols('c q z h t v b', positive=True)
    gs=[sp.Integer(1),1/(2*c),1/(4*c*c-1),1/(4*c*(2*c*c-1))]
    M=sp.Matrix([[sp.diff(f,c,k) for k in range(1,4)] for f in gs[1:]])
    poly=64*c**8+32*c**6+116*c**4+4*c**2+1
    wr=12*poly/(c**4*(4*c*c-1)**4*(2*c*c-1)**4)
    require(sp.factor(M.det()-wr)==0,'rational four-amplitude Wronskian','exact')
    det=-sp.Rational(3,2)*q**3*wr/(c*c-1)**2
    expected=-18*q**3*poly/((c*c-1)**2*c**4*(4*c*c-1)**4*(2*c*c-1)**4)
    require(sp.factor(det-expected)==0,'full collision Jacobian','exact')
    for point in [sp.Rational(6,5),sp.Rational(3,2),sp.Integer(2),sp.Integer(3),sp.Integer(5)]:
        require(det.subs({c:point,q:2})<0,f'nonzero Jacobian at c={point}','exact')
    e1,e2,e3=sp.symbols('e1 e2 e3')
    powers=[sp.Integer(3),e1,e1**2-2*e2,e1**3-3*e1*e2+3*e3]
    for k in range(4,10): powers.append(sp.expand(e1*powers[-1]-e2*powers[-2]+e3*powers[-3]))
    for k in range(1,10):
        grad=[sp.diff(powers[k],x).subs({e1:0,e2:0,e3:0}) for x in [e1,e2,e3]]
        want={1:[1,0,0],2:[0,-2,0],3:[0,0,3]}.get(k,[0,0,0])
        require(grad==want,f'Newton linear terms power={k}','exact')
    g,r=sp.symbols('g r',positive=True)
    phi=r/sp.sqrt(g*(g+2*r))
    require(sp.simplify(sp.diff(phi,r,3)-3*(3*g+r)/(sp.sqrt(g)*(g+2*r)**sp.Rational(7,2)))==0,'cubic physical-path derivative','exact')
    require((36**3+2*(-18)**3)//3==11664,'two-sided cubic multiplicity coefficient','exact')
    require(sp.simplify((-g*g*c*c/(12*(c*c-1)**2)).subs({g:1,c:2})*(-24)-sp.Rational(8,9))==0,'one-flight shape derivative 8/9','exact')
    require(sp.simplify((-sp.Rational(9,1)/(12*3*4*sp.sqrt(3)))*(-24)-sp.sqrt(3)/2)==0,'half-line shape derivative sqrt(3)/2','exact')
    # Exact integrals in a radial latent toy density 1+b*d*|z|^2.
    s,d,a=sp.symbols('s d a',positive=True)
    mass=sp.integrate((1-s)*(1+b*d*s),(s,0,1))
    eta=sp.integrate((1-s)**2*(1+b*d*s)/2,(s,0,1))/mass
    D=sp.cancel(3*eta)
    V=sp.cancel(sp.integrate(s*(1-s)*(1+b*d*s),(s,0,1))/(a*mass))
    T=sp.cancel(V/D)
    require(sp.simplify(D-(1+b*d/4)/(1+b*d/3))==0,'residual-time latent mean','exact')
    require(sp.simplify(T-(1+b*d/2)/(3*a*(1+b*d/4)))==0,'self-normalized latent ratio','exact')
    for m in range(1,9):
        ws=[(-1)**(l-1)*sp.binomial(m,l) for l in range(1,m+1)]
        require(sum(ws)==1,f'weights sum m={m}','exact')
        for k in range(1,m):
            require(sum(w*l**k for l,w in enumerate(ws,1))==0,f'offset cancellation m={m} k={k}','exact')
        require(sum(w/sp.Integer(l) for l,w in enumerate(ws,1))==sp.harmonic(m),f'harmonic identity m={m}','exact')
        old=sum(w*(1-t/(l*h))*v for l,w in enumerate(ws,1))
        require(sp.simplify(sp.diff(old,t).subs(t,0)+v*sp.harmonic(m)/h)==0,f'programmed timing singularity m={m}','exact')
        # Any polynomial of degree <m is extrapolated at the shifted point -t.
        pp=sum(d**k for k in range(m))
        shifted=sum(w*pp.subs(d,l*h-t) for l,w in enumerate(ws,1))
        require(sp.expand(shifted-pp.subs(d,-t))==0,f'smooth shifted normalization m={m}','exact')
    # Exact cofactor identity for a variable rational nearest-neighbor Hessian.
    for N in range(1,9):
        full=sp.zeros(N+1)
        bs=[]
        for i in range(N):
            bi=sp.Rational(7+i,7); ai=sp.Rational(5+i,9); di=sp.Rational(8+i,11)
            bs.append(bi)
            full[i,i]+=bi+ai; full[i+1,i+1]+=bi+di
            full[i,i+1]-=bi; full[i+1,i]-=bi
        ends=[0,N]
        if N==1:
            S=full; hd=sp.Integer(1)
        else:
            H=full[1:N,1:N]; C=full.extract(ends,list(range(1,N)))
            S=full.extract(ends,ends)-C*H.inv()*C.T; hd=H.det()
        require(sp.factor(-S[0,1]-sp.prod(bs)/hd)==0,f'variable-chain exact cofactor length={N}','exact')

def coefficients(indices):
    i=np.asarray(indices,dtype=float)
    return (1+.18*np.sin(np.sqrt(2)*i), .65+.09*np.cos(np.sqrt(3)*i),
            .72+.08*np.sin(np.sqrt(5)*i), .22*np.sin(.7+i),
            .17*np.cos(1.1+i), .7+.1*np.cos(.4*i), .8+.1*np.sin(.8*i))

def finite_chain(m: int,n: int,u: float,v: float) -> dict:
    N=n-m; bs,aa,dd,tl,tr,ql,qr=coefficients(np.arange(m,n))
    y=np.zeros(N+1); y[0]=u;y[-1]=v
    diag0=bs[:-1]+bs[1:]+dd[:-1]+aa[1:]
    cubic=tr[:-1]+tl[1:];quartic=qr[:-1]+ql[1:];off=-bs[1:-1]
    for _ in range(30):
        if N==1:break
        x=y[1:-1]
        grad=diag0*x-bs[:-1]*y[:-2]-bs[1:]*y[2:]+cubic*x*x/2+quartic*x**3/6
        if np.max(abs(grad))<2e-16: break
        diag=diag0+cubic*x+quartic*x*x/2
        ab=np.zeros((3,N-1));ab[1]=diag
        if N>2:ab[0,1:]=off;ab[2,:-1]=off
        y[1:-1]-=solve_banded((1,1),ab,grad)
    else:raise RuntimeError('Newton failed')
    x=y[1:-1];diag=diag0+cubic*x+quartic*x*x/2
    if N>1:
        grad=diag0*x-bs[:-1]*y[:-2]-bs[1:]*y[2:]+cubic*x*x/2+quartic*x**3/6
        if np.max(abs(grad))>2e-14:raise RuntimeError('Stationarity residual')
    ll=bs*(y[1:]-y[:-1])**2/2+aa*y[:-1]**2/2+dd*y[1:]**2/2
    ll+=tl*y[:-1]**3/6+tr*y[1:]**3/6+ql*y[:-1]**4/24+qr*y[1:]**4/24
    logdet=0.;last=last0=0.
    for i in range(N-1):
        pv=diag[i]-(off[i-1]**2/last if i else 0)
        pv0=diag0[i]-(off[i-1]**2/last0 if i else 0)
        if min(pv,pv0)<=0:raise RuntimeError('Nonpositive LDL pivot')
        logdet+=math.log(pv/pv0);last,last0=pv,pv0
    return {'action':float(ll.sum()),'log_amplitude':-logdet,'max_coordinate':float(max(abs(y)))}

def floating() -> list[dict]:
    out=[]
    for m in [-7,0,9]:
        errs=[]
        for N in [4,8,12,20]:
            u,v=.06,-.04;n=m+N
            f=finite_chain(m,n,u,v)
            lp=finite_chain(m,m+128,u,0)
            rm=finite_chain(n-128,n,0,v)
            lp2=finite_chain(m,m+192,u,0)
            rm2=finite_chain(n-192,n,0,v)
            da=abs(f['action']-lp['action']-rm['action'])
            db=abs(f['log_amplitude']-lp['log_amplitude']-rm['log_amplitude'])
            require(max(abs(lp['action']-lp2['action']),abs(rm['action']-rm2['action']))<1e-14,f'half-line action cutoff m={m} N={N}','float_noninterval')
            require(max(abs(lp['log_amplitude']-lp2['log_amplitude']),abs(rm['log_amplitude']-rm2['log_amplitude']))<1e-13,f'half-line twist cutoff m={m} N={N}','float_noninterval')
            require(da<.02*.8**N and db<.05*.8**N+2e-14,f'variable nonlinear chain m={m} N={N}','float_noninterval',{'action_error':da,'log_twist_error':db})
            errs.append((da,db))
            out.append({'left_site':m,'length':N,'action_error':da,'log_twist_error':db,'half_line_cutoffs':[128,192]})
        require(max(errs[-1])<1e-6*max(errs[0])+1e-13,f'long versus short comparison m={m}','float_noninterval')
    return out

def precision() -> list[dict]:
    mp.mp.dps=70;R=mp.mpf('0.25');g=1-2*R;A0=mp.sqrt(3)/2-mp.pi*R**2;alpha=mp.mpf('.4')
    out=[]
    def amp(s,j):
        radii=[R+36*s,R-18*s,R-18*s]
        return sum(1/mp.sinh(j*mp.acosh(1+g/r)) for r in radii)/(A0+45*mp.pi*s*s/4)
    phi3=3*(3*g+R)/(mp.sqrt(g)*(g+2*R)**mp.mpf('3.5'))
    cubic=11664*phi3/A0
    for st in ['0.0001','0.00005','0.000025','0.00001']:
        s=mp.mpf(st)
        cs=[abs(amp(s,j)-amp(-s,j)) for j in range(1,65)]
        finite=max(cs[:4]);norm=max(mp.exp(alpha*j)*cs[j-1] for j in range(1,65))
        ks=sorted([1/(R+36*s),1/(R-18*s),1/(R-18*s)])
        kt=sorted([1/(R-36*s),1/(R+18*s),1/(R+18*s)])
        dist=max(abs(x-y) for x,y in zip(ks,kt))
        match=36*s/(R*R-324*s*s)
        require(abs(dist-match)<mp.mpf('1e-65'),f'physical sorted matching s={st}','high_precision_noninterval')
        require(abs(cs[0]/s**3/cubic-1)<mp.mpf('.003'),f'physical cubic coefficient s={st}','high_precision_noninterval')
        require(mp.mpf('1e4')<norm/s**3<mp.mpf('1e6'),f'weighted prefix cubic scale s={st}','high_precision_noninterval')
        out.append({'s':st,'four_amplitudes_over_s3':mp.nstr(finite/s**3,20),'weighted_prefix_over_s3':mp.nstr(norm/s**3,20),'curvature_distance_over_s':mp.nstr(dist/s,20),'prefix':64,'digits':70})
    return out

def main() -> None:
    exact();chains=floating();paths=precision()
    print(json.dumps({'status':'PASS','total_checks':len(CHECKS),'counts':dict(sorted(Counter(x['kind'] for x in CHECKS).items())),
      'checks':CHECKS,'variable_chain_comparisons':chains,'physical_two_sided_path':paths,
      'environment':{'python':platform.python_version(),'numpy':np.__version__,'sympy':sp.__version__,'mpmath':mp.__version__},
      'limitations':['Finite diagnostics are not continuum or formal proof certificates.',
        'The nonperiodic chain test uses a specified polynomial chain, not a full equilibrium billiard simulation.',
        'Half-lines are approximated at two finite cutoffs; no infinite matrix is numerically certified.',
        'The sequence test covers 64 coefficients, not the whole sequence.',
        'The residual normalization integral check is an exact radial toy model; the physical theorem rests on the written Morse-coordinate proof.',
        'No interval arithmetic, sensor-noise experiment, minimax lower bound, or independent referee acceptance is claimed.']},indent=2,sort_keys=True))
if __name__=='__main__':main()
