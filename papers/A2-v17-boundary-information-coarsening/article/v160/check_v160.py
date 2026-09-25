#!/usr/bin/env python3
"""Exact finite audits of incidence, graph saturation and exceptional powers.
The manuscript contains the general proofs. These finite calculations are
independent checks of their equations, not proof or novelty certificates.
"""
from __future__ import annotations
import argparse, hashlib, importlib.util, itertools as it, json, math, subprocess, sys
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('checks157',HERE.parent/'v157'/'check_v157.py')
old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
def require(ok:bool,message:str)->None:
    if not ok:raise AssertionError(message)
def mons(variables,degree):
    return [s.prod(v**e for v,e in zip(variables,ex))
            for ex in it.product(range(degree+1),repeat=len(variables)) if sum(ex)==degree]
def incidence_ideals():
    x,u,v,t,w=s.symbols('x u v t w');out=[]
    for n in range(3,8):
        A=s.diag(s.eye(n-2),s.Matrix([[x+u,v],[v,x-u]]))
        minors=[s.expand(A.extract(rows,cols).det())
                for rows in it.combinations(range(n),n-1)
                for cols in it.combinations(range(n),n-1)]
        minors=[f for f in minors if f!=0]
        require(s.groebner(minors,x,u,v)==s.groebner([x,u,v],x,u,v),'universal simple-incidence ideal')
        pulled=[f.subs({u:t,v:t*w}) for f in minors]
        require(s.groebner(pulled,x,t,w)==s.groebner([x,t],x,t,w),'base blow-up image ideal')
        require(s.expand(A.det()-(x*x-u*u-v*v))==0,'Schur determinant')
        out.append({'n':n,'incidence_ideal':'(x,u,v)','pulled_ideal':'(x,t)','exact':True})
    return out
def graph_saturation():
    z,x,t,w,X,U,V=s.symbols('z x t w X U V')
    naive=[x*U-t*X,x*V-t*w*X,t*V-t*w*U]
    saturated=s.groebner(naive+[1-z*t],z,x,t,w,X,U,V,order='lex')
    elimination=[p.as_expr() for p in saturated.polys if not p.as_expr().has(z)]
    actual=s.groebner(elimination,x,t,w,X,U,V)
    expected=s.groebner([V-w*U,x*U-t*X],x,t,w,X,U,V)
    require(actual==expected,'remove vertical Rees torsion before specialization')
    require(s.expand((x*U-t*X).subs({X:1,t:0}))==x*U,'reduced two-branch node')
    # The special principal ideal is (x) intersect (U), with two distinct primes.
    require(s.gcd(x,U)==1 and s.lcm(x,U)==x*U,'no multiplicity in the nodal chart')
    return {'saturated_graph':['V-w*U','x*U-t*X'],'node_chart':'x*U=t',
            'special_node':'x*U=0','saturation_and_reducedness_checks':True}
def exceptional_coefficients():
    aa,A=old.symmetric(2,'a');xx,X=old.symmetric(2,'x');z=s.symbols('z')
    f=A.det();records=[];line_records=[];q,r=s.symbols('q r')
    # Three rational lines, including tangent contact and a rank-one attachment.
    lines=[('ordinary',[q+r,r,q-r]),('tangent_at_attachment',[q,r,0]),
           ('ordinary_rank_one_attachment',[q,r,r])]
    for h in range(1,5):
        F=s.Poly(s.expand((X+z*A).det()**h),z)
        for b in range(1,2*h+1):
            coeff=s.Poly(F.nth(b),*xx).coeffs();common=max(b-h,0);degree=b-2*common
            reduced=[s.cancel(c/f**common) for c in coeff]
            require(old.canonical(reduced,aa)==old.canonical(mons(aa,degree),aa),'complete exceptional plane coefficient space')
            records.append({'h':h,'residual_power':b,'determinant_factor':common,
                            'degree':degree,'dimension':math.comb(degree+2,2),'exact_span':True})
            for name,values in lines:
                subst=dict(zip(aa,values));restricted=[s.expand(c.subs(subst,simultaneous=True)) for c in reduced]
                require(old.canonical(restricted,(q,r))==old.canonical(mons((q,r),degree),(q,r)),'all tail coefficient spaces including tangencies')
                line_records.append({'line':name,'h':h,'residual_power':b,'degree':degree,'rank':degree+1})
    alpha,beta=s.symbols('alpha beta')
    T=s.Matrix([[q+alpha*r,beta*r],[beta*r,q-alpha*r]])
    require(s.expand(T.det()-(q*q-(alpha*alpha+beta*beta)*r*r))==0,'displayed two-parameter determinant')
    require(s.expand(T.det().subs({alpha:1,beta:s.I}))==q*q,'complex tangential direction')
    return records,line_records
def numerical_profiles():
    records=[]
    for n in range(3,17):
        main=sum(q-int(q==n-1) for q in range(1,n));tail=1
        require(main+tail==math.comb(n,2),'Hilbert degree conservation')
        for h in range(1,5):
            ds=[max(j-h*(n-2),0)-2*max(j-h*(n-1),0) for j in range(1,n*h+1)]
            require(min(ds)>=0 and sum(ds)==h*h,'exceptional degree and graph exponent')
            require(ds[h*(n-2)]==1 and ds[-1]==0,'centre-selecting and top powers')
            records.append({'n':n,'h':h,'main_degree':main,'tail_degree':tail,'Hilbert_constant':1,'graph_ideal_exponent':sum(ds)})
    return records
def main()->None:
    ap=argparse.ArgumentParser();ap.add_argument('--skip-inherited',action='store_true');args=ap.parse_args()
    inherited=False
    if not args.skip_inherited:
        subprocess.run([sys.executable,str(HERE.parent/'v159'/'check_v159.py')],check=True)
        p=HERE.parent/'v159'/'EXACT_CHECKS_V159.json'
        require(json.loads(p.read_text())['all_checks_pass'],'actual inherited v159 suite')
        (HERE/'INHERITED_V159_CHECKS_RERUN.json').write_bytes(p.read_bytes());inherited=True
    planes,lines=exceptional_coefficients()
    record={'revision':160,'field':'QQ, with the displayed tangential specialization in QQ(i)',
            'incidence_ideal_tests':incidence_ideals(),'Rees_graph_saturation':graph_saturation(),
            'exceptional_plane_coefficient_tests':planes,'exceptional_line_coefficient_tests':lines,
            'multidegree_and_graph_exponent_tests':numerical_profiles(),
            'inherited_v159_suite_rerun':inherited,'historical_28_checks_rerun':False,
            'general_proofs_certified_by_computation':False,'all_checks_pass':True,
            'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (HERE/'EXACT_CHECKS_V160.json').write_text(json.dumps(record,indent=2)+'\n')
    print('All exact v160 checks passed; finite audits, not general proof certificates.',flush=True)
if __name__=='__main__':main()
