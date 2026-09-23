#!/usr/bin/env python3
"""Independent polarization and exact contraction/support identities.

Finite coordinate checks only. The stabilizer argument, irreducibility,
global rank-stratum construction and inverse theorem are written proofs,
not claims of formal machine verification.
"""
from contextlib import redirect_stdout
from itertools import combinations
from math import factorial, prod
from pathlib import Path
import io
import json
import runpy
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
with redirect_stdout(io.StringIO()):
    old = runpy.run_path(str(ROOT/'checks/revision132_exact.py'))
x=old['x']; monomials=old['monomials']; wedges=old['wedges']
exponents=old['exponents']; mi={a:i for i,a in enumerate(exponents)}
triples=list(combinations(range(10),3)); ti={a:i for i,a in enumerate(triples)}

# Construct j from the defining wedge of ell*x_i, independently of the
# Fischer adjoint; divide pure-power coefficients by their multinomials.
t=sp.symbols('t1:5'); ell=sum(ti*xi for ti,xi in zip(t,x))
M=sp.Matrix([[sp.Poly(ell*xk,*x).coeff_monomial(m)
              for xk in x] for m in monomials])
j=sp.MutableSparseMatrix(210,35,{})
for row,I in enumerate(wedges):
    f=sp.Poly(M[list(I),:].det(),*t)
    for a,c in f.terms():
        if c:
            j[row,mi[a]]=c*sp.Rational(prod(factorial(k) for k in a),24)
j=sp.SparseMatrix(j)
assert j==old['adjoint']/24
assert old['C']*j==2*sp.eye(35)

def contraction(qvalues):
    out=sp.MutableSparseMatrix(120,210,{})
    for col,I in enumerate(wedges):
        for k,b in enumerate(I):
            if qvalues[b]:
                out[ti[I[:k]+I[k+1:]],col]+=(-1)**k*qvalues[b]
    return sp.SparseMatrix(out)

def quartic(f):
    p=sp.Poly(sp.expand(f),*x)
    return sp.Matrix([p.coeff_monomial(a) for a in exponents])

kernels=[]; diagonals=[0,4,7,9]
for rank in range(1,5):
    q=[int(k in diagonals[:rank]) for k in range(10)]
    K=contraction(q)*j
    expected_rank={1:20,2:30,3:34,4:34}[rank]
    assert K.rank()==expected_rank
    if rank<4:
        radical_columns=[i for i,a in enumerate(exponents)
                         if all(a[k]==0 for k in range(rank))]
        assert len(radical_columns)==35-expected_rank
        assert K[:,radical_columns]==sp.zeros(120,len(radical_columns))
        kernel_description=f'Sym^4 of the {4-rank}-dimensional radical'
    else:
        rho=sum(z*z for z in x)
        assert K*quartic(rho*rho)==sp.zeros(120,1)
        kernel_description='the line spanned by (x1^2+x2^2+x3^2+x4^2)^2'
    kernels.append({'bilinear_rank':rank,'matrix_shape':[120,35],
                    'contraction_rank':expected_rank,'kernel_dimension':35-expected_rank,
                    'kernel':kernel_description})

K=contraction([int(k in diagonals) for k in range(10)])*j
h4=x[0]**4-6*x[0]**2*x[1]**2+x[1]**4
h2=x[0]**2-x[1]**2
assert sp.expand(sum(sp.diff(h4,z,2) for z in x))==0
assert sp.expand(sum(sp.diff(h2,z,2) for z in x))==0
coefficient_row=ti[(1,2,3)]
assert (K*quartic(h4))[coefficient_row]==2
assert (K*quartic(rho*h2))[coefficient_row]==sp.Rational(2,3)

def support(z):
    cols=[]
    for b in range(10):
        q=[int(k==b) for k in range(10)]
        cols.append(contraction(q)*z)
    return sp.Matrix.hstack(*cols).rank()

representatives=[('one_variable',x[0]**4,4),
 ('two_variables',sum(z**4 for z in x[:2]),7),
 ('three_variables',sum(z**4 for z in x[:3]),9),
 ('four_variable_Fermat',sum(z**4 for z in x),10),
 ('nondegenerate_quadratic_square',rho**2,9)]
supports=[]
for name,f,expected in representatives:
    actual=support(j*quartic(f)); assert actual==expected
    supports.append({'quartic':name,'exterior_support_dimension':actual})
assert support(old['qstar'])==10

# An exact rank-eight secant, and a rank-eight tangent at a four-plane.
wi={I:i for i,I in enumerate(wedges)}
secant=sp.zeros(210,1)
secant[wi[(0,1,2,3)]]=1;secant[wi[(4,5,6,7)]]=1
assert support(secant)==8
tangent=sp.zeros(210,1)
for k in range(4):
    I=list(range(4));I[k]=4+k
    sign=(-1)**sum(I[a]>I[b] for a in range(4) for b in range(a+1,4))
    tangent[wi[tuple(sorted(I))]]+=sign
assert support(tangent)==8

receipt={'revision':134,'ok':True,'arithmetic':'exact rational arithmetic',
 'independent_polarization_columns':35,
 'polarization_matches_fischer_adjoint':True,
 'normalization':'j=C^*/24; Cj=2I; Q=jC/2',
 'canonical_contraction_kernels':kernels,
 'harmonic_nonvanishing_coefficients':['2','2/3'],
 'support_representatives':supports,
 'smooth_Cstar_support_dimension':10,
 'secant_and_tangent_sharp_examples':[8,8],
 'structural_proofs_not_machine_certified':[
   'stabilizer-shear proof of contraction kernels for arbitrary bilinear forms',
   'orthogonal irreducibility and the exterior-support classification',
   'global scheme-theoretic rank and ramification loci',
   'intrinsic normal-cone naturality and full smooth-locus reconstruction'],
 'documentary_open':['Ballico 1993 full-text theorem-level comparison']}
(ROOT/'evidence').mkdir(exist_ok=True)
(ROOT/'evidence/REVISION134_EXACT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
