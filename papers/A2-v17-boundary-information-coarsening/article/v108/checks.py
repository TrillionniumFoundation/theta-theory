#!/usr/bin/env python3
"""Finite exact checks of displayed v108 identities; not theorem certification."""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import sympy as s


def sym_variables(k: int):
    pairs = [(i, j) for i in range(k) for j in range(i, k)]
    variables = s.symbols(f'x0:{len(pairs)}')
    X = s.zeros(k)
    for z, (i, j) in zip(variables, pairs):
        X[i, j] = X[j, i] = z
    return X, variables, pairs


def conormal_rows(A: s.Matrix, etas: list[s.Matrix]):
    X, variables, pairs = sym_variables(A.rows)
    rows = []
    for eta in etas:
        ell = A * eta
        if any(v == 0 for v in ell):
            continue
        tangent = 2 * s.diag(*ell) * A
        basis = tangent.T.nullspace()
        vectors = basis + [u + v for u, v in itertools.combinations(basis, 2)]
        for n in vectors:
            f = (n.T * X * n)[0]
            rows.append([s.diff(f, z) for z in variables])
    return s.Matrix(rows), pairs


def run_checks() -> dict:
    passed = []
    u, v, T = s.symbols('u v T', real=True)
    q = s.Matrix([u*u, v*v, (u+v)**2])
    n = (q.diff(u)/2).cross(q.diff(v)/2)
    B = s.ones(3) - s.eye(3)
    assert (q.jacobian([u, v]).T * n).applyfunc(s.expand) == s.zeros(2, 1)
    assert s.expand((n.T*B*n)[0]) == 0
    passed.append('three-root conormal tangency and determinant ambiguity')

    roots = list(map(s.Integer, [1, 2, 3]))
    clocks = list(map(s.Integer, range(4, 11)))
    P = s.prod(T-t for t in clocks)
    d = [P.subs(T, r)/s.prod((r-rj)**2 for rj in roots if rj != r) for r in roots]
    assert d == [-45360, -40320, -1260]
    K = s.zeros(3)
    K[0, 1] = K[1, 0] = (roots[1]-roots[0])/(2*d[0]*d[1])
    K[0, 2] = K[2, 0] = -(roots[2]-roots[0])/(2*d[0]*d[2])
    K[1, 2] = K[2, 1] = (roots[2]-roots[1])/(2*d[1]*d[2])
    c = s.Matrix([d[i]/(T-roots[i]) for i in range(3)])
    assert s.factor((c.T*K*c)[0]) == 0
    tau = s.trace(K*B)
    assert tau == -s.Rational(1, 67737600)
    passed.append('native rational interpolation and nonzero transversality')

    z = s.symbols('R11 R22 R33 R12 R13 R23')
    R = s.Matrix([[z[0], z[3], z[4]], [z[3], z[1], z[5]], [z[4], z[5], z[2]]])
    normals = [n.subs({u: 1, v: j}) for j in range(1, 6)]
    M = s.Matrix([[s.diff((nn.T*R*nn)[0], zz) for zz in z] for nn in normals])
    system = M.col_join(s.Matrix([[s.diff(s.trace(K*R), zz) for zz in z]]))
    assert M.rank() == 5 and M.nullspace() == [s.Matrix([0, 0, 0, 1, 1, 1])]
    assert system.det() == -s.Rational(1, 58800)
    native = sum((c.subs(T, t)*c.subs(T, t).T for t in clocks), s.zeros(3))
    rhs = s.Matrix([(nn.T*native*nn)[0] for nn in normals] + [0])
    recovered = system.inv()*rhs
    assert recovered == s.Matrix([native[0,0],native[1,1],native[2,2],native[0,1],native[0,2],native[1,2]])
    passed.append('five directional jets: exact determinant, null line, and native recovery')

    B0 = s.Matrix([[0,1,s.Rational(37,64)],[1,0,1],[s.Rational(37,64),1,0]])
    assert s.trace(K*B0) == 0
    A0 = s.Matrix([[1,0],[0,1],[1,s.sqrt(37)/8]])
    q0 = s.Matrix([vv**2 for vv in A0*s.Matrix([u,v])])
    n0 = (q0.diff(u)/2).cross(q0.diff(v)/2)
    assert s.simplify((n0.T*B0*n0)[0]) == 0
    passed.append('nondegenerate exceptional loading with all second jets ambiguous')

    A4 = s.Matrix([[1,0],[0,1],[1,1],[1,-1]])
    rows4, pairs4 = conormal_rows(A4, [s.Matrix([1,j]) for j in [2,3,4,5,6,7]])
    B4 = s.Matrix(4,4,lambda i,j: s.det(s.Matrix([list(A4.row(i)),list(A4.row(j))]))**2)
    bv = s.Matrix([B4[i,j] for i,j in pairs4])
    assert rows4.rank() == 9 and rows4*bv == s.zeros(rows4.rows,1)
    X4, variables4, pairs4b = sym_variables(4)
    roots4 = list(map(s.Integer, range(1,5)))
    P4 = s.prod(T-tt for tt in range(6,15))
    d4 = [P4.subs(T,rr)/s.prod((rr-rj)**2 for rj in roots4 if rj!=rr) for rr in roots4]
    constraints = []
    for i,j,l in itertools.combinations(range(4),3):
        f = (j-i)*X4[i,j]/(d4[i]*d4[j])-(l-i)*X4[i,l]/(d4[i]*d4[l])+(l-j)*X4[j,l]/(d4[j]*d4[l])
        constraints.append([s.diff(f,zv) for zv in variables4])
    C4 = s.Matrix(constraints)
    assert C4.rank() == 3 and C4*bv != s.zeros(4,1)
    W4 = s.Matrix.hstack(*C4.nullspace())
    assert (rows4*W4).rank() == 7
    passed.append('four-root conormal kernel and seven-dimensional native recovery')

    A6 = s.Matrix([[1,0,0],[0,1,0],[0,0,1],[1,1,0],[1,0,1],[0,1,1]])
    etas6 = [s.Matrix([1,i,j]) for i,j in itertools.product([1,2,3], repeat=2)]
    rows6, _ = conormal_rows(A6, etas6)
    assert rows6.rank() == 21
    passed.append('three shared parameters: full rank 21 on symmetric six-dimensional metrics')

    eta = s.Matrix([1,2])
    tangent = 2*s.diag(*(A4*eta))*A4
    N = s.Matrix.hstack(*tangent.T.nullspace())
    R4 = s.diag(1,2,3,4) + s.ones(4)
    Q4 = R4.inv()
    H = Q4-Q4*tangent*(tangent.T*Q4*tangent).inv()*tangent.T*Q4
    G = N.T*N
    assert s.simplify(G.inv()*(N.T*H*N)*G.inv()*(N.T*R4*N)) == s.eye(2)
    passed.append('normal Hessian inversion in codimension two')

    moment = s.Matrix([[1,0,1],[0,1,0]])
    w1,w2 = s.Matrix([2,3,6]),s.Matrix([6,3,2])
    assert moment*w1 == moment*w2
    assert sum(1/x for x in w1) == sum(1/x for x in w2) == 1
    assert sum(1/x for x in s.Matrix([4,3,4])) == s.Rational(5,6)
    D = s.eye(3)/32
    assert (s.ones(1,3)*D.inv()*s.ones(3,1)).inv()[0] == s.Rational(1,96)
    assert s.diff(9/T,T,2).subs(T,12) == s.Rational(1,96)
    passed.append('reciprocal two-point fibre and corank-two value Hessian')

    A = 3*s.eye(2); BB=s.Matrix([1,-1]); C=s.eye(1)
    assert (A-BB*BB.T).is_positive_definite
    for x1,x2 in itertools.product(range(5),repeat=2):
        x=s.Matrix([x1,x2]); zz=max(0,x2-x1); ww=x1-x2+zz
        assert zz>=0 and ww>=0 and zz*ww==0
        value=(x.T*A*x)[0]+2*(x.T*BB)[0]*zz+zz**2
        assert value==3*(x1*x1+x2*x2)-min(0,x1-x2)**2
    passed.append('function-input KKT equality on 25 labelled points')

    return {'status':'passed','scope':'finite identities and examples; not universal theorem verification',
            'sympy_version':s.__version__,'check_count':len(passed),'checks':passed,
            'three_root_tau':str(tau),'six_equation_determinant':str(system.det())}


if __name__ == '__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path)
    args=parser.parse_args();result=run_checks()
    result['script_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    text=json.dumps(result,indent=2)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(text)
    print(text)
