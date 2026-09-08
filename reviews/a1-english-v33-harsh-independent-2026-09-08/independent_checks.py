#!/usr/bin/env python3
"""Independent finite diagnostics for A1 v33. Not a formal proof checker.

Run with Python 3.10+; only the standard library is used. Normal and -O
execution must give identical JSON. No assertion statements are used.
The atomic-command test is within Section 8's extended prescribed-law model,
not an enumeration of the continuous-command or worst-history optimum.
"""
from __future__ import annotations
from fractions import Fraction as F
from itertools import product, combinations
from math import comb, factorial, prod
from pathlib import Path
import hashlib
import json

BASE = 'e7dfc3a0e1c8d7a9d3be6b7f52944c5c7c59bb0c'


def check(ok: bool, message: str) -> None:
    if not ok:
        raise ArithmeticError(message)


def add(a, b):
    return tuple((a[i] if i < len(a) else F(0)) +
                 (b[i] if i < len(b) else F(0))
                 for i in range(max(len(a), len(b))))


def scale(a, c):
    return tuple(c*x for x in a)


def mul(a, b):
    out = [F(0)]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i+j] += x*y
    return tuple(out)


def power(a, n):
    z = (F(1),)
    for _ in range(n):
        z = mul(z, a)
    return z


def integral(a):
    return sum((x/F(i+1) for i, x in enumerate(a)), F(0))


def equal_poly(a, b):
    return all(x == 0 for x in add(a, scale(b, F(-1))))


def exact_example():
    # Independent integration in diamond coordinates s=X+Z, d=X-Z:
    # E[d^2 s^(2k)] = 4*(1/10)^(2k+2) / prod(2k+1,...,2k+4).
    terms = [F(4, 10**(2*k+2)*prod(range(2*k+1, 2*k+5)))
             for k in range(7)]
    a = F(1, 240)
    jk = sum(terms[:6], F(0))
    tail = F(1, 600)*F(1, 10**12)/F(99, 100)
    lo = a*a*(F(1, 12)+jk/4)
    hi = lo+a*a*tail/4
    check(lo == F(18108150189130829,12454041600000000000000), 'lower endpoint')
    check(hi == F(150901251576091,103783680000000000000), 'upper endpoint')
    check(hi-lo == F(1,136857600000000000000), 'width')
    check(lo < lo+a*a*terms[6]/4 < hi, 'next partial sum')
    k1 = (F(1,4), F(1,2))
    h2 = (F(19,40), F(1,20))
    q1 = scale(k1,F(1,2))
    q0 = add((F(1),),scale(q1,F(-1)))
    ds = [integral(mul(q,h2))/integral(q) for q in (q0,q1)]
    check(ds == [F(359,720),F(121,240)], 'centroids')
    # This checks an algebraic margin, not the continuum rearrangement proof.
    margin = F(1,2)-F(3,20)-(1+F(3,100))/4
    check(margin == F(37,400), 'tail inequality margin')
    return dict(lower=lo, upper=hi, width=hi-lo, terms=terms[:6],
                decoder_H2=ds, margin=margin,
                method='diamond-coordinate integral, not copied binomial expansion',
                continuum_global_coverage='analytical proof in referee report, not established by this script')


COMMANDS = ((F(9,20),F(11,20)), (F(11,20),F(9,20)))
NU = (F(1,3), F(2,3))
CELLS = ((F(1,4),F(1,2)), (F(3,4),F(-1,2)))


def likelihood(g, x):
    if x < 2:
        return scale(CELLS[x],g[x])
    return add(scale(CELLS[0],1-g[0]),scale(CELLS[1],1-g[1]))


def row(n, i, c, x):
    # A nontrivial rational stochastic policy, fixed in advance.
    p = F(1+(3*n+2*i+4*c+x)%9,10)
    return (1-p,p)


def support_body():
    # A deterministic rule has one binary decision for each command/report pair.
    matrices = []
    for decisions in product(range(2), repeat=6):
        a = [[F(0),F(0)] for _ in range(2)]
        for c,g in enumerate(COMMANDS):
            for k in range(2):
                a[k][decisions[3*c+k]] += NU[c]*g[k]
                a[k][decisions[3*c+2]] += NU[c]*(1-g[k])
        check(all(sum(r)==1 for r in a), 'stochastic body rows')
        overlap = sum(min(a[0][j],a[1][j]) for j in range(2))
        bound = sum(NU[c]*min(1-g[0],1-g[1]) for c,g in enumerate(COMMANDS))
        check(overlap >= bound, 'common failure overlap')
        matrices.append(a)
    m = [sum(NU[c]*g[k] for c,g in enumerate(COMMANDS)) for k in range(2)]
    for coeff in product((-1,0,1),repeat=4):
        C = (coeff[:2],coeff[2:])
        actual = max(sum(C[k][j]*a[k][j] for k in range(2) for j in range(2))
                     for a in matrices)
        formula = sum(m[k]*max(C[k]) for k in range(2)) + sum(
            NU[c]*max(sum((1-g[k])*C[k][j] for k in range(2)) for j in range(2))
            for c,g in enumerate(COMMANDS))
        check(actual == formula, 'support identity')
    return dict(deterministic_rules=64, linear_functionals=81,
                support_equalities_passed=True, overlap_lower_bound=bound,
                impossible_disjoint_rows_excluded=True,
                scope='two-atom command law, two raw cells and two retained states')


def occupancy():
    q = [(F(1),),(F(0),)]
    coeffs = [{(0,0):F(1)},{(0,0):F(0)}]
    # Each entry stores likelihood L_h(t), command probability, state law given h.
    histories = [((F(1),),F(1),(F(1),F(0)))]
    checkpoints = []
    for n in range(1,4):
        A = [[[F(0) for _ in range(2)] for _ in range(2)] for _ in range(2)]
        for i,k,j in product(range(2), repeat=3):
            A[i][k][j] = sum(NU[c]*(g[k]*row(n,i,c,k)[j] +
                                           (1-g[k])*row(n,i,c,2)[j])
                             for c,g in enumerate(COMMANDS))
        newq = [(F(0),),(F(0),)]
        newcoeff = [{},{}]
        for i,k,j in product(range(2),repeat=3):
            newq[j] = add(newq[j],scale(mul(q[i],CELLS[k]),A[i][k][j]))
            for alpha,v in coeffs[i].items():
                beta = tuple(alpha[l]+(l==k) for l in range(2))
                newcoeff[j][beta] = newcoeff[j].get(beta,F(0))+v*A[i][k][j]
        q,coeffs = newq,newcoeff
        for a in range(n+1):
            alpha=(a,n-a)
            check(sum(coeffs[j].get(alpha,F(0)) for j in range(2)) == comb(n,a),
                  'formal multinomial sum')
        for j in range(2):
            expanded=(F(0),)
            for alpha,v in coeffs[j].items():
                expanded=add(expanded,scale(mul(power(CELLS[0],alpha[0]),
                                               power(CELLS[1],alpha[1])),v))
            check(equal_poly(expanded,q[j]), 'formal expansion')
        newhist=[]
        for L,prob,z in histories:
            for c,g in enumerate(COMMANDS):
                for x in range(3):
                    zn=tuple(sum(z[i]*row(n,i,c,x)[j] for i in range(2)) for j in range(2))
                    newhist.append((mul(L,likelihood(g,x)),prob*NU[c],zn))
        histories=newhist
        # Two future failure queries, horizon N=4 and length m=4-n.
        m=4-n
        queries=(power((F(1,2),),m),power((F(19,40),F(1,20)),m))
        w=[integral(qj) for qj in q]
        b=[[integral(mul(qj,H)) for H in queries] for qj in q]
        d=[[v/w[j] if w[j] else F(0) for v in b[j]] for j in range(2)]
        q_direct=[(F(0),),(F(0),)]
        B=F(0); direct=F(0)
        for L,prob,z in histories:
            Z=integral(L)
            preds=[integral(mul(L,H))/Z for H in queries]
            B += prob*Z*sum(p*p for p in preds)/2
            for j in range(2):
                q_direct[j]=add(q_direct[j],scale(L,prob*z[j]))
                direct += prob*Z*z[j]*sum((d[j][l]-preds[l])**2 for l in range(2))/2
        for j in range(2):
            check(equal_poly(q_direct[j],q[j]), 'history-free occupancy')
        formula=B-sum(b[j][l]**2/w[j] for j in range(2) for l in range(2))/2
        check(formula==direct and direct>=0, 'mean-risk identity')
        check(sum(w)==1, 'total state mass')
        checkpoints.append(dict(stage=n, histories=len(histories), risk=direct,
                                q=q, occupancies=w))
    for denominator in (10,100,1000):
        w=F(1,denominator); b=w*F(3,7)
        check(0<=b*b/w<=w, 'perspective domination')
    return dict(checkpoints=checkpoints, exact_polynomial_equalities=True,
                independent_history_risk_equalities=True,
                zero_occupancy_extension='bound checked; continuity is analytical',
                scope='one three-stage prescribed atomic-command controller; no optimality or continuum enumeration')


def collision_flags():
    cases=((F(0),F(0)),(F(0),F(1,100)),(F(1,100),F(0)),(F(1,100),F(1,100)),
           (F(1,100),F(2,100)),(F(1,100),F(101,10000)),(F(1,100),F(3,100)))
    out=[]
    for u,v in cases:
        A=(F(0),F(1),2+u,3+v)
        nodes=[(A[i]+A[j])/20 for i in range(4) for j in range(i,4) if (i,j)!=(0,0)]
        order=[]; d=[]; todo=list(range(len(nodes)))
        while todo:
            if not order:
                chosen=min(todo,key=lambda j:(nodes[j],j)); pivot=F(1)
            else:
                scores={j:prod((abs(nodes[j]-nodes[i]) for i in order),start=F(1)) for j in todo}
                chosen=max(todo,key=lambda j:(scores[j],-j)); pivot=scores[chosen]
            order.append(chosen);todo.remove(chosen);d.append(pivot)
        check(all(d[i]>=d[i+1] for i in range(8)), 'ordered Newton scales')
        volumes=[]
        for ell in range(1,10):
            vol=max(prod((abs(nodes[i]-nodes[j]) for i,j in combinations(ids,2)),start=F(1))
                    for ids in combinations(range(9),ell))
            pd=prod(d[:ell],start=F(1))
            check(pd<=vol<=factorial(ell)*pd, 'Leja volume bounds')
            volumes.append(vol)
        rank=len(set(nodes))
        expected=6 if u==v==0 else (8 if min(abs(u),abs(v-u),abs(v-2*u))==0 else 9)
        check(rank==expected, 'two-parameter collision rank')
        out.append(dict(u=u,v=v,distinct_positive_nodes=rank,
                        all_nine_volume_bounds_passed=True))
    return dict(cases=out, scope='finite exact-rational configurations; not a proof of uniform entropy or attainment')


def encode(x):
    if isinstance(x,F):
        return f'{x.numerator}/{x.denominator}'
    raise TypeError(type(x).__name__)


def main():
    result=dict(schema='a1-v33-independent-referee-diagnostics-v1',
                manuscript_commit=BASE, arithmetic='fractions.Fraction',
                exact_example=exact_example(), support_body=support_body(),
                multistage_occupancy=occupancy(), collision_flags=collision_flags(),
                formal_proof_assistant=False, manuscript_tex_compiled=False,
                general_continuous_controller_net_enumerated=False,
                script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    print(json.dumps(result,default=encode,sort_keys=True,indent=2))


if __name__=='__main__':
    main()
