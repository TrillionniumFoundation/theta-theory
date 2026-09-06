#!/usr/bin/env python3
"""Independent, exact finite diagnostics for the source-pinned A1 v6 review.
No import of the author's code. Finite tests are not proofs of general claims.
Run: python referee_checks.py ; requires Python 3.10+ and SymPy.
"""
from __future__ import annotations
import hashlib
import itertools
import json
import math
import platform
from pathlib import Path
import sympy as s

X = s.Symbol('x')
R = s.Rational
checks = []
details = {}

def require(name, condition, **data):
    if not bool(condition):
        raise AssertionError(name)
    checks.append(dict(name=name, passed=True, **data))

def support(A, m):
    values = {R(0)}
    for _ in range(m):
        values = {v+a for v in values for a in A}
    return sorted(values)

def integral(poly, scale=1, shift=0, prior=0):
    # x=t^(1/scale). Priors: uniform; density 2t; half-uniform + half-delta_1.
    ans = 0
    for (degree,), coefficient in s.Poly(poly, X).terms():
        exponent = R(degree, scale)+shift
        moment = [1/(exponent+1), 2/(exponent+2),
                  (1/(exponent+1)+1)/2][prior]
        ans += coefficient*moment
    return s.cancel(ans)

def exact_rank(matrix):
    return s.polys.matrices.DomainMatrix.from_Matrix(s.Matrix(matrix)).rank()

def rank_fixture(A, n, m, prior=0):
    A = sorted(map(R, A))
    scale = s.ilcm(*[a.q for a in A])
    F = [1+R(i+1, 1000)*X**int(scale*A[-1]) for i in range(n)]
    P = s.Poly(s.prod(F), X).as_expr()
    V = [s.Poly(X**int(a*scale)*s.prod(F[:i]+F[i+1:]), X)
         for i in range(n) for a in A]
    degree = s.degree(P, X)
    tangent = [[v.nth(j) for v in V] for j in range(degree+1)]
    future = support(A,m)
    Z = integral(P,scale,prior=prior)
    J = [[s.cancel(integral(v.as_expr(),scale,z,prior)/Z -
                   integral(P,scale,z,prior)*integral(v.as_expr(),scale,prior=prior)/Z**2)
          for v in V] for z in future[1:]]
    return exact_rank(tangent), exact_rank(J), J

# 1. Sumset arithmetic, including gcd and nonintegral examples.
for a,b in [(1,2),(2,5),(4,10),(3,7),(5,11)]:
    B=b//math.gcd(a,b)
    observed=[len(support([R(0),R(a),R(b)],m)) for m in range(B+4)]
    predicted=[math.comb(m+2,2)-(math.comb(m-B+2,2) if m>=B else 0)
               for m in range(B+4)]
    require(f'hilbert-{a}-{b}',observed==predicted)
profile=[min(2*n,len(support([R(0),R(2),R(5)],6-n))-1) for n in range(7)]
require('sparse-asymmetric-profile',profile==[0,2,4,6,5,2,0],profile=profile)

# 2. Whole product differential, followed by exact normalized rank.
fixtures=[([0,1],3,2),([0,1,2],2,3),([0,2,5],3,2),
          ([0,2,5],2,3),([0,1,4,6],2,2),([0,R(1,2),R(5,3)],2,2)]
for index,(A,n,m) in enumerate(fixtures):
    for prior in (0,1,2):
        tr,nr,_=rank_fixture(A,n,m,prior)
        expected=min(n*(len(A)-1),len(support(list(map(R,A)),m))-1)
        require(f'product-tangent-{index}-{prior}',tr==n*(len(A)-1)+1,rank=tr)
        require(f'normalized-rank-{index}-{prior}',nr==expected,rank=nr)
# Degenerate factors are allowed to lose rank: "generic" is material.
A=[0,2,5]; F=1+X**5; V=[X**a*F**2 for a in A]
require('coincident-binomial-tangent-is-not-generic',
        exact_rank([[s.Poly(v,X).nth(j) for v in V] for j in range(16)])==3)
# Mixed nonprincipal minors, using Cauchy-form moments at rational exponents.
minor_count=0
for rows in itertools.combinations([R(0),R(1,2),R(2),R(7,2)],3):
    for cols in itertools.combinations([R(0),R(1,3),R(1),R(5)],3):
        require(f'mixed-minor-{minor_count}',s.det(s.Matrix([
            [1/(1+a+b) for b in cols] for a in rows]))>0)
        minor_count+=1

# 3. Actual calibrated sparse reports; sequential factor -> moment changeover.
cells=[R(1,3)+X**2/12,R(1,3)+X**5/12,R(1,3)-(X**2+X**5)/12]
commands=[(R(1,4),R(1,2),R(3,4)),(R(3,4),R(1,4),R(1,2))]
def likelihood(command,report):
    if report<3:
        return s.Poly(command[report]*cells[report],X).as_expr()
    return s.Poly(sum((1-command[j])*cells[j] for j in range(3)),X).as_expr()
def multiply(polynomials):
    value=s.Poly(1,X)
    for p in polynomials:
        value*=s.Poly(p,X)
    return value.as_expr()
A=[R(0),R(2),R(5)]
for word_index,word in enumerate([(3,3,3,3,3,3),(0,1,2,3,0,1),
                                  (3,0,3,1,3,2),(2,2,1,0,3,3)]):
    past=[]; state=(); min_evidence=R(1)
    for n,report in enumerate(word,1):
        f=likelihood(commands[(n+word_index)%2],report)
        past.append(f)
        P=multiply(past); Z=integral(P)
        if n<=3:
            state=state+(s.Poly(f/integral(f),X).as_expr(),)
            recovered=multiply(state)
            require(f'factor-state-{word_index}-{n}',
                    s.Poly(recovered/integral(recovered)-P/Z,X).is_zero)
        elif n==4:
            recovered=multiply(list(state)+[f])
            state={z:integral(recovered,shift=z)/integral(recovered)
                   for z in support(A,2)}
            require(f'changeover-{word_index}',
                    all(v==integral(P,shift=z)/Z for z,v in state.items()))
        else:
            coeffs={R(degree):coefficient for (degree,),coefficient in s.Poly(f,X).terms()}
            denominator=sum(c*state[a] for a,c in coeffs.items())
            new={z:s.cancel(sum(c*state[z+a] for a,c in coeffs.items())/denominator)
                 for z in support(A,6-n)}
            require(f'moment-update-{word_index}-{n}',
                    denominator>=R(1,24) and
                    all(v==integral(P,shift=z)/Z for z,v in new.items()))
            state=new

# 4. Independent finite alphabet risk enumeration; this is NOT the mechanical model.
def partitions(items):
    if not items:
        yield (); return
    first,*rest=items
    for q in partitions(rest):
        yield ((first,),)+q
        for j in range(len(q)):
            yield q[:j]+((first,)+q[j],)+q[j+1:]
def risk(p,z,M):
    return sum(z)-max(sum(sum(z[i] for i in b)**2/sum(p[i] for i in b) for b in q)
                      for q in partitions(list(range(len(p)))) if len(q)<=M)
def merge_cost(p,z,i,j):
    return s.cancel(z[i]**2/p[i]+z[j]**2/p[j]-(z[i]+z[j])**2/(p[i]+p[j]))
require('all-partitions-count',len(list(partitions(list(range(4)))))==15 and
        len(list(partitions(list(range(3)))))==5)
for amplitude in [R(0),R(1,1000),R(1,100),R(1,10)]:
    p=[R(1,4)]*4
    means=[R(1,5),R(4,5),R(1,2)+amplitude,R(1,2)-amplitude]
    z=[p[i]*means[i] for i in range(4)]
    pe=[p[0],p[1],p[2]+p[3]]; ze=[z[0],z[1],z[2]+z[3]]
    delta=merge_cost(p,z,2,3)
    gains=[s.cancel(risk(pe,ze,M)-risk(p,z,M)) for M in range(1,5)]
    require(f'partition-budget-identities-{amplitude}',
            gains[0]==0 and gains[2]==delta-min(merge_cost(p,z,i,j)
                 for i,j in itertools.combinations(range(4),2)) and gains[3]==delta
            and all(g>=0 for g in gains),gains=list(map(str,gains)))
    if amplitude<=R(1,100):
        require(f'small-amplitude-threshold-{amplitude}',gains[:3]==[0,0,0])

# 5. Uniformly positive near-additive-collision family, fixed N=5.
collision=[]
for theta in [R(0),R(1,2),R(1,10),R(1,100)]:
    A=[R(0),R(1),2+theta]
    dims=[min(2*n,len(support(A,5-n))-1) for n in range(6)]
    tr,nr,_=rank_fixture(A,3,2)
    require(f'near-collision-rank-{theta}',nr==(4 if theta==0 else 5))
    require(f'near-collision-peak-{theta}',max(dims)==(4 if theta==0 else 5))
    collision.append(dict(theta=str(theta),profile=dims,rank_at_3_2=nr))
# A different exact witness: one future contrast is t^(2+theta)-t^2.
# Its uniform-prior squared norm and first derivative at theta=0 vanish.
h=s.Symbol('h',nonnegative=True)
contrast=1/(5+2*h)-2/(5+h)+R(1,5)
require('collision-contrast-quadratic',s.cancel(contrast-2*h**2/(5*(h+5)*(2*h+5)))==0)
require('collision-uniform-positivity',R(1,3)-R(1,12)*2==R(1,6) and
        R(1,4)*R(1,6)==R(1,24))
details['near_collision']=collision
details['contrast_L2_squared']=str(s.factor(contrast))

# 6. Common-risk covariance identity and elementary physical coefficient check.
T,e,area,pi=s.symbols('T e area pi',positive=True)
C=s.Matrix([[0,1,0,0],[0,-2*T/area,T/area,T/area],
            [pi/area,-pi/area,0,0],[0,0,2*T*e/(pi*area),-2*T*e/(pi*area)]])
require('mechanical-coefficient-determinant',s.factor(C.det()) in
        (4*T**2*e/area**3,-4*T**2*e/area**3))
c,v=s.symbols('c v')
require('binary-covariance-gain',s.cancel(c*(v/c)**2+(1-c)*(v/(1-c))**2-v**2/(c*(1-c)))==0)
require('rare-probe-bound',R(5,8)**40<R(1,10**8))
for dimension in [1,4,5,6]:
    u=s.Symbol('u',nonnegative=True)
    require(f'volume-tail-{dimension}',s.integrate(1-u**R(dimension,2),(u,0,1))==R(dimension,dimension+2))

receipt=dict(review='A1 v6 independent finite checks',
    submission_commit='750a65ef62422e81307b4a61fd891ee42fa2639e',
    python=platform.python_version(),sympy=s.__version__,
    script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    checks_passed=len(checks),checks_total=len(checks),all_passed=True,
    checks=checks,details=details,
    limitations=[
      'No author code is imported; the separate author rerun has its own receipt.',
      'These are finite exact instances, not proofs for arbitrary priors or budgets.',
      'Sparse sequential fixtures check exact updates, not a numerical asymptotic exponent.',
      'The four-symbol risk fixture is categorical, not a substitution for physical pi or sqrt(3).',
      'No topological, randomized-code, global optimality, or literature-priority certificate is asserted.',
      'The near-collision uniform bounds in the technical note are analytic deductions, not inferred from these samples.'])
out=Path(__file__).with_name('INDEPENDENT_DIAGNOSTICS.json')
out.write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(passed=len(checks),total=len(checks),script_sha256=receipt['script_sha256'],
                     near_collision=collision),indent=2))
