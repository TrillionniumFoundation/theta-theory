#!/usr/bin/env python3
"""Finite algebra and mechanics for the geometric extraction, not proof certification."""
from __future__ import annotations
from fractions import Fraction as F
import json
import mpmath as mp
import sympy as sp


def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def algebra_checks() -> dict:
    v,c,cp=sp.symbols('v c cp',positive=True)
    P=sp.Matrix([[(v+c)/cp,v/(c*cp)],[v+c+cp,(v+cp)/c]])
    require(sp.simplify(P.det()-1)==0,'canonical matrix determinant')
    require(sp.simplify(P[0,0]/P[0,1]-c-c*c/v)==0,'first row quotient')
    require(sp.simplify(P[1,0]/P[1,1]-c-c*c/(v+cp))==0,'second row quotient')
    H=F(53,6);prod=[[F(1),F(0)],[F(0),F(1)]];products=0
    for j in range(1,101):
        vv=F(6,47)+F(j%11,7);cc=F(1+j%9,10);dd=F(1+j%7,8)
        A=[[(vv+cc)/dd,vv/(cc*dd)],[vv+cc+dd,(vv+dd)/cc]]
        prod=[[sum(A[a][k]*prod[k][b] for k in range(2)) for b in range(2)] for a in range(2)]
        require(0<prod[0][0]/prod[0][1]<=H,'long positive-product ratio')
        require(prod[0][1]>=F(6,47)**j,'lower off-diagonal bound')
        products+=1
    t,s,R,dx,dy=sp.symbols('t s R dx dy')
    den=(1+t*t)*(1+s*s)
    # n_num=(1-t^2,2t), tangent_num=(-2t,1-t^2)
    vx=(1-s*s)*(1-t*t)-4*s*t
    vy=2*t*(1-s*s)+2*s*(1-t*t)
    cross=dx*vy-dy*vx-2*R*s*(1+t*t)
    disc=sp.Poly(sp.expand(R*R*den*den-cross*cross),t,s)
    require(disc.total_degree()==8 and disc.degree(t)<=8 and disc.degree(s)<=8,'discriminant degree')
    require(sp.simplify(vx*vx+vy*vy-den*den)==0,'rational unit direction')
    x,y=sp.symbols('x y');b=x**4*(1-x)**4*y**4*(1-y)**4
    ibp=0
    for k in range(7):
        test=x**k
        for order in (1,2):
            left=sp.integrate(sp.integrate(sp.diff(b,x,order)*test,(x,0,1)),(y,0,1))
            right=(-1)**order*sp.integrate(sp.integrate(b*sp.diff(test,x,order),(x,0,1)),(y,0,1))
            require(sp.simplify(left-right)==0,'pushforward derivative sign')
            ibp+=1
    budgets=0
    for p in (F(1),F(3),F(8)):
        for beta in (F(0),F(2)):
            for gamma in (F(0),F(3)):
                d=1+max(16*(p+5+beta),p+4+gamma)
                require(beta+1-d/F(16)<-p-4 and gamma-d<-p-4,'extraction mass budget')
                require(-p-4+2+1 < -p,'log bandwidth and raw n^2 cost')
                budgets+=1
    # Small mass is not a pointwise small density.
    eps=F(1,100);height=eps**-2;width=eps**3
    require(height*width==eps and height>1,'mass/height negative control')
    require(F(1,2)/F(3,4)!=1,'uncorrected angle-coordinate determinant negative control')
    return {'positive_matrix_products':products,'rational_discriminant_total_degree':8,
            'sublevel_exponent':'1/16','integration_by_parts_cases':ibp,
            'strict_long_time_budgets':budgets,'negative_controls':2}


def mechanical_checks() -> dict:
    mp.mp.dps=70
    sq3=mp.sqrt(3)
    centers=[((i,j),(mp.mpf(i)+mp.mpf(j)/2,mp.mpf(j)*sq3/2))
             for i in range(-4,5) for j in range(-4,5) if i or j]
    def step(r,a,p,label=None):
        n=(mp.cos(a),mp.sin(a));q=(r*n[0],r*n[1]);c=mp.sqrt(1-p*p)
        vv=(c*n[0]-p*n[1],c*n[1]+p*n[0])
        if label is None:
            candidates=[]
            for lab,d in centers:
                z=(d[0]-q[0],d[1]-q[1]);proj=z[0]*vv[0]+z[1]*vv[1]
                disc=r*r-z[0]*z[0]-z[1]*z[1]+proj*proj
                if disc>0:
                    tau=proj-mp.sqrt(disc)
                    if tau>mp.mpf('1e-50'):candidates.append((tau,lab))
            require(bool(candidates),'missing candidate')
            candidates.sort();tau,label=candidates[0]
            require(tau<3 and 5*sq3/2-2*r>3,'finite enumeration incomplete')
            require(len(candidates)==1 or candidates[1][0]-tau>mp.mpf('1e-25'),'near competing hit')
        i,j=label;d=(mp.mpf(i)+mp.mpf(j)/2,mp.mpf(j)*sq3/2)
        z=(d[0]-q[0],d[1]-q[1]);proj=z[0]*vv[0]+z[1]*vv[1]
        disc=r*r-z[0]*z[0]-z[1]*z[1]+proj*proj
        tau=proj-mp.sqrt(disc)
        nn=((q[0]+tau*vv[0]-d[0])/r,(q[1]+tau*vv[1]-d[1])/r)
        pp=-vv[0]*nn[1]+vv[1]*nn[0]
        return tau,mp.atan2(nn[1],nn[0]),pp,label
    def word(r,a,p,labels):
        total=mp.mpf(0)
        for lab in labels:
            dt,a,p,_=step(r,a,p,lab);total+=dt
        return total,a,p
    cases=0;max_jac=mp.mpf(0);max_trans=mp.mpf(0);max_ratio=mp.mpf(0)
    for r in map(mp.mpf,('0.45','0.46','0.47')):
        for a0 in map(mp.mpf,('0.17','0.61','1.29')):
            for p0 in map(mp.mpf,('-0.31','0.23')):
                labels=[];a=a0;p=p0;J=mp.eye(2)
                for m in range(1,9):
                    dt,an,pn,lab=step(r,a,p);labels.append(lab)
                    c=mp.sqrt(1-p*p);cp=mp.sqrt(1-pn*pn);v=dt/r
                    P=-mp.matrix([[(v+c)/cp,v/(c*cp)],[v+c+cp,(v+cp)/c]])
                    J=P*J;a,p=an,pn
                    if m not in (1,2,4,8):continue
                    numeric=mp.matrix([[mp.diff(lambda aa:word(r,aa,p0,labels)[1],a0),
                                        mp.diff(lambda pp:word(r,a0,pp,labels)[1],p0)],
                                       [mp.diff(lambda aa:word(r,aa,p0,labels)[2],a0),
                                        mp.diff(lambda pp:word(r,a0,pp,labels)[2],p0)]])
                    err=max(abs(numeric[i,j]-J[i,j])/(1+abs(J[i,j])) for i in range(2) for j in range(2))
                    require(err<mp.mpf('1e-40'),'physical matrix product mismatch')
                    ra=J[0,0]/J[0,1];require(0<ra<=mp.mpf(53)/6,'physical row ratio')
                    da=mp.diff(lambda aa:word(r,aa,p0,labels)[0],a0)
                    dp=mp.diff(lambda pp:word(r,a0,pp,labels)[0],p0)
                    tr=abs(da-ra*dp+r*p0)
                    require(tr<mp.mpf('1e-38'),'uniform transverse derivative identity')
                    require(mp.sqrt(da*da+dp*dp)>=r*abs(p0)/mp.sqrt(1+(mp.mpf(53)/6)**2),'gradient lower bound')
                    max_jac=max(max_jac,err);max_trans=max(max_trans,tr);max_ratio=max(max_ratio,ra);cases+=1
    return {'precision_decimal_digits':mp.mp.dps,'regular_word_cases':cases,
            'word_lengths':[1,2,4,8],'max_relative_matrix_error':mp.nstr(max_jac,8),
            'max_transverse_identity_error':mp.nstr(max_trans,8),'max_observed_row_ratio':mp.nstr(max_ratio,8),
            'continuum_cutoff_and_density_proofs_not_certified':True}


def finite_checks() -> dict:
    return {'algebra':algebra_checks(),'mechanics':mechanical_checks(),'full_raw_LLT_certified':False}

if __name__=='__main__':
    print(json.dumps(finite_checks(),sort_keys=True,indent=2))
