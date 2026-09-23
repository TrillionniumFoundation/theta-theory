#!/usr/bin/env python3
"""Exact coordinate checks supporting, not certifying, the written v133 proofs."""
from itertools import combinations
from pathlib import Path
from math import comb, prod
import json
import sympy as s

ROOT = Path(__file__).resolve().parents[1]
x = s.symbols('x1:5')
mon = [x[i]*x[j] for i in range(4) for j in range(i, 4)]
exp = [s.Poly(m, *x).monoms()[0] for m in mon]

def sign_sort(indices):
    if len(set(indices)) != len(indices):
        return 0, ()
    return (-1)**sum(indices[i] > indices[j]
                    for i in range(len(indices)) for j in range(i+1,len(indices))), tuple(sorted(indices))

def raising(I, i, j):
    ans = {}
    for pos, k in enumerate(I):
        derivative = s.Poly(x[i]*s.diff(mon[k], x[j]), *x)
        for new, n in enumerate(mon):
            c = derivative.coeff_monomial(n)
            if c:
                J = list(I); J[pos] = new
                sign, ordered = sign_sort(J)
                if sign:
                    ans[ordered] = ans.get(ordered, 0) + sign*c
    return {k:v for k,v in ans.items() if v}

def weight(I):
    return tuple(sum(exp[k][i] for k in I) for i in range(4))

def dim_schur(lam):
    return s.prod(s.Rational(lam[i]-lam[j]+j-i, j-i)
                  for i in range(4) for j in range(i+1,4))

highest = [((0,1,2,3,4,5), (5,4,2,1)),
           ((0,1,2,4,5,7), (4,4,4,0)),
           ((0,1,2,4), (4,3,1,0)),
           ((0,1,2,3), (5,1,1,1))]
for I, lam in highest:
    assert weight(I) == lam
    for i in range(4):
        for j in range(i+1,4):
            assert not raising(I, i, j), (I,i,j)
assert [dim_schur(lam) for _,lam in highest] == [175,35,175,35]
assert 175+35 == comb(10,6)

# Sym^2 acts on basis vectors (columns), fixing the dual conventions.
def sym2(M):
    images = [sum(M[i,j]*x[i] for i in range(4)) for j in range(4)]
    polys = [s.Poly(images[i]*images[j], *x) for i in range(4) for j in range(i,4)]
    return s.Matrix(10,10,lambda i,j:polys[j].coeff_monomial(mon[i]))

t = s.symbols('t1:5')
D = sym2(s.diag(*t))
nonvanishing = []
for I, lam in highest[:2]:
    value = s.factor(D.extract(I,I).det())
    assert value == prod(t[i]**lam[i] for i in range(4))
    assert value.subs(dict.fromkeys(t,1)) == 1
    nonvanishing.append(str(value))

# Universal naturality evaluated with a nontrivial left and right change;
# these finite equalities are not a replacement for Schur's lemma.
g = s.Matrix([[1,1,0,0],[0,2,1,0],[0,0,1,1],[0,0,0,1]])
h = s.Matrix([[1,0,1,0],[0,1,0,1],[0,0,1,0],[0,0,0,1]])
T = s.Matrix([[1,2,0,1],[0,1,1,0],[1,0,2,1],[0,1,0,2]])
L = s.Matrix(6,10, lambda i,j: (1 if i==j else 0) + ((i+2*j)%5-2 if j>=6 else 0))
assert sym2(g*T*h.inv()) == sym2(g)*sym2(T)*sym2(h.inv())
minor_checks = []
for I in [(0,1,2,3,4,5), (0,1,2,4,5,7), (0,2,4,6,8,9)]:
    left = (L*sym2(g*T*h.inv())).extract(range(6),I).det()
    right = (L*sym2(g)*sym2(T)*sym2(h.inv())).extract(range(6),I).det()
    assert left == right
    minor_checks.append(str(left))
assert any(s.sympify(v) != 0 for v in minor_checks)

# All quadratic Pluecker relations of the explicit flag line.
coords = {(0,1,2,4):(1,0), (0,1,2,3):(0,1)}  # coefficients of a,b
count = 0
for I in combinations(range(10),3):
    for J in combinations(range(10),5):
        coefficient = [0,0,0]  # a^2, ab, b^2
        for pos,j in enumerate(J):
            p, K = sign_sort((*I,j))
            u = coords.get(K,(0,0)) if p else (0,0)
            v = coords.get(J[:pos]+J[pos+1:],(0,0))
            factor = (-1)**pos*p
            coefficient[0] += factor*u[0]*v[0]
            coefficient[1] += factor*(u[0]*v[1]+u[1]*v[0])
            coefficient[2] += factor*u[1]*v[1]
        assert coefficient == [0,0,0], (I,J,coefficient)
        count += 1
assert count == 30240

a,b,c,d,z = s.symbols('a b c d z')
f = (b-a)*(c*a+d*b)
assert s.expand(f.subs({a:d*a,b:-c*b}, simultaneous=True)
                -c*d*(b-a)*(d*a+c*b)) == 0
assert s.diff(f.subs({a:1,b:1+z}),z).subs(z,0) == c+d
assert s.expand(f.subs(c,-d) - d*(b-a)**2) == 0
assert s.factor(s.gcd((b-a)*a,(b-a)*b)) in [a-b,b-a]
assert f.subs({a:d,b:-c}) == 0
# A rank-one isolated secant: roots [1:1] and [2:-1], both non-endpoints.
assert s.expand(f.subs({c:1,d:2}) + (a-b)*(a+2*b)) == 0
# Pure endpoint cases have a reduced remaining root on the open torus.
assert s.expand(f.subs({c:0,d:1}) + b*(a-b)) == 0
assert s.expand(f.subs({c:1,d:0}) + a*(a-b)) == 0

receipt = {
 'ok':True, 'arithmetic':'exact integers and rational functions; no random samples',
 'highest_weight_vectors':[{'indices_one_based':[i+1 for i in I], 'weight':list(lam)} for I,lam in highest],
 'raising_operator_checks':24,
 'two_diagonal_coefficient_polynomials':nonvanishing,
 'sym2_composition_identity_checked':True,
 'universal_naturality_minor_values':minor_checks,
 'flag_line_pluecker_quadrics_checked':count,
 'residual_involution_identity':True, 'tangent_and_endpoint_identities':True,
 'scope':'Finite coordinate identities for the printed proofs, not proof verification.',
 'structural_proofs_not_machine_certified':[
  'Schur decomposition, Cauchy multiplicity one and universal block identity',
  'intrinsic normal-cone functoriality and global ruling orientation',
  'constancy of the common projective transformation',
  'scheme-theoretic fibre classification and regularity of the residual involution',
  'generic intrinsic web reconstruction', 'all inherited structural results']}
(ROOT/'evidence').mkdir(exist_ok=True)
(ROOT/'evidence/REVISION133_EXACT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
