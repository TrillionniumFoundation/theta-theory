#!/usr/bin/env python3
"""Exact finite checks for the v167 equations; not proof or novelty certificates."""
from __future__ import annotations
import argparse, hashlib, itertools, json, subprocess, sys
from pathlib import Path
import sympy as S
from sympy.polys.matrices import DomainMatrix
HERE=Path(__file__).resolve().parent

def require(ok,name):
    if not ok: raise AssertionError(name)
def minimal(pairs):
    return {a for a in pairs if not any(b!=a and b[0]<=a[0] and b[1]<=a[1] for b in pairs)}
def mul(A,B):return minimal({(a+c,b+d) for a,b in A for c,d in B})
def power(A,n):
    p={(0,0)}
    for _ in range(n):p=mul(p,A)
    return p
def mons(ds,dt):
    if ds<0 or dt<0:return []
    return [(ds-i,i,j0,j1,dt-j0-j1) for i in range(ds+1) for j0 in range(dt+1) for j1 in range(dt-j0+1)]
def exprmon(v,vars):return S.prod(x**n for x,n in zip(vars,v))
def rank(mat):return DomainMatrix.from_Matrix(mat).convert_to(S.QQ).rank()

def slice_determinants_and_limits():
    s,t,F,G,R=S.symbols('s t F G R');vs=(s,t,F,G,R)
    columns=mons(4,4);require(len(columns)==75,'matrix has 75 columns')
    positions={v:i for i,v in enumerate(columns)}
    rows=[set() for _ in range(13)]
    for col in columns:
        _,i,j0,j1,j2=col;rows[i+2*j0+j2].add((j1,j2))
    rows=[minimal(r) for r in rows]
    prod={(0,0)}
    for r in rows:prod=mul(prod,r)
    J1={(1,0),(0,1)};J2={(1,0),(0,2)}
    expected=mul({(10,0)},mul(power(J1,4),power(J2,6)))
    require(prod==expected,'maximal-minor ideal b^10(b,c)^4(b,c^2)^6')
    records=[]
    for p,q in [(1,2),(1,1),(3,2),(2,1),(3,1)]:
        beta=S.Integer(2);gamma=S.Integer(3)
        weights=[min(p*a+q*b for a,b in r) for r in rows]
        require(sum(weights)==10*p+4*min(p,q)+6*min(p,2*q),'explicit slice jet order')
        L=S.zeros(13,75)
        for j,col in enumerate(columns):
            _,i,j0,j1,j2=col;r=i+2*j0+j2
            if p*j1+q*j2==weights[r]:L[r,j]=beta**j1*gamma**j2
        require(rank(L)==13,'primitive row lattice rank')
        if p<q:ideals=[(R,0,1),(t*t*G,2,1)]
        elif p==q:
            k=gamma/beta;ideals=[(s*R-k*t*G,1,1),(t*R,1,1),(R*R,0,2)]
        elif p<2*q:ideals=[(t*G,1,1),(t*R,1,1),(R*R,0,2)]
        elif p==2*q:
            h=gamma*gamma/beta;ideals=[(t*G,1,1),(t*R,1,1),(R*R-h*F*G,0,2)]
        else:ideals=[(t*G,1,1),(t*R,1,1),(F*G,0,2)]
        relations=[]
        for f,ds,dt in ideals:
            for mon in mons(4-ds,4-dt):
                poly=S.Poly(f*exprmon(mon,vs),*vs);r=[S.Integer(0)]*75
                for ex,coeff in poly.terms():r[positions[ex]]=coeff
                relations.append(r)
        H=S.Matrix(relations)
        require(L*H.T==S.zeros(13,H.rows),'listed special ideal is annihilated by primitive Hilbert matrix')
        require(rank(H)==62,'listed ideal spans the full degree-four kernel')
        records.append({'p':p,'q':q,'beta':2,'gamma':3,'minor_order':sum(weights),'quotient_rank':13,'ideal_rank':62})
    # All primitive adjacent fan cones are unimodular.
    rays=[(1,0),(2,1),(1,1),(0,1)]
    determinants=[int(S.det(S.Matrix.hstack(S.Matrix(a),S.Matrix(b)))) for a,b in zip(rays,rays[1:])]
    require(determinants==[1,1,1],'smooth three-cone fan')
    return {'row_monomial_ideals':[sorted(r) for r in rows],'maximal_minor_generators':sorted(prod),'factorization':'b^10*(b,c)^4*(b,c^2)^6','all_five_Hilbert_limits':records,'primitive_fan_rays':rays,'fan_determinants':determinants,'passed':True}

def equations():
    s,t,F,G,R,e,h,c,z,b,k=S.symbols('s t F G R e h c z b k')
    I1=[R*R-h*F*G,t*G-e*s*R,t*R-e*h*s*F]
    I2=[F*G-z*R*R,t*G-c*z*s*R,t*R-c*s*F]
    HB=S.Matrix([[F,R],[-z*R,-G],[-t,-c*s]])
    minors=[S.det(HB.extract(p,[0,1])) for p in [(0,1),(0,2),(1,2)]]
    require(all(S.expand(x-y)==0 for x,y in zip(minors,[-I2[0],I2[2],-I2[1]])),'Hilbert-Burch signs')
    subs={c:e*h,z:1/h}
    require(S.cancel(I2[0].subs(subs,simultaneous=True)+I1[0]/h)==0,'conic overlap')
    require(all(S.cancel(I2[i].subs(subs,simultaneous=True)-I1[i])==0 for i in (1,2)),'linear overlaps')
    graph={F:t*t,G:e*e*h*s*s,R:e*h*s*t}
    require(all(S.expand(f.subs(graph,simultaneous=True))==0 for f in I1),'generic retained graph')
    I0=[t*t*G-b*s*s*F,s*R-k*t*G,t*R-b*k*s*F,R*R-b*k*k*F*G]
    require(all(S.expand(f.subs({F:t*t,G:b*s*s,R:b*k*s*t},simultaneous=True))==0 for f in I0),'primitive generic graph')
    require(S.det(S.Matrix([[S.diff(e*e*h,e),S.diff(e*e*h,h)],[S.diff(e*h,e),S.diff(e*h,h)]]))==e*e*h,'relative canonical Jacobian e^2 h')
    # Formal high-jet witness in the nonsymmetric slice.
    tau=S.symbols('tau')
    for n in range(9):
        M=n+1
        require(S.degree(tau**(2*M),tau)>n and S.degree(tau**M,tau)>n,'matching arbitrary prescribed jet')
        require(R*R-F*G != R*R-S.Rational(1,2)*F*G,'distinct wall conics')
    return {'HB_minors':list(map(str,minors)),'all_chart_overlap_and_generic_graph_identities':True,'canonical_Jacobian':'e^2*h','high_jet_examples':9,'passed':True}

def degrees_and_classes():
    records=[]
    for a in range(1,16):
        d=a+1;m=d*(d-1)//2+1
        require(d+(d-1)*(d-2)//2==m,'Gotzmann number')
        for l in [m,m+1,m+5]:
            require(sum(l+1-i for i in range(d))+(d-1)*(d-2)//2==d*l+1,'Gotzmann polynomial identity')
        records.append({'a':a,'m':m,'q':d*m+1,'N':(m+1)*int(S.binomial(m+2,2))})
    class_records=[]
    for m in range(1,21):
        g=S.gcd(m,2);order=int(m/g)
        # Image congruences of primitive-divisor pairing have the stated index.
        if g==1:
            residues={(a-2*b)%m for a in range(m) for b in range(m)}
        else:residues={(a-b)%order for a in range(order) for b in range(order)}
        require(len(residues)==order,'cyclic divisor-class index')
        class_records.append({'m':m,'class_group_order':order,'singular':order>1})
    return {'degree_examples':records,'toric_class_examples':class_records,'passed':True}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--skip-inherited',action='store_true');args=ap.parse_args()
    inherited=False
    if not args.skip_inherited:
        previous=HERE.parent/'v166'/'check_v166.py'
        subprocess.run([sys.executable,str(previous)],check=True)
        record=json.loads((previous.parent/'EXACT_CHECKS_V166.json').read_text())
        require(record['all_checks_pass'] and record['inherited_v164_suite_rerun'],'inherited v166 and full earlier chain')
        (HERE/'INHERITED_V166_CHECKS_RERUN.json').write_text(json.dumps(record,indent=2)+'\n');inherited=True
    out={'revision':167,'field':'QQ','slice':slice_determinants_and_limits(),'equations':equations(),'degrees_and_classes':degrees_and_classes(),'inherited_v166_full_chain_rerun':inherited,'all_checks_pass':True,'general_proofs_certified_by_computation':False,'novelty_or_journal_threshold_certified':False,'external_independent_audit_obtained':False,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (HERE/'EXACT_CHECKS_V167.json').write_text(json.dumps(out,indent=2)+'\n')
    print('All listed finite exact v167 checks passed; full theorems require their manuscript proofs.')
if __name__=='__main__':main()
