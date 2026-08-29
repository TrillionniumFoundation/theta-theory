#!/usr/bin/env python3
from __future__ import annotations
import itertools, json, math
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
errors=[]
checks={}

def req(cond,msg):
    if not cond: errors.append(msg)

def weights(a:float):
    return np.array([(1-a)/6,(1-a)/3,3*(1+a)/14,2*(1+a)/7],dtype=float)

def theta_of_a(a:float):
    return 0.5*math.log(3*(1+a)/(7*(1-a)))

# 1. Quantitative microcanonical finite-window test.
def falling(x,r):
    out=1.0
    for j in range(r): out*=x-j
    return out
n,k,ell=40,27,6
q=k/n
tv=0.0
for pattern in itertools.product([0,1], repeat=ell):
    u=sum(pattern)
    p_hyp=falling(k,u)*falling(n-k,ell-u)/falling(n,ell)
    p_iid=q**u*(1-q)**(ell-u)
    tv += abs(p_hyp-p_iid)
tv*=0.5
bound=sum(r/(n-r) for r in range(ell))
req(tv<=bound+1e-14, f'microcanonical TV bound failed: {tv}>{bound}')
checks['microcanonical_window_tv']={'actual':tv,'bound':bound,'pass':tv<=bound+1e-14}

# 2. One-step theta-HJB expansion for a quadratic test.
a=0.2
th=theta_of_a(a)
w=weights(a)
d=np.array([[2.,0.],[-1.,0.],[0.,4.],[0.,-3.]])
tau=np.array([2.,2.,1.,1.])
p=np.array([0.35,-0.2])
X=np.array([[0.7,0.1],[0.1,-0.4]])
b=np.array([0.15,-0.05])
c=0.3
C=sum(w[i]*np.outer(d[i],d[i]) for i in range(4))
bart=float(np.dot(w,tau))
target=bart*(c+float(b@p))+0.5*float(np.sum(C*X))+0.5*th*float(p@C@p)
errs=[]
for eps in [2e-2,1e-2,5e-3,2.5e-3]:
    vals=[]
    for i in range(4):
        delta=eps*d[i]+eps**2*tau[i]*b
        phi=float(p@delta+0.5*delta@X@delta)
        vals.append(eps**2*tau[i]*c+phi)
    m=max(th*np.array(vals)) if th!=0 else 0.0
    if abs(th)>1e-14:
        op=(m+math.log(float(np.sum(w*np.exp(th*np.array(vals)-m)))))/th
    else:
        op=float(np.dot(w,vals))
    approx=op/eps**2
    errs.append(abs(approx-target))
req(all(errs[i+1]<errs[i] for i in range(len(errs)-1)), f'HJB expansion errors not decreasing: {errs}')
req(errs[-1]<3e-3, f'HJB expansion residual too large: {errs[-1]}')
checks['theta_hjb_expansion']={'target':target,'errors':errs,'pass':not any('HJB expansion' in e for e in errors)}

# 3. Saddle-envelope finite-difference test.
# G(phi,u,v)=log-sum-exp plus strong actuator energies.
w2=np.array([0.45,0.55])
alpha=np.array([0.7,-0.2])
beta=np.array([-0.3,0.5])
th2=0.8
mu=3.0
nu=2.0
phi0=np.array([0.2,-0.1])

def G(phi,u,v):
    z=th2*(phi+alpha*u+beta*v-0.5*mu*u*u+0.5*nu*v*v)
    m=float(np.max(z))
    return (m+math.log(float(np.sum(w2*np.exp(z-m)))))/th2

def derivs(phi,u,v):
    z=th2*(phi+alpha*u+beta*v-0.5*mu*u*u+0.5*nu*v*v)
    m=float(np.max(z)); q=w2*np.exp(z-m); q=q/q.sum()
    au=alpha-mu*u
    bv=beta+nu*v
    Gu=float(q@au); Gv=float(q@bv)
    # Hessian in controls
    Guu=-mu+th2*(float(q@(au*au))-Gu*Gu)
    Gvv=nu+th2*(float(q@(bv*bv))-Gv*Gv)
    Guv=th2*(float(q@(au*bv))-Gu*Gv)
    H=np.array([[Guu,Guv],[Guv,Gvv]])
    return q,np.array([Gu,Gv]),H,au,bv

# Newton solve saddle first-order conditions.
u=v=0.0
for _ in range(30):
    qv,grad,H,au,bv=derivs(phi0,u,v)
    step=np.linalg.solve(H,grad)
    u-=step[0]; v-=step[1]
    if np.linalg.norm(step)<1e-13: break
qv,grad,H,au,bv=derivs(phi0,u,v)
req(np.linalg.norm(grad)<1e-10,'saddle root solve failed')
req(np.linalg.eigvalsh(H)[0]<0<np.linalg.eigvalsh(H)[1],'saddle Hessian signature wrong')
eta=np.array([0.6,-0.4])
zeta=np.array([-0.3,0.8])
# Pure terminal covariance.
mean_eta=float(qv@eta); mean_zeta=float(qv@zeta)
Gpp=th2*(float(qv@(eta*zeta))-mean_eta*mean_zeta)
# G_{z phi}[direction].
B_eta=np.array([
    th2*(float(qv@(au*eta))-float(qv@au)*mean_eta),
    th2*(float(qv@(bv*eta))-float(qv@bv)*mean_eta),
])
B_zeta=np.array([
    th2*(float(qv@(au*zeta))-float(qv@au)*mean_zeta),
    th2*(float(qv@(bv*zeta))-float(qv@bv)*mean_zeta),
])
formula=Gpp-float(B_eta@np.linalg.solve(H,B_zeta))

def value(phi):
    uu,vv=u,v
    for _ in range(30):
        qx,gx,Hx,_,_=derivs(phi,uu,vv)
        st=np.linalg.solve(Hx,gx); uu-=st[0]; vv-=st[1]
        if np.linalg.norm(st)<1e-13: break
    return G(phi,uu,vv)

h=2e-4
fd=(value(phi0+h*eta+h*zeta)-value(phi0+h*eta-h*zeta)-value(phi0-h*eta+h*zeta)+value(phi0-h*eta-h*zeta))/(4*h*h)
req(abs(fd-formula)<2e-5, f'saddle envelope mismatch: fd={fd}, formula={formula}')
checks['saddle_envelope']={'saddle':[u,v],'formula':formula,'finite_difference':fd,'abs_error':abs(fd-formula),'pass':abs(fd-formula)<2e-5}

# 4. Cash-additive exponential certainty equivalent check.
Xvals=np.array([-1.0,0.4,2.0]); probs=np.array([0.2,0.5,0.3]); t=0.7
ce=lambda x:(1/t)*math.log(float(np.sum(probs*np.exp(t*x))))
for shift in [-2.0,0.3,1.5]:
    req(abs(ce(Xvals+shift)-ce(Xvals)-shift)<1e-12,'cash additivity failed')
checks['cash_additivity']={'pass':not any('cash additivity' in e for e in errors)}

result={
    'status':'PASS' if not errors else 'FAIL',
    'checks':checks,
    'errors':errors,
    'scope':'Numerical/algebraic regression only. It does not certify infinite-dimensional analysis, viscosity comparison, or external review.'
}
(ROOT/'status'/'DEEP_VERIFICATION_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
raise SystemExit(1 if errors else 0)
