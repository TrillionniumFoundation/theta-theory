#!/usr/bin/env python3
"""Finite regressions for A2 v96; these are not mathematical proof verification."""
from __future__ import annotations
import argparse
import itertools
import json
from pathlib import Path
import numpy as np
from scipy.optimize import nnls


def model(r=.6, s=.2, alpha=.4, u=(1/3, 1/3), v=(.25, .75), floor=.1):
    return dict(r=r, s=s, alpha=alpha, u=np.array(u, float), v=np.array(v, float),
                floor=floor, T=np.array([1.2, 1.4, 1.6, 1.8, 2., 2.5, 3.]),
                w=np.full(7, 1/7), D=1.)


def columns(x):
    return np.vstack((x, 1-np.asarray(x)))


def observation(m, f_roots=None, g_roots=None):
    T, r, s = m['T'], m['r'], m['s']
    f = T*(T-r)**2 if f_roots is None else np.prod(T[:, None]-f_roots, axis=1)
    g = (T-s)**3 if g_roots is None else np.prod(T[:, None]-g_roots, axis=1)
    U, V, alpha = columns(m['u']), columns(m['v']), m['alpha']
    K = alpha*f[:, None, None]*np.outer(U[:, 0], V[:, 0]) + (1-alpha)*g[:, None, None]*np.outer(U[:, 1], V[:, 1])
    return K/(alpha*f+(1-alpha)*g)[:, None, None]


def score(m, jet):
    a,b,c,da,du1,du2,dv1,dv2,X,Y = np.asarray(jet, float)
    T,r,s,alpha = m['T'],m['r'],m['s'],m['alpha']
    gamma=1-alpha; U,V=columns(m['u']),columns(m['v']); P=observation(m)
    f=T*(T-r)**2; g=(T-s)**3; q=alpha*f+gamma*g
    pf=-a*(T-r)**2-b*T*(T-r)-X*T; pg=-c*(T-s)**2-Y*(T-s)
    u1,u2,v1,v2=U[:,0],U[:,1],V[:,0],V[:,1]
    d=lambda x: np.array([x,-x])
    A1=np.outer(u1,v1); A2=np.outer(u2,v2)
    dk=alpha*pf[:,None,None]*A1+gamma*pg[:,None,None]*A2
    dk+=f[:,None,None]*(da*A1+alpha*np.outer(d(du1),v1)+alpha*np.outer(u1,d(dv1)))
    dk+=g[:,None,None]*(-da*A2+gamma*np.outer(d(du2),v2)+gamma*np.outer(u2,d(dv2)))
    dq=alpha*pf+gamma*pg+da*(f-g)
    return (dk-P*dq[:,None,None])/q[:,None,None]


def fisher_data(m):
    P=observation(m); W=(m['w'][:,None,None]/P).ravel()
    S=np.column_stack([score(m, e).ravel() for e in np.eye(10)])
    L=S[:,1:8]; D=S[:,[0,8,9]]
    WL=np.sqrt(W)[:,None]*L; WD=np.sqrt(W)[:,None]*D
    sv=np.linalg.svd(WL, compute_uv=False)
    assert sv[-1] > 1e-12*sv[0], ('free score rank is numerically unresolved', sv)
    O,_=np.linalg.qr(WL,mode='reduced'); R=WD-O@(O.T@WD)
    return S,W,L,D,R,R.T@R,sv


def active_value(Q, target, tol=1e-9):
    other=[j for j in range(3) if j!=target]; candidates=[]
    scale=max(float(np.max(np.abs(Q))),1e-30)
    for n in range(3):
        for A in itertools.combinations(other,n):
            A=list(A); x=np.zeros(3)
            if A:
                G=Q[np.ix_(A,A)]
                if np.linalg.eigvalsh(G)[0] <= 1e-12*scale: continue
                x[A]=np.linalg.solve(G,-Q[A,target])
                if min(x[A]) < -tol: continue
            residual=Q[:,target]+Q@x
            if any(residual[j] < -tol*scale for j in other if j not in A): continue
            value=Q[target,target]+2*Q[target]@x+x@Q@x
            candidates.append((float(value),A,x))
    if not candidates: raise AssertionError('no numerically admissible support')
    return min(candidates,key=lambda a:a[0])


def identify(m):
    r,s,D,alpha=m['r'],m['s'],m['D'],m['alpha']
    A=(r+3*s)*(2*r-3*s)**2; B=(3*D-r)*s-2*r*D
    E=(1-alpha)*A-4*m['floor']*r**3
    return bool(abs(m['u'][0]-m['u'][1])>1e-14 or B<0 or E<0), (A,B,E)


def realizing_model(m,jet,t,Zsign=1):
    a,b,c,da,du1,du2,dv1,dv2,X,Y=jet
    out={**m,'alpha':m['alpha']+t*da,
         'u':m['u']+t*np.array([du1,du2]),'v':m['v']+t*np.array([dv1,dv2])}
    h=np.sqrt(max(Y,0)/3)
    ys=np.array([-2*h,h,h]) if Zsign==1 else np.array([-h,-h,2*h])
    fr=np.array([t*a,m['r']+t*b/2-np.sqrt(t*max(X,0)),m['r']+t*b/2+np.sqrt(t*max(X,0))])
    gr=m['s']+t*c/3+np.sqrt(t)*ys
    assert np.min(fr)>=-1e-12 and np.max(fr)<=m['D'] and np.min(gr)>=0 and np.max(gr)<=m['D']
    assert m['floor']<out['alpha']<1-m['floor']
    assert np.min(out['u'])>0 and np.max(out['u'])<1 and np.min(out['v'])>0 and np.max(out['v'])<1
    return out,fr,gr


def numerical_checks():
    cases=[model(),model(u=(.27,.48)),
           model(r=.9,s=.86,alpha=.75,floor=.2),
           model(r=.9,s=.88,alpha=.75,floor=.2,u=(.3,.5))]
    assert all(identify(m)[0] for m in cases)
    assert not identify(model(r=.9,s=.88,alpha=.75,floor=.2))[0]
    rows=[]
    for m in cases:
        S,W,L,D,R,Q,sv=fisher_data(m)
        vals=[]
        for target in (1,2):
            val,A,x=active_value(Q,target)
            other=[j for j in range(3) if j!=target]
            opt,res=nnls(R[:,other],-R[:,target],maxiter=1000)
            expected=res**2
            assert abs(val-expected)<=2e-7*max(expected,1e-25),(val,expected)
            assert val>0
            vals.append(val)
        kx,ky=vals; C=max(np.sqrt(2)*kx**(-.25),2*np.sqrt(2/3)*ky**(-.25))
        rows.append(dict(r=m['r'],s=m['s'],U_rank=1 if m['u'][0]==m['u'][1] else 2,
                         identification_signs=list(identify(m)[1]),kappa_x=kx,kappa_y=ky,C=C,
                         dominant='double' if 9*ky>=16*kx else 'triple',
                         free_score_singular_values=sv.tolist()))
    # A fixed feasible jet, checked at changing channel rank.
    jet=np.array([.1,.03,-.02,.04,.015,-.01,.02,-.03,.2,.3])
    errors=[]
    for d in (0.,.001,.01,.1):
        m=model(u=(1/3,1/3+d)); S=score(m,jet); P=observation(m)
        for t in (1e-4,1e-5,1e-6):
            alt,fr,gr=realizing_model(m,jet,t)
            PP=observation(alt,fr,gr)
            err=float(np.max(np.abs(PP-P-t*S))/t**1.5)
            assert err<10
            hw=np.sqrt(np.sum(m['w'][:,None,None]*(np.sqrt(PP)-np.sqrt(P))**2))
            norm=np.sqrt(np.sum(m['w'][:,None,None]*S*S/P))
            assert abs(hw-.5*t*norm)<10*t**1.5
            errors.append(err)
    # Exact stochastic pencil transformation at a nonidentified datum.
    m=model(r=.9,s=.88,alpha=.75,floor=.2)
    A,B,E=identify(m)[1]; cstar=4*m['r']**3/A
    V=columns(m['v']); gamma=1-m['alpha']; c=cstar
    beta1=m['alpha']*V[:,0]+gamma*(1-1/c)*V[:,1]
    beta2=gamma*V[:,1]/c
    T=m['T']; f=T*(T-m['r'])**2; g=(T-m['s'])**3; h=(1-c)*f+c*g
    old=m['alpha']*f[:,None]*V[:,0]+gamma*g[:,None]*V[:,1]
    new=f[:,None]*beta1+h[:,None]*beta2
    assert np.max(abs(old-new))<1e-13 and min(sum(beta1),sum(beta2))>=m['floor']
    # Two reflected extreme triples have equal variance but opposite product.
    h=.7; yy=np.array([[-2*h,h,h],[-h,-h,2*h]])
    assert np.allclose(yy.sum(axis=1),0) and np.allclose((yy**2).sum(axis=1),6*h*h)
    assert np.isclose(np.max(abs(yy[0]-yy[1])),2*h)
    return dict(cases=rows,score_remainder_max=max(errors),score_remainder_checks=len(errors),
                active_set_nnls_comparisons=8,stochastic_fibre_identity=True,triple_diameter_identity=True)


def symbolic_checks():
    import sympy as sp
    z,r,s,c,D,aa=sp.symbols('z r s c D aa')
    f=z*(z-r)**2; g=(z-s)**3; h=(1-c)*f+c*g
    A=(r+3*s)*(2*r-3*s)**2
    assert sp.factor(sp.discriminant(h,z)-c*(c-1)**2*(r-s)**3*(A*c-4*r**3))==0
    assert sp.expand(A-(4*r**3-27*s**2*(r-s)))==0
    RR=f/g
    assert sp.factor(sp.diff(RR,z)/RR-((2*r-3*s)*z+r*s)/(z*(z-r)*(z-s)))==0
    assert sp.factor((D-r)*(2*r*D/(3*D-r)-2*r/3)/(D-r)-2*r*r/(3*(3*D-r)))==0
    return dict(discriminant=True,threshold_polynomial=True,pencil_derivative=True,strict_geometric_margin=True)


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output',type=Path,default=Path('v96_math_diagnostics.json'))
    args=ap.parse_args()
    result=dict(scope='finite regressions, not proof verification',symbolic=symbolic_checks(),numeric=numerical_checks())
    args.output.parent.mkdir(parents=True,exist_ok=True); args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
