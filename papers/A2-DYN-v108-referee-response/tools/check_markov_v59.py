#!/usr/bin/env python3
"""Exact coefficients and finite physical-word regressions, not proof certificates."""
from __future__ import annotations
import math
import numpy as np
import sympy as sp
import mpmath as mp


def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def word_arrays(m: int) -> tuple[np.ndarray, ...]:
    P=np.array([[.75,.25],[1/3,2/3]])
    pi=np.array([4/7,3/7])
    state=np.array([0,1],dtype=int);initial=state.copy()
    weights=pi.copy();a=np.ones(2);b=np.zeros(2);count=np.zeros(2)
    xb=np.zeros(2);xa=np.ones(2)
    for _ in range(m):
        old=state
        j=np.tile(np.array([0,1]),len(old));old=np.repeat(old,2)
        initial=np.repeat(initial,2);count=np.repeat(count,2)+j
        weights=np.repeat(weights,2)*P[old,j]
        b=np.where(old==0,0.,P[j,0])+P[j,old]*np.repeat(b,2)
        a=P[j,old]*np.repeat(a,2)
        xb=np.repeat(xb,2)+np.repeat(xa,2)*np.where(j==0,0.,P[old,0])
        xa=np.repeat(xa,2)*P[old,j]
        state=j
    return state,initial,weights,a,b,count,xb,xa


def height(left: np.ndarray,right: np.ndarray,density: np.ndarray,m: int) -> tuple[float,float]:
    valid=(right>left)&(density>0)
    left,right,density=left[valid],right[valid],density[valid]
    points=np.r_[left,right];deltas=np.r_[density,-density]
    order=np.argsort(points,kind='stable');points=points[order];deltas=deltas[order]
    unique,starts=np.unique(points,return_index=True)
    jumps=np.add.reduceat(deltas,starts);levels=np.cumsum(jumps)[:-1]
    if len(levels)==0:return 0.,0.
    levels=np.maximum(levels,0.)*math.sqrt(m)
    mean=24*m/7;var=204/343
    def gaussian(x):return np.exp(-((x-mean)/math.sqrt(m))**2/(2*var))/math.sqrt(2*math.pi*var)
    err=np.maximum(abs(levels-gaussian(unique[:-1])),abs(levels-gaussian(unique[1:])))
    inside=(unique[:-1]<=mean)&(unique[1:]>=mean)
    err[inside]=np.maximum(err[inside],abs(levels[inside]-gaussian(mean)))
    return float(levels.max()),float(err.max())


def finite_checks() -> dict:
    P=sp.Matrix([[sp.Rational(3,4),sp.Rational(1,4)],[sp.Rational(1,3),sp.Rational(2,3)]])
    pi=sp.Matrix([[sp.Rational(4,7),sp.Rational(3,7)]])
    require(pi*P==pi,'stationary probability')
    for i in range(2):
        for j in range(2):require(pi[i]*P[i,j]==pi[j]*P[j,i],'detailed balance')
    s,t=sp.symbols('s t');tr=sp.Rational(3,4)+sp.Rational(2,3)*sp.exp(s+t)
    det=sp.Rational(1,2)*sp.exp(s+t)-sp.Rational(1,12)*sp.exp(s)
    C=sp.log((tr+sp.sqrt(tr**2-4*det))/2)
    at={s:0,t:0}
    cov=sp.Matrix(2,2,lambda i,j:sp.simplify(sp.diff(C,(s,t)[i],(s,t)[j]).subs(at)))
    expected=sp.Matrix([[204,192],[192,198]])/343
    require(cov==expected,'joint pressure covariance')
    require(sp.simplify(cov.det())==sp.Rational(72,2401),'covariance determinant')
    residual=sp.simplify(cov[1,1]-cov[0,1]**2/cov[0,0])
    require(residual==sp.Rational(6,119),'optimized damping variance')
    third=[sp.simplify(sp.diff(C,s,3-i,t,i).subs(at)) for i in range(3)]
    require(third==[sp.Rational(4908,16807),sp.Rational(9600,16807),sp.Rational(14016,16807)],'third cumulants')
    w1=-sp.Rational(32,17)*sp.pi;w2=2*sp.pi
    drift=sp.simplify(-(third[0]*w1*w1+2*third[1]*w1*w2+third[2]*w2*w2)/2)
    require(drift==-sp.Rational(3456,99127)*sp.pi**2,'centered drift sign/coefficient')
    for r in range(8):
        c=pi[1]*(P**r)[1,1]-pi[1]**2
        require(sp.simplify(c-sp.Rational(12,49)*sp.Rational(5,12)**r)==0,'non-independent state covariance')
    require(cov[0,0]!=sp.Rational(12,49),'iid-variance negative control')
    cases=[]
    for m in [1,2,4,8,12]:
        state,initial,weights,a,b,count,xb,xa=word_arrays(m)
        require(abs(weights.sum()-1)<1e-12,'complete word mass')
        require(np.all(a<=.75**m+1e-13) and np.all(b>=-1e-13) and np.all(b+a<=1+1e-12),'stable coarea bounds')
        for j in range(2):
            mask=state==j;order=np.argsort(b[mask]);bs=b[mask][order];aa=a[mask][order]
            require(abs(bs[0])<1e-12 and abs(bs[-1]+aa[-1]-1)<1e-12,'cylinder endpoints')
            require(np.max(abs(bs[1:]-(bs+aa)[:-1]),initial=0)<1e-12,'stable cylinder partition')
            require(np.max(abs(weights[mask]-np.array([4/7,3/7])[j]*a[mask]))<1e-12,'suffix cylinder weights')
        left=3*m+count+b+a-1;right=3*m+count+b;dens=weights/(1-a)
        mass=float(np.dot(dens,right-left));mean=float(np.dot(weights,(left+right)/2))
        require(abs(mass-1)<1e-11 and abs(mean-24*m/7)<1e-10,'raw roof normalization')
        h,e=height(left,right,dens,m)
        layers={}
        for width in [.1,.01]:
            lo=np.r_[right-(1-a)*width,left]
            hi=np.r_[right,left+(1-a)*width]
            dd=np.r_[dens,dens]
            hh,_=height(lo,hi,dd,m)
            require(abs(np.dot(dd,hi-lo)-2*width)<1e-10,'initial-age source mass')
            layers[str(width)]=hh
        cases.append({'m':m,'words':len(weights),'mass':round(mass,12),'mean':round(mean,12),
                      'normalized_height':round(h,10),'normalized_density_error':round(e,10),
                      'age_source_heights':layers})
        if m==1:require(abs(np.dot(weights,right-left)-1)>1e-2,'omitted coarea Jacobian negative control')
    for r in [sp.Rational(i,19) for i in range(-38,39)]:
        total=sum(max(sp.Rational(0),1-abs(r-k)) for k in range(-5,6))
        require(total==1,'triangle periodization')
    H=np.array([[2+1j,.2+.1j],[.2+.1j,1.5+.4j]])
    inv=np.linalg.inv(H);rhs=inv.conj().T@H.real@inv
    require(np.max(abs(inv.real-rhs))<1e-12,'Hermitian inverse identity')
    require(np.min(np.linalg.eigvalsh(inv.real))>0,'accretive inverse positivity')
    require(np.max(abs(inv@H.real@inv-inv.real))>1e-3,'unconjugated identity negative control')
    mp.mp.dps=60;peak=[]
    for eps in [mp.mpf('0.01'),mp.mpf('0.001')]:
        def psi(z):
            trace=mp.mpf(3)/4+mp.mpf(2)/3*mp.exp(1j*z*(1+eps))
            determinant=mp.mpf(1)/2*mp.exp(1j*z*(1+eps))-mp.mpf(1)/12*mp.exp(1j*z)
            lam=(trace+mp.sqrt(trace*trace-4*determinant))/2
            return mp.log(lam)-1j*z*(mp.mpf(3)/7+2*eps/7)
        center=mp.findroot(lambda z:mp.re(mp.diff(psi,z)),2*mp.pi-32*mp.pi*eps/17)
        damping=-mp.re(psi(center));v=mp.im(mp.diff(psi,center))
        require(damping>0,'damped Markov peak')
        require(abs(damping/eps**2-12*mp.pi**2/119)<mp.mpf('.04'),'damping expansion finite check')
        require(abs(v/eps**2+3456*mp.pi**2/99127)<mp.mpf('.03'),'drift expansion finite check')
        peak.append({'epsilon':str(eps),'center':mp.nstr(center,20),'damping':mp.nstr(damping,20),
                     'drift':mp.nstr(v,20),'squared_drift_over_damping':mp.nstr(v*v/damping,20)})
    return {'joint_covariance':[[str(x) for x in row] for row in cov.tolist()],
      'residual_variance':str(residual),'drift_coefficient':str(drift),
      'finite_words':cases,'peak_diagnostics':peak,'triangle_cases':77,'negative_controls':3,
      'continuous_density_and_Lorentz_height_proofs_not_certified_by_tests':True}

if __name__=='__main__':
    import json
    print(json.dumps(finite_checks(),indent=2,sort_keys=True))
