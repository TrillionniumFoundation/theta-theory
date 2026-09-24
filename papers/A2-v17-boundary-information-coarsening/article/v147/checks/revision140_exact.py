#!/usr/bin/env python3
"""Exact symbolic regressions for spectral specialization over Q(i)(t).
These are finite identities, not a formal verification of the global theorems.
"""
from pathlib import Path
from itertools import combinations
import hashlib,json,math
import sympy as s
ROOT=Path(__file__).resolve().parents[1]
t,z,x,u=s.symbols('t z s u')
I=s.eye(2);O=s.zeros(2);N=s.Matrix([[1,s.I],[s.I,-1]])
P=t*N/2; A=O.row_join(I).col_join(I.row_join(O))
C=P.row_join(I).col_join(O.row_join(P));B=A*C
zero=lambda M:all(s.simplify(q)==0 for q in M)
checks={}
checks['symmetric_pair']=A==A.T and B==B.T
checks['nilpotent_rank_one_N']=zero(N*N) and N.rank()==1
checks['factorization_all_t']=zero(C-I.col_join(P)*P.row_join(I))
checks['power_formula_all_t']=zero(C*C-O.row_join(t*N).col_join(O.row_join(O))) and zero(C**3)
checks['determinant_all_t']=s.factor((x*A+u*B).det())==x**4
checks['rank_two_all_t_kernel']=zero(C*I.col_join(-P)) and C[:2,2:]==I
checks['ranks_at_generic_and_special']=(C.rank(),(C*C).rank(),C.subs(t,0).rank(),(C*C).subs(t,0).rank())==(2,1,2,0)
checks['fixed_complement']=s.simplify(A[0,2]+s.I*A[0,3])==1 and s.simplify(B[0,2]+s.I*B[0,3])==0 and A[2,2]==0 and B[2,2]==1
# Independent Smith determinantal divisors, exact over Q(i,t)[z].
K=s.QQ_I.frac_field(t)
def gcd_minors(M,k,domain):
    vals=[]
    for rr in combinations(range(M.rows),k):
        for cc in combinations(range(M.cols),k):
            v=s.expand(M.extract(rr,cc).det())
            if v!=0: vals.append(s.Poly(v,z,domain=domain))
    if not vals:return s.Poly(0,z,domain=domain)
    g=vals[0]
    for v in vals[1:]:g=s.gcd(g,v)
    return g.monic()
Mg=z*s.eye(4)+C;Ms=Mg.subs(t,0)
generic=[gcd_minors(Mg,k,K).as_expr() for k in range(1,5)]
special=[gcd_minors(Ms,k,s.QQ_I).as_expr() for k in range(1,5)]
checks['full_determinantal_divisors']=generic==[1,1,z,z**4] and special==[1,1,z**2,z**4]
checks['inverse_formula']=zero((x*s.eye(4)+u*C)*(x*x*s.eye(4)-x*u*C+u*u*C*C)-x**3*s.eye(4))
vec=lambda M:s.Matrix(list(M))
checks['reciprocal_spans']=s.Matrix.hstack(vec(s.eye(4)),vec(C),vec(C*C)).rank()==3 and s.Matrix.hstack(vec(s.eye(4)),vec(C.subs(t,0))).rank()==2
checks['length_profiles']=[sum(min(a,e) for e in (3,1)) for a in (1,2,3,4)]==[2,3,4,4] and [sum(min(a,e) for e in (2,2)) for a in (1,2,3,4)]==[2,4,4,4]
spectator=[]
for n in range(4,9):
    tails=list(range(1,n-3));An=s.diag(A,s.eye(n-4)) if n>4 else A
    Bn=s.diag(B,*tails) if n>4 else B
    want=x**4*s.prod(x+q*u for q in tails)
    assert s.factor((x*An+u*Bn).det()-want)==0
    for tv in (0,1,s.I):
        assert Bn.subs(t,tv).rank()==n-2
        for q in tails:assert (-q*An+Bn.subs(t,tv)).rank()==n-1
    Nn=n*(n+1)//2;d=n*n+2*n-4
    length=math.comb(n*n+d,d)-math.comb(Nn,2)
    assert d==n+2*(Nn-2) and length>0
    spectator.append({'n':n,'d':d,'finite_flat_rank':length})
checks['spectator_formula_dimensions_4_to_8']=True
out={'revision':140,'ok':all(checks.values()),'checks':checks,
     'coefficient_domain':'Q(i)(t), exact symbolic arithmetic',
     'minor_gcds':{'generic':[str(q) for q in generic],'special':[str(q) for q in special]},
     'spectator_cases':spectator,
     'not_machine_certified':['intrinsic recovery of the entire projective socle neighbourhood',
       'global flatness and arbitrary base change of the relation subbundle',
       'all-dimensional spectral sheaf classification proof',
       'historical exhaustiveness or journal-level significance'],
     'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(ROOT/'evidence').mkdir(exist_ok=True)
(ROOT/'evidence/REVISION140_EXACT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
assert out['ok']
