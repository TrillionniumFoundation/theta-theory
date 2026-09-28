#!/usr/bin/env python3
"""Exact finite regressions for A2 v97; not a proof verifier.

Run from the repository root with Python 3 and SymPy installed.
All displayed bounds are checked with rational arithmetic.
"""
from __future__ import annotations
import argparse
import itertools
import json
from pathlib import Path
import sympy as s

R = s.Rational
z = s.Symbol('z')


def observation_and_score(f, g, alpha, u1, u2, v1, v2, clocks, weights):
    """Return probabilities, Fisher weights, and a rational score constructor."""
    gamma = 1-alpha
    q = alpha*f+gamma*g
    K = alpha*f*u1*v1.T+gamma*g*u2*v2.T
    Ps = [K.subs(z,T)/q.subs(z,T) for T in clocks]
    W = s.diag(*[weights[j]/Ps[j][a,b]
                 for j in range(len(clocks)) for a in range(2) for b in range(2)])
    def score(pf=0, pg=0, da=0, du1=None, du2=None, dv1=None, dv2=None):
        zero=s.zeros(2,1)
        du1=zero if du1 is None else du1
        du2=zero if du2 is None else du2
        dv1=zero if dv1 is None else dv1
        dv2=zero if dv2 is None else dv2
        dq=alpha*pf+gamma*pg+da*(f-g)
        dK=alpha*pf*u1*v1.T+gamma*pg*u2*v2.T
        dK+=da*(f*u1*v1.T-g*u2*v2.T)
        dK+=f*alpha*(du1*v1.T+u1*dv1.T)
        dK+=g*gamma*(du2*v2.T+u2*dv2.T)
        out=[]
        for j,T in enumerate(clocks):
            M=(dK.subs(z,T)-Ps[j]*s.sympify(dq).subs(z,T))/q.subs(z,T)
            out.extend([s.cancel(M[a,b]) for a in range(2) for b in range(2)])
        return s.Matrix(out)
    return Ps,W,score


def project_gram(L, D, W):
    G=L.T*W*L
    assert G.det()!=0
    Q=D.T*W*D-D.T*W*L*G.inv(method='DM')*L.T*W*D
    return Q.applyfunc(s.cancel)


def orthant_min(Q, linear, constant):
    """Exact KKT enumeration of v'Qv+2 linear'v+constant on v>=0.

    Independent positive supports suffice, including when Q is singular.
    """
    n=Q.rows
    records=[]
    for k in range(n+1):
        for A in itertools.combinations(range(n),k):
            if A:
                QA=Q.extract(A,A)
                if QA.det()==0:
                    continue
                va=-QA.inv(method='DM')*linear.extract(A,[0])
            else:
                va=s.zeros(0,1)
            v=s.zeros(n,1)
            for j,a in enumerate(A): v[a]=s.cancel(va[j])
            if any(v[a]<0 for a in A): continue
            grad=Q*v+linear
            if any(grad[j]<0 for j in range(n) if j not in A): continue
            assert all(grad[a]==0 for a in A)
            val=s.cancel((v.T*Q*v)[0]+2*(linear.T*v)[0]+constant)
            records.append((val,A,v))
    if not records: raise AssertionError('no feasible independent KKT support')
    assert all(x[0]==records[0][0] for x in records)
    return records[0]


def bracket_positive_power(value, power, digits=12):
    scale=10**digits
    n=int(s.floor(s.N(value,70)**(s.Rational(1,power))*scale))
    lo,hi=R(n,scale),R(n+1,scale)
    while lo**power>value:
        n-=1;lo,hi=R(n,scale),R(n+1,scale)
    while hi**power<=value:
        n+=1;lo,hi=R(n,scale),R(n+1,scale)
    assert lo>=0 and lo**power<=value<hi**power
    return {'lower':str(lo),'upper':str(hi),'decimal':str(s.N(value**R(1,power),18))}


def main(output):
    rr,ss=s.symbols('r s', positive=True)
    ff=z*(z-rr)**2;gg=(z-ss)**3
    cc=s.Symbol('c')
    AA=(rr+3*ss)*(2*rr-3*ss)**2
    disc=s.factor(s.discriminant((1-cc)*ff+cc*gg,z))
    assert s.expand(disc-cc*(cc-1)**2*(rr-ss)**3*(AA*cc-4*rr**3))==0
    cs=4*rr**3/AA;bs=rr*ss/(3*ss-2*rr);as_=4*rr*ss/(rr+3*ss)
    assert s.factor((1-cs)*ff+cs*gg-(z-as_)*(z-bs)**2)==0
    chi=s.factor((ff-gg).subs(z,bs)/(bs-as_))
    assert s.factor((bs-as_)*chi+(gg-ff).subs(z,bs))==0

    r,st,D,af=R(3,5),R(11,20),R(1),R(1,10)
    A=(r+3*st)*(2*r-3*st)**2
    cstar=4*r**3/A
    b=r*st/(3*st-2*r);a=4*r*st/(r+3*st)
    gamma0=af*cstar;alpha0=1-gamma0
    assert 0<st<r<D and r<b<D and st<a<r
    assert af<alpha0<1-af
    f=z*(z-r)**2;g=(z-st)**3;h=(z-a)*(z-b)**2
    assert s.expand(h-((1-cstar)*f+cstar*g))==0
    B=(3*D-r)*st-2*r*D
    assert B>0
    E0=gamma0*A-4*af*r**3
    assert E0==0
    u=s.Matrix([R(1,3),R(2,3)])
    v1=s.Matrix([R(1,4),R(3,4)]);v2=s.Matrix([R(3,4),R(1,4)])
    vf=(alpha0*v1+(gamma0-af)*v2)/(1-af)
    clocks=list(map(R,['6/5','7/5','8/5','9/5','2','5/2','3']))
    weights=[R(1,7)]*7
    Ps,W,base=observation_and_score(f,g,alpha0,u,u,v1,v2,clocks,weights)
    Pr,Wr,remote=observation_and_score(f,h,1-af,u,u,vf,v2,clocks,weights)
    assert Ps==Pr and W==Wr
    e=s.Matrix([1,-1])
    nuisance=[base(da=1),base(du1=e),base(du2=e),base(dv1=e),base(dv2=e)]
    L=s.Matrix.hstack(base(pf=-z*(z-r)),base(pg=-(z-st)**2),*nuisance)
    Dr=s.Matrix.hstack(base(pf=-(z-r)**2),base(pf=-z),base(pg=-(z-st)))
    Q=project_gram(L,Dr,W)
    kappas=[]
    for i in (1,2):
        ids=[j for j in range(3) if j!=i]
        val,support,v=orthant_min(Q.extract(ids,ids),Q.extract(ids,[i]),Q[i,i])
        assert val>0
        kappas.append((val,support))
    kx,ky=kappas[0][0],kappas[1][0]
    C4=max(4/kx,R(64,9)/ky)
    Lr=s.Matrix.hstack(remote(pf=-z*(z-r)),remote(pg=-(z-b)**2),
                       remote(pg=-(z-a)*(z-b)),remote(du1=e),remote(du2=e),
                       remote(dv1=e),remote(dv2=e))
    Cr=s.Matrix.hstack(remote(pf=-(z-r)**2),remote(pf=-z),
                       remote(pg=-(z-a)),remote(da=-1))
    target=base(da=1)
    augmented=project_gram(Lr,s.Matrix.hstack(Cr,target),W)
    val,support,v=orthant_min(augmented[:4,:4],-augmented[:4,4:5],augmented[4,4])
    assert val>0
    mu2=s.cancel(val/4)
    chiex=s.cancel(chi.subs({rr:r,ss:st}))
    Dstar=max(r-st,b-r)
    assert Dstar==R(2,15)
    assert chiex>0
    # Algebraic width identity used in the arbitrary-multiplicity proof.
    for m in range(2,21):
        for j in range(1,m+1):
            aa=j-1;bb=m-j
            if aa and bb:
                assert aa*bb*(aa+bb+2)**2>=4*(aa+1)*(bb+1)
        assert R(m-1,m)>0
    # A genuinely different singularity pattern: degree four, interior
    # multiplicities three and four, and full-rank channels on both sides.
    eps=s.Symbol('eps')
    f4=z*(z-r)**3; g4=(z-R(1,5))**4
    clocks4=clocks+[R(7,2),R(4)]; weights4=[R(1,9)]*9
    u2=s.Matrix([R(2,5),R(3,5)])
    _,W4,score4=observation_and_score(f4,g4,R(2,5),u,u2,v1,v2,clocks4,weights4)
    L4=s.Matrix.hstack(score4(pf=-z*(z-r)**2),score4(pg=-(z-R(1,5))**3),
                       score4(da=1),score4(du1=e),score4(du2=e),
                       score4(dv1=e),score4(dv2=e))
    D4=s.Matrix.hstack(score4(pf=-(z-r)**3),score4(pf=-z*(z-r)),
                       score4(pg=-(z-R(1,5))**2))
    Q4=project_gram(L4,D4,W4)
    assert all(Q4[:k,:k].det()>0 for k in range(1,4))
    ks4=[]
    for i in (1,2):
        ids=[j for j in range(3) if j!=i]
        value,A4,_=orthant_min(Q4.extract(ids,ids),Q4.extract(ids,[i]),Q4[i,i])
        assert value>0
        ks4.append(value)
    C4degree4=max(R(64,9)/ks4[0],R(9)/ks4[1])
    f4arc=s.expand(z*(z-r+2*eps)*(z-r-eps)**2)
    g4arc=s.expand((z-R(1,5)+3*eps)*(z-R(1,5)-eps)**3)
    assert s.expand(f4arc).coeff(eps,1)==0
    assert s.expand(g4arc).coeff(eps,1)==0
    assert s.expand(s.expand(f4arc).coeff(eps,2)+3*z*(z-r))==0
    assert s.expand(s.expand(g4arc).coeff(eps,2)+6*(z-R(1,5))**2)==0
    # Every higher coefficient has a nonzero zero-sum split witness.
    for m in range(2,10):
        split=s.Poly(s.expand((z+(m-1)*eps)*(z-eps)**(m-1)),z)
        assert split.coeff_monomial(z**(m-1))==0
        for k in range(2,m+1):
            coefficient=s.expand(split.coeff_monomial(z**(m-k)))
            assert coefficient.coeff(eps,k)!=0 and s.degree(coefficient,eps)==k
        boundary=s.Poly(s.expand((z-eps)**m),z)
        for k in range(1,m+1):
            assert s.degree(boundary.coeff_monomial(z**(m-k)),eps)==k
    # Independent symbolic check of the geometric-wall interval opening.
    sw=R(1,2); rs=z*(z-r)**2/(z-ss)**3
    cbound=s.cancel(rs.subs(z,1)/(rs.subs(z,1)-1))
    ccrit=4*r**3/((r+3*ss)*(2*r-3*ss)**2)
    diff=s.cancel(cbound-ccrit)
    assert diff.subs(ss,sw)==0 and s.diff(diff,ss).subs(ss,sw)==0
    bfun=r*ss/(3*ss-2*r)
    RR=rs.subs(ss,sw)
    geometric_coefficient=-s.diff(RR,z,2).subs(z,1)/(2*(RR.subs(z,1)-1)**2)
    assert geometric_coefficient>0
    assert s.cancel(s.diff(diff,ss,2).subs(ss,sw)/2-
                    geometric_coefficient*s.diff(bfun,ss).subs(ss,sw)**2)==0
    result={
      'status':'passed','role':'exact finite regression; not universal proof verification',
      'symbolic_checks':['pencil discriminant','remote double-root factorization',
                         'wall splitting coefficient','ordered-root diameter inequality m=2..20',
                         'degree-four full-rank Fisher program','coefficient-order witnesses m=2..9',
                         'geometric-wall quadratic interval opening'],
      'wall_example':{'r':str(r),'s':str(st),'D':str(D),'alpha_floor':str(af),
                      'alpha0':str(alpha0),'cstar':str(cstar),'remote_simple':str(a),
                      'remote_double':str(b),'B':str(B),'E0':str(E0),'Dstar':str(Dstar),
                      'chi':str(chiex),'vf':[str(t) for t in vf]},
      'multiplicity_regression':{'degree':4,'interior_multiplicities':[3,4],
                                 'projected_gram_positive_definite':True,
                                 'kappas':[str(x) for x in ks4],
                                 'C_interval':bracket_positive_power(C4degree4,4)},
      'geometric_wall_regression':{'r':str(r),'s':str(sw),
                                   'clearance_squared_coefficient':str(geometric_coefficient)},
      'base_local_fisher':{'kappa_x':str(kx),'kappa_y':str(ky),'C4':str(C4),
                          'C_interval':bracket_positive_power(C4,4),
                          'supports':[list(x[1]) for x in kappas]},
      'wall_remote_fisher':{'mu2':str(mu2),'mu_interval':bracket_positive_power(mu2,2,15),
                           'positive_support':list(support),'nonnegative_variables':[str(t) for t in v],
                           'projected_gram':[[str(augmented[i,j]) for j in range(5)] for i in range(5)]},
      'not_executed':['general resolution implementation','quantifier elimination of entire model',
                      'universal theorem verification','full nonlinear optimizer over all competitors']}
    Path(output).parent.mkdir(parents=True,exist_ok=True)
    Path(output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','role','wall_example']},indent=2))
    print('C_loc at wall:',result['base_local_fisher']['C_interval'])
    print('mu_E:',result['wall_remote_fisher']['mu_interval'])
    print('remote active support:',support)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',default='revisions/a2-v97/EXACT_DIAGNOSTICS.json')
    main(p.parse_args().output)
