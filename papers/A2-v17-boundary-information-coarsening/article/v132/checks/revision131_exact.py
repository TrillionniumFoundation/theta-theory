"""Finite exact regressions; these are not certificates of the structural theorems."""
from itertools import permutations, combinations, combinations_with_replacement
from collections import defaultdict
from math import factorial, prod, comb
from fractions import Fraction
from pathlib import Path
import json
import sympy as s

ROOT = Path(__file__).resolve().parents[1]
def determinant(n, total=None, index=None):
    total = total or n*n
    index = index or (lambda i,j: i*n+j)
    out = {}
    for p in permutations(range(n)):
        a = [0]*total
        for i,j in enumerate(p):
            a[index(i,j)] += 1
        out[tuple(a)] = (-1)**sum(p[i]>p[j] for i in range(n) for j in range(i+1,n))
    return out

def multiply(a,b):
    out = defaultdict(int)
    for x,c in a.items():
        for y,d in b.items():
            out[tuple(i+j for i,j in zip(x,y))] += c*d
    return {x:c for x,c in out.items() if c}

def power(a,n):
    out = {(0,)*len(next(iter(a))):1}
    for _ in range(n):
        out = multiply(out,a)
    return out

def pairing(a,b):
    return sum(c*b.get(x,0)*prod(factorial(e) for e in x) for x,c in a.items())

D = power(determinant(4),4)
P = power(determinant(3,16,lambda i,j: 4*i+j),4)
e = [0]*16
e[-1] = 4
P = multiply(P,{tuple(e):1})
assert pairing(P,D) == pairing(P,P) == 24883200
assert pairing(D,D) == 870912000
assert Fraction(pairing(P,D),pairing(D,D)) == Fraction(1,35)

x = s.symbols('a:f')
B = s.Matrix(2,3,x)
y0,y1 = s.symbols('y0 y1')
columns = []
for i,j in combinations_with_replacement(range(3),2):
    q = s.Poly((B[0,i]*y0+B[1,i]*y1)*(B[0,j]*y0+B[1,j]*y1),y0,y1)
    columns.append(s.Matrix([q.coeff_monomial(y0**2),q.coeff_monomial(y0*y1),q.coeff_monomial(y1**2)]))
S = s.Matrix.hstack(*columns)
minors = [s.Poly(S[:,list(c)].det().expand(),*x) for c in combinations(range(6),3)]
p = [B[:,list(c)].det() for c in combinations(range(3),2)]
products = [s.Poly(s.expand(prod(p[i] for i in c)),*x) for c in combinations_with_replacement(range(3),3)]
monomials = sorted(set().union(*(set(q.monoms()) for q in minors+products)))
def rank(polys):
    return s.Matrix([[q.coeff_monomial(m) for m in monomials] for q in polys]).rank()
ranks = [rank(minors),rank(products),rank(minors+products)]
assert ranks == [10,10,10]

# Monomial intersection: (u*x,v*y) in variables u,v,x,y.
ideals = [[(1,0,0,0),(0,1,0,0)],[(1,0,0,0),(0,0,0,1)],
          [(0,0,1,0),(0,1,0,0)],[(0,0,1,0),(0,0,0,1)]]
def divides(a,b):
    return all(i<=j for i,j in zip(a,b))
def intersect(a,b):
    candidates = set(tuple(max(i,j) for i,j in zip(x,y)) for x in a for y in b)
    return sorted(x for x in candidates if not any(y!=x and divides(y,x) for y in candidates))
g = ideals[0]
for ideal in ideals[1:]:
    g = intersect(g,ideal)
assert set(g) == {(1,0,1,0),(0,1,0,1)}
for a in range(1,9):
    for h in range(2,6):
        assert sum(comb(a-j+h-1,h-1) for j in range(1,a+1)) == comb(a+h-1,h)

out = {'ok':True,
 'fischer':{'cross_pairing':pairing(P,D),'p_norm_squared':pairing(P,P),'determinant_norm_squared':pairing(D,D),'projection':'1/35','determinant_power_monomials':len(D)},
 'quotient_induced_witness':{'matrix_shape':[2,3],'symmetric_degree':2,'generator_space_ranks':ranks,'maximal_minors':len(minors),'power_generators':len(products)},
 'incidence_intersection_minimal_monomial_generators':g,
 'length_identity_test_ranges':{'a':[1,8],'h':[2,5]},
 'scope':'Exact finite polynomial and combinatorial checks only; general structural proofs are not machine-certified.'}
(ROOT / 'evidence/REVISION131_EXACT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
