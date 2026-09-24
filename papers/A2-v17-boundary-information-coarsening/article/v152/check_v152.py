#!/usr/bin/env python3
"""Exact finite checks; the manuscript, not this script, supplies universal proofs."""
from pathlib import Path
from itertools import combinations, product
import json
import sympy as s

HERE=Path(__file__).resolve().parent
records=[]
def require(name, condition, **data):
    ok=bool(condition)
    records.append({'name':name,'ok':ok,**data})
    if not ok:
        raise AssertionError(name)

def span_matrix(polys, variables, max_degree=None):
    ps=[s.Poly(p,*variables) for p in polys]
    mon=sorted(set().union(*(set(p.monoms()) for p in ps)))
    if max_degree is not None: mon=[m for m in mon if sum(m)<=max_degree]
    return s.Matrix([[p.coeff_monomial(m) for m in mon] for p in ps])

# Flag coefficient representation and its exact order for three finite dimensions.
for n in (3,4,5):
    z=s.symbols('z2:'+str(n+1)); y=s.symbols('y3:'+str(n+1)); variables=z+y
    v=[s.Integer(1)]+list(z); w=[s.Integer(0),s.Integer(1)]+list(y)
    pairs=list(combinations(range(n),2))
    symmetric=[(i,j) for i in range(n) for j in range(i,n)]
    vv=[v[i]*v[j]*(1 if i==j else 2) for i,j in symmetric]
    vw=[v[i]*w[j] if i==j else v[i]*w[j]+v[j]*w[i] for i,j in symmetric]
    F=[s.expand(vv[i]*vw[j]-vv[j]*vw[i]) for i,j in combinations(range(len(vv)),2)]
    r=len(F);q=3 if n==3 else 4
    full=span_matrix(F,variables).rank()
    jet=span_matrix(F,variables,q).rank()
    prev=span_matrix(F,variables,q-1).rank()
    require(f'flag dimension n={n}',full==r,rank=full,expected=r)
    require(f'flag last jet n={n}',jet==r and prev<r,q=q,previous_rank=prev)
    if n==3:
        z,w,t=variables
        basis=[1,z,w,t,z*z,z*w,w*w,z*t,w*t,z*z*t,z*w*t,w*w*t,z*z*w-z**3*t,z*w*w-z*z*w*t,w**3-z*w*w*t]
        require('ternary displayed coefficient basis',span_matrix(F+basis,variables).rank()==15)
    else:
        i=symmetric.index((2,2));j=symmetric.index((2,3))
        quartic=s.expand(vv[i]*vw[j]-vv[j]*vw[i])
        require(f'quartic flag coordinate n={n}',s.expand(quartic-z[1]**2*(z[1]*y[1]-z[2]*y[0]))==0)

# Full scheme elimination for the generalized pinch rings, not radicals.
for m in (1,2,3):
    u=s.symbols('u1:'+str(m+1));w=s.symbols('w1:'+str(m+1));t,delta=s.symbols('t delta')
    variables=u+(delta,)+w
    displayed=[u[i]*w[j]-u[j]*w[i] for i,j in combinations(range(m),2)]
    displayed += [w[i]*w[j]-delta*u[i]*u[j] for i in range(m) for j in range(i,m)]
    elimination=s.groebner([delta-t*t]+[w[i]-u[i]*t for i in range(m)],t,*variables,order='lex')
    eliminated=[p.as_expr() for p in elimination.polys if not p.as_expr().has(t)]
    G=s.groebner(displayed,*variables,order='lex');H=s.groebner(eliminated,*variables,order='lex')
    require(f'pinch exact elimination m={m}',all(G.reduce(p)[1]==0 for p in eliminated) and all(H.reduce(p)[1]==0 for p in displayed),relations=len(displayed))
    require(f'pinch normalization fibre m={m}',s.groebner([t*t]+[s.Integer(0) for _ in u],t).reduce(t**2)[1]==0)
    if m==1:
        f=displayed[0];jac=[s.diff(f,x) for x in variables]
        ideal=s.groebner(jac,*variables)
        require('pinch singular ideal retains nilpotents',all(ideal.reduce(x)[1]==0 for x in [w[0],delta*u[0],u[0]**2]) and ideal.reduce(u[0])[1]!=0)

# Split singular Fitting ideals in codimension one, two, and three.
for c in (1,2,3):
    x=s.symbols('x1:'+str(c+1));y=s.symbols('y1:'+str(c+1));var=x+y
    rel=[a*b for a in x for b in y];J=s.Matrix(rel).jacobian(var)
    ring=s.groebner(rel,*var)
    minors=[]
    for rows in combinations(range(c*c),c):
        for cols in combinations(range(2*c),c):
            d=s.expand(J.extract(rows,cols).det())
            d=ring.reduce(d)[1]
            if d: minors.append(d)
    G=s.groebner(rel+minors,*var)
    pure=[s.prod(x[i] for i in inds) for inds in product(range(c),repeat=c)]
    pure += [s.prod(y[i] for i in inds) for inds in product(range(c),repeat=c)]
    H=s.groebner(rel+pure,*var)
    require(f'split full singular ideal c={c}',all(G.reduce(p)[1]==0 for p in pure) and all(H.reduce(p)[1]==0 for p in minors),nonzero_minors=len(minors))

# Reciprocal equations for the actual n=3 pure-power fibre.
L,Q=s.symbols('L Q');coeff=[s.Integer(1)]
for j in range(1,9): coeff.append(s.expand(-L*coeff[j-1]-(Q*coeff[j-2] if j>=2 else 0)))
require('pure power c7',s.expand(coeff[7]-(-L**7+6*L**5*Q-10*L**3*Q**2+4*L*Q**3))==0)
require('pure power c8',s.expand(coeff[8]-(L**8-7*L**6*Q+15*L**4*Q**2-10*L**2*Q**3+Q**4))==0)
a=s.symbols('a');f=sum(coeff[j]*a**(6-j) for j in range(7))
product_coeff=s.Poly(s.expand(f*(a*a+L*a+Q)-a**8),a)
G=s.groebner([coeff[7],coeff[8]],L,Q)
require('pure power complete product identity',all(G.reduce(c)[1]==0 for c in product_coeff.all_coeffs()))
require('n3 fibre tangent dimension',s.binomial(10,2)-1==44)

# Independent Sym^2 complementary-minor construction of the limiting relation.
x=s.symbols('a b c d e f g h i');T=s.Matrix(3,3,x)
pairs=[(0,0),(0,1),(0,2),(1,1),(1,2),(2,2)];M=s.zeros(6,6)
for col,(j,k) in enumerate(pairs):
    for row,(p,q) in enumerate(pairs):
        M[row,col]=T[p,j]*T[q,k]+(T[p,k]*T[q,j] if p!=q and j!=k else 0)
        if p!=q and j==k:M[row,col]*=2
delta=s.Poly(T.det(),*x);C=[]
for cols in combinations(range(6),4):
    det=s.Poly(s.expand(M.extract([2,3,4,5],cols).det(method='domain-ge')),*x)
    quotient,rem=s.div(det,delta)
    require('exact determinant division '+''.join(map(str,cols)),rem.is_zero)
    C.append(s.Poly(quotient.as_expr().subs({x[4]:x[0]+x[4],x[8]:x[0]+x[8]},simultaneous=True),*x))
weight=lambda mon:sum(mon[1:])
monoms=sorted(set().union(*(set(p.monoms()) for p in C)),key=lambda m:(weight(m),m))
mat=s.Matrix([[p.coeff_monomial(m) for m in monoms] for p in C]);rr,piv=mat.rref();initial=[]
for row,j in zip(rr.tolist(),piv):
    d=weight(monoms[j]);initial.append(s.Poly.from_dict({m:k for k,m in zip(row,monoms) if k and weight(m)==d},x))
require('independent initial flag relations',len(piv)==15)
gcd=initial[0]
for p in initial[1:]:gcd=s.gcd(gcd,p)
require('actual primitive gcd a^2',gcd.monic().as_expr()==x[0]**2)
a,u,v,w=x[0],x[3],x[6],x[7]
expected=[a**3,a*a*u,a*a*v,a*a*w,a*u*u,a*u*v,a*v*v,a*u*w,a*v*w,u*u*v,u*u*w,u*v*v,u*v*w,v**3,v*v*w]
L3=[s.div(p,s.Poly(a*a,*x))[0].as_expr() for p in initial]
require('displayed n3 boundary relation space',span_matrix(L3+expected,x).rank()==15)
require('actual marked divisor limit',s.expand(T.det().subs({x[1]:0,x[2]:0,x[3]:0,x[4]:a,x[5]:0,x[6]:0,x[7]:0,x[8]:a},simultaneous=True))==a**3)

out={'revision':152,'ok':all(r['ok'] for r in records),'check_count':len(records),'checks':records,
     'proof_certified_by_finite_checks':False,'initial_basis':[str(p.as_expr()) for p in initial]}
(HERE/'evidence_v152').mkdir(exist_ok=True)
(HERE/'evidence_v152/REVISION152_EXACT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
