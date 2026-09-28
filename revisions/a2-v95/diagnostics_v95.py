#!/usr/bin/env python3
"""Finite regression checks for A2 v95; not proof verification.

Run from the paper directory. Requires numpy, scipy and sympy.
Uses exact symbolic identities and finite numerical tests of the formulas
printed in the manuscript. No network access or repository writes.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import numpy as np
import sympy as sp
from scipy.optimize import nnls


def score_matrix(r: float, s: float, alpha: float, u: np.ndarray,
                 V: np.ndarray, clocks: np.ndarray, w: np.ndarray):
    """Columns: a,b,c,dalpha,du1,du2,dv1,dv2,X,Y."""
    f = clocks*(clocks-r)**2
    g = (clocks-s)**3
    gamma = 1-alpha
    q = alpha*f+gamma*g
    A1 = alpha*np.outer(u, V[:, 0])
    A2 = gamma*np.outer(u, V[:, 1])
    P = (f[:, None, None]*A1+g[:, None, None]*A2)/q[:, None, None]
    columns = []
    e = np.array([1., -1.])
    for i in range(10):
        v = np.eye(10)[i]
        a,b,c,da,du1,du2,dv1,dv2,X,Y = v
        pf = -a*(clocks-r)**2-b*clocks*(clocks-r)-X*clocks
        pg = -c*(clocks-s)**2-Y*(clocks-s)
        dA1 = (da*np.outer(u,V[:,0])+alpha*du1*np.outer(e,V[:,0])
               +alpha*dv1*np.outer(u,e))
        dA2 = (-da*np.outer(u,V[:,1])+gamma*du2*np.outer(e,V[:,1])
               +gamma*dv2*np.outer(u,e))
        dK = (pf[:,None,None]*A1+pg[:,None,None]*A2
              +f[:,None,None]*dA1+g[:,None,None]*dA2)
        dq = alpha*pf+gamma*pg+da*(f-g)
        score = (dK-P*dq[:,None,None])/q[:,None,None]
        columns.append(score.reshape(-1))
    S = np.stack(columns, axis=1)
    fisher_weights = (w[:,None,None]/P).reshape(-1)
    return S, np.sqrt(fisher_weights)[:,None]*S, P


def root_arc(v: np.ndarray, t: float, r: float, s: float, alpha: float,
             u: np.ndarray, V: np.ndarray, clocks: np.ndarray,
             shape: np.ndarray | None = None):
    a,b,c,da,du1,du2,dv1,dv2,X,Y = v
    if min(a,X,Y) < -1e-12:
        raise ValueError('Infeasible arc')
    if shape is None:
        shape=np.array([-np.sqrt(Y),0.,np.sqrt(Y)])
    if not (abs(np.sum(shape))<1e-9 and abs(shape@shape/2-Y)<1e-8):
        raise ValueError('Invalid triple shape')
    roots1=np.array([t*a,r-np.sqrt(t*X)+t*b/2,r+np.sqrt(t*X)+t*b/2])
    roots2=s+np.sqrt(t)*shape+t*c/3
    aa=alpha+t*da
    e=np.array([1.,-1.])
    uu=np.column_stack([u+t*du1*e,u+t*du2*e])
    vv=V+t*np.column_stack([dv1*e,dv2*e])
    f=np.prod(clocks[:,None]-roots1,axis=1)
    g=np.prod(clocks[:,None]-roots2,axis=1)
    q=aa*f+(1-aa)*g
    P=(f[:,None,None]*aa*np.outer(uu[:,0],vv[:,0])
       +g[:,None,None]*(1-aa)*np.outer(uu[:,1],vv[:,1]))/q[:,None,None]
    return P,roots1,roots2


def run_checks() -> dict:
    z,r,s,c=sp.symbols('z r s c')
    f=z*(z-r)**2; g=(z-s)**3; h=(1-c)*f+c*g
    expected=c*(c-1)**2*(r-s)**3*((r+3*s)*(2*r-3*s)**2*c-4*r**3)
    assert sp.expand(sp.discriminant(h,z)-expected)==0
    R=f/g
    ratio=((2*r-3*s)*z+r*s)/(z*(z-r)*(z-s))
    assert sp.cancel(sp.diff(R,z)/R-ratio)==0
    zs=r*s/(3*s-2*r); cs=4*r**3/((r+3*s)*(2*r-3*s)**2)
    assert sp.factor(h.subs(c,cs).subs(z,zs))==0
    assert sp.factor(sp.diff(h,z).subs(c,cs).subs(z,zs))==0
    symbolic={'discriminant':'pass','ratio_derivative':'pass','double_root':'pass'}

    # Check the classification at a finite grid away from discriminant walls.
    total=0
    for rr in (.3,.6,.9):
        for frac in (.25,.55,.7,.85,.97):
            ss=frac*rr
            p0=np.poly([0,rr,rr]); p1=np.poly([ss,ss,ss])
            for cc in (-.5,.2,.8,1.2,2.,5.,20.,200.):
                roots=np.roots((1-cc)*p0+cc*p1)
                actual=np.max(abs(roots.imag))<1e-6 and min(roots.real)>-1e-7 and max(roots.real)<1+1e-7
                predicted=False
                if ss>2*rr/3:
                    star=rr*ss/(3*ss-2*rr)
                    if star<=1:
                        cstar=4*rr**3/((rr+3*ss)*(2*rr-3*ss)**2)
                        RD=(1-rr)**2/(1-ss)**3
                        cd=RD/(RD-1)
                        predicted=cstar<=cc<=cd
                assert bool(actual)==bool(predicted), (rr,ss,cc,roots,predicted)
                total+=1

    rr=.6; ss=.4; alpha=.55
    u=np.array([.4,.6]); V=np.array([[.75,.25],[.25,.75]])
    clocks=np.linspace(1.1,2.3,7); w=np.ones(7)/7
    S,W,P=score_matrix(rr,ss,alpha,u,V,clocks,w)
    free=[1,2,3,4,5,6,7]
    L=W[:,free]
    def project(x):
        return x-L@np.linalg.lstsq(L,x,rcond=1e-12)[0]
    p0,px,py=[project(W[:,i]) for i in (0,8,9)]
    assert np.linalg.norm(p0)>1e-9
    def J(X,Y):
        zz=X*px+Y*py
        return float(zz@zz-min(0.,p0@zz)**2/(p0@p0))
    for X,Y in [(0,1),(1,0),(.3,.7),(1.2,.8)]:
        an=max(0.,-p0@(X*px+Y*py)/(p0@p0))
        nn,rnorm=nnls(p0[:,None],-(X*px+Y*py))
        assert abs(an-nn[0])<1e-6
        assert np.isclose(J(X,Y),rnorm*rnorm,rtol=1e-6,atol=1e-20)
    cone_x,resx=nnls(np.column_stack([p0,py]),-px)
    cone_y,resy=nnls(np.column_stack([p0,px]),-py)
    kx,ky=resx**2,resy**2
    assert min(kx,ky)>0
    C=max(np.sqrt(2)*kx**(-.25),2*np.sqrt(2/3)*ky**(-.25))

    # Exact stochastic reparametrization for a nonidentifiable member.
    rr2,ss2,cc=.4,.38,2.
    cf=np.poly([0,rr2,rr2]); cg=np.poly([ss2]*3)
    ch=(1-cc)*cf+cc*cg
    assert np.max(abs(np.roots(ch).imag))<1e-6
    assert np.min(np.roots(ch).real)>0 and np.max(np.roots(ch).real)<1
    beta1=alpha*V[:,0]; beta2=(1-alpha)*V[:,1]
    assert np.allclose(np.outer(beta1,cf)+np.outer(beta2,cg),
             np.outer(beta1+(1-1/cc)*beta2,cf)+np.outer(beta2/cc,ch))

    # Verify first-order scores by finite differences along admissible arcs.
    v=np.array([.2,-.1,.3,.02,.01,-.02,.03,-.01,.4,.5])
    errors=[]; hell=[]
    for t in [1e-3,1e-4,1e-5]:
        Pt,ra,rb=root_arc(v,t,rr,ss,alpha,u,V,clocks)
        assert min(ra.min(),rb.min())>=0 and max(ra.max(),rb.max())<=1
        errors.append(float(np.linalg.norm((Pt-P).reshape(-1)/t-S@v)))
        hell.append(float(np.sqrt(np.sum(w[:,None,None]*(np.sqrt(Pt)-np.sqrt(P))**2))/t))
    assert errors[-1]<errors[0]/20
    expected_h=np.linalg.norm(W@v)/2
    assert abs(hell[-1]-expected_h)<2e-5

    # The two nonsymmetric shapes attain the triple diameter at equal cost.
    Y=.7; h0=np.sqrt(Y/3)
    y1=np.array([-2*h0,h0,h0]); y2=np.array([-h0,-h0,2*h0])
    assert np.isclose(y1@y1/2,Y) and np.isclose(y2@y2/2,Y)
    assert np.isclose(np.max(abs(y1-y2)),2*np.sqrt(Y/3))
    assert 2*np.sqrt(Y/3)>np.sqrt(Y)
    v2=v.copy();v2[-1]=Y
    cost_diffs=[]
    for t in [1e-3,1e-4,1e-5]:
        Qa,*_=root_arc(v2,t,rr,ss,alpha,u,V,clocks,y1)
        Qb,*_=root_arc(v2,t,rr,ss,alpha,u,V,clocks,y2)
        cost_diffs.append(float(np.linalg.norm((Qa-Qb).reshape(-1))/t))
    assert cost_diffs[-1]<cost_diffs[0]/8
    return {'status':'passed','scope':'finite regressions, not proof verification',
            'symbolic':symbolic,'pencil_grid_cases':total,
            'score_matrix_shape':list(S.shape),'nuisance_rank':int(np.linalg.matrix_rank(L)),
            'sample_kappa_x':float(kx),'sample_kappa_y':float(ky),
            'sample_leading_constant':float(C),'finite_difference_errors':errors,
            'hellinger_over_t':hell,'limiting_hellinger_over_t':float(expected_h),
            'equal_score_shape_errors':cost_diffs,
            'other_checks':['half-ray projection','exact stochastic fibre transformation',
                            'extremal triple diameter','admissible root arcs']}

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    result=run_checks()
    text=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(text)
    print(text,end='')
