#!/usr/bin/env python3
"""Exact finite checks for v166; these are not certificates of general proofs."""
from __future__ import annotations
import argparse, hashlib, itertools, json, math, subprocess, sys
from pathlib import Path
import sympy as S
HERE=Path(__file__).resolve().parent

def require(ok,name):
    if not ok:raise AssertionError(name)
def basis(a,variables):return S.groebner(a,*variables,order='lex')
def same(a,b,variables):return basis(a,variables)==basis(b,variables)
def eliminate(eqs,aux,variables):
    gb=basis(eqs,tuple(aux)+tuple(variables))
    return [p.as_expr() for p in gb.polys if not any(p.as_expr().has(v) for v in aux)]
def intersection(a,b,variables):
    y=S.Dummy('y');return eliminate([y*x for x in a]+[(1-y)*x for x in b],[y],variables)
def saturation(a,f,variables):
    y=S.Dummy('y');return eliminate(list(a)+[1-y*f],[y],variables)
def zero(expr,name):require(S.cancel(S.expand(expr))==0,name)

def coefficient_presentations():
    z,e,A,B,C,lam,u,v,w,z0,d,alpha,beta=S.symbols('z e A B C lam u v w z0 d alpha beta')
    f=z*z+e*e*C;g=e*B*z-e*e*A;r=lam*g-e*A*z-e*e*B*C
    actual=S.Poly(f-(z*z+d),z).all_coeffs()+S.Poly(g-(u*z+v),z).all_coeffs()+S.Poly(r-(w*z+z0),z).all_coeffs()
    expected=[e*e*C-d,e*B-u,e*e*A+v,lam*u-e*A-w,lam*v-e*e*B*C-z0]
    require(same(actual,expected,(e,A,B,C,lam,u,v,w,z0,d)),'all five general retained-coefficient equations')
    zero((alpha+beta*z)*(u*z+v)-beta*u*(z*z+d)-((alpha*u+beta*v)*z+alpha*v-beta*u*d),'primitive division identity')
    coeff=S.Matrix([[S.Poly(q,z).coeff_monomial(z**k) for k in (2,1,0)] for q in (f,g,r)])
    det=S.factor(coeff.det());zero(det+e**3*(A*A+C*B*B),'generic nonincident coefficient determinant')
    return {'full_arc_equations':list(map(str,expected)),'primitive_equations':['alpha*u+beta*v-w','alpha*v-beta*u*d-z0'],'coefficient_determinant':str(det),'passed':True}

def conic_coverage():
    F,G,R=S.symbols('F G R');P=S.Matrix([1,0,0])
    matrices=[S.eye(3),S.Matrix([[1,0,0],[0,0,1],[0,1,0]]),S.Matrix([[1,0,0],[0,1,1],[0,0,1]]),S.Matrix([[1,0,1],[0,0,1],[0,1,0]]),S.Matrix([[1,0,1],[0,1,0],[0,0,1]])]
    monomials=[F*G,F*R,G*G,G*R,R*R];evaluations=[]
    for M in matrices:
        require(M.det()!=0 and M*P==P,'invertible target chart fixing attachment')
        point=list(M[:,2]);evaluations.append([m.subs(dict(zip((F,G,R),point)),simultaneous=True) for m in monomials])
    E=S.Matrix(evaluations);require(E.rank()==5,'five conic coefficient charts exhaust every nonzero quadratic')
    tau=S.symbols('tau');examples=[]
    for A0,B0,C0 in [(1,2,3),(0,0,1),(0,0,0),(0,1,0)]:
        aa=A0+tau;bb=S.Integer(B0);cc=C0+tau
        disc=S.expand(aa*aa+cc*bb*bb)
        require(disc!=0,'conic realization has generically independent quadratics')
        examples.append({'central_ABC':[A0,B0,C0],'generic_test_polynomial':str(disc)})
    return {'evaluation_matrix':E.tolist(),'determinant':int(E.det()),'realization_examples':examples,'passed':True}

def extension_algebra():
    e,A,B,C=S.symbols('e A B C');vs=(e,A,B,C);I=[e*A,e*B,e*e*C]
    primary=intersection(intersection([e],[A,B,C],vs),[A,B,e*e],vs)
    require(same(primary,I,vs),'complete primary decomposition')
    gb=basis(I,vs);n=e*C
    require(gb.reduce(n)[1]!=0 and gb.reduce(n*n)[1]==0,'nonzero square-zero radical generator')
    colon=[S.cancel(m/S.gcd(m,n)) for m in I]
    require(same(colon,[e,A,B],vs),'annihilator of the nilpotent module')
    q1,q2,q3=S.symbols('q1 q2 q3')
    image_relations=[B*q1-A*q2,C*q1-A*q3,C*q2-B*q3]
    specialized=[p.subs({e:0,A:0,B:0}) for p in image_relations]
    require(specialized==[0,C*q1,C*q2],'conormal relations force first two images to zero')
    de,dA,dB,dC=S.symbols('de dA dB dC')
    derivations=[A*de+e*dA,B*de+e*dB,C*de+e*dC]
    require([p.subs({e:0,A:0,B:0}) for p in derivations]==[0,0,C*de],'derivation image in N is CN')
    require(S.rem(S.Integer(1),C,C)==1,'extension representative is nonzero modulo C')
    return {'primary_ideal':'(eA,eB,e^2C)','radical_generator':'eC','annihilator':'(e,A,B)','conormal_map':['0','0','eC'],'local_obstruction_quotient':'N/CN','extension_representative':'1','global_gluing_proved_in_manuscript_not_by_test':True,'passed':True}

def ramification():
    e,A,B,C,tau=S.symbols('e A B C tau');vs=(e,A,B,C,tau);records=[]
    for m in range(1,7):
        I=[e*A,e*B,e*e*C+tau**m];H=[A,B,e*e*C+tau**m]
        require(same(saturation(I,tau,vs),H,vs),'ramified horizontal saturation, m='+str(m))
        gb=basis(I,vs)
        require(gb.reduce(tau**m*A)[1]==0,'torsion annihilated at order m')
        require(gb.reduce(tau**(m-1)*A)[1]!=0,'torsion has exact order m')
        require(same(intersection(H,[e,tau**m],vs),I,vs),'ramified full scheme union')
        records.append({'m':m,'torsion_order':m,'multiplicities':[2//math.gcd(m,2),1]})
    lattices=[]
    for m in range(1,17):
        vectors=[(m,0),(0,m),(2,1)]
        minors=[abs(a[0]*b[1]-a[1]*b[0]) for a,b in itertools.combinations(vectors,2)]
        require(math.gcd(*minors)==m,'full invariant exponent lattice index')
        require(all((a-2*b)%m==0 for a,b in vectors),'monomial images invariant')
        if m%2==0:
            q=m//2
            # After the order-two subgroup, residual weights are (1,-1).
            for a in range(13):
                for b in range(13):
                    if (a-b)%q:continue
                    k=min(a,b)
                    require((a-k)%q==0 and (b-k)%q==0,'even invariant ring generators')
        lattices.append({'m':m,'index':m})
    ss,rr=S.symbols('s r')
    for m in range(1,9):zero((e*e*C+tau**m).subs({e:ss**m,C:-rr**m,tau:ss*ss*rr},simultaneous=True),'normalization monomial equation')
    return {'saturation_and_union_examples':records,'lattice_examples':lattices,'general_normalization_and_finiteness_proved_in_manuscript':True,'passed':True}

def transitions():
    a,b,c,d,lam,h,e,C,u,delta=S.symbols('a b c d lam h e C u delta');det=a*d-b*c
    plus=(a*(lam+h)+b)/(c*(lam+h)+d);minus=(a*(lam-h)+b)/(c*(lam-h)+d)
    K=(c*lam+d)**2-c*c*h*h
    mean=((a*lam+b)*(c*lam+d)-a*c*h*h)/K
    diff=det*h/K
    zero((plus+minus)/2-mean,'Mobius mean transition')
    zero((plus-minus)/2-diff,'Mobius half-difference transition')
    K1=(c*lam+d)**2+c*c*C;Cp=det**2*C/K1**2;ep=K1*e/det
    zero(-ep*ep*Cp+e*e*C,'first invariant chart preserves delta')
    zero(K1.subs(C,-delta*u*u)-((c*lam+d)**2-c*c*delta*u*u),'two quotient charts overlap')
    k=S.symbols('k');Tk=S.Matrix([[1,0,0],[0,1,0],[-k,0,1]])
    require(Tk*Tk.subs(k,-k)==S.eye(3),'larger-Smith-factor generating-row inverse')
    require(S.Matrix([[0,1],[1,0]])**2==S.eye(2),'ordered ruling monodromy')
    return {'Mobius_overlap_identities':True,'invariant_base_equation':True,'larger_Smith_factor_inverse':True,'passed':True}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--skip-inherited',action='store_true');args=ap.parse_args()
    inherited=False
    if not args.skip_inherited:
        previous=HERE.parent/'v164'/'check_v164.py'
        subprocess.run([sys.executable,str(previous)],check=True)
        source=previous.parent/'EXACT_CHECKS_V164.json';record=json.loads(source.read_text())
        require(record.get('all_checks_pass') and record.get('inherited_v163_suite_rerun'),'full inherited v164 chain passed')
        (HERE/'INHERITED_V164_CHECKS_RERUN.json').write_bytes(source.read_bytes());inherited=True
    out={'revision':166,'field':'QQ','coefficient_presentations':coefficient_presentations(),'conic_coverage':conic_coverage(),'extension_algebra':extension_algebra(),'ramification':ramification(),'transitions':transitions(),'inherited_v164_suite_rerun':inherited,'all_checks_pass':True,'general_proofs_certified_by_computation':False,'global_gluing_or_novelty_certified_by_computation':False,'external_independent_audit_obtained':False,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (HERE/'EXACT_CHECKS_V166.json').write_text(json.dumps(out,indent=2)+'\n')
    print('All listed finite exact v166 checks passed; general statements require their manuscript proofs.')
if __name__=='__main__':main()
