#!/usr/bin/env python3
"""Exact, independent diagnostic checks for the A1 v20 referee report.

Requires Python >=3.10 and SymPy. Imports no manuscript/author test code.
Run: python independent_checks.py --output CHECK_RESULTS.json
These finite checks are not verification of the manuscript's general proofs.
Checks use explicit exceptions and remain active with python -O.
"""
from __future__ import annotations
import argparse
from collections import defaultdict
from itertools import combinations, product
import hashlib
import json
import math
from pathlib import Path
import platform
import sympy as S

PIN = '6f103ad252d7c65f140720f4095585026f7bb1b9'
COUNTS: dict[str, int] = defaultdict(int)
CASES: dict[str, int] = defaultdict(int)

def check(group: str, condition: object, description: str) -> None:
    if not bool(condition):
        raise ArithmeticError(f'{group}: {description}')
    COUNTS[group] += 1

def same(a: S.Matrix, b: S.Matrix) -> bool:
    return a.shape == b.shape and all(S.simplify(x) == 0 for x in a-b)

def cov(g: S.Matrix, f: S.Matrix, weights: S.Matrix) -> S.Matrix:
    return g*S.diag(*weights)*f.T - (g*weights)*(f*weights).T

def four_point() -> None:
    group = 'square_pencil_with_varying_kernel'
    a,b,c = S.symbols('a b c')
    d = 1-a-b-c
    E = S.Matrix([[1,1,1,1],[1,0,0,0],[0,1,0,0]])
    F = S.Matrix([[1,1,1,1],[0,0,1,0],[0,0,0,1]])
    w = S.Matrix([a,b,c,d])
    H = E*S.diag(*w)*F.T
    check(group, same(H,S.Matrix([[1,c,d],[a,0,0],[b,0,0]])), 'pairing')
    check(group, S.expand(H.det()) == 0, 'identically singular')
    check(group, S.expand(H.extract([0,1],[0,1]).det()) == -a*c, 'nonzero minor')
    check(group, same(H*S.Matrix([0,d,-c]), S.zeros(3,1)), 'variable kernel')
    f = E[1:3,:]/4
    g = S.ones(2,4)/2 + F[1:3,:]/4
    C = cov(g/S.sqrt(2),f,w)
    expected = -S.Matrix([c,d])*S.Matrix([[a,b]])/(16*S.sqrt(2))
    check(group, same(C,expected), 'physical covariance and query weighting')
    norm2 = sum(x*x for x in C)
    check(group, S.simplify(norm2-(a*a+b*b)*(c*c+d*d)/512)==0, 'physical scale')
    H1 = H.subs({a:S.Rational(1,4),b:S.Rational(1,4),c:S.Rational(1,4)})
    H2 = H.subs({a:S.Rational(1,5),b:S.Rational(1,5),c:S.Rational(1,5)})
    check(group, H1.col_join(H2).rank()==3, 'common kernel is zero')
    CASES[group] += 1  # symbolic family
    for total in (7,8):
        for i,j,k in product(range(1,total),repeat=3):
            l = total-i-j-k
            if l<=0:
                continue
            sub = {a:S.Rational(i,total),b:S.Rational(j,total),c:S.Rational(k,total)}
            check(group,H.subs(sub).rank()==2,'full-support pairing rank')
            check(group,C.subs(sub).rank()==1,'normalized physical rank')
            CASES[group] += 1

def block(n: int, m: int, roots: tuple[int,...]) -> tuple[S.Matrix,S.Matrix,S.Matrix]:
    points = [(j,sgn) for j in range(1,n+1) for sgn in (-1,1)]
    weights = S.Matrix([(S.Rational(1,n) + sgn*(S.Rational(1,2*n) if j in roots else 0))/2
                        for j,sgn in points])
    E = S.Matrix([[int(j==i) for j,sgn in points] for i in range(1,n+1)])
    F = S.Matrix([[1]*len(points)] + [[sgn*j**ell for j,sgn in points] for ell in range(m)])
    H = E*S.diag(*weights)*F.T
    return weights,H,S.Matrix(points)

def block_family() -> None:
    group = 'root_saturated_balanced_blocks'
    z = S.symbols('z')
    for m in range(1,5):
        n=m+1
        for size in range(m):
            for roots in combinations(range(1,n+1),size):
                weights,H,_ = block(n,m,roots)
                poly = S.prod(z-j for j in roots)
                K = S.Matrix.hstack(*[S.Matrix([0]+[S.expand(poly*z**k).coeff(z,i) for i in range(m)])
                                       for k in range(m-size)])
                check(group, all(w>0 for w in weights) and sum(weights)==1,'positive probability')
                check(group,H.rank()==1+size,'maximum pairing rank witness')
                check(group,same(H*K,S.zeros(n,m-size)) and K.rank()==m-size,'entire specified kernel')
                pts=[(j,s) for j in range(1,n+1) for s in (-1,1)]
                f=S.Matrix([[S.Rational(int(j==i),2*(n-1)) for j,s in pts] for i in range(1,n)])
                g=S.Matrix([[S.Rational(1,2)+S.Rational(s,4)*S.Rational(j,n)**ell for j,s in pts]
                            for ell in range(m)])
                check(group,cov(g,f,weights).rank()==size,'physical history rank after normalization')
                CASES[group]+=1
    group='containment_is_not_exact_kernel'
    weights,H,_=block(4,2,())
    check(group,H.rank()==1,'v19 eight-point counterexample rank')
    check(group,same(H[:,1:3],S.zeros(4,2)),'both sigma and j*sigma forced')
    CASES[group]+=1
    weights,H,_=block(4,3,(1,))
    U=S.Matrix([0,-1,1,0])
    V=S.Matrix([0,0,-1,1])
    check(group,same(H*U,S.zeros(4,1)) and same(H*V,S.zeros(4,1)),'nonsaturated line enlarges')
    check(group,H.rank()==2 and S.Matrix.hstack(U,V).rank()==2,'two-dimensional entire kernel')
    CASES[group]+=1

def density_chart() -> None:
    group='constrained_density_chart'
    pts=[(j,s) for j in range(1,5) for s in (-1,1)]
    mu=S.ones(8,1)/8
    W=S.Matrix([[s*int(j==i) for j,s in pts] for i in (1,3,4)])
    V=S.Matrix([[int(j==i) for j,s in pts] for i in (1,2,3)] + [[s*int(j==2) for j,s in pts]])
    D=S.diag(*mu)
    projection=V*D*W.T*(W*D*W.T).inv()*W
    h=V-(V*mu)*S.ones(1,8)-projection
    B=h*D*h.T
    check(group,same(h*mu,S.zeros(4,1)),'tilt means')
    check(group,same(h*D*W.T,S.zeros(4,3)),'constraint orthogonality')
    check(group,all(B[:j,:j].det()>0 for j in range(1,5)),'positive definite local Gram matrix')
    check(group,same(V*D*h.T,B),'moment chart Jacobian')
    E=S.Matrix([[int(j==i) for j,s in pts] for i in range(1,5)])
    F=S.Matrix([[1]*8,[s for j,s in pts],[j*s for j,s in pts]])
    check(group,(E*D*F.T).rank()==1,'nonmaximal center')
    CASES[group]+=1
    for t in (S.Rational(1,4),S.Rational(-1,4),S.Rational(1,100),S.Rational(-1,100)):
        tilt=S.Matrix([0,0,0,t])
        density=S.ones(8,1)+h.T*tilt
        weights=D*density
        H=E*S.diag(*weights)*F.T
        check(group,all(v>0 for v in density) and sum(weights)==1,'strictly positive normalized tilt')
        check(group,same(W*weights,S.zeros(3,1)),'annihilation retained')
        check(group,same(V*weights,V*mu+B*tilt),'exact affine moment identity')
        check(group,H.rank()==2 and same(H*S.Matrix([0,-2,1]),S.zeros(4,1)),'exact requested kernel')
        CASES[group]+=1
    group='zero_dimensional_conventions'
    check(group,(S.Matrix([[-1,1]])*S.eye(2)/2*S.ones(2,1))==S.zeros(1,1),
          'q=0: E=span(sign), F=U=span(1), balanced prior')
    CASES[group]+=1
    check(group,(S.ones(1,2)*S.eye(2)/2*S.ones(2,1))==S.ones(1,1),
          's=0: E=F=span(1), U=0, constant rank-one pencil')
    CASES[group]+=1

def leja() -> None:
    group='leja_exact_collision_identities'
    R=S.Rational
    configurations=[(R(1,4),),(R(1,3),R(1,3)),(R(0),R(1,2),R(1)),
       (R(0),R(0),R(1,2),R(1,2),R(1)),
       (R(1,5),R(1,5),R(2,5),R(3,5),R(3,5),R(4,5)),
       (R(0),R(1,1000),R(1,2),R(501,1000),R(1))]
    z=S.symbols('z')
    for nodes in configurations:
        remaining=list(range(len(nodes)))
        first=min(remaining,key=lambda i:(nodes[i],i))
        order=[first];remaining.remove(first);pivots=[S.Integer(1)]
        while remaining:
            score=lambda i:S.prod(abs(nodes[i]-nodes[k]) for k in order)
            nxt=max(remaining,key=lambda i:(score(i),-i))
            pivots.append(score(nxt));order.append(nxt);remaining.remove(nxt)
        x=[nodes[i] for i in order];q=len(x);active=len(set(x))
        L=S.zeros(q,q);T=S.zeros(q,q)
        for j in range(q):
            poly=S.expand(S.prod(z-x[k] for k in range(j)))
            for k in range(q):T[k,j]=poly.coeff(z,k)
            if pivots[j]:
                for i in range(q):L[i,j]=poly.subs(z,x[i])/pivots[j]
        W=S.Matrix([[xx**j for j in range(q)] for xx in x])
        check(group,all(pivots[j]>=pivots[j+1] for j in range(q-1)),'ordered pivots')
        check(group,same(W*T,L*S.diag(*pivots)),'Newton evaluation identity including zero pivots')
        check(group,all(abs(v)<=1 for v in L),'entrywise Leja bound')
        check(group,abs(L[:active,:active].det())==1,'active block invertible')
        for ell in range(1,q+1):
            volume=max(S.prod(abs(nodes[i]-nodes[j]) for i,j in combinations(indices,2))
                       for indices in combinations(range(q),ell))
            initial=S.prod(pivots[:ell])
            check(group,initial<=volume<=math.factorial(ell)*initial,'maximal exterior product bounds')
        CASES[group]+=1

def finite_pairing_rank() -> None:
    group='finite_pairing_common_independence'
    pairs=[
      (S.Matrix([[1,1,1,1],[1,0,0,0],[0,1,0,0]]), S.Matrix([[1,1,1,1],[0,0,1,0],[0,0,0,1]])),
      (S.Matrix([[1,0,1],[0,1,1]]),S.Matrix([[1,1,0],[0,1,1]])),
      (S.Matrix([[1,1,0],[0,0,1]]),S.Matrix([[1,0,0],[0,1,1]])),
      (S.Matrix([[1,1,1],[0,0,0]]),S.Matrix([[1,0,1],[0,1,1]])),
      (S.Matrix([[1,0,0]]),S.Matrix([[0,1,0]])),
      (S.zeros(0,2),S.ones(1,2))]
    for A,B in pairs:
        n=A.cols;variables=S.symbols(f'w0:{n}')
        H=A*S.diag(*variables)*B.T
        common=0;generic=0
        for k in range(1,min(A.rows,B.rows,n)+1):
            if any(A[:,list(cols)].rank()==k and B[:,list(cols)].rank()==k
                   for cols in combinations(range(n),k)):
                common=k
            for rows in combinations(range(A.rows),k):
                for cols in combinations(range(B.rows),k):
                    minor=S.expand(H.extract(rows,cols).det())
                    expansion=sum(A.extract(rows,I).det()*B.extract(cols,I).det()*S.prod(variables[i] for i in I)
                                  for I in combinations(range(n),k))
                    check(group,S.expand(minor-expansion)==0,'Cauchy-Binet coefficient identity')
                    if minor!=0:generic=max(generic,k)
        check(group,generic==common,'generic rank equals maximum common independence')
        CASES[group]+=1

def main() -> None:
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,default=Path('CHECK_RESULTS.json'))
    args=parser.parse_args()
    four_point();block_family();density_chart();leja();finite_pairing_rank()
    record={
      'reviewed_commit':PIN,'python':platform.python_version(),'sympy':S.__version__,
      'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
      'all_passed':True,'cases_total':sum(CASES.values()),'explicit_checks_total':sum(COUNTS.values()),
      'groups':{k:{'cases':CASES[k],'explicit_checks':COUNTS[k]} for k in sorted(COUNTS)},
      'arithmetic':'Exact rational and symbolic; no floating-point rank thresholds.',
      'scope':'Independent finite diagnostics only. No author/repository modules imported. Not formal proof verification, exhaustive novelty research, or LaTeX/CI reproduction.'}
    args.output.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(record,indent=2))

if __name__=='__main__':
    main()
