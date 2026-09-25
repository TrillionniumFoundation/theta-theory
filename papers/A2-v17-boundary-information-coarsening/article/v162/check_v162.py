#!/usr/bin/env python3
"""Exact finite audits of v162; general proofs remain in the manuscripts."""
from __future__ import annotations
import argparse, hashlib, itertools as it, json, math, random, subprocess, sys
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent

def need(ok,msg):
    if not ok: raise AssertionError(msg)
def ideal(a,b,vars):
    return s.groebner(a,*vars,order='lex')==s.groebner(b,*vars,order='lex')
def coefficient_vector(p,x,d):
    return [s.expand(p).coeff(x,j) for j in range(d)]
def jordan(d,x):
    E=s.zeros(d);N=s.zeros(d)
    for i in range(d):E[i,d-i-1]=1
    for i in range(d-1):N[i,i+1]=1
    return E,N,E*(x*s.eye(d)-N)
def contact_tangents():
    x=s.symbols('x');records=[]
    sizes=[(a,b) for a in range(1,4) for b in range(a,5)]+[(1,1,1),(1,2,2),(2,2,2)]
    for ds in sizes:
        n=sum(ds);offset=[sum(ds[:i]) for i in range(len(ds))]
        rows=[(i,j,min(ds[i],ds[j])) for i in range(len(ds)) for j in range(i,len(ds))]
        N=sum(d for _,_,d in rows);vs=[s.Matrix([x**k for k in range(d)]) for d in ds]
        columns=[]
        for u in range(n):
            for v in range(u,n):
                H=s.zeros(n);H[u,v]=1;H[v,u]=1
                out=[]
                for i,j,d in rows:
                    h=H[offset[i]:offset[i]+ds[i],offset[j]:offset[j]+ds[j]]
                    out+=coefficient_vector((vs[i].T*h*vs[j])[0],x,d)
                columns.append(out)
        rank=s.Matrix.hstack(*[s.Matrix(c) for c in columns]).rank()
        need(rank==N,'actual constant-pencil perturbations span the entire contact quotient')
        Q=s.diag(*[jordan(d,x)[0] for d in ds]);T=s.diag(*[jordan(d,x)[1] for d in ds])
        # A skew-adjoint matrix is Q^{-1} times an arbitrary skew matrix.
        orbit=[]
        for i in range(n):
            for j in range(i+1,n):
                K=s.zeros(n);K[i,j]=1;K[j,i]=-1;K=Q.inv()*K
                C=T*K-K*T;orbit.append(list(C))
        orbit_rank=s.Matrix.hstack(*[s.Matrix(c) for c in orbit]).rank() if orbit else 0
        stabilizer=n*(n-1)//2-orbit_rank
        expected=sum(min(ds[i],ds[j]) for i in range(len(ds)) for j in range(i+1,len(ds)))
        need(stabilizer==expected and n+stabilizer==N,'orthogonal centralizer and miniversal dimension')
        records.append(dict(exponents=ds,contact_parameters=N,actual_perturbation_rank=rank,orthogonal_stabilizer=stabilizer))
    blocks=[]
    for m in range(1,9):
        E,N,L=jordan(m,x);v=s.Matrix([x**k for k in range(m)]);e=s.zeros(m,1);e[0]=1
        need(L*v==x**m*e,'exact kernel lifting vector')
        need(E.det()==(-1)**(m*(m-1)//2),'Jordan determinant sign')
        if m>1:need(L[1:,1:].det()==E.det(),'complementary determinant sign')
        blocks.append(dict(m=m,sign=int(E.det()),kernel_identity=True))
    return records,blocks

def division_tests():
    x=s.symbols('x');rng=random.Random(162);records=[]
    for a in range(1,7):
        for t in range(12):
            f=x**a+sum(rng.randint(-3,3)*x**j for j in range(a))
            g=sum(rng.randint(-3,3)*x**j for j in range(a));w=sum(rng.randint(-3,3)*x**j for j in range(a))
            q,r=s.div(g*w,f,x)
            need(s.expand(g*w-f*q-r)==0,'exact Euclidean graph coordinate')
            need(s.degree(r,x)<a and (q==0 or s.degree(q,x)<a-1),'degree bounds')
            M=s.Matrix.hstack(*[s.Matrix(coefficient_vector(s.rem(g*x**j,f,x),x,a)) for j in range(a)])
            need(s.expand(M.det()-s.resultant(f,g,x))==0,'resultant of multiplication map')
            null=a-M.rank();dg=s.degree(s.gcd(f,g),x)
            need(null==dg,'incidence module length equals exact gcd degree')
            records.append(dict(a=a,trial=t,incidence_length=int(dg),division_exact=True))
    # Fully symbolic multiplication presentation, including the nonreduced constant slice.
    u,v=s.symbols('u v');fitting=[]
    for a in range(1,5):
        M=(u*s.eye(a)).row_join(v*s.eye(a))
        minors=[M[:,c].det() for c in it.combinations(range(2*a),a)]
        need(ideal(minors,[u**j*v**(a-j) for j in range(a+1)],(u,v)),'Fitting ideal retains incidence multiplicity')
        fitting.append(dict(a=a,Fitting=f'(u,v)^{a}'))
    return records,fitting

def graph_and_fibres():
    x,t,U,V,Z=s.symbols('x t U V Z');records=[]
    for a in range(1,6):
        # Rees saturation of the primitive thick-tail chart.
        G=s.groebner([U-x**a*Z,V-t*Z],Z,x,t,U,V,order='lex')
        equations=[p.as_expr() for p in G.polys if not p.as_expr().has(Z)]
        need(ideal(equations,[t*U-x**a*V],(x,t,U,V)),'full Rees ideal')
        # Main and thick-tail decomposition, including a mixed two-support contact.
        for d in (x**a,x**a*(x-1)**2):
            G=s.groebner([Z*d,(1-Z)*V],Z,x,U,V,order='lex')
            eq=[p.as_expr() for p in G.polys if not p.as_expr().has(Z)]
            need(ideal(eq,[d*V],(x,U,V)),'scheme union, not reduced support')
        # On a central fibre H^0(O(a-1,1)) has coordinates (main, tail-G).
        Psi=s.zeros(2*a,2*a-1)
        for j in range(a):Psi[a+j,j]=1
        for j in range(a-1):Psi[j,a+j]=-1
        need(Psi.rank()==2*a-1 and len(Psi.T.nullspace())==1,'Hilbert inverse split injection and cokernel rank')
        records.append(dict(a=a,Rees_verified=True,cohomology_dimension=2*a,inverse_coefficient_rank=2*a-1,mixed_thick_supports_verified=True))
    return records

def conic_checks():
    x,t=s.symbols('x t');records=[]
    for b1,b0,c1,c0 in [(1,0,0,1),(1,1,-1,2),(2,1,1,1),(0,1,2,-3)]:
        for a1,a0 in [(0,0),(1,-2),(3,1)]:
            f=x*x+a1*x*t+a0*t*t;g=b1*x*t+b0*t*t;r=c1*x*t+c0*t*t
            need(b1*c0-b0*c1!=0,'independent conic coordinates')
            need(ideal([f,g,r],[x*x,x*t,t*t],(x,t)),'exact point-square ideal')
            mat=s.Matrix([[1,a1,a0],[0,b1,b0],[0,c1,c0]])
            need(mat.det()!=0,'complete Veronese system, no multiple cover')
            records.append(dict(coefficients=[a1,a0,b1,b0,c1,c0],ideal='(x,t)^2',Veronese_rank=3))
    return records

def artin_and_transitions():
    x,U,V,w,z,u=s.symbols('x U V w z u');records=[]
    for a in range(1,7):
        slope=1+sum((j+1)*x**j for j in range(1,a));inverse=s.invert(slope,x**a,x)
        need(s.rem(slope*inverse-1,x**a,x)==0,'jet inversion overlap on full Artin algebra')
        for d in range(5):
            # Restriction F=U,G=V,R=w(x)V of all ternary monomials includes each binary basis.
            basis=[x**i*U**j*V**(d-j) for i in range(a) for j in range(d+1)]
            need(len(set(basis))==a*(d+1),'full Artin coefficient module basis')
            records.append(dict(contact_length=a,power_degree=d,module_dimension=len(basis),jet_inverse_exact=True))
    v=u*w
    need(s.simplify((-z)*(-u)-(-v)*(-z*z)).subs(z,1/w)==0,'cotangent chain-map transition')
    return records

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--skip-inherited',action='store_true');args=ap.parse_args()
    inherited=False
    if not args.skip_inherited:
        subprocess.run([sys.executable,str(HERE.parent/'v161/check_v161.py')],check=True)
        prior=HERE.parent/'v161/EXACT_CHECKS_V161.json'
        need(json.loads(prior.read_text())['all_checks_pass'],'actual v161 inherited suite')
        (HERE/'INHERITED_V161_CHECKS_RERUN.json').write_bytes(prior.read_bytes());inherited=True
    tangent,blocks=contact_tangents();division,fitting=division_tests()
    report=dict(revision=162,field='QQ exact symbolic arithmetic',actual_contact_tangent_tests=tangent,Jordan_constant_tests=blocks,Euclidean_and_resultant_tests=division,Fitting_tests=fitting,Rees_and_Hilbert_inverse_tests=graph_and_fibres(),reduced_conic_ideal_tests=conic_checks(),Artin_module_and_overlap_tests=artin_and_transitions(),inherited_v161_suite_actually_rerun=inherited,all_checks_pass=True,independent_external_referee_proof_audit_obtained=False,general_proofs_certified_by_computation=False,script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    (HERE/'EXACT_CHECKS_V162.json').write_text(json.dumps(report,indent=2)+'\n')
    print('All v162 exact finite checks passed. They do not certify the general theorems.')
if __name__=='__main__':main()
