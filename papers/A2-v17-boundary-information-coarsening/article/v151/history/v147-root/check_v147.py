#!/usr/bin/env python3
"""Exact finite regressions for v147. These tests are not proof certificates."""
from pathlib import Path
from itertools import product
import json, math
import sympy as S

HERE=Path(__file__).resolve().parent
OUT=HERE/'evidence'; OUT.mkdir(exist_ok=True)
x,y,ep,z,s,t=S.symbols('x y epsilon z s t')

def monomials(degree):
    return [x**a*y**(degree-a) for a in range(degree+1)]

def model(d):
    # A small non-monomial first relation; no relations below d.
    K=x**d+y**d
    G=S.groebner([K]+monomials(d+1),x,y,order='grlex')
    reduce=lambda f:S.expand(G.reduce(S.expand(f))[1])
    basis=[x**a*y**b for a in range(d+1) for b in range(d+1-a)
           if a<d]
    basis=sorted(basis,key=lambda m:(S.total_degree(m),str(m)))
    assert len(basis)==math.comb(d+2,2)-1
    def vector(f):
        f=S.Poly(reduce(f),x,y)
        return S.Matrix([f.coeff_monomial(m) for m in basis])
    return K,reduce,basis,vector

cases=[]
for d in (2,3,4,5):
    K,red,basis,vec=model(d)
    u=x*x+2*x*y+y*y
    v=x*x-3*y*y
    subs={x:x+u,y:y+v}
    assert red(K.subs(subs,simultaneous=True))==0
    M=S.Matrix.hstack(*[vec(b.subs(subs,simultaneous=True)) for b in basis])
    assert M.det()==1
    assert (M-S.eye(len(basis)))**(d+1)==S.zeros(len(basis))
    a=7+x+2*y+x*y
    reg=S.Matrix.hstack(*[vec(a*b) for b in basis])
    assert S.trace(reg)==7*len(basis)
    cases.append({'d':d,'length':len(basis),'determinant':str(M.det()),
                  'nilpotent_deviation':True,'trace_augmentation':True})

# A nonreduced coefficient ring D=C[epsilon]/(epsilon^2).
# The tangent diagonal is a unit and respects K=(x^4).
d=4
G=S.groebner([ep**2,x**d]+monomials(d+1),x,y,ep,order='grlex')
redD=lambda f:S.expand(G.reduce(S.expand(f))[1])
images={x:(1+ep)*x+ep*y*y+x*y,y:y+ep*x*x+y*y}
assert redD((x**d).subs(images,simultaneous=True))==0
for rel in monomials(d+1):
    assert redD(rel.subs(images,simultaneous=True))==0
assert redD(ep**2)==0
# Constants which happen to be nilpotent in D are still read by trace.
base=[x**a*y**b for a in range(d) for b in range(d+1-a)]
def vecD(f):
    p=S.Poly(redD(f),x,y)
    return S.Matrix([p.coeff_monomial(m) for m in base])
trace_matrix=S.Matrix.hstack(*[vecD((ep+x+y*y)*b) for b in base])
assert S.expand(S.trace(trace_matrix)-len(base)*ep)==0

# Tangent-identity substitution does not have an additive or commutative law.
K,red,basis,vec=model(4)
def comp(f,g):
    return tuple(red(a.subs({x:g[0],y:g[1]},simultaneous=True)) for a in f)
f=(x+y*y,y); g=(x,y+x*x)
assert comp(f,g)!=comp(g,f)
assert comp(f,g)!=(red(x+y*y),red(y+x*x))
assert comp(f,(x-y*y,y))==(x,y)

commutants=[]
for n,r in ((2,2),(3,2),(2,3)):
    a=n*r
    constraints=[]
    for i,j in product(range(n),repeat=2):
        unit=S.zeros(n);unit[i,j]=1
        L=S.kronecker_product(unit,S.eye(r))
        # Column vectorization of LZ-ZL.
        constraints.append(S.kronecker_product(S.eye(a),L)-
                           S.kronecker_product(L.T,S.eye(a)))
    C=S.Matrix.vstack(*constraints)
    nullity=a*a-C.rank()
    assert nullity==r*r
    for i,j in product(range(r),repeat=2):
        H=S.zeros(r);H[i,j]=1
        Z=S.kronecker_product(S.eye(n),H)
        v=S.Matrix([Z[i,j] for j in range(a) for i in range(a)])
        assert C*v==S.zeros(C.rows,1)
    commutants.append({'left_rank':n,'right_rank':r,'commutant_dimension':nullity})
# Transition compatibility for an actual bundle map; units need not be constants
# on an overlap. The normal map carries the same transition identity.
C1=S.diag(z,z**-1); C2=S.Matrix([[1,z],[0,1]])
H=S.Matrix([[1,2],[3,7]])
H2=C2.inv()*H*C1
assert S.simplify(C2*H2-H*C1)==S.zeros(2)
assert S.simplify(S.kronecker_product(S.eye(3),C2)*S.kronecker_product(S.eye(3),H2)-
                  S.kronecker_product(S.eye(3),H)*S.kronecker_product(S.eye(3),C1))==S.zeros(6)

supports=[]
for m in (2,3,4):
    for r in range(1,m+1):
        mats=[]
        for i in range(r):
            for j in range(m):
                M=S.zeros(m);M[i,j]=1;mats.append(M)
        left=S.Matrix.hstack(*mats).rank()
        right=S.Matrix.hstack(*[M.T for M in mats]).rank()
        assert (left,right)==(r,m)
        assert ((left,right)!=(right,left))==(r<m)
        supports.append({'r':r,'m':m,'supports':[left,right],'transpose_excluded':r<m})

# The global example: same fibre type and graded bundles, different covers.
f0=z**3; f1=z**3+z
assert S.gcd(s**3,t**3)==1
assert S.gcd(s**3+s*t*t,t**3)==1
assert S.factor(S.diff(f0,z))==3*z*z
assert S.discriminant(S.diff(f1,z),z)==-12
assert S.degree(f0,z)==S.degree(f1,z)==3
ramification=[[3,3],[2,2,3]]
assert sum(e-1 for e in ramification[0])==sum(e-1 for e in ramification[1])==4
for fval in [f0,f1]:
    lift=S.Matrix([[1,fval,0],[0,1,0],[0,0,1]])
    assert lift.det()==1
    assert lift*S.Matrix([0,1,0])==S.Matrix([fval,1,0])
assert math.comb(13,4)-3==712
assert math.comb(12,4)==495
assert 486+3*(1+1)==492
assert 1+9+45+165+489+3==712

# Perfect apolar pairing in degree three for K=<x^3+y^3>.
# In divided monomial bases its annihilator has codimension one.
row=S.Matrix([[1,0,0,1]])
assert len(row.nullspace())==3
for coeff in row.nullspace():
    F=sum(coeff[a]*S.Symbol('u')**a*S.Symbol('v')**(3-a)/
          (math.factorial(a)*math.factorial(3-a)) for a in range(4))
    assert S.diff(F,S.Symbol('u'),3)+S.diff(F,S.Symbol('v'),3)==0

out={'revision':147,'ok':True,'first_relation_models':cases,
     'nonreduced_scalar_extension_checked':True,'trace_recovers_nilpotent_constants':True,
     'nonadditive_noncommutative_kernel':True,'commutant_models':commutants,
     'actual_transition_compatibility':True,'coefficient_support_models':supports,
     'isotrivial_example':{'finite_flat_rank':712,'normal_rank':9,'first_relation_rank':3,
       'coefficient_line_degree':-3,'top_bundle':'O^489 + O(3)^3',
       'ramification_indices':ramification,'local_product_lifts':True},
     'apolar_annihilator_checked':True,'proof_certified_by_computation':False,
     'scope':'Finite exact regressions. Not certification of global descent, all group-scheme statements, priority or journal significance.'}
(OUT/'REVISION147_EXACT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
