#!/usr/bin/env python3
"""Exact finite regressions for v146. These are not formal geometric proofs."""
from pathlib import Path
import json, math
import sympy as S
ROOT = Path(__file__).resolve().parent
E = ROOT / 'evidence'
E.mkdir(exist_ok=True)
s, t, z, c, x, y = S.symbols('s t z c x y')
P = z*(z-s)*(z-t)*(z-2*s-3*t)
expected = 4*s**2*t**2*(2*s+3*t)**2*(s-t)**2*(s+3*t)**2*(s+t)**2
assert S.expand(S.discriminant(P,z)-expected) == 0
chi = t*(s+3*t)/((2*s+3*t)*(t-s))
J = (c*c-c+1)**3/(c*c*(1-c)**2)
transforms = [c, 1/c, 1-c, 1/(1-c), c/(c-1), (c-1)/c]
for a in transforms:
    assert S.cancel(J.subs(c,a)-J) == 0
chi_values = [S.cancel(chi.subs({s:1,t:k})) for k in (2,3)]
assert chi_values == [S.Rational(7,4),S.Rational(15,11)]
J_values = [S.cancel(J.subs(c,a)) for a in chi_values]
assert J_values[0] != J_values[1]
assert S.cancel(S.diff(J.subs(c,chi).subs(s,1),t)) != 0
# The three constant sections A, B0, B1 are linearly independent.
A=S.Matrix([1,1,1,1]); B0=S.Matrix([0,1,0,2]); B1=S.Matrix([0,0,1,3])
assert S.Matrix.hstack(A,B0,B1).rank()==3
# Every listed collision is included, with A still invertible and the pencil rank two.
collisions=[(0,1),(1,0),(-3,2),(1,1),(-3,1),(-1,1)]
for a,b in collisions:
    assert expected.subs({s:a,t:b})==0
    assert S.Matrix.hstack(A,a*B0+b*B1).rank()==2
assert len({S.Rational(a,b) if b else 'infinity' for a,b in collisions})==6
# Pluecker direction at [1:2], in diagonal coordinates, is not lost to scalar rescaling.
def wedge(a,b):
    return S.Matrix([a[i]*b[j]-a[j]*b[i] for i in range(4) for j in range(i+1,4)])
beta=wedge(A,B0+2*B1); tangent=wedge(A,B1)
assert S.Matrix.hstack(beta,tangent).rank()==2
K=S.kronecker_product(beta,S.eye(3))
assert K.rank()==3
# Contraction against the entire right factor recovers exactly the varying left line.
contracted=S.Matrix.hstack(*[S.Matrix([K[3*i+r,j] for i in range(6)]) for r in range(3) for j in range(3)])
assert contracted.rank()==1
assert S.Matrix.hstack(contracted,beta).rank()==1
# Shear invariance in a truncation: homogeneous top relations change only above d.
def trunc(f,d):
    p=S.Poly(S.expand(f),x,y)
    return S.Add(*[a*x**m[0]*y**m[1] for m,a in p.terms() if sum(m)<=d])
shear_cases=0
for d in (11,20):
    for a in range(d+1):
        f=x**a*y**(d-a)
        assert trunc(f.subs(x,x+y*y)-f,d)==0
        shear_cases+=1
    assert trunc((x+y*y).subs(x,x-y*y),d)==x
    assert trunc(y*y,d)!=0
# Explicit commutator: a shift-one and a shift-two substitution have shift at least three.
D=7
def compose(f,g):
    return tuple(trunc(a.subs({x:g[0],y:g[1]}, simultaneous=True),D) for a in f)
f=(x+y*y,y); fi=(x-y*y,y)
g=(x,y+x**3); gi=(x,y-x**3)
comm=compose(compose(compose(f,g),fi),gi)
for a,b in zip(comm,(x,y)):
    q=S.Poly(S.expand(a-b),x,y)
    assert all(sum(m)>=4 for m,v in q.terms() if v)
assert comm!=(x,y)
rows=[]
for n in range(3,9):
    N=n*(n+1)//2;p=N-2;d=n+2*p;M=math.comb(N,2)
    rank=math.comb(n*n+d,d)-M
    assert d==n*n+2*n-4 and rank>0 and (-1)%n!=0
    rows.append({'n':n,'N':N,'p':p,'d':d,'relation_rank':M,'finite_rank':rank})
result={'ok':True,'revision':146,'discriminant':str(S.factor(expected)),
 'cross_ratio_values':list(map(str,chi_values)),'unordered_invariant_values':list(map(str,J_values)),
 'six_cross_ratio_symmetries':True,'six_collision_points_retained':True,
 'pencil_bundle_rank_everywhere_argument':'constant A,B0,B1 independent; B0*s+B1*t not scalar A',
 'nonzero_pluecker_tangent_mod_scalars':True,'full_right_factor_contraction':True,
 'top_degree_shear_cases':shear_cases,'filtered_commutator_shift_three':True,
 'dimension_checks':rows,'proof_certified':False,
 'scope':'Finite exact calculations only. Not a formal verification of the intrinsic inverse, group exactness, priority, significance or all inherited proofs.'}
(E/'REVISION146_EXACT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
