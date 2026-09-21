#!/usr/bin/env python3
"""Finite exact algebra checks for A2 v107; not universal theorem verification."""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import sympy as s


def run_checks() -> dict:
    passed: list[str] = []
    x, y, a = s.symbols('x y a', real=True)
    q = [x*x, y*y, (x+y)**2]
    assert s.expand((q[2]-q[0]-q[1])**2-4*q[0]*q[1]) == 0
    measurement = s.Matrix([[1,0,0],[0,0,1],[1,2,1]])
    assert measurement.det() != 0
    passed.append('synchronized quadratic cone identity and measurement injectivity')

    clocks = list(map(s.Integer, [2,3,4,5]))
    V = s.Matrix([[1,-1/(t-1),-1/t,-1/(t-1)**2] for t in clocks])
    Z = s.Matrix([[-20,240,-540,320],[-8,72,-144,80]])
    assert Z*V == s.zeros(2,2).row_join(s.eye(2))
    passed.append('four-clock retained rational inverse, including signs')

    T = s.symbols('T')
    clocks = list(map(s.Integer, range(4,11)))
    V = s.Matrix([[1,-1/(t-1),-1/(t-2),-1/t,-1/(t-1)**2,-1/(t-2)**2] for t in clocks])
    h = T*(T-1)**2*(T-2)**2
    P = s.prod(T-t for t in clocks[:6])
    sites, mult = [0,1,2], [1,2,2]
    d = [-P.subs(T,r)/(-s.cancel(h/(T-r)**mu).subs(T,r)) for r,mu in zip(sites,mult)]
    ps = s.prod(T-r for r in sites)
    E = s.Matrix([[s.expand(s.cancel(ps/(T-r))).coeff(T,i) for i in range(3)] for r in sites])
    J = s.diag(*d)*E
    Z6 = V[:6,:].inv()[3:,:]
    explicit = s.Matrix([[s.cancel(h.subs(T,t)/s.diff(P,T).subs(T,t)*d[i]/(t-sites[i])) for t in clocks[:6]] for i in range(3)])
    assert Z6 == explicit
    R6 = (V[:6,:].T*V[:6,:]).inv()[3:,3:]
    H6 = J.inv()*R6*J.inv().T
    assert s.cancel(H6[0,2]-H6[1,1]) == 0
    R7 = (V.T*V).inv()[3:,3:]
    H7 = J.inv()*R7*J.inv().T
    obstruction = s.factor(H7[0,2]-H7[1,1])
    assert obstruction == -s.Rational(473241649,108060048)
    passed.append('six-clock Cauchy inverse and seven-clock non-Hankel obstruction')

    M = s.Matrix([[t**r for t in range(1,5)] for r in range(3)])
    kernel = s.Matrix([-1,3,-3,1]); one = s.ones(4,1)
    wp, wm = one + kernel/6, one - kernel/6
    assert M*kernel == s.zeros(3,1) and M*wp == M*wm
    aj = s.Rational(105,496)
    assert sum(aj/w for w in wp) == 1 == sum(aj/w for w in wm)
    assert sum(aj/w for w in one) == s.Rational(105,124) < 1
    for w in (wp,wm):
        assert all(v > 0 for v in w)
    Y = s.symbols('Y', positive=True)
    D = s.eye(3)*54/Y**3
    moment = s.ones(1,3)
    assert s.simplify((moment*D.inv()*moment.T).inv()[0]-s.diff(9/Y,Y,2)) == 0
    passed.append('fixed-budget two-point fibre example and value Hessian identity')

    def prof(A: s.Matrix, B: s.Matrix, C: s.Matrix, xx: s.Matrix) -> s.Expr:
        values = []
        for mask in itertools.product([False,True], repeat=C.rows):
            ids = [i for i,b in enumerate(mask) if b]
            zz = s.zeros(C.rows,1)
            if ids:
                zi = -C.extract(ids,ids).inv()*B[:,ids].T*xx
                for i,v in zip(ids,zi): zz[i] = v
            grad = B.T*xx+C*zz
            if all(zz[i] >= 0 for i in ids) and all(grad[i] >= 0 for i in range(C.rows) if i not in ids):
                values.append((xx.T*A*xx+2*xx.T*B*zz+zz.T*C*zz)[0])
        assert values and all(v == values[0] for v in values)
        return values[0]

    u, v = s.Matrix([1,-1]), s.Matrix([2,-1])
    A = s.eye(2)+u*u.T+v*v.T
    trials = 0
    for av in map(s.Rational, [-2,0,1]):
        C = s.Matrix([[1,av],[av,1+av**2]])
        B = u.row_join(av*u+v)
        assert A-B*C.inv()*B.T == s.eye(2)
        for xx in (s.Matrix([i,j]) for i in range(5) for j in range(5)):
            U,Vv = (u.T*xx)[0],(v.T*xx)[0]
            expected = (xx.T*A*xx)[0]-min(U,0)**2-min(Vv,0)**2
            assert prof(A,B,C,xx) == expected
            trials += 1
    passed.append(f'chain KKT fibre: {trials} exact cone points including interval endpoints')

    u,v = s.Matrix([1,-2]),s.Matrix([-2,1]); H=u.row_join(v); S=s.eye(2)
    trials=0
    for av in [s.Rational(-1,2),s.Integer(0),s.Rational(1,2)]:
        D=s.Matrix([[1,av],[av,1]]); C=D.inv(); B=H*C; A=S+H*C*H.T
        for xx in (s.Matrix([i,j]) for i in range(5) for j in range(5)):
            U,Vv=(u.T*xx)[0],(v.T*xx)[0]
            expected=(xx.T*S*xx)[0]+max(U,0)**2+max(Vv,0)**2
            assert prof(A,B,C,xx)==expected
            trials+=1
    passed.append(f'missing-empty fork fibre: {trials} exact cone points')

    u,v=s.Matrix([-1,2]),s.Matrix([2,-1]); B=u.row_join(v); A=30*s.eye(2)
    trials=0
    for av in [s.Rational(-1,2),s.Integer(0),s.Rational(1,2)]:
        C=s.Matrix([[1,av],[av,1]])
        assert (A-B*C.inv()*B.T).is_positive_definite
        for xx in (s.Matrix([i,j]) for i in range(5) for j in range(5)):
            U,Vv=(u.T*xx)[0],(v.T*xx)[0]
            assert prof(A,B,C,xx)==(xx.T*A*xx)[0]-min(U,0)**2-min(Vv,0)**2
            trials+=1
    passed.append(f'missing-full fork fibre: {trials} exact cone points')

    xi,lam,z=s.symbols('xi lam z', real=True)
    cost=s.expand((xi**3+xi)**2+(xi**2-lam)**2)
    assert s.expand(cost-(xi**6+3*xi**4+(1-2*lam)*xi**2+lam**2))==0
    passed.append('retained v106 critical cubic cost identity')
    return {'status':'passed','scope':'finite exact algebra and examples; not universal theorem verification',
            'sympy_version':s.__version__,'checks':passed,'check_count':len(passed),
            'overidentified_obstruction':str(obstruction)}


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    result=run_checks()
    result['script_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    text=json.dumps(result,indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(text+'\n')
    print(text)
