#!/usr/bin/env python3
"""Exact finite certificates for the two-component Pluecker readout.

No sampling, floating point arithmetic, or claim to machine certification of
scheme-theoretic descent/intrinsic reconstruction is made here.
"""
from itertools import combinations, product
from math import factorial, prod
from pathlib import Path
import json
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
x = sp.symbols('x1:5')
monomials = [x[i]*x[j] for i in range(4) for j in range(i, 4)]
wedges = list(combinations(range(10), 4))
wi = {v:i for i,v in enumerate(wedges)}
exponents = [v for v in product(range(5), repeat=4) if sum(v) == 4]
mi = {v:i for i,v in enumerate(exponents)}
C = sp.zeros(35, 210)
for j, indices in enumerate(wedges):
    polynomial = sp.Poly(sp.det(sp.Matrix([
        [sp.diff(monomials[k], variable) for variable in x] for k in indices])), *x)
    for exponent, coefficient in polynomial.terms():
        if coefficient:
            C[mi[exponent], j] = coefficient
wedge_norm = [prod(2 if monomials[k] in [z*z for z in x] else 1
                  for k in I) for I in wedges]
quartic_norm = [prod(factorial(k) for k in v) for v in exponents]
C = sp.SparseMatrix(C)
adjoint = sp.diag(*[sp.Rational(1,k) for k in wedge_norm])*C.T*sp.diag(*quartic_norm)
adjoint = sp.SparseMatrix(adjoint)
assert C*adjoint == 48*sp.eye(35)
Q = sp.SparseMatrix(adjoint*C/48)
assert Q*Q == Q
assert Q.rank() == 35

# All sixteen Lie algebra generators: x_a d/dx_b, including the determinant twist.
def exterior_action(a: int, b: int) -> sp.SparseMatrix:
    action = sp.zeros(10, 10)
    for j, m in enumerate(monomials):
        f = sp.Poly(x[a]*sp.diff(m, x[b]), *x)
        for i, n in enumerate(monomials):
            action[i, j] = f.coeff_monomial(n)
    out = sp.MutableSparseMatrix(210, 210, {})
    for j, I in enumerate(wedges):
        for position, old in enumerate(I):
            for new in range(10):
                c = action[new, old]
                if not c:
                    continue
                J = list(I); J[position] = new
                if len(set(J)) != 4:
                    continue
                sign = (-1)**sum(J[s] > J[t] for s in range(4) for t in range(s+1,4))
                out[wi[tuple(sorted(J))], j] += sign*c
    return sp.SparseMatrix(out)

for a in range(4):
    for b in range(4):
        L = exterior_action(a,b)
        target = sp.MutableSparseMatrix(35, 35, {})
        for j, exponent in enumerate(exponents):
            if exponent[b]:
                shifted = list(exponent); shifted[b] -= 1; shifted[a] += 1
                target[mi[tuple(shifted)], j] += exponent[b]
            if a == b:
                target[j,j] += 1
        assert C*L == target*C, (a,b,'Jacobian equivariance')
        assert Q*L == L*Q, (a,b,'projector equivariance')


def pluecker(matrix: sp.Matrix) -> sp.Matrix:
    return sp.Matrix([matrix[:,list(I)].det() for I in wedges])


def coordinate(vector: sp.Matrix, indices: tuple) -> sp.Expr:
    if len(set(indices)) < 4:
        return sp.Integer(0)
    sign = (-1)**sum(indices[i] > indices[j] for i in range(4) for j in range(i+1,4))
    return sign*vector[wi[tuple(sorted(indices))]]


def relation(vector: sp.Matrix, I: tuple, J: tuple) -> sp.Expr:
    return sp.expand(sum((-1)**k * coordinate(vector,I+(j,)) *
                         coordinate(vector,J[:k]+J[k+1:]) for k,j in enumerate(J)))


a,b = sp.symbols('a b')
relations = [((0,4,7),(0,5,6,8,9)), ((0,5,6),(1,2,5,8,9))]
M = sp.zeros(4,10)
for i,j in enumerate([0,4,7,9]): M[i,j] = 1
w = pluecker(M); qw = Q*w; pw = w-qw
expected = {(0,4,7,9):sp.Rational(1,3), (0,5,6,8):-sp.Rational(2,3),
            (1,2,5,9):-sp.Rational(2,3), (1,3,6,7):sp.Rational(2,3),
            (2,3,4,8):sp.Rational(2,3)}
assert {I:qw[i] for i,I in enumerate(wedges) if qw[i]} == expected
polynomials = [relation(a*pw+b*qw,I,J) for I,J in relations]
assert sp.expand(polynomials[0]+sp.Rational(2,9)*(b-a)*(b+2*a)) == 0
assert sp.expand(polynomials[1]+sp.Rational(4,9)*(b-a)**2) == 0
quotients = [sp.cancel(f/(b-a)) for f in polynomials]
quotient_matrix = sp.Matrix([[f.coeff(a),f.coeff(b)] for f in quotients])
assert quotient_matrix.det() != 0
assert sp.Poly(sp.gcd(*polynomials),b,a).total_degree() == 1

# The independent, already certified smooth C_* of the inherited K3 script.
Cstar = sp.Matrix([[2,-1,2,0],[-2,0,-1,1],[2,-1,-2,0],
                   [1,-1,2,1],[1,-1,0,0],[1,-2,1,-2]])
Mstar = M.copy()
for row in range(4):
    for k,col in enumerate([1,2,3,5,6,8]): Mstar[row,col] = Cstar[k,row]
wstar=pluecker(Mstar); qstar=Q*wstar; pstar=wstar-qstar
smooth_polynomials=[relation(a*pstar+b*qstar,I,J) for I,J in relations]
smooth_quotients=[sp.Poly(sp.cancel(f/(b-a)),a,b) for f in smooth_polynomials]
smooth_quotient_matrix=sp.Matrix([[f.coeff_monomial(a),f.coeff_monomial(b)] for f in smooth_quotients])
assert smooth_quotient_matrix.det()!=0

# A simple split orbit example checks the distinction between an intersection
# identity and its collision specialization; it is not a descent proof.
u,t=sp.symbols('u t')
assert sp.expand((u-t)*(u+t))==u*u-t*t
assert sp.Poly((u-t)*(u+t),u,t).subs(t,0)==u*u

receipt={
 'ok':True, 'arithmetic':'exact rational arithmetic',
 'jacobian_shape':[35,210], 'jacobian_rank':35,
 'adjoint_identity':'C C^* = 48 I_35', 'projector_idempotent':True,
 'lie_generators_checked':16,
 'monomial_basis':[str(m) for m in monomials],
 'diagonal_witness':{
   'matrix':[[int(v) for v in M.row(i)] for i in range(4)],
   'q_coordinates':{','.join(str(k+1) for k in I):str(c) for I,c in expected.items()},
   'pluecker_quadrics':[{'I':[i+1 for i in I],'J':[j+1 for j in J]} for I,J in relations],
   'restrictions':[str(sp.factor(f)) for f in polynomials],
   'linear_quotient_determinant':str(quotient_matrix.det()),
   'homogeneous_gcd':str(sp.factor(sp.gcd(*polynomials))),
   'not_asserted_smooth':True},
 'inherited_smooth_Cstar':{
   'matrix':[[int(v) for v in Mstar.row(i)] for i in range(4)],
   'restrictions':[str(sp.factor(f)) for f in smooth_polynomials],
   'linear_quotient_determinant':str(smooth_quotient_matrix.det()),
   'smoothness_source':'independently executed checks/exact_k3.py and its integral certificates'},
 'not_machine_certified':['fpqc descent and power-certified packets',
   'generic primary spreading and no-new-torsion', 'intrinsic deepest stratum and tensor ruling',
   'Cauchy coefficient-space interpretation', 'generic intrinsic web theorem']}
(ROOT/'evidence').mkdir(exist_ok=True)
(ROOT/'evidence/REVISION132_EXACT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
