#!/usr/bin/env python3
"""Exact finite regression for A2 v98, NOT a universal theorem verifier.

Run: python scripts/verify_a2_v98_math.py --output /tmp/a2-v98-exact.json
Requires SymPy 1.14.0. All acceptance tests use rational arithmetic.
"""
from __future__ import annotations
import argparse
import itertools
import json
from pathlib import Path
import sympy as s

z = s.symbols('z')
R = s.Rational
CHECKS: list[str] = []


def zero(expr: s.Expr, name: str) -> None:
    if s.cancel(s.expand(expr)) != 0:
        raise AssertionError(name)
    CHECKS.append(name)


def symbolic() -> None:
    r, b, a, h, c, q, tau = s.symbols('r b a h c q tau')
    f, g = z*(z-r)**2, (z-h)**3
    A = (r+3*h)*(2*r-3*h)**2
    pencil = (1-c)*f+c*g
    zero(s.discriminant(pencil,z)-c*(c-1)**2*(r-h)**3*(A*c-4*r**3), 'cubic discriminant')
    zero(A-4*r**3+27*h**2*(r-h), 'discriminant coefficient identity')
    cs, aa, bb = 4*r**3/A, 4*r*h/(r+3*h), r*h/(3*h-2*r)
    zero(((1-c)*f+c*g).subs(c,cs)-(z-aa)*(z-bb)**2, 'remote double-root factorization')
    zero(s.diff(f/g,z)/(f/g)-((2*r-3*h)*z+r*h)/(z*(z-r)*(z-h)), 'pencil ratio derivative')
    a0,b0,c0,d0,X,Y = s.symbols('a0 b0 c0 d0 X Y')
    pf = -a0*(z-r)**2-b0*z*(z-r)-X*z
    ph = -c0*(z-b)**2-d0*(z-a)*(z-b)-Y*(z-a)
    ft = (z-tau*a0)*((z-r-tau*b0/2)**2-tau*X)
    ht = (z-a-tau*c0)*((z-b-tau*d0/2)**2-tau*Y)
    ef = tau**2*(a0*b0*(z-r)+a0*X+b0**2*z/4)-tau**3*a0*b0**2/4
    eh = tau**2*(c0*d0*(z-b)+c0*Y+d0**2*(z-a)/4)-tau**3*c0*d0**2/4
    zero(ft-f-tau*pf-ef, 'remote first-component quadratic remainder')
    zero(ht-(z-a)*(z-b)**2-tau*ph-eh, 'remote second-component quadratic remainder')
    def coeff(v): return s.Matrix([s.expand(v).coeff(z,j) for j in range(3)])
    Jf = s.Matrix.hstack(*[coeff(s.diff(pf,v)) for v in (a0,b0,X)])
    Jh = s.Matrix.hstack(*[coeff(s.diff(ph,v)) for v in (c0,d0,Y)])
    if s.factor(Jf.det()) == 0 or s.factor(Jh.det()) == 0:
        raise AssertionError('remote chart differentials')
    CHECKS.append('remote chart differentials nonsingular with separated roots')
    u0,u1,u2,w = s.symbols('u0 u1 u2 w')
    zero(((z**3+u2*z**2+u1*z+u0).subs(z,w-u2/3))-
         (w**3+(u1-u2**2/3)*w+u0-u1*u2/3+2*u2**3/27), 'depressed cubic coefficients')
    for m in range(2,13):
        poly=s.Poly((z-1)**(m-1)*(z+m-1),z)
        for k in range(2,m+1):
            assert poly.coeff_monomial(z**(m-k)) != 0
        for j in range(1,m+1):
            aa,bb=j-1,m-j
            if aa*bb:
                assert aa*bb*(aa+bb+2)**2 >= 4*(aa+1)*(bb+1)
    CHECKS.append('multiplicity coefficient witnesses and ordered diameter inequalities, m=2..12')


CLOCKS = [R(6,5),R(7,5),R(8,5),R(9,5),R(2),R(5,2),R(3)]
ONE = s.ones(2,1)
DZ = s.zeros(2,1)
DU = s.Matrix([1,-1])


def scores(f: s.Expr,g: s.Expr,alpha: s.Rational,U:s.Matrix,V:s.Matrix,
           directions: list[tuple]) -> tuple[s.Matrix,s.Matrix]:
    """Columns are derivatives of the original normalized probabilities."""
    u1,u2,v1,v2=U[:,0],U[:,1],V[:,0],V[:,1]
    K=alpha*f*u1*v1.T+(1-alpha)*g*u2*v2.T
    q=alpha*f+(1-alpha)*g
    probs=[]; vals=[]
    for T in CLOCKS:
        qt=q.subs(z,T); Pt=K.subs(z,T)/qt
        probs.extend(list(Pt))
        vals.append((T,qt,Pt))
    columns=[]
    for pf,pg,da,du1,du2,dv1,dv2 in directions:
        dK=alpha*pf*u1*v1.T+(1-alpha)*pg*u2*v2.T
        dK+=f*(da*u1*v1.T+alpha*du1*v1.T+alpha*u1*dv1.T)
        dK+=g*(-da*u2*v2.T+(1-alpha)*du2*v2.T+(1-alpha)*u2*dv2.T)
        dq=alpha*pf+(1-alpha)*pg+da*(f-g)
        out=[]
        for T,qt,Pt in vals:
            out.extend(list((dK.subs(z,T)-Pt*dq.subs(z,T))/qt))
        columns.append(s.Matrix(out))
    assert all(p>0 for p in probs)
    W=s.diag(*[1/(7*p) for p in probs])
    return s.Matrix.hstack(*columns),W


def direction(pf=0,pg=0,da=0,channel=None):
    inc=[DZ.copy() for _ in range(4)]
    if channel is not None: inc[channel]=DU
    return (s.sympify(pf),s.sympify(pg),s.sympify(da),*inc)


def projected(L:s.Matrix,D:s.Matrix,W:s.Matrix,B=None):
    gram=L.T*W*L
    assert gram.det()!=0
    cross=L.T*W*D
    Q=D.T*W*D-cross.T*gram.inv(method='DM')*cross
    if B is None: return Q
    lb=L.T*W*B
    inv=gram.inv(method='DM')
    return Q,D.T*W*B-cross.T*inv*lb,(B.T*W*B-lb.T*inv*lb)[0]


def supports(Q:s.Matrix,g:s.Matrix,b:s.Expr):
    """Exhaust independent supports; do not assume the full Q is invertible."""
    n=Q.rows; good=[]
    for mask in range(1<<n):
        A=[i for i in range(n) if mask & (1<<i)]
        v=s.zeros(n,1)
        if A:
            qa=Q.extract(A,A)
            if not all(qa[:j,:j].det()>0 for j in range(1,len(A)+1)): continue
            va=qa.inv(method='DM')*g.extract(A,[0])
            for j,val in zip(A,va):v[j]=val
        gradient=Q*v-g
        if any(x<0 for x in v):continue
        if any(gradient[j]<0 for j in range(n) if j not in A):continue
        value=(v.T*Q*v)[0]-2*(g.T*v)[0]+b
        good.append((A,s.factor(value)))
    assert good and len({val for _,val in good})==1
    return good[0][1],[A for A,_ in good]


def base_fisher(h,alpha,rank_two=False):
    r=R(3,5);f=z*(z-r)**2;g=(z-h)**3
    u=s.Matrix([R(1,3),R(2,3)])
    U=s.Matrix.hstack(u,s.Matrix([R(2,5),R(3,5)]) if rank_two else u)
    V=s.Matrix([[R(1,4),R(3,4)],[R(3,4),R(1,4)]])
    free=[direction(pf=-z*(z-r)),direction(pg=-(z-h)**2),direction(da=1)]
    free += [direction(channel=j) for j in range(4)]
    cone=[direction(pf=-(z-r)**2),direction(pf=-z),direction(pg=-(z-h))]
    S,W=scores(f,g,alpha,U,V,free+cone)
    Q=projected(S[:,:7],S[:,7:],W);k=[]; acts=[]
    for i in (1,2):
        other=[j for j in range(3) if j!=i]
        val,A=supports(Q.extract(other,other),-Q.extract(other,[i]),Q[i,i])
        assert val>0;k.append(val);acts.append(A)
    c4=max(4/k[0],R(64,9)/k[1])
    return {'kappa_x':str(k[0]),'kappa_y':str(k[1]),'C4':str(c4),'supports':acts}


def remote_fisher():
    r,h,pi=R(3,5),R(11,20),R(1,10)
    A=(r+3*h)*(2*r-3*h)**2;cs=4*r**3/A
    a,b=4*r*h/(r+3*h),r*h/(3*h-2*r);alpha0=1-pi*cs
    f=z*(z-r)**2;g=(z-h)**3;hp=(z-a)*(z-b)**2
    u=s.Matrix([R(1,3),R(2,3)]);U=s.Matrix.hstack(u,u)
    V=s.Matrix([[R(1,4),R(3,4)],[R(3,4),R(1,4)]])
    vf=(alpha0*V[:,0]+(1-alpha0-pi)*V[:,1])/(1-pi)
    Vr=s.Matrix.hstack(vf,V[:,1])
    B0,_=scores(f,g,alpha0,U,V,[direction(da=1)])
    free=[direction(pf=-z*(z-r)),direction(pg=-(z-b)**2),direction(pg=-(z-a)*(z-b))]
    free += [direction(channel=j) for j in range(4)]
    cone=[direction(pf=-(z-r)**2),direction(pf=-z),direction(pg=-(z-a)),direction(da=-1)]
    S,W=scores(f,hp,1-pi,U,Vr,free+cone)
    Q,gstar,bstar=projected(S[:,:7],S[:,7:],W,B0)
    val,act=supports(Q,gstar,bstar); mu2=s.factor(val/4)
    assert mu2>0 and [] in act
    assert R('0.000002131024914')**2<mu2<R('0.000002131024915')**2
    chi=s.factor((f.subs(z,b)-g.subs(z,b))/(b-a))
    assert (alpha0,cs,a,b,chi)==(R(547,675),R(256,135),R(44,75),R(11,15),R(3,64))
    assert vf==s.Matrix([R(1457,4860),R(3403,4860)])
    CHECKS.append('remote Fisher program: 16 supports, exact positive mu squared and isolating interval')
    return {'mu2':str(mu2),'supports':act,'Q':[[str(x) for x in Q.row(i)] for i in range(4)],
            'g':[str(x) for x in gstar],'b':str(bstar),'alpha0':str(alpha0),'cstar':str(cs),
            'a':str(a),'b_root':str(b),'chi':str(chi),'vf':[str(x) for x in vf]}


def main() -> None:
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    symbolic()
    old=base_fisher(R(1,5),R(2,5))
    assert R(old['C4'])==R(78550423766145732273576408862601811503774391446,385279214348552940073664077156875)
    assert R('3778.707')**4<R(old['C4'])<R('3778.708')**4
    rank2=base_fisher(R(1,5),R(2,5),True)
    assert R('59.970')**4<R(rank2['C4'])<R('59.971')**4
    wall=base_fisher(R(11,20),R(547,675))
    assert R('5975.429249985072')**4<R(wall['C4'])<R('5975.429249985073')**4
    CHECKS.append('three base Fisher programs: all finite supports and rational fourth-power intervals')
    remote=remote_fisher()
    result={'evidence_scope':'exact finite regression; not universal proof verification',
            'sympy':s.__version__,'checks':CHECKS,'passed':True,
            'rank_one_base':old,'rank_two_base':rank2,'wall_base':wall,'wall_remote':remote}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(f'PASS: {len(CHECKS)} regression groups; output {args.output}')

if __name__=='__main__': main()
