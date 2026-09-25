#!/usr/bin/env python3
"""Exact finite audits for v158; these are not certificates of general proofs."""
from __future__ import annotations
import argparse, hashlib, importlib.util, itertools as it, json, subprocess, sys
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('checks157',HERE.parent/'v157'/'check_v157.py')
old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)

def require(test: bool, message: str) -> None:
    if not test: raise AssertionError(message)

def singular_block(e: int):
    a,b=s.symbols('a b');L=s.zeros(e,e+1)
    for i in range(e):L[i,i]=a;L[i,i+1]=b
    A=s.zeros(2*e+1)
    if e:
        A[:e+1,e+1:]=L.T;A[e+1:,:e+1]=L
    return A

def regular_block(k: int):
    a,b=s.symbols('a b');J=s.zeros(k);T=s.zeros(k)
    for i in range(k):T[i,k-1-i]=1
    for i in range(k-1):J[i,i+1]=1
    A=T*(a*s.eye(k)+b*J)
    require(A==A.T,'symmetric regular Kronecker block')
    return A

def toeplitz(A, j: int):
    a,b=s.symbols('a b');A0=A.subs({a:1,b:0});A1=A.subs({a:0,b:1});n=A.rows
    C=s.zeros(n*(j+2),n*(j+1))
    for i in range(j+1):
        C[i*n:(i+1)*n,i*n:(i+1)*n]=A0
        C[(i+1)*n:(i+2)*n,i*n:(i+1)*n]=A1
    return C

def syzygies():
    a,b=s.symbols('a b');cases=[]
    specs=[((e,),k) for e in range(4) for k in (0,1,2) if 2*e+1+k>=3]
    specs += [((0,2),0),((1,1),0),((0,1),2),((1,2),1),((0,0,1),1),((0,0),3)]
    for es,k in specs:
        mats=[singular_block(e) for e in es]
        if k:mats.append(regular_block(k))
        A=s.diag(*mats);n=A.rows;r=n-len(es);got=[]
        for j in range((n-1)//2+1):
            C=toeplitz(A,j);v=C.cols-C.rank();got.append(v)
            require(v==sum(max(j-e+1,0) for e in es),'exact Toeplitz nullity')
        ext=[0,0]+got
        recovered=[ext[j+2]-2*ext[j+1]+ext[j] for j in range(len(got))]
        require(recovered==[es.count(j) for j in range(len(got))],'minimal-index inversion')
        require(A.subs({a:2,b:3}).rank()==r,'generic normal rank')
        # Independent rational Grassmannian map: maximal minors of kernel vectors.
        columns=[];offset=0
        for e in es:
            col=s.zeros(n,1)
            for i in range(e+1):col[offset+i]=a**i*(-b)**(e-i)
            require(A*col==s.zeros(n,1),'homogeneous kernel vector')
            columns.append(col);offset+=2*e+1
        K=s.Matrix.hstack(*columns);coeff=[]
        for idx in it.combinations(range(n),len(es)):
            f=s.expand(K.extract(idx,range(len(es))).det())
            if f:coeff.append(f)
        gcd=s.polys.polytools.terms_gcd(coeff[0])
        for f in coeff[1:]:gcd=s.gcd(gcd,f)
        require(s.Poly(gcd,a,b).total_degree()==0,'kernel Pluecker has no common factor')
        degree=s.Poly(coeff[0],a,b).total_degree()
        require(degree==sum(es),'image-plane Pluecker degree')
        require(k+2*degree==r,'global conservation on canonical blocks')
        cases.append({'minimal_indices':list(es),'regular_block_size':k,'n':n,'normal_rank':r,'nullities':got,'image_plane_degree':degree})
    return cases

def top_power_chart():
    x,y,u,v,w=s.symbols('x y u v w')
    U=s.Matrix([[1,0],[0,1],[x,y]]);H=s.Matrix([[u,v],[v,w]]);A=U*H*U.T
    pairs=list(it.combinations(range(3),2));pl=s.Matrix([U.extract(i,[0,1]).det() for i in pairs])
    compound=s.Matrix([[A.extract(i,j).det() for j in pairs] for i in pairs])
    require(compound.applyfunc(s.expand)==(H.det()*pl*pl.T).applyfunc(s.expand),'exact rank-two compound factorization')
    require(A.det()==0,'rank-two determinant vanishing')
    return {'ambient_dimension':3,'rank':2,'symbolic_compound_equals_detH_times_pluecker_square':True,'Grassmannian_coordinates':[str(z) for z in pl]}

def tail_ideals():
    z,t,u=s.symbols('z t u');xx,X=old.symmetric(3,'x');A=s.diag(z,z+t,1);rows=[]
    for h in (1,2,3):
        F=s.Poly(s.expand((X+u*A).det()**h),u)
        for p in range(1,3*h+1):
            coefficients=s.Poly(F.nth(p),*xx).coeffs()
            b=p-h
            if b<=0:expected=[s.Integer(1)]
            elif b<=h:expected=[z**j*t**(b-j) for j in range(b+1)]
            else:expected=[(z*(z+t))**(b-h)*z**j*t**(2*h-b-j) for j in range(2*h-b+1)]
            G=s.groebner(coefficients,z,t,domain=s.QQ);H=s.groebner(expected,z,t,domain=s.QQ)
            require(G==H,'tail ideals from determinant coefficients over QQ[z,t]')
            rows.append({'h':h,'p':p,'groebner_basis':[str(q.as_expr()) for q in G.polys]})
    # Scheme charts of the blow-up at the point, with a reduced nodal fibre.
    v=s.symbols('v');require(s.factor(z*v)==z*v,'nodal chart')
    require(s.gcd(z,v)==1,'distinct reduced chart factors')
    return rows

def tail_linear_systems():
    x,y,scale=s.symbols('x y scale');rows=[]
    for n in range(3,7):
        for h in range(1,5):
            for p in range(1,n*h+1):
                exponents=[ex for ex in it.product(range(h+1),repeat=n) if sum(ex)==p]
                valuation=min(ex[0]+ex[1] for ex in exponents)
                leading=[x**ex[0]*(x+y)**ex[1] for ex in exponents if ex[0]+ex[1]==valuation]
                b=p-h*(n-2);degree=0 if b<=0 else min(b,2*h-b)
                common=(x*(x+y))**max(b-h,0)
                reduced=[s.cancel(f/common) for f in leading]
                span=old.canonical(reduced,(x,y));expected=old.canonical([x**j*y**(degree-j) for j in range(degree+1)],(x,y))
                require(span==expected,'complete tail Veronese coefficient space')
                rows.append({'n':n,'h':h,'p':p,'degree':degree,'dimension':len(span)})
    return rows

def spectral_block_test():
    a,b=s.symbols('a b');rows=[]
    for e,k in [(0,2),(1,2),(1,3),(2,2)]:
        A=s.diag(singular_block(e),regular_block(k));At=A.subs(b,1);r=2*e+k;vals=[]
        for q in range(1,r+1):
            values=[]
            for rr in it.combinations(range(A.rows),q):
                for cc in it.combinations(range(A.rows),q):
                    f=s.expand(At.extract(rr,cc).det())
                    if f:values.append(min(t[0] for t,c in s.Poly(f,a).terms()))
            vals.append(min(values))
        recovered=[vals[0]]+[vals[i]-vals[i-1] for i in range(1,r)]
        require(recovered==[0]*(r-1)+[k],'Smith exponents of mixed symmetric pencil')
        rows.append({'minimal_index':e,'regular_block':k,'minor_valuations':vals,'nonzero_Smith_exponents':recovered})
    return rows

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--skip-inherited',action='store_true');args=ap.parse_args()
    inherited=False
    if not args.skip_inherited:
        subprocess.run([sys.executable,str(HERE.parent/'v157'/'check_v157.py')],check=True)
        receipt=HERE.parent/'v157'/'EXACT_CHECKS_V157.json'
        require(json.loads(receipt.read_text())['all_checks_pass'],'inherited v157 suite')
        (HERE/'INHERITED_V157_CHECKS_RERUN.json').write_bytes(receipt.read_bytes());inherited=True
    out={'revision':158,'field':'QQ','syzygy_tests':syzygies(),'top_power_chart':top_power_chart(),'tail_ideal_tests':tail_ideals(),'tail_linear_systems':tail_linear_systems(),'mixed_spectral_tests':spectral_block_test(),'inherited_v157_suite_rerun':inherited,'historical_28_checks_rerun':False,'general_proofs_certified_by_computation':False,'all_checks_pass':True,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (HERE/'EXACT_CHECKS_V158.json').write_text(json.dumps(out,indent=2)+'\n')
    print('All exact v158 checks passed. These are finite checks, not a general proof certificate.',flush=True)
if __name__=='__main__':main()
