#!/usr/bin/env python3
"""Exact finite controls for A2 v58; no manuscript checker is imported.
Run with Python 3: python independent_checks.py
All arithmetic is rational. The controls are not proofs of smooth,
infinite-dimensional, probabilistic, or global geometric statements.
"""
from __future__ import annotations
from fractions import Fraction as F
from math import factorial
import json


def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def mul(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    return [[sum((a[i][k]*b[k][j] for k in range(len(b))), F(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def eye(n: int) -> list[list[F]]:
    return [[F(i == j) for j in range(n)] for i in range(n)]


def norm(a: list[list[F]]) -> F:
    return max(sum(map(abs, row), F(0)) for row in a)


def geometry(t: F, eta: F) -> tuple[F, F, F, F, F]:
    c = (t + 1/t)/2
    c0 = 1 + eta*(c*c-1)
    c1 = c*c/c0
    r0, r1 = c0/c, c/c0
    require(c0 > 1 and c1 > 1 and r0*r1 == 1, 'admissibility')
    return c, c0, c1, r0, r1


def block(t: F, r0: F, r1: F, n: int) -> tuple[list, list]:
    den = 1-t**(2*n)
    a = (1+t**(2*n))/den
    b, c = 2*(r0*t)**n/den, 2*(r1*t)**n/den
    return [[a, b], [c, a]], [[a, -b], [-c, a]]


def block_controls() -> dict:
    ts = [F(1,100),F(1,10),F(1,3),F(1,2),F(2,3),F(4,5),F(9,10),F(99,100),F(999,1000)]
    etas = [F(1,1000),F(1,10),F(1,2),F(9,10),F(999,1000)]
    vectors = [[F(-3), F(2)], [F(1), F(0)], [F(0), F(1)]]
    count = vector_count = 0
    for t in ts:
        theta = (1+t*t)/2
        C, K = (3+t**6)/(1-t**6), 4/(1-t**6)
        for eta in etas:
            _, _, _, r0, r1 = geometry(t, eta)
            require(max(r0*t, r1*t) < theta < 1, 'contracting shape factors')
            source_sum = forward_sum = inverse_sum = improved_sum = F(0)
            for n in range(3,65):
                M, I = block(t,r0,r1,n)
                require(mul(M,I) == eye(2), 'explicit inverse')
                require(M[0][0]*M[1][1]-M[0][1]*M[1][0] == 1, 'determinant')
                require(max(norm(M),norm(I)) <= C, 'uniform block bound')
                DM = [[M[i][j]-F(i==j) for j in range(2)] for i in range(2)]
                DI = [[I[i][j]-F(i==j) for j in range(2)] for i in range(2)]
                require(max(norm(DM),norm(DI)) <= K*theta**n, 'identity correction')
                # Endpoint appears once; each interior site twice.
                own = 1 + 2*t**(2*n)/(1-t**(2*n))
                cross = 2*r0**n*t**n/(1-t**(2*n))
                require(own == M[0][0] and cross == M[0][1], 'visit multiplicities')
                for v in vectors:
                    w = [sum((M[i][k]*v[k] for k in range(2)),F(0)) for i in range(2)]
                    nv, nw = max(map(abs,v)), max(map(abs,w))
                    require(nv/C <= nw <= C*nv, 'fixed-lower-jet two-sided bound')
                    vector_count += 1
                if n <= 16:
                    v = [F((-1)**n,n+1), F(2,n+2)]
                    w = [sum((M[i][k]*v[k] for k in range(2)),F(0)) for i in range(2)]
                    z = [sum((I[i][k]*v[k] for k in range(2)),F(0)) for i in range(2)]
                    h = [w[i]-v[i] for i in range(2)]
                    R = F(3,2)
                    source_sum += R**n*max(map(abs,v))/factorial(n)
                    forward_sum += R**n*max(map(abs,w))/factorial(n)
                    inverse_sum += R**n*max(map(abs,z))/factorial(n)
                    improved_sum += (R/theta)**n*max(map(abs,h))/factorial(n)
                count += 1
            require(max(forward_sum,inverse_sum) <= C*source_sum, 'finite coefficient sums')
            require(improved_sum <= K*source_sum, 'correction radius gain')
    bad, bad_inv = block(F(1,2),F(4),F(1,4),12)
    bad_C = (3+F(1,2)**6)/(1-F(1,2)**6)
    require(mul(bad,bad_inv)==eye(2) and norm(bad)>bad_C, 'inadmissible negative control')
    return {'admissible_blocks':count,'two_sided_vector_checks':vector_count,
            'orders':[3,64],'coefficient_sums_orders':[3,16],
            'inadmissible_determinant_one_negative_control':True}


def jacobi_controls() -> dict:
    cases = 0
    for t in (F(1,3),F(2,3),F(9,10)):
        sinh = lambda n: (t**(-n)-t**n)/2
        for eta in (F(1,10),F(1,2),F(9,10)):
            c,c0,c1,_,_ = geometry(t,eta)
            cs = [c0,c1]
            g = F(7,5)
            for j in range(2,15):
                n = j-1
                H = [[F(0) for _ in range(n)] for _ in range(n)]
                for i in range(n):
                    H[i][i]=2*cs[(i+1)%2]/g
                    if i+1<n: H[i][i+1]=H[i+1][i]=-1/g
                G = []
                for i in range(1,j):
                    row=[]
                    for k in range(1,j):
                        a,b=min(i,k),max(i,k)
                        sigprod=cs[1-i%2] if i%2==k%2 else c
                        row.append(g*sigprod/c*sinh(a)*sinh(j-b)/(sinh(1)*sinh(j)))
                    G.append(row)
                require(mul(H,G)==eye(n), 'finite Green inverse')
                dm2,dm1=F(1),2*c1/g
                for i in range(2,j):
                    dm2,dm1=dm1,2*cs[i%2]/g*dm1-dm2/g**2
                sig0j=c1 if j%2==0 else c
                d0=c*sinh(1)/(g*sig0j*sinh(j))
                require((1/g)**j/dm1==d0, 'normalized cofactor')
                require(G[0][-1]/g**2==d0, 'mixed Schur coefficient')
                cases+=1
    return {'exact_finite_jacobi_cases':cases,'flight_lengths':[2,14]}


def density_controls() -> dict:
    S=lambda x:x*x+x**3/7+x**4/5
    Sp=lambda x:2*x+3*x*x/7+4*x**3/5
    A=lambda x:2+x+x*x
    Ap=lambda x:1+2*x
    C=lambda y:3-y+y*y
    Cp=lambda y:-1+2*y
    d=F(5)
    density=lambda x,y:A(x)*C(y)*(d-S(x)-S(y))
    ratio=lambda x,y:density(x,y)*density(F(0),F(0))/(density(x,F(0))*density(F(0),y))
    anchor=F(1,5); q=S(anchor)/(d-S(anchor))
    require(q*q==1-ratio(anchor,anchor) and q>0, 'positive scalar anchor')
    points=[F(-1,4),F(-1,7),F(0),F(1,9),F(1,4)]
    for x in points:
        tx=(1-ratio(x,anchor))/q
        require(d*tx/(1+tx)==S(x), 'signed action recovery')
        for y in points:
            H=d-S(x)-S(y)
            f=density(x,y)
            fx=(Ap(x)*H-A(x)*Sp(x))*C(y)
            fy=A(x)*(Cp(y)*H-C(y)*Sp(y))
            fxy=Ap(x)*Cp(y)*H-Ap(x)*C(y)*Sp(y)-A(x)*Cp(y)*Sp(x)
            require((fxy*f-fx*fy)/f**2==-Sp(x)*Sp(y)/H**2,'mixed log derivative')
            require(1-ratio(x,y)==S(x)*S(y)/((d-S(x))*(d-S(y))),'four-density defect')
    require(S(F(1,4)) != S(F(-1,4)), 'nonzero odd coefficient retained')
    return {'rational_density_pairs':len(points)**2,'separate_factors':True,
            'nonzero_cubic_action':True,'billiard_realization_claimed':False}


def scope_controls() -> dict:
    n=8
    L=eye(n)
    for i in range(1,n): L[i][i-1]=F(-3)
    inv=[[F(3**(i-j)) if i>=j else F(0) for j in range(n)] for i in range(n)]
    require(mul(L,inv)==eye(n) and norm(inv)==3280,'strict lower coupling')
    M=[[F(2),F(1)],[F(0),F(3)]]
    Mi=[[F(1,2),F(-1,6)],[F(0),F(1,3)]]
    lattice=[[F(2),F(1,3)],[F(1,5),F(3)]]
    require(mul(mul(lattice,M),Mi)==lattice,'nonunimodular marked reconstruction')
    return {'identity_diagonal_8_block_inverse_norm':3280,
            'triangular_example_is_abstract_not_a_billiard_counterexample':True,
            'marked_gain_determinant':6}


def main() -> dict:
    return {'status':'pass','arithmetic':'exact rational',
            'blocks':block_controls(),'jacobi':jacobi_controls(),
            'density':density_controls(),'scope':scope_controls(),
            'imports_author_checker':False,'mathematical_certification':False,
            'limits':'Finite algebra only; no certification of trace-class limits, smooth remainders, statistical risk, analytic continuation, or global rigidity.'}


if __name__=='__main__':
    print(json.dumps(main(),indent=2,sort_keys=True))
