#!/usr/bin/env python3
"""Exact finite diagnostics for A2 v109. These do not certify universal proofs."""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import sympy as s


def product_matrix(U: s.Matrix) -> s.Matrix:
    """Columns of U are polynomial coefficients, lowest degree first."""
    k, c = U.shape
    rows = []
    for a in range(c):
        for b in range(a, c):
            rows.append([sum(U[i, a]*U[j, b] for i in range(k)
                             for j in range(k) if i+j == h)
                         for h in range(2*k-1)])
    return s.Matrix(rows)


def interpolation(k: int):
    t = s.symbols('t')
    roots = list(map(s.Integer, range(1, k+1)))
    clocks = list(map(s.Integer, range(k+2, 3*k+3)))
    p = s.prod(t-r for r in roots)
    h, P = s.expand(p*p), s.prod(t-u for u in clocks)
    d = [P.subs(t, r)/s.prod((r-u)**2 for u in roots if u != r)
         for r in roots]
    J = s.Matrix([[s.Poly(s.cancel(d[i]*p/(t-r)), t).nth(a)
                   for a in range(k)] for i, r in enumerate(roots)])
    return t, roots, clocks, p, h, P, d, J


def modrank(rows: list[list[int]], prime: int) -> int:
    A = [list(row) for row in rows]
    rank = 0
    for col in range(len(A[0])):
        pivot = next((i for i in range(rank,len(A)) if A[i][col] % prime),None)
        if pivot is None:
            continue
        A[rank], A[pivot] = A[pivot], A[rank]
        inv = pow(int(A[rank][col]),-1,prime)
        A[rank] = [x*inv % prime for x in A[rank]]
        for i in range(rank+1,len(A)):
            c = A[i][col]
            if c:
                A[i] = [(x-c*y) % prime for x,y in zip(A[i],A[rank])]
        rank += 1
        if rank == len(A):
            break
    return rank


def modinverse(A: list[list[int]], prime: int) -> list[list[int]]:
    n = len(A)
    B = [list(row) + [int(i==j) for j in range(n)] for i,row in enumerate(A)]
    for col in range(n):
        pivot = next(i for i in range(col,n) if B[i][col] % prime)
        B[col], B[pivot] = B[pivot], B[col]
        inv = pow(int(B[col][col]),-1,prime)
        B[col] = [x*inv % prime for x in B[col]]
        for i in range(n):
            if i != col:
                c = B[i][col]
                B[i] = [(x-c*y) % prime for x,y in zip(B[i],B[col])]
    return [row[n:] for row in B]


def modq(x: s.Rational, prime: int) -> int:
    return int(x.p)*pow(int(x.q),-1,prime) % prime


def rational_examples() -> list[dict]:
    results = []
    prime = 1000003
    assert s.isprime(prime)
    for d in (2,3,6):
        k = 3*d+2
        _,roots,clocks,_,_,_,_,J = interpolation(k)
        A = s.Matrix([[r**a for a in range(d)] for r in roots])
        N = s.Matrix.hstack(*A.T.nullspace())
        U = J.T*N
        coeff = [[modq(U[i,j],prime) for i in range(k)] for j in range(k-d)]
        rows = []
        for x in range(k-d):
            for y in range(x,k-d):
                row = [0]*(2*k-1)
                for i in range(k):
                    for j in range(k):
                        row[i+j] = (row[i+j]+coeff[x][i]*coeff[y][j]) % prime
                rows.append(row)
        rank = modrank(rows,prime)
        assert rank == 2*k-1
        # Independent route: invert the raw square score matrix over the field,
        # compress its retained columns, and never use J or multiplication.
        V = [[1]+[modq(-1/(t-r),prime) for r in roots]
                +[modq(-1/(t-r)**2,prime) for r in roots] for t in clocks]
        Z = modinverse(V,prime)[k+1:]
        NN = [[modq(N[i,a],prime) for i in range(k)] for a in range(k-d)]
        compressed = [[sum(NN[a][i]*Z[i][j] for i in range(k)) % prime
                       for j in range(2*k+1)] for a in range(k-d)]
        score_rows = [[compressed[a][j]*compressed[b][j] % prime
                       for j in range(2*k+1)] for a in range(k-d) for b in range(a,k-d)]
        score_rank = modrank(score_rows,prime)
        assert score_rank == 2*k-1
        results.append({'name':'rational global one-point example and raw-score cross-check',
                        'd':d,'k':k,'prime':prime,'product_rank_mod_prime':rank,
                        'raw_score_rank_mod_prime':score_rank,
                        'roots':'1,...,k','clocks':'k+2,...,3k+2',
                        'loadings':'A[i,l]=i**l, i=1,...,k, l=0,...,d-1',
                        'point':'q_A(e1)=(1,...,1)',
                        'global_fibre_argument':'f**2-1 has k>2(d-1) distinct roots, so f=+1 or -1'})
    return results


def run_checks() -> dict:
    checks = []
    for d in (2, 3, 6, 10):
        k = 3*d+2
        S = list(range(d+1)) + list(range(2*d+1, 3*d+2))
        U = s.eye(k)[:, S]
        sums = sorted({a+b for a in S for b in S})
        assert sums == list(range(2*k-1))
        M = product_matrix(U)
        # The rows are unit coordinate vectors, so the distinct sums give rank.
        assert len({tuple(row) for row in M.tolist()}) == 2*k-1
        ambient_nullity = (k*(k+1)-(k-d)*(k-d+1))//2
        assert ambient_nullity == 5*d*(d+1)//2
        checks.append({'name': 'monomial product coverage', 'd': d, 'k': k,
                       'native_rank': 2*k-1, 'ambient_nullity': ambient_nullity})
    assert all((3*d+2 < d*(d+1)//2) == (d >= 6) for d in range(2, 50))
    checks.append({'name': 'noninjective symmetric-measurement threshold', 'first_d': 6})

    for k in (2, 3):
        t, roots, clocks, p, h, P, d, J = interpolation(k)
        V = s.Matrix([[s.Integer(1)] + [-1/(u-r) for r in roots]
                      + [-1/(u-r)**2 for r in roots] for u in clocks])
        Z = V.inv()[k+1:, :]
        xi = [h.subs(t,u)/s.diff(P,t).subs(t,u) for u in clocks]
        explicit = s.Matrix([[xi[j]*d[i]/(u-roots[i])
                              for j,u in enumerate(clocks)] for i in range(k)])
        assert Z == explicit and J.det() != 0
        beta = [s.Rational(j+2,j+1) for j in range(len(clocks))]
        R = Z*s.diag(*beta)*Z.T
        omega = [xi[j]**2*beta[j]/p.subs(t,u)**2 for j,u in enumerate(clocks)]
        theta = [sum(w*u**a for w,u in zip(omega,clocks)) for a in range(2*k-1)]
        H = s.Matrix(k,k,lambda a,b: theta[a+b])
        assert R == J*H*J.T
        full = V.T*s.diag(*[1/b for b in beta])*V
        schur = full[k+1:,k+1:] - full[k+1:,:k+1]*full[:k+1,:k+1].inv()*full[:k+1,k+1:]
        assert schur*R == s.eye(k)
        checks.append({'name': 'native rational score inverse and Schur complement', 'k': k})

    for d in (2, 3):
        k = 3*d+2
        *_, J = interpolation(k)
        t = -J[:, d+1]
        assert all(v > 0 for v in t)
        E = list(range(d+1,2*d+1))
        S = [a for a in range(k) if a not in E]
        W = J.T.inv()[:, S]
        T = J[:, E]
        assert T.T*W == s.zeros(d,k-d)
        assert J.T*W == s.eye(k)[:, S]
        checks.append({'name': 'positive native target and exact normal-polynomial space', 'd': d})

    W = s.Matrix([[1,1],[1,2],[2,0]])
    R = s.Matrix([[5,1,0],[1,4,1],[0,1,3]])
    K, B = W.T*W, W.T*R*W
    Hessian = 2*W*B.inv()*W.T
    G = W.T*Hessian*W/2
    assert K*G.inv()*K == B
    assert G.inv() != B
    checks.append({'name': 'nonorthonormal Gram normalization and factor of two'})

    U = s.eye(4)[:, [0,1,3]]
    M = product_matrix(U)
    assert M.rank() == 6 and M*s.eye(7)[:,5] == s.zeros(M.rows,1)
    checks.append({'name': 'incomplete product space has genuine one-dimensional fibre'})

    k = 4
    theta = s.Matrix([sum(s.Integer(j)**a for j in range(1,6)) for a in range(2*k-1)])
    H = s.Matrix(k,k,lambda a,b: theta[a+b])
    delta = s.Matrix([1,-2,0,1,0,-1,2])
    D = s.Matrix(k,k,lambda a,b: delta[a+b])
    x = s.symbols('x')
    derivative = (H+x*D).inv().diff(x).subs(x,0)
    assert derivative == -H.inv()*D*H.inv()
    h, sigma = s.symbols('h sigma', positive=True)
    mean_derivative = h**2*derivative
    fisher_scalar = s.trace(mean_derivative.T*mean_derivative)/sigma**2
    assert s.cancel(fisher_scalar/h**4 - s.trace(derivative.T*derivative)/sigma**2) == 0
    checks.append({'name': 'inverse differential and fourth-power offset information'})

    checks.extend(rational_examples())
    return {'status': 'passed', 'scope': 'finite exact algebra; not universal proof or novelty certification',
            'sympy_version': s.__version__, 'check_count': len(checks), 'checks': checks}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    out = run_checks()
    out['script_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    text = json.dumps(out, indent=2, sort_keys=True)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text)
    print(text, end='')
