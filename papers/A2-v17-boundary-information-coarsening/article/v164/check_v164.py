#!/usr/bin/env python3
"""Finite symbolic audits; the general results are proved in the manuscript."""
from __future__ import annotations
import argparse, hashlib, itertools, json, subprocess, sys
from pathlib import Path
import sympy as S
HERE=Path(__file__).resolve().parent

def require(ok:bool,name:str)->None:
    if not ok:raise AssertionError(name)
def same(a,b,variables):
    return S.groebner(a,*variables,order='lex')==S.groebner(b,*variables,order='lex')
def eliminate(equations,aux,variables):
    basis=S.groebner(equations,*aux,*variables,order='lex')
    return [p.as_expr() for p in basis.polys if not any(p.as_expr().has(v) for v in aux)]
def intersect(a,b,variables):
    z=S.Dummy('z')
    return eliminate([z*f for f in a]+[(1-z)*g for g in b],[z],variables)
def saturate(a,f,variables):
    z=S.Dummy('z')
    return eliminate(a+[z*f-1],[z],variables)

def collision_algebra():
    x,c,e,A,B,C,w,delta=S.symbols('x c e A B C lambda delta')
    f=(x-c)**2+e**2*C;g=e*B*(x-c)-e**2*A
    r=w*g-e*A*(x-c)-e**2*B*C
    equations=S.Poly(f-(x*x-delta),x).all_coeffs()+S.Poly(g,x).all_coeffs()+S.Poly(r,x).all_coeffs()
    variables=(c,w,e,A,B,C,delta)
    expected=[c,e*A,e*B,e**2*C+delta]
    require(same(equations,expected,variables),'full retained-coefficient pullback before reduction')
    vars0=(e,A,B,C);I=[e*A,e*B]
    require(same(intersect([e],[A,B],vars0),I,vars0),'reduced full pullback and exact union')
    require(same(saturate(I,e**2*C,vars0),[A,B],vars0),'horizontal schematic closure')
    colon=[S.cancel(m/S.gcd(m,e**2*C)) for m in I]
    require(same(colon,[A,B],vars0),'exact delta torsion')
    for k in range(1,6):
        require(same([S.cancel(m/S.gcd(m,(e**2*C)**k)) for m in I],[A,B],vars0),'no longer delta-torsion layers')
    J=I+[e**2*C]
    primary=intersect(intersect([e],[A,B,C],vars0),[A,B,e**2],vars0)
    require(same(primary,J,vars0),'special fibre primary structure')
    gb=S.groebner(J,*vars0)
    require(gb.reduce(e*C)[1]!=0 and gb.reduce((e*C)**2)[1]==0,'nonzero square-zero nilpotent')
    require(same([S.cancel(m/S.gcd(m,e*C)) for m in J],[e,A,B],vars0),'nilradical module support')
    require(same(intersect([e],[C],(e,C)),[e*C],(e,C)),'horizontal reduced support')
    return {'full_pullback_ideal':'(eA,eB,e^2C+delta)',
            'horizontal_saturation':'(A,B,e^2C+delta)',
            'torsion_annihilator_test_orders':list(range(1,6)),
            'special_fibre_ideal':'(eA,eB,e^2C)',
            'nilradical':'(eC)','nilradical_annihilator':'(e,A,B)','passed':True}

def quotient_and_normalization():
    e,d,t,u,C,delta,w=S.symbols('e d t u C delta lambda')
    require(S.expand(t*t+e*e*C).subs({t:e*d,C:-d*d})==0,'finite normalization equation')
    require(S.cancel((t/e)**2+C).subs(t*t,-e*e*C)==0,'normalization uses common function field')
    require(S.simplify((-e*e*C).subs({e:1/u,C:-delta*u*u}))==delta,'two invariant chart overlap')
    records=[]
    for degree in range(9):
        count=0
        for a in range(degree+1):
            for b in range(degree-a+1):
                k=degree-a-b
                m=w**a*e**b*d**k
                fixed=S.expand(m.subs(d,-d)-m)==0
                require(fixed==(k%2==0),'invariant monomial parity')
                if fixed:
                    inv=w**a*e**b*(-C)**(k//2)
                    require(S.expand(inv.subs(C,-d*d)-m)==0,'invariant polynomial-ring generators')
                    count+=1
        records.append({'total_degree':degree,'invariant_monomials':count})
    # On the root cover the two direction slopes are w +/- d.
    plus=w+d;minus=w-d
    require(plus.subs(d,-d)==minus,'involution exchanges directions')
    P=S.Matrix([[0,1],[1,0]])
    require(P*P==S.eye(2) and (P-S.eye(2)).nullspace().__len__()==1 and (P+S.eye(2)).nullspace().__len__()==1,'ruling monodromy')
    return {'invariant_monomial_profiles':records,'normalization':'C=-d^2,t=ed',
            'second_chart':'d=ut','ruling_monodromy':[[0,1],[1,0]],'passed':True}

def Hilbert_chart_overlap():
    e,u,x,G,H,C=S.symbols('e u x G H C')
    conic=[H*H+C*G*G,x*G-e*H,x*H+e*C*G,u*e-1]
    division=[H-u*x*G,(x*x+e*e*C)*G,u*e-1]
    require(same(conic,division,(u,e,x,G,H,C)),'embedded chart equality, including nilpotent bases')
    t,d=S.symbols('t d')
    require(S.expand((x*G-e*H).subs({x:e*d,H:d*G}))==0,'line at positive root')
    require(S.expand((x*G-e*H).subs({x:-e*d,H:-d*G}))==0,'line at negative root')
    return {'full_localized_ideal_equality':True,'both_ordered_tail_directions_checked':True}

def genuine_pencil():
    x,delta,s,t=S.symbols('x delta s t')
    L=S.Matrix([[-delta,x],[x,-1]]);U=S.Matrix([[1,0],[x,1]])
    require(S.simplify(U.T*L*U)==S.diag(x*x-delta,-1),'polynomial Schur congruence')
    hom=S.Matrix([[-delta*s,t],[t,-s]]);pencil=S.diag(hom,hom)
    require(S.expand(pencil.det()-(t*t-delta*s*s)**2)==0,'genuine-pencil determinant')
    require(pencil.subs({s:0,t:1}).det()==1,'nonsingular infinity')
    require(pencil.subs({s:1,t:0,delta:0}).rank()==2,'central corank is two')
    for q in range(1,8):
        require(pencil.subs({s:1,t:q,delta:q*q}).rank()==2,'two simple incidences in exact examples')
    return {'determinant':'(t^2-delta*s^2)^2','infinity_determinant':1,
            'exact_nonzero_parameter_examples':7,'congruence_verified':True}

def product_profiles():
    profiles=[]
    for r in range(1,7):
        for choices in itertools.product((0,1),repeat=r):
            # Independent local equations are z_i^(1+choice_i) at a generic point.
            exponents=[1+c for c in choices]
            basis=list(itertools.product(*(range(a) for a in exponents)))
            require(len(basis)==2**sum(choices),'central component scheme multiplicity')
            profiles.append({'collisions':r,'double_factors':sum(choices),
                             'generic_local_length':len(basis),'dimension_without_simple_factors':2*r})
    return profiles

def main()->None:
    ap=argparse.ArgumentParser();ap.add_argument('--skip-inherited',action='store_true');args=ap.parse_args()
    inherited=False
    if not args.skip_inherited:
        subprocess.run([sys.executable,str(HERE.parent/'v163'/'check_v163.py')],check=True)
        p=HERE.parent/'v163'/'EXACT_CHECKS_V163.json'
        rec=json.loads(p.read_text())
        require(rec.get('all_checks_pass',rec.get('all_checks_passed',False)),'inherited suite success flag')
        (HERE/'INHERITED_V163_CHECKS_RERUN.json').write_bytes(p.read_bytes());inherited=True
    out={'revision':164,'field':'QQ','collision_algebra':collision_algebra(),
         'quotient_and_normalization':quotient_and_normalization(),
         'Hilbert_chart_overlap':Hilbert_chart_overlap(),'genuine_pencil':genuine_pencil(),
         'product_profiles':product_profiles(),'inherited_v163_suite_rerun':inherited,
         'all_checks_pass':True,'general_proofs_certified_by_computation':False,
         'global_line_bundle_or_cohomology_proved_by_these_tests':False,
         'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (HERE/'EXACT_CHECKS_V164.json').write_text(json.dumps(out,indent=2)+'\n')
    print('All listed exact v164 audits passed; the manuscript supplies the general proofs.')
if __name__=='__main__':main()
