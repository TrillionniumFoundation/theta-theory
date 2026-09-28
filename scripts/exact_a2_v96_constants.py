#!/usr/bin/env python3
"""Exact rational active-set evaluations at two fixed A2 family data.
This checks arithmetic instances; the family theorem is proved in the manuscript.
"""
from __future__ import annotations
import argparse
import itertools
import json
from pathlib import Path
import sympy as s


def evaluate(rank_two=False):
    R=s.Rational
    r,root_s,alpha=R(3,5),R(1,5),R(2,5)
    u1=s.Matrix([R(1,3),R(2,3)])
    u2=s.Matrix([R(2,5),R(3,5)]) if rank_two else u1
    v1=s.Matrix([R(1,4),R(3,4)]); v2=s.Matrix([R(3,4),R(1,4)])
    T=[R(6,5),R(7,5),R(8,5),R(9,5),s.Integer(2),R(5,2),s.Integer(3)]
    js=s.symbols('a b c da du1 du2 dv1 dv2 X Y')
    a,b,c,da,du1,du2,dv1,dv2,X,Y=js; gamma=1-alpha
    d=lambda x:s.Matrix([x,-x])
    scores=[]; weights=[]
    for z in T:
        f=z*(z-r)**2; g=(z-root_s)**3; q=alpha*f+gamma*g
        A1=u1*v1.T; A2=u2*v2.T; P=(alpha*f*A1+gamma*g*A2)/q
        pf=-a*(z-r)**2-b*z*(z-r)-X*z
        pg=-c*(z-root_s)**2-Y*(z-root_s)
        dk=alpha*pf*A1+gamma*pg*A2
        dk+=f*(da*A1+alpha*d(du1)*v1.T+alpha*u1*d(dv1).T)
        dk+=g*(-da*A2+gamma*d(du2)*v2.T+gamma*u2*d(dv2).T)
        dq=alpha*pf+gamma*pg+da*(f-g)
        sc=(dk-P*dq)/q
        scores.extend(list(sc)); weights.extend([R(1,7)/p for p in P])
    S=s.Matrix(scores).jacobian(js); W=s.diag(*weights)
    L=S[:,1:8]; D=S[:,[0,8,9]]; gram=L.T*W*L
    Q=D.T*W*D-(D.T*W*L)*gram.inv(method='DM')*(L.T*W*D)
    Q=s.simplify(Q)
    assert gram.det()>0 and Q[0,0]>0
    rows=[]; ks=[]
    for i in (1,2):
        other=[j for j in range(3) if j!=i]; accepted=[]
        for count in range(3):
            for aa in itertools.combinations(other,count):
                A=list(aa); x=s.zeros(3,1)
                if A:
                    G=Q.extract(A,A)
                    if G.det()<=0: continue
                    vv=-G.inv(method='DM')*Q.extract(A,[i])
                    if any(v<0 for v in vv): continue
                    for j,v in zip(A,vv): x[j]=v
                residual=Q[:,i]+Q*x
                if any(residual[j]<0 for j in other if j not in A): continue
                value=s.factor(Q[i,i]+2*(Q[i,:]*x)[0]+(x.T*Q*x)[0])
                accepted.append((A,value,x))
        assert accepted and all(v==accepted[0][1] for _,v,_ in accepted)
        A,k,x=accepted[0]; assert k>0; ks.append(k)
        rows.append(dict(target='x' if i==1 else 'y',support=A,kappa=str(k),
                         decimal=str(s.N(k,22)),minimizing_nonnegative_coordinates=[str(v) for v in x],
                         admissible_support_count=len(accepted)))
    kx,ky=ks; double=(9*ky>=16*kx)
    C4=4/kx if double else R(64,9)/ky
    lo=s.floor(s.root(C4,4)*1000)/1000; hi=lo+R(1,1000)
    assert lo**4<C4<hi**4
    return dict(U_rank=2 if rank_two else 1,Q_rank=Q.rank(),free_gram_rank=7,
                exact_Q=[[str(Q[i,j]) for j in range(3)] for i in range(3)],
                programs=rows,dominant='double' if double else 'triple',C_fourth_power=str(C4),
                C_decimal=str(s.N(s.root(C4,4),22)),C_rational_isolating_interval=[str(lo),str(hi)],
                interpretation='C is the unique positive fourth root of C_fourth_power')


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output',type=Path,default=Path('v96_exact_constants.json'))
    args=ap.parse_args()
    result={'scope':'exact rational arithmetic at two fixed data, not general proof verification',
            'cases':[evaluate(False),evaluate(True)]}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    for c in result['cases']:
        print('rank',c['U_rank'],'Q rank',c['Q_rank'],'C',c['C_decimal'],'phase',c['dominant'])
        for p in c['programs']: print(' ',p['target'],p['support'],p['decimal'])

if __name__=='__main__': main()
